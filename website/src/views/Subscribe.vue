<template>
  <div class="subscribe px-4 pt-4">
    <div ref="feedLinks">
      <h2 class="text-h5 pb-4">Feeds</h2>
      <!-- TODO: Add Atom feeds here -->
      <url-display label="Okrožnice" :value="`${vueAppApi}/feeds/circulars.atom`"></url-display>
      <url-display label="Nadomeščanja" :value="`${vueAppApi}/feeds/substitutions.atom`"></url-display>
      <url-display label="Jedilniki" :value="`${vueAppApi}/feeds/menus.atom`"></url-display>
      <url-display label="Razporedi delitve kosila" :value="`${vueAppApi}/feeds/schedules.atom`"></url-display>
    </div>

    <div class="pt-6" ref="calendarLinks">
      <h2 class="text-h5 pb-4">Calendars</h2>
      <!-- TODO: Add iCal calendars here -->
      <url-display label="Urnik & Nadomeščanja" :value="`${vueAppApi}/calendar/combined/${selectedEntity}`"></url-display>
      <url-display label="Urnik" :value="`${vueAppApi}/calendar/timetable/${selectedEntity}`"></url-display>
      <url-display label="Nadomeščanja" :value="`${vueAppApi}/calendar/substitutions/${selectedEntity}`"></url-display>
      <url-display label="Razporedi delitve kosila" :value="`${vueAppApi}/calendar/schedules/${selectedEntity}`"></url-display>
    </div>
  </div>
</template>

<style lang="scss">
// Center subscribe page
.subscribe {
  margin: 0 auto;
  max-width: 40rem;
}
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

import UrlDisplay from '@/components/subscribe/UrlDisplay.vue'

@Component({
  components: {
    UrlDisplay
  }
})
export default class Subscribe extends Vue {
  vueAppApi = process.env.VUE_APP_BACKEND
  created (): void {
    document.title = process.env.VUE_APP_TITLE + ' – Subscription'
    this.$emit('setPageTitle', 'Subscription')
    this.$emit('setPullToRefreshAllowed', false)
  }

  destroyed (): void {
    this.$emit('setPullToRefreshAllowed', true)
  }
}
</script>
