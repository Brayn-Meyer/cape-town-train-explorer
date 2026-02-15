import type { Schedule } from "@/types/transit";
import { Clock, MapPin } from "lucide-react";

interface StationPopupProps {
  name: string;
  lines: string[];
  schedules: Schedule[];
}

export function StationPopupContent({ name, lines, schedules }: StationPopupProps) {
  const grouped = schedules.reduce<Record<string, string[]>>((acc, s) => {
    if (!acc[s.destination]) acc[s.destination] = [];
    acc[s.destination].push(s.time);
    return acc;
  }, {});

  return (
    <div className="p-4 min-w-[220px] max-w-[300px]">
      <div className="flex items-center gap-2 mb-2">
        <MapPin className="h-4 w-4 text-primary shrink-0" />
        <h3 className="font-bold text-base text-card-foreground">{name}</h3>
      </div>
      <div className="flex flex-wrap gap-1 mb-3">
        {lines.map((line) => (
          <span
            key={line}
            className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-muted text-muted-foreground"
          >
            {line}
          </span>
        ))}
      </div>
      {Object.keys(grouped).length > 0 ? (
        <div className="space-y-2">
          <div className="flex items-center gap-1 text-xs font-medium text-muted-foreground">
            <Clock className="h-3 w-3" />
            Departures
          </div>
          {Object.entries(grouped).map(([dest, times]) => (
            <div key={dest} className="text-xs">
              <span className="font-semibold text-card-foreground">→ {dest}</span>
              <div className="flex flex-wrap gap-1 mt-0.5">
                {times.map((t) => (
                  <span
                    key={t}
                    className="bg-primary/10 text-primary px-1.5 py-0.5 rounded text-[10px] font-mono"
                  >
                    {t}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-xs text-muted-foreground italic">No schedules available</p>
      )}
    </div>
  );
}
