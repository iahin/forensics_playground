import { Button, PageHeader, Row, Col } from "antd";
import { SearchOutlined } from "@ant-design/icons";
import GraphSpace from "./Visualisation.GraphSpace";

function Visualisation() {
  return (
    <div>
      <div className="site-page-header-ghost-wrapper">
        <PageHeader
          ghost={false}
          title="Visualisation"
          subTitle="Graph browser for queries."
          extra={[]}
        ></PageHeader>
      </div>
      <div style={{ margin: "20px" }}>
        <GraphSpace />
      </div>
    </div>
  );
}

export default Visualisation;
