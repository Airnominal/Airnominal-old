<template>
  <v-card class="small" tile outlined>
    <line-chart class="ma-3" ref="chart" :chart-data="measurements" :options="options" />
    <v-card-actions>
      <v-btn small color="blue" text @click="zoomReset">All</v-btn>
      <v-btn small color="blue" text @click="zoomSet(24*60)">Last 24h</v-btn>
      <v-btn small color="blue" text @click="zoomSet(60)">Last 60min</v-btn>
      <v-btn small color="blue" text @click="zoomSet(10)">Last 10min</v-btn>
    </v-card-actions>
    <v-card-actions class="mt-n4 text-actions">
      <span class="ps-3">Range:</span>
      <v-text-field dense hide-details type="datetime-local" class="inline-input mt-n1 mx-2" v-model="rangeStart" @change="handleRangeSelection" /> —
      <v-text-field dense hide-details type="datetime-local" class="inline-input mt-n1 mx-2" v-model="rangeEnd" @change="handleRangeSelection" />
    </v-card-actions>
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
import { SettingsModule } from '@/store/modules/settings'
import { getColor } from '@/utils/colors'
import { getLocalISOString } from '@/utils/date'

Chart.register(zoomPlugin, ...registerables)
Vue.use(VComp)

@Component({
  components: { LineChart }
})
export default class TextDisplay extends Vue {
  @Prop() stations!: Station[]
  @Prop() data!: Measurement[]
  @Prop() type!: Sensor

  @Ref() readonly chart!: ExtractComponentData<typeof LineChart>

  rangeStart: string | null = null
  rangeEnd: string | null = null

  currentZoom?: number
  userZoom = false

  created (): void {
    // Set chart title
    this.options.scales!.y!.title!.text = `${this.type.name} (${this.type.unit})`
    this.options.plugins!.title!.text = this.type.name

    // Prevent user-set zoom from resetting
    this.options.plugins!.zoom!.pan!.onPan = () => { this.userZoom = true }
    this.options.plugins!.zoom!.zoom!.onZoom = () => { this.userZoom = true }

    // Set query params to the current zoom
    const setQueryParams = (context: { chart: Chart }) => {
      if (!SettingsModule.storeRangeInURL || !this.userZoom) return

      const oldQuery = this.$router.currentRoute.query
      const newQuery = { ...oldQuery }

      newQuery.from = new Date(context.chart.scales.x.min).toISOString()
      newQuery.to = new Date(context.chart.scales.x.max).toISOString()

      this.rangeStart = getLocalISOString(newQuery.from)
      this.rangeEnd = getLocalISOString(newQuery.to)

      if (oldQuery.from !== newQuery.from || oldQuery.to !== newQuery.to) {
        this.$router.replace({ query: newQuery })
      }
    }
    this.options.plugins!.zoom!.pan!.onPanComplete = setQueryParams
    this.options.plugins!.zoom!.zoom!.onZoomComplete = setQueryParams
  }

  mounted (): void {
    const fromDate = Date.parse(this.$router.currentRoute.query.from as string)
    const toDate = Date.parse(this.$router.currentRoute.query.to as string)

    // Allow setting from and to dates using query params
    if (fromDate || toDate) {
      this.userZoom = true
      const chart = this.chart.chartInstance
      chart?.zoomScale('x', {
        min: fromDate || chart.scales.x.min,
        max: toDate || chart.scales.x.max
      }, 'none')
      this.rangeStart =  getLocalISOString(fromDate)
      this.rangeEnd = getLocalISOString(toDate)
      return
    }

    // Display last 60 minutes by default
    this.zoomSet(60)
  }

  resetQueryParams (): void {
    if (!SettingsModule.storeRangeInURL) return

    const query = { ...this.$router.currentRoute.query }
    let needsChange = !!(query.from || query.to)

    delete query.from
    delete query.to

    this.rangeStart = null
    this.rangeEnd = null

    if (needsChange) this.$router.replace({ query: query })
  }

  zoomReset (): void {
    this.userZoom = false
    this.resetQueryParams()

    this.chart.chartInstance?.resetZoom('none')
    this.currentZoom = undefined
    this.userZoom = false
  }

  zoomSet (minutes: number, force = true): void {
    this.userZoom = false
    if (force) this.resetQueryParams()

    const chart = this.chart.chartInstance
    const scaleBounds = chart?.getInitialScaleBounds().x!
    const scaleLimits = chart?.scales.x!

    const dataMax = (scaleBounds.max || scaleLimits.max || 0) + 15000
    const dataMin = Math.max(dataMax - minutes*60*1000, scaleBounds.min || scaleLimits.min || 0)

    chart?.zoomScale('x', { min: dataMin, max: dataMax }, 'none')
    this.currentZoom = minutes
  }

  handleRangeSelection (): void {
    this.userZoom = true
    if (!SettingsModule.storeRangeInURL) return

    const oldQuery = this.$router.currentRoute.query
    const newQuery = { ...oldQuery }

    if (this.rangeStart) newQuery.from = this.rangeStart
    else delete newQuery.from

    if (this.rangeEnd) newQuery.to = this.rangeEnd
    else delete newQuery.to

    if (oldQuery.from !== newQuery.from || oldQuery.to !== newQuery.to) {
      this.$router.replace({ query: newQuery })
    }

    const chart = this.chart.chartInstance
    const scaleBounds = chart?.getInitialScaleBounds().x!
    chart?.zoomScale('x', {
      min: this.rangeStart ? Date.parse(this.rangeStart) : scaleBounds.min,
      max: this.rangeEnd ? Date.parse(this.rangeEnd) :  scaleBounds.max
    }, 'none')
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
      const color = getColor(parseInt(platform.id))
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
  onMeasurementsChanged () {
    // If user has not explicitly zoomed in, re-zoom to show the latest data
    if (this.userZoom) return

    this.chart.chartInstance?.resetZoom('none')
    if (this.currentZoom) this.zoomSet(this.currentZoom, false)
  }
}
</script>
