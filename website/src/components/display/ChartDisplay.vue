<template>
  <v-card class="pa-3 small" tile outlined>
    <line-chart :chart-options="chartOptions" :chart-data="measurements" />
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { Measurement, Platform, Sensor, StorageModule } from '@/store/modules/storage'

import LineChart from '@/components/charts/LineChart'

@Component({
  components: { LineChart }
})
export default class TextDisplay extends Vue {
  @Prop() platforms!: Platform[]
  @Prop() type!: Sensor

  chartOptions = {
    response: true,

    scales: {
      xAxes: [{
        type: 'time',
        time: {
          isoWeekday: true,
          tooltipFormat: 'll HH:mm:ss',
          displayFormats: {
            millisecond: 'HH:mm:ss.SSS',
            second: 'HH:mm:ss',
            minute: 'HH:mm',
            hour: 'HH'
          }
        }
      }]
    }
  }

  get measurements (): any {
    let source =  [...StorageModule.measurements.values()].filter((item: Measurement) => item.data.name == this.type.mes_type)

    let data: {
      datasets: {
        data: { x: any, y: any }[],
        fill: boolean,
        [_any: string | number | symbol]: unknown,
      }[]
    } = {
      datasets: []
    }

    // TODO: Improve this (set Y axis label, add platform name...)
    for (const platform of this.platforms) {
      const current = source.filter(item => item.platform == platform.id)
      data.datasets.push({
        data: current.map(data => ({x: data.timestamp, y: data.data.value})),
        fill: false,
        label: `${this.type.name} (${this.type.unit})`,
      })
    }

    console.log(data)
    return data
  }
}
</script>
