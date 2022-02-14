import React, { useState, useEffect } from "react";
import { List,Button, Card,Space } from "antd";

import "antd/dist/antd.css";
import "./index.css";
import image from './historical_sim.png';

function Comp_HistoricalSimilarity() {

  const data = [
  'SPF1', 'SPF2', 'SPF3', 'SPF4', 'SPF5', 'SPF6'
];

  
  return (
    <div style={{display: 'flex', justifyContent:'flex-start'}} >

    <List 
      style={{width:'40%'}}
      size="small"
      header={<div>Case Id</div>}
      bordered
      dataSource={data}
      renderItem={item => <List.Item>
        <Button block >{item}</Button>
        </List.Item>}
    />


    <div >
      
      <Card 
      title="Case Similarity Graph">

        <img style={{width:'80%'}} src={ image } alt="image not found" />

    </Card>
      
    </div>
    </div>
    
  );
}

export default Comp_HistoricalSimilarity;
