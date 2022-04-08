<template>
  <v-row class="px-8 pt-8">
    <v-col>
      <v-list>
        <strong>Select Station</strong>
        <v-list-item-group color="primary">
          <v-list-item v-for="station in stations.values()" :key="station.id" :to="{ name: 'viewStation', params: { stations: station.id } }" link>
            <v-list-item-content>
              <v-list-item-title v-text="station.name"></v-list-item-title>
              <v-list-item-subtitle v-text="station.description"></v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-col>
  </v-row>
</template>

<style lang="scss">
.v-list.v-sheet.theme--dark {
  background-color: inherit;
}
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

import { displaySnackbar } from '@/utils/snackbar'
import { Station, getStations } from '@/utils/getStations'
import { SettingsModule } from '@/store/modules/settings'

@Component({})
export default class StationsList extends Vue {
  updater?: number
  stations = new Map<string, Station>()

  created (): void {
    // Display updated message
    if ('updated' in this.$route.query) {
      displaySnackbar('Successfully updated')
    }

    // Register stations updater
    let fetchData = async () => { this.stations = (await getStations())[0] }
    this.updater = setInterval(fetchData, SettingsModule.updateInterval * 1000)
    fetchData()

    // Set page title
    document.title = process.env.VUE_APP_TITLE
    this.$emit('setPageTitle', 'Airnominal')
  }

  destroyed (): void {
    // Unregister stations updater
    clearInterval(this.updater)
  }
}
</script>
