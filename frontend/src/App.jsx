import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './components/NavBar';
import Footer from './components/Footer';

const Layout = () => (
  <div className="md:flex md:min-h-screen">
    <Navbar />
    <div className="flex-1 md:ml-[20%] p-4 dark:bg-slate-900 text-black dark:text-white">
      <Outlet />
      <Footer />
    </div>
  </div>
);

export default Layout;
