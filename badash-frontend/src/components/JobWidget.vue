<template>
  <div class="widget pure-u-1 pure-u-md-1-2 pure-u-lg-1-3">
      <h2>{{ job.title }}</h2>
      <p v-if="this.job.events[0].result"><i class="fa fa-exclamation-triangle"></i></p>
      <p v-else><i class="fa fa-check-circle"></i></p>
      <p><span class="value">{{ this.job.events[0].value }}°</span></p>
      <p><span class="label">{{ this.job.events[0].datetimestamp|formatDate }}</span></p>
  </div>
</template>

<script>
export default {
  name: 'job-widget',
  props: ['job'],
  data () {
    return {
      other: {},
      event: this.job.events[0]
    }
  }
}
</script>

<style scoped>
.value {
    font-size: 400%;
}

.widget {
    border-radius: .5em;
    box-shadow: 2px 2px 2px 1px rgba(0, 0, 0, .2);
    padding: .5em;
}
</style>