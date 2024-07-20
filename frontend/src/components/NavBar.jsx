import React from 'react';
import { Link } from 'react-router-dom';
import DarkModeToggle from './DarkModeToggle';

const Navbar = () => {
  return (
    <nav className="bg-gray-600 dark:bg-black text-white h-screen w-1/5 fixed top-0 left-0 p-4 flex flex-col justify-between">
      <div>
        <h1 className="text-2xl font-bold mb-4">Token Data View</h1>
        <DarkModeToggle />
        <ul className="space-y-4  text-white">
          <li>
            <Link
              to="/"
              className="hover:text-yellow-500 text-white"
            >
              Stablecoin Yield
            </Link>
          </li>
          <li>
            <Link
              to="/"
              className="hover:text-yellow-500  text-white"
            >
              Stablecoins
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
