"use client";

import React, { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { LineChart as ChartIcon, AlertTriangle } from "lucide-react";
import { API_BASE_URL } from "../lib/api";

interface Props { selectedDistrict: string }
type Daily = { date: string; actual: number; baseline: null; anomaly_pct: null };
type Series = {
  dataset: string;
  data_mode: string;
  unit: string;
  last_observation: string | null;
  period: { start: string; end_exclusive: string };
  climatological_baseline: string;
  points: Daily[];
};

export const TimeSeriesChart: React.FC<Props> = ({ selectedDistrict }) => {
  const [days, setDays] = useState<number>(30);
  const [series, setSeries] = useState<Series | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setSeries(null);
    setError(null);
    fetch(
      API_BASE_URL + "/satellite/gee/precipitation-series/" +
      encodeURIComponent(selectedDistrict) + "?days=" + days,
      { signal: controller.signal }
    )
      .then(async (res) => {
        if (!res.ok) {
          const body = await res.json().catch(() => ({}));
          throw new Error(body.detail || "CHIRPS indisponível (HTTP " + res.status + ")");
        }
        return res.json();
      })
      .then((data: Series) => setSeries(data))
      .catch((err: Error) => {
        if (err.name !== "AbortError") setError(err.message);
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [selectedDistrict, days]);

  return (
    <section className="bg-white p-5 rounded-xl border border-stone-200 shadow-sm space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-stone-100 pb-3">
        <div className="flex items-center gap-2">
          <ChartIcon className="w-5 h-5 text-emerald-700" />
          <div>
            <h3 className="text-sm font-bold text-stone-900">Precipitação histórica · CHIRPS</h3>
            <p className="text-[11px] text-stone-600">
              Últimos dias com dados publicados, não previsão meteorológica nem observação horária
            </p>
          </div>
        </div>
        <div className="flex gap-1 bg-stone-100 p-1 rounded-lg">
          {[7, 30, 90, 180].map((range) => (
            <button
              key={range}
              onClick={() => setDays(range)}
              aria-pressed={days === range}
              className={
                "px-2.5 py-1.5 rounded-md text-xs font-semibold " +
                (days === range ? "bg-white shadow-sm text-emerald-800" : "text-stone-600")
              }
            >
              {range}d
            </button>
          ))}
        </div>
      </div>

      {loading && (
        <div className="h-60 flex items-center justify-center text-xs text-stone-500">
          A consultar séries históricas no Earth Engine…
        </div>
      )}
      {error && (
        <div role="alert" className="min-h-32 p-4 flex flex-col justify-center gap-2 rounded-lg border border-amber-300 bg-amber-50 text-amber-900 text-xs">
          <div className="font-bold flex items-center gap-2"><AlertTriangle className="w-4 h-4" /> Série CHIRPS indisponível</div>
          <p>{error}</p>
          <p>Não é utilizada qualquer série demonstrativa como substituição silenciosa.</p>
        </div>
      )}
      {!loading && series && (
        <>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={series.points} margin={{ top: 10, right: 20, bottom: 5, left: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e7e5e4" vertical={false} />
                <XAxis dataKey="date" fontSize={10} tickFormatter={(value: string) => value.slice(5)} />
                <YAxis fontSize={10} unit="mm" />
                <Tooltip
                  formatter={(value: number) => [value + " mm", "CHIRPS diário"]}
                  labelFormatter={(label: string) => "Data: " + label}
                />
                <Line type="monotone" dataKey="actual" stroke="#0284c7" strokeWidth={2} dot={false} connectNulls={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <p className="text-xs text-stone-600">
            Última observação disponível: <strong>{series.last_observation ?? "não informada"}</strong>.
            As anomalias climatológicas ainda não foram calculadas; não é apresentada uma normal histórica inventada.
          </p>
          <p className="text-[10px] text-stone-500 border-t border-stone-100 pt-2">
            Fonte: {series.dataset} · {series.data_mode} · {series.unit} · média espacial do distrito GeoMoz.
          </p>
        </>
      )}
    </section>
  );
};
