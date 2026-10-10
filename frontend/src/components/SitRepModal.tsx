"use client";

import React, { useState, useEffect } from "react";
import { SituationReport, fetchApi } from "../lib/api";
import { FileText, Printer, Download, X, ShieldAlert, CheckCircle, Database } from "lucide-react";

interface SitRepModalProps {
  districtId: string;
  isOpen: boolean;
  onClose: () => void;
}

export const SitRepModal: React.FC<SitRepModalProps> = ({ districtId, isOpen, onClose }) => {
  const [report, setReport] = useState<SituationReport | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    if (!isOpen) return;

    async function loadReport() {
      setLoading(true);
      const fallback: SituationReport = {
        report_id: `SITREP-${districtId.toUpperCase()}-20260917`,
        generated_at: "2026-09-17 10:30 UTC",
        title: `Boletim Especial de Risco Climático & Cheias — Bacia do Incomati (${districtId})`,
        country: "Moçambique",
        region: "Maputo Província / Bacia do Incomati",
        executive_summary: `O distrito de ${districtId} apresenta risco hidrometeorológico crítico devido à saturação do solo e elevação da vazão do Rio Incomati após acumulado de chuva extraordinário de 7 dias (+112% da média histórica).`,
        overall_risk_score: 74.0,
        overall_risk_level: "HIGH",
        hazard_matrix: {
          flood: { hazard_score: 82.5, risk_score: 76.0, level: "CRITICAL", status: "CRÍTICO" },
          drought: { hazard_score: 18.0, risk_score: 15.0, level: "LOW", status: "BAIXO" },
          water_stress: { hazard_score: 35.0, risk_score: 30.0, level: "MODERATE", status: "MODERADO" }
        },
        total_population_exposed: 42500,
        total_buildings_exposed: 9650,
        critical_infrastructure_count: 14,
        key_drivers: [
          "Precipitação Acumulada em 7 Dias: 138.2 mm (+112% vs histórico)",
          "Morfologia do Terreno: Planície aluvial com TWI de 12.4",
          "Transbordo Fluvial: Sentinel-1 SAR detectou +68.5% de expansão de lâmina d'água"
        ],
        recommended_mitigation_actions: [
          "Ativação do Centro de Operações de Emergência Distrital (COED)",
          "Salvaguarda técnica do calado da ponte da EN1 sobre o Incomati",
          "Evacuação preventiva de ribeirinhos e gado nas cotas inferiores a 18m"
        ],
        data_sources: [],
        disclaimer: "Documento emitido pelo CLYMEX AI para apoio à decisão. Diretrizes de emergência cabem com exclusividade ao INGD."
      };

      const data = await fetchApi<SituationReport>(`/reports/${districtId}`, fallback);
      setReport(data);
      setLoading(false);
    }
    loadReport();
  }, [isOpen, districtId]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[2000] flex items-center justify-center bg-stone-900/40 backdrop-blur-xs p-4 overflow-y-auto">
      <div className="bg-white rounded-2xl border border-stone-200 shadow-2xl max-w-4xl w-full max-h-[90vh] flex flex-col overflow-hidden">
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-stone-200 flex items-center justify-between bg-stone-50/80">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-emerald-600 text-white flex items-center justify-center shadow-xs">
              <FileText className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-base font-black text-stone-900">
                Boletim de Inteligência Climática (SitRep)
              </h2>
              <p className="text-xs text-stone-500 font-mono">
                {report?.report_id || "Carregando..."} • {report?.generated_at}
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => window.print()}
              className="flex items-center space-x-1 px-3 py-1.5 rounded-lg border border-stone-200 text-stone-700 bg-white hover:bg-stone-50 text-xs font-semibold shadow-xs"
            >
              <Printer className="w-3.5 h-3.5" />
              <span>Imprimir / PDF</span>
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-stone-400 hover:text-stone-700 hover:bg-stone-100"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-6 text-stone-800 text-xs leading-relaxed">
          {loading ? (
            <div className="py-20 text-center text-stone-400">Gerando relatório de situação...</div>
          ) : report ? (
            <>
              {/* Title & Banner */}
              <div className="p-4 rounded-xl border border-emerald-200 bg-emerald-50/40 flex flex-wrap items-center justify-between gap-4">
                <div>
                  <span className="text-[10px] font-black uppercase tracking-wider text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded">
                    {report.country} • {report.region}
                  </span>
                  <h3 className="text-lg font-black text-stone-900 mt-1">
                    {report.title}
                  </h3>
                </div>

                <div className="text-right">
                  <div className="text-[10px] uppercase font-bold text-stone-500">Risco Composto</div>
                  <div className="text-2xl font-black text-red-700 font-mono">
                    {report.overall_risk_score} / 100
                  </div>
                  <span className="bg-red-600 text-white text-[10px] font-black px-2 py-0.5 rounded-full uppercase">
                    {report.overall_risk_level}
                  </span>
                </div>
              </div>

              {/* Executive Summary */}
              <div>
                <h4 className="text-xs font-black text-stone-900 uppercase tracking-wider mb-1.5">
                  1. Sumário Executivo
                </h4>
                <p className="p-3 bg-stone-50 rounded-lg border border-stone-200 text-stone-700 leading-relaxed">
                  {report.executive_summary}
                </p>
              </div>

              {/* Exposure Summary */}
              <div>
                <h4 className="text-xs font-black text-stone-900 uppercase tracking-wider mb-2">
                  2. Ativos e População em Risco
                </h4>
                <div className="grid grid-cols-3 gap-3 text-center">
                  <div className="p-3 bg-stone-50 rounded-lg border border-stone-200">
                    <span className="text-[10px] text-stone-400 uppercase block">População Exposta</span>
                    <strong className="text-base font-black text-stone-900 font-mono">
                      {report.total_population_exposed.toLocaleString()} hab
                    </strong>
                  </div>

                  <div className="p-3 bg-stone-50 rounded-lg border border-stone-200">
                    <span className="text-[10px] text-stone-400 uppercase block">Edifícios na Mancha</span>
                    <strong className="text-base font-black text-stone-900 font-mono">
                      {report.total_buildings_exposed.toLocaleString()}
                    </strong>
                    <span className="text-[9px] text-stone-400 block">Google Open Buildings</span>
                  </div>

                  <div className="p-3 bg-stone-50 rounded-lg border border-stone-200">
                    <span className="text-[10px] text-stone-400 uppercase block">Infraestruturas Críticas</span>
                    <strong className="text-base font-black text-stone-900 font-mono">
                      {report.critical_infrastructure_count} instalações
                    </strong>
                  </div>
                </div>
              </div>

              {/* Drivers & Recommendations */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h4 className="text-xs font-black text-stone-900 uppercase tracking-wider mb-2">
                    3. Principais Fatores Contribuintes
                  </h4>
                  <ul className="space-y-1.5">
                    {report.key_drivers.map((driver, idx) => (
                      <li key={idx} className="p-2.5 bg-stone-50 rounded border border-stone-200/80 text-stone-700">
                        {driver}
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h4 className="text-xs font-black text-stone-900 uppercase tracking-wider mb-2">
                    4. Ações de Mitigação Recomendadas
                  </h4>
                  <ul className="space-y-1.5">
                    {report.recommended_mitigation_actions.map((act, idx) => (
                      <li key={idx} className="p-2.5 bg-emerald-50/60 rounded border border-emerald-200 text-emerald-950 font-medium">
                        {act}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Provenance & Disclaimer */}
              <div className="p-3 bg-stone-50 rounded-lg border border-stone-200 text-[11px] text-stone-500 space-y-1">
                <div className="flex items-center space-x-1 font-bold text-stone-700">
                  <Database className="w-3.5 h-3.5 text-emerald-600" />
                  <span>Proveniência Científica & Fontes Orbitais:</span>
                </div>
                <p>
                  ESA Copernicus Sentinel-1 SAR & Sentinel-2 MSI • ECMWF ERA5-Land • CHIRPS v2.0 • Copernicus DEM GLO-30 • Google Open Buildings v3 • WorldPop Africa.
                </p>
                <p className="pt-1 text-[10px] text-stone-400 italic">
                  {report.disclaimer}
                </p>
              </div>
            </>
          ) : null}
        </div>
      </div>
    </div>
  );
};
