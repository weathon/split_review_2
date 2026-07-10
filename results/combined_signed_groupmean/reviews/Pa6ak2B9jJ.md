Now I have a clear picture. Let me compile the final review.

## Summary

This paper proposes AUTO-RT, an RL-based framework for automatic jailbreak strategy exploration in LLMs. The key idea is to decompose attack generation into a strategy generator and a repurposer, enabling hierarchical search. Two techniques — Dynamic Strategy Pruning (DSP) and Progressive Reward Tracking (PRT) with a first-inverse rate (FIR) heuristic — address sparse-reward exploration. Experiments across 16 white-box and 2 black-box LLMs show substantial ASR improvements over baselines.

## Strengths

- **Well-motivated problem framing (Section 1, lines 15-28).** The exploitability-vs-severity distinction is a genuine conceptual contribution, with concrete examples (Grandma's Exploit, Past-Tense Attack) that directly motivate the strategy-level formulation rather than being rhetorical.

- **Hierarchical decomposition of attack generation (Section 2.2, Equation 2).** Separating the attack model into a strategy generator (AM^g) and a rephraser (AM^r) is a clean architectural choice that enables strategy-level exploration beyond fixed-template approaches.

- **FIR metric for downgrade model selection (Section 2.3.3, lines 109-121).** The first-inverse concept is a genuinely novel heuristic. Figure 4 provides reasonable evidence across 6 target models that the FIR-indicated model produces better attack results than arbitrarily chosen ones.

- **Extensive model coverage (Table 1).** Testing across 16 white-box LLMs spanning multiple families (Llama, Mistral, Yi, Gemma, Qwen, R2D2) is substantially broader than typical red-teaming papers and supports consistency evaluation across varying safety alignments.

- **Ablation study cleanly separates DSP and PRT contributions (Table 2).** The pattern that PRT has a larger effect on DeD while DSP has a larger effect on SeD is coherent and supports the design rationale.

## Weaknesses

### Major

- **Ambiguous evaluation metric with potential test-set leakage (Section 3.1, lines 127, 147-149).** The paper defines dataset splits as $\mathcal{T}_{\text{tm}}$ (training) and $\mathcal{T}_{\text{ts}}$ (test) at line 127, but then uses the undefined notation $\mathcal{T}_{\text{st}}$ in the primary effectiveness metric (Equation 6): the "average ASR of the top 100 strategies with the highest ASR on $\mathcal{T}_{\text{st}}$." The top-100 selection and evaluation are both done on $\mathcal{T}_{\text{st}}$. If $\mathcal{T}_{\text{st}}$ refers to the test set (a natural reading given the proximity to $\mathcal{T}_{\text{ts}}$), this constitutes test-set leakage: strategies are cherry-picked for test-set performance and evaluated on the same set, producing an optimistic upper bound. This would inflate AUTO-RT's reported advantages over baselines that were not afforded the same post-hoc selection. The notation must be clarified and the metric redesigned if leakage is confirmed.

- **No variance or statistical significance for central results (Table 1).** Table 1 reports single ASR values with no standard deviations, confidence intervals, or replication information. Given stochastic processes (PPO training, strategy sampling, rephrasing), the reader cannot assess stability. Some differences are small (e.g., AUTO-RT's 15.00% vs RL's 14.55% on Llama 3 8B — a ~3% relative difference). The abstract claims improvement "by up to 16.63%" with no confidence interval. Standard deviations over at least 3 random seeds are needed for the main results.

- **Missing SeD value in human-based comparison (Table 3).** AUTO-RT's Semantic Diversity (SeD) value is blank in Table 3, making the comparison with AutoDAN, Human Template, and Past-Tense incomplete. Without this value, the diversity claim relative to human-crafted methods in the comparison is partially unevidenced.

### Minor

- **Abstract claim "by up to 16.63%" unanchored (lines 9, 34).** This figure appears in the abstract and introduction but is never explicitly tied to a specific model or baseline comparison in the main text or tables. The largest improvement visible in Table 1 (Gemma 2 2B: 48.15% vs 7.49% = 40.66pp) is far larger, making the 16.63% value untraceable.

- **DeD > ASR in black-box setting unexplained (Table 4).** For Llama 3 70B, DeD (15.00) exceeds ASR (14.88), meaning applying a defense does not reduce attack success. This unusual result is not discussed.

- **Non-potential-based reward shaping acknowledged but not analyzed (Section 2.3.3, line 109).** The paper correctly notes PRT "does not follow the potential-based function structure," which in standard RL theory means the optimal policy can change. The defense (a heuristic about unsafe subsets being nested) is plausible but no theoretical or empirical analysis is given for when/n whether the optimal policy is preserved.

- **Notation inconsistencies across metric names.** The paper uses ASR$_{\text{st}}$ (Eq. 6), ASR$_{rst}$ (Table 1), ASR$_{att}$ (Table 2, Figure 3), and ASR$_{tot}$ (Table 4) for related concepts without explaining whether they differ, creating confusion.

- **R2D2 underperformance qualified but could be discussed more deeply (Table 1, lines 158-185).** AUTO-RT (12.45%) underperforms Few-Shot (27.18%) on R2D2. The paper acknowledges this but offers no analysis of why, limiting insight into the method's boundaries.

### Trivial

- **No concrete example of discovered strategies.** The paper motivates with "Grandma's Exploit" and "Past-Tense Attack" but never shows what a strategy discovered by AUTO-RT looks like. A qualitative table would strengthen the "strategy-level exploration" claim.

## Nice-to-Haves

- A table of representative attack strategies discovered by AUTO-RT, showing the strategy text, rephrased query, and target model response.
- Downgrade model construction details (amount of toxic data, fine-tuning procedure, ICL setup) for reproducibility.
- A note on total computational cost (e.g., total GPU hours for creating 6 intermediate models + running AUTO-RT for each target).

## Removed Points

These points from the input review were filtered out:
- "R2D2 as counterexample to 'consistently achieves highest ASR' claim": The paper acknowledges R2D2 explicitly ("a sampling-based method outperforms others") and qualifies the claim ("across a wide range"), making this a misreading — the paper already caveats this.
- "Missing experimental comparison with PAIR/TAP/AutoDAN-turbo": The paper discusses these text-feedback methods in Related Work and explains the distinct feedback paradigm. Scope boundary, not a missing baseline.
- "Llama-Guard2-8B accuracy not discussed": Generic classifier concern applicable to nearly all red-teaming work using classifiers.
- "Theoretical claim about optimal policy preservation citing Sun et al. (2021)": Standard citation; the concern is overly nitpicky for an empirical paper.
- "Transition from Eq. 1 to Eq. 2 not discussed": Highly minor formulation detail that does not affect the paper's claims.
- "Severity not directly measured": The paper frames severity as motivation but uses standard binary ASR in evaluation — a noted scope limitation rather than a flaw.
- "Downgrade model construction details insufficiently specified": The paper references Appendix B for details; the appendix was stripped by the parser. This is likely addressed in the full submission.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Clarify the $\mathcal{T}_{\text{st}}$ notation immediately.** State explicitly which dataset split the top-100 selection uses. If it uses the test set, redesign the evaluation (e.g., select on the training set or use all discovered strategies without selection). If it uses the training set, fix the notation and state this clearly.
2. **Report variance.** Run at least 3 seeds for the main comparison (Table 1) and ablation (Table 2), reporting mean ± std.
3. **Fill in the missing SeD value** in Table 3 and explain the across-model aggregation method for the aggregate ASR.
4. **Anchor "by up to 16.63%":** specify which model and baseline comparison this figure refers to, or remove it from the abstract.
5. **Provide qualitative examples** of discovered attack strategies in the main text.

Now, for calibration: I examined 10 calibration anchors.

**Round-1 bracket:** Based on comparison with anchors, the narrowest plausible score range is 4.5–6.5. The paper is clearly stronger than the 4.25 (Reject) and 5.25 (Reject) anchors (which had fundamental novelty/comparison failures that the current paper lacks) but weaker than the 8.00 Curiosity-driven Red-teaming anchor (which had clean, variance-reported evaluation and minor weaknesses only).

**Narrowing to final score:** Comparing scored items:

- The 5.75 "Universal Jailbreak Backdoors" anchor (Accept) had weaknesses including missing baselines (-9.96) and impracticality concerns. The current paper has similar-magnitude weaknesses (test-set ambiguity at -9.98, no variance at -10.00). However, the current paper has broader model coverage and more novel technical depth. Score: ~5.5.
- The 6.25 "Efficient Jailbreak via MAB" anchor (Accept) had severe weaknesses: no comparison with existing methods (-9.85, -9.96), weak theory (-10.00), poor presentation (-9.99). Despite this, it was accepted at 6.25. The current paper has fewer issues and better evaluation, suggesting it could score at least as high — but the test-set leakage ambiguity is a serious concern that the MAB paper didn't have. Score: ~5.5.
- The 4.25/5.25 reject anchors all had fundamental novelty or methodological problems that the current paper doesn't share.

My final score is **5.5**. The paper has genuine contributions (hierarchical decomposition, FIR metric) and evaluation breadth. However, the ambiguous evaluation metric (potential test-set leakage), missing variance, and missing SeD are significant concerns that must be resolved before acceptance. The core work is publishable, but the evidence in its current form does not fully support the strength of the claims.

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>