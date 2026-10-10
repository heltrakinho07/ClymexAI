"use client";

import React from "react";
import { 
  ShieldAlert, 
  Droplets, 
  SunMedium, 
  Waves, 
  Radio, 
  FileText, 
  LineChart, 
  Map, 
  Layers, 
  Building2, 
  Home,
  Info
} from "lucide-react";

interface NavbarProps {
  currentTab: string;
  setCurrentTab: (tab: string) => void;
  activeRole: string;
  setActiveRole: (role: string) => void;
  isLiveMode: boolean;
  setIsLiveMode: (live: boolean) => void;
  onOpenGeeModal?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentTab,
  setCurrentTab,
  activeRole,
  setActiveRole,
  isLiveMode,
  setIsLiveMode,
  onOpenGeeModal,
}) => {
  const navItems = [
    { id: "overview", label: "Visão Geral", icon: Layers },
    { id: "risk", label: "Risco Climático", icon: Map },
    { id: "flood", label: "Cheias", icon: Waves },
    { id: "drought", label: "Secas", icon: SunMedium },
    { id: "water_stress", label: "Estresse Hídrico", icon: Droplets },
    { id: "exposure", label: "Exposição", icon: Building2 },
    { id: "sensors", label: "Sensores IoT", icon: Radio },
    { id: "alerts", label: "Alertas", icon: ShieldAlert },
    { id: "analytics", label: "Séries Temporais", icon: LineChart },
    { id: "reports", label: "Boletins / SitRep", icon: FileText },
    { id: "landing", label: "Sobre o CLYMEX", icon: Home },
  ];

  return (
    <header className="sticky top-0 z-50 bg-white border-b border-stone-200 shadow-sm">
      {/* Top Utility Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2 flex flex-wrap items-center justify-between gap-2 border-b border-stone-100 text-xs">
        <div className="flex items-center space-x-3">
          <button
            onClick={() => setIsLiveMode(!isLiveMode)}
            title="Clique para alternar entre Dados Reais de Geoprocessamento e Cenário Simulado"
            className={`flex items-center space-x-1.5 px-3 py-1 rounded-full border text-xs font-bold transition-all shadow-xs cursor-pointer ${
              isLiveMode
                ? "bg-emerald-600 text-white border-emerald-700 hover:bg-emerald-700"
                : "bg-amber-50 text-amber-900 border-amber-300 hover:bg-amber-100"
            }`}
          >
            <span
              className={`w-2 h-2 rounded-full ${
                isLiveMode ? "bg-emerald-200 animate-ping" : "bg-amber-500"
              }`}
            ></span>
            <span>{isLiveMode ? "DADOS REAIS: GEOPROCESSAMENTO VIVO (ECMWF)" : "CENÁRIO SIMULADO (CHEIA EXTREMA)"}</span>
          </button>

          {onOpenGeeModal && (
            <button
              onClick={onOpenGeeModal}
              className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full border border-emerald-300 bg-emerald-50 text-emerald-900 text-[11px] font-bold hover:bg-emerald-100 transition-colors cursor-pointer"
              title="Clique para configurar o Google Earth Engine e satélites"
            >
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
              <span>🛰️ GEE Ativo (geoprocessamento-426809)</span>
            </button>
          )}

          <span className="text-stone-500 hidden lg:inline text-[11px]">
            Demonstrador: <strong>Bacia do Incomati & Grande Maputo</strong>
          </span>
        </div>


        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-1.5 text-stone-600">
            <Info className="w-3.5 h-3.5 text-emerald-600" />
            <span className="hidden md:inline">Satélites:</span>
            <span className="font-semibold text-stone-800">Sentinel-1 SAR & 2 MSI | ERA5-Land</span>
          </div>

          <div className="flex items-center space-x-2">
            <label htmlFor="role-select" className="text-stone-500 text-[11px]">Perfil:</label>
            <select
              id="role-select"
              value={activeRole}
              onChange={(e) => setActiveRole(e.target.value)}
              className="bg-stone-50 border border-stone-200 text-stone-800 rounded px-2 py-0.5 text-xs font-medium focus:outline-none focus:ring-1 focus:ring-emerald-500"
            >
              <option value="ANALYST">Analista Geoespacial (INGD/ARA-Sul)</option>
              <option value="ADMIN">Administrador do Sistema</option>
              <option value="INSTITUTION">Parceiro Institucional (Distrital)</option>
              <option value="VIEWER">Visualizador Público</option>
            </select>
          </div>
        </div>
      </div>

      {/* Main Nav Header */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo */}
          <div 
            onClick={() => setCurrentTab("overview")} 
            className="flex items-center space-x-3 cursor-pointer select-none"
          >
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-emerald-600 to-teal-700 flex items-center justify-center text-white shadow-sm shadow-emerald-700/20">
              <Waves className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xl font-black tracking-tight text-stone-900 font-sans">
                  CLYMEX <span className="text-emerald-600">AI</span>
                </span>
                <span className="text-[10px] uppercase font-bold tracking-widest bg-stone-100 text-stone-600 px-1.5 py-0.5 rounded border border-stone-200">
                  v1.0 MVP
                </span>
              </div>
              <p className="text-[11px] font-medium text-emerald-800/80 -mt-0.5">
                Predict Risk. Protect Tomorrow.
              </p>
            </div>
          </div>

          {/* Navigation Items (Scrollable horizontally on mobile) */}
          <nav className="flex items-center space-x-1 overflow-x-auto py-2 no-scrollbar">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setCurrentTab(item.id)}
                  className={`flex items-center space-x-1.5 px-3 py-2 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                    isActive
                      ? "bg-emerald-600 text-white shadow-sm shadow-emerald-700/20"
                      : "text-stone-600 hover:text-stone-900 hover:bg-stone-100/80"
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? "text-white" : "text-emerald-700"}`} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </div>
    </header>
  );
};
