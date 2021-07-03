import { Button, PageHeader } from "antd";
import { SearchOutlined } from "@ant-design/icons";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Summarydata from "./components/Home.Summarydata";
import QuerySearch from "./components/QuerySearch";
import Visualisation from "./components/Visualisation";
import Discovery from "./components/Discovery";

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/querysearch" component={QuerySearch} />
          <Route path="/visualisation" component={Visualisation} />
          <Route path="/discovery" component={Discovery} />
        </Switch>
      </div>
    </Router>
  );
}

const Home = () => (
  <div>
    <div className="site-page-header-ghost-wrapper">
      <PageHeader
        ghost={false}
        title="Analytics"
        subTitle="Knowledge Graph Intelligence and Insights."
        extra={[
          <Button
            key="1"
            type="primary"
            icon={<SearchOutlined />}
            href="http://localhost:3000/querysearch"
          >
            Query
          </Button>,
        ]}
      ></PageHeader>
    </div>
    <div style={{ margin: "20px" }}>
      <Summarydata />
      {/* <Emptydata /> */}
    </div>
  </div>
);

export default App;
