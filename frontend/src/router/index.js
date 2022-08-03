import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import AuthorizationForm from '../components/AuthorizationForm.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/groups',
    name: 'Groups',
    component: function () {
      return import('../views/Groups.vue')
    }
  },
  {
    path: '/auth',
    name: 'Auth',
    component: AuthorizationForm
  },
  {
    path: '/upload',
    name: 'UploadedPictures',
    component: function () {
      return import('../views/UploadedPictures.vue')
    }
  }
]

const router = new VueRouter({
  routes
})

export default router
