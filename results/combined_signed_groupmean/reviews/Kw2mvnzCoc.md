Now I have comprehensive calibration data. Let me write the final review.

## Summary

TSPulse proposes an ultra-light pre-trained time-series model (1M parameters) that learns three complementary embedding views (temporal, spectral, semantic) via disentangled masked reconstruction across spaces and abstraction levels. It evaluates on four diagnostic tasks — anomaly detection, classification, imputation, and similarity search — across 75+ datasets, reporting state-of-the-art zero-shot and fine-tuned results while being 10–100× smaller than comparably-performing models.

## Strengths

- **Well-motivated architecture with empirical evidence of functional specialization.** The paper correctly identifies a real limitation of existing pre-trained TS models (entangled temporal/spectral/semantic signals) and proposes a clean solution: training different embedding segments with complementary objectives. The sensitivity analysis in Table 2 provides the paper's strongest evidence — temporal embeddings show 130% distortion under phase shift vs. 12% for semantic embeddings — demonstrating genuinely differentiated behavior. This goes well beyond typical ablation studies.

- **Exceptional parameter efficiency.** At 1M parameters, TSPulse is genuinely tiny compared to baselines (MOMENT 40M, Chronos 46M, UniTS 340M). The efficiency data in Figure 7 (0.387ms CPU inference vs 5.51–46.71ms for baselines) is concrete and compelling, making a credible case for GPU-free deployment.

- **Clean ablation studies with large, unambiguous effects.** Table 1 isolates specific contributions: removing hybrid pre-training causes a 79% imputation MSE increase, removing TSLens causes 11–16% accuracy drops, removing dual-space learning causes 7–8% drops. These are decisive effects that confirm the claimed components are doing real work.

- **Broad evaluation across four tasks.** Anomaly detection (TSB-AD with 40 datasets), classification (29 UEA datasets), imputation (6 LTSF datasets × 4 mask ratios), and similarity search — evaluated in both zero-shot and fine-tuned settings — represents a genuine evaluation effort.

## Weaknesses

### Fatal

- **The imputation results contain a verifiable contradiction that undermines the headline "50%+ gains" claim.** The paper states (Section 4.3, line 202): "Compared to statistical interpolation methods, TSPulse shows 50%+ gains." However, Figure 6 shows the "Interpol" baseline achieving Mean MSE = **0.039** while TSPulse (ZS) achieves Mean MSE = **0.074** — nearly double (worse). The IMP(%) column for Interpol is blank ("—"), which is consistent with TSPulse being worse than this baseline. The Fine-Tuned section then shows TSPulse (FT) achieving 0.039 — matching the Interpol baseline exactly. As presented, this directly contradicts the paper's central claim of "+50% gains in zero-shot imputation" (Abstract and Contributions). This issue requires author clarification to resolve.

### Major

- **No statistical significance or variance reporting anywhere in the paper.** Every result table reports a single number (mean accuracy, mean MSE, VUS-PR) with no standard deviation, confidence intervals, or indication of how many runs were performed. The classification improvement over VQShape (0.733 vs 0.701, a 0.032 difference) and the anomaly detection advantage over SubPCA (0.48 vs 0.42, a 0.06 difference) could plausibly be within measurement noise on high-variance benchmarks like UEA and TSB-AD. Without variance information, the reliability of the claimed margins cannot be evaluated.

### Minor

- **The "zero-shot" anomaly detection claim is overstated.** The paper discloses (Section 4.1, line 166) that TSPulse-ZS uses a "small labeled official tuning-set" for multi-head triangulation to select the best-performing head. This is transparent in the body, but the abstract and contributions frame "zero-shot" as a headline capability without this qualification. Readers encountering "zero-shot" in the abstract will reasonably assume no target-data labels are used. The contribution remains meaningful with this caveat, but the framing is misleading.

- **The term "disentanglement" is used non-standardly.** The paper uses "disentanglement" to describe functional specialization of different embedding segments via different training objectives. This differs from the conventional usage in representation learning (e.g., β-VAE with independent factors of variation and metrics like MIG/DCI/SAP). The sensitivity analysis (Table 2) shows differentiated responses to perturbations, which is evidence of specialization but not necessarily disentanglement in the established sense. Using "functional specialization" or "multi-view representation learning" would be more accurate and avoid overclaiming.

### Trivial

None.

## Nice-to-Haves

