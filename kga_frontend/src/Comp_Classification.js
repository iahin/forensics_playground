import React, { useState, useEffect } from "react";
import { Table, Button, Typography, Modal, Dropdown, Menu } from "antd";

import "antd/dist/antd.css";
import "./index.css";

function Comp_Classification() {
  const { Title } = Typography;

  const [isModalVisible, setIsModalVisible] = useState(false);
  const [state, setState] = React.useState("Click here to select an option");
  const [loading, setLoading] = React.useState(true);
  const [data, setData] = React.useState([]);
  const [lastlabel, setLastlabel] = React.useState("");

  const get_classification_result_apiurl =
    "http://localhost:3004/get_classification_result?caseid=" +
    localStorage.getItem("caseid");

  const post_classification_result_apiurl =
    "http://localhost:3004/post_classification_result?caseid=" +
    localStorage.getItem("caseid");

  const run_prediction =
    "http://localhost:3004/run_prediction?caseid=" +
    localStorage.getItem("caseid");

  //* First page load
  useEffect(() => {
    fetch(get_classification_result_apiurl)
      .then((res) => {
        if (res.ok) {
          return res.json();
        } else {
          throw new Error("Something went wrong");
        }
      })
      .then((databody) => {
        console.log(databody.message);
        setData(databody.message);
        //to get the last predicted label

        setLastlabel(
          databody.message[databody.message.length - 1].MacClassification
        );

        setLoading(false);
      })
      .catch((error) => console.log(error));
  }, []);

  //* Button Clicks
  const lblsendapi = () => {
    fetch(post_classification_result_apiurl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        userlabel: state,
        user: localStorage.getItem("caseUser"),
      }),
    })
      .then((res) => console.log(res.json()))
      .then(() => window.location.reload());
  };

  const runpredict = () => {
    fetch(run_prediction)
      .then((res) => res.json())
      .then((databody) => {
        console.log(databody.message);
        //setData(JSON.parse(databody.message).slice(0));
      })
      .then((rel) => window.location.reload())
      .catch((error) => console.log(error));
  };

  //* Popup click events
  const lblselect_onClick = ({ key }) => {
    setState(key);
  };

  function renderlabellogic(param) {
    switch (param) {
      case "Unauthorized Access":
        return [
          <Menu.Item key="Data Theft">
            <a target="_blank" rel="noopener noreferrer"></a>
            Data Theft
          </Menu.Item>,
          <Menu.Item key="Unknown">
            <a target="_blank" rel="noopener noreferrer"></a>
            Unknown
          </Menu.Item>,
        ];
      case "Data Theft":
        return [
          <Menu.Item key="Unauthorised Access">
            <a target="_blank" rel="noopener noreferrer"></a>
            Unauthorised Access
          </Menu.Item>,
          <Menu.Item key="Unknown">
            <a target="_blank" rel="noopener noreferrer"></a>
            Unknown
          </Menu.Item>,
        ];
      default:
        return [
          <Menu.Item key="Unauthorised Access">
            <a target="_blank" rel="noopener noreferrer"></a>
            Unauthorised Access
          </Menu.Item>,
          <Menu.Item key="Data Theft">
            <a target="_blank" rel="noopener noreferrer"></a>
            Data Theft
          </Menu.Item>,
        ];
    }
  }

  //! Logic: if prediction is Unauth, drop to have other labels as cannot be same as what is predicted.
  const menu = (
    <Menu onClick={lblselect_onClick}>{renderlabellogic(lastlabel)}</Menu>
  );

  const showModal = () => {
    setIsModalVisible(true);
  };

  const handleOk = () => {
    lblsendapi();
    setIsModalVisible(false);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
  };

  //* Table data
  const columns = [
    {
      title: "Time",
      dataIndex: "key",
      key: "key",
    },
    {
      title: "Machine Classification",
      dataIndex: "MacClassification",
      key: "MacClassification",
    },
    {
      title: "Score ",
      dataIndex: "Satfac",
      key: "Satfac",
    },
    {
      title: "User Correction",
      dataIndex: "UserCor",
      key: "UserCor",
    },
    {
      title: "User",
      dataIndex: "user",
      key: "user",
    },
  ];

  //* Render
  return (
    <div>
      <div style={{ display: "flex", justifyContent: "flex-start" }}>
        <Typography>
          <Title>Classification</Title>
        </Typography>

        {lastlabel ? (
          <Button style={{ margin: "10px" }} onClick={showModal}>
            Expert Correction
          </Button>
        ) : (
          ""
        )}
      </div>

      <Modal
        title="Expert Correction"
        visible={isModalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
      >
        <Typography>
          <Title level={5}>
            Please select a label to correct the classification.
          </Title>
        </Typography>

        <Dropdown overlay={menu} placement="bottomCenter">
          <Button style={{ width: "100%", textAlign: "left" }}>{state}</Button>
        </Dropdown>
      </Modal>

      {data.length > 0 ? (
        <Table
          columns={columns}
          dataSource={data}
          pagination={false}
          bordered
          scroll={{ y: 240 }}
        />
      ) : (
        <div>
          No classification found, click on Run Classification button to start.
          <Button style={{ margin: "10px" }} onClick={runpredict}>
            Run Classification
          </Button>
        </div>
      )}
    </div>
  );
}

export default Comp_Classification;
