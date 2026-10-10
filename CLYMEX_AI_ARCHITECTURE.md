# CLYMEX AI — Arquitetura de Inteligência de Risco Climático
**"Predict Risk. Protect Tomorrow."**

---

## 1. Visão Geral e Posicionamento

O **CLYMEX AI** é uma plataforma de Inteligência de Risco Climático de nível institucional e operacional, desenhada para transformar terabytes de dados geoespaciais brutos (satélites, reanálises meteorológicas, hidrologia, topografia e vulnerabilidade socioeconômica) em **inteligência preditiva acionável**.

O foco demonstrador inicial é **Moçambique**, com ênfase na **Grande Maputo e Bacia Hidrográfica do Rio Incomati** (abrangendo áreas de alto risco de cheias e estresse hídrico como Manhiça, Marracuene, Boane, Magude, Moamba e Xai-Xai), concebido desde o primeiro commit para escalar para toda a África Austral (SADC) e o continente africano.

> **Princípio Fundamental:** O CLYMEX AI **não é apenas um visualizador de mapas (GIS viewer)**. É um motor de decisão que responde a cinco perguntas essenciais:
> 1. **O quê?** (Tipo de perigo: Cheia, Seca, Estresse Hídrico)
> 2. **Onde?** (Localização precisa, limites administrativos e bacias hidrográficas)
> 3. **Quando?** (Horizonte temporal: monitoramento atual, 7 dias, 30 dias, sazonal)
> 4. **Por quê?** (Fatores contribuintes mensuráveis e explicáveis)
> 5. **Com que confiança?** (Índice de confiança baseado na qualidade e frescura dos dados)

---

## 2. A Arquitetura em 7 Camadas

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ CAMADA 7 — APLICAÇÕES & INTERFACES                                         │
│ • Dashboard WebGIS Interativo (Next.js 14, MapLibre GL, Tailwind, Shadcn/UI) │
│ • Portais de Decisão por Perfil (Admin, Analista, Instituição, Cidadão)     │
│ • Canais de Disseminação Rápida: REST API, Webhooks, Alertas por SMS/WhatsApp│
└──────────────────────────────────────▲──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────┴──────────────────────────────────────┐
│ CAMADA 6 — INTELIGÊNCIA DE DECISÃO & RELATÓRIOS                             │
│ • Score de Risco Climático Unificado (0 a 100)                              │
│ • Motor de Explicabilidade Científica (Decomposição de fatores de risco)    │
│ • Gerador Automático de Boletins e SitReps (PDF / Markdown / JSON)          │
│ • Sistema de Alertas Antecipados (Early Warning) com Níveis de Ação        │
└──────────────────────────────────────▲──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────┴──────────────────────────────────────┐
│ CAMADA 5 — MOTOR DE RISCO CLIMÁTICO (RISK ENGINE)                           │
│ • Equação Central de Risco: RISCO = PERIGO (H) × EXPOSIÇÃO (E) × VULN. (V)   │
│ • Classificação Normalizada: BAIXO (0-20), MODERADO (21-40), ALTO (41-60),  │
│   MUITO ALTO (61-80), CRÍTICO (81-100)                                      │
│ • Rastreabilidade de Proveniência: OBSERVED vs ESTIMATED vs PREDICTED vs DEMO│
└──────────────────────────────────────▲──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────┴──────────────────────────────────────┐
│ CAMADA 4 — MOTORES GEOAI & MACHINE LEARNING                                 │
│ • Motor de Cheias: Chuva acumulada + Declive + TWI + SAR Water Change       │
│ • Motor de Secas: Anomalia NDVI (VCI) + Percentil de Umidade do Solo + Temp │
│ • Motor de Estresse Hídrico: Déficit de Evapotranspiração + Balanço Hídrico  │
│ • Detecção de Anomalias Geoespaciais (Z-Score sobre baselines históricos)    │
└──────────────────────────────────────▲──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────┴──────────────────────────────────────┐
│ CAMADA 3 — PROCESSAMENTO GEOESPACIAL & DADOS ESPACIAIS                      │
│ • Banco de Dados Espacial: PostgreSQL + PostGIS (com suporte a TimescaleDB) │
│ • Pipeline Python: GeoPandas, Shapely, Rasterio, GDAL, PyProj               │
│ • Servidor de Vetores e Tiles: MVT (Mapbox Vector Tiles) e COG              │
│ • Isolamento de Modo DEMO com dados sintéticos fisicamente realistas        │
└──────────────────────────────────────▲──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────┴──────────────────────────────────────┐
│ CAMADA 2 — INGESTÃO & CONECTORES DE DADOS                                   │
│ • Ponte com Google Earth Engine (Processamento em nuvem via Python SDK)     │
│ • Ingestores Meteorológicos: ERA5-Land, CHIRPS, GPM IMERG                   │
│ • Ingestores de Exposição: Google Open Buildings, WorldPop, OpenStreetMap    │
│ • Gateway IoT (Fase 2): Broker MQTT para telemetria de sensores ESP32       │
└──────────────────────────────────────▲──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────┴──────────────────────────────────────┐
│ CAMADA 1 — FONTES DE DADOS E SENSORES                                       │
│ • Óptico: Sentinel-2 MSI, Landsat 8/9, MODIS                                │
│ • Radar (SAR): Sentinel-1 C-Band SAR (detecção de água sob nuvens)          │
│ • Modelo Digital de Elevação: Copernicus DEM GLO-30 / SRTM 30m              │
│ • Hidrografia: Bacias hidrográficas, rede de rios (HydroSHEDS)              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Metodologia Científica de Risco

