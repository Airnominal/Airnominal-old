import { displaySnackbar } from '@/utils/snackbar'
import { fetchHandle } from '@/utils/fetch'

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

let measurementsStore: Measurement[] = []

export async function getMeasurements (platforms?: string[], measurements?: string[], from?: string): Promise<[Measurement[], boolean]> {
  if (!navigator.onLine) {
    displaySnackbar('No internet connection')
    return [measurementsStore, false]
  }

  let params = new URLSearchParams()
  if (from) params.set('from', from)
  if (platforms?.length) params.set('platform', platforms.join(','))
  if (measurements?.length) params.set('measurements', measurements.join(','))

  try {
    const response = await fetchHandle(process.env.VUE_APP_BACKEND + '/measurements?' + params.toString())
    measurementsStore = await response.json()
    return [measurementsStore, true]
  } catch (error) {
    displaySnackbar('Error while accessing data')
    console.error(error)
    return [measurementsStore, false]
  }
}
