import { getModule, Module, Mutation, VuexModule } from 'vuex-module-decorators'

import store from '@/store'

export enum ThemeType {
  System,
  Light,
  Dark
}

@Module({ name: 'settings', dynamic: true, preserveState: true, preserveStateType: 'mergeReplaceArrays', store })
class Settings extends VuexModule {
  enablePullToRefresh = false
  storeRangeInURL = true
  displayCurrentData = true
  displayCharts = true
  displayMaps = true
  updateInterval = 60
  theme: ThemeType = ThemeType.System

  @Mutation
  setEnablePullToRefresh (enablePullToRefresh: boolean): void {
    this.enablePullToRefresh = enablePullToRefresh
  }

  @Mutation
  setStoreRangeInURL (storeRangeInURL: boolean): void {
    this.storeRangeInURL = storeRangeInURL
  }

  @Mutation
  setDisplayCurrentData (displayCurrentData: boolean): void {
    this.displayCurrentData = displayCurrentData
  }

  @Mutation
  setDisplayCharts (displayCharts: boolean): void {
    this.displayCharts = displayCharts
  }

  @Mutation
  setDisplayMaps (displayMaps: boolean): void {
    this.displayMaps = displayMaps
  }

  @Mutation
  setUpdateInterval (updateInterval: number): void {
    this.updateInterval = updateInterval
  }

  @Mutation
  setTheme (theme: ThemeType): void {
    this.theme = theme
  }
}

export const SettingsModule = getModule(Settings)
