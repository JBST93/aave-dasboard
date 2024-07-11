import axios from 'axios';

const instance = axios.create({
  baseURL: 'https://defi-dashboard-99d015fc546e.herokuapp.com/', // Replace with your Flask backend URL
});

export default instance;
