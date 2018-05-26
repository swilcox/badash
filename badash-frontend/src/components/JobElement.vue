<template>
  <v-card>
    <v-card-title>
    <h2>{{ job.title }}</h2>
    <p><status-widget :event="this.job.events[0]"></status-widget></p>
    </v-card-title>
    <v-card-text>
      <display-field :jobConfig="config" :event="this.job.events[0]"></display-field>
      <p><v-chip>{{ this.job.events[0].datetimestamp|formatDate }}</v-chip></p>
    </v-card-text>
    <v-card-actions>
      <v-btn :to="{ name: 'job-detail', params: { jobSlug: job.slug } }">details</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import StatusWidget from '@/components/widgets/StatusWidget'
import DisplayField from '@/components/DisplayField'

export default {
  name: 'job-element',
  props: ['job'],
  computed: {
    'config': function () {
      const defaultConfig = {
        'widget': 'plain'
      }
      return Object.assign({}, defaultConfig, this.job.config)
    }
  },
  components: {
    StatusWidget,
    DisplayField
  }
}
</script>

<style>
</style>