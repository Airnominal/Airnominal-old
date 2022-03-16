<template>
  <div v-if="isReady">
    <v-row class="px-8 pt-8" v-for="sensor in sensors" :key="sensor.mes_type">
      <!-- TODO: Improve display -->
      <chart-display class="ma-3" :platforms="platforms" :type="sensor" />
    </v-row>
  </div>
  <loading v-else />
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

import { displaySnackbar } from '@/utils/snackbar'
import TextDisplay from '@/components/display/TextDisplay.vue'
import ChartDisplay from '@/components/display/ChartDisplay.vue'
import { Platform, Sensor, StorageModule } from '@/store/modules/storage'
import Loading from '@/components/base/Loading.vue'

@Component({
  components: { Loading, ChartDisplay, TextDisplay }
})
export default class ViewPlatform extends Vue {
  isReady = false

  get platforms (): Platform[] {
    const platformId = this.$route.params.platform.split(',')
    const platformInfo = platformId.map(id => StorageModule.platforms.get(id))
    return (platformInfo as Platform[])
  }

  get sensors (): Sensor[] {
    let sensorList = new Set<Sensor>()
    // TODO: Properly remove duplicates
    for (const platform of this.platforms) {
      for (const sensor of platform.sensors) {
        sensorList.add(sensor)
      }
    }
    console.log(sensorList)
    return [...sensorList]
  }

  async created (): Promise<void> {
    const platformId = this.$route.params.platform.split(',')

    // Update data
    await StorageModule.updatePlatforms()
    await StorageModule.updateMeasurements(platformId)

    // Handle invalid platforms
    const platformInfo = platformId.map(id => StorageModule.platforms.get(id))
    if (!platformInfo.every(item => item)) {
      await this.$router.replace({ name: 'notFound', params: { 0: this.$route.fullPath } })
      return
    }

    // Set page title
    const platformName = platformInfo.map(item => item?.name).join(', ')
    document.title = process.env.VUE_APP_TITLE + ' – ' + platformName
    this.$emit('setPageTitle', 'Platform – ' + platformName)

    this.isReady = true
  }
}
</script>
