Now I have enough data to finalize my review. Let me compile it.

## Summary
This paper proposes STBP, a continual spatio-temporal forecasting (CSTF) framework that combines a frequency-domain backbone (FreNet) with linear graph attention (DLGA) and an incrementally expandable contextual pattern bank. The backbone extracts stable temporal representations and captures dynamic spatial correlations, while the pattern bank (per-node trainable parameters) adapts incrementally via parameter expansion and prompt-based gating. Experiments on three streaming datasets report 21% MAE reductions over the best baseline on two traffic datasets, with strong few-shot performance.

## Strengths
- **Well-designed ablation isolating each component's contribution**: Figure 4 systematically tests five variants (Retrain, Online, w/o Backbone, w/o DLGA, EAC). Crucially, the "w/o Backbone" variant (pattern bank + CNN/GCN backbone, as used by baselines) achieves ~24 MAE on PEMS-Stream vs. EAC's ~26 MAE, directly demonstrating that the pattern bank design is superior to EAC's dynamic prompt pool as a continual learning mechanism—on the *same* weak backbone. The ablation also shows FreNet and DLGA each contribute independently.
- **Strong few-shot robustness under data scarcity**: Table 2 shows STBP achieves 13.58 vs EAC's 16.13 MAE on PEMS-Stream (10% data setting), a 15.8% improvement that is *larger* than the full-data gap (21.44% vs 15.8% is not a typo—under few-shot the relative gain is preserved or improved). This supports the claim that the frozen-backbone-plus-pattern-bank design transfers effectively to low-resource scenarios.
- **Computational efficiency with strong accuracy**: Figure 8 shows STBP achieves the best MAE with training cost only marginally higher than EAC. The linear attention variant (O(N)) reduces GPU memory growth vs. full attention O(N²) as confirmed on the toy dataset (Figure 8 right panel).
- **Clean architectural design with empirical validation**: The separation between a frozen backbone (preserving general knowledge) and expanding pattern bank (adapting to new distributions) is a principled design. Figures 3 and 6 show the pattern bank autonomously forms meaningful clusters where nodes within clusters share similar temporal dynamics, and new nodes from later periods are correctly assigned to existing clusters.

## Weaknesses

### Fatal
None

### Major
- **Backbone and continual learning contributions are confounded**: The FreNet+DLGA backbone is architecturally superior to the CNN+GCN backbones used by all CSTF baselines. From Figure 4's approximate values on PEMS-Stream: "Retrain" (FreNet+DLGA backbone, no pattern bank, retrained from scratch each period) achieves ~20 MAE, "w/o Backbone" (pattern bank + CNN/GCN) achieves ~24 MAE, and "Our" achieves ~15 MAE. The ~4 MAE gap from Retrain to w/o Backbone is attributable to backbone quality; the ~5 MAE gap from Retrain to Our is the pattern bank contribution. Yet the headline claim frames the entire ~11 MAE improvement over EAC (~26) as a unified contribution. The critical missing experiment—running EAC (and ideally other CSTF methods) on the FreNet+DLGA backbone—is absent. This single experiment would cleanly separate the two contributions. Without it, the reader cannot determine whether the pattern bank is a better continual learning mechanism than EAC's prompt pool, or whether most of the gain comes from the backbone. The "w/o Backbone" ablation tests the complementary direction (pattern bank on weak backbone), which provides one direction of evidence but not the reverse. **Why it matters**: This is the central experimental gap that weakens the paper's ability to claim STBP's continual learning mechanism is superior to prior CSTF methods.

- **Near-zero improvement on AIR-Stream with some metrics worse than baselines**: STBP's average MAE improvement over EAC on AIR-Stream is only 2.35% (23.64 vs 24.21, Table 1), and at horizon 6, STBP's RMSE (39.81) is actually slightly *worse* than EAC's (39.63). The paper does not discuss this cross-domain disparity. If the pattern bank is the main driver, this near-zero improvement on non-traffic data raises questions about its robustness outside traffic data. **Why it matters**: The 21% headline gains are on traffic data only; the only non-traffic result is near-baseline, undermining the generalizability claim.

### Minor
- **Limited dataset diversity**: All three datasets come from two domains (US highway traffic and Chinese air quality). Both traffic datasets are from California highway systems and likely share distributional characteristics. Even one additional dataset from a different domain (e.g., energy, weather) would strengthen the generalizability claim.
- **Privacy protection and storage efficiency claims unsupported**: Section 4.2 claims the pattern bank offers "advantages in privacy protection and storage efficiency" because it encodes "high-level abstractions rather than raw historical data." No privacy analysis (e.g., membership inference attacks) or storage comparison with replay-based methods is provided.
- **No total parameter count comparison**: The pattern bank grows as N_τ × 3d (three groups of parameters). For CA-Stream with thousands of nodes and d up to 256, this could be substantial. A parameter count comparison would contextualize the "scalable" claim.
- **Why pattern bank clusters emerge is unexplained**: The t-SNE visualization (Figures 3, 6) shows meaningful clusters forming, but the paper asserts this as a design property ("the contextual pattern bank autonomously distinguishes heterogeneous and relevant nodes," Section 4.2) without explaining the mechanism. Analysis of what drives clustering (gradient dynamics, gating mechanism properties) would strengthen the contribution.

