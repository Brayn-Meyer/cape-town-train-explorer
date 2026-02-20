import { useCallback, useMemo, useState } from "react";
import type { Station, Schedule, RoutesGeoJSON } from "@/types/transit";
import stationsData from "@/data/stations.json";
import schedulesData from "@/data/schedules.json";
import stationConnectionsData from "@/data/station_connections.json";
import { ALL_LINES, LINE_COLORS } from "@/types/transit";

type StationConnection = {
  id: string;
  front: string[];
  rear: string[];
};

const STATION_ID_ALIASES: Record<string, string> = {
  eersterivier: "eerste_river",
  kapteinsklip: "kapteinsklip_station",
};

function normalizeStationId(id: string): string {
  return STATION_ID_ALIASES[id] ?? id;
}

function buildRoutesFromConnections(
  stations: Station[],
  connections: StationConnection[]
): RoutesGeoJSON {
  const stationById = new Map(stations.map((station) => [station.id, station]));
  const seenSegments = new Set<string>();
  const features: RoutesGeoJSON["features"] = [];

  for (const connection of connections) {
    const fromStation = stationById.get(normalizeStationId(connection.id));
    if (!fromStation) {
      continue;
    }

    const neighbors = [...connection.front, ...connection.rear];

    for (const neighborId of neighbors) {
      const toStation = stationById.get(normalizeStationId(neighborId));
      if (!toStation || fromStation.id === toStation.id) {
        continue;
      }

      const segmentKey = [fromStation.id, toStation.id].sort().join("::");
      if (seenSegments.has(segmentKey)) {
        continue;
      }
      seenSegments.add(segmentKey);

      const sharedLines = ALL_LINES.filter(
        (line) => fromStation.line.includes(line) && toStation.line.includes(line)
      );

      for (const line of sharedLines) {
        features.push({
          type: "Feature",
          properties: {
            line,
            color: LINE_COLORS[line] || "#888888",
          },
          geometry: {
            type: "LineString",
            coordinates: [
              [fromStation.lon, fromStation.lat],
              [toStation.lon, toStation.lat],
            ],
          },
        });
      }
    }
  }

  return {
    type: "FeatureCollection",
    features,
  };
}

export function useTransitData() {
  const [searchQuery, setSearchQuery] = useState("");
  const [activeLines, setActiveLines] = useState<string[]>([...ALL_LINES]);
  const [showConnectionLines, setShowConnectionLines] = useState(false);

  const stations = stationsData as Station[];
  const schedules = schedulesData as Schedule[];
  const stationConnections = stationConnectionsData as StationConnection[];
  const routes = useMemo(
    () => buildRoutesFromConnections(stations, stationConnections),
    [stations, stationConnections]
  );

  const filteredStations = useMemo(() => {
    return stations.filter((s) => {
      const matchesSearch = s.name.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesLine = s.line.some((l) => activeLines.includes(l));
      return matchesSearch && matchesLine;
    });
  }, [stations, searchQuery, activeLines]);

  const filteredRoutes = useMemo(() => {
    return {
      ...routes,
      features: routes.features.filter((f) => activeLines.includes(f.properties.line)),
    };
  }, [routes, activeLines]);

  const getSchedulesForStation = useCallback(
    (stationId: string) => schedules.filter((s) => s.station_id === stationId),
    [schedules]
  );

  const toggleLine = useCallback((line: string) => {
    setActiveLines((prev) =>
      prev.includes(line) ? prev.filter((l) => l !== line) : [...prev, line]
    );
  }, []);

  const toggleConnectionLines = useCallback(() => {
    setShowConnectionLines((prev) => !prev);
  }, []);

  return {
    stations: filteredStations,
    routes: filteredRoutes,
    showConnectionLines,
    searchQuery,
    setSearchQuery,
    activeLines,
    toggleLine,
    toggleConnectionLines,
    getSchedulesForStation,
    allStations: stations,
  };
}
