<template>
    <div>
        {{ event.display_field }}
    </div>
</template>

<script>
export default {
  name: 'raw-widget',
  props: ['jobConfig', 'event'],
  computed: {
    config: function () {
      const defaultRawWidget = {
        'color': null
      }
      return Object.assign({}, defaultRawWidget, this.jobConfig.rawWidget)
    }
  }
}
</script>

<style>
</style>
