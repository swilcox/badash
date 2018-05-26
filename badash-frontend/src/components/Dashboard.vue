<template>
<v-container grid-list-md text-xs-center>
  <v-layout row wrap>
    <v-flex xs12>
    <h1>{{ dashboard.title }}</h1>
    </v-flex>
  
    <v-flex md4 sm6 xs12 v-for="job in dashboard.jobs" :key="job.slug">
      <job-element :job="job" ></job-element> 
    </v-flex>
  
  </v-layout>
</v-container>
</template>

<script>
import JobElement from './JobElement'

export default {
  name: 'Dashboard',
  data () {
    return {
      dashboard: {}
    }
  },
  components: {
    JobElement
  },
  methods: {
    getDashboards () {
      if (this.$route.params.dashboardSlug !== undefined) {
        this.$http.get('dashboards/' + this.$route.params.dashboardSlug).then(response => {
          this.dashboard = response.body
        },
        response => {
          console.log(response.statusText)
        })
      }
    }
  },
  watch: {
    '$route.params.dashboardSlug': function (slug) {
      if (slug !== undefined) {
        this.getDashboards()
      }
    }
  },
  mounted () {
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
