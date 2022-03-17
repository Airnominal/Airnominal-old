<template>
  <div>
    <span class="subtitle-1">{{ platform.name }}</span>
    <ul>
      <li>
        <strong>Last Updated:</strong>
        {{ lastUpdated }}
      </li>
      <li v-for="measurement in latest" :key="measurement.hash">
        <strong>{{ platform.sensors.find(item => item.mes_type === measurement.data.name).name }}:</strong>
        {{ measurement.data.value }}
        {{ measurement.data.unit }}
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

import { displaySnackbar } from '@/utils/snackbar'
import { Measurement, Platform, StorageModule } from '@/store/modules/storage'

@Component
export default class CurrentDisplay extends Vue {
  @Prop() platform!: Platform

  get lastUpdated (): string {
    return StorageModule.lastUpdated || 'No data'
  }

  get latest (): Measurement[] {
    let latestData = new Map<string, Measurement>()
    for (let measurement of StorageModule.measurements.values()) {
      if (measurement.platform == this.platform.id) latestData.set(measurement.data.name, measurement)
    }
    return [...latestData.values()]
  }
}
</script>
