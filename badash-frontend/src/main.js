// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
// import Vuetify from 'vuetify'
import moment from 'moment-timezone'
import('vuetify/dist/vuetify.min.css')

Vue.config.productionTip = false
// Vue.http.options.root = process.env.API_ROOT
Vue.http.options.root = process.env.API_BASE_URL
console.log(process.env.API_BASE_URL)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})

Vue.filter('formatDate', function (value) {
  if (value) {
    return moment(String(value)).format('YYYY-MM-DD hh:mm:ssa')
  }
})
