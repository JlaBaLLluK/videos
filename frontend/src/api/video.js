import baseAPI from '@/api/api.js';
import {getMe} from '@/api/index.js';

export async function getVideos(endpoint) {
  try {
    const response = await baseAPI.get(endpoint);
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

export async function deleteVideo(videoId) {
  await baseAPI.delete(`video/videos/${videoId}/`);
  await getMe();
}
