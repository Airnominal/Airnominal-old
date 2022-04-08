<template>
  <v-card class="small" tile outlined>
    <l-map style="height: 504px;" :bounds="bounds" :zoom="zoom">
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
      <l-polyline
        v-for="item in polylines"
        :key="item.id"
        :lat-lngs="item.points"
        :visible="item.visible"
        :color="item.color"
      />
    </l-map>
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
import { LMap, LTileLayer, LMarker, LTooltip, LPolyline } from 'vue2-leaflet'
import { LatLngBounds, latLngBounds } from 'leaflet'

import { Station } from '@/utils/getStations'
import { Measurement } from '@/utils/getMeasurements'
import { getColor } from '@/utils/colors'
import { fixMarkerIcons, Marker, Polyline } from '@/utils/map'

import 'leaflet/dist/leaflet.css'

fixMarkerIcons()

@Component({
  components: { LMap, LTileLayer, LMarker, LTooltip, LPolyline }
})
export default class MapDisplay extends Vue {
  @Prop() stations!: Map<string, Station>
  @Prop() data!: Measurement[]

  url = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
  attribution = '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors'
  bounds: LatLngBounds = latLngBounds([[0, 0]])
  zoom = 15

  markers: Marker[] = []
  polylines: Polyline[] = []

  @Watch('data')
  @Watch('stations')
  onDataChanged () {
    performance.mark('view.map.begin')

    let latestLocations = new Map<string, Marker>()
    let locationHistories = new Map<string, Polyline>()

    for (let measurement of this.data) {
      if (!measurement.coordinates) continue

      // Get station for each data row
      const station = this.stations.get('' + measurement.platform)
      if (!station) continue

      // Store latest locations for each station
      latestLocations.set(measurement.platform, {
        position: measurement.coordinates,
        tooltip: station.name,
      })

      // Store location history for each location
      // If location history is already initialized, just add new location to array
      // Otherwise, create a new polyline object with the current location
      const history = locationHistories.get(measurement.platform)
      if (history && history.points) {
        history.points.push(measurement.coordinates)
      } else {
        locationHistories.set(measurement.platform, {
          points: [measurement.coordinates],
          color: getColor(parseInt(measurement.platform))
        })
      }
    }

    const markers = [...latestLocations.values()]
    const polylines = [...locationHistories.values()]
    const bounds = latLngBounds(markers.map(marker => marker.position || [0, 0])).pad(0.05)

    this.bounds = bounds
    this.markers = markers
    this.polylines = polylines

    performance.mark('view.map.end')
    performance.measure('view.map', 'view.map.begin', 'view.map.end')
  }

  mounted () {
    this.onDataChanged()
  }

}
</script>
