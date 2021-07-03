import React, { Component } from "react";
import {
  Divider,
  List,
  message,
  Spin,
  Card,
  Row,
  Col,
  Table,
  Descriptions,
  Tag,
} from "antd";
import reqwest from "reqwest";
import { columns as uniqjCol, data as uniqueData } from "./uniqueendpointa";
const fakeDataUrl =
  "https://randomuser.me/api/?results=5&inc=name,gender,email,nat&noinfo";

class Summarydata extends React.Component {
  state = {
    data: [],
    loading: false,
    hasMore: true,
  };

  componentDidMount() {
    this.fetchData((res) => {
      this.setState({
        data: res.results,
      });
    });
  }

  fetchData = (callback) => {
    reqwest({
      url: fakeDataUrl,
      type: "json",
      method: "get",
      contentType: "application/json",
      success: (res) => {
        callback(res);
      },
    });
  };
  getDatails = (entitiyName) => {
    return (
      <div>
        <List
          size="small"
          dataSource={this.state.data}
          renderItem={(item) => <List.Item>{item[entitiyName]}</List.Item>}
        >
          {this.state.loading && this.state.hasMore && (
            <div className="demo-loading-container">
              <Spin />
            </div>
          )}
        </List>
      </div>
    );
  };
  render() {
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
        <Row gutter={16}>
          <Col span={16}>
            {/* <Table /> */}
            <Table columns={columns} dataSource={data} />
          </Col>
          <Col span={8}>
            <Card title="Case Overview">
              <Descriptions bordered size="small">
                <Descriptions.Item label="Case ID" span={4}>
                  SPF123
                </Descriptions.Item>
                <Descriptions.Item label="Status" span={2}>
                  Open
                </Descriptions.Item>
                <Descriptions.Item label="Date Created" span={2}>
                  12/03/2021
                </Descriptions.Item>
                <Descriptions.Item label="Created By" span={4}>
                  Isfaque Tuhin
                </Descriptions.Item>
                <Descriptions.Item label="Owner" span={4}>
                  Isfaque Tuhin
                </Descriptions.Item>
                <Descriptions.Item label="Case Members" span={4}>
                  Zhenlin | James
                </Descriptions.Item>
              </Descriptions>
            </Card>
          </Col>
        </Row>
        <Divider></Divider>
        <Row gutter={16}>
          <Col span={16}>
            <Card size="small" title="Critical Endpoints">
              <Table columns={uniqjCol} dataSource={uniqueData} />
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

export default Summarydata;
