import { useCallback, useMemo, useState } from "react";
import type { Station, Schedule, RoutesGeoJSON } from "@/types/transit";
import stationsData from "@/data/stations.json";
import routesData from "@/data/routes.json";
import schedulesData from "@/data/schedules.json";
import { ALL_LINES } from "@/types/transit";

export function useTransitData() {
  const [searchQuery, setSearchQuery] = useState("");
  const [activeLines, setActiveLines] = useState<string[]>([...ALL_LINES]);

  const stations = stationsData as Station[];
  const routes = routesData as RoutesGeoJSON;
  const schedules = schedulesData as Schedule[];

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