O cálculo de risco no CLYMEX AI segue a convenção internacional do UNDRR (Escritório das Nações Unidas para a Redução do Risco de Desastres) e do IPCC:

$$\text{Risco} = \text{Perigo (Hazard)} \times \text{Exposição (Exposure)} \times \text{Vulnerabilidade (Vulnerability)}$$

### 3.1 Perigo de Cheias ($H_{\text{flood}} \in [0, 100]$)
Combina indicadores hidrometeorológicos e morfométricos do terreno:
1. **Precipitação Recente e Anomalia:** Volume acumulado em 3, 7 e 30 dias (via CHIRPS/ERA5) comparado com a média climatológica móvel.
2. **Topografia e Escoamento:** Modelo Digital de Elevação (DEM GLO-30), declividade e *Topographic Wetness Index* (TWI):
   $$\text{TWI} = \ln\left(\frac{\alpha}{\tan \beta}\right)$$
   onde $\alpha$ é a área de contribuição a montante e $\beta$ é a inclinação local.
3. **Proximidade à Rede Hidrográfica:** Distância ponderada aos canais principais do Rio Incomati e afluentes.
4. **Água Superficial por Radar SAR:** Variação no retroespalhamento de Sentinel-1 (VV/VH backscatter change) para detectar acúmulo de lâmina d'água mesmo sob chuva intensa e cobertura total de nuvens.

### 3.2 Perigo de Secas ($H_{\text{drought}} \in [0, 100]$)
1. **Índice de Condição da Vegetação (VCI):**
   $$\text{VCI} = \frac{\text{NDVI} - \text{NDVI}_{\min}}{\text{NDVI}_{\max} - \text{NDVI}_{\min}} \times 100$$
2. **Anomalia de Umidade do Solo:** Déficit em relação ao percentil histórico do horizonte superficial e radicular.
3. **Índice Padronizado de Precipitação (SPI):** Desvio padrão da precipitação em 30 e 90 dias.
4. **Anomalia de Temperatura da Superfície (LST):** Desvio de calor que amplifica a evapotranspiração.

### 3.3 Motor de Exposição ($E \in [0, 100]$)
A camada de exposição quantifica ativamente os bens humanos e materiais situados na zona de influência do perigo:
- **População exposta:** Estimada com base em densidade WorldPop e censos locais.
- **Edifícios e estruturas:** Integração da base **Google Open Buildings** (edifícios mapeados por IA com estimativa de área e altura) e OpenStreetMap.
- **Infraestrutura crítica:** Hospitais, centros de saúde, escolas, pontes e eixos rodoviários estratégicos (como a Estrada Nacional EN1).
- **Agricultura:** Áreas de cultivo de subsistência e comercial (culturas irrigadas de açúcar e hortícolas ao longo do vale do Incomati).

