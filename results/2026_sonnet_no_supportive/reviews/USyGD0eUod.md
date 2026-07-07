Now I have sufficient calibration. Let me compose the final review.

---

## Summary
This paper applies the Adebayo et al. (2020) randomization sanity check to sparse autoencoder (SAE) evaluation: it asks whether common SAE quality metrics and auto-interpretability pipelines distinguish SAEs trained on genuine Pythia transformers (70M–6.9B parameters) from those trained on randomly initialized ones. The central finding is that aggregate fuzzing AUROC often cannot make this distinction, especially at larger scales. The paper proposes token distribution entropy as a preliminary alternative metric that does separate trained from random models, and presents toy model analyses to speculate about mechanisms.

---

## Strengths

- **Novel, field-relevant sanity check.** Adapting the Adebayo et al. (2020) randomization test to SAE evaluation is a direct, well-motivated contribution. The mechanistic interpretability field has largely operated without asking whether its primary evaluation metric (auto-interpretability AUROC) passes a null-model baseline, and the finding that it often does not is consequential. This is a specific, well-motivated experimental design, not a generic critique.

- **Empirical breadth across model sizes and randomization schemes.** The study spans five Pythia model sizes (70M–6.9B), three distinct randomization schemes (re-randomized incl./excl. embeddings, step-0), and a Gaussian-embedding control that anchors what chance performance looks like. The finding that randomized models approach or match trained models on AUROC (Figures 1 and 2), especially at larger scales, is replicated across enough configurations to be credible. Robustness to hyperparameters (expansion factor 16–128, sparsity 16/32, 100M vs. 1B token subsets) is also reported.

- **Token distribution entropy as a concrete alternative metric.** Figure 2 (row 7) shows that entropy cleanly separates trained from randomized variants: trained models' features increase in entropy across layers (becoming more abstract), while randomized models' features remain token-specific with low entropy. This is a measurable, specific finding rather than a vague call for better metrics.

- **Appropriate scope and honest framing.** The authors are explicit that the finding does not imply SAEs fail to capture meaningful computation, only that aggregate metrics cannot confirm this (Sections 5 and 6). The limitations section candidly acknowledges the evaluator model choice.

---

## Weaknesses

### Fatal
None.

### Major

- **AUROC asymmetry is underanalyzed.** Figure 1 shows the trained Pythia-6.9B model achieves fuzzing AUROC = 0.79, while all three randomized variants reach 0.87–0.88. The paper consistently frames this as randomized models being "similar" to trained, but the randomized models systematically *exceed* the trained model. This is qualitatively different from and more alarming than mere similarity: it suggests the metric may reward token-specificity, a property that is more present in untrained networks. The paper's only offered explanation—that "features become more specific as SAE size increases" (Section 3)—is speculative and does not account for the directional reversal. The conclusion that the metric is "insufficient" is correct, but understating the direction (randomized > trained, not just ≈ trained) weakens the overall framing and the urgency of the finding.

### Minor

- **Toy model section defers its central question.** Section 4 explicitly states: "we leave the question of which predominates…to future work." The Pareto frontier analysis (Figure 5) shows that randomly initialized MLP outputs improve over their inputs for both superposed and Gaussian inputs, and the paper reads this as evidence of sparsification. However, there is no quantitative bridge from these toy-model dynamics to the Pythia-scale transformer results. The section functions as a plausibility argument for two competing hypotheses (preservation vs. amplification of superposition) rather than evidence for either.

- **No variance reported across random seeds in main figures.** The paper samples 100 latents per SAE for AUROC estimation. Appendix E covers multiple random seeds for one figure, but Figure 2 carries no error bars. For smaller models where the trained/randomized AUROC gap is modest, sampling variance over 100 latents could be material.

- **INT4 quantized evaluator not ablated.** The paper uses Meta-Llama-3.1-70B-Instruct-AWQ-INT4 for all auto-interpretability scoring. The limitations section acknowledges that alternative evaluator models could yield different insights (Section 5), but does not report whether a non-quantized or larger evaluator changes the main finding for smaller model scales where trained/randomized gaps are already small.

### Trivial
None surviving filtering.

---

## Nice-to-Haves

- The token distribution entropy result is the paper's most actionable finding, but it is described as "preliminary" and presented at a single-metric proof-of-concept level. Reporting what AUROC entropy achieves in separating trained from randomized across the full five model sizes—mirroring the fuzzing AUROC analysis—would significantly strengthen the claim.

- The parameter norm hypothesis (Section 3: re-randomized variants are closer to trained than step-0 because norm is preserved by design) could be directly tested, e.g., by comparing step-0 models with artificially rescaled norms against re-randomized variants.

- A cleaner statement of where AUROC discrimination breaks down (around 410M or 1B based on Figure 2) would be valuable for practitioners.

