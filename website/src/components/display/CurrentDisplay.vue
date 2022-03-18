<template>
  <div>
    <span class="subtitle-1">{{ station.name }}</span>
    <ul>
      <li>
        <strong>Last Updated:</strong>
        {{ lastUpdated }}
      </li>
      <li v-for="measurement in latest" :key="measurement.hash">
        <strong>{{ station.sensors.find(item => item.mes_type === measurement.data.name).name }}:</strong>
        {{ measurement.data.value }}
        {{ measurement.data.unit }}
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

import { Station } from '@/utils/getStations'
import { Measurement } from '@/utils/getMeasurements'

@Component
export default class CurrentDisplay extends Vue {
  @Prop() station!: Station
  @Prop() data!: Measurement[]
  @Prop() lastUpdated!: string

  get latest (): Measurement[] {
    let latestData = new Map<string, Measurement>()

    for (let measurement of this.data) {
      if (measurement.platform == this.station.id) {
        latestData.set(measurement.data.name, measurement)
      }
    }

    return [...latestData.values()]
  }
}
</script>
