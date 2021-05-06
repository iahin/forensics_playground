import { Graph } from "react-d3-graph";
import { Button, PageHeader, Row, Col, Divider, Checkbox } from "antd";
import KeySearch from "./Home.KeySearch";
// graph payload (with minimalist structure)

function onChange(checkedValues) {
  console.log("checked = ", checkedValues);
}

const plainOptions = ["Process", "File", "IPAddress"];
const options = [
  { label: "Process", value: "Process" },
  { label: "File", value: "File" },
  { label: "IPAddress", value: "IPAddress" },
];
const optionsWithDisabled = [
  { label: "Process", value: "Process" },
  { label: "File", value: "File" },
  { label: "IPAddress", value: "IPAddress", disabled: false },
];

const data = {
  nodes: [{ id: "Harry" }, { id: "Sally" }, { id: "Alice" }],
  links: [
    { source: "Harry", target: "Sally" },
    { source: "Harry", target: "Alice" },
  ],
};
// the graph configuration, just override the ones you need
const myConfig = {
  nodeHighlightBehavior: true,
  node: {
    color: "lightgreen",
    size: 120,
    highlightStrokeColor: "blue",
  },
  link: {
    highlightColor: "lightblue",
  },
};

const onClickNode = function (nodeId) {
  window.alert(`Clicked node ${nodeId}`);
};

const onClickLink = function (source, target) {
  window.alert(`Clicked link between ${source} and ${target}`);
};
function GraphSpace() {
  const style = {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  };
  return (
    <div style={style}>
      <Graph
        id="graph-id" // id is mandatory
        data={data}
        config={myConfig}
        onClickNode={onClickNode}
        onClickLink={onClickLink}
      />

      <div>
        <Divider orientation="center">Keyword Search</Divider>
        <KeySearch />
        <Divider orientation="center">Node Type Visibility</Divider>
        <Checkbox.Group
          options={plainOptions}
          defaultValue={["IPAddress"]}
          onChange={onChange}
        />
        <Divider orientation="center">Link Type Visibility</Divider>
        <Checkbox.Group
          options={options}
          defaultValue={["IPAddress"]}
          onChange={onChange}
        />
        <Divider orientation="center">Details</Divider>
      </div>
    </div>
  );
}

export default GraphSpace;
