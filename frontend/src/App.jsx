import { Button, Container, createTheme, TextField, ThemeProvider } from '@mui/material'
import './App.css'
import ButtonUsage from './buttonUsage'
import { useState } from 'react';

function App() {
  const [link, setLink] = useState("")
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
        <Button>生成备份</Button>
      </Container>
    </ThemeProvider>
  )
}

export default App
