<template>
  <div>
    <value-widget v-if="jobConfig.widget === 'value'" :jobConfig="jobConfig" :event="event"></value-widget>
    <markdown-widget v-else-if="jobConfig.widget === 'markdown'" :jobConfig="jobConfig" :event="event"></markdown-widget>
    <raw-widget v-else-if="jobConfig.widget === 'raw'" :jobConfig="jobConfig" :event="event"></raw-widget>
    <plain-widget v-else :jobConfig="jobConfig" :event="event"></plain-widget>
  </div>
</template>

<script>
import ValueWidget from '@/components/widgets/ValueWidget'
import RawWidget from '@/components/widgets/RawWidget'
import PlainWidget from '@/components/widgets/PlainWidget'
import MarkdownWidget from '@/components/widgets/MarkdownWidget'

export default {
  name: 'display-field',
  props: ['jobConfig', 'event'],
  components: {
    ValueWidget,
    RawWidget,
    PlainWidget,
    MarkdownWidget
  }
}
</script>
