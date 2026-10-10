"use client";

import React from "react";
import { SensorTelemetry } from "../lib/api";
import { Radio, Battery, Wifi, AlertTriangle, CheckCircle2, XCircle } from "lucide-react";

interface SensorsTableProps {
  sensors: SensorTelemetry[];
  onOpenSimulator?: () => void;
}

export const SensorsTable: React.FC<SensorsTableProps> = ({ sensors, onOpenSimulator }) => {
  const getStatusBadge = (status: string) => {
    switch (status) {
      case "ONLINE":
        return (
          <span className="flex items-center space-x-1 bg-emerald-50 text-emerald-800 px-2 py-0.5 rounded-full text-[11px] font-bold border border-emerald-200">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
            <span>ONLINE</span>
          </span>
        );
      case "WARNING":
        return (
          <span className="flex items-center space-x-1 bg-amber-50 text-amber-800 px-2 py-0.5 rounded-full text-[11px] font-bold border border-amber-200">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
            <span>AVISO</span>
          </span>
        );
      default:
        return (
          <span className="flex items-center space-x-1 bg-red-50 text-red-800 px-2 py-0.5 rounded-full text-[11px] font-bold border border-red-200">
            <span className="w-1.5 h-1.5 rounded-full bg-red-500"></span>
            <span>FALHA</span>
          </span>
        );
    }
  };

  return (
    <div className="bg-white p-5 rounded-xl border border-stone-200 shadow-sm space-y-4">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-stone-100 pb-3">
        <div className="flex items-center space-x-2">
          <div className="w-7 h-7 rounded-md bg-emerald-50 text-emerald-700 flex items-center justify-center">
            <Radio className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-stone-900">Rede Telemétrica de Sensores Ambientais (IoT)</h3>
            <p className="text-[11px] text-stone-500">
              Estações hidrométricas, pluviométricas e albufeiras da Bacia do Incomati (Arquitetura ESP32 / LoRaWAN)
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-3 text-xs">
          {onOpenSimulator && (
            <button
              onClick={onOpenSimulator}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-xs transition-colors cursor-pointer"
            >
              <Radio className="w-3.5 h-3.5" />
              <span>Simular Envio LoRaWAN / ESP32</span>
            </button>
          )}

          <span className="bg-stone-100 text-stone-700 px-2.5 py-1 rounded-full border border-stone-200 font-semibold">
            {sensors.length} Estações Monitoradas
          </span>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="border-b border-stone-200 bg-stone-50/70 text-stone-600 font-bold uppercase text-[10px] tracking-wider">
              <th className="py-2.5 px-3">Estação / ID</th>
              <th className="py-2.5 px-3">Bacia / Rio</th>
              <th className="py-2.5 px-3">Variável</th>
              <th className="py-2.5 px-3 text-right">Leitura Atual</th>
              <th className="py-2.5 px-3 text-center">Status</th>
              <th className="py-2.5 px-3 text-center">Qualidade (QC)</th>
              <th className="py-2.5 px-3 text-center">Bateria</th>
              <th className="py-2.5 px-3">Última Transmissão</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-stone-100">
            {sensors.map((s) => (
              <tr key={s.sensor_id} className="hover:bg-stone-50/50 transition-colors">
                <td className="py-3 px-3">
                  <div className="font-bold text-stone-900">{s.station_name}</div>
                  <div className="text-[10px] font-mono text-stone-400">{s.sensor_id}</div>
                </td>

                <td className="py-3 px-3 text-stone-600 font-medium">
                  {s.basin}
                </td>

                <td className="py-3 px-3">
                  <span className="bg-stone-100 text-stone-700 px-2 py-0.5 rounded text-[11px] font-semibold border border-stone-200">
                    {s.sensor_type}
                  </span>
                </td>

                <td className="py-3 px-3 text-right font-mono font-bold text-stone-900 text-sm">
                  {s.current_value} <span className="text-xs font-normal text-stone-500">{s.unit}</span>
                </td>

                <td className="py-3 px-3 text-center">
                  {getStatusBadge(s.status)}
                </td>

                <td className="py-3 px-3 text-center">
                  <span className="font-mono font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                    {s.data_quality_score}%
                  </span>
                </td>

                <td className="py-3 px-3 text-center font-mono">
                  <div className="flex items-center justify-center space-x-1 text-stone-700">
                    <Battery className={`w-3.5 h-3.5 ${s.battery_pct < 30 ? "text-red-500" : "text-emerald-600"}`} />
                    <span>{s.battery_pct}%</span>
                  </div>
                </td>

                <td className="py-3 px-3 text-stone-500 font-mono text-[11px]">
                  {new Date(s.last_seen).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })} UTC
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="flex items-center justify-between text-[11px] text-stone-500 pt-2 border-t border-stone-100">
        <span>Protocolo de Transmissão: MQTT Broker & LoRaWAN Gateway</span>
        <span>Controle de Qualidade: Detecção de Spikes, Limites Físicos e Deriva de Sensor</span>
      </div>
    </div>
  );
};
