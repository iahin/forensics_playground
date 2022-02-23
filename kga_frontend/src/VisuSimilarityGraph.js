import React, { useState, useEffect } from "react";
import { notification } from "antd";
import "./index.css";
import { Graph } from "react-d3-graph";
export default function VisuSimilarityGraph(props) {
  const myConfig = {
    nodeHighlightBehavior: true,
    node: {
      color: "lightgreen",
      size: 100,
      highlightStrokeColor: "blue",
    },
    link: {
      highlightColor: "lightblue",
    },
  };

  const onClickLink = function (source, target) {
    notification.open({
      message: "Graph Link Details",
      description: `Clicked link between ${source} and ${target}`,
      onClick: () => {
        console.log(source);
      },
    });
  };

  return props.showgraph ? (
    <Graph
      id="graph-id" // id is mandatory
      data={props.showgraph}
      config={myConfig}
      onClickLink={onClickLink}
    />
  ) : (
    "Click on a case at the left to get started."
  );
}
