<template>
  <div>
    <span class="subtitle-1">{{ station.name }}</span>
    <ul>
      <li>
        <strong>Last Updated:</strong>
        {{ lastUpdated.replace('T', ' ').slice(0, 19) + ' Z' }}
      </li>
      <li>
        <strong>Last Data:</strong>
        {{ lastData }}
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
import { getLocalISOString } from '@/utils/date'

@Component
export default class CurrentDisplay extends Vue {
  @Prop() station!: Station
  @Prop() data!: Measurement[]
  @Prop() lastUpdated!: string

  lastData: string = 'No data'

  get latest (): Measurement[] {
    performance.mark('view.current.begin')

    let latestData = new Map<string, Measurement>()
    let latestDate: string | undefined = undefined

    for (let measurement of this.data) {
      if (measurement.platform == this.station.id) {
        latestData.set(measurement.data.name, measurement)
        latestDate = measurement.timestamp
      }
    }

    if (latestDate) {
      const converted = getLocalISOString(latestDate)
      if (converted) this.lastData = converted.replace('T', ' ').slice(0, 19) + ' Z'
    }

    performance.mark('view.current.end')
    performance.measure('view.current', 'view.current.begin', 'view.current.end')

    return [...latestData.values()]
  }
}
</script>
