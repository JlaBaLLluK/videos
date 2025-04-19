import axios from 'axios';
import router from '@/router/index.js';
import createAuthRefreshInterceptor from 'axios-auth-refresh';
import {refreshToken} from '@/api/index.js';
import {errorToast} from '@/plugins/toasts.js';

const baseAPI = axios.create({
  baseURL: 'http://localhost:8000/api/v1/',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  }
});

async function refreshLogic() {
  try {
    await refreshToken();
  } catch (e) {
    errorToast('Для выполнения этого действия необходимо войти в аккаунт');
    await router.push({name: 'login'});
  }
}

createAuthRefreshInterceptor(baseAPI, refreshLogic);

baseAPI.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response.status === 404) {
      router.push({name: 'notFound'});
    }
    else {
      return Promise.reject(error);
    }
  }
);

export default baseAPI;
