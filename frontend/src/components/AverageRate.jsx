import React from 'react';
import { styled } from '@mui/material/styles';
import Tooltip from '@mui/material/Tooltip';
import { tooltipClasses } from '@mui/material/Tooltip';

const LightTooltip = styled(({ className, ...props }) => (
  <Tooltip
    {...props}
    classes={{ popper: className }}
  />
))(({ theme }) => ({
  [`& .${tooltipClasses.tooltip}`]: {
    backgroundColor: theme.palette.common.white,
    color: 'rgba(0, 0, 0, 0.87)',
    boxShadow: theme.shadows[1],
    fontSize: 11,
  },
}));

const AverageYieldRate = ({ title, data, input, description, className }) => (
  <LightTooltip
    title={description || ''}
    placement="top"
  >
    <div
      className={`bg-white dark:bg-gray-800 shadow-md rounded-lg p-4 md:mb-0 ${className}`}
    >
      <h3 className="text-xl font-bold mb-2 flex items-center leading-tight">
        {title}
        {description && <span className="ml-2 text-gray-500">(?)</span>}
      </h3>
      <p className="text-lg">
        {data}
        {input}
      </p>
    </div>
  </LightTooltip>
);

export default AverageYieldRate;
