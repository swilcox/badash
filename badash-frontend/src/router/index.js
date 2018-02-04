import Vue from 'vue'
import Router from 'vue-router'
import VueResource from 'vue-resource'
import Home from '@/components/Home'
import Dashboard from '@/components/Dashboard'
import JobDetail from '@/components/JobDetail'
import Callback from '@/components/Callback'
import Settings from '@/components/Settings'
import Vuetify from 'vuetify'
import VueGoogleMaps from 'vue-googlemaps'
import GoogleConfig from '../../config/google'

Vue.use(Vuetify)
Vue.use(Router)
Vue.use(VueResource)
Vue.use(VueGoogleMaps, {
  load: {
    apiKey: GoogleConfig.mapsApiKey,
    libraries: ['places']
  }
})

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
    },
    {
      path: '/settings',
      component: Settings,
      name: 'settings'
    }
  ],
  mode: 'history'
})
