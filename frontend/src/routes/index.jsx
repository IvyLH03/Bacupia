import { createFileRoute } from '@tanstack/react-router'
import { Button, Container, createTheme, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, ThemeProvider } from '@mui/material'
import { useEffect, useState } from 'react';
import '../app.css'

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

  const handleDownload = (tid) => {
    setIsLoading(true)
    fetch(`https://api.ivylh03.net/bacupia/request/${tid}`)
      // .then( res => res.blob() )
      // .then( blob => {
      //   let file = window.URL.createObjectURL(blob);
      //   window.location.assign(file);
      //   setIsLoading(false)
      // })
      .then(res=> res.json())
      .then(data=> console.log(data))
  }

  useEffect(() => {
    console.log("Loading state changed:", isLoading);
  }, [isLoading]);

  return (
    <ThemeProvider theme={theme}>
      <Container>
        <Container>
          <h1>Bacupia - NGA 安科备份</h1>
          <TextField label="安科链接" variant="outlined" sx={{width:"300"}} value={link} onChange={event=>{setLink(event.target.value)}}/>
          <br/><br/>
          <Button disabled={isLoading || (! isUrlValid)} onClick={() => {handleDownload(tid)}}>{isLoading? "正在处理...":(isUrlValid?"生成备份":"链接不完整")}</Button>
        </Container>
        <Container>
          <FileListComponent/>
        </Container>
      </Container>
    </ThemeProvider>
  )
}

function FileListItem({data}) {
  return <>
    {data.name}
  </>
}

function FileListComponent () {
  const [fileList, setFileList] = useState([])
  useEffect(()=>{
    fetch(`https://api.ivylh03.net/bacupia/archive`)
    .then(res=>res.json())
    .then(data=>{
      setFileList(data)
      console.log(data)
    })
  },[])
  // return <>
  //   {fileList.map(e => <FileListItem data={e}/>)}
  // </>
  return <TableContainer component={Paper}>
  <Table sx={{ minWidth: 650 }} aria-label="simple table">
    <TableHead>
      <TableRow>
        <TableCell>文档名</TableCell>
        <TableCell align="right">创建时间</TableCell>
        <TableCell align="right">状态</TableCell>

      </TableRow>
    </TableHead>
    <TableBody>
      {fileList.map((row) => (
        <TableRow
          key={row.name}
          sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
        >
          <TableCell component="th" scope="row">
            {row.name}
          </TableCell>
          <TableCell align="right">{
            new Date(row.time * 1000).toUTCString()
          }</TableCell>
        </TableRow>
      ))}
    </TableBody>
  </Table>
</TableContainer>
}