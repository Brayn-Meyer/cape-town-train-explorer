import { useCallback, useMemo, useState } from "react";
import type { Station, Schedule, RoutesGeoJSON } from "@/types/transit";
import stationsData from "@/data/stations.json";
import schedulesData from "@/data/schedules.json";
import { ALL_LINES, LINE_COLORS } from "@/types/transit";

function distanceSquared(a: Station, b: Station): number {
  const dLat = a.lat - b.lat;
  const dLon = a.lon - b.lon;
  return dLat * dLat + dLon * dLon;
}

function buildLineSegments(lineStations: Station[]): [Station, Station][] {
  if (lineStations.length < 2) {
    return [];
  }

  const segments: [Station, Station][] = [];
  const visited = new Set<number>([0]);

  while (visited.size < lineStations.length) {
    let bestFrom = -1;
    let bestTo = -1;
    let bestDistance = Number.POSITIVE_INFINITY;

    for (const fromIndex of visited) {
      for (let toIndex = 0; toIndex < lineStations.length; toIndex += 1) {
        if (visited.has(toIndex)) {
          continue;
        }

        const candidateDistance = distanceSquared(
          lineStations[fromIndex],
          lineStations[toIndex]
        );

        if (candidateDistance < bestDistance) {
          bestDistance = candidateDistance;
          bestFrom = fromIndex;
          bestTo = toIndex;
        }
      }
    }

    if (bestFrom === -1 || bestTo === -1) {
      break;
    }

    segments.push([lineStations[bestFrom], lineStations[bestTo]]);
    visited.add(bestTo);
  }

  return segments;
}

function buildRoutesFromStations(stations: Station[]): RoutesGeoJSON {
  const features = ALL_LINES.flatMap((line) => {
    const lineStations = stations.filter((station) => station.line.includes(line));
    const segments = buildLineSegments(lineStations);

    return segments.map(([fromStation, toStation]) => ({
      type: "Feature" as const,
      properties: {
        line,
        color: LINE_COLORS[line] || "#888888",
      },
      geometry: {
        type: "LineString" as const,
        coordinates: [
          [fromStation.lon, fromStation.lat] as [number, number],
          [toStation.lon, toStation.lat] as [number, number],
        ],
      },
    }));
  });

  return {
    type: "FeatureCollection",
    features,
  };
}

export function useTransitData() {
  const [searchQuery, setSearchQuery] = useState("");
  const [activeLines, setActiveLines] = useState<string[]>([...ALL_LINES]);

  const stations = stationsData as Station[];
  const schedules = schedulesData as Schedule[];
  const routes = useMemo(() => buildRoutesFromStations(stations), [stations]);

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

  return {
    stations: filteredStations,
    routes: filteredRoutes,
    searchQuery,
    setSearchQuery,
    activeLines,
    toggleLine,
    getSchedulesForStation,
    allStations: stations,
  };
}
