/* eslint-disable no-console */

import { getModule, Module, MutationAction, VuexModule } from 'vuex-module-decorators'

import store from '@/store'
import { displaySnackbar } from '@/utils/snackbar'

export interface Sensor {
  mes_type: string;
  name: string;
  unit: string;
}

export interface Platform {
  id: string;
  name: string;
  description: string;
  sensors: Sensor[];
}

export interface Measurement {
  hash: string;
  timestamp: string;
  platform: string;
  coordinates?: [number, number];
  data: {
    name: string,
    unit: string,
    value: number,
  }
}

export async function updateAllData (silent = false): Promise<void> {
  await Promise.all([
    StorageModule.updatePlatforms(),
    StorageModule.updateMeasurements(),
  ])

  if (!silent) displaySnackbar('Data updated')
}

class HTTPError extends Error {
  status: number

  constructor (message: string, status: number) {
    super(message)

    this.name = 'HTTPError'
    this.status = status
  }
}

async function fetchHandle (input: RequestInfo, init?: RequestInit): Promise<Response> {
  const response = await fetch(input, init)

  if (!response.ok) {
    throw new HTTPError(`Invalid response status from the API: ${response.status}`, response.status)
  }

  return response
}

@Module({ name: 'storage', dynamic: true, /* preserveState: true, preserveStateType: 'mergeReplaceArrays', */ store })
class Storage extends VuexModule {
  lastUpdated: string | null = null

  platforms: Map<string, Platform> = new Map()
  measurements: Map<string, Measurement> = new Map()

  @MutationAction
  async updatePlatforms () {
    if (!navigator.onLine) {
      displaySnackbar('No internet connection')
      return
    }

    try {
      const response = await fetchHandle(process.env.VUE_APP_BACKEND + '/platforms')
      const platformsList = await response.json()
      const platformsMap = new Map<string, Platform>(platformsList.map((item: Platform) => [item.id, item]))
      return { platforms: platformsMap }
    } catch (error) {
      displaySnackbar('Error while accessing data')
      console.error(error)
    }
  }

  @MutationAction
  async updateMeasurements (platforms?: string[], measurements?: string[]) {
    if (!navigator.onLine) {
      displaySnackbar('No internet connection')
      return
    }

    const lastUpdated = this.lastUpdated
    const newUpdated = (new Date()).toISOString()

    let params = new URLSearchParams()
    if (lastUpdated) params.set('from', lastUpdated)
    if (platforms?.length) params.set('platform', platforms.join(','))
    if (measurements?.length) params.set('measurements', measurements.join(','))

    try {
      const response = await fetchHandle(process.env.VUE_APP_BACKEND + '/measurements?' + params.toString())
      const measurementsList = await response.json()
      const measurementsMap = new Map<string, Measurement>(measurementsList.map((item: Measurement) => [item.hash, item]))
      return { measurements: new Map([...this.measurements, ...measurementsMap]), lastUpdated: newUpdated }
    } catch (error) {
      displaySnackbar('Error while accessing data')
      console.error(error)
    }
  }
}

export const StorageModule = getModule(Storage)
