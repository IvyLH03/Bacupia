import { createFileRoute } from '@tanstack/react-router'
import { Button, CircularProgress, Container, createTheme, IconButton, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, ThemeProvider } from '@mui/material'
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
  const [pendingFileList, setPendingFileList] = useState([])

  const refreshFilelist = () => {
    fetch(`https://api.ivylh03.net/bacupia/archive`)
    .then(res=>res.json())
    .then(data=>{
      setAvailableFileList(data)
      console.log(data)
    })
  }

  useEffect(()=>{
    refreshFilelist()
    if(pendingFileList.length > 0) {
      setTimeout(refreshFilelist, 10000)
    }
  },[isLoading])

  // send backup request to backend
  const handleRequest = (tid) => {
    setIsLoading(true)
    fetch(`https://api.ivylh03.net/bacupia/request/${tid}`)
    .then( res => res.json() )
    .then( data => {
      console.log(data)
    })
  }

  return (
    <ThemeProvider theme={theme}>
      <Container>
        <Container>
          <h1>Bacupia - NGA 安科备份</h1>
          <TextField label="安科链接" variant="outlined" sx={{width:"300"}} value={link} onChange={event=>{setLink(event.target.value)}}/>
          <br/><br/>
          <Button disabled={isLoading || (! isUrlValid)} onClick={() => {handleRequest(tid)}}>{isLoading? "正在处理...":(isUrlValid?"生成备份":"链接不完整")}</Button>
        </Container>
        <Container>
          <FileListComponent availableFileList={availableFileList} pendingFileList={pendingFileList}/>
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

function FileListComponent ({availableFileList, pendingFileList}) {
  // return <>
  //   {fileList.map(e => <FileListItem data={e}/>)}
  // </>
  return <>
    {
      pendingFileList.length > 0?
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>文档名</TableCell>
              <TableCell align="right">备份时间</TableCell>
              <TableCell align="right">状态</TableCell>

            </TableRow>
          </TableHead>
          <TableBody>
            {pendingFileList.map(e => 
              <FileListItem key={e.name} data={e} available/>
            )}
          </TableBody>
        </Table>
      </TableContainer>
      :
      <></>
    }
    <br/>
    {
      availableFileList.length > 0?
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>文档名</TableCell>
              <TableCell align="right">备份时间</TableCell>
              <TableCell align="right">状态</TableCell>

            </TableRow>
          </TableHead>
          <TableBody>
            {availableFileList.map(e => 
              <FileListItem key={e.name} data={e} available/>
            )}
          </TableBody>
        </Table>
      </TableContainer>
      :
      <></>
    }
    
  </>
}