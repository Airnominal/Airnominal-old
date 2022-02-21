<template>
  <div class="settings px-4 pt-4">
    <!-- TODO: Add settings actions here -->

   <!--  <settings-action v-model="entitySelectionDialog"
      :icon="mdiTuneVariant"
      :label="selectedEntityLabel"
      :message="selectedEntity" />

    <settings-action v-model="snackSelectionDialog"
      :icon="mdiTuneVariant"
      :message="selectedSnack"
      label="Izbrana malica" />

    <settings-action v-model="lunchSelectionDialog"
      :icon="mdiTuneVariant"
      :message="selectedLunch"
      label="Izbrano kosilo" /> -->

    <v-divider class="mt-6" />

    <!-- TODO: Add settings switches here -->

    <settings-switch v-model="showSubstitutions" label="Prikaži nadomeščanja" />
    <settings-switch v-model="showLinksInTimetable" label="Prikaži povezave v urniku" />
    <settings-switch v-model="showHoursInTimetable" label="Prikaži ure v urniku" />
    <settings-switch v-model="enablePullToRefresh" label="Pull to Refresh" />
    <settings-switch v-model="enableUpdateOnLoad" label="Updates on Load" />

    <v-divider class="my-6" />

    <settings-action v-model="themeSelectionDialog"
      :icon="mdiWeatherNight"
      :message="themeStatus"
      label="Color Theme" />

    <v-divider class="my-6" />

    <settings-action :icon="mdiUpdate"
      :message="`Current version: ${appVersion}`"
      label="Update app"
      @click.native="updateApp" />

    <settings-action :icon="mdiUpdate"
      :message="`Current version: ${dataVersion}`"
      label="Update data"
      @click.native="updateData" />

    <!-- TODO: Add settings dialogs (for settings actions) here -->

    <v-dialog v-model="entitySelectionDialog" width="35rem">
      <entity-selection v-if="entitySelectionDialog"
        initial-selection-stage="1"
        is-dialog="1"
        @closeDialog=closeEntityDialog />
    </v-dialog>

    <v-dialog v-model="snackSelectionDialog" width="35rem">
      <snack-selection v-if="snackSelectionDialog" @closeDialog=closeSnackDialog />
    </v-dialog>

    <v-dialog v-model="lunchSelectionDialog" width="35rem">
      <lunch-selection v-if="lunchSelectionDialog" @closeDialog=closeLunchDialog />
    </v-dialog>

    <v-dialog v-model="themeSelectionDialog" width="35rem">
      <theme-selection v-if="themeSelectionDialog" @closeDialog=closeThemeDialog />
    </v-dialog>
  </div>
</template>

<style lang="scss">
// Add back top padding that is removed by a dialog
.v-dialog > .v-card > .v-card__text {
  padding: 16px 24px 20px !important;
}

// Center settings page
.settings {
  margin: 0 auto;
  max-width: 40rem;
}
</style>

<script lang="ts">
import { mdiTuneVariant, mdiUpdate, mdiWeatherNight } from '@mdi/js'
import { Component, Vue } from 'vue-property-decorator'

import SettingsAction from '@/components/settings/SettingsAction.vue'
import SettingsSwitch from '@/components/settings/SettingsSwitch.vue'
import ThemeSelection from '@/components/settings/ThemeSelection.vue'
import { SettingsModule, ThemeType } from '@/store/modules/settings'
import { StorageModule, updateAllData } from '@/store/modules/storage'

@Component({
  components: {
    ThemeSelection,
    SettingsAction,
    SettingsSwitch,
  }
})
export default class Settings extends Vue {
  mdiTuneVariant = mdiTuneVariant
  mdiWeatherNight = mdiWeatherNight
  mdiUpdate = mdiUpdate

  // Get app version
  get appVersion (): string {
    return process.env.VUE_APP_VERSION || 'No data'
  }

  // Get data version
  get dataVersion (): string {
    if (!StorageModule.lastUpdated) return 'No data'

    const lastUpdated = typeof StorageModule.lastUpdated === 'string' ? new Date(StorageModule.lastUpdated) : StorageModule.lastUpdated
    return lastUpdated.toISOString()
  }

  // TODO: Add other values here

  // Get theme type as string from enum
  get themeStatus (): string {
    switch (SettingsModule.theme) {
      case ThemeType.System:
        return 'System'
      case ThemeType.Light:
        return 'Light'
      case ThemeType.Dark:
        return 'Dark'
    }
  }

  // Dialog states
  // TODO: Add dialog states here
  entitySelectionDialog = false
  snackSelectionDialog = false
  lunchSelectionDialog = false
  themeSelectionDialog = false

  // TODO: Add other toggles here

  // Sync toggles with Vuex state
  get showSubstitutions (): boolean {
    return SettingsModule.showSubstitutions
  }

  set showSubstitutions (showSubstitutions: boolean) {
    SettingsModule.setShowSubstitutions(showSubstitutions)
  }

  get showLinksInTimetable (): boolean {
    return SettingsModule.showLinksInTimetable
  }

  set showLinksInTimetable (showLinksInTimetable: boolean) {
    SettingsModule.setShowLinksInTimetable(showLinksInTimetable)
  }

  get showHoursInTimetable (): boolean {
    return SettingsModule.showHoursInTimetable
  }

  set showHoursInTimetable (showHoursInTimetable: boolean) {
    SettingsModule.setShowHoursInTimetable(showHoursInTimetable)
  }

  get enablePullToRefresh (): boolean {
    return SettingsModule.enablePullToRefresh
  }

  set enablePullToRefresh (enablePullToRefresh: boolean) {
    SettingsModule.setEnablePullToRefresh(enablePullToRefresh)
  }

  get enableUpdateOnLoad (): boolean {
    return SettingsModule.enableUpdateOnLoad
  }

  set enableUpdateOnLoad (enableUpdateOnLoad: boolean) {
    SettingsModule.setEnableUpdateOnLoad(enableUpdateOnLoad)
  }

  // Prepare view
  created (): void {
    document.title = process.env.VUE_APP_TITLE + ' – Settings'
    this.$emit('setPageTitle', 'Settings')
    this.$emit('setPullToRefreshAllowed', false)
  }

  destroyed (): void {
    this.$emit('setPullToRefreshAllowed', true)
  }

  // Handle update requests
  async updateApp (): Promise<void> {
    if (process.env.NODE_ENV === 'production' && navigator.serviceWorker && navigator.serviceWorker.controller) {
      // Skip service worker waiting
      navigator.serviceWorker.controller.postMessage({ type: 'SKIP_WAITING' })
      await new Promise(resolve => setTimeout(resolve, 200))
    }

    // Add GET parameter to invalidate cache of index HTML file
    window.location.href = location.protocol + '//' + location.host + '?updated=' + (new Date()).getTime()
  }

  async updateData (): Promise<void> {
    await updateAllData()
  }

  // Handle dialogs
  // TODO: Add other dialog close functins here
  closeEntityDialog (): void {
    this.entitySelectionDialog = false
  }

  closeSnackDialog (): void {
    this.snackSelectionDialog = false
  }

  closeLunchDialog (): void {
    this.lunchSelectionDialog = false
  }

  closeThemeDialog (): void {
    this.themeSelectionDialog = false
  }
}
</script>
