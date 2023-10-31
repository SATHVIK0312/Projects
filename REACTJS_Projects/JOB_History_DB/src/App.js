import './App.css';
import Login from './Login';
import { DataGrid, GridActionsCellItem } from '@mui/x-data-grid';
import { GridToolbar } from '@mui/x-data-grid-pro';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import apiUrlMapping from '../src/Resources/apiMapping.json';
import { Button } from '@mui/material';
import { TextField } from '@mui/material';
import { Dialog, DialogContent, DialogActions, DialogTitle} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';



const getRowsWithId = (rows) => {
  let id = 0;
  let completeRowListArray = [];
  for (let row of rows) {
    const rowsWithId = {
      id: id,
      ...row,
    };
    id++;
    completeRowListArray.push(rowsWithId);
  }
  return completeRowListArray;
};

function App() {

  const [loggedIn, setLoggedIn] = useState(false);
  useEffect(() => {
    if (loggedIn) {
      getAllRecords();
    }
  }, [loggedIn]);

  const handleLogin = () => {
    setLoggedIn(true);
  };
  
  const jobTable = [
    {
      field: "acions",
      type: "actions",
      width: 100,
      getActions: (event) => [
        <GridActionsCellItem onClick={(e) => deleteRecord(event.id)} icon={<DeleteIcon/>} label='Delete'/>,
        <GridActionsCellItem onClick={(e) => onClickofEditButton(event)} icon={<EditIcon/>} label='Edit'/>
      ]
    },
    {
      field: 'empid',
      headerName: 'Employee ID',
      width: 250,
    },
    {
      field: 'start',
      headerName: 'Start Date',
      width: 250,
    },
    {
      field: 'end',
      headerName: 'End Date',
      width: 250,
    },
    {
      field: 'jobid',
      headerName: 'Job ID',
      width: 250,
    },
    {
      field: 'depid',
      headerName: 'Department ID',
      width: 250,
    },
  ];

  const getAllRecords = () => {
    axios.get(apiUrlMapping.jobData.getAll).then((response) => {
      console.log(response.data);
      setRows(getRowsWithId(response.data));
    });
  };

  useEffect(() => { getAllRecords(); }, []);

  const [rows, setRows] = useState([]);
  

  const onClickofSaveRecord = () =>
  {
    setAddOrEdit("Save")
    handleClickOpen()
  }

  const forAddandEdit = (type) =>
  {
    if (type === "Edit") (editingRecord())
    if (type === "Save") (creatingRecord())
  }

  const handleClickOpen = () => {setOpen(true)};
  const handleClose = () => {setOpen(false)};
  const [open, setOpen] = useState(false);
  const [addOrEdit, setAddOrEdit] = useState("");
  const [empid, setempid] = useState("");
  const [start, setstart] = useState("");
  const [end, setend] = useState("");
  const [jobid, setjobid] = useState("");
  const [depid, setdepid] = useState("");

  const creatingRecord = () => 
  {
    if(empid !== undefined && start !== undefined && end !== undefined && jobid !== undefined){
      let payload={
        "empid":empid,
        "start" : start ,
        "end"   : end    ,
        "jobid": jobid,
        "depid": depid,
      }
      axios.post(apiUrlMapping.jobData.post,payload).then(response =>
        {
          getAllRecords()
          handleClose()
          setempid("")
          setstart("")
          setend("")
          setjobid("")
          setdepid("")
        })
    }
  }

  const deleteRecord = (index) =>
  {
    let dataId = rows[index]._id
    axios.delete(apiUrlMapping.jobData.delete + "/" + dataId).then(() => {getAllRecords();});
  }

  const onClickofEditButton = (e) => {
    console.log(e)
    setAddOrEdit("Edit")
    let editRecord = rows[e.id]
    console.log(editRecord)
    setempid(editRecord.empid)
    setstart(editRecord.start)
    setend(editRecord.end)
    setjobid(editRecord.jobid)
    setdepid(editRecord.depid)
    seteditId(editRecord._id)
    handleClickOpen()
  }
  
  const [editId, seteditId] = useState(""); 

  const editingRecord = () =>
  {
    if(empid !== undefined && start !== undefined && end !== undefined && jobid !== undefined){
      let payload={
        "empid":empid,
        "start" : start ,
        "end"   : end    ,
        "jobid": jobid,
        "depid": depid
      }
      axios.put(apiUrlMapping.jobData.put + "/" + editId,payload).then(response =>
        {
          getAllRecords()
          handleClose()
          setempid("")
          setstart("")
          setend("")
          setjobid("")
          setdepid("")
        })
  }}
 
  if (!loggedIn) {
    return <Login onLogin={handleLogin} />;
  }
  
  return (
    <div className='App'>
      
      <div className='table-container'>
        <h1>JOB HISTORY DATA</h1>
        <div className='data-grid-container'>
          <DataGrid
            rows={rows}
            columns={jobTable}
            components={{ Toolbar: GridToolbar }}
            componentsProps={{ toolbar: { showQuickFilter: true } }}
            pageSize={5} 
            rowsPerPageOptions={[5]} 
            pagination
            checkboxSelection
            disableSelectionOnClick
          />
        </div>
      </div>
      <div className='center'>
        <br></br>
        <Button variant='contained' onClick={onClickofSaveRecord}> ADD RECORD </Button>
        <br></br>
        <br></br>
      </div>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Save the JOB HISTORY Data</DialogTitle>
        <DialogContent>
            <TextField autoFocus margin='dense' id="empid" onChange={(e) => {setempid(e.target.value)}} value={empid} label="Employee ID" type='text' fullWidth/>
            <TextField autoFocus margin='dense' id="start" onChange={(e) => {setstart(e.target.value)}} value={start} label="Start Date" type='text' fullWidth/>
            <TextField autoFocus margin='dense' id="end" onChange={(e) => {setend(e.target.value)}} value={end} label="End Date" type='text' fullWidth/>
            <TextField autoFocus margin='dense' id="jobid" onChange={(e) => {setjobid(e.target.value)}} value={jobid} label="Job ID" type='text' fullWidth/>
            <TextField autoFocus margin='dense' id="depidid" onChange={(e) => {setdepid(e.target.value)}} value={depid} label="Department ID" type='text' fullWidth/>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}> Cancel </Button>
          <Button onClick={() => { forAddandEdit(addOrEdit) }} > Save </Button>
        </DialogActions>
      </Dialog>

    </div>
  );
}

export default App;
