Now let me read the limitations and conclusion sections more carefully, and verify specific claims.Now I have a thorough understanding of the paper. Let me draft the review and then calibrate.Now let me do Round 1 calibration — bracketing across score bands with topic-relevant queries.Let me read a few key anchor reviews for calibration.Now I have a good picture of the calibration landscape. Let me establish my Round 1 bracket.

**Round 1 bracket analysis:**

- **Strong reject (<1.5)**: Papers are fundamentally broken (financial neural networks, UMAP visualization, Chinese NLP robotics). The paper under review is vastly stronger.
- **Reject (1.5-3.5)**: "Understanding Skill Adaptation with SAEs" (2.50), "Sparsity beyond TopK" (1.67), "Automatically Identifying Sparse Circuits" (3.40) — all have more fundamental issues than this paper.
- **Borderline reject (3.5-5.5)**: "SAGE: SAE Evaluations" (4.00), "Compute Optimal Inference in SAEs" (4.67), "SAEs Find Interpretable Features" (4.80), "Feature-Aligned SAEs" (4.00) — these have weaker experimental designs or more limited contributions.
- **Borderline accept (5.5-7.5)**: "Best Practices Activation Patching" (6.67, Accept), "Interpretability Illusions in Generalization" (5.60, Reject), "Subspace Interpretability Illusion" (6.33, Accept) — most similar in spirit.
- **Accept (7.5-8.5)**: "Sparse Feature Circuits" (8.00) — stronger theoretical depth + constructive contribution.
- **Strong accept (>8.5)**: No results.

**Initial bracket: 5.0–6.5**

The paper is most comparable to the interpretability illusion/negative-result papers in the 5.6–6.67 range. It has stronger experimental breadth than "Interpretability Illusions in Generalization" (5.60) but less theoretical depth than "Is This the Subspace You Are Looking for?" (6.33) and less actionable guidance than "Best Practices of Activation Patching" (6.67).

Now let me write the final consolidated review.

---

## Summary
This paper applies the Adebayo et al. (2020) randomization sanity check to SAE-based interpretability pipelines, testing whether commonly used SAE quality metrics and auto-interpretability scores can distinguish trained transformers from randomly initialized ones. Across Pythia models (70M–6.9B) and multiple randomization schemes (re-randomized with/without embeddings, Step-0, and a Gaussian-embedding control), the authors find that aggregate auto-interpretability scores (fuzzing/detection AUROC) and reconstruction metrics are often similar for trained and random models. They additionally introduce token distribution entropy as a metric that successfully distinguishes the settings, and present toy models exploring why random networks may preserve or amplify superposition.

## Strengths
- **Well-designed experimental framework with informative controls.** The five model variants—trained, re-randomized incl/excl embeddings, Step-0, and Gaussian control—create a genuinely informative comparison. The Gaussian-embedding control (Section 3, lines 59–69) provides a clear floor showing the metrics aren't completely broken (AUROC ≈ 0.50), while the random variants show that they capture structure present even without training. This is a more sophisticated design than a simple trained-vs-random comparison.

- **Thorough scale sweep with nuanced findings.** Testing across Pythia-70M through Pythia-6.9B (Figure 2) reveals a scale-dependent effect: smaller models show some discrimination while the gap narrows at larger scales. This nuance, combined with robustness checks across expansion factors (R=16–128) and sparsity values (k=16, 32) in Figure 18, adds substantial credibility and prevents the findings from being dismissed as hyperparameter-dependent.

- **Token distribution entropy as a constructive signal.** The observation that trained-model SAE latents show increasing token-distribution entropy across layers—while randomized-model latents stay low (Figure 2, last row; lines 91–127)—is a genuine positive contribution. It concretely demonstrates that *some* metric can separate the conditions and provides a constructive complement to the negative result.

- **Careful scoping in the body and limitations.** The paper explicitly states: "we do not claim that SAEs fail to capture information from trained Transformers above and beyond randomly initialized transformers; only that aggregate auto-interpretability measures do not necessarily indicate the existence of interesting underlying features" (line 173). The toy model section is appropriately framed as plausibility demonstrations, not complete explanations (line 23).

## Weaknesses

### Fatal
None

