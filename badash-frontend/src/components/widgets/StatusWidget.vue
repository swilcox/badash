<template>
    <span v-if="event.result"><i class="fa fa-exclamation-triangle"></i></span>
    <span v-else><i class="fa fa-check-circle"></i></span>
</template>

<script>
export default {
  name: 'status-widget',
  props: ['event']
}
</script>
