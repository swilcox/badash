<template>
  <div class="dashboard-view">
    <h1>Dashboard: {{ dashboard.title }}</h1>
    <hr/>
    <div class="jobs-container pure-g">
        <job-widget v-for="job in dashboard.jobs" :key="job.slug" :job="job" ></job-widget>
    </div>
  </div>
</template>

<script>
import JobWidget from './JobWidget'
export default {
  name: 'Dashboard',
  data () {
    return {
      dashboard: {}
    }
  },
  components: {
    JobWidget
  },
  methods: {
    getDashboards () {
      this.$http
        .get('http://localhost:8000/dashboards/' + this.$route.params.slug).then(response => {
          this.dashboard = response.body
        },
        response => {
          console.log(response.statusText)
        })
    }
  },
  created () {
    this.getDashboards()
    this.interval = setInterval(function () {
      this.getDashboards()
    }.bind(this), 30000)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    ul.dashboard-list {
        list-style: none;
    }
</style>
