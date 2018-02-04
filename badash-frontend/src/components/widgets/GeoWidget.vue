<template>
    <div>
      <googlemaps-map
        class="map"
        :center.sync="displayPosition"
        :zoom="config.zoom"
        :options="mapOptions">
        <googlemaps-marker
					title="Location"
					:position="displayPosition" />
      </googlemaps-map>
    </div>
</template>

<script>
export default {
  name: 'geo-widget',
  props: ['jobConfig', 'event'],
  computed: {
    config: function () {
      const defaultGeoWidget = {
        'zoom': 10
      }
      return Object.assign({}, defaultGeoWidget, this.jobConfig.geoWidget)
    },
    mapOptions () {
      return {
        clickableIcons: false
      }
    },
    displayPosition: function () {
      return this.event.display_field
    }
  }
}
</script>

<style>
  .map {
    height: 300px;
  }
</style>
