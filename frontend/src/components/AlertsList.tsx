"use client";

import React from "react";
import { AlertRecord } from "../lib/api";
import { ShieldAlert, AlertTriangle, CheckCircle, Bell, ArrowRight, Waves, SunMedium, Droplets } from "lucide-react";

interface AlertsListProps {
  alerts: AlertRecord[];
  onSelectArea?: (areaId: string) => void;
}

export const AlertsList: React.FC<AlertsListProps> = ({ alerts, onSelectArea }) => {
  return (
    <div className="bg-white p-5 rounded-xl border border-stone-200 shadow-sm space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-stone-100 pb-3">
        <div className="flex items-center space-x-2">
          <div className="w-7 h-7 rounded-md bg-red-50 text-red-700 flex items-center justify-center">
            <ShieldAlert className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-stone-900">Cenários Simulados de Alerta</h3>
            <p className="text-[11px] text-stone-500">
              Simulação educativa com limiares definidos no motor. Não são alertas oficiais nem leituras actuais.
            </p>
          </div>
        </div>

        <span className="text-xs font-bold bg-red-100 text-red-800 px-2.5 py-1 rounded-full border border-red-200">
          {alerts.length} {alerts.length === 1 ? "Alerta DEMO" : "Alertas DEMO"}
        </span>
      </div>

      {/* Alerts Feed */}
      <div className="space-y-3">
        {alerts.map((alert) => {
          const isCritical = alert.risk_level === "CRITICAL";

          return (
            <div
              key={alert.id}
              className={`p-4 rounded-xl border transition-all ${
                isCritical
                  ? "border-red-300 bg-red-50/40 hover:bg-red-50/70"
                  : "border-amber-300 bg-amber-50/30 hover:bg-amber-50/60"
              }`}
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center space-x-2">
                  <span
                    className={`px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider ${
                      isCritical ? "bg-red-600 text-white" : "bg-amber-600 text-white"
                    }`}
                  >
                    {alert.risk_level}
                  </span>
                  <span className="text-xs font-mono text-stone-500">{alert.id}</span>
                  <span className="text-xs text-stone-500">• {alert.location}</span>
                </div>

                <span className="text-[11px] text-stone-500 font-mono">
                  {new Date(alert.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })} UTC
                </span>
              </div>

              <h4 className="text-sm font-bold text-stone-900 mt-2">
                {alert.title}
              </h4>

              {/* Trigger Condition */}
              <div className="mt-2 text-xs text-stone-700 bg-white/80 p-2.5 rounded-lg border border-stone-200/80">
                <strong className="text-stone-900">Gatilho do Cenário:</strong> {alert.trigger_condition}
              </div>

              {/* Impact stats */}
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-3 text-xs">
                <div className="bg-white p-2 rounded border border-stone-200/60">
                  <span className="text-[10px] text-stone-400 block uppercase">Área Estimada (DEMO)</span>
                  <strong className="text-stone-800 font-mono">{alert.affected_area_sqkm} km²</strong>
                </div>

                <div className="bg-white p-2 rounded border border-stone-200/60">
                  <span className="text-[10px] text-stone-400 block uppercase">População Estimada</span>
                  <strong className="text-stone-800 font-mono">
                    {alert.estimated_population_exposed.toLocaleString()} hab
                  </strong>
                </div>

                <div className="bg-white p-2 rounded border border-stone-200/60">
                  <span className="text-[10px] text-stone-400 block uppercase">Confiança heurística</span>
                  <strong className="text-emerald-700 font-mono">{alert.confidence_pct}%</strong>
                </div>
              </div>

              {/* Recommended Action */}
              <div className="mt-3 text-xs text-emerald-900 bg-emerald-50/70 p-2.5 rounded-lg border border-emerald-200">
                <strong className="text-emerald-950 block mb-0.5">Ações Recomendadas de Mitigação:</strong>
                <p className="leading-relaxed">{alert.recommended_action}</p>
              </div>

              {/* Disclaimer */}
              <div className="mt-2 text-[10px] text-stone-400 italic">
                {alert.disclaimer}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
