import axios from 'axios';

const instance = axios.create({
  baseURL: 'https://www.tokendataview.com',
});

export default instance;
