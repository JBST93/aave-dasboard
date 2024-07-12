import React from 'react';
import FetchData from './components/FetchData';
import Footer from './components/Footer';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';

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
          minHeight: '100vh',
          width: '100%', // Ensure the box takes full width
          textAlign: 'center',
          padding: 2,
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
