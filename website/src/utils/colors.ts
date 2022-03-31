const colors = [
  '#F44336',
  '#9C27B0',
  '#3F51B5',
  '#00BCD4',
  '#4CAF50',
  '#CDDC39',
  '#FFC107',
  '#FF5722'
]

export function getColor(key: number): string {
  return colors[key % colors.length]
}
