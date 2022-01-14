import React, { useEffect, useState, useMemo } from 'react';
import {
  Container
} from 'reactstrap';
import TableContainer from './qik-results-table';
import 'bootstrap/dist/css/bootstrap.min.css';
import Modal from "react-modal"; 
import Button from '@material-ui/core/Button';
import { BrowserRouter as Router, Switch, Route, Link, useHistory } from 'react-router-dom';
import { camelizeKeys, decamelizeKeys } from 'humps';

const App = () => {

  const [data, setData,page,setPage] = useState([]);
  useEffect(() => {
    const doFetch = async () => {
      const response = await fetch('/api/Repo');
      const repoItems = await response.json();
      console.log(decamelizeKeys(repoItems))
      setData(decamelizeKeys(repoItems));
    };
    doFetch();
  }, []);

  const columns = useMemo(
    () => [
      {
        Header:'S/N',      
        Cell: (row) => {
          return row.cell.row.index+1;
        },
      },
      {
        Header: 'Title',
        accessor: 'title',
      },
      {
        Header: 'Description',
        accessor: 'description',
      },
      {
        Header: 'Date Time Created',
        accessor: 'date_time_created',
      },
      {
        Header: 'Status',
        accessor: 'status',
      },
    ],
    []
  );
  const history = useHistory();

  function goToQueryBuilder(){
    history.push('/query-builder');
  }

  return (
    <div width="80%">
    <Button variant="outlined" onClick={() => goToQueryBuilder()}>+ New Query</Button>
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