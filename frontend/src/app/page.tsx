"use client";

import React, { useState, useEffect } from "react";
import dynamic from "next/dynamic";
import { Navbar } from "../components/Navbar";
import { RiskCard } from "../components/RiskCard";
import { ExplainabilityPanel } from "../components/ExplainabilityPanel";
import { ExposureMetrics } from "../components/ExposureMetrics";
import { TimeSeriesChart } from "../components/TimeSeriesChart";
import { AlertsList } from "../components/AlertsList";
import { SensorsTable } from "../components/SensorsTable";
import { DistrictMatrixTable } from "../components/DistrictMatrixTable";
import { SitRepModal } from "../components/SitRepModal";
import { LandingView } from "../components/LandingView";
import { GeeConfigModal } from "../components/GeeConfigModal";
import { CustomAoiModal } from "../components/CustomAoiModal";
import { IoTSimulatorModal } from "../components/IoTSimulatorModal";
import { EarthObservationPanel } from "../components/EarthObservationPanel";
import {
  RiskAssessment,
  AlertRecord,
  SensorTelemetry,
  ExposureBreakdown,
  fetchApi,
} from "../lib/api";
import {
  Waves,
  SunMedium,
  Droplets,
  Layers,
  FileText,
  ShieldAlert,
  Users,
  Building2,
  Radio,
  ExternalLink,
} from "lucide-react";

// Client-only dynamic import for Leaflet map
const DynamicMap = dynamic(
  () => import("../components/MapComponent").then((mod) => mod.MapComponent),
  {
    ssr: false,
    loading: () => (
      <div className="w-full h-full min-h-[520px] flex items-center justify-center bg-stone-50 border border-stone-200 rounded-xl text-stone-400 text-xs">
        Carregando motor cartográfico Leaflet...
      </div>
    ),
  }
);

