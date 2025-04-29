import {createRouter, createWebHistory} from 'vue-router';
import {videoRoutes} from '@/router/video.js';
import {playlistRoutes} from '@/router/playlist.js';

const routes = [
  ...videoRoutes, ...playlistRoutes,
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
  },
  {
    path: '/results',
    name: 'searchResult',
    component: () => import('@/views/SearchResultView.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'notFound',
    component: () => import('@/views/NotFound.vue'),
  },
  {
    path: '/registration',
    children: [
      {
        path: '',
        name: 'registration',
        component: () => import('@/views/auth/RegistrationView.vue'),
      },
      {
        path: 'confirm',
        name: 'registrationConfirm',
        component: () => import('@/views/auth/RegistrationConfirmationView.vue'),
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/auth/LoginView.vue'),
  },
  {
    path: '/:username',
    name: 'profile',
    component: () => import('@/views/core/ProfileView.vue'),
    children: [
      {
        path: 'update',
        name: 'profileUpdate',
        component: () => import('@/views/core/ProfileUpdateView.vue'),
      },
      {
        path: 'subscribers',
        name: 'subscribersList',
        component: () => import('@/views/core/SubscribersListView.vue')
      },
      {
        path: 'video-upload',
        name: 'videoUpload',
        component: () => import('@/views/video/VideoUploadView.vue')
      },
      {
        path: 'videos',
        name: 'userVideos',
        component: () => import('@/views/video/UserVideosView.vue'),
      },
      {
        path: 'playlists',
        children: [
          {
            path: '',
            name: 'userPlaylists',
            component: () => import('@/views/playlist/UserPlaylistsListView.vue'),
          },
          {
            path: ':id',
            name: 'userPlaylistDetail',
            component: () => import('@/views/playlist/PlaylistDetailView.vue')
          }
        ]
      }
    ]
  },
  {
    path: '/subscriptions',
    name: 'subscriptionsList',
    component: () => import('@/views/core/SubscriptionsListView.vue')
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes: routes
});

router.beforeEach(async(to) => {
  if (to.name === 'registrationConfirm' && !localStorage.getItem('registeredUserData')) {
    await router.push({name: 'notFound'});
  }
});

export default router;
