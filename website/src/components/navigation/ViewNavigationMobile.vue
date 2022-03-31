<!-- Component for displaying navigation between views on mobile -->

<template>
  <v-bottom-navigation fixed grow>
    <v-btn :to="{ name: 'stationsList' }">
      <span>Stations List</span>
      <v-icon>{{ mdiFormatListBulleted }}</v-icon>
    </v-btn>

    <v-btn :to="{ name: 'stationsMap' }">
      <span>Stations Map</span>
      <v-icon>{{ mdiMap }}</v-icon>
    </v-btn>
  </v-bottom-navigation>
</template>

<script lang="ts">
import { mdiFormatListBulleted, mdiMap } from '@mdi/js'
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class ViewNavigationMobile extends Vue {
  mdiFormatListBulleted  = mdiFormatListBulleted
  mdiMap = mdiMap
}
</script>
