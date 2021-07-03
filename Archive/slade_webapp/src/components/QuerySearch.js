import React, { Component } from "react";
import SavedQuery from "./QuerySearch.SavedQuery";
import { Query, Builder, Utils as QbUtils } from "react-awesome-query-builder";
import "react-awesome-query-builder/lib/css/styles.css";
import AntdConfig from "react-awesome-query-builder/lib/config/antd";
import "react-awesome-query-builder/css/antd.less";
import { Button, PageHeader } from "antd";
import { SearchOutlined } from "@ant-design/icons";

const InitialConfig = AntdConfig;

const data = {
  qty: {
    label: "Qty",
    type: "number",
    fieldSettings: {
      min: 0,
    },
    valueSources: ["value"],
    preferWidgets: ["number"],
  },
  price: {
    label: "Price",
    type: "number",
    valueSources: ["value"],
    fieldSettings: {
      min: 10,
      max: 100,
    },
    preferWidgets: ["slider", "rangeslider"],
  },
  color: {
    label: "Color",
    type: "select",
    valueSources: ["value"],
    fieldSettings: {
      listValues: [
        { value: "yellow", title: "Yellow" },
        { value: "green", title: "Green" },
        { value: "orange", title: "Orange" },
      ],
    },
  },
  is_promotion: {
    label: "Promo?",
    type: "boolean",
    operators: ["equal"],
    valueSources: ["value"],
  },
};

const config = {
  ...InitialConfig,
  fields: data,
};

// You can load query value from your backend storage (for saving see `Query.onChange()`)
const queryValue = { id: QbUtils.uuid(), type: "group" };

class QuerySearch extends Component {
  state = {
    tree: QbUtils.checkTree(QbUtils.loadTree(queryValue), config),
    config: config,
  };

  render() {
    return (
      <div>
        <div className="site-page-header-ghost-wrapper">
          <PageHeader
            ghost={false}
            title="Query Builder"
            subTitle="Customise query for visualisation."
            extra={[]}
          ></PageHeader>
        </div>
        <Query
          {...config}
          value={this.state.tree}
          onChange={this.onChange}
          renderBuilder={this.renderBuilder}
        />
        {/* {this.renderResult(this.state)} */}
        <SavedQuery />
      </div>
    );
  }

  renderBuilder = (props) => (
    <div className="query-builder-container" style={{ padding: "10px" }}>
      <div className="query-builder qb-lite">
        <Builder {...props} />
      </div>
    </div>
  );

  renderResult = ({ tree: immutableTree, config }) => (
    <div className="query-builder-result">
      <div>
        Query string:{" "}
        <pre>{JSON.stringify(QbUtils.queryString(immutableTree, config))}</pre>
      </div>
      <div>
        MongoDb query:{" "}
        <pre>
          {JSON.stringify(QbUtils.mongodbFormat(immutableTree, config))}
        </pre>
      </div>
      <div>
        SQL where:{" "}
        <pre>{JSON.stringify(QbUtils.sqlFormat(immutableTree, config))}</pre>
      </div>
      <div>
        JsonLogic:{" "}
        <pre>
          {JSON.stringify(QbUtils.jsonLogicFormat(immutableTree, config))}
        </pre>
      </div>
    </div>
  );

  onChange = (immutableTree, config) => {
    // Tip: for better performance you can apply `throttle` - see `examples/demo`
    this.setState({ tree: immutableTree, config: config });

    const jsonTree = QbUtils.getTree(immutableTree);
    console.log(jsonTree);
    // `jsonTree` can be saved to backend, and later loaded to `queryValue`
  };
}

export default QuerySearch;
