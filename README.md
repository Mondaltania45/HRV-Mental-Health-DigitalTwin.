# WHO-Style Explainable Digital Twin of Heart Rate Variability and Cognitive Mental Load

[![Developer](https://img.shields.io/badge/Developer-Ms.%20Taniya%20Mondal%2C%20B.Tech-blue.svg)](#lead-developer)
[![Version](https://img.shields.io/badge/Version-1.0-emerald.svg)](#version-history)
[![Framework](https://img.shields.io/badge/Standard-WHO%20Digital%20Health-teal.svg)](https://www.who.int)
[![Dataset](https://img.shields.io/badge/Dataset-Kaggle%20HRV%20%26%20MWL%20(Auditya%20Sutarto)-orange.svg)](https://www.kaggle.com/datasets/audityasutarto/heart-rate-variability-and-cognitive-mental-load)
[![Explainability](https://img.shields.io/badge/XAI-SHAP%20TreeExplainer-purple.svg)](#explainable-ai-framework)

---

## 📋 Executive Overview

This repository presents an **Explainable, WHO-Grounded In Silico Digital Twin** for monitoring cardiovascular autonomic regulation and predicting subjective cognitive mental workload (**NASA-TLX**). 

Trained and validated on empirical biotelemetry from the benchmark **Auditya Sutarto Heart Rate Variability and Cognitive Mental Workload Dataset** (30 human participants across 60 multi-condition trials), the framework bridges clinical psychophysiology with predictive artificial intelligence and Explainable AI (XAI).

### 🌟 Key Capabilities
1. **In Silico Autonomic Modeling**: Continuous virtual synchronization of cardiac autonomic state vector $\mathbf{s}(t) = [\text{HR}, \text{SDNN}, \text{RMSSD}, \text{LF}, \text{HF}, \text{LF/HF}]$.
2. **Cognitive Workload Prediction**: Machine learning pipeline predicting continuous NASA Task Load Index ($0 - 100$) with cross-participant GroupKFold validation.
3. **WHO Clinical Risk Stratification**: Four-tier clinical stratification (Tier I: Optimal, Tier II: Adaptive, Tier III: Compensatory Overload Risk, Tier IV: Severe Exhaustion).
4. **Explainable AI (XAI) Engine**: SHAP (SHapley Additive exPlanations) TreeExplainer decomposition providing local directional attributions, automated natural language WHO clinical narratives, and counterfactual intervention guidance.
5. **Interactive "What-If" Counterfactual Simulator**: In silico experimentation testing the physiological impact of 0.1 Hz resonant paced breathing, mindful micro-breaks, and prolonged overwork before clinical implementation.
6. **WHO 0.1 Hz Resonant Paced Breathing Guide**: Built-in 6 breaths/minute visual coherence pacer designed to mechanically stimulate baroreflex gain and restore vagal parasympathetic tone.

---

## 👤 Lead Developer & Attribution
* **Lead Developer**: **Ms. Taniya Mondal, B.Tech**
* **System Version**: **1.0**
* **Clinical Standards Reference**: WHO Guidelines on Mental Health at Work (2022) & Task Force of ESC / NASPE (1996) HRV Standards.

---

## 🫀 Physiological Foundations & WHO Guidelines

The autonomic nervous system (ANS) dynamically regulates homeostatic cardiac function via two opposing branches:
- **Parasympathetic Branch (Vagus Nerve)**: Acts as an immediate cardio-inhibitory "brake" slowing sinoatrial firing. Reflected by high-frequency fluctuations:
  $$\text{RMSSD} = \sqrt{\frac{1}{N-1}\sum_{i=1}^{N-1} (RR_{i+1} - RR_i)^2}$$
  and High-Frequency (HF) spectral power ($0.15 - 0.40\text{ Hz}$).
- **Sympathetic Branch**: Accelerates chronotropic state during cognitive load, mental arithmetic, and emotional stress. Reflected in Low-Frequency (LF) power ($0.04 - 0.15\text{ Hz}$) and the **LF/HF Ratio** (Sympathovagal Balance).

### Clinical Normative Reference Framework
| Biomarker | Physiological Metric | Normative Optimal | Clinical Risk Threshold |
| :--- | :--- | :--- | :--- |
| **HR** | Chronotropic Heart Rate | $60 - 80\text{ bpm}$ | $> 100\text{ bpm}$ (Tachycardia) |
| **SDNN** | Overall Autonomic Flexibility | $> 50\text{ ms}$ | $< 20\text{ ms}$ (Autonomic Rigidity) |
| **RMSSD** | Vagal Parasympathetic Tone | $> 42\text{ ms}$ | $< 20\text{ ms}$ (Severe Vagal Withdrawal) |
| **LF/HF** | Sympathovagal Balance Ratio | $0.5 - 2.0$ | $> 3.5$ (Sympathetic Hyperarousal) |
| **NASA-TLX**| Cognitive Mental Workload | $< 40 / 100$ | $> 75 / 100$ (Critical Overload) |

---

## 🏗️ System Architecture

```
                                  [ Wearable / ECG Biotelemetry ]
                                                │
                                                ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   TWIN_CORE ENGINE                                     │
│                                                                                        │
│   ┌─────────────────────┐   ┌────────────────────────┐   ┌─────────────────────────┐   │
│   │   data_loader.py    │   │      models.py         │   │   who_standards.py      │   │
│   │  Ingestion, Typos   │──▶│  RandomForest/Ensemble │──▶│  Tiers I - IV, Indices  │   │
│   │  Artifact Cleansing │   │  GroupKFold Validation │   │  Evidence Prescriptions │   │
│   └─────────────────────┘   └────────────────────────┘   └─────────────────────────┘   │
│                                           │                                            │
│                                           ▼                                            │
│   ┌────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              explainability.py                                 │   │
│   │      SHAP TreeExplainer  •  Waterfall Breakdown  •  Clinical WHO Narrative     │   │
│   └────────────────────────────────────────────────────────────────────────────────┘   │
│                                           │                                            │
│                                           ▼                                            │
│   ┌────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               digital_twin.py                                  │   │
│   │    State Synchronization  •  What-If Sandbox  •  Counterfactual Interventions  │   │
│   └────────────────────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              FLASK WEB DASHBOARD & API                                 │
│    Vitals Monitor  •  SHAP Decomposition  •  What-If Sandbox  •  0.1 Hz Paced Pacer     │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Experimental Results & Validation

Validation conducted via **5-Fold GroupKFold Cross-Validation** (grouped strictly by participant ID to eliminate data leakage):

| Model Architecture | Cross-Validation MAE | RMSE | Explanatory Paradigm |
| :--- | :---: | :---: | :--- |
| **Random Forest (Primary Twin)** | **$15.99 \pm 3.69$** | **$19.97$** | **Exact SHAP TreeExplainer & Feature Interactions** |
| **Ridge Regression** | $15.71 \pm 2.23$ | $17.79$ | Linear Parametric Coefficients |
| **ElasticNet Regularization** | $15.20 \pm 3.43$ | $17.52$ | Sparse Penalized Attribution |
| **Gradient Boosting** | $17.09 \pm 3.08$ | $21.53$ | Gradient Tree Ensemble |

---

## 🚀 Quick Start Guide

### 1. Prerequisites
* Python 3.10+ (Tested up to Python 3.14 on Windows 11)
* Standard internet browser (Chrome, Edge, Firefox)

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/<your-username>/hrv-cognitive-digital-twin.git
cd hrv-cognitive-digital-twin
pip install -r requirements.txt
```

### 3. Model Training and Figure Generation
To re-evaluate models and generate all publication figures:
```bash
python train_and_evaluate.py
```

### 4. Launching the Web Dashboard
Double-click `run_dashboard.bat` (Windows) or execute:
```bash
python web_app/app.py
```
Open **`http://127.0.0.1:5000`** in your browser.

---

## 🌐 Step-by-Step Guide to Upload to GitHub

Follow these exact steps to push this complete project to GitHub:

### Step 1: Initialize Git Repository
Open PowerShell or Terminal in the project root:
```bash
git init
```

### Step 2: Configure Git User Info (If not already set)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Stage All Project Files
```bash
git add .
```

### Step 4: Commit with Version 1.0 Message
```bash
git commit -m "Initial Release: WHO-Style Explainable HRV Digital Twin v1.0 by Ms. Taniya Mondal, B.Tech"
```

### Step 5: Create a New Repository on GitHub
1. Navigate to [GitHub.com/new](https://github.com/new).
2. Set repository name: `hrv-cognitive-mental-load-digital-twin`.
3. Set visibility to **Public** or **Private**.
4. **Do not** check "Initialize with README" (since you already have one).
5. Click **Create repository**.

### Step 6: Link Remote & Push to Main Branch
```bash
git branch -M main
git remote add origin https://github.com/<your-username>/hrv-cognitive-mental-load-digital-twin.git
git push -u origin main
```

Your repository is now live with full documentation, source code, and trained models!

---

## 📜 Scientific References & Acknowledgments
1. **Auditya Sutarto (2020)**: *Heart Rate Variability and Cognitive Mental Workload Dataset*, Kaggle.
2. **World Health Organization (2022)**: *WHO Guidelines on Mental Health at Work*, World Health Organization, Geneva.
3. **WHO (2021)**: *Global Strategy on Digital Health 2020–2025*, World Health Organization.
4. **Task Force of ESC and NASPE (1996)**: *Heart rate variability: standards of measurement, physiological interpretation and clinical use*, Circulation, 93(5), 1043-1065.
5. **Lundberg, S. M., & Lee, S. I. (2017)**: *A unified approach to interpreting model predictions*, Advances in Neural Information Processing Systems (NeurIPS).

---
*Developed by **Ms. Taniya Mondal, B.Tech** &bull; Version 1.0 &bull; 2026*
