<template>
  <div v-if="isReady">
    <v-row class="px-4 pt-4">
      <v-col class="ps-4 pt-4" cols="12" style="max-width: 420px;">
        <v-card class="pb-4" tile outlined>
          <div class="pt-4 px-4 text-h6">Current Data</div>
          <div class="pt-4 px-4" v-for="station in stations" :key="station.id">
            <current-display :station="station" :data="data" :last-updated="lastUpdated" />
          </div>
        </v-card>
      </v-col>
      <v-col class="ps-4 pt-4" cols="12" style="max-width: 700px;" v-for="sensor in sensors" :key="sensor.mes_type">
        <chart-display :stations="stations" :data="data" :type="sensor" />
      </v-col>
    </v-row>
  </div>
  <loading v-else />
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

import ChartDisplay from '@/components/display/ChartDisplay.vue'
import CurrentDisplay from '@/components/display/CurrentDisplay.vue'
import Loading from '@/components/base/Loading.vue'
import { getStations, Sensor, Station } from '@/utils/getStations'
import { Measurement, getMeasurements } from '@/utils/getMeasurements'
import { SettingsModule } from '@/store/modules/settings'

@Component({
  components: { CurrentDisplay, ChartDisplay, Loading }
})
export default class ViewStation extends Vue {
  isReady = false
  lastUpdated?: string
  updaterId?: number

  stations: Station[] = []
  sensors: Sensor[] = []
  data: Measurement[] = []

  async created (): Promise<void> {
    const stationIds = this.$route.params.stations.split(',')

    // Get current stations
    const allStations = (await getStations())[0]
    const currStations = stationIds.map(id => allStations.find(item => item.id === id))
    this.stations = (currStations as Station[])

    // Check for non-existing stations
    if (!currStations.every(item => item)) {
      await this.$router.replace({
        name: 'notFound',
        params: { 0: this.$route.fullPath }
      })
      return
    }

    // Get available sensors
    let sensors = new Map<string, Sensor>()
    for (const station of this.stations) {
      for (const sensor of station.sensors) {
        sensors.set(sensor.mes_type, sensor)
      }
    }
    this.sensors = [...sensors.values()]

    // Set page title
    const stationNames = currStations.map(item => item?.name).join(', ')
    document.title = process.env.VUE_APP_TITLE + ' – ' + stationNames
    this.$emit('setPageTitle', 'Station – ' + stationNames)

    // Register measurements updater
    let fetchData = async () => {
      const newUpdated = (new Date()).toISOString()

      const [data, success] = await getMeasurements(stationIds, undefined, this.lastUpdated)
      if (!success) return

      // Combine with existing data and remove duplicates
      const combined = new Map<string, Measurement>()
      for (const item of this.data) combined.set(item.hash, item)
      for (const item of data) combined.set(item.hash, item)

      // Sort and save them
      this.data = [...combined.values()].sort((a, b) => (a.timestamp > b.timestamp) ? 1 : -1)
      this.lastUpdated = newUpdated
      console.log(this.data)
    }

    this.updaterId = setInterval(fetchData, SettingsModule.updateInterval * 1000)
    await fetchData()
    this.isReady = true
  }

  destroyed (): void {
    // Unregister measurements updater
    clearInterval(this.updaterId)
  }
}
</script>