---

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Figure 5 color coding confusion (harsh critic).** The critic noted that "Superposed inputs" and "GloVe inputs" both appear labeled orange. This is a parser/caption artifact: the figure uses separate subplot pairs for toy datasets and GloVe vectors, and the color coding is consistent within each pair. Not an author error; removed per formatting artifact rule.

- **"Pruned" vs. "Fuzzing" AUROC label inconsistency (harsh critic).** Figure 2 row 4 is labeled "AUROC (Pruned)" while the text uses "Fuzzing." This reflects Paulo et al. (2024) implementation nomenclature ("pruned" is a task variant in that framework) rather than a conceptual mismatch. Removed as a minor naming convention difference.

- **CE loss score criticism (harsh critic).** The critic noted CE loss "adds nothing to the trained-vs-randomized comparison." The paper itself states this clearly ("only makes sense for the trained variant," Section 3) and includes the metric only for its intended purpose: characterizing trained model SAE quality against literature benchmarks. This is not a weakness; removed as a strawman.

---

## Novel Insights

The paper's most underappreciated finding is directional: randomized Pythia-6.9B models achieve *higher* fuzzing AUROC (0.87–0.88) than the trained model (0.79), not merely similar scores. If this directional asymmetry is robust, it implies the standard evaluation metric may be anti-correlated with the property it is meant to measure—rewarding token-specificity that is more pronounced in untrained networks. This would mean the metric is not just uninformative but systematically misleading. This deserves explicit attention in follow-up work developing alternative metrics and may be the paper's most consequential empirical observation.

---

## Suggestions

1. In Section 3 and Figure 1, explicitly address the directional asymmetry (randomized > trained on AUROC at 6.9B) with either a mechanistic account or clear acknowledgment that it is an open and alarming finding.
2. Add error bands from Appendix E's multiple-seed experiments to the main Figure 2 panels.
3. Develop the entropy discriminator into a full sweep matching the fuzzing AUROC analysis (all five model sizes, per layer), to shift the contribution from "here is a failure mode and a direction" to "here is a candidate replacement metric."
4. Test the parameter-norm hypothesis directly by rescaling step-0 weights to match trained-model norms and checking whether the step-0 curve moves toward the re-randomized curves.

---

## Score and Decision

**Calibration anchors:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| `nSDOkm0SKo.md` | 1.00 | R1 | Unrelated financial networks paper; far below this paper's quality |
| `tcsZt9ZNKD.md` | 1.75 (bimodal) | R1 | "Scaling and evaluating SAEs" — placed in 1.5-3.5 bracket but scores 3/10/10/8/10 due to one outlier; the paper itself is a top SAE contribution |
| `F76bwRSLeK.md` | 4.80 | R1 | Original SAE paper finding interpretable features; accepted borderline; less critical/evaluative than this paper |
| `ZtvRqm6oBu.md` | 5.25 | R1 | SAE unlearning application; less methodologically foundational than this paper |
| `1Njl73JKjB.md` | 7.00 | R1 | "Principled Evaluations of SAEs" — proposes evaluation framework with supervised dictionaries; closely analogous, fully worked-out |
| `9ca9eHNrdH.md` | 7.00 | R1 | "SAEs Do Not Find Canonical Units" — critical examination of SAEs; two novel methods (stitching + meta-SAEs); comparable in spirit |
| `XAjfjizaKs.md` | 6.50 | R1 | Multi-layer SAEs for residual streams; solid incremental contribution |
| `imT03YXlG2.md` | 6.50 | R1 | SAE for CLIP vision transformer; solid application paper |
| `I4e82CIDxv.md` | 8.00 | R1 | Sparse feature circuits; more methodologically complete and practically actionable |

**Round 1 bracket:** 6.0–7.5. The paper is clearly above the borderline rejection zone (avg 3–5), but sits below the fully elaborated evaluation frameworks and multi-technique contributions at 7–8.

**Narrowing:** The two closest anchors are `1Njl73JKjB.md` and `9ca9eHNrdH.md`, both at 7.0. Compared to those papers, this submission is:
- Narrower in scope (a single sanity check rather than a full evaluation framework or dual-technique investigation)
- More preliminary in its positive contribution (entropy metric described as "proof-of-concept")
- Equally clear in identifying a genuine limitation of the field
- Somewhat weaker in the analysis depth (AUROC asymmetry underanalyzed, toy model inconclusive)

`XAjfjizaKs.md` (avg 6.5) and `imT03YXlG2.md` (avg 6.5) are more limited-scope application papers; this submission's contribution is more foundational but less developed than the 7.0 papers. A score of **6.5** reflects an honest accept: the sanity check is real and important, the empirical scope is credible, but the paper leaves its most interesting observations (directional asymmetry, entropy discriminator) in a preliminary state that warrants continued development.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>