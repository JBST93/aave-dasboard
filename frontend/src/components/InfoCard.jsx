const InfoCard = (props) => {
  return (
    <div className="w-full md:max-w-sm p-4 my-2 bg-white border shadow dark:bg-gray-800 border-gray-300 dark:border-teal-700">
      <div className="flex items-center gap-2">
        <svg
          className="w-7 h-7 text-gray-500 dark:text-gray-400"
          height="64"
          viewBox="0 0 64 64"
          xmlns="http://www.w3.org/2000/svg"
          fill="currentColor"
        >
          <circle
            cx="16"
            cy="16"
            r="6"
          />
          <circle
            cx="48"
            cy="48"
            r="6"
          />
          <line
            x1="16"
            y1="48"
            x2="48"
            y2="16"
            stroke="currentColor"
            strokeWidth="4"
          />
        </svg>
        <h5 className="md:text-xl text-xl font-semibold tracking-tight text-gray-900 dark:text-white">
          {props.title}
        </h5>
      </div>
      <p className="text-2xl font-medium text-gray-900 dark:text-white py-2">
        {props.value}%
      </p>
      <p className="text-xs md:text-sm text-gray-500 dark:text-gray-400">
        {props.description}
      </p>
    </div>
  );
};

export default InfoCard;
