export interface Station {
  id: string;
  name: string;
  lat: number;
  lon: number;
  line: string[];
}

export interface Schedule {
  station_id: string;
  destination: string;
  time: string;
}

export interface RouteFeature {
  type: "Feature";
  properties: { line: string; color: string };
  geometry: {
    type: "LineString";
    coordinates: [number, number][];
  };
}

export interface RoutesGeoJSON {
  type: "FeatureCollection";
  features: RouteFeature[];
}

export const LINE_COLORS: Record<string, string> = {
  Southern: "#2563EB",
  Northern: "#DC2626",
  Central: "#16A34A",
  "Cape Flats": "#ff9e3e",
};

export const ALL_LINES = ["Southern", "Northern", "Central", "Cape Flats"];
