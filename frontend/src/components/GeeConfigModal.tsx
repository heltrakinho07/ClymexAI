"use client";

import React, { useState, useEffect } from "react";
import { X, Satellite, CheckCircle2, RefreshCw, Layers, ShieldCheck, ExternalLink, Cpu } from "lucide-react";
import { API_BASE_URL } from "../lib/api";

interface GeeConfigModalProps {
  isOpen: boolean;
  onClose: () => void;
  onProjectChange?: (projectId: string) => void;
}

export const GeeConfigModal: React.FC<GeeConfigModalProps> = ({
  isOpen,
  onClose,
  onProjectChange,
}) => {
  const [projectId, setProjectId] = useState<string>("geoprocessamento-426809");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [geeInfo, setGeeInfo] = useState<any>(null);

  // Fetch status when modal opens
  useEffect(() => {
    if (isOpen) {
      fetch(`${API_BASE_URL}/satellite/gee/status`)
        .then((res) => res.json())
        .then((data) => {
          setGeeInfo(data);
          if (data.project_id) setProjectId(data.project_id);
        })
        .catch(() => {});
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSaveAndTest = async () => {
    setIsLoading(true);
    setStatusMessage(null);

    try {
      const res = await fetch(`${API_BASE_URL}/satellite/gee/configure`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project_id: projectId.trim() || "geoprocessamento-426809",
        }),
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}: configuração rejeitada`);
      const data = await res.json();
      setGeeInfo(data);
      setStatusMessage(data.connected ? "✅ Earth Engine autenticado." : "⚠️ Project ID guardado; Earth Engine ainda não autenticado no servidor.");
      if (onProjectChange) {
        onProjectChange(projectId.trim() || "geoprocessamento-426809");
      }
    } catch (err: any) {
      setStatusMessage(`❌ Erro ao validar: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[3000] flex items-center justify-center p-4 bg-stone-900/50 backdrop-blur-xs">
      <div className="bg-white rounded-2xl border border-stone-200 shadow-2xl max-w-xl w-full overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="px-6 py-4 border-b border-stone-100 flex items-center justify-between bg-stone-50/50">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center">
              <Satellite className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-black text-stone-900">
                Google Earth Engine (GEE)
              </h2>
              <p className="text-xs text-stone-500">
                Observação da Terra em Escala Planetária & GeoAI
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

        {/* Body */}
        <div className="p-6 space-y-5 overflow-y-auto">
          {/* Status Badge Banner */}
          <div className="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 flex items-start space-x-3">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
            <div className="text-xs space-y-1">
              <div className="font-bold text-emerald-900 flex items-center space-x-2">
                <span>{geeInfo?.connected ? "Earth Engine autenticado" : "Earth Engine ainda não autenticado"}</span>
                <span className="bg-emerald-200 text-emerald-900 px-2 py-0.5 rounded-full text-[10px] font-mono">
                  {geeInfo?.connected ? "ATIVO" : "POR CONFIGURAR"}
                </span>
              </div>
              <p className="text-emerald-800 text-[11px] leading-relaxed">
                As camadas só serão disponibilizadas como índices quando forem realmente processadas no backend.
              </p>
            </div>
          </div>

          {/* Project ID Input */}
          <div className="space-y-1.5">
            <label className="block text-xs font-bold text-stone-700 uppercase tracking-wider">
              Google Cloud Project ID (GEE Quota):
            </label>
            <div className="flex space-x-2">
              <input
                type="text"
                value={projectId}
                onChange={(e) => setProjectId(e.target.value)}
                placeholder="ex: geoprocessamento-426809"
                className="flex-1 px-3 py-2 text-xs font-mono rounded-lg border border-stone-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-stone-50"
              />
              <button
                type="button"
                onClick={() => setProjectId("geoprocessamento-426809")}
                className="px-3 py-2 text-[11px] font-semibold text-stone-600 bg-stone-100 hover:bg-stone-200 rounded-lg transition-colors"
              >
                Padrão
              </button>
            </div>
            <p className="text-[11px] text-stone-500">
              Projeto ativo associado à cota do Google Earth Engine para Moçambique.
            </p>
          </div>

          <p className="text-xs text-stone-600 bg-stone-50 border border-stone-200 rounded-lg p-3">
            As credenciais de contas de serviço GEE devem ser configuradas como segredo privado no servidor.
            Nunca cole chaves JSON no navegador.
          </p>

          {/* Connected Satellites Grid */}
          <div className="space-y-2">
            <div className="text-xs font-bold text-stone-700 uppercase tracking-wider flex items-center space-x-1.5">
              <Layers className="w-4 h-4 text-emerald-600" />
              <span>Satélites & Coleções Planetárias Integradas</span>
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="p-2.5 rounded-lg border border-stone-200 bg-stone-50/70">
                <div className="font-bold text-stone-800">🛰️ Sentinel-2 MSI</div>
                <div className="text-[11px] text-stone-500">10m · NDVI, NDWI, MNDWI</div>
                <div className="text-[10px] text-emerald-700 font-medium mt-1">Revisita: 5 dias</div>
              </div>

              <div className="p-2.5 rounded-lg border border-stone-200 bg-stone-50/70">
                <div className="font-bold text-stone-800">📡 Sentinel-1 C-SAR</div>
                <div className="text-[11px] text-stone-500">10m · Inundação por Radar</div>
                <div className="text-[10px] text-emerald-700 font-medium mt-1">Imune a Nuvens</div>
              </div>

              <div className="p-2.5 rounded-lg border border-stone-200 bg-stone-50/70">
                <div className="font-bold text-stone-800">⛰️ Copernicus GLO-30</div>
                <div className="text-[11px] text-stone-500">30m · DEM, Declividade, TWI</div>
                <div className="text-[10px] text-emerald-700 font-medium mt-1">Topografia de Alta Precisão</div>
              </div>

              <div className="p-2.5 rounded-lg border border-stone-200 bg-stone-50/70">
                <div className="font-bold text-stone-800">🌧️ CHIRPS & Radar</div>
                <div className="text-[11px] text-stone-500">0.05° · Precipitação Diária</div>
                <div className="text-[10px] text-emerald-700 font-medium mt-1">Tempo Real & Anomalias</div>
              </div>
            </div>
          </div>

          {/* Feedback Message */}
          {statusMessage && (
            <div className={`p-3 rounded-lg text-xs font-semibold ${
              statusMessage.startsWith("✅") ? "bg-emerald-50 text-emerald-800 border border-emerald-200" : "bg-rose-50 text-rose-800 border border-rose-200"
            }`}>
              {statusMessage}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-stone-100 flex items-center justify-between bg-stone-50/50">
          <span className="text-[11px] text-stone-500">
            Arquitetura Decoupled CLYMEX AI + GeoMoz
          </span>
          <div className="flex space-x-2">
            <button
              onClick={onClose}
              className="px-4 py-2 text-xs font-bold text-stone-600 hover:text-stone-800 transition-colors"
            >
              Fechar
            </button>
            <button
              onClick={handleSaveAndTest}
              disabled={isLoading}
              className="px-4 py-2 text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg shadow-xs flex items-center space-x-1.5 transition-all disabled:opacity-50"
            >
              {isLoading ? (
                <>
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  <span>Validando...</span>
                </>
              ) : (
                <>
                  <ShieldCheck className="w-3.5 h-3.5" />
                  <span>Salvar & Validar Conexão</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
