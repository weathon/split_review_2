## Summary

This paper revisits multi-head LoRA architectures for multi-task learning, presenting three findings: (1) a simplified multi-head variant (M-LoRA) that removes routing and achieves high inter-head similarity outperforms complex diversity-promoting variants like R-LoRA; (2) a standard single-adapter LoRA with sufficiently increased rank is competitive with multi-component architectures, suggesting the complexity of multi-adapter designs may not be necessary; and (3) Align-LoRA, which adds an auxiliary KL-divergence or MK-MMD loss to align task representations in the shared down-projection space, improves multi-task generalization with zero inference overhead. The paper spans evaluations across Qwen2.5 (3B–14B), LLaMA2 (7B, 13B), and LLaMA3-8B.

## Strengths

1. **Clear counterexample to an active assumption (Section 3.2, Table 1, Figure 2).** The paper demonstrates that M-LoRA — a stripped-down multi-head variant with no routing and high inter-head similarity (median cosine similarity >0.85) — outperforms R-LoRA, which was explicitly designed to maximize head diversity. The "w/o Router" ablation on HydraLoRA (Table 1) isolates that dropout+summation is the mechanism, not just removing the router. This is a genuine empirical finding that challenges a premise the community has been building on.

2. **Honest practical constraint as motivation (Section 2.2, paragraphs on inference latency).** The paper correctly identifies that non-mergeable routers cost inference latency, which the multi-component MTL-LoRA literature has largely ignored. This is a valid practical concern that gives the paper's argument real-world grounding: Align-LoRA merges into the backbone with zero inference overhead.

3. **Broad model coverage.** Evaluations span Qwen2.5 (3B, 7B, 14B), LLaMA2 (7B, 13B), and LLaMA3-8B, which is more thorough than most LoRA papers and helps establish that the findings are not model-specific.

4. **Align-LoRA is simple and practical.** The method adds only a loss term and no parameters, and uses *fewer* trainable parameters than multi-component baselines while achieving higher average scores (Table 4: A-LoRA-K 50.28 vs R-LoRA 48.32 on Qwen2.5-7B; Table 5: 80.06 vs M-LoRA 78.51 on Qwen2.5-3B).

## Weaknesses

### Fatal
None.

### Major

1. **The mechanism driving Align-LoRA's gains is not established.** Align-LoRA adds an auxiliary loss (KL divergence or MK-MMD) that aligns task distributions in the latent space of the down-projection matrix **A**. This is equivalent to adding a regularizer. The paper does not include a baseline where a simpler regularizer (e.g., weight decay, dropout strength increase, or an L2 penalty on representation norms) is applied to a high-rank LoRA. Without such a control, the claim that *representation alignment specifically* (rather than generic regularization reducing overfitting to individual tasks) drives the improvements is unsubstantiated. The paper also lacks a control experiment where the alignment loss is applied to randomly permuted task labels — if the method still improves under that control, alignment of genuinely task-relevant representations cannot be the mechanism. This gap directly affects whether the paper's central claim about *why* Align-LoRA works is credible. (Section 5, Tables 4–5)

2. **No variance or statistical significance reported for any experiment.** Tables 1–5 show single numbers with no standard deviation, confidence intervals, or mention of multiple seeds. Given that many comparative margins are small (~0.5–1.5 points), it is unclear whether the observed differences are meaningful. For example, M-LoRA's 75.45 vs R-LoRA's 74.67 (Table 1) is a ~0.8 point gain across 5 tasks where individual task margins vary; without variance, the reader cannot assess significance. This is a notable gap for a paper making many comparative claims.

### Minor

