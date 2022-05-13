import React, { useState, useEffect } from "react";
import { List, Button, Card, Space, Typography } from "antd";

import "antd/dist/antd.css";
import "./index.css";
import VisuSimilarityGraph from "./VisuSimilarityGraph.js";

export function Comp_HistoricalSimilarity(props) {
  const { Title } = Typography;

  const [graphdata, setGraphdata] = useState();

  const get_similarity_graph =
    "http://localhost:3004/get_similarity_graph?caseid=" +
    localStorage.getItem("caseid");

  const run_histsimilarity =
    "http://localhost:3004/run_histsimilarity?caseid=" +
    localStorage.getItem("caseid");

  //* Button Clicks
  const btRunSim = () => {
    fetch(run_histsimilarity, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => console.log(res.json()))
      .then(() => window.location.reload());
  };

  const btGetSimGraph = (key) => {
    fetch(get_similarity_graph, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        pair2caseid: key,
      }),
    })
      .then((res) => res.json())
      .then((databody) => {
        console.log(databody.message);
        setGraphdata(databody.message);
        //setData(JSON.parse(databody.message).slice(0));
      });
  };

  return (
    <div>
      <div
        style={{
          display: "flex",
          justifyContent: "flex-start",
        }}
      >
        <Typography>
          <Title>Historical Similarity</Title>
        </Typography>

        <Button style={{ margin: "10px" }} onClick={btRunSim}>
          Similar Historical Cases
        </Button>
      </div>
      <div
        style={{
          display: "flex",
          justifyContent: "flex-start",
        }}
      >
        <List
          style={{ width: "40%" }}
          size="small"
          header={<h4>Case List</h4>}
          bordered
          dataSource={props.histosims}
          renderItem={(item) => (
            <List.Item>
              <Button
                value={item}
                block
                onClick={(e) => btGetSimGraph(e.target.value)}
              >
                {item}
              </Button>
            </List.Item>
          )}
        />

        <Card
          title="Case Similarity Graph"
          style={{ width: "100%", height: "100%" }}
        >
          <VisuSimilarityGraph showgraph={graphdata}> </VisuSimilarityGraph>
        </Card>
      </div>
    </div>
  );
}

export default Comp_HistoricalSimilarity;
