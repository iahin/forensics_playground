//Component Ref: https://ant.design/components/overview/
//Wireframe: https://app.mockplus.com/rp/editor/kEuKGbhU1vn/JCyEp3vGEA

import React, { useState, useEffect } from "react";

import { Button, PageHeader, Dropdown, Menu, Table, Typography } from "antd";
import "antd/dist/antd.css";
import "./index.css";

import Comp_CaseDetails from "./Comp_CaseDetails.js";
import Comp_Classification from "./Comp_Classification.js";
import Comp_EventTimeline from "./Comp_EventTimeline.js";
import Comp_GraphInsight from "./Comp_GraphInsight.js";
import Comp_HistoricalSimilarity from "./Comp_HistoricalSimilarity.js";

function App() {
  const { Title } = Typography;

  const [loading, setLoading] = React.useState(true);
  const [data, setData] = React.useState();
  const [histodata, setHistodata] = React.useState();

  const apiurl = "http://localhost:3004/get_caseidlist";

  const get_histsimilarity =
    "http://localhost:3004/get_histsimilarity?caseid=" +
    localStorage.getItem("caseid");

  useEffect(() => {
    //get case ids
    fetch(apiurl)
      .then((results) => results.json())
      .then((databody) => {
        setData(databody.message);
        setLoading(false);
      })
      //get historical sim array
      .then(
        fetch(get_histsimilarity)
          .then((res) => {
            if (res.ok) {
              return res.json();
            } else {
              throw new Error("Something went wrong");
            }
          })
          .then((databody) => {
            setHistodata(databody.message);
          })
          .catch((error) => console.log(error))
      );
  }, []);

  const onClick = ({ key }) => {
    localStorage.setItem("caseid", key);
    window.location.reload();
  };

  const menu = (
    <Menu onClick={onClick}>
      {loading
        ? "Loading..."
        : data.map((item) => (
            <Menu.Item key={item}>
              <a target="_blank" rel="noopener noreferrer"></a>
              {item}
            </Menu.Item>
          ))}
    </Menu>
  );

  return (
    <div className="sub-body">
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginLeft: "30px",
          marginTop: "20px",
        }}
      >
        <div style={{ display: "flex", justifyContent: "flex-start" }}>
          <Typography>
            <Title level={2}>Case Analysis</Title>
          </Typography>

          <Dropdown overlay={menu} placement="bottomCenter">
            <Button style={{ marginTop: "8px", marginLeft: "20px" }}>
              {localStorage.getItem("caseid")
                ? localStorage.getItem("caseid")
                : "Select Case"}
            </Button>
          </Dropdown>
        </div>

        <div>
          <Button
            style={{
              marginRight: "10px",
              marginTop: "20px",
            }}
          >
            Generate Report
          </Button>
          <Button
            type="primary"
            style={{
              marginRight: "30px",
              marginTop: "20px",
            }}
          >
            Close Case
          </Button>
        </div>
      </div>

      <div className="site-card-border-less-wrapper">
        <Typography>
          <Title>Case Details</Title>
        </Typography>
        <Comp_CaseDetails />
      </div>

      <div className="site-card-border-less-wrapper">
        <Comp_Classification />
      </div>

      <div className="site-card-border-less-wrapper">
        {histodata ? (
          <Comp_HistoricalSimilarity histosims={histodata} />
        ) : (
          "Loading..."
        )}
      </div>

      {/* <div className="site-card-border-less-wrapper">
        <Typography>
          <Title>Event Timeline</Title>
        </Typography>
      </div> */}

      <div className="site-card-border-less-wrapper">
        <Typography>
          <Title>Knowledge Graph Insights</Title>
        </Typography>
        TO BE ADDED
      </div>
    </div>
  );
}

export default App;
