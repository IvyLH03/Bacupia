import { createFileRoute } from '@tanstack/react-router'
import { Button, CircularProgress, Container, createTheme, Divider, IconButton, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, ThemeProvider, Typography } from '@mui/material'
import { useEffect, useState } from 'react';
import '../app.css'
import DownloadIcon from '@mui/icons-material/Download';

export const Route = createFileRoute('/')({
  component: RouteComponent,
})

function RouteComponent() {
  return <Index/>
}

function getUrlParam(url, paramName) {
  // Create a URL object
  const urlObj = new URL(url);
  // Use URLSearchParams to get the parameter value
  return urlObj.searchParams.get(paramName);
}

function Index() {
  const [link, setLink] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [currentTaskId, setCurrentTaskId] = useState("")
  const [taskStatus, setTaskStatus] = useState("CLEAR")
  
  let isUrlValid = false
  let tid = 0

  try {
    tid = getUrlParam(link, "tid")
    isUrlValid = true
  } catch(e) {
    isUrlValid = false
  }

  const theme = createTheme({
    colorSchemes: {
      dark: true,
    },
  });


  const [availableFileList, setAvailableFileList] = useState([])

  const refreshFilelist = () => {
    fetch(`https://api.ivylh03.net/bacupia/archive`)
    .then(res=>res.json())
    .then(data=>{
      setAvailableFileList(data.sort((a, b) => b.time - a.time))
    })
  }

  const getTaskStatus = (taskId) => {
    fetch(`https://api.ivylh03.net/bacupia/status/${taskId}`)
    .then(res=>res.json())
    .then(data=>{
      setTaskStatus(data.state)
      // console.log(data.state)
      if(data.state === 'PENDING') {
        setTimeout(() => getTaskStatus(taskId), 2000)
      }
      if(data.state === 'SUCCESS') {
        setIsLoading(false)
        setCurrentTaskId('')
      }
    })
  }

  useEffect(()=>{
    refreshFilelist()
  },[taskStatus])

  useEffect(() => {
    if(currentTaskId !== ""){
      getTaskStatus(currentTaskId)
    }
  },[currentTaskId])

  // send backup request to backend
  const handleRequest = (tid) => {
    setIsLoading(true)
    fetch(`https://api.ivylh03.net/bacupia/request/${tid}`)
    .then( res => res.json() )
    .then( data => {
      setCurrentTaskId(data.task_id)
    })
  }

  return (
    <ThemeProvider theme={theme}>
      <Container>
        <Container>
          <h1>Bacupia - NGA 安科备份</h1>
          <br/>
          <TextField label="安科链接" variant="outlined" sx={{width:"300"}} value={link} onChange={event=>{setLink(event.target.value)}}/>
          <br/><br/>
          <Button disabled={isLoading || (! isUrlValid)} onClick={() => {handleRequest(tid)}}>{isLoading? <CircularProgress/>:(isUrlValid?"生成备份":"链接不完整")}</Button>
        </Container>
        <Container>
          <FileListComponent availableFileList={availableFileList}/>
        </Container>
      </Container>
    </ThemeProvider>
  )
}

// download files from the backend
const handleDownload = (filename) => {
  fetch(`https://api.ivylh03.net/bacupia/download/${filename}`)
  .then( res => res.blob() )
  .then( blob => {
    const file = window.URL.createObjectURL(blob);
    window.location.assign(file);
  })
}




function FileListItem({data, available}) {
  return <TableRow
    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
  >
    <TableCell component="th" scope="row">
      {data.name}
    </TableCell>
    <TableCell align="right">{
      new Date(data.time * 1000).toUTCString()
    }</TableCell>
    <TableCell align="right">{
      available?
      <IconButton color="primary" onClick={()=>handleDownload(data.name)}>
        <DownloadIcon fontSize="large" />
      </IconButton>
      :
      <CircularProgress />
    }</TableCell>

  </TableRow>
}

function FileListComponent ({availableFileList}) {
  // return <>
  //   {fileList.map(e => <FileListItem data={e}/>)}
  // </>
  return <>
    {
      availableFileList.length > 0?
      <Container sx={{marginTop:2}}>
        <Divider/>
        <br/>
        <Typography>
          列表内文件为本站所保存的历史备份记录，下载时请注意备份时间。<br/>
          如需最新备份请重新提交。如果以前没有备份过，完成后会刷新在列表里；如果以前曾经备份过，则会覆盖以前的记录。
        </Typography>
        <br/>
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>文档名</TableCell>
                <TableCell align="right">备份时间</TableCell>
                <TableCell align="right"></TableCell>

              </TableRow>
            </TableHead>
            <TableBody>
              {availableFileList.map(e => 
                <FileListItem key={e.name} data={e} available/>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Container>

      :
      <></>
    }
    
  </>
}