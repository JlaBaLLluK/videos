import {createRouter, createWebHistory} from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'notFound',
    component: () => import('@/views/NotFound.vue'),
  },
  {
    path: '/registration',
    name: 'registration',
    component: () => import('@/views/auth/RegistrationView.vue'),
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

export default router;
