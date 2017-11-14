<template>
  <div class="dashboard-list">
    <h1>{{ msg }}</h1>
    <h2>Dashboards</h2>
  <div class="dashboard-list">
  </div>
    <ul class="dashboard-list">
      <li v-for="dash in dashboards" :key="dash.slug"><router-link :to="{ name: 'dashboard', params: { slug: dash.slug } }">{{ dash.title }}</router-link></li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data () {
    return {
      msg: 'BaDash',
      dashboards: []
    }
  },
  methods: {
    getDashboards () {
      this.$http
        .get('http://localhost:8000/dashboards').then(response => {
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

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    ul.dashboard-list {
        list-style: none;
    }
</style>
