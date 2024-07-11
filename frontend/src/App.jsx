import React from 'react';
import FetchData from './components/FetchData';
import Footer from './components/Footer';

import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <link
          rel="preconnect"
          href="https://fonts.googleapis.com"
        />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossorigin
        />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"
        />
        <h1>Money Market Rates</h1>
        <FetchData />
        <Footer />
      </header>
    </div>
  );
}

export default App;
