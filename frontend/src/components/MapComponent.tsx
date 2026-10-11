"use client";

import React, { useEffect, useRef, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { API_BASE_URL, RiskAssessment } from "../lib/api";

interface MapComponentProps {
  selectedDistrict: string;
  onSelectDistrict: (districtId: string) => void;
  activeHazardLayer: "OVERALL_CLIMATE" | "FLOOD" | "DROUGHT" | "WATER_STRESS";
  districtsGeoJson: any;
  provincesGeoJson: any;
  riskAssessments: RiskAssessment[];
  riversGeoJson: any;
  floodExtentGeoJson: any;
  infrastructureGeoJson: any;
  sensorsData: any[];
  onOpenGeeConfig?: () => void;
  onAoiCalculated?: (exposure: any, coords: [number, number][]) => void;
}

export const MapComponent: React.FC<MapComponentProps> = ({
  selectedDistrict,
  onSelectDistrict,
  activeHazardLayer,
  districtsGeoJson,
  provincesGeoJson,
  riskAssessments,
  riversGeoJson,
  floodExtentGeoJson,
  infrastructureGeoJson,
  sensorsData,
  onOpenGeeConfig,
  onAoiCalculated,
}) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const layerGroupsRef = useRef<{ [key: string]: L.LayerGroup }>({});

  const [basemap, setBasemap] = useState<"satellite" | "light">("satellite");
  const [activeGeeIndex, setActiveGeeIndex] = useState<string>("none");
  const [geeNotice, setGeeNotice] = useState<string>("");
  const [isDrawingAoi, setIsDrawingAoi] = useState<boolean>(false);
  const [aoiPoints, setAoiPoints] = useState<[number, number][]>([]);
  const [isCalculatingAoi, setIsCalculatingAoi] = useState<boolean>(false);

  const [layersVisible, setLayersVisible] = useState({
    provinces: true,
    districts: true,
    rivers: true,
    floodExtent: true,
    infrastructure: true,
    sensors: true,
    radar: false,
  });

  const baseTilesRef = useRef<L.TileLayer | null>(null);
  const radarTileRef = useRef<L.TileLayer | null>(null);
  const geeTileRef = useRef<L.TileLayer | null>(null);
  const aoiLayerGroupRef = useRef<L.LayerGroup | null>(null);

  // Color is driven by current hazard scores; missing assessments are neutral gray.
  const getDistrictColor = (feature: any) => {
    const result = riskAssessments.find((risk) => risk.area_id === feature?.properties?.id);
    if (!result) return "#94a3b8";
    if (result.risk_score <= 20) return "#059669";
    if (result.risk_score <= 40) return "#eab308";
    if (result.risk_score <= 60) return "#f97316";
    if (result.risk_score <= 80) return "#dc2626";
    return "#7f1d1d";
  };

  // 1. Initialize Map
  useEffect(() => {
    if (!mapContainerRef.current) return;

    if (!mapInstanceRef.current) {
      const map = L.map(mapContainerRef.current, {
        center: [-25.55, 32.75],
        zoom: 9,
        minZoom: 7,
        maxZoom: 18,
        zoomControl: true,
      });

      // Default Basemap: ESRI World Imagery / Sentinel-2 High-res
      baseTilesRef.current = L.tileLayer(
        "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        {
          attribution: '&copy; <a href="https://www.esri.com/">ESRI</a> | Copernicus Sentinel-2 | Maxar',
          maxZoom: 18,
        }
      ).addTo(map);

      // RainViewer Live Weather Radar
      radarTileRef.current = L.tileLayer(
        "https://tilecache.rainviewer.com/v2/radar/nowcast_latest/256/{z}/{x}/{y}/2/1_1.png",
        {
          opacity: 0.65,
          zIndex: 50,
          attribution: '&copy; <a href="https://www.rainviewer.com/">RainViewer</a> Live Radar',
        }
      );

      // Layer groups
      layerGroupsRef.current = {
        provinces: L.layerGroup().addTo(map),
        districts: L.layerGroup().addTo(map),
        rivers: L.layerGroup().addTo(map),
        floodExtent: L.layerGroup().addTo(map),
        infrastructure: L.layerGroup().addTo(map),
        sensors: L.layerGroup().addTo(map),
      };

      aoiLayerGroupRef.current = L.layerGroup().addTo(map);

      mapInstanceRef.current = map;
    }

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, []);

  // 2. Basemap Switcher
  useEffect(() => {
    const map = mapInstanceRef.current;
    if (!map) return;

    if (baseTilesRef.current) {
      map.removeLayer(baseTilesRef.current);
    }

    if (basemap === "satellite") {
      baseTilesRef.current = L.tileLayer(
        "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        {
          attribution: '&copy; <a href="https://www.esri.com/">ESRI</a> | Copernicus Sentinel-2 | Maxar',
          maxZoom: 18,
        }
      ).addTo(map);
    } else {
      baseTilesRef.current = L.tileLayer(
        "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        {
          attribution: '&copy; <a href="https://carto.com/">CARTO</a> | OpenStreetMap contributors',
          subdomains: "abcd",
          maxZoom: 19,
        }
      ).addTo(map);
    }
  }, [basemap]);

  // 3. Radar Layer Visibility
  useEffect(() => {
    const map = mapInstanceRef.current;
    if (!map || !radarTileRef.current) return;

    if (layersVisible.radar) {
      if (!map.hasLayer(radarTileRef.current)) {
        radarTileRef.current.addTo(map);
      }
    } else {
      if (map.hasLayer(radarTileRef.current)) {
        map.removeLayer(radarTileRef.current);
      }
    }
  }, [layersVisible.radar]);

  // 4. Google Earth Engine (GEE) Satellite Layer
  useEffect(() => {
    const map = mapInstanceRef.current;
    if (!map) return;

    if (geeTileRef.current) {
      map.removeLayer(geeTileRef.current);
      geeTileRef.current = null;
    }

    setGeeNotice("");
    if (activeGeeIndex !== "none") {
      // Fetch GEE Tile URL from backend
      fetch(`${API_BASE_URL}/satellite/gee/tile`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          index: activeGeeIndex,
          district_id: selectedDistrict,
        }),
      })
        .then(async (res) => {
          const data = await res.json();
          if (!res.ok) throw new Error(data.detail || `HTTP ${res.status}`);
          return data;
        })
        .then((data) => {
          if (data && !data.is_processed_layer) {
            setGeeNotice("Índice indisponível: GEE ainda não processou esta camada. Não será mostrado um mapa-base com legenda espectral.");
            return;
          }
          if (data && data.tile_url && mapInstanceRef.current) {
            geeTileRef.current = L.tileLayer(data.tile_url, {
              opacity: 0.75,
              zIndex: 40,
              attribution: data.attribution || "Google Earth Engine (GEE)",
            }).addTo(mapInstanceRef.current);
          }
        })
        .catch((err) => {
          setGeeNotice("Camada GEE indisponível: " + (err?.message || "erro no processamento"));
          console.warn("GEE Tile fetch notice:", err);
        });
    }
  }, [activeGeeIndex, selectedDistrict]);

  // 5. Interactive AOI Drawing Mode
  useEffect(() => {
    const map = mapInstanceRef.current;
    if (!map) return;

    const onMapClick = (e: L.LeafletMouseEvent) => {
      if (!isDrawingAoi) return;
      const { lat, lng } = e.latlng;
      setAoiPoints((prev) => [...prev, [lat, lng]]);
    };

    map.on("click", onMapClick);
    return () => {
      map.off("click", onMapClick);
    };
  }, [isDrawingAoi]);

  // Render AOI points and polygon on map
  useEffect(() => {
    const aoiGroup = aoiLayerGroupRef.current;
    if (!aoiGroup) return;

    aoiGroup.clearLayers();

    if (aoiPoints.length > 0) {
      // Draw points
      aoiPoints.forEach(([lat, lng], idx) => {
        L.circleMarker([lat, lng], {
          radius: 5,
          fillColor: "#059669",
          color: "#ffffff",
          weight: 2,
          fillOpacity: 0.9,
        })
          .bindTooltip(`Vértice ${idx + 1}`, { permanent: false })
          .addTo(aoiGroup);
      });

      // Draw polyline or polygon
      if (aoiPoints.length >= 3) {
        L.polygon(aoiPoints, {
          color: "#059669",
          weight: 2.5,
          fillColor: "#10b981",
          fillOpacity: 0.25,
          dashArray: "5, 5",
        }).addTo(aoiGroup);
      } else if (aoiPoints.length === 2) {
        L.polyline(aoiPoints, {
          color: "#059669",
          weight: 2,
          dashArray: "5, 5",
        }).addTo(aoiGroup);
      }
    }
  }, [aoiPoints]);

  const handleFinishAoi = async () => {
    if (aoiPoints.length < 3) return;
    setIsCalculatingAoi(true);

    try {
      // Send [[lng, lat], ...] to backend
      const coords = aoiPoints.map(([lat, lng]) => [lng, lat]);
      // Close loop
      coords.push(coords[0]);

      const res = await fetch(`${API_BASE_URL}/exposure/custom-polygon`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(coords),
      });

      if (res.ok) {
        const exposureData = await res.json();
        if (onAoiCalculated) {
          onAoiCalculated(exposureData, aoiPoints);
        }
      }
    } catch (err) {
      console.error("AOI exposure calculation failed:", err);
    } finally {
      setIsCalculatingAoi(false);
      setIsDrawingAoi(false);
    }
  };

  const handleClearAoi = () => {
    setAoiPoints([]);
    setIsDrawingAoi(false);
    if (aoiLayerGroupRef.current) {
      aoiLayerGroupRef.current.clearLayers();
    }
  };

  // 6. Vector GeoJSON Layers
  useEffect(() => {
    const map = mapInstanceRef.current;
    const groups = layerGroupsRef.current;
    if (!map || !groups) return;

    // National provincial limits from GeoMoz.
    groups.provinces.clearLayers();
    if (layersVisible.provinces && provincesGeoJson) {
      L.geoJSON(provincesGeoJson, {
        style: { color: "#064e3b", weight: 1.5, opacity: 0.8, fillOpacity: 0 },
        interactive: false,
      }).addTo(groups.provinces);
    }

    // 1. Districts Layer
    groups.districts.clearLayers();
    if (layersVisible.districts && districtsGeoJson) {
      L.geoJSON(districtsGeoJson, {
        style: (feature) => ({
          fillColor: getDistrictColor(feature),
          fillOpacity: feature?.properties?.id === selectedDistrict ? 0.65 : 0.35,
          color: feature?.properties?.id === selectedDistrict ? "#064e3b" : "#475569",
          weight: feature?.properties?.id === selectedDistrict ? 3.5 : 1.5,
          dashArray: feature?.properties?.id === selectedDistrict ? "" : "3",
        }),
        onEachFeature: (feature, layer) => {
          const props = feature.properties || {};
          const isSelected = props.id === selectedDistrict;

          layer.bindTooltip(
            `<strong>${props.name}</strong><br/><span style="font-size: 11px; color: #475569;">${props.province} · GeoMoz 2017</span>`,
            { sticky: true, className: "text-xs font-sans" }
          );

          layer.on({
            click: () => {
              if (props.id && !isDrawingAoi) {
                onSelectDistrict(props.id);
              }
            },
            mouseover: (e) => {
              const l = e.target;
              l.setStyle({ fillOpacity: 0.75, weight: 3 });
            },
            mouseout: (e) => {
              const l = e.target;
              l.setStyle({
                fillOpacity: isSelected ? 0.65 : 0.35,
                weight: isSelected ? 3.5 : 1.5,
              });
            },
          });
        },
      }).addTo(groups.districts);
    }

    // 2. Rivers Layer
    groups.rivers.clearLayers();
    if (layersVisible.rivers && riversGeoJson) {
      L.geoJSON(riversGeoJson, {
        style: {
          color: "#0284c7",
          weight: 3.5,
          opacity: 0.85,
        },
        onEachFeature: (feature, layer) => {
          const p = feature.properties || {};
          layer.bindTooltip(`<strong>${p.name}</strong><br/>Traçado ilustrativo (DEMO)`, {
            sticky: true,
          });
        },
      }).addTo(groups.rivers);
    }

    // 3. Flood Extent (Sentinel-1 SAR)
    groups.floodExtent.clearLayers();
    if (layersVisible.floodExtent && floodExtentGeoJson) {
      L.geoJSON(floodExtentGeoJson, {
        style: {
          fillColor: "#0ea5e9",
          fillOpacity: 0.55,
          color: "#0369a1",
          weight: 2,
          dashArray: "4",
        },
        onEachFeature: (feature, layer) => {
          const p = feature.properties || {};
          layer.bindTooltip(
            `<div class="p-1">
              <strong class="text-sky-800">${p.name}</strong><br/>
              <span class="text-[11px] text-stone-600">Sensor: ${p.sensor}</span><br/>
              <span class="text-[11px] font-semibold text-rose-600">Lâmina estimada: ${p.water_depth_est_m}m</span>
            </div>`,
            { sticky: true }
          );
        },
      }).addTo(groups.floodExtent);
    }

    // 4. Critical Infrastructure
    groups.infrastructure.clearLayers();
    if (layersVisible.infrastructure && infrastructureGeoJson) {
      L.geoJSON(infrastructureGeoJson, {
        pointToLayer: (feature, latlng) => {
          const cat = feature.properties?.category;
          let markerColor = "#059669";
          let label = "INF";

          if (cat === "HEALTHCARE") {
            markerColor = "#dc2626";
            label = "+";
          } else if (cat === "TRANSPORT_CORRIDOR") {
            markerColor = "#d97706";
            label = "═";
          } else if (cat === "WATER_RESERVOIR") {
            markerColor = "#0284c7";
            label = "~";
          }

          const icon = L.divIcon({
            className: "custom-div-icon",
            html: `<div style="background-color: ${markerColor}; width: 22px; height: 22px; border-radius: 50%; border: 2px solid white; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 11px; box-shadow: 0 2px 6px rgba(0,0,0,0.25);">${label}</div>`,
            iconSize: [22, 22],
            iconAnchor: [11, 11],
          });

          return L.marker(latlng, { icon });
        },
        onEachFeature: (feature, layer) => {
          const p = feature.properties || {};
          layer.bindPopup(
            `<div style="font-family: sans-serif; font-size: 12px; line-height: 1.4;">
              <strong style="color: #064e3b; font-size: 13px;">${p.name}</strong><br/>
              <span style="color: #64748b;">Categoria:</span> <strong>${p.category}</strong><br/>
              <span style="color: #64748b;">Criticidade:</span> <strong style="color: ${p.criticality === 'CRITICAL' ? '#dc2626' : '#d97706'}">${p.criticality}</strong><br/>
              <span style="color: #64748b;">Risco de Inundação:</span> <strong>${p.flood_risk_exposure}</strong>
            </div>`
          );
        },
      }).addTo(groups.infrastructure);
    }

    // 5. Sensor Telemetry Nodes
    groups.sensors.clearLayers();
    if (layersVisible.sensors && sensorsData) {
      sensorsData.forEach((s) => {
        const statusColor = s.status === "ONLINE" ? "#059669" : s.status === "WARNING" ? "#d97706" : "#dc2626";

        const icon = L.divIcon({
          className: "sensor-icon",
          html: `<div style="background-color: #ffffff; border: 2.5px solid ${statusColor}; width: 24px; height: 24px; border-radius: 6px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(0,0,0,0.18);">
                  <span style="width: 8px; height: 8px; border-radius: 50%; background-color: ${statusColor};"></span>
                 </div>`,
          iconSize: [24, 24],
          iconAnchor: [12, 12],
        });

        const marker = L.marker([s.latitude, s.longitude], { icon });
        marker.bindPopup(
          `<div style="font-family: sans-serif; font-size: 12px;">
            <strong style="color: #064e3b; font-size: 13px;">${s.station_name}</strong><br/>
            <span style="color: #64748b;">ID:</span> <code>${s.sensor_id}</code><br/>
            <span style="color: #64748b;">Tipo:</span> <strong>${s.sensor_type}</strong><br/>
            <span style="color: #64748b;">Valor Atual:</span> <strong style="font-size: 14px; color: ${statusColor}">${s.current_value} ${s.unit}</strong><br/>
            <span style="color: #64748b;">Qualidade do Dado (QC):</span> <strong>${s.data_quality_score}%</strong><br/>
            <span style="color: #64748b;">Bateria:</span> <strong>${s.battery_pct}%</strong>
          </div>`
        );
        marker.addTo(groups.sensors);
      });
    }
  }, [
    selectedDistrict,
    activeHazardLayer,
    districtsGeoJson,
    provincesGeoJson,
    riskAssessments,
    riversGeoJson,
    floodExtentGeoJson,
    infrastructureGeoJson,
    sensorsData,
    layersVisible,
    isDrawingAoi,
  ]);

  return (
    <div className="relative w-full h-full min-h-[500px] rounded-xl overflow-hidden border border-stone-200 shadow-sm bg-white">
      {/* Map Container */}
      <div ref={mapContainerRef} className="w-full h-full min-h-[500px]" />

      {/* AOI Drawing Banner (Top-Center) */}
      {isDrawingAoi && (
        <div className="absolute top-3 left-1/2 -translate-x-1/2 z-[1000] bg-white/95 backdrop-blur-sm px-4 py-2 rounded-xl border border-emerald-300 shadow-lg flex items-center space-x-3 text-xs">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping"></span>
          <span className="font-bold text-emerald-900">
            Modo Desenho AOI: Clique no mapa para posicionar os vértices ({aoiPoints.length} marcados)
          </span>
          <button
            onClick={handleFinishAoi}
            disabled={aoiPoints.length < 3 || isCalculatingAoi}
            className="px-3 py-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-lg transition-colors disabled:opacity-50"
          >
            {isCalculatingAoi ? "Calculando..." : "Finalizar & Calcular"}
          </button>
          <button
            onClick={handleClearAoi}
            className="px-2.5 py-1 bg-stone-100 hover:bg-stone-200 text-stone-700 font-bold rounded-lg transition-colors"
          >
            Cancelar
          </button>
        </div>
      )}

      {/* Layer Control Box (Top-Right) */}
      <div className="absolute top-3 right-3 z-[1000] bg-white/95 backdrop-blur-sm p-3 rounded-lg border border-stone-200 shadow-md text-xs space-y-2.5 max-w-[240px]">
        {/* Basemap Switcher */}
        <div>
          <div className="font-bold text-stone-800 text-[11px] uppercase tracking-wider mb-1">
            Fundo Cartográfico
          </div>
          <div className="grid grid-cols-2 gap-1 bg-stone-100 p-0.5 rounded-md border border-stone-200">
            <button
              onClick={() => setBasemap("satellite")}
              className={`px-1.5 py-1 rounded text-[10px] font-bold transition-all ${
                basemap === "satellite"
                  ? "bg-emerald-600 text-white shadow-xs"
                  : "text-stone-600 hover:text-stone-900"
              }`}
            >
              🛰️ Satélite Real
            </button>
            <button
              onClick={() => setBasemap("light")}
              className={`px-1.5 py-1 rounded text-[10px] font-bold transition-all ${
                basemap === "light"
                  ? "bg-emerald-600 text-white shadow-xs"
                  : "text-stone-600 hover:text-stone-900"
              }`}
            >
              🗺️ Mapa Claro
            </button>
          </div>
        </div>

        {/* Google Earth Engine (GEE) Satellite Selector */}
        <div className="border-t border-stone-200 pt-2">
          <div className="flex items-center justify-between mb-1">
            <span className="font-bold text-emerald-900 text-[11px] uppercase tracking-wider flex items-center space-x-1">
              <span>🛰️ Earth Engine (GEE)</span>
            </span>
            {onOpenGeeConfig && (
              <button
                onClick={onOpenGeeConfig}
                className="text-[10px] text-emerald-700 hover:underline font-bold"
              >
                ⚙️ Ajustes
              </button>
            )}
          </div>
          <select
            value={activeGeeIndex}
            onChange={(e) => setActiveGeeIndex(e.target.value)}
            className="w-full bg-emerald-50/70 border border-emerald-300 text-emerald-900 font-bold text-[11px] rounded-lg px-2 py-1.5 focus:ring-1 focus:ring-emerald-500"
          >
            <option value="none">Nenhuma camada espectral</option>
            <option value="ndvi">🌱 Sentinel-2 NDVI (Vigor Vegetal / Seca)</option>
            <option value="ndwi">💧 Sentinel-2 NDWI (Água Superficial)</option>
            <option value="flood_sar">🌊 Sentinel-1 SAR (Mancha de Cheia)</option>
            <option value="elevation">⛰️ Copernicus DEM 30m (Elevação)</option>
            <option value="precipitation">🌧️ Radar & CHIRPS (Chuva)</option>
          </select>
        </div>

        {geeNotice && (
          <div role="status" className="text-[10px] text-amber-800 bg-amber-50 border border-amber-200 rounded p-2">
            {geeNotice}
          </div>
        )}

        {/* AOI Drawing Tool Trigger */}
        <div className="border-t border-stone-200 pt-2">
          {!isDrawingAoi ? (
            <button
              onClick={() => {
                setIsDrawingAoi(true);
                setAoiPoints([]);
              }}
              className="w-full py-1.5 bg-stone-100 hover:bg-emerald-50 hover:text-emerald-800 border border-stone-200 hover:border-emerald-300 text-stone-700 rounded-lg font-bold text-[11px] flex items-center justify-center space-x-1.5 transition-all"
            >
              <span>✏️ Desenhar Área de Risco (AOI)</span>
            </button>
          ) : (
            <button
              onClick={handleClearAoi}
              className="w-full py-1.5 bg-rose-50 border border-rose-200 text-rose-700 rounded-lg font-bold text-[11px] flex items-center justify-center space-x-1.5 transition-all"
            >
              <span>✕ Cancelar Desenho</span>
            </button>
          )}
        </div>

        {/* Layer Checkboxes */}
        <div className="border-t border-stone-200 pt-2 space-y-1.5">
          <div className="font-bold text-stone-800 text-[11px] uppercase tracking-wider mb-1">
            Camadas Vetoriais
          </div>

          <label className="flex items-center space-x-2 cursor-pointer text-stone-700 hover:text-stone-900">
            <input
              type="checkbox"
              checked={layersVisible.radar}
              onChange={(e) => setLayersVisible({ ...layersVisible, radar: e.target.checked })}
              className="rounded text-emerald-600 focus:ring-emerald-500 w-3.5 h-3.5"
            />
            <span className="flex items-center space-x-1 font-semibold text-emerald-900 text-[11px]">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping"></span>
              <span>Radar Chuva ao Vivo</span>
            </span>
          </label>

          <label className="flex items-center space-x-2 cursor-pointer text-stone-700 hover:text-stone-900">
            <input
              type="checkbox"
              checked={layersVisible.provinces}
              onChange={(e) => setLayersVisible({ ...layersVisible, provinces: e.target.checked })}
              className="rounded text-emerald-700 focus:ring-emerald-500 w-3.5 h-3.5"
            />
            <span>Províncias de Moçambique (GeoMoz)</span>
          </label>

          <label className="flex items-center space-x-2 cursor-pointer text-stone-700 hover:text-stone-900">
            <input
              type="checkbox"
              checked={layersVisible.districts}
              onChange={(e) => setLayersVisible({ ...layersVisible, districts: e.target.checked })}
              className="rounded text-emerald-600 focus:ring-emerald-500 w-3.5 h-3.5"
            />
            <span className="text-[11px]">Distritos-piloto (GeoMoz)</span>
          </label>

          <label className="flex items-center space-x-2 cursor-pointer text-stone-700 hover:text-stone-900">
            <input
              type="checkbox"
              checked={layersVisible.rivers}
              onChange={(e) => setLayersVisible({ ...layersVisible, rivers: e.target.checked })}
              className="rounded text-sky-600 focus:ring-sky-500 w-3.5 h-3.5"
            />
            <span className="text-[11px] flex items-center space-x-1">
              <span className="w-2 h-0.5 bg-sky-600 inline-block"></span>
              <span>Rios ilustrativos (DEMO)</span>
            </span>
          </label>

          <label className="flex items-center space-x-2 cursor-pointer text-stone-700 hover:text-stone-900">
            <input
              type="checkbox"
              checked={layersVisible.floodExtent}
              onChange={(e) => setLayersVisible({ ...layersVisible, floodExtent: e.target.checked })}
              className="rounded text-sky-500 focus:ring-sky-500 w-3.5 h-3.5"
            />
            <span className="text-[11px] flex items-center space-x-1">
              <span className="w-2 h-2 bg-sky-400/60 border border-sky-600 inline-block"></span>
              <span>Cheia simulada (DEMO)</span>
            </span>
          </label>

          <label className="flex items-center space-x-2 cursor-pointer text-stone-700 hover:text-stone-900">
            <input
              type="checkbox"
              checked={layersVisible.infrastructure}
              onChange={(e) => setLayersVisible({ ...layersVisible, infrastructure: e.target.checked })}
              className="rounded text-stone-600 focus:ring-stone-500 w-3.5 h-3.5"
            />
            <span className="text-[11px]">Infraestruturas Críticas</span>
          </label>

          <label className="flex items-center space-x-2 cursor-pointer text-stone-700 hover:text-stone-900">
            <input
              type="checkbox"
              checked={layersVisible.sensors}
              onChange={(e) => setLayersVisible({ ...layersVisible, sensors: e.target.checked })}
              className="rounded text-emerald-600 focus:ring-emerald-500 w-3.5 h-3.5"
            />
            <span className="text-[11px]">Estações IoT (Fase 2)</span>
          </label>
        </div>
      </div>

      {/* Cartographic Legend (Bottom-Left) */}
      <div className="absolute bottom-3 left-3 z-[1000] bg-white/95 backdrop-blur-sm p-3 rounded-lg border border-stone-200 shadow-md text-xs space-y-1.5 max-w-[240px]">
        {activeGeeIndex === "ndvi" ? (
          <div>
            <div className="font-bold text-stone-800 text-[11px] uppercase tracking-wider mb-1">
              Sentinel-2 NDVI (Vigor Vegetal)
            </div>
            <div className="h-3 w-full rounded bg-gradient-to-r from-[#8B4513] via-[#FFFACD] via-[#ADFF2F] to-[#006400] mb-1"></div>
            <div className="flex justify-between text-[10px] text-stone-600 font-mono">
              <span>-0.15 (Solo)</span>
              <span>0.35 (Mod)</span>
              <span>0.85 (Forte)</span>
            </div>
          </div>
        ) : activeGeeIndex === "ndwi" ? (
          <div>
            <div className="font-bold text-stone-800 text-[11px] uppercase tracking-wider mb-1">
              Sentinel-2 NDWI (Água Superficial)
            </div>
            <div className="h-3 w-full rounded bg-gradient-to-r from-[#8B4513] via-[#FFFFFF] via-[#00FFFF] to-[#00008B] mb-1"></div>
            <div className="flex justify-between text-[10px] text-stone-600 font-mono">
              <span>-0.5 (Solo Seco)</span>
              <span>0.0</span>
              <span>+0.5 (Lâmina d'água)</span>
            </div>
          </div>
        ) : activeGeeIndex === "elevation" ? (
          <div>
            <div className="font-bold text-stone-800 text-[11px] uppercase tracking-wider mb-1">
              Copernicus DEM 30m (Cota)
            </div>
            <div className="h-3 w-full rounded bg-gradient-to-r from-[#004b23] via-[#ccff33] via-[#f9c74f] to-[#f94144] mb-1"></div>
            <div className="flex justify-between text-[10px] text-stone-600 font-mono">
              <span>0m (Aluvial)</span>
              <span>50m</span>
              <span>150m (Planalto)</span>
            </div>
          </div>
        ) : (
          <div>
            <div className="font-bold text-stone-800 text-[11px] uppercase tracking-wider">
              Níveis de Risco Climático
            </div>
            <div className="grid grid-cols-2 gap-1 text-[11px] mt-1">
              <div className="flex items-center space-x-1.5">
                <span className="w-3 h-3 rounded bg-emerald-600"></span>
                <span className="text-stone-700">Baixo (0-20)</span>
              </div>
              <div className="flex items-center space-x-1.5">
                <span className="w-3 h-3 rounded bg-amber-500"></span>
                <span className="text-stone-700">Mod (21-40)</span>
              </div>
              <div className="flex items-center space-x-1.5">
                <span className="w-3 h-3 rounded bg-orange-600"></span>
                <span className="text-stone-700">Alto (41-60)</span>
              </div>
              <div className="flex items-center space-x-1.5">
                <span className="w-3 h-3 rounded bg-red-600"></span>
                <span className="text-stone-700">Crítico (&gt;80)</span>
              </div>
            </div>
          </div>
        )}

        <div className="text-[10px] text-stone-500 pt-1 border-t border-stone-200">
          *Google Earth Engine / Copernicus Sentinel-2 & GLO-30
        </div>
      </div>
    </div>
  );
};
