## Summary

This paper proposes ARENABENCHER, a framework that automatically evolves existing benchmarks by generating harder variants of test cases through LLM-based rewriting while preserving the original "core ability." The key design choice is multi-model feedback: for each candidate rewrite, a random subset of models is probed, and candidates that *consistently* degrade performance across sampled models are selected, mitigating the single-model bias of prior augmentation methods. The framework also uses iterative refinement with in-context demonstrations. Evaluations on GSM8K, CommonsenseQA, and AdvBench (Harmful Behaviors) across 6 models (LLaMA3, Qwen3, Mistral, 1B–7B) show that updated benchmarks increase difficulty while maintaining reasonable alignment and fairness.

## Strengths

1. **Well-motivated multi-model aggregation.** The argument that single-model adversarial augmentation produces model-specific artifacts is clearly articulated (§1, §2), and the design of selecting candidates that depress performance across *multiple* sampled models is a principled response to that problem. The ablation comparing m=1 vs. m=3 (Tables 1 and 2) provides evidence that multi-model feedback produces larger difficulty gains than single-model feedback.

2. **Structured evaluation desiderata.** The four formal criteria — Separability, Fairness, Alignment, Difficulty (§3.5) — give the framework a clear quality vocabulary beyond simple accuracy drops. Having explicit definitions (e.g., fairness as inverse mean absolute deviation of failure counts) makes the evaluation more transparent than an ad-hoc approach.

3. **Human annotation and transparent failure case.** The human evaluation on 100 GSM8K samples (95% aligned, 96% correct) (§4.2) provides ground-truth validation beyond automated metrics. The paper also voluntarily presents and discusses a concrete failure case (Fig. 2) where the verifier accepted an unsolvable question — a degree of transparency that is uncommon and useful for understanding the method's limitations.

## Weaknesses

### Fatal
None.

### Major

1. **No empirical comparison against any prior benchmark augmentation method.** The Related Work section (§2) surveys multiple prior methods — MATH-Perturb (Huang et al., 2025), Automatic Robustness Stress Testing (Hou et al., 2025), PAIR (Chao et al., 2025), and simpler numerical perturbation approaches — and positions ARENABENCHER as addressing their limitations (single-model optimization, local perturbations). Yet **none of these methods appear as experimental baselines.** The only comparison in Tables 1 and 2 is between two variants of ARENABENCHER (m=1 vs. m=3). While this ablation shows that multi-model feedback helps relative to single-model feedback within the framework, it does not substantiate the claim that ARENABENCHER improves upon existing approaches from the literature. For example: does ARENABENCHER produce larger or more consistent difficulty gains than MATH-Perturb on the same models? Does the multi-model selection meaningfully improve fairness over a single-model adversarial baseline? Without at least one comparison, the paper cannot demonstrate that its contribution is meaningful *relative to the prior work it surveys*.

2. **Evaluation metrics overlap with the optimization objective, and no held-out model evaluation.** ARENABENCHER selects candidates by maximizing aggregate loss across sampled models, and then evaluates success using Difficulty (defined as 1 − best-model accuracy, directly related to loss) and Separability (variance of accuracies). These are essentially the same quantities the method optimizes for. Showing that optimized items score higher on their optimization target is a sanity check rather than a validation of generalizable improvement. The concern is compounded because **all 6 models** used for evaluation (Table 1) are drawn from the same pool used to provide loss feedback during generation. While models are *sampled* per test case (m=3 out of 6), the evaluation does not include any held-out model that was entirely excluded from the feedback process. This makes it difficult to assess whether ARENABENCHER discovers genuinely generalizable weaknesses or variants that are adversarially tailored to these 6 specific models.

### Minor

3. **Small and homogeneous model pool.** K=6 models from three families, all open-source, all in the 1B–7B range. Three model families is reasonable diversity, but the small sample size makes the √K heuristic (m=3) sample half the pool, which is far from the regime where ensemble diversity arguments typically apply. The paper invokes Breiman (2001) and Chen & Guestrin (2016) to justify √K, but those citations refer to random feature selection in tree ensembles — a setting with no established connection to sampling language models for benchmark scoring. The choice of m=3 for K=6 is reasonable heuristically, but the cited justification is decorative. Additionally, the paper states that models cover "parameter scales from 1B to 4B" (§4.1) yet Table 1 includes Mistral-7B-I (7B parameters), a minor factual inconsistency.

