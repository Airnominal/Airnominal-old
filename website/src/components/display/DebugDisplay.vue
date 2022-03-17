<template>
  <div>
    <strong>{{ name }}</strong>
    <ul>
      <li v-for="measurement in measurements" :key="measurement.hash">
        {{measurement}}
      </li>
    </ul>
  </div>

</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

import { displaySnackbar } from '@/utils/snackbar'
import { Measurement, Platform, StorageModule } from '@/store/modules/storage'

@Component
export default class DebugDisplay extends Vue {
  @Prop() platform!: string

  get name (): string | undefined {
    return StorageModule.platforms.get(this.platform)?.name
  }

  get measurements (): Measurement[] {
    return [...StorageModule.measurements.values()].filter((item: Measurement) => item.platform == this.platform)
  }
}
</script>
