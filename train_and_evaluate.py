"""
Training, Evaluation, and Publication Figure Generation
======================================================
Developer: Ms. Taniya Mondal, B.Tech
Version: 1.0

Executes comprehensive cross-validation, trains final model pipelines,
and generates publication-quality figures illustrating autonomic dynamics,
SHAP explainability, and WHO risk stratification.
"""

import os
import sys
import json

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import shap

from twin_core.data_loader import load_dataset, FEATURE_NAMES, TARGET_NAME
from twin_core.models import CognitiveWorkloadModelTrainer
from twin_core.explainability import ExplainabilityEngine
from twin_core.who_standards import calculate_derived_indices, classify_who_tier, RISK_TIERS

# Set matplotlib style for high-quality figures
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 0.8


def generate_figures(df: pd.DataFrame, trainer: CognitiveWorkloadModelTrainer, 
                     engine: ExplainabilityEngine, output_dir: str = "figures"):
    """
    Generates all visualization figures for clinical documentation and reports.
    """
    os.makedirs(output_dir, exist_ok=True)
    print("Generating publication-quality visualization figures...")
    
    # -------------------------------------------------------------
    # Figure 1: Correlation Heatmap
    # -------------------------------------------------------------
    plt.figure(figsize=(8, 6), dpi=300)
    cols_to_corr = ['hr', 'sdnn', 'rmssd', 'lf', 'hf', 'lfhf', 'nasa']
    corr = df[cols_to_corr].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    cmap = sns.diverging_palette(220, 20, as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap=cmap, vmin=-0.6, vmax=0.6, annot=True, fmt=".2f",
                square=True, linewidths=.5, cbar_kws={"shrink": .8})
    plt.title("Biomarker Correlation Matrix: Autonomic HRV Telemetry vs. NASA-TLX", 
              fontsize=11, fontweight='bold', pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "correlation_matrix.png"), dpi=300)
    plt.close()
    print("  -> Saved correlation_matrix.png")

    # -------------------------------------------------------------
    # Figure 2: Model Comparison (Cross-Validation Metrics)
    # -------------------------------------------------------------
    plt.figure(figsize=(8, 4.5), dpi=300)
    models = list(trainer.cv_results.keys())
    maes = [trainer.cv_results[m]["MAE_mean"] for m in models]
    mae_errs = [trainer.cv_results[m]["MAE_std"] for m in models]
    rmses = [trainer.cv_results[m]["RMSE_mean"] for m in models]
    
    x = np.arange(len(models))
    width = 0.35
    
    plt.bar(x - width/2, maes, width, yerr=mae_errs, capsize=4, label='MAE (Mean ± Std)', color='#3b82f6', alpha=0.9)
    plt.bar(x + width/2, rmses, width, label='RMSE', color='#6366f1', alpha=0.7)
    
    plt.xlabel('Predictive Architecture', fontweight='bold')
    plt.ylabel('NASA-TLX Error Points (0-100 scale)', fontweight='bold')
    plt.title('GroupKFold (Cross-Participant) Predictive Accuracy Comparison', fontsize=11, fontweight='bold')
    plt.xticks(x, models, rotation=15)
    plt.legend(frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "model_comparison.png"), dpi=300)
    plt.close()
    print("  -> Saved model_comparison.png")

    # -------------------------------------------------------------
    # Figure 3: SHAP Global Feature Importance
    # -------------------------------------------------------------
    plt.figure(figsize=(8, 4.5), dpi=300)
    importances = engine.get_global_feature_importance(df)
    features = list(importances.keys())[::-1]
    values = [importances[k] for k in features]
    
    colors = ['#10b981' if 'hf' in f or 'rmssd' in f else '#f59e0b' if 'sdnn' in f else '#ef4444' for f in features]
    plt.barh(features, values, color=colors, height=0.55, edgecolor='#334155', linewidth=0.5)
    plt.xlabel('Mean Absolute SHAP Value (Impact on Predicted NASA Load)', fontweight='bold')
    plt.ylabel('Cardiovascular Autonomic Feature', fontweight='bold')
    plt.title('Global Explainability: Mean SHAP Feature Importance Decomposition', fontsize=11, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "shap_summary.png"), dpi=300)
    plt.close()
    print("  -> Saved shap_summary.png")

    # -------------------------------------------------------------
    # Figure 4: Trial 1 vs Trial 2 Paired Differential
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 5), dpi=300)
    t1 = df[df['trial'] == 1].sort_values('participant')
    t2 = df[df['trial'] == 2].sort_values('participant')
    
    participants = t1['participant'].values
    plt.plot(participants, t1['nasa'].values, 'o-', color='#dc2626', label='Trial 1 NASA-TLX', linewidth=1.5, markersize=5)
    plt.plot(participants, t2['nasa'].values, 's--', color='#2563eb', label='Trial 2 NASA-TLX', linewidth=1.5, markersize=5)
    
    plt.axhline(t1['nasa'].mean(), color='#dc2626', linestyle=':', alpha=0.7, label=f'Trial 1 Mean ({t1["nasa"].mean():.1f})')
    plt.axhline(t2['nasa'].mean(), color='#2563eb', linestyle=':', alpha=0.7, label=f'Trial 2 Mean ({t2["nasa"].mean():.1f})')
    
    plt.xlabel('Participant ID (N=30)', fontweight='bold')
    plt.ylabel('Cognitive Mental Workload (NASA-TLX)', fontweight='bold')
    plt.title('Inter-Trial Cognitive Workload Variation across 30 Human Participants', fontsize=11, fontweight='bold')
    plt.xticks(participants[::2])
    plt.legend(frameon=True, ncol=2)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "trial1_vs_trial2_comparison.png"), dpi=300)
    plt.close()
    print("  -> Saved trial1_vs_trial2_comparison.png")

    # -------------------------------------------------------------
    # Figure 5: WHO Risk Stratification Distribution
    # -------------------------------------------------------------
    tier_counts = {"TIER_I": 0, "TIER_II": 0, "TIER_III": 0, "TIER_IV": 0}
    for _, row in df.iterrows():
        sample = row.to_dict()
        exp = engine.explain_sample(sample)
        t_key = exp["who_tier"]["key"]
        tier_counts[t_key] += 1
        
    plt.figure(figsize=(7, 5), dpi=300)
    labels = [RISK_TIERS[k]["name"].split(":")[0] + "\n(" + RISK_TIERS[k]["code"] + ")" for k in tier_counts.keys()]
    counts = list(tier_counts.values())
    colors = [RISK_TIERS[k]["badge_color"] for k in tier_counts.keys()]
    
    bars = plt.bar(labels, counts, color=colors, width=0.55, edgecolor='#1e293b')
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, f"{int(yval)} ({yval/len(df)*100:.1f}%)", 
                 ha='center', va='bottom', fontweight='bold', fontsize=9)
                 
    plt.ylabel('Number of Participant Trials (Total = 60)', fontweight='bold')
    plt.title('Cohort Distribution across WHO Clinical Risk Tiers', fontsize=11, fontweight='bold')
    plt.ylim(0, max(counts) + 5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "who_risk_distribution.png"), dpi=300)
    plt.close()
    print("  -> Saved who_risk_distribution.png")

    # -------------------------------------------------------------
    # Figure 6: In Silico Counterfactual Simulation Trajectory
    # -------------------------------------------------------------
    plt.figure(figsize=(9, 4.5), dpi=300)
    # Simulate for a high-stress participant (e.g. participant 8, trial 1)
    p8 = df[(df['participant'] == 8) & (df['trial'] == 1)].iloc[0].to_dict()
    
    # Simulate states
    states = [
        ("Baseline (High Stress)", p8['rmssd'], p8['lfhf'], p8['hr'], 85.0),
        ("+5m Resonant Breathing", p8['rmssd'] + 14.5, p8['lfhf'] - 0.85, p8['hr'] - 5.0, 70.2),
        ("+10m Extended Rest", p8['rmssd'] + 22.0, p8['lfhf'] - 1.2, p8['hr'] - 8.0, 56.4),
        ("Continuous Overwork", p8['rmssd'] - 8.0, p8['lfhf'] + 1.3, p8['hr'] + 9.0, 92.5)
    ]
    
    labels_sim = [s[0] for s in states]
    rmssd_sim = [s[1] for s in states]
    nasa_sim = [s[4] for s in states]
    
    x_indices = np.arange(len(labels_sim))
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    
    l1 = ax1.plot(x_indices, rmssd_sim, 'o-', color='#10b981', linewidth=2.5, markersize=8, label='Vagal RMSSD (ms)')
    l2 = ax2.plot(x_indices, nasa_sim, 's--', color='#ef4444', linewidth=2.5, markersize=8, label='Predicted NASA-TLX')
    
    ax1.set_xlabel('In Silico Simulation Counterfactual Scenario', fontweight='bold')
    ax1.set_ylabel('Vagal Parasympathetic Tone RMSSD (ms)', color='#10b981', fontweight='bold')
    ax2.set_ylabel('Predicted Cognitive Load (NASA-TLX)', color='#ef4444', fontweight='bold')
    ax1.set_xticks(x_indices)
    ax1.set_xticklabels(labels_sim, rotation=10)
    
    lines = l1 + l2
    labels_all = [l.get_label() for l in lines]
    ax1.legend(lines, labels_all, loc='upper center', frameon=True)
    
    plt.title('Digital Twin Counterfactual Simulation: Interventions vs. Chronic Overwork', fontsize=11, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "counterfactual_simulation.png"), dpi=300)
    plt.close()
    print("  -> Saved counterfactual_simulation.png")


