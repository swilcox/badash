<template>
    <div>
        <vue-markdown :source="event.display_field"></vue-markdown>
    </div>
</template>

<script>
import VueMarkdown from 'vue-markdown'

export default {
  name: 'markdown-widget',
  props: ['jobConfig', 'event'],
  computed: {
    config: function () {
      const defaultMarkdownWidget = {
        'color': null
      }
      return Object.assign({}, defaultMarkdownWidget, this.jobConfig.markdownWidget)
    }
  },
  components: {
    VueMarkdown
  }
}
</script>

<style>
</style>
