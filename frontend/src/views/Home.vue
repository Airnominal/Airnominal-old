<template>
  <v-row class="px-8 pt-8">
    <v-col>
      <div class="mt-2">
        TODO: Stuff
      </div>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

import { displaySnackbar } from '@/utils/snackbar'

@Component
export default class Home extends Vue {
  created (): void {
    // Display updated message
    if ('updated' in this.$route.query) {
      displaySnackbar('Successfully updated')
    }
  }
}
</script>
