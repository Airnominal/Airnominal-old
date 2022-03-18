<template>
  <v-card class="small" tile outlined>
    <line-chart class="ma-3" ref="chart" :chart-data="measurements" :options="options" />
    <v-card-actions>
      <v-btn small color="blue" text @click="zoomReset">All</v-btn>
      <v-btn small color="blue" text @click="zoomSet(24*60)">Last 24h</v-btn>
      <v-btn small color="blue" text @click="zoomSet(60)">Last 60min</v-btn>
      <v-btn small color="blue" text @click="zoomSet(10)">Last 10min</v-btn>
    </v-card-actions>
    <!--
    <v-card-actions class="mt-n3 text-actions">
      <span class="ps-3">Range:</span>
      <v-text-field dense hide-details type="datetime-local" class="inline-input mt-n2 mx-2">Test</v-text-field> —
      <v-text-field dense hide-details type="datetime-local" class="inline-input mt-n2 mx-2">Test</v-text-field>
    </v-card-actions>
    -->
  </v-card>
</template>

<style lang="scss">
.inline-input {
  max-width: 12rem !important;
}

.text-actions {
  font-size: 0.75rem !important;
  font-weight: 500;
  line-height: 2.25rem;
  letter-spacing: 0.0892857143em !important;
  font-family: "Roboto", sans-serif !important;
  text-transform: uppercase !important;
}
</style>

<script lang="ts">
import VComp from '@vue/composition-api'
import { Component, Prop, Ref, Vue, Watch } from 'vue-property-decorator'
import { ExtractComponentData, LineChart } from 'vue-chart-3'
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

  @Ref() readonly chart!: ExtractComponentData<typeof LineChart>

  currentZoom?: number
  userZoom = false

  created (): void {
    // Set chart title
    this.options.scales!.y!.title!.text = `${this.type.name} (${this.type.unit})`
    this.options.plugins!.title!.text = this.type.name

    // Prevent user-set zoom from resetting
    this.options.plugins!.zoom!.pan!.onPan = () => { this.userZoom = true }
    this.options.plugins!.zoom!.zoom!.onZoom = () => { this.userZoom = true }
  }

  mounted (): void {
    this.zoomSet(60)
  }

  zoomReset (): void {
    this.chart.chartInstance?.resetZoom('none')
    this.currentZoom = undefined
    this.userZoom = false
  }

  zoomSet (minutes: number): void {
    const chart = this.chart.chartInstance
    const scaleBounds = chart?.getInitialScaleBounds().x!
    const scaleLimits = chart?.scales.x!

    const dataMax = (scaleBounds.max || scaleLimits.max || 0) + 15000
    const dataMin = Math.max(dataMax - minutes*60*1000, scaleBounds.min || scaleLimits.min || 0)

    chart?.zoomScale('x', { min: dataMin, max: dataMax }, 'none')
    this.currentZoom = minutes
    this.userZoom = false
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
        },
        ticks: {
          autoSkip: true,
          autoSkipPadding: 25,
          maxRotation: 0,
          minRotation: 0,
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
          mode: 'x',
        },
        limits: {
          x: {
            minRange: 65 * 1000
          }
        }
      },
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

    // console.log(data)
    return data
  }

  @Watch('measurements')
  onMeasurementsChange() {
    // If user has not explicitly zoomed in, re-zoom to show the latest data
    if (this.userZoom) return

    this.chart.chartInstance?.resetZoom('none')
    if (this.currentZoom) this.zoomSet(this.currentZoom)
  }

}
</script>
