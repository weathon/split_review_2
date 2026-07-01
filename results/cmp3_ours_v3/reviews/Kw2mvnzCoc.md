## Summary

TSPulse proposes a 1M-parameter pre-trained time-series model with disentangled representations across temporal, spectral, and semantic embedding spaces. The architecture uses multi-output heads with separate reconstruction objectives, lightweight post-hoc fusers (MHT for AD, TSLens for classification), and a hybrid masking strategy. Evaluated on anomaly detection (TSB-AD), classification (UEA), imputation, and similarity search, TSPulse achieves strong results on AD and classification while being compact enough for CPU deployment.

## Strengths

1. **Well-motivated disentanglement framework with empirical validation (Sections 2, 6, Table 2).** The paper designs three explicit embedding views (temporal, spectral, semantic) trained via separate reconstruction objectives. The sensitivity analysis in Table 2 provides concrete evidence that the three embeddings respond differently to phase shifts, noise, and missing data, confirming that the objectives produce embeddings with distinct properties. The ablation study (Table 1b) further shows removing either short or long embeddings reduces classification accuracy by 8–10%.

2. **Extremely compact model with measured efficiency (1M parameters, CPU-deployable).** The paper achieves genuine practical value: a 1M-parameter model running at 0.387ms per inference on CPU (Figure 7), with latency comparisons showing 10–100× speed advantages over MOMENT and Chronos. The efficiency is measured and reported, not just claimed.

3. **Solid anomaly detection and classification results on established benchmarks (Sections 4.1–4.2).** On TSB-AD, TSPulse (ZS) achieves VUS-PR 0.48 (univariate) and 0.36 (multivariate), outperforming all pre-trained and non-pre-trained baselines including MOMENT. On 29 UEA datasets, TSPulse (FT) achieves mean accuracy 0.733 vs. 0.701 for VQShape — a genuine, if modest, improvement. These two task areas provide the paper's most defensible empirical support.

4. **Informative ablation studies isolating component contributions (Table 1).** The 79% imputation drop when hybrid pre-training is replaced with block masking, and the 11–16% drop when TSLens is replaced with pooling, give a clear picture of which innovations matter. The identity initialization for channel mixers (9% drop when removed) is a motivated design choice that the ablation confirms is effective.

## Weaknesses

### Fatal
None.

### Major

1. **Misleading imputation claims (Section 4.3, Figure 6, Abstract).** The paper claims "Compared to statistical interpolation methods, TSPulse shows 50%+ gains" (line 202) and the abstract states "+50% on imputation." However, the Interpol baseline — listed in the same table under "Zero-Shot (Prompt-Tuned/Statistical)" — achieves Mean MSE 0.039, which *ties* TSPulse (FT) at 0.039 and *handily beats* TSPulse (ZS) at 0.074. The IMP(%) column in Figure 6 leaves the Interpol row blank rather than reporting the negative improvement. The +50% claim is only valid when comparing against Naive (0.339) and Linear (0.161) while ignoring Interpol. This is a selective representation of the evidence. The paper must either explain why Interpol is an inappropriate comparison or honestly acknowledge that a simple interpolation method matches the fine-tuned model and outperforms the zero-shot model. The abstract claim needs revision.

2. **Task-specific pre-training undermines the "versatile" framing and confounds comparisons (Section 3.1).** Section 3.1 states: "we specialize the pre-training for every task through reweighting loss objectives to prioritize heads most relevant to the target task" (line 86). TSPulse is therefore a family of task-specialized pre-trained models, not a single model used across tasks. The baselines (MOMENT, UniTS, VQShape) are evaluated as single models across tasks without task-specific re-pre-training. This asymmetry means the comparison conflates architectural innovation with the pre-training strategy. The paper should acknowledge this limitation and ideally report results from a single un-reweighted pre-trained model to isolate the architecture's contribution.

### Minor

3. **"Zero-shot" anomaly detection uses labeled data for head selection (Section 4.1, Section 3.3).** The TSPulse (ZS) variant uses a labeled official tuning set for multi-head triangulation to select the best-performing head. Section 3.3 acknowledges: "when a small labeled validation set is available, it can be used to select the most effective head" (line 119). The fully unsupervised variant (Head_ensemble) is reported only in the ablation (Table 1a) at VUS-PR 0.44 vs. 0.48 for Head_triangulation, while the main results (Figure 4) only show the 0.48 score. Reporting both numbers side-by-side in the main results would make the effect of the labeled tuning set transparent.

4. **"Disentanglement" claim is weaker than standard usage (Section 6).** The paper uses "disentanglement" to mean different embedding *subsets* have different invariance properties (temporal embeddings are phase-sensitive, semantic embeddings are robust). This is distinct from the β-VAE notion where individual latent dimensions each capture a distinct generative factor. The paper's claim is still interesting and useful, but acknowledging this difference would calibrate reader expectations.

### Trivial
None.

## Nice-to-Haves
- **Statistical significance:** The paper reports point estimates only across 29 classification datasets and 40 AD datasets. Confidence intervals or significance tests would strengthen the claims, especially given the modest (5%) improvement over VQShape on classification.

## Removed Points
These points from the input review were removed with justification:

