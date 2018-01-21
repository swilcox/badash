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
          <v-list-tile v-for="dash in dashboards" :key="dash.slug" :to="{ name: 'dashboard', params: { slug: dash.slug } }">
            <v-list-tile-action>
              <v-icon>dashboard</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>{{ dash.title }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-divider></v-divider>
          <v-list-tile @click="">
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
          <v-btn slot="activator"><v-icon>account_circle</v-icon></v-btn>
          <v-list>
            <login></login>
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
import Login from '@/components/Login'

export default {
  name: 'app',
  data: () => ({
    drawer: null,
    dashboards: []
  }),
  components: {
    Login
  },
  methods: {
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
