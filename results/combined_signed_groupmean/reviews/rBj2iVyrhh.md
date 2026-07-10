## Summary

This paper proposes Classifier-Constrained Alternating Training (CCAT), a two-stage framework for mitigating modality imbalance in multimodal learning. The key insight is that prior alternating-training methods (MLA, Reconboost) prevent encoder-level interference but fail to stop the classifier from developing an entrenched bias toward the faster-converging modality. CCAT addresses this by (1) pretraining a balanced classifier using bidirectional cross-attention with a modality-contribution regularization term, then (2) freezing this classifier as a stable anchor during modality-alternating training, with modality-specific LoRA modules for adaptation and a sample-level secondary update for severely imbalanced samples. Experiments on CREMA-D, Kinetic-Sound, and MVSA show consistent improvements over existing SOTA methods.

## Strengths

- **Well-motivated diagnosis of a real limitation.** The paper identifies a genuine gap in prior alternating-training methods: encoder-level decoupling does not prevent the classifier from developing structural preference for the faster-converging modality. This observation (Section 1) is clearly articulated, and the proposed two-stage solution—pretraining an unbiased classifier then freezing it—is a coherent, direct response. The analogy to class-imbalance remedies (fixed last-layer classifiers) provides a clear intellectual scaffold.

- **Consistent improvement across three datasets.** CCAT outperforms all baselines on all three benchmarks. The gain on Kinetic-Sound (+6.76 absolute points over the next-best method, LFM) is substantial and robust. The gains on CREMA-D (+2.27) and MVSA (+1.92) are more modest but directionally consistent.

- **Comprehensive ablation study.** Table 2 systematically ablated four components (classifier freezing, alternating training, secondary updates, LoRA). Removing any component reduces performance across all three datasets, confirming that each contributes to the overall result.

- **Additional evidence through feature visualization.** Figure 5 provides t-SNE visualizations with quantitative clustering metrics (CH, SH, DB), demonstrating that CCAT produces more separable feature representations than MLA or a variant without the frozen classifier. This is a useful sanity check beyond accuracy comparisons.

## Weaknesses

### Major

1. **No statistical significance or variance reported for any result.** The paper reports only averages of three random seeds (Table 1 caption) without standard deviations, confidence intervals, or individual trial values. The CREMA-D gain (+2.27pp over the best baseline) and MVSA gain (+1.92pp) are small enough that routine variance (1–2pp is typical on these benchmarks) could produce overlap. Without variance, the reader cannot assess whether these improvements reflect real superiority or random seed variation. Even the large KS gain (+6.76pp) would benefit from variance reporting for completeness.

2. **Abstract contains a factual arithmetic error.** The abstract states "accuracy gains of +1.35% on CREMA-D," but Table 1 shows CCAT at 85.89% and the best baseline (LFM) at 83.62%, a difference of +2.27 percentage points. The KS (+6.76) and MVSA (+1.92) figures in the abstract match the table. This is a factual error in a headline claim and must be corrected.

### Minor

3. **Overclaimed theoretical contribution.** Section 3.1 is framed as "a proof" and "a unified theoretical framework" (contribution i), but is actually a qualitative analogy supported by simplified gradient equations under strong assumptions. The γ coefficients in Eq. (3) are described as "implicitly learned modality utilization coefficients" without formal definition. The analysis identifies a useful conceptual parallel between class imbalance and modality imbalance, but it does not constitute a rigorous proof or theoretical framework as claimed. The paper should tone down these claims to match what is actually delivered.

4. **Figure 1 caption contradicts the data it describes.** The caption (line 34) states that "Ours" shows "a more pronounced imbalance," but the data table (lines 36–43) shows Ours achieves a gap of 0.30 (0.65 vs 0.35) compared to MLA's gap of 0.80 (0.90 vs 0.10)—strictly *more balanced*. This is a writing error, not a data problem, but it appears in the paper's central motivating figure and must be corrected.

5. **Stage 2 contribution computation underspecified.** The paper states (line 179) that in Stage 2, the contribution score computation follows "the same decision-level fusion used in the inference stage." However, Eq. (5) requires a fused feature vector f_i for mutual information computation, and it is not specified what f_i represents under decision-level fusion where no explicit fused representation exists. This makes the sample-level secondary update (Algorithm 1, lines 10–15) difficult to reproduce as described.

6. **Baseline implementation protocol not documented.** The paper does not state whether all baselines were reimplemented with the same encoder backbones (ResNet18 for audio/visual, ResNet50/BERT for text-image) or whether results were taken from original papers using potentially different architectures. This ambiguity makes the comparison's fairness uncertain.

### Trivial

7. **Minor numerical inconsistency.** The text (line 22) says MLA reduces contribution disparity to 0.92, but the table data shows MLA's dominant modality at 0.90 at epoch 100. The origin of 0.92 is unclear and needs clarification.

## Nice-to-Haves

- Discuss failure cases (e.g., when both modalities are weak, or when β triggers secondary updates on a large fraction of the batch).
- Report training time comparisons to quantify the computational overhead of secondary updates.
- Include a limitations paragraph.

## Removed Points

These points from the input review were removed after verification against the paper:

