<template>
  <v-container grid-list-md text-xs-center>
  <v-layout row wrap>
    <v-flex xs12>
      <h1>{{ job.title }}</h1>
      <h3>{{ job.description }}</h3>
      <display-field v-if="job.config" :jobConfig="job.config" :event="job.events[0]"></display-field>
        <v-expansion-panel expand>
          <v-expansion-panel-content v-for="event in job.events" :key="event.id">
            <div slot="header"><v-chip>{{ event.datetimestamp|formatDate }}</v-chip><status-widget :event="event"></status-widget> {{ event.display_field }}</div>
            <div>
              <display-field :jobConfig="job.config" :event="event"></display-field>
              <other-fields :event="event"></other-fields>
            </div>
          </v-expansion-panel-content>
        </v-expansion-panel>
    </v-flex>
  </v-layout>
  </v-container>
</template>

<script>
import OtherFields from '@/components/widgets/OtherFields'
import DisplayField from '@/components/DisplayField'
import StatusWidget from '@/components/widgets/StatusWidget'

export default {
  name: 'job-detail',
  props: ['slug'],
  data () {
    return {
      job: {
      }
    }
  },
  components: {
    OtherFields,
    StatusWidget,
    DisplayField
  },
  methods: {
    getJob () {
      this.$http.get(`jobs/${this.$route.params.slug}`).then(response => {
        this.job = response.body
      },
      response => {
        console.log(response.statusText)
      })
    }
  },
  created () {
    this.getJob()
  }
}
</script>

<style>
</style>