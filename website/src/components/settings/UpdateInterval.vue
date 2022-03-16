<template>
  <v-card width="35rem">
    <v-toolbar class="text-uppercase" color="primary" dark>
      Set Update Interval
    </v-toolbar>

    <v-card-text class="text--primary mb-n12">
      <v-text-field
        v-model="updateInterval"
        @keyup.enter="closeDialog"
        type="number"
        suffix="s"
        min="1"
        step="1"
        autofocus
        placeholder="Enter update interval (in seconds)"
      />
    </v-card-text>

    <v-card-actions class="justify-end">
      <v-btn text v-on:click=closeDialog>Ok</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

import { SettingsModule, ThemeType } from '@/store/modules/settings'

@Component
export default class UpdateInterval extends Vue {
  get updateInterval (): number {
    return SettingsModule.updateInterval
  }

  set updateInterval (updateInterval: number) {
    SettingsModule.setUpdateInterval(updateInterval)
  }

  closeDialog (): void {
    this.$emit('closeDialog')
  }
}
</script>
