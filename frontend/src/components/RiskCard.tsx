"use client";

import React from "react";
import { RiskAssessment } from "../lib/api";
import { TrendingUp, TrendingDown, Minus, ShieldCheck, AlertTriangle } from "lucide-react";

interface RiskCardProps {
  assessment: RiskAssessment | null;
}

export const RiskCard: React.FC<RiskCardProps> = ({ assessment }) => {
  if (!assessment) return null;

  const getRiskColor = (level: string) => {
    switch (level) {
      case "CRITICAL":
        return {
          bg: "bg-red-50",
          text: "text-red-800",
          border: "border-red-300",
          badge: "bg-red-600 text-white",
          bar: "bg-red-600",
        };
      case "VERY_HIGH":
        return {
          bg: "bg-orange-50",
          text: "text-orange-800",
          border: "border-orange-300",
          badge: "bg-orange-600 text-white",
          bar: "bg-orange-600",
        };
      case "HIGH":
        return {
          bg: "bg-amber-50",
          text: "text-amber-800",
          border: "border-amber-300",
          badge: "bg-amber-600 text-white",
          bar: "bg-amber-600",
        };
      case "MODERATE":
        return {
          bg: "bg-yellow-50",
          text: "text-yellow-800",
          border: "border-yellow-300",
          badge: "bg-yellow-600 text-white",
          bar: "bg-yellow-500",
        };
      default:
        return {
          bg: "bg-emerald-50",
          text: "text-emerald-800",
          border: "border-emerald-300",
          badge: "bg-emerald-600 text-white",
          bar: "bg-emerald-600",
        };
    }
  };

  const colors = getRiskColor(assessment.risk_level);

  return (
    <div className={`p-5 rounded-xl border ${colors.border} ${colors.bg} shadow-sm transition-all`}>
      <div className="flex items-start justify-between">
        <div>
          <div className="text-xs font-bold uppercase tracking-wider text-stone-500">
            {assessment.province} • {assessment.basin}
          </div>
          <h2 className="text-2xl font-black text-stone-900 mt-0.5">
            {assessment.area_name}
          </h2>
        </div>

        <div className="flex flex-col items-end">
          <span className={`px-3 py-1 rounded-full text-xs font-black tracking-wider uppercase shadow-xs ${colors.badge}`}>
            {assessment.risk_level}
          </span>
          <div className="flex items-center space-x-1 mt-1 text-xs text-stone-600 font-medium">
            {assessment.trend === "Increasing" && <TrendingUp className="w-3.5 h-3.5 text-red-600" />}
            {assessment.trend === "Decreasing" && <TrendingDown className="w-3.5 h-3.5 text-emerald-600" />}
            {assessment.trend === "Stable" && <Minus className="w-3.5 h-3.5 text-stone-500" />}
            <span>Tendência: {assessment.trend}</span>
          </div>
        </div>
      </div>

      {/* Main Score & Progress Bar */}
      <div className="mt-4">
        <div className="flex items-baseline justify-between mb-1.5">
          <span className="text-xs font-semibold text-stone-700">Índice de Risco Composto</span>
          <span className="text-3xl font-black text-stone-900 font-mono">
            {assessment.risk_score}
            <span className="text-sm font-normal text-stone-500"> / 100</span>
          </span>
        </div>

        <div className="w-full h-3 bg-stone-200/80 rounded-full overflow-hidden">
          <div
            className={`h-full ${colors.bar} transition-all duration-500 rounded-full`}
            style={{ width: `${Math.min(100, Math.max(5, assessment.risk_score))}%` }}
          />
        </div>
      </div>

      {/* 3 Components: Hazard x Exposure x Vulnerability */}
      <div className="grid grid-cols-3 gap-2 mt-4 pt-3 border-t border-stone-200/80 text-center">
        <div className="bg-white/90 p-2 rounded-lg border border-stone-200/60 shadow-xs">
          <div className="text-[10px] font-bold text-stone-500 uppercase">Perigo (H)</div>
          <div className="text-base font-black text-stone-800 font-mono mt-0.5">
            {assessment.hazard_score}
          </div>
          <div className="text-[10px] text-stone-500">Biofísico</div>
        </div>

        <div className="bg-white/90 p-2 rounded-lg border border-stone-200/60 shadow-xs">
          <div className="text-[10px] font-bold text-stone-500 uppercase">Exposição (E)</div>
          <div className="text-base font-black text-stone-800 font-mono mt-0.5">
            {assessment.exposure_score}
          </div>
          <div className="text-[10px] text-stone-500">Pop & Ativos</div>
        </div>

        <div className="bg-white/90 p-2 rounded-lg border border-stone-200/60 shadow-xs">
          <div className="text-[10px] font-bold text-stone-500 uppercase">Vulnerabilidade (V)</div>
          <div className="text-base font-black text-stone-800 font-mono mt-0.5">
            {assessment.vulnerability_score}
          </div>
          <div className="text-[10px] text-stone-500">Capacidade</div>
        </div>
      </div>

      {/* Scientific Confidence & Mode notice */}
      <div className="mt-3 flex items-center justify-between text-[11px] text-stone-600">
        <div className="flex items-center space-x-1">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
          <span>Confiança dos Dados: <strong>{assessment.confidence_pct}%</strong></span>
        </div>
        <span className="bg-stone-100 text-stone-600 px-2 py-0.5 rounded border border-stone-200 text-[10px] font-semibold">
          MODO: {assessment.data_mode}
        </span>
      </div>
    </div>
  );
};
