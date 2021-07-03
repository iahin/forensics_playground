import {
  Button,
  PageHeader,
  Table,
  Tabs,
  Descriptions,
  Tag,
  Badge,
  Row,
  Col,
  Card,
  Timeline,
} from "antd";
import { SearchOutlined } from "@ant-design/icons";
import React from "react";

function Discovery() {
  const { TabPane } = Tabs;
  //Data template
  const columns = [
    {
      title: "Crime Predicted",
      dataIndex: "crime",
      key: "crime",
      render: (text) => <a href="http://localhost:3000/discovery">{text}</a>,
    },
    {
      title: "Likelihood",
      dataIndex: "likelihood",
      key: "likelihood",
    },
    {
      title: "Discovery Date",
      dataIndex: "date",
      key: "date",
    },
  ];

  const data = [
    {
      key: "1",
      crime: "Unauthorised Access",
      likelihood: "78.64%",
      date: "12 March 2021",
    },
  ];
  return (
    <div>
      <div className="site-page-header-ghost-wrapper">
        <PageHeader
          ghost={false}
          title="Potential Discovery"
          subTitle="Generated insights based on knowledge graph."
          extra={[]}
        ></PageHeader>
      </div>
      <Row>
        <Col flex={8}>
          <div className="card-container">
            <Tabs type="card">
              <TabPane tab="Details" key="1">
                <Descriptions bordered size="small">
                  <Descriptions.Item label="Crime Identified" span={4}>
                    Unauthorised Access
                  </Descriptions.Item>
                  <Descriptions.Item label="Likelyhood" span={2}>
                    <Tag color="#f54">78.46%</Tag>
                  </Descriptions.Item>
                </Descriptions>
              </TabPane>
              <TabPane tab="Indicators" key="2">
                <Table columns={columns} dataSource={data} />
              </TabPane>
              <TabPane tab="Timeline" key="3">
                <Timeline mode="left">
                  <Timeline.Item label="2015-09-01">
                    Create a services
                  </Timeline.Item>
                  <Timeline.Item label="2015-09-01 09:12:11">
                    Solve initial network problems
                  </Timeline.Item>
                  <Timeline.Item>Technical testing</Timeline.Item>
                  <Timeline.Item label="2015-09-01 09:12:11">
                    Network problems being solved
                  </Timeline.Item>
                </Timeline>
              </TabPane>
              <TabPane tab="Visualisation" key="4"></TabPane>
            </Tabs>
          </div>
        </Col>
        <Col flex={2}>
          <Card title="Data Summary">
            <Descriptions bordered size="small">
              <Descriptions.Item label="Case ID" span={4}>
                SPF123
              </Descriptions.Item>
              <Descriptions.Item label="Evidence types" span={4}>
                Logs, Forensics Image, Registry
              </Descriptions.Item>
              <Descriptions.Item label="Total Ingestion" span={4}>
                394,558
              </Descriptions.Item>
              <Descriptions.Item label="Total Data Size" span={4}>
                88 Gb
              </Descriptions.Item>
              <Descriptions.Item label="Last file added" span={4}>
                Host123USer6.evtx
              </Descriptions.Item>
            </Descriptions>
          </Card>
        </Col>
      </Row>
    </div>
  );
}

export default Discovery;
