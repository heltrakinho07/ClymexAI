"use client";

import React from "react";
import { ExposureBreakdown } from "../lib/api";
import { Users, Building2, GraduationCap, Cross, Navigation, Sprout, AlertCircle } from "lucide-react";

interface ExposureMetricsProps {
  exposure: ExposureBreakdown | null;
  areaName: string;
}

export const ExposureMetrics: React.FC<ExposureMetricsProps> = ({ exposure, areaName }) => {
  if (!exposure) return null;

  return (
    <div className="bg-white p-5 rounded-xl border border-stone-200 shadow-sm space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-stone-100 pb-3">
        <div className="flex items-center space-x-2">
          <div className="w-7 h-7 rounded-md bg-sky-50 text-sky-700 flex items-center justify-center">
            <Building2 className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-stone-900">Análise de Exposição de Ativos & População</h3>
            <p className="text-[11px] text-stone-500">
              Intersecção geoespacial com <strong>Google Open Buildings</strong> e <strong>WorldPop</strong>
            </p>
          </div>
        </div>

        <span className="text-[10px] font-bold text-stone-600 bg-stone-100 px-2.5 py-1 rounded-full border border-stone-200">
          Área: {areaName}
        </span>
      </div>

      {/* Grid of Key Exposed Metrics */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
        {/* Population */}
        <div className="p-3 rounded-lg border border-stone-200 bg-stone-50/60">
          <div className="flex items-center space-x-2 text-stone-600 mb-1">
            <Users className="w-4 h-4 text-emerald-700" />
            <span className="text-xs font-semibold">População Exposta</span>
          </div>
          <div className="text-xl font-black text-stone-900 font-mono">
            {exposure.population_exposed.toLocaleString()}
          </div>
          <div className="text-[10px] text-stone-500 mt-0.5">
            Densidade: {exposure.population_density_per_sqkm} hab/km²
          </div>
        </div>

        {/* Buildings (Google Open Buildings) */}
        <div className="p-3 rounded-lg border border-stone-200 bg-stone-50/60">
          <div className="flex items-center space-x-2 text-stone-600 mb-1">
            <Building2 className="w-4 h-4 text-sky-700" />
            <span className="text-xs font-semibold">Edifícios na Mancha</span>
          </div>
          <div className="text-xl font-black text-stone-900 font-mono">
            {exposure.buildings_count.toLocaleString()}
          </div>
          <div className="text-[10px] text-stone-500 mt-0.5">
            Base: Google Open Buildings v3
          </div>
        </div>

        {/* Roads (EN1) */}
        <div className="p-3 rounded-lg border border-stone-200 bg-stone-50/60">
          <div className="flex items-center space-x-2 text-stone-600 mb-1">
            <Navigation className="w-4 h-4 text-amber-700" />
            <span className="text-xs font-semibold">Eixos Rodoviários</span>
          </div>
          <div className="text-xl font-black text-stone-900 font-mono">
            {exposure.roads_km} <span className="text-xs font-normal">km</span>
          </div>
          <div className="text-[10px] text-stone-500 mt-0.5">
            Trecho crítico da EN1
          </div>
        </div>

        {/* Health Centers */}
        <div className="p-3 rounded-lg border border-stone-200 bg-stone-50/60">
          <div className="flex items-center space-x-2 text-stone-600 mb-1">
            <Cross className="w-4 h-4 text-red-700" />
            <span className="text-xs font-semibold">Unidades de Saúde</span>
          </div>
          <div className="text-xl font-black text-stone-900 font-mono">
            {exposure.hospitals_count}
          </div>
          <div className="text-[10px] text-stone-500 mt-0.5">
            Centros de saúde e postos
          </div>
        </div>

        {/* Schools */}
        <div className="p-3 rounded-lg border border-stone-200 bg-stone-50/60">
          <div className="flex items-center space-x-2 text-stone-600 mb-1">
            <GraduationCap className="w-4 h-4 text-indigo-700" />
            <span className="text-xs font-semibold">Escolas Expostas</span>
          </div>
          <div className="text-xl font-black text-stone-900 font-mono">
            {exposure.schools_count}
          </div>
          <div className="text-[10px] text-stone-500 mt-0.5">
            Primárias e secundárias
          </div>
        </div>

        {/* Cropland / Agriculture */}
        <div className="p-3 rounded-lg border border-stone-200 bg-stone-50/60">
          <div className="flex items-center space-x-2 text-stone-600 mb-1">
            <Sprout className="w-4 h-4 text-emerald-700" />
            <span className="text-xs font-semibold">Área Agrícola</span>
          </div>
          <div className="text-xl font-black text-stone-900 font-mono">
            {exposure.cropland_hectares.toLocaleString()} <span className="text-xs font-normal">ha</span>
          </div>
          <div className="text-[10px] text-stone-500 mt-0.5">
            Cana, hortícolas e arroz
          </div>
        </div>
      </div>

      {/* Critical Facilities List */}
      {exposure.critical_infrastructure && exposure.critical_infrastructure.length > 0 && (
        <div className="pt-2 border-t border-stone-100">
          <div className="text-xs font-bold text-stone-700 uppercase tracking-wider mb-2">
            Infraestruturas Críticas no Perímetro de Risco:
          </div>
          <ul className="space-y-1.5 text-xs text-stone-700">
            {exposure.critical_infrastructure.map((fac, idx) => (
              <li key={idx} className="flex items-center space-x-2 bg-stone-50 px-2.5 py-1.5 rounded border border-stone-200/70">
                <AlertCircle className="w-3.5 h-3.5 text-amber-600 shrink-0" />
                <span className="font-medium">{fac}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