- **Similarity search evaluates a nonstandard proxy task.** REMOVED. The paper's Section 4.4 transparently describes the setup: queries are generated by augmenting indexed samples, and the paper states "This setup tests the embeddings' robustness in retrieving distorted similar patterns" (line 248). The comparison against MOMENT and Chronos under the same protocol is fair, and the framing matches the evaluation.

- **"Family match" vs. "fine-grained match" distinction defined in appendix.** REMOVED per policy (weakness about missing appendix content).

- **Single unified pre-training ablation.** REMOVED as subsumed by Weakness 2.

- **Formatting, style, and appendix-availability criticisms.** REMOVED per policy guidelines.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions

1. **Correct the imputation claims in the abstract and Section 4.3.** Report the Interpol comparison honestly, including the negative IMP(%) where applicable. Either explain why Interpol is not a fair comparator or reframe claims to reflect actual relative performance.

2. **Report results from a single, un-reweighted pre-trained model across all tasks** to separate the effect of architecture from task-specific pre-training, or clearly frame the contribution as "task-specialized pre-trained models" rather than "versatile."

3. **Present Head_ensemble (fully unsupervised) and Head_triangulation (tuning-set-informed) side-by-side** in the main AD results figure so readers can see the effect of the labeled tuning set transparently.

4. **Calibrate the "disentanglement" language** to distinguish embedding-subset-level specialization from per-dimension factor separation.

## Score and Decision

**Calibration anchors used (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| nSDOkm0SKo (Financial markets) | 1.00 | R1-bracket | Not comparable; trivial paper |
| 5lUdTogEL3 (Person ReID) | 1.00 | R1-bracket | Not comparable |
| xJ5CF1aOOX (Self-supervised TS PT) | 2.50 | R1-bracket | Weaker: limited novelty, narrow scope |
| xFvHcgj1fO (OML-AD) | 3.00 | R1-bracket | Weaker: online ML for AD, narrow |
| SZErAetdMu (TS Modeling at Scale) | 3.00 | R1-bracket | Weaker: lacks empirical strength |
| RuYl15smRv (AnomalyTCN) | 3.40 | R1-bracket | Weaker: narrower scope, efficiency focus only |
| KJ1w6MzVZw (Large Pre-trained TS) | 3.80 | R1-bracket | Weaker: limited novelty, domain overlap issues |
| W1wlE4bPqP (Uncertainty-aware TS FM) | 4.00 | R1-bracket | Comparable scope, less architectural novelty |
| ZkEsEFFUyo (Pushing Limits TS PT) | 4.33 | R1-bracket | CloudOps domain, different focus |
| LGafQ1g2D2 (Can LLMs Understand TS) | 5.20 | R1-bracket | Different methodology |
| **aKcd7ImG5e (DADA)** | **6.00** | **R1-bracket** | **Similar pre-training + AD approach; comparable scope, TSPulse has more tasks but also more issues** |
| 8TBGdH3t6a (Hybrid prototypes) | 5.60 | R1-bracket | MTS anomaly detection only, narrower |
| gRXLa6LS3J (FoMo-0D) | 5.75 | R1-bracket | Zero-shot OD, different task |
| eWocmTQn7H (MODEM) | 6.50 | R1-bracket | Diffusion for AD, different approach |
| **bWcnvZ3qMb (FITS)** | **8.00** | **R1-bracket** | **Ultra-compact TS model; cleaner claims, better scoped, stronger execution** |
| 2sCcTMWPc2 (TimelyGPT) | 5.50 | R2-narrow | TS PT model, rejected; less empirical support |
| tdttNKCtyB (ROSE) | 5.75 | R2-narrow | Register-assisted forecasting; similar register token idea, rejected |
| 39n570rxyO (OTiS) | 5.20 | R2-narrow | General TS model, rejected |
| iI7hZSczxE (DIOSC) | 5.67 | R2-narrow | TS disentanglement; accepted but limited scope (electricity) |
| yVGGtsOgc7 (Multi-task Disentangle) | 5.80 | R2-narrow | Disentanglement theory; accepted |
| aWkAKucZMR (ShuffleMTM) | 5.50 | R2-narrow | Masked TS modeling, rejected |
| WS7GuBDFa2 (Learn to Embed Patches) | 6.25 | R2-narrow | TS representation learning, accepted |
| dCcY2pyNIO (In-context TS Predictor) | 6.25 | R2-narrow | TS forecasting, accepted |

**Round 1 bracket:** 5.5–7.0. **Round 2 narrowing:** The paper is stronger than rejected papers in the 5.2–5.8 range (OTiS, ROSE, ShuffleMTM) due to its novel architecture and strong AD/classification results, but weaker than clean 8.0 papers like FITS. It is comparable to DADA (6.0) — both have solid contributions and fixable issues. The misleading imputation claims are a real concern but do not invalidate the core technical contribution.

**Final score: 6.0 — borderline accept.** The core contribution (disentangled multi-space representations in a 1M-parameter architecture) is novel, well-motivated, and convincingly validated on anomaly detection and classification. The compactness and CPU efficiency are practically valuable. However, the imputation claims are misleadingly reported (Interpol baseline is omitted from the advertised gains), and the "versatile" framing is inconsistent with task-specific pre-training. These issues are fixable with honest revision, and the paper's core strengths justify acceptance contingent on addressing them.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>