### 3.4 Matriz de Classificação de Risco
O escore final varia de 0 a 100 e é mapeado para níveis operacionais:

| Escore | Nível | Ação Operacional |
| :--- | :--- | :--- |
| **0 – 20** | **BAIXO (LOW)** | Monitoramento de rotina e manutenção de sensores. |
| **21 – 40** | **MODERADO (MODERATE)** | Alerta preventivo às lideranças distritais. |
| **41 – 60** | **ALTO (HIGH)** | Emissão de boletim antecipado; proteção de ativos vulneráveis. |
| **61 – 80** | **MUITO ALTO (VERY HIGH)** | Pré-mobilização de equipes de defesa civil e agricultores. |
| **81 – 100**| **CRÍTICO (CRITICAL)** | Ativação do protocolo de contingência e evacuação preventiva. |

---

## 4. Stack Tecnológica de Produção

### Frontend
- **Framework:** Next.js 14+ (App Router), React 18/19, TypeScript
- **Estilização & Componentes:** Tailwind CSS, Shadcn/UI (Radix UI), Lucide Icons
- **Visualização Geoespacial:** MapLibre GL JS / Leaflet, com suporte a vector tiles e rasters
- **Gráficos e Séries Temporais:** Recharts
- **Design System:** Tema escuro/claro com paleta voltada a salas de controle e centros de comando

### Backend & Processamento Geoespacial
- **Linguagem & Framework:** Python 3.11+, FastAPI, Pydantic v2
- **Bibliotecas Geoespaciais:** GeoPandas, Shapely, Rasterio, PyProj, GDAL, NumPy, SciPy
- **Machine Learning & Estatística:** Scikit-Learn, XGBoost, Anomaly Detection (Z-Score & Isolation Forest)
- **Integração de Satélites:** Conector isolado para Google Earth Engine (Python API `ee`)
- **Autenticação & Segurança:** JWT, hashing com bcrypt, RBAC (`ADMIN`, `ANALYST`, `INSTITUTION`, `VIEWER`)

### Banco de Dados & Armazenamento
- **Banco Principal:** PostgreSQL 16 com extensão PostGIS 3.4
- **Dados Temporais/IoT:** Arquitetura compatível com TimescaleDB para telemetria de sensores
- **Modo Local:** Suporte a SQLite + SpatiaLite / GeoJSON serializado para desenvolvimento rápido sem atrito de dependências externas

---

## 5. Roteiro de Implementação em Fases

1. **Fase 1 (MVP Imediato):**
   - Estrutura monorepo modular (`/backend` e `/frontend`).
   - Base geoespacial de Moçambique e Bacia do Incomati (Distritos: Manhiça, Marracuene, Matola, Boane, Magude, Moamba, Namaacha, Chókwè).
   - Motores de Cheia, Seca e Estresse Hídrico com explicabilidade clara.
   - Modo DEMO explícito com dados sintéticos cientificamente plausíveis para demonstração instantânea offline.
   - Dashboard WebGIS interativo com filtros administrativos e alternância de camadas.
   - Geração de relatórios de situação (SitRep) em formato visual e exportável.
   - Documentação OpenAPI/Swagger completa.

2. **Fase 2 (IoT & Telemetria em Tempo Real):**
   - Conexão de sensores de nível de água por ultrassom/radar via ESP32.
   - Broker MQTT (Mosquitto/EMQX) e ingestion service com validação de dados (data quality score).

3. **Fase 3 (GeoAI Avançada & Expansão SADC):**
   - Segmentação de inundações em tempo real por redes neurais convolucionais (U-Net) em imagens de radar.
   - Modelos de previsão hidrológica baseados em redes neurais de grafos (GNN) ao longo da bacia fluvial.
   - Suporte multi-país (África do Sul, Eswatini, Zimbábue, Zâmbia, Malawi).