1. **The "high-rank single LoRA" claim is slightly over-stated.** The abstract says a standard single-adapter LoRA "also achieves highly competitive performance," which is accurate. But the introduction (line 25) states it can "match or even outperform these intricate multi-component variants." The actual evidence (Tables 2–3) shows that the high-rank single LoRA is competitive with R-LoRA, HydraLoRA, LoRAHub, and LoRA MoE, but it *consistently trails M-LoRA* (the paper's own simplified baseline) on 7B models (Table 2: 42.21 vs M-LoRA 42.83 on LLaMA2-7B; Table 3: 49.51 vs M-LoRA 49.74 on Qwen2.5-7B). Since the paper's own arc moves from M-LoRA to the question "is multi-head even necessary?", the fact that a high-rank single LoRA cannot match M-LoRA weakens the rhetorical force, though the claim about other multi-component methods holds. (Section 4, Tables 2–3)

2. **The theoretical analysis (Section 5.3) is a standard MTL bound with no LoRA-specific content.** The bound R_MTL(f) ≤ (1/M) Σ R_train(f; D̂_i) + (λ/M) Σ_{i<j} Δ(D_i, D_j) + O(√(log(1/δ)/n_total)) is a generic multi-task/domain adaptation bound (traceable to Ben-David et al., 2006; Mansour et al., 2009). It does not incorporate any property of LoRA — not the low-rank structure, not the parameter budget, not the A/B decomposition. The paper claims to "derive a novel generalization bound for MTL" (line 255), which overstates the novelty. The bound essentially restates: if you reduce distribution discrepancy, the bound tightens. Removing this section would not weaken the paper's empirical contribution.

3. **The connection between M-LoRA's natural similarity and Align-LoRA's explicit alignment is underdeveloped.** If M-LoRA already achieves >0.85 median inter-head similarity naturally, and Align-LoRA improves performance by enforcing alignment, it is unclear whether Align-LoRA produces *more* aligned representations than M-LoRA or does something qualitatively different. The paper mentions feature visualizations (Appendix I.1) and shows that alignment can enhance even multi-head architectures (M-LoRA+Align, Appendix I), but this analysis is deferred to the appendix rather than presented in the main text. Without it in the main body, the connection between the two core findings remains associative rather than causal. (Section 5, comparison to Section 3)

4. **A-LoRA-M (MMD variant) has mixed performance.** In Table 5 (Qwen2.5-3B), A-LoRA-M scores 78.35, which is *lower* than M-LoRA's 78.51. On Qwen2.5-7B, A-LoRA-M (82.31) is below M-LoRA (82.46). This undercuts the claim that "the principle of aligning representations is broadly applicable" and that both instantiations are similarly successful. The choice of alignment metric matters substantially, and this should be discussed as a limitation. (Section 5.2, Table 5)

5. **The experimental protocol changes between sections in ways that are never reconciled.** Section 3 uses a 5-task benchmark with own test sets. Section 4 switches to the HydraLoRA protocol (Flanv2 training → BBH evaluation). Section 5.2 uses the 5-task set → BBH (Table 4) and an 8-task benchmark (Table 5). Because the training distributions differ, it is unclear whether the rank-scaling findings from Section 4 (Flanv2) carry over to the alignment findings in Section 5 (5-task set). A consistent protocol throughout would make the cumulative argument stronger.

### Trivial
None worth listing beyond the above.

## Nice-to-Haves

- Adding a regularized LoRA baseline (e.g., weight decay, L2 penalty on representation norms) to distinguish alignment-specific effects from generic regularization.
- Adding a control experiment with alignment applied to randomly permuted task labels.
- Reporting variance (e.g., standard deviation across seeds) for all main tables.
- Moving the representation visualization (Appendix I.1) to the main text to directly support the mechanism claim.
- Removing or substantially rewriting the theoretical section to either incorporate LoRA-specific structure or state it as a standard bound with appropriate citations.
- Acknowledging that A-LoRA-M's mixed performance limits the generality claim about alignment metrics.

## Removed Points

- **"The bound reuses the symbol λ from the loss function (Eq. 6), but it is unclear whether the bound's λ is the same as the method's hyperparameter."** — Removed because this is a minor notation issue that is clear in context. The bound uses λ generically for the trade-off weight, and the paper does not conflate the two uses in a misleading way.

- **"Table 4 training setup ambiguity: not specifying which modules LoRA is applied to"** — Removed because the critic acknowledges these details are in the appendix, and the main paper needs to remain concise. This is a standard organizational choice, not a weakness.

- **"M-LoRA rank clarification: the paper could be clearer that total parameter count differs"** — Removed because Tables 2-3 already report "% Param" for each method, making the parameter count differences transparent.

- **Critic's claim that the paper's strongest performing method (Align-LoRA-K) is either multi-head (M-LoRA) or a single adapter with alignment loss, and "neither is a pure 'just increase the rank' approach"** — Removed because the paper does not claim Align-LoRA is a "pure increase rank" approach. Align-LoRA is presented as a separate validation of the representation-alignment hypothesis, not as evidence for the rank-scaling finding.

## Novel Insights

The reviewer insight about the tension between M-LoRA's naturally high similarity and Align-LoRA's explicit alignment is genuinely novel and not addressed fully by the paper as written. If M-LoRA already converges to >0.85 similarity, what does the alignment loss add? The paper mentions M-LoRA+Align in the appendix but does not develop this comparison in the main text, leaving the relationship between the two findings ambiguous. A second novel observation is that the MMD variant (A-LoRA-M) underperforms M-LoRA on the 8-task benchmark while the KL variant succeeds — this asymmetry is important and suggests the alignment metric choice is consequential, but the paper treats both variants as broadly successful.

## Suggestions

- Add a regularized LoRA baseline (e.g., increased weight decay or an L2 penalty on **A**-space representation norms) to Tables 4–5. If Align-LoRA still outperforms this baseline, the mechanism claim is supported; if not, the paper should reframe the contribution as "an effective auxiliary loss for multi-task LoRA" rather than "representation alignment specifically drives gains."
- Report standard deviations or confidence intervals for all main results (Tables 1–5). Even reporting the range across 2–3 seeds would substantially improve credibility.
- Move the representation visualization (Appendix I.1) and the M-LoRA+Align results into the main paper to connect the two core findings.
- Calibrate the language in the introduction (line 25) from "match or even outperform" to "is competitive with" when referring to the high-rank single LoRA relative to multi-component variants, since it consistently trails M-LoRA.
- Either remove the theoretical section or add a bound that actually exploits LoRA's low-rank structure (e.g., connecting rank to Rademacher complexity of the function class).

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>