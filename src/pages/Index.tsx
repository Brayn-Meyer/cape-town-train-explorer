import { useState } from "react";
import { useTransitData } from "@/hooks/useTransitData";
import { TrainMap } from "@/components/map/TrainMap";
import { Sidebar } from "@/components/Sidebar";
import { Menu, X } from "lucide-react";

const Index = () => {
  const {
    stations,
    routes,
    searchQuery,
    setSearchQuery,
    activeLines,
    toggleLine,
    getSchedulesForStation,
  } = useTransitData();

  const [selectedStationId, setSelectedStationId] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen w-screen overflow-hidden">
      {/* Desktop sidebar */}
      <div className="hidden md:block w-80 shrink-0 border-r border-border">
        <Sidebar
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          activeLines={activeLines}
          toggleLine={toggleLine}
          stations={stations}
          onStationClick={(id) => setSelectedStationId(id)}
        />
      </div>

      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div className="md:hidden fixed inset-0 z-50 flex">
          <div className="w-80 max-w-[85vw] shadow-2xl">
            <Sidebar
              searchQuery={searchQuery}
              setSearchQuery={setSearchQuery}
              activeLines={activeLines}
              toggleLine={toggleLine}
              stations={stations}
              onStationClick={(id) => {
                setSelectedStationId(id);
                setSidebarOpen(false);
              }}
            />
          </div>
          <div className="flex-1 bg-foreground/30" onClick={() => setSidebarOpen(false)} />
        </div>
      )}

      {/* Map */}
      <div className="flex-1 relative">
        <button
          className="md:hidden absolute top-4 left-4 z-10 bg-card text-card-foreground p-2.5 rounded-lg shadow-lg border border-border"
          onClick={() => setSidebarOpen(true)}
        >
          <Menu className="h-5 w-5" />
        </button>

        <TrainMap
          stations={stations}
          routes={routes}
          getSchedulesForStation={getSchedulesForStation}
          selectedStationId={selectedStationId}
        />
      </div>
    </div>
  );
};

export default Index;