4. **No statistical uncertainty reported.** Results are presented as point estimates from a single run, with no confidence intervals, standard deviations, or significance tests. The pipeline involves multiple stochastic components (random model subset sampling, LLM-based generation with temperature>0, verification). Without multiple runs, the reader cannot assess whether reported differences (e.g., m=3 vs. m=1) are reliable.

5. **Alignment verification relies on the same model family that generates the updates.** GPT-4o is used for objective extraction, candidate generation, verification, and alignment measurement (§4.1, §3.5). High alignment scores (90–94% in Table 2) may partly reflect self-consistency rather than objective faithfulness. The human evaluation on 100 GSM8K samples is a partial corrective, but covers only one of the three benchmarks and is too small to fully mitigate this concern. The failure case in Figure 2 — where the verifier accepted an unsolvable question — concretely demonstrates that the verification pipeline can miss errors.

6. **Overclaim on "contamination-resilient" evaluation.** The conclusion states that ARENABENCHER is "a first step toward continuously evolving and contamination-resilient evaluation" (§5). The method generates harder test cases, which is a plausible strategy for staying ahead of contamination, but the paper does not test for contamination resistance, measure whether generated variants avoid leakage, or compare against any contamination-aware baseline. The framing overstates what is demonstrated.

### Trivial
- The Δ columns in Table 1 use both ↑ and ↓ arrows to indicate direction, which is conventional but the table header marks Acc with ↑ (higher is better) while ΔAcc uses ↓ (drop is good for difficulty) — a minor clarity issue.

## Nice-to-Haves
- **Hold-out model evaluation:** Evaluating the updated benchmarks on at least 1–2 models that were entirely excluded from the feedback pool (e.g., a larger model or a different model family) would address the most critical generalizability concern.
- **Ablation of iterative refinement:** The paper runs R=3 iterations but never ablates this. Reporting results with R=1 would clarify how much of the gain comes from iteration vs. single-pass generation with multi-model scoring.
- **Per-test-case success rate:** Reporting what fraction of original test cases could not be successfully updated (failed verification or yielded no valid candidate) would help assess the method's coverage.

## Removed Points

- **"Mistral-7B-I only has m=3":** This is factually incorrect; Table 1 shows both m=3 and m=1 rows for Mistral-7B-I. Removed as a factual error.
- **"Δ columns mix signs making table harder to read":** Removed as a formatting nitpick. The ↑/↓ convention is standard and unambiguous.
- **"The paper cannot substantiate its central claim... not an evidential gap that can be patched":** The missing baselines criticism is retained (as Major weakness 1), but the framing that it is an unaddressable structural gap is removed. Missing baselines are addressable with additional experiments.
- **Specific reference to "at time of writing" / "not yet released" concerns:** None present in the original review; noted for completeness.

## Novel Insights

None beyond the paper's own contributions. The review surfaces a consistent structural pattern: the paper has a well-motivated framework and reasonable methodology, but the evaluation design systematically avoids comparisons that would distinguish ARENABENCHER from the prior work it surveys. This is a common gap in single-system papers at the intersection of evaluation methodology and LLM-based generation, and the observation that the evaluation metrics are partially circular with the optimization objective is worth noting for future work in this space.

## Suggestions

1. **Add at least two baseline comparisons:** (a) a simple numerical perturbation baseline and (b) one prior LLM-based rewriting method (e.g., MATH-Perturb or Automatic Robustness Stress Testing) on the same benchmarks and model pool. Without this, the paper cannot substantiate its positioning.
2. **Include held-out model evaluation** on at least one model not in the feedback pool, to test whether the harder variants generalize beyond the specific 6 models used.
3. **Report results with multiple random seeds** (at least 3) with means and standard deviations for the main metrics in Tables 1 and 2, given the stochasticity of the pipeline.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>