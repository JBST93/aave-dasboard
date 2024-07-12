import React from 'react';
import FetchData from './components/FetchData';
import Footer from './components/Footer';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';

import './App.css';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          width: '100vw',
          textAlign: 'center',
          minHeight: '100vh', // Ensure the box covers the full viewport height
        }}
      >
        <h1>Money Market Rates</h1>
        <FetchData />
        <Footer />
      </Box>
    </ThemeProvider>
  );
}

export default App;
