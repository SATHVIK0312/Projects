import './App.css';
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
  const locationTable = [
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
      field: 'locid',
      headerName: 'Location ID',
      width: 250,
    },
    {
      field: 'postal',
      headerName: 'Pin Code',
      width: 250,
    },
    {
      field: 'city',
      headerName: 'City',
      width: 250,
    },
    {
      field: 'countryid',
      headerName: 'Country ID',
      width: 250,
    },
  ];

  const getAllRecords = () => {
    axios.get(apiUrlMapping.locationData.getAll).then((response) => {
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
  const [locid, setlocid] = useState("");
  const [postal, setpostal] = useState("");
  const [city, setcity] = useState("");
  const [countryid, setcountryid] = useState("");

  const creatingRecord = () => 
  {
    if(locid !== undefined && postal !== undefined && city !== undefined && countryid !== undefined){
      let payload={
        "locid":locid,
        "postal" : postal ,
        "city"   : city    ,
        "countryid": countryid
      }
      axios.post(apiUrlMapping.locationData.post,payload).then(response =>
        {
          getAllRecords()
          handleClose()
          setlocid("")
          setpostal("")
          setcity("")
          setcountryid("")
        })
    }
  }

  const deleteRecord = (index) =>
  {
    let dataId = rows[index]._id
    axios.delete(apiUrlMapping.locationData.delete + "/" + dataId).then(() => {getAllRecords();});
  }

  const onClickofEditButton = (e) => {
    console.log(e)
    setAddOrEdit("Edit")
    let editRecord = rows[e.id]
    console.log(editRecord)
    setlocid(editRecord.locid)
    setpostal(editRecord.postal)
    setcity(editRecord.city)
    setcountryid(editRecord.countryid)
    seteditId(editRecord._id)
    handleClickOpen()
  }
  
  const [editId, seteditId] = useState(""); 

  const editingRecord = () =>
  {
    if(locid !== undefined && postal !== undefined && city !== undefined && countryid !== undefined){
      let payload={
        "locid":locid,
        "postal" : postal ,
        "city"   : city    ,
        "countryid": countryid
      }
      axios.put(apiUrlMapping.locationData.put + "/" + editId,payload).then(response =>
        {
          getAllRecords()
          handleClose()
          setlocid("")
          setpostal("")
          setcity("") 
          setcountryid("")
        })
  }}
 
  return (
    <div className='App'>
      <div className='table-container'>
        <h1>LOCATION DATA</h1>
        <div className='data-grid-container'>
          <DataGrid
            rows={rows}
            columns={locationTable}
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
        <DialogTitle>Save the Location Data</DialogTitle>
        <DialogContent>
            <TextField autoFocus margin='dense' id="locid" onChange={(e) => {setlocid(e.target.value)}} value={locid} label="Location ID" type='text' fullWidth/>
            <TextField autoFocus margin='dense' id="postal" onChange={(e) => {setpostal(e.target.value)}} value={postal} label="PINCODE" type='text' fullWidth/>
            <TextField autoFocus margin='dense' id="city" onChange={(e) => {setcity(e.target.value)}} value={city} label="City" type='text' fullWidth/>
            <TextField autoFocus margin='dense' id="countryid" onChange={(e) => {setcountryid(e.target.value)}} value={countryid} label="Country ID" type='text' fullWidth/>
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
