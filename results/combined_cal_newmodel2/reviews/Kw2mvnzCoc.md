## Summary

This paper introduces TSPulse, a family of ultra-lightweight pre-trained time-series models (1M parameters) that learn disentangled temporal, spectral, and semantic embeddings via multi-head masked reconstruction across representation spaces and abstraction levels. The model is evaluated on four diagnostic tasks (anomaly detection, classification, imputation, similarity search) across 75+ datasets and demonstrates strong zero-shot and fine-tuned performance with CPU-deployable efficiency.

## Strengths

- **The core idea — disentangled masked reconstruction across spaces (time vs. frequency) and abstraction levels (local vs. global) — is well-motivated and architecturally clean (Section 2).** The paper makes a concrete case that time-series signals live in multiple representation spaces and at different abstraction levels, and that lumping these into a single embedding hurts transferability. The solution — three complementary embedding views (temporal, spectral, semantic) learned via separate reconstruction heads acting on different segments of the decoder output — follows directly from this motivation.

- **The ablation studies are thorough and informative (Section 5, Table 1).** Each major design choice (disentanglement, hybrid masking, TSLens, identity weight initialization, dual-space learning) is ablated across multiple tasks, and the drops are mostly non-trivial (e.g., 79% imputation degradation without hybrid pre-training, 11–16% classification drop without TSLens). This gives confidence that the reported performance is not coming from one dominant factor.

- **The sensitivity analysis of embedding disentanglement (Section 6, Table 2) provides direct evidence for the claimed property.** Showing that temporal embeddings are highly sensitive to phase shifts (130% distortion), FFT embeddings are less so (21%), and semantic embeddings are the most robust across all perturbations (4.6–12%) is exactly the pattern one would expect from disentangled representations. This is compelling validation that the losses are doing what the paper claims.

- **The efficiency achievement is real and practically meaningful.** At 1M parameters with CPU inference measured in sub-millisecond times (0.387ms per sample for similarity search), this addresses a genuine deployment gap compared to models 10–100× larger.

## Weaknesses

### Fatal
None.

### Major

- **The imputation results contain a factual inaccuracy that misrepresents the comparison (Section 4.3, Figure 6).** The paper claims "Compared to statistical interpolation methods, TSPulse shows 50%+ gains" (line 202). However, the table shows **Interpol** (a statistical interpolation method listed under the Zero-Shot category) achieving Mean MSE of **0.039**, while TSPulse (ZS) achieves **0.074** — lower MSE is better, so TSPulse is roughly 2× worse than Interpol. The IMP(%) column for Interpol is left blank ("-"), consistent with TSPulse not being better. The 50%+ figure is computed only against Linear (MSE 0.161) and Naive (0.339), not against Interpol. The abstract's "+50% on imputation" is therefore an overstatement that does not hold against all statistical interpolation baselines. The paper must acknowledge this discrepancy and clarify which baselines the claimed gains refer to.

- **No measures of variance or statistical significance are reported anywhere in the paper.** Classification results are reported as point estimates (e.g., TSPulse FT: 0.733 mean accuracy across 29 datasets). Anomaly detection improvements over SubPCA are modest in absolute terms (0.48 vs 0.42, a 0.06 VUS-PR difference). Without standard deviations, confidence intervals, or statistical tests, it is impossible to assess whether the reported improvements are statistically reliable or within the range of noise. This weakens the evidence for modest-margin claims.

### Minor

- **The "zero-shot" framing is ambiguous.** Section 3.1 states that pre-training is specialized per task through reweighting loss objectives, meaning there are separate model variants for each diagnostic task. The standard meaning of "zero-shot" in the pre-training literature (e.g., MOMENT, GPT4TS evaluations) refers to a single pre-trained model generalizing across tasks. TSPulse does not do this — it is zero-shot across datasets *within a task*, not across tasks. The abstract and introduction imply a broader zero-shot capability than what was actually built. While the paper does disclose this design choice in Section 3.1, the framing could mislead readers.

- **The "disentanglement" terminology slightly overclaims the architectural mechanism.** The backbone (TSMixer) processes all tokens — time patches, FFT patches, and register tokens — together through the same mixer layers with full information mixing across all positions. The "disentanglement" is achieved by the loss heads operating on different portions of the decoder output, with no architectural mechanism (e.g., mutual information minimization, orthogonal projection) to prevent cross-talk in the shared backbone. The sensitivity analysis (Table 2) provides empirical support that the final embeddings behave as desired, so this does not invalidate the method. However, "multi-view representation learning via output-head specialization" would be a more precise description.

- **The "Interpol" baseline in the imputation experiment (Figure 6) is never defined or discussed in the text.** It achieves the best MSE among zero-shot methods (0.039, matching TSPulse FT) yet receives no explanation. Readers cannot assess whether Interpol is a valid comparison or whether it operates under different assumptions.

