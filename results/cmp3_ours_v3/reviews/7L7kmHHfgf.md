Now let me write the final consolidated review.

## Summary

PIRN proposes a prototype-driven reconstruction framework for few-shot multimodal anomaly detection (MAD). The method combines three components: Balanced Prototype Assignment (BPA) via optimal transport to prevent codebook collapse, Adaptive Prototype Refinement (APR) to update prototypes at inference to bridge the train-test gap, and Multimodal Normality Communication (MNC) for cross-modal knowledge transfer. Experiments on MVTec-3D-AD, Eyecandies, and Real-IAD show consistent gains under few-shot settings, and the method achieves strong computational efficiency (85% FLOP reduction vs. FIND while matching accuracy).

## Strengths

- **Well-motivated problem with clear diagnosis of prior failures.** Section 1 precisely identifies why cross-modal alignment and memory-bank methods degrade in few-shot settings — alignment overfits sparse correspondences and memory banks lack coverage of normal variation — motivating the prototype-based reconstruction direction naturally and specifically.

- **Clean modular design where each component targets a distinct failure mode.** BPA (balanced OT) addresses codebook collapse, APR bridges the train-test distribution gap via gated GRU updates during inference, and MNC enables cross-modal collaboration. The architecture diagram (Fig. 2) makes the data flow clear, and the use of balanced optimal transport for both assignment and context extraction is technically coherent.

- **Consistent empirical gains under few-shot settings (Table 1).** On MVTec-3D-AD, PIRN improves AUROC_I over the next-best Table-1 baseline (INP-Former) by +3.9 at 5-shot, +3.7 at 10-shot, and +2.4 at 50-shot. Similar consistent gains hold on Eyecandies across all three metrics.

- **Strong computational efficiency (Table 4).** At 103.36G FLOPs and 17.49ms latency, PIRN is far more efficient than FIND (728.46G, 76.09ms) while matching its accuracy — an 85% FLOP reduction and 4.35× speedup. This is a genuine practical advantage for deployment.

- **Informative diagnostic analysis (Figure 4).** The OT-movement visualization directly shows that BPA routing induces larger feature displacement for anomalous patch tokens than normal ones, supporting the claimed mechanism of prototype-based normal/anomalous discrimination.

## Weaknesses

### Major

- **FIND baseline is absent from the main few-shot comparison (Table 1).** FIND is cited as "the recent SOTA" (line 278) and achieves 0.921 AUROC_I on the 10-shot MVTec-3D-AD setting (Table 4) — only 0.001 below PIRN's 0.922. Yet FIND does not appear in Table 1, the primary table where PIRN's few-shot superiority is established. The text reports gains of "+3.7 points" over INP-Former at 10-shot, but the actual gap to the closest competitor (FIND) is +0.1 points — a very different story. The authors should either add FIND to Table 1 for all shot settings, or clearly explain any methodological reason preventing its inclusion. This omission directly affects the headline claim of "consistently superior performance" and must be addressed.

### Minor

- **Loss function specification is imprecise.** The training objective is described as "an intra-modal feature reconstruction loss, e.g., a soft mining loss (Luo et al., 2025)" (line 144), followed by "In practice, we minimize the cosine distance" between encoder and reconstructed embeddings. The "e.g." framing is inappropriate for a primary training loss — the paper should state exactly what loss is being optimized, with a formula, whether modality losses are summed or weighted, and whether any regularization terms apply to the OT plans or gating parameters.

- **APR's core assumption is asserted but not directly validated.** The paper claims (lines 106–110) that balanced OT assigns anomalous patches diffusely across prototypes, causing them to contribute weakly to prototype updates. However, no experiment directly tests this. Figure 4 shows that anomalous tokens undergo larger displacement after reconstruction — but this is a consequence of prototypes being normal, not evidence that OT assignment itself suppresses anomalous contributions during the refinement step. A controlled experiment comparing APR's prototype updates when fed all patches vs. only known-normal patches would substantiate this claim.

- **No estimates of statistical variability.** No standard deviations or confidence intervals are reported for any result in Tables 1–8. With few-shot sampling, results can vary substantially depending on which specific samples are drawn. Reporting mean and std over multiple few-shot trials (e.g., 3–5 random draws of the shot subsets) is standard practice for few-shot benchmarks, and its absence makes it difficult to assess robustness to sampling variation.

- **Naming inconsistency: "CFM" in text vs. "CTM" in tables.** The method attributed to Costanzino et al. (2024) is called "CFM" in the introduction and related work (lines 13, 64) but appears as "CTM" in Table 1 (rows 160, 168, 176, 184). These appear to reference the same paper but use different abbreviations, which is confusing.

