export function getLocalISOString (date: number | string | Date): string {
  date = new Date(date)
  date.setMinutes(date.getMinutes() - date.getTimezoneOffset())
  return date.toISOString().slice(0, 16)
}
