import { MapContainer, TileLayer, GeoJSON, Marker, Popup, useMap } from "react-leaflet";
import { useState, useEffect } from "react";
import type { Station, RoutesGeoJSON, Schedule } from "@/types/transit";
import { LINE_COLORS } from "@/types/transit";
import { createStationIcon } from "./StationIcon";
import { StationPopupContent } from "./StationPopup";
import type { PathOptions } from "leaflet";

interface TrainMapProps {
  stations: Station[];
  routes: RoutesGeoJSON;
  getSchedulesForStation: (id: string) => Schedule[];
  selectedStationId?: string | null;
}

function FlyToStation({ station }: { station: Station | null }) {
  const map = useMap();
  useEffect(() => {
    if (station) {
      map.flyTo([station.lat, station.lon], 14, { duration: 0.8 });
    }
  }, [station, map]);
  return null;
}

export function TrainMap({ stations, routes, getSchedulesForStation, selectedStationId }: TrainMapProps) {
  const [selected, setSelected] = useState<string | null>(null);
  const activeId = selectedStationId ?? selected;

  useEffect(() => {
    if (selectedStationId) setSelected(selectedStationId);
  }, [selectedStationId]);

  const selectedStation = stations.find((s) => s.id === activeId) ?? null;

  return (
    <MapContainer
      center={[-33.96, 18.50]}
      zoom={11}
      className="h-full w-full z-0"
      zoomControl={false}
      maxBounds={[[-34.4, 18.2], [-33.7, 18.9]]}
      minZoom={10}
    >
      <TileLayer
        attribution='&copy; <a href="https://carto.com/">CARTO</a>'
        url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
      />

      <FlyToStation station={selectedStation} />

      <GeoJSON
        key={routes.features.map((f) => f.properties.line).join(",")}
        data={routes as any}
        style={(feature) => {
          const line = feature?.properties?.line || "";
          return {
            color: LINE_COLORS[line] || "#888",
            weight: 4,
            opacity: 0.85,
          } as PathOptions;
        }}
      />

      {stations.map((station) => {
        const colors = station.line.map((l) => LINE_COLORS[l] || "#888");
        const isSelected = station.id === activeId;
        return (
          <Marker
            key={station.id}
            position={[station.lat, station.lon]}
            icon={createStationIcon(colors, isSelected)}
            eventHandlers={{
              click: () => setSelected(station.id),
            }}
          >
            <Popup>
              <StationPopupContent
                name={station.name}
                lines={station.line}
                schedules={getSchedulesForStation(station.id)}
              />
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
}
