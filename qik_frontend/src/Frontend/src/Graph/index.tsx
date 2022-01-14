import React, { useEffect, useRef, useState } from "react";
import {
  DataSet,
  Network,
  Options,
  Data,
} from "vis-network/standalone/esm/vis-network";
import axios from 'axios';

export const KnowledgeGraph = () => {
  // A reference to the div rendered by this component
  const domNode = useRef<HTMLDivElement>(null);

  // A reference to the vis network instance
  const network = useRef<Network | null>(null);

  const [dataToDisplay, setData] = useState('');
  const [edgesDataState, setEdges] = useState([]);
  const [nodesDataState, setNodes] = useState([]);
  const [graphDataState, setGraph] = useState({});
  const [loaded, setLoaded] = useState(0);

  if(edgesDataState.length == 0 && nodesDataState.length == 0 && loaded == 0){
    console.log('i am in')

    let graph = {};

    var params = window.location.search;
    if(params != ''){

      axios.get('/api/Repo/RetrieveOne'+params)
      .then(res => {
        var data = res.data.nodesData;
        graph = Object.values(JSON.parse(data))[0];
        setGraph(Object.values(JSON.parse(data))[0])

        let edgesData = [];
        let nodesData = [];
        
        for (let GraphData of Object.values(Object.values(JSON.parse(data))[0])) {
          
          if(GraphData['type'] === 'link'){
                var tempObject = {id: GraphData['id'], label: GraphData['t'], to: GraphData['id2'], from: GraphData['id1']};
                edgesData.push(tempObject)
              }
              else if(GraphData['type'] === 'node'){
                var nodeObject = {id: GraphData['id'], label: GraphData['t']};
                nodesData.push(nodeObject)
              }
          }

        setEdges(edgesData);
        setNodes(nodesData);

      })
      .catch((error) => {
        console.log(error)
      });
    }

    setLoaded(1);
  }
  
  var nodes = new DataSet(nodesDataState)
  var edges = new DataSet(edgesDataState)

  const data: Data = {
    nodes,
    edges,
  };

  const processOnClick = function (edgeClicked: string | any[], nodesClicked: string | any[]) {
    console.log(edgeClicked, nodesClicked)

    var everything = "";

    for(var i = 0; i < edgeClicked.length; i++){
      everything = everything + "id: " + edgesDataState[i]['id'] + " label : " + edgesDataState[i]['label'] + " \n "
    }
    for(var i = 0; i < nodesClicked.length; i++){
      everything = everything + "id: " + nodesDataState[i]['id'] + " label : " + nodesDataState[i]['label'] + " \n "
    }
    setData(everything)
  }

  const options: Options = {height: "450px"};

  useEffect(() => {
  if (domNode.current) {
    network.current = new Network(domNode.current, data, options);
    network.current.on
    ("click", event => {
      processOnClick(event.edges, event.nodes);
    });
  }
  }, [domNode, network, data, options]);

  return (
    <div>
      <div ref={domNode}/>
    <div className='new-line'>
      {dataToDisplay}
    </div>
    </div>
  );
};

export default KnowledgeGraph;
