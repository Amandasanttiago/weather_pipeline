# 🌤️ Weather Pipeline - Engenharia de Dados

![GitHub](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-green)
![Airflow](https://img.shields.io/badge/Airflow-2.0%2B-red)
![dbt](https://img.shields.io/badge/dbt-1.0%2B-orange)
![BigQuery](https://img.shields.io/badge/BigQuery-Cloud-blue)

---

## 📋 Sobre o Projeto

Pipeline de dados completo para coleta, processamento e análise de dados meteorológicos utilizando a API **Open-Meteo**.

O projeto implementa uma arquitetura moderna com camadas **RAW, STAGING, INTERMEDIATE e MARTS**, seguindo boas práticas de engenharia de dados (ELT).

---

## 🏗️ Arquitetura

```
API Open-Meteo 
    ↓
Airflow (Orquestração)
    ↓
PostgreSQL (RAW)
    ↓
BigQuery (Data Warehouse)
    ↓
dbt (Transformações)
    ↓
Dados Analíticos (MARTS)
```

---

## 🚀 Tecnologias Utilizadas

* **Apache Airflow** – Orquestração do pipeline
* **Astro CLI** – Gerenciamento do ambiente Airflow
* **PostgreSQL** – Camada RAW (Data Lake)
* **Google BigQuery** – Data Warehouse
* **dbt (Data Build Tool)** – Transformações e modelagem
* **Cosmos** – Integração Airflow + dbt
* **Docker** – Containerização

---

## 📊 Fluxo do Pipeline

### 1️⃣ Extract

* Coleta dados da API Open-Meteo (temperatura, umidade, precipitação)
* Previsão para 16 dias (Rio de Janeiro)
* Validação e logging

### 2️⃣ Load – Camada RAW

* Inserção no PostgreSQL
* Tabela `raw_weather` com estrutura JSONB
* Controle de `ingestion_timestamp`

### 3️⃣ Load – BigQuery

* Transferência PostgreSQL → BigQuery
* Dataset `weather_dataset`
* Tabela `raw_weather`

### 4️⃣ Transformações com dbt

#### 🔹 Staging (`stg_weather`)

* Parsing de timestamps
* Extração de data e hora
* Tratamento de tipos (CAST)
* Cálculo de umidade percentual
* Deduplicação

#### 🔹 Intermediate (`int_weather_enriched`)

* ID sequencial
* Dia da semana (DOW)
* Classificação por período do dia
* Classificação de temperatura

#### 🔹 Marts (`dim_weather`)

* Modelo final para análise
* Dados limpos, enriquecidos e prontos para BI

---

## 🔧 Configuração do Ambiente

### Pré-requisitos

* Docker + Docker Compose
* Astro CLI
* Conta Google Cloud com BigQuery ativado
* Python 3.9+

---

### 📥 Instalação

#### 1️⃣ Clone o repositório

```bash
git clone https://github.com/Amandasanttiago/weather_pipeline.git
cd weather_pipeline
```

#### 2️⃣ Configure as credenciais

Coloque sua chave JSON do Google Cloud em:

```
dags/dbt/weather_project/sua-chave.json
```

#### 3️⃣ Inicie o ambiente

```bash
astro dev start
```

#### 4️⃣ Acesse o Airflow

```
http://localhost:8080
Usuário: admin
Senha: admin
```

---

## 📈 Modelagem de Dados

### 📌 Tabela Final – `dim_weather`

| Coluna                    | Tipo      | Descrição                          |
| ------------------------- | --------- | ---------------------------------- |
| id_weather                | INTEGER   | Identificador único                |
| data                      | DATE      | Data da medição                    |
| hora                      | TIME      | Hora da medição                    |
| temperatura               | FLOAT64   | Temperatura (°C)                   |
| humidade                  | FLOAT64   | Umidade relativa (%)               |
| dia_semana                | INTEGER   | Dia da semana (1–7)                |
| periodo_dia               | STRING    | manhã/tarde/noite/madrugada        |
| classificacao_temperatura | STRING    | muito_quente/quente/agradavel/frio |
| ingestion_timestamp       | TIMESTAMP | Timestamp de ingestão              |

---

## 🔒 Segurança

* Credenciais via variáveis de ambiente
* `.json` fora do versionamento
* `.gitignore` configurado
* Conexões seguras

---

## ✅ Testes Implementados

* Teste de singularidade (ID único)
* Teste de não nulidade
* Teste de valores aceitos

---

## 🎯 Próximos Passos

* [ ] Implementar testes unitários completos
* [ ] Criar dashboard no Looker Studio
* [ ] Configurar alertas de falha
* [ ] Publicar documentação com dbt docs

---

## 📝 Licença

MIT License

---

## 👩‍💻 Autora

**Amanda Santiago**
Engenheira de Dados

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge\&logo=github\&logoColor=white)](https://github.com/Amandasanttiago)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge\&logo=linkedin\&logoColor=white)](https://linkedin.com/in/amanda-santiago)

---

⭐ Se este projeto te ajudou, considere dar uma estrela!
