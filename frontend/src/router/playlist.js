export const playlistRoutes = [
  {
    path: '/my-playlists',
    children: [
      {
        path: '',
        name: 'playlistsList',
        component: () => import('@/views/playlist/MyPlaylistsListView.vue')
      },
      {
        path: 'create',
        name: 'playlistCreate',
        component: () => import('@/views/playlist/PlaylistCreateView.vue')
      },
      {
        path: ':id/edit',
        name: 'playlistEdit',
        component: () => import('@/views/playlist/PlaylistEditView.vue')
      },
      {
        path: ':id',
        name: 'playlistDetail',
      }
    ]
  }
];
