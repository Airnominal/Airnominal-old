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
  updateInterval = 10
  theme: ThemeType = ThemeType.System

  @Mutation
  setEnablePullToRefresh (enablePullToRefresh: boolean): void {
    this.enablePullToRefresh = enablePullToRefresh
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
