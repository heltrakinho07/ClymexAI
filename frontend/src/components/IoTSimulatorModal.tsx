"use client";

import React, { useState } from "react";
import { X, Radio, Send, CheckCircle2, AlertTriangle, XCircle, BatteryCharging, Zap } from "lucide-react";
import { API_BASE_URL, SensorTelemetry } from "../lib/api";

interface IoTSimulatorModalProps {
  isOpen: boolean;
  onClose: () => void;
  sensors: SensorTelemetry[];
  onTelemetryUpdated: () => void;
}

export const IoTSimulatorModal: React.FC<IoTSimulatorModalProps> = ({
  isOpen,
  onClose,
  sensors,
  onTelemetryUpdated,
}) => {
  const [selectedSensorId, setSelectedSensorId] = useState<string>(
    sensors[0]?.sensor_id || "MZ-INC-WL-01"
  );
  const [sensorValue, setSensorValue] = useState<number>(5.4);
  const [batteryPct, setBatteryPct] = useState<number>(92);
  const [isTransmitting, setIsTransmitting] = useState<boolean>(false);
  const [qcResult, setQcResult] = useState<any>(null);

  if (!isOpen) return null;

  const currentSensor = sensors.find((s) => s.sensor_id === selectedSensorId) || sensors[0];

  // Quick preset test cases
  const applyPreset = (type: "normal" | "surge" | "out_of_bounds") => {
    if (type === "normal") {
      setSensorValue(currentSensor?.sensor_type === "WATER_LEVEL" ? 5.2 : 25.0);
      setBatteryPct(94);
    } else if (type === "surge") {
      setSensorValue(currentSensor?.sensor_type === "WATER_LEVEL" ? 9.8 : 120.0);
      setBatteryPct(78);
    } else if (type === "out_of_bounds") {
      setSensorValue(currentSensor?.sensor_type === "WATER_LEVEL" ? 28.5 : 450.0);
      setBatteryPct(15);
    }
  };

  const handleTransmit = async () => {
    setIsTransmitting(true);
    setQcResult(null);

    try {
      const payload = {
        sensor_id: selectedSensorId,
        sensor_type: currentSensor?.sensor_type || "WATER_LEVEL",
        value: Number(sensorValue),
        battery: Number(batteryPct),
      };

      const res = await fetch(`${API_BASE_URL}/sensors/telemetry`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        const data = await res.json();
        setQcResult(data);
        onTelemetryUpdated();
      }
    } catch (err) {
      console.error("Telemetry transmission error:", err);
    } finally {
      setIsTransmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[3000] flex items-center justify-center p-4 bg-stone-900/50 backdrop-blur-xs">
      <div className="bg-white rounded-2xl border border-stone-200 shadow-2xl max-w-lg w-full overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="px-6 py-4 border-b border-stone-100 flex items-center justify-between bg-stone-50/50">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center">
              <Radio className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-black text-stone-900">
                Simulador de Telemetria IoT & Gateway LoRaWAN
              </h2>
              <p className="text-[11px] text-stone-500">
                Transmissão de Pacotes ESP32 & Avaliação de Controle de Qualidade (QC)
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-stone-400 hover:text-stone-700 hover:bg-stone-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-4 overflow-y-auto">
          {/* Station Selector */}
          <div className="space-y-1">
            <label className="text-xs font-bold text-stone-700 uppercase tracking-wider">
              Estação Telemétrica Alvo:
            </label>
            <select
              value={selectedSensorId}
              onChange={(e) => setSelectedSensorId(e.target.value)}
              className="w-full bg-stone-50 border border-stone-200 text-stone-900 font-bold text-xs rounded-lg px-3 py-2 focus:ring-1 focus:ring-emerald-500"
            >
              {sensors.map((s) => (
                <option key={s.sensor_id} value={s.sensor_id}>
                  {s.station_name} ({s.sensor_id}) — {s.sensor_type}
                </option>
              ))}
            </select>
          </div>

          {/* Preset Buttons */}
          <div className="space-y-1">
            <div className="text-[11px] font-bold text-stone-600 uppercase tracking-wider">
              Cenários de Teste Rápidos:
            </div>
            <div className="grid grid-cols-3 gap-2">
              <button
                type="button"
                onClick={() => applyPreset("normal")}
                className="py-1.5 px-2 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 text-emerald-800 rounded-lg text-[11px] font-bold transition-all text-center"
              >
                🟢 Normal (Estável)
              </button>
              <button
                type="button"
                onClick={() => applyPreset("surge")}
                className="py-1.5 px-2 bg-amber-50 hover:bg-amber-100 border border-amber-200 text-amber-800 rounded-lg text-[11px] font-bold transition-all text-center"
              >
                🟠 Pico de Cheia
              </button>
              <button
                type="button"
                onClick={() => applyPreset("out_of_bounds")}
                className="py-1.5 px-2 bg-rose-50 hover:bg-rose-100 border border-rose-200 text-rose-800 rounded-lg text-[11px] font-bold transition-all text-center"
              >
                🔴 Falha / Fora da Escala
              </button>
            </div>
          </div>

          {/* Form Fields: Value & Battery */}
          <div className="grid grid-cols-2 gap-3 pt-1">
            <div className="space-y-1">
              <label className="text-xs font-bold text-stone-700 flex justify-between">
                <span>Leitura ({currentSensor?.unit || "m"}):</span>
                <span className="font-mono text-emerald-800">{sensorValue}</span>
              </label>
              <input
                type="number"
                step="0.1"
                value={sensorValue}
                onChange={(e) => setSensorValue(parseFloat(e.target.value) || 0)}
                className="w-full px-3 py-1.5 text-xs font-mono rounded-lg border border-stone-200 bg-stone-50"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-bold text-stone-700 flex justify-between">
                <span>Bateria:</span>
                <span className="font-mono text-stone-600">{batteryPct}%</span>
              </label>
              <input
                type="range"
                min="5"
                max="100"
                value={batteryPct}
                onChange={(e) => setBatteryPct(parseInt(e.target.value) || 0)}
                className="w-full accent-emerald-600"
              />
            </div>
          </div>

          {/* Transmit Button */}
          <button
            onClick={handleTransmit}
            disabled={isTransmitting}
            className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl shadow-xs flex items-center justify-center space-x-2 transition-all disabled:opacity-50"
          >
            <Send className="w-4 h-4" />
            <span>{isTransmitting ? "Transmitindo Pacote LoRaWAN..." : "Transmitir Pacote Telemétrico"}</span>
          </button>

          {/* Real-time QC Engine Feedback */}
          {qcResult && (
            <div className={`p-4 rounded-xl border text-xs space-y-2 ${
              qcResult.status === "ACCEPTED" ? "bg-emerald-50 border-emerald-200 text-emerald-950" : "bg-rose-50 border-rose-200 text-rose-950"
            }`}>
              <div className="flex items-center justify-between font-bold">
                <span className="flex items-center space-x-1.5">
                  {qcResult.status === "ACCEPTED" ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  ) : (
                    <XCircle className="w-4 h-4 text-rose-600" />
                  )}
                  <span>Resultado QC: {qcResult.status}</span>
                </span>
                <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-white border border-stone-200">
                  Pontuação QC: {qcResult.quality_score}%
                </span>
              </div>

              <div className="text-[11px] space-y-0.5 text-stone-600">
                <div>Sensor Atualizado: <strong>{qcResult.station_name}</strong></div>
                <div>Status Atribuído: <strong>{qcResult.assigned_status}</strong></div>
                <div>Destino: <code>{qcResult.storage_destination}</code></div>
              </div>

              {qcResult.quality_flags && qcResult.quality_flags.length > 0 && (
                <div className="pt-1 border-t border-stone-200/60">
                  <span className="font-bold text-[10px] uppercase text-rose-800">Flags de Anomalia Detectadas:</span>
                  <ul className="list-disc list-inside text-[11px] text-rose-700 mt-0.5">
                    {qcResult.quality_flags.map((flag: string, idx: number) => (
                      <li key={idx}>{flag}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-stone-100 flex justify-end bg-stone-50/50">
          <button
            onClick={onClose}
            className="px-4 py-1.5 text-xs font-bold text-stone-600 hover:text-stone-800"
          >
            Fechar
          </button>
        </div>
      </div>
    </div>
  );
};
