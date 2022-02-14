import React, { useState } from "react";
import { Table, Button, Typography, Modal, Dropdown, Menu } from "antd";

import "antd/dist/antd.css";
import "./index.css";

function Comp_Classification() {
  const { Title } = Typography;

  const [isModalVisible, setIsModalVisible] = useState(false);

  const [state, setState] = React.useState("Unauthorised Access");

  const onClick = ({ key }) => {
    // message.info(`Click on item ${key}`);
    setState(key);
  };

  const menu = (
    <Menu onClick={onClick}>
      <Menu.Item key="Unauthorised Access">
        <a target="_blank" rel="noopener noreferrer"></a>
        Unauthorised Access
      </Menu.Item>
      <Menu.Item key="Data Theft">
        <a target="_blank" rel="noopener noreferrer"></a>
        Data Theft
      </Menu.Item>
    </Menu>
  );

  const showModal = () => {
    setIsModalVisible(true);
  };

  const handleOk = () => {
    setIsModalVisible(false);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
  };

  const columns = [
    {
      title: "Name",
      dataIndex: "name",
      key: "name",
    },
    {
      title: "Age",
      dataIndex: "age",
      key: "age",
    },
    {
      title: "Address",
      dataIndex: "address",
      key: "address",
    },
  ];

  const dataSource = [
    {
      key: "1",
      name: "Mike",
      age: 32,
      address: "10 Downing Street",
    },
    {
      key: "2",
      name: "John",
      age: 42,
      address: "10 Downing Street",
    },
  ];

  return (
    <div >
      <div style={{display: 'flex', justifyContent:'flex-start'}}>
      
      <Typography>
          <Title>Classification</Title>
      </Typography>
      
      <Button style={{margin: '10px'}} onClick={showModal}>
      Improve
      </Button>
      
      </div>
      
       <Modal title="Basic Modal" visible={isModalVisible} onOk={handleOk} onCancel={handleCancel}>
         <Typography>
          <Title level={5}>Select the appropriate classification for this case.</Title>
      </Typography>

      <Dropdown overlay={menu} placement="bottomCenter" >
          <Button style={{width: "100%", textAlign: 'left'}}>{state}</Button>
      </Dropdown>

      </Modal>

      <Table
      columns={columns}
      dataSource={dataSource}
      pagination={false}
      bordered
      scroll={{ y: 240 }}
    />
    </div>
    
  );
}

export default Comp_Classification;
