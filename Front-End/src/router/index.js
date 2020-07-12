import Vue from 'vue'
import VueRouter from 'vue-router'

import Index from '@/components/Index'
import Home from '@/components/Home'
import Profile from '@/components/Profile'
import Login from '@/components/Login'
import Logout from '@/components/Logout'
import Search from '@/components/Search'
import Takings from '@/components/Takings'
import Watchings from '@/components/Watchings'
import Notifications from '@/components/Notifications'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'index',
    component: Index
  },
  {
    path: '/home',
    name: 'home',
    component: Home
  },
  {
    path: '/profile',
    name: 'profile',
    component: Profile
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/logout',
    name: 'logout',
    component: Logout
  },
  {
    path: '/search',
    name: 'search',
    component: Search
  },
  {
    path: '/takings',
    name: 'takings',
    component: Takings
  },
  {
    path: '/watchings',
    name: 'watchings',
    component: Watchings
  },
  {
    path: '/notifications',
    name: 'notifications',
    component: Notifications
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
