import React, { useEffect } from 'react';
import { IoMoon, IoSunny } from 'react-icons/io5';

function DarkModeToggle() {
  const [dark, setDark] = React.useState(false);

  // Function to toggle dark mode
  const darkModeHandler = () => {
    const newDarkMode = !dark;
    setDark(newDarkMode);
    document.body.classList.toggle('dark', newDarkMode);

    // Persist user's preference in local storage
    localStorage.setItem('dark-mode', newDarkMode);
  };

  // UseEffect to set the initial mode based on user preference or local storage
  useEffect(() => {
    // Check local storage first
    const storedDarkMode = localStorage.getItem('dark-mode');
    if (storedDarkMode !== null) {
      const isDarkMode = storedDarkMode === 'true';
      setDark(isDarkMode);
      document.body.classList.toggle('dark', isDarkMode);
    } else {
      // Otherwise, use system preference
      const prefersDarkMode = window.matchMedia(
        '(prefers-color-scheme: dark)'
      ).matches;
      setDark(prefersDarkMode);
      document.body.classList.toggle('dark', prefersDarkMode);
    }
  }, []);

  return (
    <div className="flex items-center space-x-2">
      <span>{dark ? <IoSunny /> : <IoMoon />}</span>
      <label className="relative inline-flex items-center cursor-pointer">
        <input
          type="checkbox"
          className="sr-only justify-item-center"
          checked={dark}
          onChange={darkModeHandler}
        />
        <div className="w-12 p-1 flex items-center h-6 bg-yellow-500 rounded-full dark:bg-teal-700 transition-colors duration-300 ease-in-out">
          <div
            className={`dot bg-white w-5 h-5 rounded-full transition-transform duration-300 ease-in-out transform ${
              dark ? 'translate-x-full  bg-black' : 'translate-x-0'
            }`}
          ></div>
        </div>
      </label>
    </div>
  );
}

export default DarkModeToggle;
