import { Search, Train, X } from "lucide-react";
import { Input } from "@/components/ui/input";
import { ALL_LINES, LINE_COLORS } from "@/types/transit";
import type { Station } from "@/types/transit";

interface SidebarProps {
  searchQuery: string;
  setSearchQuery: (q: string) => void;
  activeLines: string[];
  toggleLine: (line: string) => void;
  stations: Station[];
  onStationClick: (id: string) => void;
}

export function Sidebar({
  searchQuery,
  setSearchQuery,
  activeLines,
  toggleLine,
  stations,
  onStationClick,
}: SidebarProps) {
  return (
    <div className="flex flex-col h-full bg-sidebar text-sidebar-foreground">
      {/* Header */}
      <div className="p-5 border-b border-sidebar-border">
        <div className="flex items-center gap-2 mb-4">
          <Train className="h-6 w-6 text-sidebar-primary" />
          <h1 className="text-lg font-bold tracking-tight">Cape Town Rail</h1>
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search stations..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-9 bg-sidebar-accent border-sidebar-border text-sidebar-foreground placeholder:text-muted-foreground"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery("")}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-sidebar-foreground"
            >
              <X className="h-3.5 w-3.5" />
            </button>
          )}
        </div>
      </div>

      {/* Line filters */}
      <div className="p-4 border-b border-sidebar-border">
        <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">
          Lines
        </p>
        <div className="flex flex-wrap gap-2">
          {ALL_LINES.map((line) => {
            const active = activeLines.includes(line);
            return (
              <button
                key={line}
                onClick={() => toggleLine(line)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold transition-all"
                style={{
                  backgroundColor: active ? LINE_COLORS[line] : "transparent",
                  color: active ? "white" : LINE_COLORS[line],
                  border: `2px solid ${LINE_COLORS[line]}`,
                  opacity: active ? 1 : 0.5,
                }}
              >
                {line}
              </button>
            );
          })}
        </div>
      </div>

      {/* Station list */}
      <div className="flex-1 overflow-y-auto [direction:rtl]">  {/* Add RTL direction */}
        <div className="p-3 [direction:ltr]">  {/* Reset direction for content */}
          <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">
            Stations ({stations.length})
          </p>
          <div className="space-y-1">
            {stations.map((station) => (
              <button
                key={station.id}
                onClick={() => onStationClick(station.id)}
                className="w-full text-left px-3 py-2 rounded-lg text-sm hover:bg-sidebar-accent transition-colors flex items-center justify-between group"
              >
                <span className="font-medium">{station.name}</span>
                <div className="flex gap-1">
                  {station.line.map((l) => (
                    <span
                      key={l}
                      className="w-2.5 h-2.5 rounded-full shrink-0"
                      style={{ backgroundColor: LINE_COLORS[l] }}
                    />
                  ))}
                </div>
              </button>
            ))}
            {stations.length === 0 && (
              <p className="text-xs text-muted-foreground italic py-4 text-center">
                No stations found
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}