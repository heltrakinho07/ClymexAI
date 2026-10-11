# CLYMEX AI
### *"Predict Risk. Protect Tomorrow."*

Plataforma de **Inteligência e Risco Climático** orientada à transformação de terabytes de dados geoespaciais, satelitais, meteorológicos, hidrológicos e socioeconômicos em **inteligência preditiva acionável**.

O demonstrador da **Fase 1 (MVP)** tem foco em **Moçambique**, com ênfase na **Bacia Hidrográfica do Rio Incomati e Grande Maputo** (distritos de Manhiça, Marracuene, Matola, Boane, Magude, Moamba, Maputo Cidade e Chókwè), concebido desde o primeiro commit para escalar para toda a África Austral (SADC).

---

## 🌿 Identidade Visual & Design System

Conforme especificação operacional, o CLYMEX AI utiliza uma paleta de **Cores Naturais e Branco Puro**:
- **Canvas Principal:** Branco puro (`#ffffff`) e pedra suave (`#fafaf9`).
- **Verdes Naturais & Floresta:** Tons de esmeralda e floresta (`#064e3b`, `#059669`, `#10b981`) para vegetação, sustentabilidade e risco baixo.
- **Tons Hidro & Oceânicos:** Azuis oceânicos (`#0284c7`, `#0369a1`, `#0ea5e9`) para o Rio Incomati, hidrografia e radar Sentinel-1 SAR.
- **Tons de Terra & Seca:** Âmbar e terracota (`#b45309`, `#d97706`, `#f59e0b`) para solos, topografia e estresse hídrico.
- **Alertas de Risco:** Escala semafórica padronizada (Verde = Baixo, Âmbar = Moderado, Laranja = Alto, Vermelho = Crítico).

---

## 🏛️ A Arquitetura em 7 Camadas

```
DADOS (Satélites Sentinel-1/2, CHIRPS, ERA5, Copernicus DEM, Google Open Buildings)
  ↓
INGESTÃO (Conectores Python, Google Earth Engine Bridge, Reanálise)
  ↓
PROCESSAMENTO GEOESPACIAL (GeoPandas, Shapely, TWI, Anomalias Z-score)
  ↓
GEOAI & ML (Motores de Cheia, Seca e Estresse Hídrico)
  ↓
MOTOR DE RISCO CLIMÁTICO (Risco = Perigo × Exposição × Vulnerabilidade)
  ↓
INTELIGÊNCIA DE DECISÃO (Explicabilidade AI, Alertas Antecipados, Boletins SitRep)
  ↓
APLICAÇÕES (Dashboard WebGIS Leaflet, REST API v1, Alertas)
```

---

## 🔬 Metodologia Científica do Motor de Risco

O escore de risco varia de **0 a 100** e é calculado segundo as diretrizes do UNDRR:

$$\text{Risco} = \text{Perigo (H)} \times \text{Exposição (E)} \times \text{Vulnerabilidade (V)}$$

| Escore | Nível Operacional | Significado Prático |
| :--- | :--- | :--- |
| **0 – 20** | **BAIXO (LOW)** | Monitoramento de rotina; condições hidrológicas normais. |
| **21 – 40** | **MODERADO (MODERATE)** | Aviso preventivo aos comitês distritais. |
| **41 – 60** | **ALTO (HIGH)** | Emissão de alerta antecipado; salvaguarda de infraestrutura. |
| **61 – 80** | **MUITO ALTO (VERY HIGH)** | Pré-mobilização de meios de resgate e evacuação de várzeas. |
| **81 – 100**| **CRÍTICO (CRITICAL)** | Ativação do protocolo de contingência e salvamento de vidas. |

### Explicabilidade Científica (Explainability)
Cada predição do CLYMEX AI responde obrigatoriamente a cinco perguntas:
1. **O quê?** (Perigo específico: Cheia Aluvial, Seca Agrícola, Estresse Hídrico)
2. **Onde?** (Distrito, Bacia e coordenadas geográficas)
3. **Quando?** (Janela temporal e acumulação de chuvas)
4. **Por quê?** (Fatores contribuintes percentuais: TWI, declive, anomalia de chuva, expansão de lâmina de água por radar)
5. **Com que confiança?** (Índice de confiança baseado na qualidade das fontes orbitais)

---

