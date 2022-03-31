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
export default class TextDisplay extends Vue {
  @Prop() stations!: Station[]
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
    let latestLocations = new Map<string, Marker>()
    let locationHistories = new Map<string, Polyline>()

    for (let measurement of this.data) {
      const station = this.stations.find(station => station.id == measurement.platform)
      if (!station || !measurement.coordinates) continue

      // Store latest locations for each station
      latestLocations.set(measurement.platform, {
        position: measurement.coordinates,
        tooltip: station.name,
      })

      // Store location history for each location
      let history = [...locationHistories.get(station.id)?.points || [], measurement.coordinates]
      locationHistories.set(station.id, { points: history, color: getColor(parseInt(station.id)) })
    }

    const markers = [...latestLocations.values()]
    const polylines = [...locationHistories.values()]
    const bounds = latLngBounds(markers.map(marker => marker.position || [0, 0]))

    this.bounds = bounds.pad(0.05)
    this.markers = markers
    this.polylines = polylines
  }

  mounted () {
    this.onDataChanged()
  }

}
</script>
