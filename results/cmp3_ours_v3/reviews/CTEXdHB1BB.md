## Summary

This paper introduces CANON (Conditional advaNtage estimatiON), a method for incorporating metric-based priors (e.g., entropy, response length) into advantage estimation for RLVR training of LLMs without prescribing a directional preference (higher-is-better or lower-is-better). CANON regroups sampled responses by a metric value into two equal-sized groups, then computes inter-group (cross-group) and intra-group (within-group) advantages. The paper shows that DR.GRPO is a special case (μ=0.5), proves that the inter-group advantage selectively amplifies the grouping metric without amplifying independent metrics (Theorem 2), and demonstrates empirically across three LLMs on math and logic reasoning tasks that CANON variants outperform prior methods, with notable efficiency improvements on the performance–cost Pareto frontier.

## Strengths

- **Clean, well-motivated reformulation (Sections 4.1–4.2).** The core idea of regrouping responses by a metric then computing inter-/intra-group advantages is simple and directly addresses a genuine limitation of prior work: hand-crafted directional penalties (e.g., "higher entropy is better") require careful tuning and can fail when the optimal direction varies. The unification showing DR.GRPO as the μ=0.5 special case (Eq. 7) is elegant and connects CANON cleanly to existing practice.

- **Selective amplification guarantee (Theorem 2, Section 4.2).** Proving that grouping by metric c₁ does not amplify the influence of an independent metric c₂ is the right theoretical property for a method whose claim is to amplify the target metric without biasing other factors. This meaningfully distinguishes CANON from naive advantage scaling.

- **Strong efficiency results (Section 5.3, Table 3, Figure 4).** The Pareto frontier analysis is the most compelling empirical contribution. CANON-Eff dominates baselines across the performance–cost trade-off, and the stability observation (Length Reward (+) collapses from 54.8 to 22.5 when its coefficient moves from 0.004 to 0.005, while CANON-Eff degrades gracefully) is a concrete practical advantage. The 2.63× performance gain in low-token-budget scenarios is striking and practically significant.

- **Interpretable training dynamics analysis (Figure 2, Section 5.1).** The decomposition of Inter-group advantage as exploitation (entropy decrease, rapid math gains) and Intra-group advantage as exploration (entropy increase, later logic gains) provides an intuitive, empirically supported explanation for why the scheduling works.

## Weaknesses

### Fatal
None.

### Major
- **Radar chart (Figure 3) numbers do not match the main results tables, and no explanation is provided.** The data table embedded in Figure 3 (lines 212–225) presents values inconsistent with Tables 1 and 2. For Qwen-7B, the radar chart shows DR.GRPO Math=57.6 (which equals CANON-Inter Entropy's Math Acc in Table 1, *not* DR.GRPO's 55.7), CANON-Inter Math=45.0 (Table 1: 57.6), CANON-Intra Math=35.0 (Table 1: 54.7), and CANON-Dynamic Math=45.0 (Table 1: 56.7). For Llama-8B, the radar chart's DR.GRPO values (22.6, 18.9) match the *Cosin-First-Inter-Later-Intra* variant in Table 2, not DR.GRPO's actual numbers (22.0, 14.9). The caption says "Performance is measured on a scale from 0 to 100" but does not define any normalization, while the data table column headers say "(%)". The neat multiples of 5 across all CANON variants further suggest rounding or a normalization procedure that is not disclosed. Since Figure 3 is the headline visualization for the claim "CANON-Dynamic achieves the highest performance across both tasks for all models," this discrepancy undermines trust in the central empirical claim and must be resolved.

- **No measure of variance or statistical significance is reported for any result.** Tables 1–3 report only point estimates. The gains over DR.GRPO are modest in several cases (e.g., CANON-Inter Entropy on math: +1.9 points average). Several benchmarks (AIME 24/25, AMC) have very few problems and are reported as Avg@10, which likely has high variance. Without confidence intervals, error bars, or multi-seed results, the reader cannot assess whether the reported improvements are systematic or within the noise of a single run. This is especially relevant for the scheduling strategies (Section 5.2), where different strategies are selected post-hoc for different models, raising the possibility of selection-vs.-variance confound.

### Minor
- **Model-specific scheduling selection weakens the generality claim.** As reported in Section 5.2, different scheduling strategies are used for different models: Cosin-First-Inter-Later-Intra for Qwen-7B and Llama-8B, but First-Inter-Later-Intra for Qwen-1.5B. The justification ("its training accuracy range (0–0.6) aligns well with its learning progress") is post-hoc, and the paper notes that accuracy-based scheduling for Qwen-7B and Llama-8B "trigger[s] excessive exploration and consequently lead[s] to suboptimal final performance." This means that CANON-Dynamic, in its best-performing form, requires per-model tuning, and the paper provides no principled criterion for selecting a strategy. While the individual CANON-Inter/Intra variants need no such tuning, this limitation should be acknowledged more explicitly.

