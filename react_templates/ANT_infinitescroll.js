import React, { Component } from "react";
import {
  List,
  message,
  Avatar,
  Spin,
  Table,
  Typography,
  Card,
  Input,
  Row,
  Col,
  Empty,
  Button,
  Space,
} from "antd";
import InfiniteScroll from "react-infinite-scroller";
import reqwest from "reqwest";
const fakeDataUrl =
  "https://randomuser.me/api/?results=10&inc=name,gender,email,nat&noinfo";

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

  handleInfiniteOnLoad = () => {
    let { data } = this.state;
    this.setState({
      loading: true,
    });
    if (data.length > 14) {
      message.warning("Infinite List loaded all");
      this.setState({
        hasMore: false,
        loading: false,
      });
      return;
    }
    this.fetchData((res) => {
      data = data.concat(res.results);
      this.setState({
        data,
        loading: false,
      });
    });
  };

  render() {
    const infiniteScroll = (
      <div className="demo-infinite-container">
        <InfiniteScroll
          initialLoad={false}
          pageStart={0}
          loadMore={this.handleInfiniteOnLoad}
          hasMore={!this.state.loading && this.state.hasMore}
          useWindow={false}
        >
          <List
            dataSource={this.state.data}
            renderItem={(item) => (
              <List.Item key={item.id}>
                <List.Item.Meta title={item.name.last} />
              </List.Item>
            )}
          >
            {this.state.loading && this.state.hasMore && (
              <div className="demo-loading-container">
                <Spin />
              </div>
            )}
          </List>
        </InfiniteScroll>
      </div>
    );

    const intelObservables = <div className="site-card-wrapper"></div>;
    return (
      <div>
        <p>Contians the discovered intelligence from evidence data.</p>
        <Row gutter={16}>
          <Col span={8}>
            <Card size="small" title="Host">
              {infiniteScroll}
            </Card>
          </Col>
          <Col span={8}>
            <Card size="small" title="Users">
              {infiniteScroll}
            </Card>
          </Col>
          <Col span={8}>
            <Card size="small" title="IP Address">
              {infiniteScroll}
            </Card>
          </Col>
        </Row>

        <Row gutter={16}>
          <Col span={12}>
            <Card size="small" title="Host">
              {infiniteScroll}
            </Card>
          </Col>
          <Col span={12}>
            <Card size="small" title="Users">
              {infiniteScroll}
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

export default Summarydata;
