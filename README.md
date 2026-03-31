# 🤖 AI-Powered Text Classifier: End-to-End NLP Pipeline

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Medallion-orange.svg)](#-arquitetura-medalhão)
[![ML](https://img.shields.io/badge/ML-Hybrid_Inference-green.svg)](#-estratégia-de-machine-learning)

Este projeto implementa uma solução industrial de **Classificação de Mensagens de Atendimento** utilizando técnicas avançadas de Processamento de Linguagem Natural (NLP) e Engenharia de Dados. O sistema ingere dados via API, processa-os em múltiplas camadas de qualidade e disponibiliza uma interface de inferência híbrida.

---

## 🏗️ Arquitetura Medalhão (Data Engineering)

O pipeline segue o padrão de arquitetura medalhão para garantir a integridade e rastreabilidade dos dados:

1.  **Bronze (Staging):** Ingestão bruta de respostas do Typeform. Validação de esquema via `Pydantic`.
2.  **Silver (Processed):** Limpeza técnica, normalização e **Deduplicação Semântica**. Removemos mensagens idênticas para evitar *overfitting* e *data leakage*.
3.  **Gold (Master):** Dataset mestre pronto para ML, com particionamento de Treino (Train) e Teste (Test) estratificado por categoria.

---

## 🧠 Estratégia de Machine Learning

Devido à natureza dinâmica e, por vezes, escassa de dados reais, adotamos uma **Arquitetura de Inferência Híbrida**:

-   **Modelo Local (Scikit-Learn):** Um classificador `LogisticRegression` com `TfidfVectorizer` (n-grams 1-2) para processamento de baixo custo e alta performance.
-   **Fallback de Elite (OpenAI GPT-4o-mini):** Caso a confiança do modelo local seja inferior a **60%**, o sistema escala automaticamente a demanda para um LLM (Large Language Model), garantindo precisão superior mesmo em cenários de "Cold Start".

---

## 🛠️ Stack Tecnológico

-   **Linguagem:** Python 3.13
-   **Processamento:** Pandas, NumPy
-   **Machine Learning:** Scikit-Learn, Joblib
-   **IA Generativa:** OpenAI API (GPT-4o-mini)
-   **Interface:** Streamlit
-   **Engenharia:** Pydantic (Data Validation), Tenacity (Retry Logic)

---

## 🚀 Como Executar

### 1. Preparação do Ambiente
```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente (.env)
TYPEFORM_TOKEN=seu_token
TYPEFORM_FORM_ID=id_do_form
OPENAI_API_KEY=sua_chave_opcional
```

### 2. Rodar o Pipeline Completo (End-to-End)
Este comando executa a ingestão, processamento e treinamento do modelo local.
```bash
python main.py
```

### 3. Interface de Predição (CLI)
```bash
python predict.py "Minha fatura veio com valor errado, preciso de suporte financeiro."
```

### 4. Dashboard Web (Streamlit)
```bash
streamlit run app.py
```

---

## 📊 Governança e Qualidade

Para garantir a confiabilidade profissional, o projeto implementa:
-   **Prevenção de Data Leakage:** Filtro rigoroso de interseção de textos entre treino e teste.
-   **Logging Estruturado:** Rastreabilidade de cada fase do pipeline.
-   **Versionamento de Artefatos:** Modelos salvos em `/model` com metadados de versão.

---
**Desenvolvido sob padrões de Engenharia de Dados & AI Engineering.**