### Major
- **Title overclaims relative to evidence.** The title states "Automated Interpretability Metrics Do Not Distinguish Trained and Random Transformers," but the CE loss score (loss recovered) trivially distinguishes them—the paper itself acknowledges "the CE loss score only makes sense for the trained variant" (line 89). This is arguably the single most downstream-relevant SAE metric because it measures whether the SAE preserves the model's actual computation. The paper buries this observation rather than foregrounding it as a positive result ("here is one metric that works"). While the body and conclusion are more carefully scoped ("under certain conditions," "aggregate auto-interpretability measures"), the title invites readers to generalize beyond the evidence. This is a framing problem, not a structural flaw, but it risks misleading the community about the scope of the finding.

- **No causal or interventional evaluation metrics tested.** The mechanistic interpretability community increasingly uses activation patching, steering, and feature ablation to validate SAE features. The paper evaluates auto-interpretability scores (fuzzing, detection AUROC), reconstruction metrics (explained variance, cosine similarity), and L1 norms, but omits this entire class of evaluation. It is highly likely that causal metrics would trivially distinguish trained from random models (features from random models have no reason to be causally relevant to model behavior). This omission narrows the paper's contribution—the finding applies to distributional/correlational metrics specifically, not to "automated interpretability metrics" broadly—yet the limitations section (Section 5) does not acknowledge this gap.

### Minor
- **Thin statistical characterization of auto-interpretability results.** Only 100 latents are sampled per SAE for auto-interpretability scoring (line 77), out of up to 262K at expansion factor R=64. While the paper references Appendix E for multiple random seeds, the main text reports no confidence intervals, variance estimates, or sensitivity analysis for the AUROC comparisons. The claim that trained and random models produce "similar" scores is currently visual rather than statistical, making it harder to evaluate the strength of the evidence.

- **Large gap between toy models and full results.** Section 4.1's demonstration that matrix multiplication preserves superposition is mathematically straightforward (linear-Gaussian transforms remain linear-Gaussian). The more interesting Section 4.2 finding—that random MLPs appear to amplify sparsity regardless of input distribution—is presented for a 2-layer MLP with n_d=2 dimensions, but no attempt is made to bridge the gap to 32-layer transformers with d_model=4096. The paper honestly defers this (line 23), but the toy section's explanatory value remains limited.

### Trivial
None

## Nice-to-Haves
- Promote the token distribution entropy analysis from a preliminary observation to a first-class contribution, with threshold calibration and practical guidance for using it as a screening tool.
- Report bootstrap confidence intervals on the AUROC comparisons to make the "similar" claim quantitatively rigorous.
- Test whether findings generalize beyond TopK SAEs to other architectures (JumpReLU, Gated SAEs).
- Include at least one simple causal metric (e.g., feature ablation impact on downstream predictions) to precisely characterize which class of metrics fails and which succeeds.

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **"The abstract's use of 'similar' does heavy lifting"**: The abstract qualifies with "in many settings" and the conclusion says "under certain conditions." The body's scoping is appropriately careful; the issue is confined to the title, which is already captured in Major weakness #1.
- **"Should test whether re-randomized SAE features align with trained model features due to shared embedding structure"**: This is a follow-up research question beyond the paper's stated scope, not a weakness of the current study.
- **"Paper reads as a strong workshop paper or first draft"**: This is a subjective assessment not anchored to a specific technical weakness and conflates editorial opinion with review.
- **Criticism about the abstract claiming SAEs "produce... reconstruction metrics that are similar"**: Figure 2 does show noticeably lower explained variance and cosine similarity for some random variants, but the paper's text acknowledges these differences (lines 83–87) and correctly focuses the "similarity" claim on auto-interpretability scores where the overlap is most striking. The paper's characterization is reasonable.

## Novel Insights
The paper's most novel contribution is demonstrating that the Adebayo et al. (2020) randomization sanity check, when applied to the SAE + auto-interpretability pipeline at scale, reveals that aggregate auto-interpretability scores may primarily capture statistical structure in the input data and architectural inductive biases rather than learned computation. The finding that the gap between trained and random narrows with increasing model scale (rather than widening) is particularly notable, as it suggests the problem may worsen as the field moves to larger models. The token distribution entropy observation provides a concrete, constructive signal for distinguishing "simple token-level" features from "abstract learned" features.

