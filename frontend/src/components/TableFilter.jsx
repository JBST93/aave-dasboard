import React, { useState, useEffect } from 'react';
import Select from 'react-select';
import Slider from 'rc-slider';
import 'rc-slider/assets/index.css';

const TableFilter = ({ data = [], onFilterChange }) => {
  const [selectedTokens, setSelectedTokens] = useState([]);
  const [selectedChains, setSelectedChains] = useState([]);
  const [minApy, setMinApy] = useState(0);
  const [minAmountSupplied, setMinAmountSupplied] = useState(0);

  // Generate options for Select components from the data prop
  const tokenOptions =
    data.length > 0
      ? Array.from(new Set(data.map((item) => item.token))).map((token) => ({
          value: token,
          label: token,
        }))
      : [];
  const chainOptions =
    data.length > 0
      ? Array.from(new Set(data.map((item) => item.chain))).map((chain) => ({
          value: chain,
          label: chain,
        }))
      : [];

  // Call onFilterChange whenever the filters change
  useEffect(() => {
    onFilterChange({
      tokens: selectedTokens.map((token) => token.value),
      chains: selectedChains.map((chain) => chain.value),
      minApy,
      minAmountSupplied,
    });
  }, [
    selectedTokens,
    selectedChains,
    minApy,
    minAmountSupplied,
    onFilterChange,
  ]);

  const handleResetFilters = () => {
    setSelectedTokens([]);
    setSelectedChains([]);
    setMinApy(0);
    setMinAmountSupplied(0);
    onFilterChange({
      tokens: [],
      chains: [],
      minApy: 0,
      minAmountSupplied: 0,
    });
  };

  return (
    <div className="flex justify-around p-5 filter-component">
      <div className="filter-group">
        <label>Select Tokens</label>
        <Select
          isMulti
          options={tokenOptions}
          value={selectedTokens}
          onChange={setSelectedTokens}
        />
      </div>

      <div className="filter-group">
        <label>Select Chains</label>
        <Select
          isMulti
          options={chainOptions}
          value={selectedChains}
          onChange={setSelectedChains}
        />
      </div>

      <div className="filter-group">
        <label>Minimum APY</label>
        <Slider
          min={0}
          max={100}
          value={minApy}
          onChange={setMinApy}
        />
        <span>{minApy}%</span>
      </div>

      <div className="filter-group">
        <label>Minimum Amount Supplied</label>
        <Slider
          min={0}
          max={1000000}
          value={minAmountSupplied}
          onChange={setMinAmountSupplied}
          onAfterChange={() =>
            onFilterChange({
              tokens: selectedTokens.map((token) => token.value),
              chains: selectedChains.map((chain) => chain.value),
              minApy,
              minAmountSupplied,
            })
          }
        />
        <span>{minAmountSupplied}</span>
      </div>
      <div>
        <button onClick={handleResetFilters}>Reset Filters</button>
      </div>
    </div>
  );
};

export default TableFilter;