1. **"Missing ablation of the regularization term"** — The scoring model assigned this near-zero impact. While informative, the ℒ_reg term is part of Stage 1 pretraining and its contribution is separable from the core alternating pipeline. Not a required ablation at this stage.
2. **"LoRA is not standard LoRA"** — The paper defines LoRA_m(z) = B^m A^m z, applied as a residual correction. This is a valid low-rank adaptation; the analogy is appropriate.
3. **"No code release mentioned"** — Code release is a large artifact; this is a reproducibility desire, not a weakness of the submitted work.
4. **"No limitation/failure-case discussion"** and **"Computational overhead not discussed"** — These are suggestions for improvement, moved to Nice-to-Haves.
5. **"MI estimator not standard"** — The paper cites Zhou et al. (2025b) as the source; the formula is presented as adapted from that reference.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Fix the abstract CREMA-D number (change +1.35% to +2.27%).
2. Correct the Figure 1 caption ("more pronounced imbalance" → "substantially reduced imbalance").
3. Report standard deviations or individual seed values for all main results.
4. Specify exactly what f_i represents in Stage 2 when using decision-level fusion.
5. Clarify whether all baselines were reimplemented with the same backbones or cited from original papers.
6. Tone down the theoretical claims in Section 3.1 to match the qualitative/analogical nature of the analysis.

---

## Calibration Report

**Calibration anchors retrieved (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| `5lUdTogEL3.md` | 1.00 | R1 | No | Unrelated topic (person re-id); strong reject anchor |
| `gwZ90hFSL2.md` | 1.00 | R1 | No | Unrelated (cross-lingual NLP); strong reject anchor |
| `nSDOkm0SKo.md` | 1.00 | R1 | No | Unrelated (financial modeling); strong reject anchor |
| `a4O528mek9.md` | 3.00 | R1 | No | Multimodal learning under incomplete data; much weaker empirical contribution |
| `YrxhSkfHh0.md` | 3.33 | R1 | No | Multimodal feature extraction method; less comprehensive evaluation |
| `gNoqEdT2wO.md` | 2.33 | R1 | No | Multimodal continual learning benchmark; different problem |
| `ul1cjLB98Y.md` | 5.25 | R1 | Yes | **Most comparable anchor.** Theory of unimodal bias in multimodal learning. Rejected partly because theory only applied to linear networks and lacked real-world validation. Our paper has stronger empirical results on real benchmarks, making it the stronger paper. |
| `XTwwtlEfTF.md` | 4.50 | R1 | Yes | Robust multimodal learning with missing modalities. Rejected for missing baselines and limited novelty. Our paper has clearer novelty and stronger baselines. |
| `Pa6SiS66p0.md` | 4.33 | R1 | No | Multimodal continual learning; different problem scope |
| `5BXWhVbHAK.md` | 6.33 | R1/R2 | Yes | Cross-modal synergy without paired supervision. Accepted despite novelty concerns, due to strong theory + experiments. Our paper has comparable empirical work; the theory is weaker but the practical contribution is clearer. |
| `LuVulfPgZN.md` | 6.00 | R1 | No | Out-of-modal generalization. Accept with all 6s. Similar contribution level. |
| `6Mg7pjG7Sw.md` | 6.00 | R1 | No | Data-efficient multimodal mapping. Accept with all 6s. Similar contribution level. |
| `uAFHCZRmXk.md` | 8.00 | R1 | No | Analysis paper on modality gap in VLMs. Much stronger theoretical depth; different genre. |
| `TPZRq4FALB.md` | 8.00 | R1 | No | Test-time adaptation for multimodal reliability bias. Stronger theoretical framing. |
| `WyEdX2R4er.md` | 8.00 | R1 | No | Visual data-type understanding in VLMs. Unrelated to modality imbalance. |
| `Rc8z5wLzBF.md` | 5.75 | R2 | No | Omni-bench benchmark paper. Rejected; different contribution type. |
| `1L52bHEL5d.md` | 6.00 | R2 | Yes | Test-time adaptation for missing modalities. Accepted with all 6s despite weaknesses comparable to ours (-9.93 for code, -9.99 for contribution overlap). Supports a 6.0 placement. |
| `U2K4bQVWez.md` | 5.83 | R2 | Yes | CentroBind for multimodal representations. Rejected for limited baselines and being incremental. Our paper has stronger baselines and more comprehensive evaluation. |

**Bracket reasoning:** Round 1 placed the paper above 5.25 (Theory of Unimodal Bias) and 4.50 (Robust MML), and comparable to or slightly below 6.33 (Synergize Training). Round 2 confirmed alignment with the 5.75–6.33 band, with the Test-Time Adaptation paper (6.00, Accept) providing the closest point anchor.

**Impact-score comparison:** The paper's strongest items (diagnosis +9.72, consistent improvement +10.00, t-SNE evidence +7.23) are comparable in magnitude to the anchors' strongest items. The two most impactful weaknesses (no variance -9.99, abstract error -10.00) are significant but fixable—neither invalidates the core method. The overclaimed theory (-10.00) reflects presentation overreach rather than a method flaw. Like the Test-Time Adaptation anchor (6.00, accepted despite -9.93 and -9.99 weaknesses), this paper's correctable weaknesses do not outweigh its clear methodological contribution and consistent empirical results.

**Final score:** 6.0 — Borderline Accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>