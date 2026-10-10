"use client";

import React, { useState, useEffect } from "react";
import { fetchApi, API_BASE_URL } from "../lib/api";
import {
  Layers,
  Download,
  FileSpreadsheet,
  FileCode2,
  ArrowUpDown,
  ExternalLink,
  ShieldAlert,
  Building2,
  Users,
  Waves,
} from "lucide-react";

interface DistrictMatrixRow {
  id: string;
  name: string;
  province: string;
  composite_risk_score: number;
  risk_level: string;
  dominant_hazard: string;
  flood_score: number;
  drought_score: number;
  water_stress_score: number;
  population_exposed: number;
  buildings_exposed: number;
  roads_flooded_km: number;
  schools_exposed: number;
  hospitals_exposed: number;
  cropland_hectares: number;
  rainfall_7d_mm: number;
  rainfall_anomaly_pct: number;
  soil_moisture_pct: number;
  ndvi_current: number;
  distance_to_river_km: number;
  topographic_wetness_index: number;
  confidence_pct: number;
  data_mode: string;
}

interface DistrictMatrixTableProps {
  onSelectDistrict: (districtId: string) => void;
  isLiveMode: boolean;
}

export const DistrictMatrixTable: React.FC<DistrictMatrixTableProps> = ({
  onSelectDistrict,
  isLiveMode,
}) => {
  const [data, setData] = useState<DistrictMatrixRow[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [sortField, setSortField] = useState<keyof DistrictMatrixRow>("composite_risk_score");
  const [sortAsc, setSortAsc] = useState<boolean>(false);

  useEffect(() => {
    async function loadMatrix() {
      setLoading(true);
      const modeParam = isLiveMode ? "live" : "demo";
      const res = await fetchApi<DistrictMatrixRow[]>(`/exports/matrix?mode=${modeParam}`, []);
      setData(res);
      setLoading(false);
    }
    loadMatrix();
  }, [isLiveMode]);

  const handleSort = (field: keyof DistrictMatrixRow) => {
    if (sortField === field) {
      setSortAsc(!sortAsc);
    } else {
      setSortField(field);
      setSortAsc(false);
    }
  };

  const sortedData = [...data]
    .filter((row) =>
      row.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      row.province.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .sort((a, b) => {
      const valA = a[sortField];
      const valB = b[sortField];
      if (typeof valA === "number" && typeof valB === "number") {
        return sortAsc ? valA - valB : valB - valA;
      }
      return sortAsc
        ? String(valA).localeCompare(String(valB))
        : String(valB).localeCompare(String(valA));
    });

  const getRiskBadge = (level: string) => {
    switch (level) {
      case "CRITICAL":
        return "bg-red-600 text-white";
      case "VERY_HIGH":
        return "bg-orange-600 text-white";
      case "HIGH":
        return "bg-amber-600 text-white";
      case "MODERATE":
        return "bg-yellow-600 text-white";
      default:
        return "bg-emerald-600 text-white";
    }
  };

  return (
    <div className="bg-white p-5 rounded-xl border border-stone-200 shadow-sm space-y-4">
      {/* Header & Controls */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-stone-100 pb-3">
        <div className="flex items-center space-x-2">
          <div className="w-7 h-7 rounded-md bg-emerald-50 text-emerald-700 flex items-center justify-center">
            <Layers className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-stone-900">
              Matriz Comparativa Multi-Perigo (Todos os Distritos)
            </h3>
            <p className="text-[11px] text-stone-500">
              Comparação lado a lado de risco, perigo biofísico, TWI e exposição para a Bacia do Incomati
            </p>
          </div>
        </div>

        {/* Action Buttons: GeoJSON & Search */}
        <div className="flex items-center space-x-2">
          <input
            type="text"
            placeholder="Filtrar distrito..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="bg-stone-50 border border-stone-200 text-stone-800 text-xs rounded-lg px-2.5 py-1.5 focus:ring-1 focus:ring-emerald-500"
          />

          <a
            href={`${API_BASE_URL}/exports/geojson`}
            download="clymex_incomati_risk.geojson"
            className="flex items-center space-x-1 bg-stone-100 hover:bg-stone-200 text-stone-800 px-3 py-1.5 rounded-lg text-xs font-semibold border border-stone-200 transition-all"
          >
            <FileCode2 className="w-3.5 h-3.5 text-emerald-700" />
            <span className="hidden sm:inline">Exportar GeoJSON</span>
          </a>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="border-b border-stone-200 bg-stone-50/70 text-stone-600 font-bold uppercase text-[10px] tracking-wider">
              <th
                onClick={() => handleSort("name")}
                className="py-2.5 px-3 cursor-pointer hover:text-stone-900"
              >
                <div className="flex items-center space-x-1">
                  <span>Distrito</span>
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>

              <th
                onClick={() => handleSort("composite_risk_score")}
                className="py-2.5 px-3 text-right cursor-pointer hover:text-stone-900"
              >
                <div className="flex items-center justify-end space-x-1">
                  <span>Risco Composto</span>
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>

              <th className="py-2.5 px-3 text-center">Nível</th>
              <th className="py-2.5 px-3 text-right">Cheia</th>
              <th className="py-2.5 px-3 text-right">Seca</th>
              <th className="py-2.5 px-3 text-right">Estresse</th>
              <th className="py-2.5 px-3 text-right">Pop. Exposta</th>
              <th className="py-2.5 px-3 text-right">Edifícios (Open Bld)</th>
              <th className="py-2.5 px-3 text-right">Dist. Rio</th>
              <th className="py-2.5 px-3 text-right">TWI</th>
              <th className="py-2.5 px-3 text-center">Ações</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-stone-100">
            {loading ? (
              <tr>
                <td colSpan={11} className="text-center py-8 text-stone-400">
                  Calculando matriz comparativa com dados reais...
                </td>
              </tr>
            ) : sortedData.length === 0 ? (
              <tr>
                <td colSpan={11} className="text-center py-8 text-stone-400">
                  Nenhum distrito encontrado.
                </td>
              </tr>
            ) : (
              sortedData.map((row) => (
                <tr key={row.id} className="hover:bg-stone-50/60 transition-colors">
                  <td className="py-3 px-3">
                    <div className="font-bold text-stone-900">{row.name}</div>
                    <div className="text-[10px] text-stone-500">{row.province}</div>
                  </td>

                  <td className="py-3 px-3 text-right font-mono font-black text-stone-900 text-sm">
                    {row.composite_risk_score}
                  </td>

                  <td className="py-3 px-3 text-center">
                    <span
                      className={`px-2 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider ${getRiskBadge(
                        row.risk_level
                      )}`}
                    >
                      {row.risk_level}
                    </span>
                  </td>

                  <td className="py-3 px-3 text-right font-mono text-stone-700">
                    {row.flood_score}
                  </td>

                  <td className="py-3 px-3 text-right font-mono text-stone-700">
                    {row.drought_score}
                  </td>

                  <td className="py-3 px-3 text-right font-mono text-stone-700">
                    {row.water_stress_score}
                  </td>

                  <td className="py-3 px-3 text-right font-mono font-semibold text-stone-800">
                    {row.population_exposed.toLocaleString()}
                  </td>

                  <td className="py-3 px-3 text-right font-mono text-stone-700">
                    {row.buildings_exposed.toLocaleString()}
                  </td>

                  <td className="py-3 px-3 text-right font-mono text-stone-600">
                    {row.distance_to_river_km} km
                  </td>

                  <td className="py-3 px-3 text-right font-mono text-emerald-800 font-bold">
                    {row.topographic_wetness_index}
                  </td>

                  <td className="py-3 px-3 text-center">
                    <div className="flex items-center justify-center space-x-1.5">
                      <button
                        onClick={() => onSelectDistrict(row.id)}
                        title="Inspecionar no mapa"
                        className="p-1 rounded hover:bg-emerald-50 text-emerald-700 border border-stone-200"
                      >
                        <ExternalLink className="w-3.5 h-3.5" />
                      </button>
                      <a
                        href={`${API_BASE_URL}/exports/csv/${row.id}`}
                        download={`clymex_risk_${row.id}.csv`}
                        title="Baixar Boletim CSV"
                        className="p-1 rounded hover:bg-stone-100 text-stone-600 border border-stone-200"
                      >
                        <Download className="w-3.5 h-3.5" />
                      </a>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="flex flex-wrap items-center justify-between gap-2 text-[11px] text-stone-500 pt-2 border-t border-stone-100">
        <span>Fonte: ECMWF ERA5-Land, Copernicus DEM GLO-30 & Google Open Buildings v3</span>
        <span>
          Modo Ativo: <strong>{isLiveMode ? "OBSERVED (Geoprocessamento Vivo)" : "DEMO (Simulado)"}</strong>
        </span>
      </div>
    </div>
  );
};
