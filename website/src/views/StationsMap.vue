<template>
  <l-map class="full-page-map" :bounds="bounds" :zoom="zoom">
    <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
    <l-marker
      v-for="marker in markers"
      :key="marker.id"
      :visible="marker.visible"
      :draggable="marker.draggable"
      :lat-lng.sync="marker.position"
      :icon="marker.icon"
      @click="marker.onclick ? marker.onclick(marker) : () => {}">
      <l-tooltip :content="marker.tooltip" :options="{ permanent: true }" />
    </l-marker>
  </l-map>
</template>

<style lang="scss">
// Make sure all surrounding padding is removed
.full-page-map {
  height: calc(100vh - 64px) !important;
  width: calc(100% + 2 * 12px) !important;
  margin: -12px;
}

@media (max-width: 1063.75px) {
  .full-page-map {
    height: calc(100vh - 64px - 54px) !important;
  }
}

@media (max-width: 959.75px) {
  .full-page-map {
    height: calc(100vh - 58px - 54px) !important;
  }
}
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { LMap, LMarker, LTileLayer, LTooltip } from 'vue2-leaflet'
import { latLngBounds, LatLngBounds } from 'leaflet'

import { displaySnackbar } from '@/utils/snackbar'
import { fixMarkerIcons, Marker } from '@/utils/map'
import { getStations } from '@/utils/getStations'
import { getLatestMeasurements } from '@/utils/getMeasurements'
import { SettingsModule } from '@/store/modules/settings'

import 'leaflet/dist/leaflet.css'

fixMarkerIcons()

@Component({
  components: { LMap, LTileLayer, LMarker, LTooltip }
})
export default class StationsMap extends Vue {
  url = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
  attribution = '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors'
  bounds: LatLngBounds = latLngBounds([[0, 0]])
  zoom = 15

  markers: Marker[] = []
  updater?: number

  created (): void {
    // Display updated message
    if ('updated' in this.$route.query) {
      displaySnackbar('Successfully updated')
    }

    // Register stations updater
    this.updater = setInterval(this.fetchData, SettingsModule.updateInterval * 1000)
    this.fetchData()

    // Set page title
    document.title = process.env.VUE_APP_TITLE
    this.$emit('setPageTitle', 'Airnominal')
  }

  destroyed (): void {
    // Unregister stations updater
    clearInterval(this.updater)
  }

  async fetchData (): Promise<void> {
    const locations = new Map<string, Marker>()

    const stations = (await getStations())[0]
    const data = (await getLatestMeasurements())[0]

    for (let measurement of data) {
      // Get station for each data row
      const station = stations.find(station => station.id == measurement.platform)
      if (!station || !measurement.coordinates) continue

      // Store latest locations for each station
      locations.set(measurement.platform, {
        position: measurement.coordinates,
        tooltip: station.name,
        onclick: () => {
          this.$router.push({ name: 'viewStation', params: { stations: station.id }})
        }
      })
    }

    // Set map's markers and bounds
    this.markers = [...locations.values()]
    this.bounds = latLngBounds(this.markers.map(marker => marker.position || [0, 0])).pad(0.05)
  }
}
</script>
