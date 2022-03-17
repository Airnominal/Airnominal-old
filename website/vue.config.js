process.env.VUE_APP_VERSION = require('./package.json').version

const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  pwa: {
    name: process.env.VUE_APP_TITLE,
    manifestPath: 'site.webmanifest',

    themeColor: '#145ca4',
    msTileColor: '#145ca4',

    workboxOptions: {
      navigateFallback: '/index.html',
      navigateFallbackDenylist: [/\./]
    },

    manifestOptions: {
      name: process.env.VUE_APP_TITLE,
      short_name: process.env.VUE_APP_SHORT,
      description: process.env.VUE_APP_DESCRIPTION,
      categories: process.env.VUE_APP_CATEGORIES.split(','),
      keywords: process.env.VUE_APP_KEYWORDS.split(','),

      scope: '/',
      start_url: '/'
    }
  }
})
