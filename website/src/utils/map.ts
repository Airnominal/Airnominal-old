import { Icon, LatLngExpression } from 'leaflet'

export type Marker = {
  id?: string,
  visible?: boolean,
  draggable?: boolean,
  position?: LatLngExpression,
  icon?: Icon,
  tooltip?: string,
  onclick?: (marker: Marker) => void,
}

export type Polyline = {
  id?: string,
  visible?: boolean,
  color?: string,
  points?: LatLngExpression[],
}

/**
 * Fixes the missing marker icons.
 *
 * See: https://vue2-leaflet.netlify.app/quickstart/#marker-icons-are-missing
 */
export function fixMarkerIcons (): void {
  type IconDefault = Icon.Default & {
    _getIconUrl?: string;
  }

  delete (Icon.Default.prototype as IconDefault)._getIconUrl
  Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
  })
}
