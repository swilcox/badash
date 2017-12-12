<template>
    <v-list>
        <v-list-tile v-for="k in Object.keys(event)" :key="k">
            <v-list-tile-content>
                <v-list-tile-title>{{ k }}</v-list-tile-title>
                <v-list-tile-sub-title>{{ event[k] }}</v-list-tile-sub-title>
            </v-list-tile-content>
        </v-list-tile>
    </v-list>
</template>

<script>
export default {
  name: 'other-fields',
  props: ['event']
}
</script>

<style>
</style>