import { displaySnackbar } from '@/utils/snackbar'
import { fetchHandle } from '@/utils/fetch'

export interface Sensor {
  mes_type: string;
  name: string;
  unit: string;
}

export interface Station {
  id: string;
  name: string;
  description: string;
  sensors: Sensor[];
}

let stationsStore: Station[] = []

export async function getStations (): Promise<[Station[], boolean]> {
  if (!navigator.onLine) {
    displaySnackbar('No internet connection')
    return [stationsStore, false]
  }

  try {
    const response = await fetchHandle(process.env.VUE_APP_BACKEND + '/platforms?_now=' + Date.now())
    stationsStore = await response.json()
    return [stationsStore, true]
  } catch (error) {
    displaySnackbar('Error while accessing data')
    console.error(error)
    return [stationsStore, false]
  }
}
