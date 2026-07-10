## Summary

This paper applies sparse autoencoders (SAEs) to both trained and randomly-initialized Pythia transformers (70M–6.9B parameters) and evaluates them with standard auto-interpretability metrics (fuzzing/detection AUROC). The central finding is that at larger model scales (1B, 6.9B parameters), these metrics fail to distinguish trained from randomly-initialized models — and indeed the randomized variants sometimes score *higher* than the trained model. The paper recommends routine randomized baselines and proposes token distribution entropy as a supplementary measure of feature "abstractness" that does differentiate the two settings. This is a timely and actionable sanity-check result for the mechanistic interpretability community.

## Strengths

- **The core negative finding is important and actionable.** For Pythia-6.9b, aggregate auto-interpretability AUROC scores for random-weight transformers match or exceed those from trained transformers (Figure 1: Trained AUC ≈ 0.79, all randomized variants AUC ≈ 0.87). This is a genuinely concerning result that should influence how the field validates SAE feature quality. (Impact: **+9.98**)

- **Scale is used effectively across five model sizes (70M to 6.9B).** The finding that the gap between trained and random models shrinks with scale is more informative than a single-model-size result and justifies the paper's emphasis on this pattern. (Impact: **+9.93**)

- **The token distribution entropy analysis provides a concrete path forward.** It demonstrates that a simple measure — entropy of latent activations over token IDs — can differentiate trained from random features (trained entropy increases with layer depth; random entropy stays flat), strengthening the paper's methodological recommendations beyond a purely negative result. (Impact: **+9.77**)

- **The experimental design is well-structured**, with five model variants (Trained, Re-randomized incl./excl. embeddings, Step-0, Gaussian-input Control) that carefully isolate different sources of structure. The Step-0 variant using Pythia's actual initialization checkpoints avoids concerns about the randomization procedure not matching the true initialization distribution. (Impact: **+3.18**)

## Weaknesses

### Major

- **The title overstates the finding relative to the data.** The title "Auto-Interpretability Metrics Do Not Distinguish Trained and Random Transformers" is unqualified, but the paper's own results show that for Pythia-70m and Pythia-160m, the AUROC metrics *do* distinguish trained from random (Figure 2, AUROC Pruned row: trained ≈ 0.65–0.75 vs. randomized ≈ 0.55–0.65). The pattern is scale-dependent: the failure occurs primarily at the larger scales (1B, 6.9B). While the paper text appropriately hedges ("in many settings," "under certain conditions"), the title makes a claim broader than the evidence supports. This matters because casual readers may draw a more sweeping conclusion than the data warrants. (Impact: **-9.61**)

### Minor

- **The toy model section (Section 4) provides limited evidential weight for understanding the main result.** The paper is appropriately upfront that these are plausibility demonstrations (line 131: "we leave the question of which predominates…to future work"), but this candor means the section does not advance a mechanistic understanding of *why* the metrics converge with scale. Section 4.1's argument that matrix multiplication preserves a generative notion of superposition is largely a mathematical tautology given the generative model's assumptions. Section 4.2's finding — that random MLP outputs look similar regardless of whether inputs were superposed or Gaussian — undercuts rather than supports the explanatory story. The section would be stronger either substantially revised to make quantitative predictions tied to the scaling trend, or trimmed to focus more space on the main empirical results. (Impact: **-9.66**)

- **Only 100 latents are sampled per SAE** (line 77) for auto-interpretability scoring. SAEs typically learn tens of thousands of latents; a sample of 100 raises questions about whether the aggregate AUROC reliably estimates the full distribution, especially for fine-grained comparisons across model variants. The paper notes consistency across multiple random seeds (Appendix E), which partially mitigates this concern, but the small sample limits confidence in the token distribution entropy analysis specifically, which relies on these same 100 latents.

### Trivial

- None.

## Nice-to-Haves

- **A systematic analysis of *why* the gap between trained and random closes with scale** would substantially strengthen the paper. Possible factors include: (a) larger random models having more structured activations, (b) the SAE expansion factor being held constant while the residual stream dimension grows (giving the SAE more capacity to overfit), or (c) the auto-interpretability LLM (Llama-3.1-70B) being better at generating plausible explanations for any activations from larger models. The paper speculates about some of these (line 87) but does not ablate them.

- **The token distribution entropy could be validated by showing it correlates with something downstream**, such as the causal effect of intervening on features. Without such validation, entropy is just another aggregate metric that might also fail under new conditions.

## Removed Points

These points were flagged by the input review but removed with justification:

1. **"Section 4.3 uses GloVe embeddings rather than the actual Pythia embedding matrices"** — REMOVED (factually incorrect). The paper states: "we train SAEs on pre-trained GloVe word vectors, **the embedding matrices of Pythia models**, the results of passing these inputs to a randomly initialized two-layer MLP, and Gaussian controls" (line 157). Both GloVe and Pythia embeddings are used.

