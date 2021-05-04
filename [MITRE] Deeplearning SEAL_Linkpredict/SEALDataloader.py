import random
import os.path as osp
from itertools import chain
import numpy as np
from scipy.sparse.csgraph import shortest_path
import torch
import torch.nn.functional as F
from torch_geometric.data import Data, InMemoryDataset
from torch_geometric.utils import (negative_sampling, add_self_loops,
                                   train_test_split_edges, k_hop_subgraph,
                                   to_scipy_sparse_matrix)


class SEALDataset(InMemoryDataset):
    def __init__(self, dataset, num_hops, split='train', path =  osp.join(osp.dirname(osp.realpath(__file__)), '.', 'data')):
        # path = osp.join(osp.dirname(osp.realpath(__file__)),
        #                 '.', 'data')
        self.data = dataset
        self.num_hops = num_hops
        super(SEALDataset, self).__init__(path)
        index = ['train', 'val', 'test'].index(split)
        self.data, self.slices = torch.load(self.processed_paths[index])

    @property
    def processed_file_names(self):
        return ['SEAL_train_data.pt', 'SEAL_val_data.pt', 'SEAL_test_data.pt']

    def process(self):
        random.seed(12345)
        torch.manual_seed(12345)

        data = train_test_split_edges(self.data)

        edge_index, _ = add_self_loops(data.train_pos_edge_index)
        data.train_neg_edge_index = negative_sampling(
            edge_index, num_nodes=data.num_nodes,
            num_neg_samples=data.train_pos_edge_index.size(1))

        self.__max_z__ = 0

        # Collect a list of subgraphs for training, validation and test.
        train_pos_list = self.extract_enclosing_subgraphs(
            data.train_pos_edge_index, data.train_pos_edge_index, 1)
        train_neg_list = self.extract_enclosing_subgraphs(
            data.train_neg_edge_index, data.train_pos_edge_index, 0)

        val_pos_list = self.extract_enclosing_subgraphs(
            data.val_pos_edge_index, data.train_pos_edge_index, 1)
        val_neg_list = self.extract_enclosing_subgraphs(
            data.val_neg_edge_index, data.train_pos_edge_index, 0)

        test_pos_list = self.extract_enclosing_subgraphs(
            data.test_pos_edge_index, data.train_pos_edge_index, 1)
        test_neg_list = self.extract_enclosing_subgraphs(
            data.test_neg_edge_index, data.train_pos_edge_index, 0)

        # Convert labels to one-hot features.
        for data in chain(train_pos_list, train_neg_list, val_pos_list,
                          val_neg_list, test_pos_list, test_neg_list):
            data.x = F.one_hot(data.z, self.__max_z__ + 1).to(torch.float)

        torch.save(self.collate(train_pos_list + train_neg_list),
                   self.processed_paths[0])
        torch.save(self.collate(val_pos_list + val_neg_list),
                   self.processed_paths[1])
        torch.save(self.collate(test_pos_list + test_neg_list),
                   self.processed_paths[2])

    def extract_enclosing_subgraphs(self, link_index, edge_index, y):
        data_list = []
        for src, dst in link_index.t().tolist():
            sub_nodes, sub_edge_index, mapping, _ = k_hop_subgraph(
                [src, dst], self.num_hops, edge_index, relabel_nodes=True)
            src, dst = mapping.tolist()

            # Remove target link from the subgraph.
            mask1 = (sub_edge_index[0] != src) | (sub_edge_index[1] != dst)
            mask2 = (sub_edge_index[0] != dst) | (sub_edge_index[1] != src)
            sub_edge_index = sub_edge_index[:, mask1 & mask2]

            # Calculate node labeling.
            z = self.drnl_node_labeling(sub_edge_index, src, dst,
                                        num_nodes=sub_nodes.size(0))

            data = Data(x=self.data.x[sub_nodes], z=z,
                        edge_index=sub_edge_index, y=y)
            data_list.append(data)

        return data_list

    def drnl_node_labeling(self, edge_index, src, dst, num_nodes=None):
        # Double-radius node labeling (DRNL).
        src, dst = (dst, src) if src > dst else (src, dst)
        adj = to_scipy_sparse_matrix(edge_index, num_nodes=num_nodes).tocsr()

        idx = list(range(src)) + list(range(src + 1, adj.shape[0]))
        adj_wo_src = adj[idx, :][:, idx]

        idx = list(range(dst)) + list(range(dst + 1, adj.shape[0]))
        adj_wo_dst = adj[idx, :][:, idx]

        dist2src = shortest_path(adj_wo_dst, directed=False, unweighted=True,
                                 indices=src)
        dist2src = np.insert(dist2src, dst, 0, axis=0)
        dist2src = torch.from_numpy(dist2src)

        dist2dst = shortest_path(adj_wo_src, directed=False, unweighted=True,
                                 indices=dst - 1)
        dist2dst = np.insert(dist2dst, src, 0, axis=0)
        dist2dst = torch.from_numpy(dist2dst)

        dist = dist2src + dist2dst
        dist_over_2, dist_mod_2 = dist // 2, dist % 2

        z = 1 + torch.min(dist2src, dist2dst)
        z += dist_over_2 * (dist_over_2 + dist_mod_2 - 1)
        z[src] = 1.
        z[dst] = 1.
        z[torch.isnan(z)] = 0.

        self.__max_z__ = max(int(z.max()), self.__max_z__)

        return z.to(torch.long)
