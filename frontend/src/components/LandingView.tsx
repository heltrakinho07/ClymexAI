"use client";

import React from "react";
import { 
  Waves, 
  ShieldCheck, 
  Cpu, 
  Satellite, 
  Radio, 
  Activity, 
  Compass, 
  ArrowRight, 
  CheckCircle2, 
  Globe2, 
  Building2, 
  Droplets, 
  SunMedium, 
  Layers
} from "lucide-react";

interface LandingViewProps {
  onEnterDashboard: () => void;
}

export const LandingView: React.FC<LandingViewProps> = ({ onEnterDashboard }) => {
  return (
    <div className="bg-white text-stone-900 min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-16 pb-24 border-b border-stone-100 bg-gradient-to-b from-emerald-50/40 via-white to-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          <div className="inline-flex items-center space-x-2 bg-emerald-100/70 border border-emerald-300/60 px-3.5 py-1.5 rounded-full text-xs font-bold text-emerald-900 mb-6 shadow-xs">
            <span className="w-2 h-2 rounded-full bg-emerald-600 animate-ping"></span>
            <span>Inteligência Climática de Nova Geração para África</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-black tracking-tight text-stone-900 font-sans max-w-4xl mx-auto leading-tight">
            CLYMEX <span className="text-emerald-600">AI</span>
          </h1>
          <p className="text-xl sm:text-2xl font-bold text-emerald-800 mt-2 font-serif italic">
            "Predict Risk. Protect Tomorrow."
          </p>

          <p className="text-base sm:text-lg text-stone-600 max-w-2xl mx-auto mt-5 leading-relaxed font-normal">
            Plataforma de Inteligência e Risco Climático movida a Inteligência Artificial, 
            observação orbital por satélite, análises geoespaciais e sensores ambientais.
          </p>

          <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
            <button
              onClick={onEnterDashboard}
              className="flex items-center space-x-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-6 py-3.5 rounded-xl shadow-md shadow-emerald-700/20 transition-all text-sm group"
            >
              <span>Acessar Plataforma WebGIS</span>
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </button>

            <a
              href="#how-it-works"
              className="px-6 py-3.5 rounded-xl border border-stone-200 text-stone-700 bg-stone-50 hover:bg-stone-100 text-sm font-semibold transition-all"
            >
              Conhecer a Metodologia
            </a>
          </div>

          {/* 4 Pillars: Detect, Predict, Understand, Act */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-16 max-w-4xl mx-auto text-left">
            <div className="p-4 rounded-xl border border-stone-200 bg-white shadow-xs">
              <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center mb-2 font-black">
                1
              </div>
              <h3 className="font-bold text-stone-900 text-sm">DETECTAR</h3>
              <p className="text-xs text-stone-500 mt-1">
                Monitoramento por radar Sentinel-1 SAR e óptico multiespectral Sentinel-2.
              </p>
            </div>

            <div className="p-4 rounded-xl border border-stone-200 bg-white shadow-xs">
              <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center mb-2 font-black">
                2
              </div>
              <h3 className="font-bold text-stone-900 text-sm">PREVER</h3>
              <p className="text-xs text-stone-500 mt-1">
                Modelos físicos e de GeoAI calculando precipitação extrema e dinâmica de cheia.
              </p>
            </div>

            <div className="p-4 rounded-xl border border-stone-200 bg-white shadow-xs">
              <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center mb-2 font-black">
                3
              </div>
              <h3 className="font-bold text-stone-900 text-sm">COMPREENDER</h3>
              <p className="text-xs text-stone-500 mt-1">
                Explicabilidade científica com decomposição transparente de cada fator de risco.
              </p>
            </div>

            <div className="p-4 rounded-xl border border-stone-200 bg-white shadow-xs">
              <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center mb-2 font-black">
                4
              </div>
              <h3 className="font-bold text-stone-900 text-sm">AGIR</h3>
              <p className="text-xs text-stone-500 mt-1">
                Alertas antecipados e boletins de situação para defesa civil e lideranças.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Problem & Solution */}
      <section className="py-20 border-b border-stone-100 bg-stone-50/50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded border border-emerald-200">
                O Desafio em Moçambique & África Austral
              </span>
              <h2 className="text-2xl sm:text-3xl font-black text-stone-900 mt-3 leading-tight">
                Vulnerabilidade a Eventos Extremos sem Inteligência Integrada
              </h2>
              <p className="text-stone-600 text-sm mt-4 leading-relaxed">
                Bacias como a do <strong>Rio Incomati</strong> e do <strong>Limpopo</strong> enfrentam ciclos devastadores de cheias súbitas e secas prolongadas. Sistemas convencionais fornecem previsões meteorológicas genéricas que não informam <em>quem</em> e <em>quais infraestruturas</em> estão em risco iminente.
              </p>

              <ul className="space-y-2.5 mt-6 text-sm text-stone-700">
                <li className="flex items-start space-x-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 mt-0.5 shrink-0" />
                  <span>Déficit de sensores físicos in-situ ao longo dos vales fluviais.</span>
                </li>
                <li className="flex items-start space-x-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 mt-0.5 shrink-0" />
                  <span>Nuvens densas durante ciclones que impedem o uso de satélites ópticos comuns.</span>
                </li>
                <li className="flex items-start space-x-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 mt-0.5 shrink-0" />
                  <span>Falta de cruzamento espacial com edifícios e estradas críticas (ex: EN1).</span>
                </li>
              </ul>
            </div>

            <div className="bg-white p-6 rounded-2xl border border-stone-200 shadow-sm space-y-4">
              <span className="text-xs font-bold uppercase tracking-wider text-stone-500">
                A Resposta Tecnológica do CLYMEX AI
              </span>
              <h3 className="text-lg font-black text-stone-900">
                A Equação Central de Risco Acionável
              </h3>
              <div className="p-4 bg-emerald-50/50 rounded-xl border border-emerald-200 text-center font-mono font-bold text-emerald-900 text-lg">
                RISCO = PERIGO × EXPOSIÇÃO × VULNERABILIDADE
              </div>
              <p className="text-xs text-stone-600 leading-relaxed">
                O CLYMEX AI cruza o perigo hidrometeorológico com a base <strong>Google Open Buildings</strong> (milhões de estruturas mapeadas por IA) e <strong>WorldPop</strong>, gerando scores de 0 a 100 categorizados em 5 níveis operacionais: <em>Baixo, Moderado, Alto, Muito Alto e Crítico</em>.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 3 Core Climate Risk Engines */}
      <section className="py-20 border-b border-stone-100 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto">
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded border border-emerald-200">
              Motores Especializados
            </span>
            <h2 className="text-2xl sm:text-3xl font-black text-stone-900 mt-3">
              Três Verticais de Perigo em Uma Única Plataforma
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
            {/* Flood */}
            <div className="p-6 rounded-2xl border border-stone-200 bg-stone-50/50 hover:bg-white hover:border-emerald-200 transition-all shadow-xs">
              <div className="w-10 h-10 rounded-xl bg-sky-100 text-sky-700 flex items-center justify-center mb-4">
                <Waves className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-stone-900">Inteligência de Cheias (Flood Engine)</h3>
              <p className="text-xs text-stone-600 mt-2 leading-relaxed">
                Usa radar Sentinel-1 SAR (penetração de nuvens), modelo digital de terreno Copernicus DEM GLO-30, índice TWI e acumulados CHIRPS/ERA5 para mapear expansão de lâmina d'água na bacia aluvial.
              </p>
            </div>

            {/* Drought */}
            <div className="p-6 rounded-2xl border border-stone-200 bg-stone-50/50 hover:bg-white hover:border-emerald-200 transition-all shadow-xs">
              <div className="w-10 h-10 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center mb-4">
                <SunMedium className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-stone-900">Inteligência de Secas (Drought Engine)</h3>
              <p className="text-xs text-stone-600 mt-2 leading-relaxed">
                Calcula o Índice de Condição da Vegetação (VCI) via Sentinel-2 NDVI, percentil de umidade do solo em camadas radiculares e anomalias de temperatura LST para salvaguarda agrícola.
              </p>
            </div>

            {/* Water Stress */}
            <div className="p-6 rounded-2xl border border-stone-200 bg-stone-50/50 hover:bg-white hover:border-emerald-200 transition-all shadow-xs">
              <div className="w-10 h-10 rounded-xl bg-teal-100 text-teal-700 flex items-center justify-center mb-4">
                <Droplets className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-stone-900">Estresse Hídrico & Albufeiras</h3>
              <p className="text-xs text-stone-600 mt-2 leading-relaxed">
                Monitora volumes úteis de reservatórios estratégicos (Barragens de Corumana e Pequenos Libombos) e a pressão consuntiva de irrigação para o abastecimento da Grande Maputo.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Roadmap Section */}
      <section className="py-20 border-b border-stone-100 bg-stone-50/40">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto">
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded border border-emerald-200">
              Roteiro de Expansão
            </span>
            <h2 className="text-2xl sm:text-3xl font-black text-stone-900 mt-3">
              Da Bacia do Incomati a Toda a África Austral
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
            <div className="p-5 rounded-xl border border-emerald-300 bg-emerald-50/50">
              <span className="text-xs font-black text-emerald-800 uppercase tracking-wider block">
                Fase 1 — MVP Operacional (Atual)
              </span>
              <h4 className="font-bold text-stone-900 text-sm mt-1">Demonstrador Incomati / Maputo</h4>
              <p className="text-xs text-stone-600 mt-2 leading-relaxed">
                Integração orbital de Sentinel-1/2, CHIRPS, ERA5, Google Open Buildings, motor de risco explainable e WebGIS interativo.
              </p>
            </div>

            <div className="p-5 rounded-xl border border-stone-200 bg-white">
              <span className="text-xs font-black text-stone-500 uppercase tracking-wider block">
                Fase 2 — Telemetria IoT
              </span>
              <h4 className="font-bold text-stone-900 text-sm mt-1">Sensores Físicos ESP32 / LoRaWAN</h4>
              <p className="text-xs text-stone-600 mt-2 leading-relaxed">
                Instalação de réguas linimétricas por radar e pluviômetros conectados via MQTT com controle de qualidade em tempo real.
              </p>
            </div>

            <div className="p-5 rounded-xl border border-stone-200 bg-white">
              <span className="text-xs font-black text-stone-500 uppercase tracking-wider block">
                Fase 3 — GeoAI & Expansão SADC
              </span>
              <h4 className="font-bold text-stone-900 text-sm mt-1">Redes Hidrológicas GNN & SADC</h4>
              <p className="text-xs text-stone-600 mt-2 leading-relaxed">
                Deep learning para segmentação automática de satélite, modelos de grafos neurais e expansão para Eswatini, África do Sul e Zimbábue.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-white border-t border-stone-200 text-center text-xs text-stone-500">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-2">
          <div className="font-black text-stone-900 text-base">
            CLYMEX <span className="text-emerald-600">AI</span>
          </div>
          <p className="font-serif italic text-emerald-800">"Predict Risk. Protect Tomorrow."</p>
          <p className="text-[11px] text-stone-400">
            © 2026 CLYMEX AI. Desenvolvido para resiliência climática em Moçambique e África Austral.
          </p>
        </div>
      </footer>
    </div>
  );
};
