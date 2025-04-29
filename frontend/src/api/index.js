import baseAPI from '@/api/api.js';

export async function userRegistration(credentials) {
  try {
    const response = await baseAPI.post('core/users/', credentials);
    return {
      data: response.data,
      status: response.status
    };
  } catch (error) {
    return {
      data: error.response.data,
      status: error.response.status
    };
  }
}

export async function userRegistrationConfirmation(username) {
  const response = await baseAPI.patch('core/users/registration-confirm/', {username: username});
  return response.data.message;
}

export async function userLogin(credentials) {
  try {
    const response = await baseAPI.post('auth/login/', credentials);
    const {access, refresh} = response.data;
    localStorage.setItem('accessToken', access);
    localStorage.setItem('refreshToken', refresh);
    baseAPI.defaults.headers['Authorization'] = `Bearer ${access}`;
    await getMe();
    window.dispatchEvent(new Event('user-login'));
    return {
      data: response.data,
      status: response.status
    };
  } catch (error) {
    return {
      data: error.response.data,
      status: error.response.status
    };
  }
}

export async function sendResetPasswordCode(username) {
  try {
    const response = await baseAPI.get(`core/users/${username}/send-reset-password-code/`);
    return {
      data: response.data,
      status: response.status
    };
  } catch (error) {
    return {
      data: error.response.data,
      status: error.response.status
    };
  }
}

export async function resetPassword(username) {
  await baseAPI.patch(`core/users/${username}/reset-password/`);
}

export async function userDelete(username, password) {
  console.log(password);
  try {
    const response = await baseAPI.delete(`core/users/${username}/`, {
      params: {
        password: password,
      }
    });
    return {
      data: response.data,
      status: response.status
    };
  } catch (error) {
    return {
      data: error.response.data,
      status: error.response.status
    };
  }
}

export async function getMe() {
  const response = await baseAPI.get('core/users/me');
  localStorage.setItem('user', JSON.stringify(response.data));
}

export async function userLogout() {
  try {
    const data = {
      'refresh': localStorage.getItem('refreshToken')
    };
    await baseAPI.post('auth/logout/', data);
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    baseAPI.defaults.headers['Authorization'] = '';
    window.dispatchEvent(new Event('user-logout'));
  } catch (error) {
    console.error(error);
  }
}

export async function getUserData(username) {
  try {
    const response = await baseAPI.get(`core/users/${username}/`);
    return {
      data: response.data,
      status: response.status
    };
  } catch (error) {
    return {
      data: error.response.data,
      status: error.response.status
    };
  }
}

export async function updateUserData(username, data) {
  try {
    const response = await baseAPI.patch(`core/users/${username}/`, data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    });
    await getMe();
    return {
      data: response.data,
      status: response.status
    };
  } catch (error) {
    return {
      data: error.response.data,
      status: error.response.status,
    };
  }
}

export async function updateUserPassword(data) {
  try {
    const response = await baseAPI.patch('/core/users/update-password/', data);
    return {
      data: response.data,
      status: response.status
    };
  } catch (error) {
    return {
      data: error.response.data,
      status: error.response.status
    };
  }
}

export async function subscribe(username) {
  try {
    const response = await baseAPI.put(`core/users/${username}/subscribe/`);
    return {
      data: response.data,
      status: response.status,
    };
  } catch (error) {
    return {
      data: error.response.data,
      status: error.response.status,
    };
  }
}

export async function getUsersList(url) {
  try {
    const response = await baseAPI.get(url);
    return {
      data: response.data,
      status: response.status,
    };
  } catch (error) {
    return {
      data: error.response.data,
      status: error.response.status,
    };
  }
}

export async function search(queryParans) {
  const response = await baseAPI.get('core/search/', {params: queryParans});
  return response.data;
}
