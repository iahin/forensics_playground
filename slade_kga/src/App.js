import React, { useState } from "react";

import { Statistic, Row, Col, Button, PageHeader, Badge, Card } from "antd";
import "antd/dist/antd.css";
import "./index.css";

import Graphcomp from "./Graphcomp";

function App() {
  return (
    <div
      style={{
        paddingTop: "20px",
        paddingLeft: "20px",
      }}
    >
      <PageHeader
        className="site-page-header"
        title="Analytics Report"
        subTitle="Knowledge Graph Analytics"
        style={{ fontSize: "30" }}
      />

      <div
        style={{
          paddingTop: "20px",
          paddingLeft: "20px",
          display: "flex",
          alignItems: "center",
          justifyContent: "left",
        }}
        className="site-card-border-less-wrapper"
      >
        <Row gutter={16}>
          <Col span={4}>
            <Card
              title="Cybercrime Classification"
              bordered={false}
              style={{ width: 300 }}
            >
              <p>Card content</p>
              <p>Card content</p>
              <p>Card content</p>
            </Card>
          </Col>
        </Row>
      </div>
    </div>
  );
}

export default App;
