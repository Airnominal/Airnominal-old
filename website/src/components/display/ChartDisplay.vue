<template>
  <v-card class="pa-3 small" tile outlined>
    <line-chart :chart-data="measurements" :options="options" />
  </v-card>
</template>

<script lang="ts">
import VComp from '@vue/composition-api'
import { Component, Prop, Vue } from 'vue-property-decorator'
import { LineChart } from 'vue-chart-3'
import { Chart, ChartOptions, LinearScaleOptions, registerables } from 'chart.js'
import zoomPlugin from 'chartjs-plugin-zoom'

import 'chartjs-adapter-date-fns'
import { Sensor, Station } from '@/utils/getStations'
import { Measurement } from '@/utils/getMeasurements'

Chart.register(zoomPlugin, ...registerables)
Vue.use(VComp)

const colors = [
  '#F44336',
  '#9C27B0',
  '#3F51B5',
  '#00BCD4',
  '#4CAF50',
  '#CDDC39',
  '#FFC107',
  '#FF5722'
]

@Component({
  components: { LineChart }
})
export default class TextDisplay extends Vue {
  @Prop() stations!: Station[]
  @Prop() data!: Measurement[]
  @Prop() type!: Sensor

  created (): void {
    this.options.scales!.y!.title!.text = `${this.type.name} (${this.type.unit})`
    this.options.plugins!.title!.text = this.type.name
  }

  options: ChartOptions<'line'> = {
    scales: {
      x: {
        type: 'time',
        time: {
          isoWeekday: true,
          tooltipFormat: 'yyyy-MM-dd HH:mm',
          displayFormats: {
            millisecond: 'HH:mm:ss.SSS',
            second: 'HH:mm:ss',
            minute: 'HH:mm',
            hour: 'HH:mm'
          }
        }
      },
      y: {
        title: {
          display: true
        }
      }
    },
    plugins: {
      title: {
        display: true,
        font: { size: 16 },
      },
      zoom: {
        pan: {
          enabled: true,
          modifierKey: 'alt',
          mode: 'x',
        },
        zoom: {
          drag: { enabled: true, modifierKey: 'ctrl' },
          wheel: { enabled: true },
          pinch: { enabled: true },
          mode: 'x'
        }
      }
    },
    animation: false,
  }

  get measurements (): any {
    let source = this.data.filter((item: Measurement) => item.data.name == this.type.mes_type)

    let data: {
      datasets: {
        data: { x: any, y: any }[],
        fill: boolean,
        [_any: string | number | symbol]: unknown,
      }[]
    } = {
      datasets: []
    }

    let values: number[] = []

    for (const platform of this.stations) {
      const color = colors[parseInt(platform.id) % colors.length]
      const current = source.filter(item => item.platform == platform.id)

      values.push(...current.map(value => value.data.value))

      data.datasets.push({
        data: current.map(data => ({ x: data.timestamp, y: data.data.value })),
        label: platform.name,
        backgroundColor: color,
        borderColor: color,
        fill: false,
        tension: 0.1
      })
    }

    (this.options.scales!.y as LinearScaleOptions)!.suggestedMin = Math.max(Math.min(...values) - 5, 0);
    (this.options.scales!.y as LinearScaleOptions)!.suggestedMax = Math.max(...values) + 5

    console.log(data)
    return data
  }
}
</script>
