Now I have sufficient calibration data. Let me produce the final review.

## Summary

This paper identifies and formalizes Dual-level Noisy Correspondence (DNC) in Multi-modal Entity Alignment (MMEA)—noise in both intra-entity (entity-attribute) and inter-graph (entity-entity, attribute-attribute) correspondences. The proposed framework, RULE, estimates correspondence reliability via a two-fold principle (uncertainty from Dempster-Shafer Theory + consensus from marginal contribution), uses these estimates to guide robust attribute fusion (DRF) and inter-graph discrepancy elimination (DRL) during training, and further employs a test-time reasoning module (TTR) using Qwen2.5-VL-72B to refine similarity scores. Experiments on five benchmarks under three noise levels show substantial improvements over seven baselines.

## Strengths

1. **Novel and well-motivated problem formulation (Section 1, Figure 1).** The DNC problem—simultaneous noise at intra-entity and inter-graph levels—is a realistic challenge that existing MMEA methods assume away. The paper grounds this with concrete examples and cites statistics (e.g., "over 50% in ICEWS benchmarks") to show real-world prevalence.

2. **Two-fold reliability principle is theoretically grounded and empirically validated (Sections 2.2.1–2.2.3, Figures 3b and 4).** Using Dempster-Shafer Theory via Dirichlet evidence to quantify uncertainty is a principled choice. Theorem 1 correctly identifies the insufficiency of uncertainty alone, motivating the consensus principle. Figures 3b and 4 show clean separation between noisy and clean pairs—convincing evidence that the estimation mechanism works as designed.

3. **Training-time components (DRL + DRF) produce clear, substantial improvements on the challenging Non-name setting (Table 1, Table 3).** At 50% DNC on ICEWS-WIKI, RULE without TTR (56.5 H@1, from ablation) still outperforms the best baseline (HHREA at 43.9) by 12.6 points. Even the stripped "w/o DRL" baseline is low (31.6), but the ablation chain shows each component adds meaningful value: w/o DRF=50.4, w/o TTR=56.5, full=58.2. This demonstrates that the core methodological contribution—robust training under DNC—is effective on its own terms.

4. **Comprehensive evaluation across 5 benchmarks, 7 baselines, 3 noise levels, and two evaluation protocols.** The inclusion of both inherent (real-world) and artificially injected noise at 20% and 50% provides a thorough picture of robustness at different noise intensities.

## Weaknesses

### Fatal
None.

### Major

1. **The test-time MLLM creates an asymmetric comparison that the paper does not sufficiently flag.** RULE uses Qwen2.5-VL-72B-Instruct (a 72B multimodal LLM) during inference (Section 3.1), while none of the seven baselines have access to any comparable model. The paper states "For fair comparisons, we adopt the same backbone (i.e., CLIP) for all baselines and our method"—but this refers only to the attribute encoder backbone, not the 72B MLLM. The ablation (Table 3) reveals the impact: in the All-attributes setting, the MLLM alone adds 3.6 H@1 (94.0→97.6) while the full TTR adds only 0.1 more. The headline All-attributes results (Table 2) are therefore inflated by an external resource. However, this does **not** invalidate the core contribution—in the Non-name setting, MLLM alone adds only 0.1 H@1 (56.5→56.6), and even without TTR, RULE's training-time components dramatically outperform baselines. The paper should present the training-time results as the primary comparison and flag TTR-enhanced results separately.

**Severity justification**: This is the most significant issue. It concerns fairness of comparison and presentation but does not undermine the paper's central thesis about robust training under DNC.

### Minor

2. **All-attributes setting conflates DNC robustness with name-attribute discriminability.** At 50% DNC in All-attributes (Table 2), RULE achieves 97.7 H@1 on ICEWS-WIKI, but even MEAformer reaches 91.9. The entity name is highly discriminative and robust to the injected noise types, making this setting less informative for measuring true DNC robustness. The paper already addresses this by including the Non-name setting, but presents both settings as equally probative without explicitly discussing this caveat.

3. **Consensus estimation via greedy strategy (Section 2.2.2) is under-specified.** Equation 7 defines π₀ with |π₀| = ⌊M/2 + 1⌋ for M ≥ 3, but the main text does not specify *which* attributes form this initial subset. The selection criterion matters because different initial subsets could lead to different π* through the greedy procedure. The paper references "Appendix F.3", but the main text should state the selection principle.

4. **Assumption 1 boundary cases are not directly examined.** The assumption that correct attributes contribute non-negative marginal contribution while incorrect ones contribute negative (Section 2.2.2) is intuitive but not obviously true for partially relevant attributes. While aggregate results support its practical utility, a direct analysis of Δ distributions for known clean vs. noisy attributes would strengthen confidence.

