"use client";

import React from "react";
import { RiskAssessment } from "../lib/api";
import { HelpCircle, CheckCircle2, AlertCircle, ArrowUpRight, ArrowDownRight } from "lucide-react";

interface ExplainabilityPanelProps {
  assessment: RiskAssessment | null;
}

export const ExplainabilityPanel: React.FC<ExplainabilityPanelProps> = ({ assessment }) => {
  if (!assessment) return null;

  return (
    <div className="bg-white p-5 rounded-xl border border-stone-200 shadow-sm space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-stone-100 pb-3">
        <div className="flex items-center space-x-2">
          <div className="w-7 h-7 rounded-md bg-emerald-50 text-emerald-700 flex items-center justify-center">
            <HelpCircle className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-stone-900">Explicabilidade do Risco (AI & GeoAI)</h3>
            <p className="text-[11px] text-stone-500">
              Por que esta área apresenta um risco de nível <strong>{assessment.risk_level}</strong>?
            </p>
          </div>
        </div>
        <span className="text-[11px] font-mono bg-emerald-50 text-emerald-800 px-2 py-0.5 rounded border border-emerald-200 font-semibold">
          Confiança: {assessment.confidence_pct}%
        </span>
      </div>

      {/* 5 Scientific Questions: WHAT, WHERE, WHEN, WHY, HOW CONFIDENT */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs bg-stone-50/70 p-3 rounded-lg border border-stone-100">
        <div>
          <span className="text-[10px] font-bold uppercase text-stone-400 block">O quê? (Perigo)</span>
          <span className="font-semibold text-stone-800">
            {assessment.hazard_type === "FLOOD" ? "Cheia Aluvial" : assessment.hazard_type === "DROUGHT" ? "Seca Agrícola" : "Multi-perigo Climático"}
          </span>
        </div>

        <div>
          <span className="text-[10px] font-bold uppercase text-stone-400 block">Onde? (Local)</span>
          <span className="font-semibold text-stone-800">{assessment.area_name}, {assessment.basin}</span>
        </div>

        <div>
          <span className="text-[10px] font-bold uppercase text-stone-400 block">Quando? (Janela)</span>
          <span className="font-semibold text-stone-800">Acumulado 7d & Atual</span>
        </div>

        <div>
          <span className="text-[10px] font-bold uppercase text-stone-400 block">Confiança</span>
          <span className="font-semibold text-emerald-700">{assessment.confidence_pct}% (Satélite + Radar)</span>
        </div>
      </div>

      {/* Primary Contributing Drivers */}
      <div className="space-y-3">
        <div className="text-xs font-bold text-stone-700 uppercase tracking-wider">
          Fatores Contribuintes Principais (Geoespacial & Hidrológico)
        </div>

        <div className="space-y-2.5">
          {assessment.primary_drivers.map((driver, idx) => {
            const isIncreasing = driver.direction === "INCREASING_RISK";
            return (
              <div
                key={idx}
                className="p-3 rounded-lg border border-stone-200/80 bg-stone-50/50 hover:bg-white hover:border-emerald-200 transition-all"
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="flex items-center space-x-2">
                    {isIncreasing ? (
                      <ArrowUpRight className="w-4 h-4 text-red-600 shrink-0" />
                    ) : (
                      <ArrowDownRight className="w-4 h-4 text-emerald-600 shrink-0" />
                    )}
                    <span className="text-xs font-bold text-stone-900">{driver.factor_name}</span>
                  </div>

                  <span className="text-xs font-mono font-bold text-stone-700 shrink-0 bg-white px-2 py-0.5 rounded border border-stone-200">
                    {driver.metric_value}
                  </span>
                </div>

                <p className="text-[11px] text-stone-600 mt-1 pl-6 leading-relaxed">
                  {driver.description}
                </p>

                {/* Contribution percentage bar */}
                <div className="mt-2 pl-6 flex items-center space-x-2 text-[10px] text-stone-500">
                  <span>Contribuição no Perigo:</span>
                  <div className="flex-1 h-1.5 bg-stone-200 rounded-full overflow-hidden">
                    <div
                      className={`h-full ${isIncreasing ? "bg-red-500" : "bg-emerald-500"} rounded-full`}
                      style={{ width: `${Math.min(100, driver.contribution_pct)}%` }}
                    />
                  </div>
                  <span className="font-mono font-bold">{driver.contribution_pct}%</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
