import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-gray-200 p-4 md:h-screen md:w-1/5 md:fixed md:top-0 md:left-0 md:flex md:flex-col">
      <ul className="space-y-4 text-white">
        <li>
          <Link
            to="/"
            className="hover:underline"
          >
            Stablecoin Yield
          </Link>
        </li>
        <li>
          <Link
            to="/"
            className="hover:underline"
          >
            Stablecoins
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
