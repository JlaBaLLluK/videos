export const playlistRoutes = [
  {
    path: '/playlists',
    children: [
      {
        path: '',
        name: 'myPlaylistsList',
        component: () => import('@/views/playlist/PlaylistsListView.vue')
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
        component: () => import('@/views/playlist/PlaylistDetailView.vue')
      }
    ]
  }
];
