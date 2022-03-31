<!-- Component for displaying navigation between views on desktop -->

<template>
  <v-navigation-drawer :mini-variant="!isNavigationExpanded" app clipped mini-variant-width="72" permanent>
    <v-list rounded class="pt-6">
      <v-list-item link :to="{ name: 'stationsList' }">
        <v-list-item-icon>
          <v-icon>{{ mdiFormatListBulleted }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Stations List</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item link :to="{ name: 'stationsMap' }">
        <v-list-item-icon>
          <v-icon>{{ mdiMap }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Stations Map</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>

    <template v-slot:append>
      <v-list-item link @click="isNavigationExpanded = !isNavigationExpanded">
        <v-list-item-icon>
          <v-icon>{{ isNavigationExpanded ? mdiChevronLeft : mdiChevronRight }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title></v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </template>
  </v-navigation-drawer>
</template>

<style lang="scss">
// Fix jumping icons caused by closing expanded navigation drawer
.v-navigation-drawer--custom-mini-variant {
  .v-list-item {
    justify-content: unset !important;
  }
}
</style>

<script lang="ts">
import { mdiChevronLeft, mdiChevronRight, mdiFormatListBulleted, mdiMap } from '@mdi/js'
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class ViewNavigationDesktop extends Vue {
  mdiFormatListBulleted  = mdiFormatListBulleted
  mdiMap = mdiMap

  mdiChevronRight = mdiChevronRight
  mdiChevronLeft = mdiChevronLeft

  isNavigationExpanded = false
}
</script>
