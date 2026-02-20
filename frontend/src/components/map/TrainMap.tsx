import { MapContainer, TileLayer, GeoJSON, Marker, Popup, useMap } from "react-leaflet";
import { useState, useEffect } from "react";
import type { Station, RoutesGeoJSON, Schedule } from "@/types/transit";
import { LINE_COLORS } from "@/types/transit";
import { createStationIcon } from "./StationIcon";
import { StationPopupContent } from "./StationPopup";
import type { PathOptions } from "leaflet";

/* ================================
   Props
================================ */

interface TrainMapProps {
  stations: Station[];
  routes: RoutesGeoJSON;
  showConnectionLines: boolean;
  getSchedulesForStation: (id: string) => Schedule[];
  selectedStationId?: string | null;
}

/* ================================
   Map Config
================================ */

const DEFAULT_CENTER: [number, number] = [-33.95218, 18.50888]; // Cape Town
const DEFAULT_ZOOM = 10;

const MAP_MIN_ZOOM = 9;
const MAP_MAX_ZOOM = 18;

// Cape Town bounding box
const CAPE_TOWN_BOUNDS: [[number, number], [number, number]] = [
  [-34.6, 17.95], // South West (expanded outward)
  [-33.45, 19.2], // North East (expanded outward)
];

/* ================================
   MapTiler Tile URL
================================ */

function getMapTilerTileUrl() {
  const key = (import.meta.env.VITE_MAPTILER_KEY as string | undefined)?.trim();

  if (key) {
    return `https://api.maptiler.com/maps/streets-v2/{z}/{x}/{y}.png?key=${key}`;
  }

  // Fallback to OpenStreetMap tiles when no MapTiler key is provided
  return "https://tile.openstreetmap.org/{z}/{x}/{y}.png";
}

/* ================================
   Fly To Station
================================ */

function FlyToStation({ station }: { station: Station | null }) {
  const map = useMap();

  useEffect(() => {
    if (station) {
      map.flyTo([station.lat, station.lon], MAP_MAX_ZOOM, {
        duration: 0.8,
      });
    }
  }, [station, map]);

  return null;
}

function ResizeMap({ watch }: { watch?: unknown }) {
  const map = useMap();

  useEffect(() => {
    const doResize = () => {
      // Small timeout to allow layout to settle before invalidating size
      setTimeout(() => map.invalidateSize(), 100);
    };

    doResize();
    window.addEventListener("resize", doResize);

    return () => {
      window.removeEventListener("resize", doResize);
    };
  }, [map, watch]);

  return null;
}

/* ================================
   Main Map Component
================================ */

export function TrainMap({
  stations,
  routes,
  showConnectionLines,
  getSchedulesForStation,
  selectedStationId,
}: TrainMapProps) {
  const [selected, setSelected] = useState<string | null>(null);

  const activeId = selectedStationId ?? selected;

  useEffect(() => {
    if (selectedStationId) {
      setSelected(selectedStationId);
    }
  }, [selectedStationId]);

  const selectedStation =
    stations.find((s) => s.id === activeId) ?? null;

  const mapTilerTileUrl = getMapTilerTileUrl();

  /* ================================
     Render
  ================================ */

  return (
    <div className="map-container absolute inset-0 w-full">
      <MapContainer
        center={DEFAULT_CENTER}
        zoom={DEFAULT_ZOOM}
        className="h-full w-full z-0"
        zoomControl={false}
        minZoom={MAP_MIN_ZOOM}
        maxZoom={MAP_MAX_ZOOM}
        maxBounds={CAPE_TOWN_BOUNDS}
        maxBoundsViscosity={0.2} // Prevents dragging out
      >
      {/* ===========================
          Base Map Layer
      =========================== */}

      <TileLayer
        attribution='&copy; <a href="https://www.maptiler.com/copyright/" target="_blank" rel="noreferrer">MapTiler</a> &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noreferrer">OpenStreetMap contributors</a>'
        url={mapTilerTileUrl}
      />

        {/* ===========================
          Auto Fly + Resize
        =========================== */}

        <FlyToStation station={selectedStation} />
        <ResizeMap watch={activeId} />

      {/* ===========================
          Train Routes
      =========================== */}

      {showConnectionLines && (
        <GeoJSON
          key={routes.features
            .map((f) => f.properties.line)
            .join(",")}
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
      )}

      {/* ===========================
          Stations
      =========================== */}

      {stations.map((station) => {
        const colors = station.line.map(
          (l) => LINE_COLORS[l] || "#888"
        );

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
    </div>
  );
}