- **Undefined metric Fmax_95 in Table 3.** This metric appears alongside AUROC_I, AUROC_P, and AUPRO but is not defined in the evaluation protocol section, which only lists the three standard metrics.

- **"Less than 1%" claim in Figure 1 not directly verifiable.** The caption states PIRN achieves superior performance "using less than 1% of the training data," but the x-axis is labeled "Available Training Samples / All Samples (0% to 100%)" and the 1% threshold is not marked or directly readable from the plot. This should be stated precisely: which shot setting corresponds to "less than 1%" on which dataset.

### Trivial

None.

## Nice-to-Haves

- The paper attributes degradation at K=50 and K=100 prototypes solely to a weakened information bottleneck. An alternative (not mutually exclusive) explanation is that the balanced OT constraint forces mass onto irrelevant prototypes when certain normal patterns are absent from a test image. Discussing this would enrich the analysis.

- The gating scalars γ_rgb and γ_sn are learned at training time and fixed during inference (line 130). Optimal gating may depend on whether the current test sample contains anomalies. Discussing this as a limitation would be valuable.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Ablation table (Table 2) is "uninterpretable" due to formatting.** The reviewer noted that all rows show identical checkmarks and row 4 shows 0.967 exceeding the full model's 0.922. This is a PDF parser artifact — the checkmark symbols and column alignment are mangled by extraction (every row shows identical ✓ symbols, which cannot be the original rendering). The text confirms the ablation follows expected patterns ("Removing each component...results in a consistent performance drop"). Per policy, formatting/parser artifacts are not author errors.

- **Criticism about balanced OT forcing mass to irrelevant prototypes.** This was presented as an alternative explanation the paper should have considered. It is a valid observation but belongs as a nice-to-have suggestion, not a core weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add FIND to Table 1** (or justify its exclusion) to provide an honest picture of the closest competitor. The current framing gains credibility from full transparency.
2. **Specify the exact loss function** with a formula, including any weighting or regularization terms.
3. **Run a controlled experiment for APR:** compare prototype updates using (a) the proposed OT-weighted context from all patches vs. (b) context from only ground-truth normal patches. If similar, the claim is supported; if not, discuss the failure mode.
4. **Report standard deviations** over multiple few-shot draws (3–5 random seeds).
5. **Fix the CFM/CTM naming inconsistency** and define Fmax_95.
6. **Clarify the "less than 1%" claim** by stating the exact shot setting on each dataset.

## Score and Decision

### Calibration Anchors

| Path | Avg Score | Round | Comparison to PIRN |
|---|---|---|---|
| `gTsLBDMZrL.md` — Prototype-oriented Fast Refinement for Few-shot IAD | 5.50 (Reject) | R2 | Topically similar (few-shot AD, OT for prototypes) but PIRN has a cleaner full-framework design, better writing, and more comprehensive experiments. The missing-baseline issue (GraphCore) is analogous to PIRN's missing FIND. |
| `Zzs3JwknAY.md` — One-for-All Few-Shot Anomaly Detection via Prompt Learning | 6.40 (Accept) | R2 | Both address few-shot AD, both have missing-baseline/comparison issues, both accepted with revision. PIRN has cleaner ablation but less extensive related work integration. |
| `8TBGdH3t6a.md` — Learn Hybrid Prototypes for MTSAD | 5.60 (Accept) | R2 | Prototype-based reconstruction AD, similar methodological theme. PIRN has stronger empirical story but more significant reporting gap. |
| `J2we1sVd9m.md` — Prototype-based OT for OOD Detection | 4.60 (Reject) | R3 | Uses OT + prototypes for distribution-shift detection. While conceptually related, PIRN's technical execution and experiments are substantially stronger. |

**Round 1 bracket:** I formed an initial bracket of [5.5, 6.5] after reading the paper and the harsh critic's review.

**Round 2 narrowing:** After reading the full reviews of the 5.5 anchor (gTsLBDMZrL — accepted-adjacent but rejected prototype+OT few-shot AD paper) and the 6.4 anchor (Zzs3JwknAY — accepted few-shot AD paper with similar missing-baseline issues), I narrowed to [5.5, 6.0]. PIRN is clearly stronger than the rejected 5.5 paper (full framework vs. plugin, better writing, more experiments) but has the significant FIND omission that tempers enthusiasm relative to a clean accept.

**Final score:** 5.5. This paper demonstrates a technically coherent framework with genuine empirical and efficiency advantages. The FIND omission is its most serious weakness — fixable, but it obscures the true competitive landscape and softens the headline claims. The paper's core technical contribution is solid, and addressing the FIND issue along with the minor concerns would make it accept-ready.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>