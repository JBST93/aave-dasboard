import axios from 'axios';

const instance = axios.create({
  baseURL: 'https://defi-dashboard-99d015fc546e.herokuapp.com/',
});

export default instance;
