import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async'; // Import HelmetProvider

import App from './App.jsx';
import './index.css';

import ProjectList from './pages/ProjectList.jsx';
import StablecoinYield from './pages/StablecoinYield';
import Yield from './pages/Yield';

import StablecoinInfo from './pages/StablecoinInfo';
import Blog from './pages/Blog';
import StablecoinYieldFarming from './pages/blog/StablecoinYieldFarming';
import CurvePools from './pages/project/CurvePools.jsx';
import Contact from './pages/Contact.jsx';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />, // Use App as the main layout component
    children: [
      {
        path: '/',
        element: <StablecoinYield />, // Default route when visiting '/'
      },
      {
        path: '/yields',
        element: <Yield />, // Default route when visiting '/'
      },
      {
        path: 'projects',
        element: <ProjectList />, // Nested route for '/projects'
      },
      {
        path: 'blog',
        element: <Blog />, // This route renders the Blog component for '/blog'
      },
      {
        path: 'blog/stablecoin-yield-farming',
        element: <StablecoinYieldFarming />, // This renders the specific blog post without the Blog component
      },
      {
        path: 'stablecoin',
        element: <StablecoinInfo />, // Nested route for '/stablecoin'
      },
      {
        path: 'curve-pools',
        element: <CurvePools />, // Nested route for '/stablecoin'
      },
      {
        path: 'contact',
        element: <Contact />, // Nested route for '/stablecoin'
      },
    ],
  },
  // You can add a wildcard route for handling 404 not found pages if needed
  // {
  //   path: '*',
  //   element: <NotFound />, // Catch-all route for 404 pages
  // },
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <HelmetProvider>
      <RouterProvider router={router} />
    </HelmetProvider>
  </React.StrictMode>
);
