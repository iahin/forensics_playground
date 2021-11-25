import torch.nn as nn
import math
import torch


class SCNN(nn.ModuleList):
    """
    Explanation: https://towardsdatascience.com/text-classification-with-cnns-in-pytorch-1113df31e79f
    """

    def __init__(self, embedding_dim, hidden_size, output_size):
        super(SCNN, self).__init__()

        self.seq_len = 1
        self.embedding_size = embedding_dim
        self.hiddendim = hidden_size
        self.out_size = output_size

        self.stride = 1
        self.kernel_1 = 1
        self.kernel_2 = 1

        self.conv_1 = nn.Conv1d(self.seq_len, self.hiddendim,
                                self.kernel_1, self.stride)
        self.conv_2 = nn.Conv1d(self.seq_len, self.hiddendim,
                                self.kernel_2, self.stride)

        self.pool_1 = nn.MaxPool1d(self.kernel_1, self.stride)
        self.pool_2 = nn.MaxPool1d(self.kernel_2, self.stride)

        self.fc1 = nn.Linear(self.in_features_fc(), self.out_size)

        self.bn1 = nn.BatchNorm1d(self.hiddendim)
        self.bn2 = nn.BatchNorm1d(self.hiddendim)
        self.dropout = nn.Dropout(p=0.25)
        self.ln1 = nn.LayerNorm(self.in_features_fc())

    def in_features_fc(self):
        out_conv_1 = ((self.embedding_size - 1 *
                       (self.kernel_1 - 1) - 1) / self.stride) + 1
        out_conv_1 = math.floor(out_conv_1)
        out_pool_1 = (
                             (out_conv_1 - 1 * (self.kernel_1 - 1) - 1) / self.stride) + 1
        out_pool_1 = math.floor(out_pool_1)

        out_conv_2 = ((self.embedding_size - 1 *
                       (self.kernel_2 - 1) - 1) / self.stride) + 1
        out_conv_2 = math.floor(out_conv_2)
        out_pool_2 = (
                             (out_conv_2 - 1 * (self.kernel_2 - 1) - 1) / self.stride) + 1
        out_pool_2 = math.floor(out_pool_2)

        return (out_pool_1 + out_pool_2) * self.hiddendim

    def forward_once(self, x):
        x1 = self.conv_1(x)
        X1 = self.bn1(x1)
        x1 = torch.relu(x1)
        x1 = self.pool_1(x1)

        x2 = self.conv_2(x)
        x2 = self.bn2(x2)
        x2 = torch.relu((x2))
        x2 = self.pool_2(x2)

        union = torch.cat((x1, x2), 2)
        union = union.reshape(union.size(0), -1)

        return union

    def forward(self, input1, input2):
        h1 = self.forward_once(input1)
        h2 = self.forward_once(input2)
        out = torch.abs(h1 - h2)
        out = self.fc1(out)
        out = self.dropout(out)
        out = torch.sigmoid(out)

        return out
