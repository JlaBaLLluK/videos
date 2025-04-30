export const videoRoutes = [
  {
    path: '/my-videos',
    children: [
      {
        path: 'published',
        name: 'myVideos',
        component: () => import('@/views/video/VideosListView.vue')
      },
      {
        path: ':id',
        name: 'videoEdit',
        component: () => import('@/views/video/VideoEditView.vue')
      }
    ]
  },
  {
    path: '/watch-later',
    name: 'watchLater',
    component: () => import('@/views/video/VideosListView.vue')
  }
];
