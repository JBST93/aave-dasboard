import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import DarkModeToggle from './DarkModeToggle';

const NavBar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleNavbar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      <button
        className="md:hidden focus:outline-none p-4 fixed top-0 right-0 z-20"
        onClick={toggleNavbar}
      >
        <svg
          className="w-6 h-6 text-black dark:text-white"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d={isOpen ? 'M6 18L18 6M6 6l12 12' : 'M4 6h16M4 12h16m-7 6h7'}
          ></path>
        </svg>
      </button>

      <nav
        className={`bg-gray-200 dark:bg-gray-800 text-black dark:text-white h-screen w-1/5 fixed top-0 left-0 p-4 flex flex-col justify-between transform ${
          isOpen
            ? '-translate-x-0 w-4/5 z-20'
            : '-translate-x-full w-0/5 overflow-hidden'
        } md:translate-x-0 transition-transform duration-300 ease-in-out`}
      >
        <div>
          <h1 className="text-2xl font-bold mb-4">Token Data View</h1>
          <button className="text-gray-900 bg-white border dark:border-teal-700 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 font-medium rounded-full text-sm px-5 py-2.5 me-2 mb-2 dark:bg-gray-800 dark:text-white dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700">
            <DarkModeToggle />
          </button>
          <br></br>
          <ul className="space-y-4 text-white">
            <li>
              <Link
                to="/stablecoin"
                className="hover:text-yellow-500 text-black dark:text-white"
              >
                Stablecoins (in progress)
              </Link>
            </li>
            <li>
              <Link
                to="/"
                className="hover:text-yellow-500 text-black dark:text-white"
              >
                Stablecoin yields
              </Link>
            </li>
          </ul>
        </div>
      </nav>
    </>
  );
};

export default NavBar;
