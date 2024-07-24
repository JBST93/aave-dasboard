import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://www.tokendataview.com',
});

export default instance;
