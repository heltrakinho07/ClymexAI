"use client";

import React, { useEffect, useState } from "react";
import { Satellite, Waves, Mountain, Sprout, Calendar, AlertTriangle, Droplets, Settings } from "lucide-react";
import { API_BASE_URL } from "../lib/api";

interface EarthObservationPanelProps {
  selectedDistrict: string;
  onOpenGeeConfig?: () => void;
}

type Metrics = {
  data_mode: string;
  data_source: string;
  ndvi_mean: number | null;
  ndwi_water_extent_sqkm: number | null;
  sar_flood_inundated_sqkm: number | null;
  dem_elevation_mean_m: number | null;
  dem_slope_mean_deg: number | null;
  rainfall_7d_mm: number | null;
  dates: Record<string, string>;
  methods: Record<string, string>;
  warnings: string[];
};

function metric(value: number | null | undefined, decimals = 2) {
  return typeof value === "number" && Number.isFinite(value) ? value.toFixed(decimals) : "—";
}

export const EarthObservationPanel: React.FC<EarthObservationPanelProps> = ({ selectedDistrict, onOpenGeeConfig }) => {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setError(null);
    setMetrics(null);
    fetch(API_BASE_URL + "/satellite/gee/metrics/" + encodeURIComponent(selectedDistrict), {
      signal: controller.signal,
    })
      .then(async (res) => {
        if (!res.ok) {
          const body = await res.json().catch(() => ({}));
          throw new Error(body.detail || "HTTP " + res.status);
        }
        return res.json();
      })
      .then((data: Metrics) => setMetrics(data))
      .catch((err: Error) => {
        if (err.name !== "AbortError") setError(err.message);
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [selectedDistrict]);

  const cards = [
    {
      name: "Sentinel-2 · NDVI",
      icon: Sprout,
      value: metric(metrics?.ndvi_mean),
      unit: "índice",
      description: "Média espacial com máscara de nuvens",
      date: metrics?.dates?.sentinel2,
    },
    {
      name: "Sentinel-2 · Água NDWI",
      icon: Waves,
      value: metric(metrics?.ndwi_water_extent_sqkm, 1),
      unit: "km²",
      description: "Área indicativa com NDWI > 0,1",
      date: metrics?.dates?.sentinel2,
    },
    {
      name: "Sentinel-1 · Candidatos a cheia",
      icon: Waves,
      value: metric(metrics?.sar_flood_inundated_sqkm, 1),
      unit: "km²",
      description: "Mudança SAR não validada como inundação",
      date: metrics?.dates?.sentinel1,
    },
    {
      name: "Copernicus · Altitude",
      icon: Mountain,
      value: metric(metrics?.dem_elevation_mean_m, 1),
      unit: "m",
      description: "Modelo digital de superfície estático",
      date: undefined,
    },
    {
      name: "CHIRPS · Chuva 7 dias",
      icon: Droplets,
      value: metric(metrics?.rainfall_7d_mm, 1),
      unit: "mm",
      description: "Sete dias até ao último registo publicado",
      date: metrics?.dates?.chirps,
    },
  ];

  return (
    <section className="bg-white rounded-xl border border-stone-200 shadow-sm p-5 space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-stone-100 pb-3">
        <div className="flex items-center gap-2">
          <Satellite className="w-5 h-5 text-emerald-700" />
          <div>
            <h3 className="text-sm font-bold text-stone-900">Observação da Terra · Earth Engine</h3>
            <p className="text-xs text-stone-500">{selectedDistrict.toUpperCase()} · GeoMoz · métricas derivadas por satélite</p>
          </div>
        </div>
        {onOpenGeeConfig && (
          <button onClick={onOpenGeeConfig} className="flex items-center gap-1 text-xs text-emerald-700 font-semibold">
            <Settings className="w-4 h-4" /> Configuração
          </button>
        )}
      </div>

      {loading && <p className="text-xs text-stone-500 py-4">A consultar e processar colecções no Earth Engine…</p>}
      {error && (
        <div role="alert" className="rounded-lg border border-amber-300 bg-amber-50 text-amber-900 p-3 text-xs space-y-1">
          <div className="font-bold flex items-center gap-2"><AlertTriangle className="w-4 h-4" /> Índices satelitais indisponíveis</div>
          <p>{error}</p>
          <p>Não serão apresentados valores fictícios. Configure as credenciais GEE no servidor e confirme o acesso ao GeoMoz.</p>
        </div>
      )}

      {metrics && !loading && (
        <>
          <p className="text-[11px] text-amber-900 bg-amber-50 border border-amber-200 rounded-md p-2">
            Índices derivados de observações orbitais, mas estimativas não calibradas para avisos de emergência. Consultar a data de cada fonte.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {cards.map((card) => {
              const Icon = card.icon;
              return (
                <div key={card.name} className="rounded-lg border border-stone-200 bg-stone-50 p-3 min-w-0">
                  <div className="flex items-center gap-1.5 text-xs font-semibold text-stone-700">
                    <Icon className="w-4 h-4 text-emerald-700 shrink-0" /> {card.name}
                  </div>
                  <div className="text-2xl font-bold font-mono text-stone-900 mt-1">
                    {card.value} <span className="text-xs font-normal text-stone-500">{card.unit}</span>
                  </div>
                  <p className="text-[11px] text-stone-600 mt-1">{card.description}</p>
                  {card.date && (
                    <p className="text-[10px] text-stone-500 mt-1 flex items-center gap-1">
                      <Calendar className="w-3 h-3" /> Última imagem: {card.date}
                    </p>
                  )}
                </div>
              );
            })}
          </div>
          {metrics.warnings.length > 0 && (
            <p className="text-[11px] text-amber-800">{metrics.warnings.join(" · ")}</p>
          )}
          <p className="text-[10px] text-stone-500 border-t border-stone-100 pt-2">
            Fonte: Google Earth Engine / Copernicus / CHIRPS. Estatísticas de área são indicativas.
            GEE utiliza os limites administrativos do GeoMoz (referência 2017).
          </p>
        </>
      )}
    </section>
  );
};