export default function Home() {
  const [currentTab, setCurrentTab] = useState<string>("overview");
  const [selectedDistrict, setSelectedDistrict] = useState<string>("manhica");
  const [activeRole, setActiveRole] = useState<string>("ANALYST");
  const [isSitRepOpen, setIsSitRepOpen] = useState<boolean>(false);
  const [isLiveMode, setIsLiveMode] = useState<boolean>(true);
  const [isGeeModalOpen, setIsGeeModalOpen] = useState<boolean>(false);
  const [isAoiModalOpen, setIsAoiModalOpen] = useState<boolean>(false);
  const [isIoTSimulatorOpen, setIsIoTSimulatorOpen] = useState<boolean>(false);
  const [aoiExposure, setAoiExposure] = useState<ExposureBreakdown | null>(null);
  const [aoiCoords, setAoiCoords] = useState<[number, number][]>([]);

  // Core Data States
  const [currentAssessment, setCurrentAssessment] = useState<RiskAssessment | null>(null);
  const [allRisks, setAllRisks] = useState<RiskAssessment[]>([]);
  const [districtsGeoJson, setDistrictsGeoJson] = useState<any>(null);
  const [riversGeoJson, setRiversGeoJson] = useState<any>(null);
  const [floodExtentGeoJson, setFloodExtentGeoJson] = useState<any>(null);
  const [infrastructureGeoJson, setInfrastructureGeoJson] = useState<any>(null);
  const [sensorsData, setSensorsData] = useState<SensorTelemetry[]>([]);
  const [alertsData, setAlertsData] = useState<AlertRecord[]>([]);

  // Load Data from FastAPI Backend
  useEffect(() => {
    async function loadInitialData() {
      // 1. Districts GeoJSON
      const dists = await fetchApi<any>("/areas", null);
      setDistrictsGeoJson(dists);

      // 2. Rivers GeoJSON
      const rivs = await fetchApi<any>("/areas/rivers", null);
      setRiversGeoJson(rivs);

      // 3. Flood Extent GeoJSON
      const floods = await fetchApi<any>("/areas/flood-extent", null);
      setFloodExtentGeoJson(floods);

      // 4. Critical Infrastructure
      const infra = await fetchApi<any>("/exposure", null);
      setInfrastructureGeoJson(infra);

      // 5. Sensors
      const sensors = await fetchApi<SensorTelemetry[]>("/sensors", []);
      setSensorsData(sensors);

      // 6. Alerts
      const alerts = await fetchApi<AlertRecord[]>("/alerts", []);
      setAlertsData(alerts);

      // 7. All Risks
      const risks = await fetchApi<RiskAssessment[]>("/risk", []);
      setAllRisks(risks);
    }
    loadInitialData();
  }, []);

  const reloadSensors = async () => {
    const updated = await fetchApi<SensorTelemetry[]>("/sensors", []);
    setSensorsData(updated);
  };

  // Update assessment when selected district, hazard tab, or live mode changes
  useEffect(() => {
    async function loadAssessment() {
      let hazardParam = "OVERALL_CLIMATE";
      if (currentTab === "flood") hazardParam = "FLOOD";
      if (currentTab === "drought") hazardParam = "DROUGHT";
      if (currentTab === "water_stress") hazardParam = "WATER_STRESS";

      const modeParam = isLiveMode ? "live" : "demo";

      const assessment = await fetchApi<RiskAssessment>(
        `/risk/${selectedDistrict}?hazard=${hazardParam}&mode=${modeParam}`,
        null as any
      );
      setCurrentAssessment(assessment);
    }
    loadAssessment();
  }, [selectedDistrict, currentTab, isLiveMode]);

  // Determine active hazard layer for map coloring
  const getActiveHazardLayer = (): "OVERALL_CLIMATE" | "FLOOD" | "DROUGHT" | "WATER_STRESS" => {
    if (currentTab === "flood") return "FLOOD";
    if (currentTab === "drought") return "DROUGHT";
    if (currentTab === "water_stress") return "WATER_STRESS";
    return "OVERALL_CLIMATE";
  };

  if (currentTab === "landing") {
    return (
      <div>
        <Navbar
          currentTab={currentTab}
          setCurrentTab={setCurrentTab}
          activeRole={activeRole}
          setActiveRole={setActiveRole}
          isLiveMode={isLiveMode}
          setIsLiveMode={setIsLiveMode}
          onOpenGeeModal={() => setIsGeeModalOpen(true)}
        />
        <LandingView onEnterDashboard={() => setCurrentTab("overview")} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#fafaf9] text-stone-900 flex flex-col font-sans">
      {/* Top Navbar */}
      <Navbar
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
        activeRole={activeRole}
        setActiveRole={setActiveRole}
        isLiveMode={isLiveMode}
        setIsLiveMode={setIsLiveMode}
        onOpenGeeModal={() => setIsGeeModalOpen(true)}
      />


      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
        {/* District & Context Filter Header */}
        <div className="bg-white p-4 rounded-xl border border-stone-200 shadow-xs flex flex-wrap items-center justify-between gap-4">
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center space-x-2">
              <label htmlFor="district-select" className="text-xs font-bold text-stone-700 uppercase tracking-wider">
                Distrito Focal:
              </label>
              <select
                id="district-select"
                value={selectedDistrict}
                onChange={(e) => setSelectedDistrict(e.target.value)}
                className="bg-stone-50 border border-stone-200 text-stone-900 font-bold text-xs rounded-lg px-3 py-1.5 focus:ring-1 focus:ring-emerald-500"
              >
                <option value="manhica">Manhiça (Risco Alto/Crítico - Cheia Vale do Incomati)</option>
                <option value="marracuene">Marracuene (Risco Alto - Estuário do Incomati)</option>
                <option value="matola">Matola (Risco Moderado - Bacia Urbana)</option>
                <option value="boane">Boane (Risco Moderado - Umbeluzi / Albufeira)</option>
                <option value="magude">Magude (Risco Alto - Seca no Alto Incomati)</option>
                <option value="moamba">Moamba (Risco Moderado - Barragem de Corumana)</option>
                <option value="maputo_city">Maputo Cidade (Risco Moderado - Drenagem Costeira)</option>
                <option value="chokwe">Chókwè (Risco Crítico - Perímetro Irrigado Limpopo)</option>
              </select>
            </div>

            <div className="hidden sm:flex items-center space-x-1.5 text-xs text-stone-500 bg-stone-50 px-2.5 py-1 rounded-md border border-stone-200">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
              <span>Bacia Hidrográfica do Incomati & Grande Maputo</span>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => setIsSitRepOpen(true)}
              className="flex items-center space-x-1.5 bg-emerald-600 hover:bg-emerald-700 text-white px-3.5 py-1.5 rounded-lg text-xs font-bold shadow-xs transition-all"
            >
              <FileText className="w-4 h-4" />
              <span>Gerar Boletim Oficial (SitRep)</span>
            </button>
          </div>
        </div>

        {/* 4 Quick KPI Summary Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded-xl border border-stone-200 shadow-xs">
            <div className="flex items-center justify-between text-stone-500 text-xs">
              <span>Risco Médio da Bacia</span>
              <Waves className="w-4 h-4 text-emerald-700" />
            </div>
            <div className="text-2xl font-black text-stone-900 mt-1 font-mono">
              64.2 <span className="text-xs font-normal text-stone-500">/ 100</span>
            </div>
            <div className="text-[11px] font-semibold text-amber-700 mt-0.5">
              Nível Geral: ALTO (Cheias Aluviais)
            </div>
          </div>

          <div className="bg-white p-4 rounded-xl border border-stone-200 shadow-xs">
            <div className="flex items-center justify-between text-stone-500 text-xs">
              <span>População sob Alerta</span>
              <Users className="w-4 h-4 text-sky-700" />
            </div>
            <div className="text-2xl font-black text-stone-900 mt-1 font-mono">
              128,500 <span className="text-xs font-normal text-stone-500">hab</span>
            </div>
            <div className="text-[11px] text-stone-500 mt-0.5">
              Base: WorldPop Africa 100m
            </div>
          </div>

          <div className="bg-white p-4 rounded-xl border border-stone-200 shadow-xs">
            <div className="flex items-center justify-between text-stone-500 text-xs">
              <span>Edifícios na Cota Crítica</span>
              <Building2 className="w-4 h-4 text-emerald-700" />
            </div>
            <div className="text-2xl font-black text-stone-900 mt-1 font-mono">
              26,450
            </div>
            <div className="text-[11px] text-stone-500 mt-0.5">
              Google Open Buildings v3
            </div>
          </div>

          <div className="bg-white p-4 rounded-xl border border-stone-200 shadow-xs">
            <div className="flex items-center justify-between text-stone-500 text-xs">
              <span>Qualidade Telemetria (QC)</span>
              <Radio className="w-4 h-4 text-emerald-600" />
            </div>
            <div className="text-2xl font-black text-emerald-700 mt-1 font-mono">
              96.8%
            </div>
            <div className="text-[11px] text-emerald-800 font-semibold mt-0.5">
              7/7 Estações Ativas (ESP32)
            </div>
          </div>
        </div>

        {/* Tab Specific Views or Main Dashboard Grid */}
        {currentTab === "sensors" ? (
          <SensorsTable sensors={sensorsData} onOpenSimulator={() => setIsIoTSimulatorOpen(true)} />
        ) : currentTab === "alerts" ? (
          <AlertsList alerts={alertsData} onSelectArea={setSelectedDistrict} />
        ) : currentTab === "analytics" ? (
          <div className="space-y-6">
            <DistrictMatrixTable onSelectDistrict={setSelectedDistrict} isLiveMode={isLiveMode} />
            <TimeSeriesChart selectedDistrict={selectedDistrict} />
            <SensorsTable sensors={sensorsData} onOpenSimulator={() => setIsIoTSimulatorOpen(true)} />
          </div>
        ) : currentTab === "reports" ? (
          <div className="bg-white p-8 rounded-xl border border-stone-200 text-center space-y-4">
            <div className="w-12 h-12 rounded-xl bg-emerald-100 text-emerald-700 mx-auto flex items-center justify-center">
              <FileText className="w-6 h-6" />
            </div>
            <h2 className="text-xl font-black text-stone-900">
              Boletins & Relatórios de Situação Climática
            </h2>
            <p className="text-xs text-stone-600 max-w-md mx-auto">
              Gere relatórios padronizados para o Instituto Nacional de Gestão e Redução do Risco de Desastres (INGD), ARA-Sul e seguradoras agrícolas.
            </p>
            <button
              onClick={() => setIsSitRepOpen(true)}
              className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-6 py-2.5 rounded-lg text-xs shadow-xs"
            >
              Abrir Boletim Oficial de {currentAssessment?.area_name || "Manhiça"}
            </button>
          </div>
        ) : (
          /* Main 2-Column Responsive Layout: WebGIS on Left, Decision Intelligence on Right */
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Left 7 Columns: Interactive Map & Time Series */}
              <div className="lg:col-span-7 space-y-6">
                <div className="h-[520px]">
                  <DynamicMap
                    selectedDistrict={selectedDistrict}
                    onSelectDistrict={setSelectedDistrict}
                    activeHazardLayer={getActiveHazardLayer()}
                    districtsGeoJson={districtsGeoJson}
                    riversGeoJson={riversGeoJson}
                    floodExtentGeoJson={floodExtentGeoJson}
                    infrastructureGeoJson={infrastructureGeoJson}
                    sensorsData={sensorsData}
                    onOpenGeeConfig={() => setIsGeeModalOpen(true)}
                    onAoiCalculated={(exp, coords) => {
                      setAoiExposure(exp);
                      setAoiCoords(coords);
                      setIsAoiModalOpen(true);
                    }}
                  />
                </div>

                {/* Multi-temporal graph under the map */}
                <TimeSeriesChart selectedDistrict={selectedDistrict} />
              </div>

              {/* Right 5 Columns: Risk Score, Explainability & Exposure */}
              <div className="lg:col-span-5 space-y-6">
                {/* Risk Score & Level Card */}
                <RiskCard assessment={currentAssessment} />

                {/* Earth Observation GEE Spectral Metrics */}
                <EarthObservationPanel
                  selectedDistrict={selectedDistrict}
                  onOpenGeeConfig={() => setIsGeeModalOpen(true)}
                />

                {/* Explainability Engine */}
                <ExplainabilityPanel assessment={currentAssessment} />

                {/* Exposure Breakdown */}
                <ExposureMetrics
                  exposure={currentAssessment?.exposure || null}
                  areaName={currentAssessment?.area_name || selectedDistrict}
                />
              </div>
            </div>

            {/* Full Comparative District Matrix */}
            <DistrictMatrixTable
              onSelectDistrict={setSelectedDistrict}
              isLiveMode={isLiveMode}
            />
          </div>
        )}


        {/* Active Alerts Banner at Bottom */}
        {alertsData.length > 0 && currentTab !== "alerts" && (
          <div className="pt-2">
            <AlertsList alerts={alertsData} onSelectArea={setSelectedDistrict} />
          </div>
        )}
      </main>

      {/* Situation Report Modal */}
      <SitRepModal
        districtId={selectedDistrict}
        isOpen={isSitRepOpen}
        onClose={() => setIsSitRepOpen(false)}
      />

      {/* Google Earth Engine (GEE) Configuration Modal */}
      <GeeConfigModal
        isOpen={isGeeModalOpen}
        onClose={() => setIsGeeModalOpen(false)}
      />

      {/* Custom Drawn AOI Exposure Modal */}
      <CustomAoiModal
        isOpen={isAoiModalOpen}
        onClose={() => setIsAoiModalOpen(false)}
        exposure={aoiExposure}
        polygonCoords={aoiCoords}
      />

      {/* IoT Telemetry Simulator Modal */}
      <IoTSimulatorModal
        isOpen={isIoTSimulatorOpen}
        onClose={() => setIsIoTSimulatorOpen(false)}
        sensors={sensorsData}
        onTelemetryUpdated={reloadSensors}
      />
    </div>
  );
}
