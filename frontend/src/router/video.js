export const videoRoutes = [
  {
    path: '/my-videos',
    children: [
      {
        path: 'published',
        name: 'publishedVideos',
        component: () => import('@/views/video/UserVideosView.vue')
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
    component: () => import('@/views/video/WatchLaterView.vue')
  }
];
