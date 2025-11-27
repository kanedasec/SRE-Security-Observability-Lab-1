# SRE Security Observability Lab 1

Este laboratório tem como objetivo mostrar, na prática, como **riscos de segurança podem ser tratados como métricas de confiabilidade**, permitindo controles automatizados, SLOs, dashboards e alertas.

## Objetivo do Projeto

Criar um serviço simples (Flask) **instrumentado com Prometheus** para observar:

- Taxa de sucesso de login (SLI)
- Falhas de autenticação (401)
- Latência de login (p95)
- Healthcheck da aplicação
- Coleta e raspagem de métricas via Prometheus
- Visualização dos indicadores no Grafana

Este laboratório serve como base para os próximos (alerting, ITGC automatizado, evidências contínuas, IAM, CloudTrail, GuardDuty, etc.).

---

## Estrutura do Repositório

```
project-1-sre-security-observability/
  ├── app/
  │   ├── api.py
  │   └── Dockerfile
  ├── docker-compose.yml
  ├── requirements.txt
  ├── prometheus/
  │   └── prometheus.yml
  ├── grafana/
  │   └── dashboards/
  └── README.md
```

---

## Componentes

### **1. Flask API (Instrumentada)**
Endpoints:

- `/healthz` – healthcheck
- `/login` – login com falhas aleatórias (30% de chance)
- `/metrics` – endpoint Prometheus

Métricas expostas:

- `login_requests_total`
- `login_failures_total`
- `login_latency_seconds` (histograma)

### **2. Prometheus**
- Configurado para fazer scrape a cada 5s
- Coleta as métricas expostas pela API
- Disponível em `http://localhost:9090`

### **3. Grafana**
- Conectado ao Prometheus
- Dashboards para:
  - SLI de login
  - p95 de latência
  - taxa de falhas
- Disponível em `http://localhost:3000`

---

## SLIs, SLOs e SLA (SRE aplicado a segurança)

### **SLIs (Service Level Indicators)**

- **Confiabilidade de Login:**  

  ```
  (sum(rate(login_requests_total[5m])) - sum(rate(login_failures_total[5m])))
    / sum(rate(login_requests_total[5m]))
  ```

- **Performance (p95):**

  ```
  histogram_quantile(
    0.95,
    sum(rate(login_latency_seconds_bucket[5m])) by (le)
  )
  ```

### **SLOs (Service Level Objectives)**

- **SLO 1 — Confiabilidade de login:**  
  99% de logins bem-sucedidos em janelas de 5 minutos.

- **SLO 2 — Latência:**  
  p95 de latência < 300 ms.

---

## Executando o projeto

### 1. Build e execução

```
docker compose up --build
```

### 2. Acessos rápidos

- **API:** http://localhost:5000/healthz  
- **Prometheus:** http://localhost:9090  
- **Grafana:** http://localhost:3000  

### 3. Gerar tráfego para alimentar métricas

```
#!/usr/bin/env bash
for i in {1..50}; do
    curl -s -o /dev/null -w "%{http_code}
" http://localhost:5000/login
done
```

---

## 🧠 Conceitos Aprendidos no Laboratório

- Como instrumentar serviços
- Como transformar risco de AppSec em métrica *quantitativa*
- Como construir SLIs e SLOs baseados em comportamento de segurança
- Como montar dashboards operacionais com foco em segurança
- Base para alertas de segurança orientados a SLO (próximo laboratório)

---

## 📚 Referências

- Prometheus client_python docs
- Grafana Dashboards Guide
- CNCF Observability Whitepaper
