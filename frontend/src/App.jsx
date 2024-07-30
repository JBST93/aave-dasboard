import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './components/NavBar';
import Footer from './components/Footer';

const Layout = () => (
  <div className="md:flex">
    <div className="md:h-screen md:w-1/5">
      <Navbar />
    </div>
    <div className="w-full md:w-4/5 p-4 bg-white dark:bg-gray-900 text-black dark:text-white">
      <Outlet />
      <Footer />
    </div>
  </div>
);

export default Layout;
