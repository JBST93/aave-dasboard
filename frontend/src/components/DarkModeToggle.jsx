import React from 'react';
import { IoMoon, IoSunny } from 'react-icons/io5';

function DarkModeToggle() {
  const [dark, setDark] = React.useState(false);

  const darkModeHandler = () => {
    setDark(!dark);
    document.body.classList.toggle('dark');
  };

  return (
    <div className="flex items-center space-x-2">
      <span>{dark ? <IoSunny /> : <IoMoon />}</span>
      <label className="relative inline-flex items-center cursor-pointer">
        <input
          type="checkbox"
          className="sr-only"
          checked={dark}
          onChange={darkModeHandler}
        />
        <div className="w-11 h-6 bg-gray-200 rounded-full dark:bg-gray-700">
          <div
            className={`dot absolute left-1 top-1 bg-white w-5 h-5 rounded-full transition ${
              dark ? 'transform translate-x-full bg-yellow-500' : ''
            }`}
          ></div>
        </div>
      </label>
    </div>
  );
}

export default DarkModeToggle;
