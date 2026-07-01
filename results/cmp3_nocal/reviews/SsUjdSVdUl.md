Now let me write the final review.

## Summary

This paper diagnoses a key failure mode in RL-based training of critique models: optimizing solely on indirect rewards from actor refinement (e.g., refinement correctness) improves helpfulness but leaves discriminability under-optimized, producing conservative or aggressive critics. It proposes Critique-RL, a two-stage RL approach that first optimizes discriminability via direct correctness-matching rewards (Stage I), then optimizes helpfulness while preserving discriminability through a retained discrimination reward and KL regularization toward the Stage I model (Stage II). Experiments on math reasoning tasks with Qwen2.5-3B/7B show consistent improvements over SFT, STaR, Retroformer (PPO), and CTRL (GRPO) baselines, with ablations confirming the contribution of each stage.

## Strengths

- **Well-motivated problem diagnosis (§4.1, Figure 3).** The paper identifies a concrete and non-obvious failure mode: indirect reward signals from actor refinement do not adequately optimize discriminability. The training dynamics visualization in Figure 3 cleanly demonstrates this — discriminability for originally-correct and originally-incorrect responses diverges over training, producing either conservative or aggressive critics. This is a genuine finding supported by evidence on the page.
- **Clean, principled two-stage solution.** The method directly follows from the diagnosis: Stage I optimizes discriminability via direct reward, Stage II optimizes helpfulness while anchoring discriminability via retained r_dis and KL regularization toward the Stage I model. The ablations (Table 3) confirm that removing either stage or the discrimination-preserving regularization hurts performance — exactly the evidence the method's logic demands.
- **Consistent experimental results across models and tasks.** The method outperforms all baselines on every in-domain dataset for both 3B and 7B models (Table 1) and on both OOD datasets (Table 4). Gains are not marginal: e.g., on MATH with 7B, Critique-RL achieves 58.40% vs. the best baseline (CTRL) at 53.86% — a 4.54 pp improvement. The iterative training results (Table 2) show continued improvement across iterations.
- **Thorough ablation study (Table 3).** The ablations systematically isolate Stage I alone, Stage II alone, Stage II without discrimination regularization, and Stage II with alternative reward functions. Results confirm the core thesis: both stages matter, and the discrimination-preserving regularization in Stage II is crucial.

## Weaknesses

### Fatal
None.

### Major

- **No reported variance or multi-seed results.** All tables (Tables 1–4) report single numbers with no standard deviations, confidence intervals, or any mention of multiple runs. RL training for LLMs is known to be noisy; differences of 1–3 pp between methods could fall within typical variance, especially for the 3B model. For example, on MATH (3B), the 2.46 pp advantage of Critique-RL (48.60) over CTRL (46.14), and on TheoremQA (7B) the 0.3 pp advantage (21.4 vs. 21.1), are presented without any indication of statistical reliability. This is a significant evidential gap for an RL paper that asks readers to accept fine-grained rankings between methods. The paper states it "report[s] best results" (§5.1), which further obscures run-to-run variability.

- **RL algorithm confound between method and baselines.** Critique-RL uses RLOO, while Retroformer uses PPO and CTRL uses GRPO (§5.1). The paper does not control for the base RL algorithm when comparing against these baselines, making it unclear how much of the observed improvement comes from the two-stage design vs. RLOO being a better-suited algorithm for this setting (e.g., RLOO may handle sparse reward structure better than PPO/GRPO). The ablation study (Table 3) partially alleviates this by comparing reward designs within the RLOO framework, but the headline comparisons against Retroformer and CTRL remain confounded. A "RLOO + refine reward only" baseline would be needed to isolate the two-stage contribution.

### Minor

- **Abstract and introduction frame gains against the weakest baseline.** The reported "9.02% gain on in-domain tasks and 5.70% gain on out-of-domain tasks" are absolute percentage point improvements over the "No Critic" baseline (computed from Table 1). Against the strongest prior RL method (CTRL), the average improvement for 7B in-domain is approximately 3.90 pp. Framing against "No Critic" inflates the apparent contribution relative to prior work; the abstract should also report gains against the strongest baseline.

- **Method requires an oracle verifier during training.** The reward signals r_dis (Stage I) and r_refine (Stage II) both depend on r_oracle, which requires ground-truth answer matching. This limits the method as presented in the main paper to tasks with verifiable answers. The paper acknowledges this limitation and cites summarization experiments in the appendix, but the core contribution is for settings where ground-truth rewards are available during training — an honest scope limitation worth noting.

- **SFT critique data filtering is underspecified.** The paper states "We filter the critique data based on the correctness of refinement to ensure the quality" (§4.1) but does not specify the exact filtering criterion, what proportion of data was kept, or how this affects the SFT initialization. If only critiques leading to correct refinements are kept, this biases the initialization toward responses where the actor can improve, which may affect subsequent RL behavior. Clarification would strengthen confidence in the experimental setup.

- **The reward asymmetry in Stage II is not discussed.** In Eq. 9, r_refine contributes up to 1.0 to the total reward while r_dis contributes at most β₁=0.2 (set to 0.2). This 5× asymmetry means Stage II is dominated by the refinement signal. The ablation confirms that removing discrimination components hurts, so the regularization is doing something — but the paper does not discuss whether the relative weighting matters or how β₁ was chosen.

### Trivial
None.

## Nice-to-Haves

- Report results over 3+ random seeds with means and standard deviations. If computational cost is prohibitive, report results from 2 runs and note the range.
- Run at least one baseline using RLOO with the same reward function used by Retroformer/CTRL to isolate the two-stage design contribution from the RL algorithm choice.
- Frame headline gains against the strongest prior baseline (CTRL or Retroformer) alongside the "No Critic" comparison in the abstract and introduction.

## Removed Points
These points were flagged for removal from the input review; they are listed here for completeness but should not factor into the evaluation.

- **Inference compute scaling figure labeling error.** The harsh critic flagged a duplicated "w/o Critique-RL (3B)" label in Figure 1's table. The caption explains "@2k and @3k indicating sampling amounts that are 2 times and 3 times the x-axis value," and the main text (§6) describes the comparison clearly. The labeling duplication is a parser-rendering artifact. **Removed per rule on parser artifacts.**
- **Missing β₂ hyperparameter value.** The harsh critic noted β₂'s value is not explicitly stated. The main KL coefficient (0.01) and β₁=0.2 are provided. The appendix likely documents β₂. **Removed per rule on undisclosed hyperparameter nitpicks.**
- **STaR baseline implementation details.** The harsh critic noted missing details about STaR iterations and filtering. These are standard details the appendix likely contains. **Removed per rule on missing appendix content.**
- **Oracle verifier generality criticism tied to appendix unavailability.** The original claim that "the claim of generality to open-ended tasks cannot be evaluated from what is presented" was reframed to focus on the scope limitation (oracle verifier required during training) rather than the unavailability of appendix content. **Removed per rule on missing appendix content.**

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Add variance estimates from multiple runs to all main results tables.
- Include a controlled baseline (RLOO + refine-only reward) to disentangle the two-stage design from the RL algorithm choice.
- In the abstract and introduction, report improvements against the strongest prior baseline (CTRL) as well as against "No Critic."
- Clarify the SFT critique data filtering criterion and the proportion of data retained.
- Discuss or ablate the β₁ weighting choice for the discrimination reward in Stage II.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>