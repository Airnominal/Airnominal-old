import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import { SettingsModule, ThemeType } from '@/store/modules/settings'

Vue.use(Vuetify)

export default new Vuetify({
  icons: {
    iconfont: 'mdiSvg'
  },
  theme: {
    dark: (SettingsModule.theme === ThemeType.System && window.matchMedia('(prefers-color-scheme: dark)').matches) || SettingsModule.theme === ThemeType.Dark,
    options: {
      themeCache: {
        get: key => localStorage.getItem(`vuetify-theme-${JSON.stringify(key)}`),
        set: (key, value) => localStorage.setItem(`vuetify-theme-${JSON.stringify(key)}`, value)
      }
    }
  }
})