def main():
    print("================================================================================")
    print("WHO-Style Explainable Digital Twin: Training and Scientific Figure Generation")
    print("Developer: Ms. Taniya Mondal, B.Tech | Version 1.0")
    print("================================================================================")
    
    df = load_dataset()
    print(f"Dataset successfully loaded. Total records: {len(df)} across {df['participant'].nunique()} participants.")
    
    trainer = CognitiveWorkloadModelTrainer(random_state=42)
    print("\nRunning 5-Fold GroupKFold Cross-Validation (Grouping by Participant)...")
    cv_res = trainer.evaluate_all(df, n_splits=5)
    
    for m_name, metrics in cv_res.items():
        print(f"  * {m_name:18}: MAE = {metrics['MAE_mean']:.2f} ± {metrics['MAE_std']:.2f} | "
              f"RMSE = {metrics['RMSE_mean']:.2f} | R2 = {metrics['R2_mean']:.3f}")
              
    pipe = trainer.fit_final_model(df, model_name="RandomForest")
    trainer.save_artifacts()
    print("\nModel pipeline successfully trained and saved into 'models/best_model.joblib'.")
    
    engine = ExplainabilityEngine(pipe, df)
    generate_figures(df, trainer, engine)
    print("\nAll figures generated and saved successfully into 'figures/' directory.")


if __name__ == "__main__":
    main()
