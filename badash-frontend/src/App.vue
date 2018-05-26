<template>
  <div id="app">
    <v-app dark>
      <v-navigation-drawer
        clipped
        fixed
        v-model="drawer"
        app
      >
        <v-list dense>
          <v-subheader>Dashboards</v-subheader>
          <v-list-tile v-for="dash in dashboards" :key="dash.slug" :to="{ name: 'dashboard', params: { dashboardSlug: dash.slug } }">
            <v-list-tile-action>
              <v-icon>dashboard</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>{{ dash.title }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-divider></v-divider>
          <v-list-tile :to="{ name: 'settings' }" v-if="isLoggedIn()">
            <v-list-tile-action>
              <v-icon>settings</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>Settings</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-navigation-drawer>
      <v-toolbar app fixed clipped-left>
        <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
        <v-toolbar-title><router-link :to="{ name: 'home' }"><img class="header-logo" src="./assets/badash-logo.png"></router-link></v-toolbar-title>
        <v-spacer></v-spacer>
        <v-menu offset-y>
          <v-btn icon slot="activator"><v-icon v-if="!isLoggedIn()">account_box</v-icon>
          <v-avatar v-if="isLoggedIn()"><img :src="getUserInfo().picture"/></v-avatar>
          </v-btn>
          <v-list>
            <v-list-tile v-if="isLoggedIn()">    
              <v-list-tile-title>{{ getUserInfo().nickname }}</v-list-tile-title>
            </v-list-tile>
            <v-list-tile v-if="!isLoggedIn()" @click="handleLogin()">
              <v-list-tile-action>
                <v-list-tile-action><v-icon>account_circle</v-icon></v-list-tile-action>
              </v-list-tile-action>
              <v-list-tile-content>
                <v-list-tile-title>Log In</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-list-tile v-if="isLoggedIn()" @click="handleLogout()">
              <v-list-tile-action>
                <v-list-tile-action><v-icon>exit_to_app</v-icon></v-list-tile-action>
              </v-list-tile-action>
              <v-list-tile-content>
                <v-list-tile-title>Sign Out</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>
        </v-menu>
      </v-toolbar>
      <v-content>
        <v-container fluid fill-height>
          <v-fade-transition mode="out-in">
            <router-view></router-view>
          </v-fade-transition>
        </v-container>
      </v-content> 
      <v-footer app fixed>BADash</v-footer>     
    </v-app>
  </div>
</template>

<script>
import { isLoggedIn, login, logout, getUserProfile } from '@/utils/auth'

export default {
  name: 'app',
  data: () => ({
    drawer: null,
    dashboards: []
  }),
  methods: {
    handleLogin () {
      login()
    },
    handleLogout () {
      logout()
    },
    isLoggedIn () {
      return isLoggedIn()
    },
    getUserInfo () {
      return getUserProfile()
    },
    getDashboards () {
      this.$http
        .get('dashboards').then(response => {
          this.dashboards = response.body['dashboard_list']
        },
        response => {
          console.log(response.statusText)
        })
    }
  },
  beforeMount () {
    this.getDashboards()
  }
}
</script>

<style>
  .header-logo {
      height: 2em;
      margin: 5px 0px -5px 5px;
      padding: 0px 0px -5px 0px;
  }

</style>
