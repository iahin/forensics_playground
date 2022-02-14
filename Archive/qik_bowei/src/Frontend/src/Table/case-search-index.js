import React, { useEffect, useState, useMemo } from 'react';
import {
  Container
} from 'reactstrap';
import TableContainer from './qik-repository-table';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Dropdown, Selection } from 'react-dropdown-now';
import { Button } from 'antd';
import axios from 'axios';
import Moment from 'moment';

const App = () => {
  const BarStyling = {width:"20rem",background:"#F2F1F9", border:"none", padding:"0.5rem"};
  const [input, setInput] = useState('');

  const [data, setData,page,setPage] = useState([]);
  const [dropdownSelection, setDropdownSelection] = useState('All');

  const dropdownOnChange = (value) => {
    setDropdownSelection(value)
    console.log(value)
    console.log(dropdownSelection)
  }

  const options = [
    { id: 'all', value: 'All', label: 'All'},
    { id: 'caseID', value: 'CaseID', label: 'Case ID'},
    { id: 'caseName', value: 'CaseName', label: 'Case Name'},
    { id: 'caseDesc', value: 'CaseDesc', label: 'Case Description'},
    { id: 'crimeType', value: 'CrimeType', label: 'Crime Type'},
    { id: 'status', value: 'Status', label: 'Status'},
    { id: 'creator', value: 'Creator', label: 'Creator'},
    { id: 'assignee', value: 'Assignee', label: 'Assignee'},
    { id: 'priority', value: 'Priority', label: 'Priority'},
  ];

  const columns = useMemo(
    () => [
      {
        Header:'S/N',      
        Cell: (row) => {
          return row.cell.row.index+1;
        },
      },
      {
        Header: 'Case ID',
        accessor: 'caseID',
      },
      {
        Header: 'Case Name',
        accessor: 'caseName',
      },
      {
        Header: 'Case Description',
        accessor: 'caseDesc',
      },
      {
        Header: 'Create Time',
        accessor: 'createTime',
        accessor: row => Moment(row.createTime[0].value).format("DD/MM/YYYY H:mm"),
      },
      {
        Header: 'Crime Type',
        accessor: 'crimeType',
      },
      {
        Header: 'Status',
        accessor: 'status',
      },
      {
        Header: 'Creator',
        accessor: 'creator',
      },
    ],
    []
  );

  const search = (params) => {
    axios.post('/api/Cases/SearchCase?option='+params+'&query='+input)
      .then(res => {
        console.log(res)
        setData(res.data);
      })  
      .catch((error) => {
        console.log(error)
      });      
  }

  return (
    <div width="80%">

    <div>
    <input 
      style={BarStyling}
      key="search"
      value={input}
      placeholder={"search cases..."}
      onChange={(e) => setInput(e.target.value)}
    />

    <Dropdown
      placeholder="All"
      className="my-className"
      options={options}
      value={dropdownSelection}
      onChange={(value) => dropdownOnChange(value.label)}
      onSelect={(value) => console.log('selected!', value)} // always fires once a selection happens even if there is no change
      onClose={(closedBySelection) => console.log('closedBySelection?:', closedBySelection)}
      onOpen={() => console.log('open!')}
    />

    <Button type="primary" onClick={()=>search(dropdownSelection, input)}>Search</Button>
    </div>

    <Container style={{ marginTop: 100 }}>
      <TableContainer
        columns={columns}
        data={data}
        pagination={{
          onChange(current) {
            setPage(current);
          }}}
      />
    </Container>
    </div>
  );
};

export default App;