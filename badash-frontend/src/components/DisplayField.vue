<template>
  <div>
    <value-widget v-if="jobConfig.widget === 'value'" :jobConfig="jobConfig" :event="event"></value-widget>
    <markdown-widget v-else-if="jobConfig.widget === 'markdown'" :jobConfig="jobConfig" :event="event"></markdown-widget>
    <raw-widget v-else-if="jobConfig.widget === 'raw'" :jobConfig="jobConfig" :event="event"></raw-widget>
    <geo-widget v-else-if="jobConfig.widget === 'geo'" :jobConfig="jobConfig" :event="event"></geo-widget>
    <plain-widget v-else :jobConfig="jobConfig" :event="event"></plain-widget>
  </div>
</template>

<script>
import ValueWidget from '@/components/widgets/ValueWidget'
import RawWidget from '@/components/widgets/RawWidget'
import PlainWidget from '@/components/widgets/PlainWidget'
import MarkdownWidget from '@/components/widgets/MarkdownWidget'
import GeoWidget from '@/components/widgets/GeoWidget'

export default {
  name: 'display-field',
  props: ['jobConfig', 'event'],
  components: {
    ValueWidget,
    RawWidget,
    PlainWidget,
    MarkdownWidget,
    GeoWidget
  }
}
</script>
