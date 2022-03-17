<template>
  <div v-if="isReady">
    <v-row class="px-4 pt-4">
      <v-col class="ps-4 pt-4" cols="12" style="max-width: 420px;">
        <v-card class="pb-4" tile outlined>
          <div class="pt-4 px-4 text-h6">Current Data</div>
          <div class="pt-4 px-4" v-for="platform in platforms" :key="platform.id">
            <current-display :platform="platform" />
          </div>
        </v-card>
      </v-col>
      <v-col class="ps-4 pt-4" cols="12" style="max-width: 700px;" v-for="sensor in sensors" :key="sensor.mes_type">
        <chart-display :platforms="platforms" :type="sensor" />
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

import { Platform, Sensor, StorageModule } from '@/store/modules/storage'

@Component({
  components: { CurrentDisplay, ChartDisplay, Loading }
})
export default class ViewStation extends Vue {
  isReady = false

  get platforms (): Platform[] {
    const platformId = this.$route.params.stations.split(',')
    const platformInfo = platformId.map(id => StorageModule.platforms.get(id))
    return (platformInfo as Platform[])
  }

  get sensors (): Sensor[] {
    let sensors = new Map<string, Sensor>()

    // TODO: Properly remove duplicates
    for (const platform of this.platforms) {
      for (const sensor of platform.sensors) {
        sensors.set(sensor.mes_type, sensor)
      }
    }
    console.log(sensors)
    return [...sensors.values()]
  }

  async created (): Promise<void> {
    const platformId = this.$route.params.stations.split(',')

    // Update data
    await StorageModule.updatePlatforms()
    await StorageModule.updateMeasurements(platformId)

    // Handle invalid stations
    const platformInfo = platformId.map(id => StorageModule.platforms.get(id))
    if (!platformInfo.every(item => item)) {
      await this.$router.replace({ name: 'notFound', params: { 0: this.$route.fullPath } })
      return
    }

    // Set page title
    const platformName = platformInfo.map(item => item?.name).join(', ')
    document.title = process.env.VUE_APP_TITLE + ' – ' + platformName
    this.$emit('setPageTitle', 'Station – ' + platformName)

    this.isReady = true
  }
}
</script>
