import axios from '../api/axios.js';

const fetchData = async (api_endpoint) => {
  try {
    const response = await axios.get(`${api_endpoint}`);
    const transformedData = response.data.map((item, index) => ({
      ...item,
      sequentialId: index + 1,
      tvl_formatted2: Math.round(item.tvl),
      yield_rate_reward_formatted:
        item.yield_rate_reward === null || item.yield_rate_reward === 0
          ? ''
          : item.yield_rate_reward.toFixed(2),
      apy_sum: (
        parseFloat(item.yield_rate_base) +
        (item.yield_rate_reward ? parseFloat(item.yield_rate_reward) : 0)
      ).toFixed(2),
      information_formatted: Array.isArray(item.information)
        ? item.information.join(', ')
        : item.information || '',
    }));
    return transformedData;
  } catch (error) {
    console.error('Error fetching data:', error);
    return [];
  }
};

export default fetchData;