## Suggestions
- Narrow the title to match the body's careful scoping (e.g., "Aggregate Auto-Interpretability Scores Do Not Distinguish Trained and Random Transformers").
- Foreground the CE loss score result as a positive finding: frame the paper as "here is which class of metrics fails and which succeeds" rather than "metrics don't work."
- Add a paragraph to the limitations section explicitly noting the omission of causal/interventional metrics and explaining why they were excluded.
- Report variance/confidence intervals for the 100-latent AUROC samples in the main text to quantify the "similarity" claim.

## Score and Decision

### Calibration Anchors

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| nSDOkm0SKo (Financial Markets NN) | 1.00 | R1 | Fundamentally broken; paper under review is vastly stronger |
| P49gSPmrvN (UMAP Scientific Discourse) | 1.00 | R1 | Trivial contribution; not comparable |
| gwZ90hFSL2 (Humanoid Robots Chinese NLP) | 1.00 | R1 | Not a research contribution; not comparable |
| tcsZt9ZNKD (Scaling and Evaluating SAEs) | 8.20 | R1 | Directly related topic but makes positive contributions (TopK SAEs); paper under review is a sanity check, not a methodological advance |
| Wxl0JMgDoU (Skill Adaptation with SAEs) | 2.50 | R1 | Narrow scope, weak evaluation; paper under review has stronger experimental design |
| UbLvSPMvMA (Sparsity beyond TopK) | 1.67 | R1 | Weak contribution; not comparable |
| 89wVrywsIy (Sparse Circuits Hierarchical Tracing) | 3.40 | R1 | Methodological issues; paper under review is better executed |
| ghH6YYDs15 (Compute Optimal Inference SAEs) | 4.67 | R1 | Theoretical contribution with limited empirics; paper under review has broader empirical grounding |
| sknUS8X9q0 (SAGE: SAE Evaluations) | 4.00 | R1 | Similar topic (SAE evaluation) but presentation/clarity issues; paper under review is better written and executed |
| F76bwRSLeK (SAEs Find Interpretable Features) | 4.80 | R1 | Foundational SAE paper; paper under review provides an important check on claims from papers like this |
| NB8qn8iIW9 (Feature-Aligned SAEs) | 4.00 | R1 | Limited novelty; paper under review has clearer contribution |
| Hf17y6u9BC (Best Practices Activation Patching) | 6.67 | R1 | Most similar in spirit—methodological evaluation of interpretability tools. That paper provides more actionable recommendations; paper under review has a stronger negative finding but weaker constructive contribution |
| bXeSwrVgjN (Benchmarking Deletion Metrics) | 6.00 | R1 | Similar "metrics evaluation" paper; paper under review has more impact on a more active subfield |
| v675Iyu0ta (Interpretability Illusions in Generalization) | 5.60 | R1 | Most comparable: also a negative-result interpretability paper. Paper under review has stronger experimental design and more impactful findings for a hotter topic |
| Ebt7JgMHv1 (Subspace Interpretability Illusion) | 6.33 | R1 | Also an interpretability illusion paper but with stronger theoretical grounding and more actionable guidance; paper under review is more empirical |
| I4e82CIDxv (Sparse Feature Circuits) | 8.00 | R1 | Strong positive contribution to SAE-based interpretability; paper under review is complementary but less constructive |

**Round 1 bracket: 5.0–6.5**

**Narrowing within bracket:** The paper is stronger than "Interpretability Illusions in Generalization" (5.60, rejected) due to its broader experimental design, more impactful subfield, and constructive entropy contribution. It is somewhat weaker than "Is This the Subspace You Are Looking for?" (6.33, accepted) which has stronger theoretical depth and more actionable guidance, and weaker than "Best Practices of Activation Patching" (6.67, accepted) which provides clearer recommendations. The paper's title overclaim and missing causal metrics are real but addressable concerns. The core experimental finding is novel, timely, and well-executed.

**Final calibrated score: 6.0**

The paper delivers a genuinely important sanity check for a high-traffic subfield. The experimental design is thorough and the finding is novel. However, the overclaiming in the title, the omission of causal metrics, and the underdeveloped constructive half (what should the community do instead?) keep it from a clear accept. The paper is a solid borderline accept—the negative result is convincing and timely, but the paper would benefit from tighter framing and at least one causal metric to characterize the scope of the problem.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>