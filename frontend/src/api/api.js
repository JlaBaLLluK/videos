import axios from 'axios';
import router from '@/router/index.js';
import {toast} from 'bulma-toast';

const baseAPI = axios.create({
  baseURL: 'http://localhost:8000/api/v1/',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  }
});

baseAPI.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response.status === 404) {
      router.push({name: 'notFound'});
    } else if (error.response.status === 401) {
      toast({
        type: 'is-danger',
        position: 'top-center',
        message: 'Для выполнения этого действия необходимо войти в аккаунт.',
        duration: 3000,
      });
      router.push({name: 'login'});
    } else {
      return Promise.reject(error);
    }
  }
);

export default baseAPI;
