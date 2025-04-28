import baseAPI from '@/api/api.js';

export async function createPlaylist(data) {
  try {
    const response = await baseAPI.post('/playlist/playlists/', data);
    return {
      data: response.data,
      status: response.status
    };
  } catch (error) {
    return {
      data: error.response.data,
      status: error.status
    };
  }
}

export async function getPlaylists() {
  const response = await baseAPI.get('/playlist/playlists/');
  return response.data;
}
