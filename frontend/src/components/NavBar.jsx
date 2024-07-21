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
        className="md:hidden p-4 fixed top-0 right-0 z-20"
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
          isOpen ? '-translate-x-0 w-4/5' : '-translate-x-full w-1/5'
        } md:translate-x-0 transition-transform duration-300 ease-in-out z-20`}
      >
        <div>
          <h1 className="text-2xl font-bold mb-4">Token Data View</h1>
          <DarkModeToggle />
          <ul className="space-y-4 text-white">
            <li>
              <Link
                to="/"
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
            <li>
              <Link
                to="/"
                className="hover:text-yellow-500 text-black dark:text-white"
              >
                Ethereum yields (in progress)
              </Link>
            </li>
            <li>
              <Link
                to="/"
                className="hover:text-yellow-500 text-black dark:text-white"
              >
                CEX Volumes
              </Link>
            </li>
            <li>
              <Link
                to="/"
                className="hover:text-yellow-500 text-black dark:text-white"
              >
                Bitcoin ETF
              </Link>
            </li>
          </ul>
        </div>
      </nav>
    </>
  );
};

export default NavBar;