## 🗺️ Limites administrativos reais de Moçambique — GeoMoz

O CLYMEX usa a biblioteca Python **[GeoMoz](https://github.com/geolithicamz-hub/geomoz)** para obter fronteiras administrativas de Moçambique, em vez de desenhar polígonos sintéticos como se fossem limites oficiais.

```bash
pip install geomoz
```

O pacote também está listado em `backend/requirements.txt` e é instalado pela imagem Docker do backend. No primeiro carregamento, o GeoMoz pode descarregar os conjuntos de dados de províncias e distritos do seu repositório externo e guardá-los em cache. A execução inicial exige conectividade com essa fonte (ou um cache previamente preparado).

- `GET /api/v1/areas`: distritos-piloto cobertos pelo demonstrador, com geometrias GeoMoz.
- `GET /api/v1/areas/provinces`: todas as províncias e a Cidade de Maputo.
- `GET /api/v1/areas/districts`: todos os distritos GeoMoz.
- `GET /api/v1/areas/districts?province=Gaza`: distritos da província indicada.
- `GET /api/v1/areas/districts?focus_only=true`: só as geometrias-piloto.

**Importante:** estes dados administrativos são uma referência cartográfica (base 2017). Não demonstram, por si só, a extensão actual de uma cheia. Se GeoMoz estiver indisponível, o endpoint devolve erro e não substitui as fronteiras por geometrias falsas.

O mapa diferencia as camadas administrativas reais da hidrografia e das manchas de cheia **demonstrativas**. A opção meteorológica externa gera uma avaliação **ESTIMATED**, porque continua a combinar observações/modelos meteorológicos com parâmetros inferidos. As camadas de índices GEE só são desenhadas como resultados calculados quando o serviço entrega uma imagem efectivamente processada.

### 929 Challenge 2026

A estratégia de produto, discurso comercial, guião de demonstração e critérios de validação para o concurso encontram-se em [docs/929_CHALLENGE_2026.md](docs/929_CHALLENGE_2026.md). O estado actual é de **protótipo demonstrativo**, não serviço oficial de aviso antecipado.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.11+ (ou 3.14)
- Node.js 18+ (ou 20+)
- npm 9+

---

### Opção 1: Inicialização Rápida no Windows (1 Clique)
Basta clicar duas vezes no arquivo ou executar no terminal:
```powershell
.\start_clymex.bat
```
Este script inicia:
1. O backend FastAPI na porta `http://localhost:8000`
2. O frontend Next.js na porta `http://localhost:3000`

---

### Opção 2: Inicialização Manual

#### 1. Backend (FastAPI):
```powershell
# Ativar o ambiente virtual
.\venv\Scripts\Activate.ps1

# Definir o PYTHONPATH e iniciar a API
$env:PYTHONPATH="backend"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- **Documentação Interativa Swagger:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Healthcheck:** [http://localhost:8000/health](http://localhost:8000/health)

#### 2. Frontend (Next.js 14 + Leaflet):
```powershell
cd frontend
npm run dev
```
- **Dashboard WebGIS:** [http://localhost:3000](http://localhost:3000)

---

### Opção 3: Execução com Docker Compose
```bash
docker-compose up --build
```

---

## 🧪 Executando os Testes Automatizados

### Testes do Backend (Pytest):
```powershell
$env:PYTHONPATH="backend"
.\venv\Scripts\python.exe -m pytest backend/tests -v
```
*Garante 100% de cobertura nos cálculos dos motores de Cheia, Seca, Estresse Hídrico, Exposição e rotas da API.*

### Validação do Build do Frontend (Next.js):
```powershell
cd frontend
npm run build
```

---

## 📡 Roteiro das Próximas Fases

- **Fase 2 (IoT & Telemetria em Tempo Real):** Instalação de sensores de nível com ESP32 e LoRaWAN nas pontes do Rio Incomati (ex: E-33 da EN1) conectados via MQTT com controle de qualidade automatizado (QC).
- **Fase 3 (GeoAI Avançada & Expansão SADC):** Segmentação de inundações por redes neurais convolucionais (U-Net) em imagens de radar SAR, modelos de grafos neurais (GNN) hidrológicos e expansão para Eswatini, África do Sul e Zimbábue.

---

**CLYMEX AI** — *Predict Risk. Protect Tomorrow.*
