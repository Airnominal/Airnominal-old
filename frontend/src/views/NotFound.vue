<template>
  <v-row class="px-8 pt-8">
    <v-col>
      <div class="paragraph-text mt-2">
        The page you were looking for does not exist. Please check the page address.
      </div>
    </v-col>
  </v-row>
</template>

<style lang="scss">
// Configure font size
.paragraph-text {
  font-size: 18px;
}
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class NotFound extends Vue {
  created (): void {
    document.title = process.env.VUE_APP_TITLE + ' – Not Found'
    this.$emit('setPageTitle', 'Not Found')
  }
}
</script>
