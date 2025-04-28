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

export async function editPlaylist(id, data) {
  try {
    data.videos = data.videos_in_playlist.map((item) => item.id);
    const response = await baseAPI.patch(`playlist/playlists/${id}/`, data);
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

export async function deletePlaylist(playlistId) {
  await baseAPI.delete(`/playlist/playlists/${playlistId}/`);
}
