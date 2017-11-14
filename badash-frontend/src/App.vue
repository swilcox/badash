<template>
  <div id="app">
    <app-header id="app-header"></app-header>
    <router-view/>
    <app-footer id="app-footer"></app-footer>
  </div>
</template>

<script>
import AppHeader from './components/AppHeader'
import AppFooter from './components/AppFooter'
export default {
  name: 'app',
  components: {
    AppHeader,
    AppFooter
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.label {
  background-color: #2c3e50;
  border-radius: .5em;
  color: #fff;
  padding-left: .5em;
  padding-right: .5em;
}

.label-warning {
  background-color: #f0ad4e;
}

</style>
