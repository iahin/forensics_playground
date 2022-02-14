import React, { useState, useEffect } from "react";
import { Descriptions } from "antd";

import "antd/dist/antd.css";
import "./index.css";

function Comp_CaseDetails() {

  const [loading, setLoading] = React.useState(true);

  const [data, setData] = React.useState();
  
  const apiurl = "http://localhost:3004/get_casedetails?caseid=" + localStorage.getItem('caseid')
  
  async function getdata(url) {
        fetch(url)
        .then(results => results.json())
        .then(databody=> {
          console.log(databody.message)
          setData(databody.message)
          setLoading(false)
        })
      }

  useEffect(() => {
    getdata(apiurl);
  }, []);

  
  // if (props.caseid !== "Select Case"){
  //   getdata(apiurl)
  // }else{

  // }

  return (
    <Descriptions bordered>

      <Descriptions.Item label="Case Name">{loading ? 'Loading...' : `${data.CaseName}`}
      </Descriptions.Item>

      <Descriptions.Item span={2}label="Suspected Crimetype">{loading ? 'Loading...' : `${data.CrimeType}`}
      </Descriptions.Item>

      <Descriptions.Item span={1} label="Status">{loading ? 'Loading...' : `${data.Status}`}
      </Descriptions.Item>
      
      <Descriptions.Item span={1}label="Create Time">{loading ? 'Loading...' : `${data.CreateTime}`}
      </Descriptions.Item>

      <Descriptions.Item span={1}label="Priority">{loading ? 'Loading...' : `${data.Priority}`}
      </Descriptions.Item>


      <Descriptions.Item span={3} label="Case Description">{loading ? 'Loading...' : `${data.CaseDesc}`}
      </Descriptions.Item>

      <Descriptions.Item span={1}label="Creator">{loading ? 'Loading...' : `${data.Creator}`}
      </Descriptions.Item>

       <Descriptions.Item span={2}label="Assignee">{loading ? 'Loading...' : `${data.Assignee}`}
      </Descriptions.Item>

      <Descriptions.Item span={1}label="Close Time">{loading ? 'Loading...' : `${data.CloseTime}`}
      </Descriptions.Item>

      <Descriptions.Item span={1}label="Close By">{loading ? 'Loading...' : `${data.CloseBy}`}
      </Descriptions.Item>

      
      
      
    </Descriptions>
  );
}

export default Comp_CaseDetails;
