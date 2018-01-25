import Vue from 'vue'
import Router from 'vue-router'
import VueResource from 'vue-resource'
import Home from '@/components/Home'
import Dashboard from '@/components/Dashboard'
import JobDetail from '@/components/JobDetail'
import Callback from '@/components/Callback'
import Vuetify from 'vuetify'

Vue.use(Vuetify)
Vue.use(Router)
Vue.use(VueResource)

   // replace with env variable

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/dashboard/:slug',
      name: 'dashboard',
      component: Dashboard
    },
    {
      path: '/job/:slug',
      name: 'job-detail',
      component: JobDetail
    },
    {
      path: '/callback',
      component: Callback
    }
  ],
  mode: 'history'
})