### Trivial
None.

## Nice-to-Haves

- The paper could benefit from standardizing its imputation evaluation to include the Interpol baseline in its reported improvement statistics, or at minimum explaining what Interpol is and why it performs so well.
- Clarify what "virtual channel expansion" refers to in the main text (currently only mentioned in the ablation).

## Removed Points

These points are flagged to be removed, treat them with caution:

- *"The evaluation configuration for imputation gives TSPulse an advantage (MOMENT pre-trained with block masking, TSPulse evaluated with hybrid masking)"* — REMOVED because the paper's own ablation (Table 1c, 79% drop without hybrid PT) transparently acknowledges this.
- *"No discussion of trade-off between task-specific pre-training and universality"* — REMOVED as scope creep. The paper explicitly adopts a task-specialized design and justifies it.
- *"Virtual channel expansion not defined in main text"* — REMOVED as a trivial presentation issue that could be addressed with one sentence.
- *"The claim that TSPulse outperforms models 10-100x larger is unsurprising if those models are general-purpose and TSPulse is task-specialized"* — REMOVED because this is speculative about reader expectations, not an error in the paper.
- *"Classification improvements of 5% over VQShape are modest"* — REMOVED because a 5% average improvement across 29 datasets is meaningful; the 5–16% range is accurately reported.
- Generic strengths from the input review ("this paper addressed an important problem") — REMOVED.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Acknowledge the Interpol discrepancy transparently and correct the imputation claim in the abstract to reflect fair comparisons.
2. Add variance estimates (standard deviations across datasets or random seeds) for classification and anomaly detection results.
3. Clarify the zero-shot framing — e.g., state in the abstract that "within each diagnostic task, the model generalizes to unseen datasets without fine-tuning."
4. Provide a brief definition of the Interpol baseline in the main text.
5. Consider softening the "disentanglement" terminology, or add a note clarifying that the separation is loss-driven rather than architecturally enforced in the backbone.

## Score and Decision

**Calibration Anchors.** All anchors retrieved across rounds, with avg human score:

| Path | Score | Round | Itemized? | Comparison |
|------|-------|-------|-----------|------------|
| FITS (bWcnvZ3qMb) | 8.00 | R1 | Yes | Ultra-lightweight TS model with clean execution. Stronger execution but narrower scope. TSPulse has broader evaluation but a factual inaccuracy. |
| TEMPO (YH5w12OUuU) | 6.33 | R1 | Yes | GPT-based TS forecasting. Similar weakness severity (missing benchmarks, marginal gains). |
| DADA (aKcd7ImG5e) | 6.00 | R1 | Yes | General TS anomaly detector. Comparable quality; TSPulse has higher-rated strengths but also concrete weaknesses. |
| ROSE (tdttNKCtyB) | 5.75 | R1 | Yes | Register-assisted TS forecasting. More complex, lower evaluation breadth than TSPulse. |
| Lightweight Pre-trained Transformers (Iip7rt9UL3) | 4.75 | R1 | Yes | Remote sensing focused. Smaller performance gains, narrower scope. |
| Large Pre-trained TS models (KJ1w6MzVZw) | 3.80 | R1 | Yes | Weak execution, missing baselines, poor notation. TSPulse is clearly stronger. |
| Zero-shot Imputation (NPSZ7V1CCY) | 6.25 | R2 | No | Zero-shot imputation for ODE systems. Comparable quality. |
| Conditional Info Bottleneck (K1mcPiDdOJ) | 6.50 | R2 | No | Imputation focused. Cleaner evaluation but narrower tasks. |
| Multi-Resolution Diffusion (eWocmTQn7H) | 6.50 | R2 | No | Anomaly detection. Similar evaluation quality. |
| TimeInf (Vz0CWFMPUe) | 5.80 | R2 | No | Data contribution method. Different task but similar evaluation rigor. |

**Round-1 bracket:** 5.5–7.5 (between ROSE at 5.75 and FITS at 8.0).

**Round-2 narrowing:** Compared against anchors at 5.75–6.50. TSPulse's strength favorability (13–16) is higher than all comparable anchors (TEMPO: 6.6–11.8, DADA: 4.8–12.5), indicating genuinely strong positive aspects. However, its two Major weaknesses — the factual inaccuracy in the imputation claim (favorability 2.66) and the complete absence of variance estimates (favorability -1.37) — are concrete and verified from the paper, keeping it from the 6.5+ range. The imputation issue is particularly salient because it is a verifiable factual error in the paper's own data table, not a methodological disagreement. The final score of **6.0** reflects a paper with a solid core contribution and high-rated strengths, but held back by presentation flaws that need correction before the claims can be fully trusted.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>