- **The ablation comparing CANON against direct numerical scaling (A = A * 2) in Table 4 is a weak straw man.** Showing that uniform 2× scaling fails does not isolate whether CANON's effectiveness comes from the regrouping operation specifically, as opposed to any non-uniform amplification scheme. A more informative baseline would be multiplying the advantage by a monotonic function of the metric (e.g., A * sigmoid(metric)) or using the metric as an additive offset (A + β · normalized_metric). These would test whether CANON's specific regrouping design is genuinely necessary or whether any metric-sensitive reshaping would capture similar gains.

- **Hyperparameter sensitivity of α is not explored.** The paper uses α ∈ {0.5, 0.7, 0.8, 0.88, 0.96} for the Pareto analysis but does not discuss how performance varies with α within a narrow range or whether the method is robust to small changes. Similarly, μ is studied primarily at the endpoints (0, 0.5, 1) in the main experiments.

- **Claim that Length-based CANON-Inter "maintains nearly unchanged performance" (55.7 vs. 55.3) is too strong without variance estimates.** The 0.4-point drop could be within noise, and the paper does not report variance to support this claim.

### Trivial
None.

## Nice-to-Haves
- Including DAPO as a comparison baseline would strengthen the positioning, since DAPO is cited as influencing the training setup but is not directly compared.
- The ZebraLogic subsets (Mid, Large, XLarge) are defined by solution space size thresholds, but the paper does not report how many examples fall into each subset, making it hard to assess reliability of the "Acc" columns.
- Theorem 1's condition requires equal-sized groups. The paper uses this in practice, but it would be informative to characterize the amplification factor when groups are not perfectly balanced.

## Removed Points
These points are flagged to be removed, treat them with caution:
- **Missing related work.** Per policy, we cannot verify whether missing citations exist. Removed.
- **Formatting/style nitpicks.** Per policy, parser artifacts are not author errors. Removed.
- **Criticism about "not yet released" code/models.** The paper cites its code availability; per policy, cited entities are assumed to exist. Removed.
- **"Theorem 1 condition is restrictive" framed as a fatal limitation.** The paper operates in the equal-sized-group regime, so this is not a practical problem. The point was demoted to a nice-to-have.
- **Criticism about "the paper claims state-of-the-art but doesn't compare against DAPO."** DAPO is a training framework whose key technique (clip-higher) the paper adopts, not an advantage estimation method. Demoted to nice-to-have.

## Novel Insights
The harsh critic's careful cross-referencing of the radar chart data against Tables 1–2 reveals a data consistency problem that a surface-level reading would miss: the headline visualization uses numbers that systematically differ from the paper's own result tables in ways that cannot be explained by rounding alone. Additionally, the observation that the direct numerical scaling baseline in Section 6 tests uniform amplification (which no one would expect to work) rather than any non-uniform metric-conditioned scheme identifies a gap in the paper's ablation strategy that goes beyond a standard presentation fix.

## Suggestions
- Reconcile the radar chart (Figure 3) data explicitly with Tables 1–2, or clearly state the normalization procedure if one was used. If normalization was applied, show raw numbers alongside normalized ones and explain why normalization was necessary.
- Report variance across at least 3 seeds for the central comparisons (DR.GRPO vs. CANON-Inter/Intra, Table 1). This is standard practice in RL experiments and would substantially increase confidence in the reported gains.
- Include a broader set of metric-conditioned advantage baselines in the ablation (e.g., A * sigmoid(metric), A + β·metric) to isolate the benefit of the regrouping design over other non-uniform amplification schemes.
- Explicitly acknowledge the model-specific scheduling limitation as a limitation and, if possible, provide guidance for practitioners on how to select a scheduling strategy for a new model.
- Report the number of examples in each ZebraLogic subset to help readers assess result reliability.

**Calibration Details:**
- Round 1 bracket: 5–6 (between borderline reject and borderline accept).
- Anchors inspected:
  - *On Designing Effective RL Reward at Training Time for LLM Reasoning* (5.17, Reject) — adjacent topic; less novel method, similar rigor concerns. Our paper has a more novel method but the radar chart issue is a bigger presentation problem.
  - *Towards Learning to Reason at Pre-Training Scale* (5.50, Reject) — similar-level contribution with systematic analysis but incomplete solution. Our paper has more conclusive results but a presentation inconsistency.
  - *Language Model Self-improvement by RL Contemplation* (6.00, Accept) — less novel method (similar to RLAIF), cleaner presentation. Our paper has a more novel method but the radar chart issue reduces confidence.
  - *Vanishing Gradients in RFT* (6.25, Accept) — strong theoretical contribution with clean experiments. Our paper has comparable theory but a more concerning data presentation issue.
  - *Skill or Luck? Return Decomposition* (6.25, Accept) — clean theory, limited experiments (MinAtar only). Our paper has more extensive experiments but the visualization inconsistency.
- Final score 5.5: The paper has genuine novelty and strong efficiency results, but the unexplained discrepancy in the headline visualization and the absence of variance reporting prevent a higher score. The contribution is on the borderline — curable with revisions.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>