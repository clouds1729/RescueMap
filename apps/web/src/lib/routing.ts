export function formatDistance(distance?: number): string {
  if (typeof distance !== "number") return "No route";
  return `${distance.toFixed(1)} px`;
}