- Training curves or gradient norm comparisons during fine-tuning would strengthen the claim about identity-initialized channel mixers improving training stability.
- The IMP(%) column in Figure 4 has inconsistencies (e.g., some values don't match simple arithmetic from the reported numbers). This is presentation-level but should be corrected.

## Removed Points

These points are flagged to be removed, treat them with caution:
- Concern about selective baseline reporting in AD (only top 3 SOTA models shown in main text): The paper explicitly acknowledges this and defers full results to Appendix A.11. Deferring to the appendix is standard practice for a leaderboard with 40 methods.
- Request for comparison against more lightweight models: The paper already compares against the smallest available variants of MOMENT and Chronos, and against standard data-specific baselines.
- Suggestion about the similarity search using custom datasets: The paper describes the setup (synthetic + UCR-based data) and defers full details to the appendix. This is acceptable for a diagnostic evaluation.

## Novel Insights

The most novel observation from combining the review content is that the sensitivity analysis (Table 2) — showing dramatically different robustness profiles across embedding types (130% distortion for temporal under phase shift vs. 21% for FFT vs. 12% for semantic) — constitutes the paper's strongest and most original evidence. The magnitude of these differences is striking and provides a concrete, testable signature of genuine functional specialization that goes well beyond typical ablation or attention-visualization studies. This deserves more emphasis as the paper's most distinctive empirical finding, independent of the benchmark results.

## Suggestions

1. **Resolve the imputation contradiction** by clarifying what "Interpol" is, explaining why its MSE is 0.039 while TSPulse (ZS) is 0.074, and either retracting or re-scoping the "50%+ gains over statistical methods" claim.
2. **Add variance information** (standard deviations or confidence intervals) to all main results, or at minimum state the number of runs and whether results are consistent across seeds.
3. **Qualify "zero-shot"** in the abstract by noting that the anomaly detection variant uses a small labeled tuning set for head selection.
4. **Reconsider the "disentanglement" terminology** — either adopt "functional specialization" or "multi-view representation learning," or formally define what disentanglement means in this context and provide appropriate metrics.

## Score and Decision

### Calibration Analysis

**Round 1 bracket:** 3.0 – 4.5

**Anchors retrieved:**
| Path | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| FITS (bWcnvZ3qMb) | 8.00 | R1 | Yes | Very clean paper, simple method, no fatal issues. TSPulse has more novelty but a factual contradiction. TSPulse below. |
| DADA (aKcd7ImG5e) | 6.00 | R1 | Yes | Had contribution exaggeration concerns (-9.98, -10.00) but no factual errors in results. TSPulse below because its weakness is a verifiable data contradiction. |
| ROSE (tdttNKCtyB) | 5.75 | R2 | Yes | Well-executed pre-trained forecasting model, minor weaknesses. TSPulse is more ambitious but has a fatal contradiction. TSPulse below. |
| NuwaTS (jC6E2iTgfr) | 4.00 | R1 | Yes | Marginal improvements, design concerns. TSPulse's other three tasks are stronger, but the fatal contradiction places it at a similar level. |
| Large PT TS (KJ1w6MzVZw) | 3.80 | R2 | Yes | Missing baselines, poor notation, ill-defined experiments. TSPulse has better presentation/evaluation but a fatal contradiction. |

**Itemized impact comparison:** TSPulse shares high-magnitude strengths with FITS (architecture motivation +10.00, ablations +9.56, parameter efficiency +9.64) but unlike FITS (whose max weakness was -7.53), TSPulse carries two near-decisive negative items: the imputation contradiction (-10.00) and the lack of variance (-9.99). The contradiction is a verifiable factual issue (the paper's own table contradicts its claim), which is more severe than the opinion-based "exaggerated contribution" complaints that pulled DADA to 6.00. This places TSPulse below DADA (6.00) and below ROSE (5.75), in the 3.0–4.0 range where papers with clear evidential flaws reside.

The paper has genuine contributions — the architectural design is sound, the sensitivity analysis is compelling, and the parameter efficiency is remarkable. However, the imputation contradiction is a factual error in the paper itself that invalidates one of four headline claims, and the absence of variance reporting weakens confidence in the remaining three. These are resolvable issues, but as presented the evidence does not support the paper's strongest claims.

**Final score: 3.5** — between "reject" (3) and "borderline reject" (4). The paper would benefit from clarification of the imputation results, addition of variance information, and toning down of overclaims.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>