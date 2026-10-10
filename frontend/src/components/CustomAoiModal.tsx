"use client";

import React from "react";
import { X, Users, Building2, Hospital, GraduationCap, MapPin, Download, CheckCircle2 } from "lucide-react";
import { ExposureBreakdown } from "../lib/api";

interface CustomAoiModalProps {
  isOpen: boolean;
  onClose: () => void;
  exposure: ExposureBreakdown | null;
  polygonCoords: [number, number][];
}

export const CustomAoiModal: React.FC<CustomAoiModalProps> = ({
  isOpen,
  onClose,
  exposure,
  polygonCoords,
}) => {
  if (!isOpen || !exposure) return null;

  const handleDownloadGeoJson = () => {
    // GeoJSON coordinates format is [lng, lat]
    const geoJsonCoords = polygonCoords.map(([lat, lng]) => [lng, lat]);
    // Close polygon if not closed
    if (geoJsonCoords.length > 0 && (geoJsonCoords[0][0] !== geoJsonCoords[geoJsonCoords.length - 1][0] || geoJsonCoords[0][1] !== geoJsonCoords[geoJsonCoords.length - 1][1])) {
      geoJsonCoords.push(geoJsonCoords[0]);
    }

    const feature = {
      type: "Feature",
      properties: {
        name: "Área Personalizada de Análise (AOI)",
        calculated_at: new Date().toISOString(),
        population_exposed: exposure.population_exposed,
        buildings_count: exposure.buildings_count,
        roads_km: exposure.roads_km,
        cropland_ha: exposure.cropland_hectares,
        source: "CLYMEX AI Exposure Engine (Google Open Buildings v3 & WorldPop Africa)",
      },
      geometry: {
        type: "Polygon",
        coordinates: [geoJsonCoords],
      },
    };

    const blob = new Blob([JSON.stringify(feature, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `clymex_aoi_exposure_${new Date().toISOString().slice(0, 10)}.geojson`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="fixed inset-0 z-[3000] flex items-center justify-center p-4 bg-stone-900/50 backdrop-blur-xs">
      <div className="bg-white rounded-2xl border border-stone-200 shadow-2xl max-w-lg w-full overflow-hidden flex flex-col">
        {/* Header */}
        <div className="px-6 py-4 border-b border-stone-100 flex items-center justify-between bg-stone-50/50">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center">
              <MapPin className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-black text-stone-900">
                Análise de Exposição — Área de Interesse (AOI)
              </h2>
              <p className="text-[11px] text-stone-500">
                Interseção espacial sobre Google Open Buildings & WorldPop
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-stone-400 hover:text-stone-700 hover:bg-stone-100 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-4">
          <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center space-x-2 text-xs text-emerald-800">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
            <span>Polígono processado com sucesso. {polygonCoords.length} vértices geodésicos validados.</span>
          </div>

          {/* Metric Grid */}
          <div className="grid grid-cols-2 gap-3 text-xs">
            <div className="p-3 bg-stone-50 rounded-xl border border-stone-200">
              <div className="flex items-center space-x-1.5 text-stone-500 text-[11px]">
                <Users className="w-3.5 h-3.5 text-sky-600" />
                <span>População no Polígono</span>
              </div>
              <div className="text-xl font-black text-stone-900 mt-1 font-mono">
                {exposure.population_exposed.toLocaleString()}
              </div>
              <div className="text-[10px] text-stone-400">WorldPop Africa 100m</div>
            </div>

            <div className="p-3 bg-stone-50 rounded-xl border border-stone-200">
              <div className="flex items-center space-x-1.5 text-stone-500 text-[11px]">
                <Building2 className="w-3.5 h-3.5 text-emerald-600" />
                <span>Edifícios Mapeados</span>
              </div>
              <div className="text-xl font-black text-stone-900 mt-1 font-mono">
                {exposure.buildings_count.toLocaleString()}
              </div>
              <div className="text-[10px] text-stone-400">Google Open Buildings v3</div>
            </div>

            <div className="p-3 bg-stone-50 rounded-xl border border-stone-200">
              <div className="flex items-center space-x-1.5 text-stone-500 text-[11px]">
                <GraduationCap className="w-3.5 h-3.5 text-amber-600" />
                <span>Escolas no Perímetro</span>
              </div>
              <div className="text-xl font-black text-stone-900 mt-1 font-mono">
                {exposure.schools_count}
              </div>
              <div className="text-[10px] text-stone-400">Infraestrutura Social</div>
            </div>

            <div className="p-3 bg-stone-50 rounded-xl border border-stone-200">
              <div className="flex items-center space-x-1.5 text-stone-500 text-[11px]">
                <Hospital className="w-3.5 h-3.5 text-rose-600" />
                <span>Centros de Saúde</span>
              </div>
              <div className="text-xl font-black text-stone-900 mt-1 font-mono">
                {exposure.hospitals_count}
              </div>
              <div className="text-[10px] text-stone-400">Rede Sanitária</div>
            </div>
          </div>

          {/* Critical Facilities list if any */}
          {exposure.critical_infrastructure && exposure.critical_infrastructure.length > 0 && (
            <div className="space-y-1.5">
              <div className="text-[11px] font-bold text-stone-700 uppercase tracking-wider">
                Instalações Críticas Intersectadas:
              </div>
              <div className="max-h-24 overflow-y-auto space-y-1">
                {exposure.critical_infrastructure.map((fac, idx) => (
                  <div key={idx} className="text-xs px-2.5 py-1 bg-stone-50 border border-stone-200 rounded-md text-stone-700">
                    📍 {fac}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-stone-100 flex items-center justify-between bg-stone-50/50">
          <button
            onClick={onClose}
            className="px-3.5 py-1.5 text-xs font-bold text-stone-600 hover:text-stone-800"
          >
            Fechar
          </button>
          <button
            onClick={handleDownloadGeoJson}
            className="px-3.5 py-1.5 text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg shadow-xs flex items-center space-x-1.5"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Baixar GeoJSON da AOI</span>
          </button>
        </div>
      </div>
    </div>
  );
};