2. **"The 'Detection' AUROC results should be in the main text, not an appendix"** — REMOVED (misreading). AUROC (Detection) is shown as its own row in Figure 2 in the main text. Only the full ROC curves are in Appendix B; the aggregate metric is in the main figure.

3. **"Missing variance/error bars on AUROC values"** — REMOVED. The paper references multiple random seeds in Appendix E, and the central claim is about the overall pattern (overlap between trained and random), not precise point estimates. This is a reasonable level of rigor for this type of empirical comparison.

4. **"The Gaussian-input Control variant is less informative than it appears"** — REMOVED. The paper presents the control as a lower-bound sanity check ("we expect auto-interpretability to perform at the level of chance," line 69) and does not overclaim its informativeness. The more informative comparisons (Re-randomized, Step-0) are the primary focus.

5. **"The GloVe experiment in Section 4.3 uses a single random seed"** — REMOVED. The paper transparently states this limitation (line 157: "we use a single random seed").

## Novel Insights

None beyond the paper's own contributions. The input review did not surface any perspective that the paper does not already articulate.

## Suggestions

1. **Revise the title** to reflect the scale-dependent nature of the finding, e.g., "Auto-Interpretability Metrics Fail to Distinguish Trained and Random Transformers at Scale."
2. **Either strengthen or trim Section 4.** As a plausibility demonstration it is honest but weak. Either develop it into a quantitative model that predicts the scaling trend, or replace it with more thorough characterization of the main empirical result (e.g., ablating the SAE expansion factor vs. model size).
3. **Consider reporting confidence intervals or bootstrapped error bars** on the AUROC values for the 100-latent samples to quantify the uncertainty of the comparisons.

## Score and Decision

### Calibration Report

**Round 1 bracket:** I identified the paper as plausibly in the 5.5–7.5 range, given its nature as an empirical sanity-check paper without new methodological proposals.

**Anchors retrieved across all queries:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `nSDOkm0SKo.md` (Financial markets) | 1.00 | R1 | No | Topically unrelated; strong reject baseline |
| `5lUdTogEL3.md` (Person re-id) | 1.00 | R1 | No | Topically unrelated |
| `tcsZt9ZNKD.md` (Scaling SAEs) | 8.20 | R1 | No | Method paper with strong technical contribution; our paper lacks this novelty |
| `F76bwRSLeK.md` (SAEs find interpretable features) | 4.80 | R1 | Yes | Mixed reviews, serious methodological concerns from some reviewers; our paper is cleaner |
| `9ca9eHNrdH.md` (SAEs don't find canonical units) | 7.00 | R1 | Yes | Closest analog — negative result about SAEs with novel methods (stitching, meta-SAEs). Our paper lacks comparable methodological novelty |
| `1Njl73JKjB.md` (Principled evaluations) | 7.00 | R1 | Yes | Proposes new evaluation framework; our paper is pure empirical study |
| `OZWHYyfPwY.md` (Don't trust your eyes) | 7.00 | R2 | Yes | Similar sanity-check spirit about interpretability, but has new fooling circuits + theory. Our paper lacks methodological novelty |
| `v675Iyu0ta.md` (Interpretability Illusions) | 5.60 | R2 | Yes | Similar negative result, but only on toy Dyck tasks. Our paper tests on real LLMs at scale |
| `bXeSwrVgjN.md` (Benchmarking Deletion Metrics) | 6.00 | R2 | Yes | Mixed reviews, has both positives and serious criticisms |
| `todLTYB1I7.md` (Principled Eval Framework) | 5.00 | R2 | Yes | More severe limitations (claims-methods mismatch); our paper is cleaner |

**Narrowing:** Compared to the strongest anchor ("Don't Trust Your Eyes," 7.00), our paper shares very high-impact strengths (important negative finding) but lacks the methodological novelty (new fooling circuits, formal theory) that drove that paper's score. Compared to the weakest relevant anchor ("Interpretability Illusions," 5.60), our paper has a clear advantage in testing on real LLMs at scale vs. toy tasks. The scoring model rated our paper's core strengths very highly (+9.98, +9.93, +9.77) but also rated the title and toy-model issues as highly impactful weaknesses (-9.61, -9.66). This tension places the paper below the novel-method negative-result papers (7.00) but above the toy-task-only papers (5.60).

**Final score:** 6.0 — borderline accept. The paper makes a real, well-evidenced contribution with important implications for the field, but the title overreach and weak toy model section prevent it from reaching the "accept" tier. The experimental design, use of scale, and entropy analysis are genuinely strong, and the core finding is important enough to warrant publication with revisions.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>