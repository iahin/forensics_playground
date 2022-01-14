import React, { useEffect, useState, useMemo } from 'react';
import {
  Container
} from 'reactstrap';
import TableContainer from './qik-repository-table';
import 'bootstrap/dist/css/bootstrap.min.css';
import Modal from "react-modal"; 
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
        Header: 'Crime Type',
        accessor: 'crime_type',
      },
      {
        Header: 'Status',
        accessor: 'status',
      },
    ],
    []
  );

  return (
    <div width="80%">
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