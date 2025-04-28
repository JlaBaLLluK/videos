export const playlistRoutes = [
  {
    path: '/playlists',
    children: [
      {
        path: '',
        name: 'playlistsList',
        component: () => import('@/views/playlist/PlaylistsListView.vue')
      },
      {
        path: 'create',
        name: 'playlistCreate',
        component: () => import('@/views/playlist/PlaylistCreateView.vue')
      }
    ]
  }
];