### Trivial
None.

## Nice-to-Haves
- Report results with variance/confidence intervals over multiple runs (single-run reporting is standard in this field but would strengthen the paper).
- Discuss the computational cost of invoking the 72B MLLM per query for practical applicability.
- Analyze sensitivity to hyperparameters β and γ beyond default fixed values (referenced to Appendix G.10).
- Include a simpler robust baseline in the ablation (e.g., confidence-based filtering or trimmed MSE) to isolate the value of the Dirichlet-based formulation.

## Removed Points
Points from the harsh critic review removed per filtering rules:
- **"MLLM CoT prompt opacity"** → The paper references Appendix F.5 and Appendix I for full prompt details. Appendix content is stripped, so this is not a verifiable omission from the main text.
- **"Circular dependency between reliability and representations"** → This describes standard end-to-end training (representations improve iteratively as the loss is optimized), not a methodological flaw.
- **Table 2 column header formatting** → Parser artifact; the original paper uses proper dataset names.
- **"Could be one of the first" claim is vague** → The claim is appropriately qualified ("to the best of our knowledge," "could be one of the first") and scoped to MMEA specifically.
- **"w/o DRL ablation is too weak"** → The ablation already shows a clean degradation chain; adding a simpler robust loss baseline is a nice-to-have, not a weakness.
- **"No statistical significance"** → Single-run reporting is standard in MMEA/entity alignment literature; demoted to nice-to-have.

## Novel Insights

The harsh critic's analysis reveals a useful structural observation: the paper's contribution is actually two separable parts—(1) the training-time robust framework (DRL+DRF) which is the paper's strongest contribution, convincingly demonstrated by the Non-name results, and (2) the test-time MLLM module which is a complementary enhancement whose value is concentrated in the All-attributes setting (adding 3.6 H@1 there vs. 0.1 in Non-name). The ablation further shows that within TTR, the MLLM scores dominate—the combination with prior scores adds negligible benefit (MLLM Enhance=97.6 vs. full TTR=97.7 in All-attributes). This suggests that if the MLLM asymmetry concern is resolved by separating these contributions in the main results, the paper's core thesis about robust training stands on strong ground.

## Suggestions

1. In revision, separate training-time and test-time contributions explicitly: present "w/o TTR" (or a clear training-only variant) as the primary comparison point against baselines in the main tables, and present TTR-enhanced results in a clearly marked separate column or section. This resolves the fairness concern while preserving the completeness of the ablation story.

2. Specify the π₀ selection criterion in Section 2.2.2 (Eq. 7) in the main text—e.g., sorted by individual confidence, random, or other principle.

3. Add a brief note in the results discussion acknowledging that the All-attributes setting benefits from the highly discriminative name attribute and that the Non-name setting provides the cleaner test of DNC robustness.

## Score and Decision

**Calibration Summary.** Retrieval anchored against 13k human reviews. Round-1 bracket: 6.0–7.5. 

| Anchor Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| Revisit and Outstrip Entity Alignment (GEEA) | z3dfuRcGAK | 6.67 | 1,2 | Similar EA domain, comparable contribution level; our paper has stronger empirical gaps but a presentation fairness concern GEEA doesn't have. |
| Multiple Heads are Better than One (MoMoK) | ue1Tt3h1VC | 6.60 | 1,2 | MMKG representation paper; similar type/severity of weaknesses (clarity gaps, evaluation scope). Our paper has a more novel problem formulation. |
| Neuro-symbolic Entity Alignment (NeuSymEA) | NNUiUwQWx6 | 5.75 | 1,2 | Rejected despite 5-6 scores; had major complexity and hyperparameter sensitivity concerns. Our paper is stronger in both problem novelty and empirical validation. |
| MOFI: Noisy Entity Annotated Images | QQYpgReSRk | 6.25 | 2 | Had concerns about unfair comparison (dataset size asymmetry) similar to our MLLM issue; accepted with revisions. |
| LoGra-Med: Multi-Graph Alignment | SOsotxYtPC | 5.25 | 2 | Rejected; weaker empirical results and novelty. |
| EMMA: Multi-modal Alignment | Ev4iw23gdI | 5.75 | 2 | Accepted but with narrower scope and weaker empirical gaps. |

The paper sits at 6.5: above NeuSymEA (5.75) and EMMA (5.75) due to clearer problem novelty and stronger Non-name results; comparable to MoMoK (6.60) and GEEA (6.67) where similar-level presentation issues exist. The MLLM asymmetry prevents a higher score (7.5+ range) but the core contribution is well-supported by the Non-name results.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>