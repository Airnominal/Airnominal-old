<template>
  <v-row class="px-8 pt-8">
    <v-col>
      <v-list>
        <strong>Select Platform</strong>
        <v-list-item-group color="primary">
          <v-list-item v-for="[id, platform] in platforms" :key="id" link :to="{ name: 'viewPlatform', params: { platform: id } }">
            <v-list-item-content>
              <v-list-item-title v-text="platform.name"></v-list-item-title>
              <v-list-item-subtitle v-text="platform.description"></v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

import { displaySnackbar } from '@/utils/snackbar'
import TextDisplay from '@/components/display/TextDisplay.vue'
import ChartDisplay from '@/components/display/ChartDisplay.vue'
import { Platform, StorageModule } from '@/store/modules/storage'

@Component({
  components: { ChartDisplay, TextDisplay }
})
export default class Home extends Vue {
  get platforms (): Map<string, Platform> {
    return StorageModule.platforms
  }

  created (): void {
    // Display updated message
    if ('updated' in this.$route.query) {
      displaySnackbar('Successfully updated')
    }
  }
}
</script>
