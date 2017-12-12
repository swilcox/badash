<template>
    <div>
        {{ event.display_field }}
    </div>
</template>

<script>
export default {
  name: 'plain-widget',
  props: ['jobConfig', 'event'],
  computed: {
    config: function () {
      const defaultPlainWidget = {
        'color': null
      }
      return Object.assign({}, defaultPlainWidget, this.jobConfig.plainWidget)
    }
  }
}
</script>

<style>
</style>
