import { Button, Container, createTheme, TextField, ThemeProvider } from '@mui/material'
import './App.css'
import ButtonUsage from './buttonUsage'
import { useState } from 'react';

function getUrlParam(url, paramName) {
  // Create a URL object
  const urlObj = new URL(url);
  // Use URLSearchParams to get the parameter value
  return urlObj.searchParams.get(paramName);
}



function App() {
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

  return (
    <ThemeProvider theme={theme}>
      <Container>
        <h1>Bacupia - NGA 安科备份</h1>
        <TextField label="安科链接" variant="outlined" sx={{width:"300"}} value={link} onChange={event=>{setLink(event.target.value)}}/>
        <br/><br/>
        <Button disabled={isLoading || (! isUrlValid)} href={`http://api.ivylh03.net:5000/bacupia/${tid}`} onClick={()=>{setIsLoading(true)}}>{isLoading? "正在处理...":(isUrlValid?"生成备份":"链接不完整")}</Button>
      </Container>
    </ThemeProvider>
  )
}

export default App
