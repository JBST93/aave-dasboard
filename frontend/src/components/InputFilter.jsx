import React, { useEffect } from 'react';
import Select from 'react-select';
import makeAnimated from 'react-select/animated';

const InputFilter = ({ data, setSelectedBlockchains, resetFilter }) => {
  // Create an array with all the item.chain values and get the distinct ones
  const uniqueChains = Array.from(new Set(data.map((item) => item.chain)));

  // Create options in the format expected by react-select
  const options = uniqueChains.map((chain) => ({ value: chain, label: chain }));

  const animatedComponents = makeAnimated();

  const customStyles = {
    control: (provided, state) => ({
      ...provided,
      height: '2.5rem',
      overflow: 'hidden',
      borderColor: state.isFocused ? '' : '',
      boxShadow: state.isFocused ? '0 0 0 1px #4FD1C5' : 'none',
    }),
    valueContainer: (provided) => ({
      ...provided,
      display: 'flex',
      flexWrap: 'nowrap',
      overflow: 'hidden',
    }),
    multiValue: (provided) => ({
      ...provided,
      backgroundColor: '#1F2937',
    }),
    multiValueLabel: (provided) => ({
      ...provided,
      color: '#FFFFFF',
    }),
    multiValueRemove: (provided) => ({
      ...provided,
      color: '#9CA3AF',
      cursor: 'pointer',
      '&:hover': {
        backgroundColor: '#4B5563',
        color: '#FFFFFF',
      },
    }),
    menu: (provided) => ({
      ...provided,
      zIndex: 40,
    }),
    menuList: (provided) => ({
      ...provided,
      maxHeight: '150px',
      overflowY: 'auto',
    }),
    placeholder: (provided) => ({
      ...provided,
      zIndex: 41,
    }),
  };

  const placeholderStyles = 'text-gray-500 pl-1 py-0.5';
  const selectInputStyles = 'dark:bg-gray-800';
  const valueContainerStyles = 'gap-1';
  const singleValueStyles = 'leading-7 ml-1';
  const multiValueStyles =
    'bg-yellow-50 dark:bg-gray-900 rounded items-center py-0.5 pl-2 pr-1 gap-1.5';
  const multiValueLabelStyles = 'leading-6 py-0.5';
  const multiValueRemoveStyles =
    'border border-gray-200 bg-white hover:bg-red-50 hover:text-red-800 text-gray-500 hover:border-red-300 rounded-md';
  const indicatorsContainerStyles = 'gap-1';
  const clearIndicatorStyles =
    'text-gray-500 p-1 rounded-md hover:bg-red-50 hover:text-red-800';
  const indicatorSeparatorStyles = 'bg-gray-300 dark:bg-gray-500';
  const dropdownIndicatorStyles =
    'p-1 hover:bg-gray-100 text-gray-500 rounded-md hover:text-black dark:bg-gray-800';
  const menuStyles =
    'p-1 mt-2 border border-gray-200 bg-white rounded-lg dark:bg-gray-800';
  const groupHeadingStyles =
    'ml-3 mt-2 mb-1 text-gray-500 text-sm dark:bg-red-200';
  const optionStyles = {
    base: 'hover:cursor-pointer px-3 py-2 rounded',
    focus:
      'bg-gray-100 active:bg-gray-200 active: dark:bg-gray-200 dark:text-black',
    selected:
      "after:content-['✔'] after:ml-2 after:text-green-500 text-gray-500",
  };
  const noOptionsMessageStyles =
    'text-gray-500 p-2 bg-gray-50 dark:bg-gray-800 rounded-sm';

  return (
    <Select
      placeholder="Filter by blockchain"
      components={animatedComponents}
      closeMenuOnSelect={false}
      isMulti
      name="blockchain"
      options={options}
      styles={customStyles}
      className="basic-multi-select"
      classNamePrefix="Select"
      onChange={(selectedOptions) => {
        setSelectedBlockchains(
          selectedOptions ? selectedOptions.map((option) => option.value) : []
        );
      }}
      classNames={{
        control: () =>
          'h-full overflow-hidden border border-gray-300 text-sm dark:border-teal-600 bg-white dark:bg-gray-800 text-gray-400 dark:text-white focus:outline-none focus:ring-2',
        placeholder: () => placeholderStyles,
        input: () => selectInputStyles,
        valueContainer: () => valueContainerStyles,
        singleValue: () => singleValueStyles,
        multiValue: () => multiValueStyles,
        multiValueLabel: () => multiValueLabelStyles,
        multiValueRemove: () => multiValueRemoveStyles,
        indicatorsContainer: () => indicatorsContainerStyles,
        clearIndicator: () => clearIndicatorStyles,
        indicatorSeparator: () => indicatorSeparatorStyles,
        dropdownIndicator: () => dropdownIndicatorStyles,
        menu: () => menuStyles,
        groupHeading: () => groupHeadingStyles,
        option: ({ isFocused, isSelected }) =>
          `${isFocused ? optionStyles.focus : ''} ${
            isSelected ? optionStyles.selected : ''
          } ${optionStyles.base}`,
        noOptionsMessage: () => noOptionsMessageStyles,
      }}
    />
  );
};

export default InputFilter;
