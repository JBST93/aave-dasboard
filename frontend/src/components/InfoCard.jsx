const InfoCard = (props) => {
  return (
    <div className="w-full md:max-w-sm p-4 my-2 bg-white shadow dark:bg-gray-800 border-gray-300">
      <div className="flex items-center gap-2">
        <h5 className="md:text-lg text-lg font-bold tracking-tight text-gray-900 dark:text-white">
          {props.title}
        </h5>
      </div>
      <p className="text-2xl font-medium text-gray-900 dark:text-white py-2">
        {props.value} {props.scale}
      </p>
      <p className="text-sm md:text-sm text-gray-500 dark:text-gray-400">
        {props.description}
      </p>
      {props.link ? (
        <a
          href={props.link}
          className="text-blue-600 hover:text-blue-800 text-xs"
        >
          Click Here To Learn More
        </a>
      ) : (
        ''
      )}
    </div>
  );
};

export default InfoCard;