### Trivial
None

## Nice-to-Haves
- Run EAC/STRAP on the FreNet+DLGA backbone to cleanly isolate the pattern bank's continual learning contribution—this is the single highest-priority improvement.
- Provide per-dataset analysis explaining why gains are 21% on traffic but only 2.35% on air quality.
- Show forecasting visualizations for more systematic node samples rather than cherry-picked individual nodes (Figure 7).

## Removed Points
These points are flagged to be removed, treat them with caution:
- None removed—both reviewers' main points were verified against the paper and found to be substantively valid.

## Novel Insights
The most novel insight from synthesizing the reviews is the decomposition of the paper's ~21% improvement over EAC into separable backbone and pattern bank contributions. The ablation data (Figure 4) reveals that roughly 40% of the gain on PEMS-Stream comes from the superior backbone alone (Retrain ~20 vs EAC ~26), while the pattern bank adds a further ~25% on top (Retrain ~20 → Our ~15). This decomposition is important because the paper frames all ~21% improvement as a unified contribution, when the headline numbers conflate two separable improvements. However, the pattern bank does appear to provide genuine continual learning value: it outperforms EAC's prompt mechanism even when both use the same weak backbone (~24 vs ~26 from w/o Backbone ablation), and the few-shot gap is preserved or enlarged.

## Suggestions
- Run EAC on the FreNet+DLGA backbone and report results. This single experiment would validate or deflate the pattern bank's contribution and is straightforward to execute.
- Add analysis of why AIR-Stream performance gaps are much smaller than traffic datasets.
- Soften or remove the privacy claim unless evidence (e.g., membership inference experiments) is provided.
- Include total parameter counts for STBP vs. baselines.

## Calibration Report

**Round 1 — Bracketing anchors retrieved:**

| Anchor | Path | Avg Human Score | Round | Relevance |
|--------|------|----------------|-------|-----------|
| EAC (Expand and Compress) | FRzCIlkM7I.md | 6.75 | R1 | Direct predecessor/baseline; STBP claims to outperform it substantially |
| N-ForGOT | rLlDt2FQvz.md | 6.25 | R1 | Open temporal graph continual learning; theoretical grounding, accept |
| Learning system dynamics (MS-GODE) | rjuZyMfLSd.md | 6.25 | R1 | Continual learning for dynamical systems; novel benchmark, accept |
| SKI-CL | URCfZ2NgaR.md | 5.33 | R1 | Continual MTS forecasting; good application but rejected |
| Spatio-Temporal Graph Knowledge Distillation | akKNGGWegr.md | 5.25 | R1 | ST knowledge distillation; well-presented but rejected |
| CeGNN (Spatiotemporal Learning on Cell-embedded Graphs) | 0je4SA7Jg.md | 3.40 | R1 | ST graph paper, rejected |
| S2GNN (Spectral ST Graph NN) | uiyljVIP0k.md | 5.40 | R1 | Unifying long/short ST forecasting, rejected |
| KITS (Inductive ST Kriging) | mkjKqeBXkt.md | 5.67 | R1 | Incremental training for ST kriging, rejected |

**Initial bracket: 6.0–7.0**

STBP is more comprehensively validated than EAC (6.75, which is its most directly comparable anchor) with a superior backbone and a demonstrably better pattern bank mechanism (shown in the "w/o Backbone" ablation). However, the backbone confound means the headline 21% improvement over EAC is inflated—the actual pattern bank contribution is roughly 50% of that headline gain. STBP is clearly above the rejected ST-graph papers in the 5.0-5.7 range (SKI-CL, S2GND, KITS) due to stronger empirical validation, cleaner architecture, and more substantial improvements. It sits in the same range as EAC (6.75) and other accepted continual-learning-on-graphs papers (6.25).

**Final score: 6.5** — STBP offers a genuinely improved framework over EAC with a superior backbone and a demonstrably better pattern bank mechanism, strong few-shot results, and efficient computation. However, the missing cross-backbone experiment means the paper cannot cleanly attribute its gains to the continual learning mechanism vs. backbone architecture, and the near-zero improvement on the only non-traffic dataset limits the generalizability claim.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>