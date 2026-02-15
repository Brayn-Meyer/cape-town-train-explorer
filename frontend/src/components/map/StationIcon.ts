import L from "leaflet";

export function createStationIcon(colors: string[], isSelected: boolean) {
  const size = isSelected ? 20 : 14;
  const border = isSelected ? 3 : 2;
  const primaryColor = colors[0] || "#2563EB";

  return L.divIcon({
    className: "custom-station-marker",
    html: `<div style="
      width: ${size}px;
      height: ${size}px;
      border-radius: 50%;
      background: ${primaryColor};
      border: ${border}px solid white;
      box-shadow: 0 2px 6px rgba(0,0,0,0.35);
      transition: all 0.2s ease;
      ${isSelected ? "transform: scale(1.2);" : ""}
    "></div>`,
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
  });
}
