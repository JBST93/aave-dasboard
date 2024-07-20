import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import './index.css';

import StablecoinYield from './pages/StablecoinYield';
import StablecoinInfo from './pages/StablecoinInfo';
// import NotFound from './components/NotFound';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />, // Use App as the main layout component
    children: [
      {
        path: '/',
        element: <StablecoinYield />, // Nested route
      },
    ],
  },
  {
    path: '/stablecoin',
    element: <App />, // Use App as the main layout component
    children: [
      {
        path: '/stablecoin',
        element: <StablecoinInfo />, // Nested route
      },
    ],
    // Add more nested routes as needed
    // {
    //   path: '*',
    //   element: <NotFound />,
    // },
  },
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
