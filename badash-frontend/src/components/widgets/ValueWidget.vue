<template>
    <div>
        <v-progress-circular
            :size="100"
            :width="15"
            :rotate="90"
            :value="displayValue"
            :color="config.color"
            >
            {{ config.prefix }}{{ event.display_field }}{{ config.suffix }}
        </v-progress-circular>
    </div>
</template>

<script>
export default {
  name: 'value-widget',
  props: ['jobConfig', 'event'],
  computed: {
    config: function () {
      const defaultValueWidget = {
        'min': 0.0,
        'max': 100.0,
        'prefix': '',
        'suffix': '',
        'color': null
      }
      return Object.assign({}, defaultValueWidget, this.jobConfig.valueWidget)
    },
    displayValue: function () {
      return ((this.event.display_field - this.config.min) / (this.config.max - this.config.min)) * 100.0
    }
  }
}
</script>

<style>
</style>
