"use client";

import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  Area,
  ComposedChart,
} from "recharts";
import { fetchApi } from "../lib/api";
import { LineChart as ChartIcon, Calendar } from "lucide-react";

interface TimeSeriesChartProps {
  selectedDistrict: string;
}

export const TimeSeriesChart: React.FC<TimeSeriesChartProps> = ({ selectedDistrict }) => {
  const [indicator, setIndicator] = useState<string>("rainfall");
  const [temporalRange, setTemporalRange] = useState<string>("30d");
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      const fallback = [
        { date: "2026-09-01", actual: 2.1, baseline: 2.5, anomaly_pct: -16.0 },
        { date: "2026-09-05", actual: 5.4, baseline: 3.1, anomaly_pct: 74.0 },
        { date: "2026-09-10", actual: 14.8, baseline: 2.8, anomaly_pct: 428.0 },
        { date: "2026-09-14", actual: 22.0, baseline: 3.0, anomaly_pct: 633.0 },
        { date: "2026-09-15", actual: 58.4, baseline: 3.2, anomaly_pct: 1725.0 },
        { date: "2026-09-16", actual: 76.2, baseline: 3.1, anomaly_pct: 2358.0 },
        { date: "2026-09-17", actual: 64.5, baseline: 3.4, anomaly_pct: 1797.0 },
      ];

      const res = await fetchApi<any[]>(
        `/weather/timeseries?indicator=${indicator}&district=${selectedDistrict}`,
        fallback
      );
      setData(res);
      setLoading(false);
    }
    loadData();
  }, [indicator, selectedDistrict]);

  const getIndicatorUnit = () => {
    switch (indicator) {
      case "rainfall":
        return "mm";
      case "ndvi":
        return "Índice (-1 a 1)";
      case "soil_moisture":
        return "%";
      case "river_stage":
        return "m";
      default:
        return "";
    }
  };

  return (
    <div className="bg-white p-5 rounded-xl border border-stone-200 shadow-sm space-y-4">
      {/* Header & Filter Controls */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-stone-100 pb-3">
        <div className="flex items-center space-x-2">
          <div className="w-7 h-7 rounded-md bg-emerald-50 text-emerald-700 flex items-center justify-center">
            <ChartIcon className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-stone-900">Séries Temporais & Anomalias Hidroclimáticas</h3>
            <p className="text-[11px] text-stone-500">
              Comparação do valor observado contra o baseline histórico (10-20 anos)
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          {/* Indicator Select */}
          <select
            value={indicator}
            onChange={(e) => setIndicator(e.target.value)}
            className="bg-stone-50 border border-stone-200 text-stone-800 text-xs rounded-lg px-2.5 py-1.5 font-medium focus:ring-1 focus:ring-emerald-500"
          >
            <option value="rainfall">Precipitação (CHIRPS/ERA5)</option>
            <option value="ndvi">Vigor Vegetativo NDVI (Sentinel-2)</option>
            <option value="soil_moisture">Umidade do Solo (ERA5-Land)</option>
            <option value="river_stage">Nível do Rio Incomati (m)</option>
          </select>

          {/* Temporal Scale Buttons */}
          <div className="flex items-center space-x-1 bg-stone-100 p-0.5 rounded-lg border border-stone-200 text-xs">
            {["7d", "30d", "90d", "1y"].map((scale) => (
              <button
                key={scale}
                onClick={() => setTemporalRange(scale)}
                className={`px-2 py-1 rounded-md text-[11px] font-semibold transition-all ${
                  temporalRange === scale
                    ? "bg-white text-emerald-800 shadow-xs"
                    : "text-stone-600 hover:text-stone-900"
                }`}
              >
                {scale}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Chart Area */}
      <div className="w-full h-64 pt-2">
        {loading ? (
          <div className="w-full h-full flex items-center justify-center text-xs text-stone-400">
            Carregando séries temporais...
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={data} margin={{ top: 10, right: 20, bottom: 20, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
              <XAxis
                dataKey="date"
                stroke="#94a3b8"
                fontSize={10}
                tickFormatter={(val) => val.slice(5)}
                tickLine={false}
              />
              <YAxis stroke="#94a3b8" fontSize={10} tickLine={false} unit={getIndicatorUnit()} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#ffffff",
                  borderColor: "#e2e8f0",
                  borderRadius: "8px",
                  fontSize: "12px",
                  boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
                }}
                formatter={(value: any, name: any) => [
                  `${value} ${getIndicatorUnit()}`,
                  name === "actual" ? "Valor Observado" : "Baseline Histórico",
                ]}
                labelFormatter={(label) => `Data: ${label}`}
              />
              <Legend
                verticalAlign="top"
                align="right"
                wrapperStyle={{ fontSize: "11px", paddingBottom: "10px" }}
              />
              {/* Baseline Area */}
              <Area
                type="monotone"
                dataKey="baseline"
                name="Baseline Climatológico"
                fill="#ecfdf5"
                stroke="#10b981"
                strokeDasharray="4 4"
                strokeWidth={1.5}
              />
              {/* Observed Line */}
              <Line
                type="monotone"
                dataKey="actual"
                name="Observado / Estimado"
                stroke="#0284c7"
                strokeWidth={2.5}
                dot={{ r: 2.5, fill: "#0284c7" }}
                activeDot={{ r: 5 }}
              />
            </ComposedChart>
          </ResponsiveContainer>
        )}
      </div>

      <div className="flex items-center justify-between text-[11px] text-stone-500 pt-2 border-t border-stone-100">
        <span>Fonte: ECMWF ERA5-Land & CHIRPS v2.0 calibrado</span>
        <span className="text-emerald-700 font-semibold">*Linha tracejada verde representa a normal de 20 anos</span>
      </div>
    </div>
  );
};
