## Summary

This paper targets the under-explored problem of unsafe intermediate reasoning in Large Reasoning Models (LRMs)—harmful content that persists in chain-of-thought traces even when final responses are safe. The authors first document this gap systematically across existing safety-aligned LRMs (RealSafe, STAR), then identify two critical phenomena in reasoning dynamics: *safety triggers* (steps after which continuation is near-certain to be safe) and *compliance cues* (steps strongly correlated with unsafe continuations, Pearson R=0.85). Based on these insights, they propose **Intervened Preference Optimization (IPO)**, which replaces compliance cues with sampled safety triggers to construct preference pairs, then applies partial-trajectory DPO at the divergence point. IPO achieves substantial reductions in reasoning harmfulness across three LRM families (DS-8B, DS-7B, Qwen3-8B) and multiple adversarial benchmarks while preserving reasoning capability, and is computationally more efficient than RL-based alternatives.

## Strengths

1. **Well-documented problem identification.** The paper convincingly demonstrates that existing safety-aligned LRMs exhibit a large gap between response safety and reasoning safety. For example, RealSafe-7B has 0.0% harmful answers on JailbreakBench but 22.0% harmful reasoning; on WildJailbreak the gap is 2.4% vs 52.2% (Figure 2). This establishes a real, non-trivial deficiency.

2. **Novel empirical insights into safety dynamics.** The identification of *safety triggers* (reasoning steps where continuation safety probability jumps to ~100%) and *compliance cues* (steps with Pearson R=0.85 correlation with unsafe continuations) in Sections 3.1–3.2 is genuinely informative and goes beyond prior qualitative observations. The CSR metric is well-defined, and the finding that safety is concentrated at a few critical tokens rather than uniformly distributed is non-obvious and directly actionable.

3. **Clean intervention experiment (Section 3.3).** Showing that replacing the first compliance cue with a safety trigger reduces harmful continuation from 100% to ~60% in a single substitution, and to ~15% after 5 iterative interventions (Figure 6), provides direct causal evidence that the identified dynamics are causal, not merely correlational. This experiment is the paper's strongest piece of evidence motivating the IPO method.

4. **Strong results across diverse settings.** Table 2 shows IPO achieving the lowest harmful reasoning ratios on StrongReject and WildJailbreak across all three model families. The improvements are substantial in absolute terms: e.g., on WildJailbreak reasoning, DS-8B goes from 82.4% (base) to 23.4% (IPO), versus 36.3% (best baseline, GRPO). These gains come with preserved or improved reasoning benchmarks (AIME, MATH, GPQA, HumanEval), demonstrating a favorable safety-utility trade-off.

5. **Computational efficiency.** IPO requires ~14 generations per prompt and ~40 minutes training time, versus GRPO's ≥40 generations and >2 hours (Section 4.3), a practical advantage for adoption.

6. **Robustness analysis on compliance cue detectors.** Table 3 shows stable IPO performance when the compliance cue detector is replaced with DeepSeek-R1 or even DS-8B itself (GPT-4o: 13.7% avg harmful; DeepSeek-R1: 13.6%; DS-8B: 19.4%), mitigating concerns about detector dependency.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **GPT-4o serves both as compliance cue detector and safety evaluator, creating an incompletely addressed confound.** The safety evaluation (line 42) and compliance cue detection for training data (line 189) both use GPT-4o. The ablation in Table 3 varies the detector during *training* (showing robustness), but the *evaluation* still uses GPT-4o for all conditions, including the detector-ablation rows. Therefore the reported results reflect GPT-4o's safety judgments rather than independently validated safety. The paper validates the detector against human annotation (>80% consistency, line 193), and varying the detector during training still works—these partially mitigate the concern. Still, a human evaluation on a subset of outputs comparing IPO against the strongest baseline would substantially strengthen confidence that the measured gains are not artifacts of the judge.

2. **Safety trigger pool construction is underspecified.** The trigger pool is identified from 30 JailbreakBench prompts (line 138), from which "six representative safety triggers" are sampled for IPO training (line 209). The paper omits: (a) how many unique triggers were identified in total, (b) the criteria for selecting the six "representative" triggers, (c) whether triggers are domain-specific or generalize across attack types, and (d) sensitivity to the number of triggers. This introduces an opaque human selection step into an otherwise automated pipeline, limiting reproducibility.

3. **IPO combines multiple design elements whose individual contributions are not fully ablated.** The method includes: (a) compliance cue detection, (b) safety trigger intervention, (c) partial-trajectory DPO, (d) an auxiliary SFT loss (RPO-style), and (e) a two-stage training procedure with over-refusal mitigation. Table 3 ablates only component (c)—partial DPO vs full DPO vs SFT on the intervened dataset. No ablation isolates the contribution of the auxiliary SFT loss, the over-refusal mitigation stage, or the number of safety triggers. While the overall method clearly works, attribution of gains is incomplete. (The intervention effect itself is validated in Section 3.3, which partially compensates.)

4. **On JailbreakBench, GRPO achieves better reasoning safety than IPO, contradicting the paper's narrative framing.** On JailbreakBench for DS-8B, GRPO achieves 0.3% harmful reasoning versus IPO's 5.7% (Table 2). The paper's narrative emphasizes that IPO "overcomes the rollout-diversity limitation of reinforcement learning," yet on this benchmark the RL-based method is strictly better. IPO's advantage emerges on the more adversarial benchmarks (StrongReject, WildJailbreak), which is informative—it could suggest that IPO confers robustness under attack while GRPO suffices for simple refusal—but the paper does not discuss this. The current framing ("IPO outperforms GRPO") is true on average but masks this nuance.

5. **The loss formulation in Equation 4 is not standard DPO and may contain a technical discrepancy.** The standard DPO objective at the partial-trajectory level would be:
   $$-\log\sigma\left(\beta\log\frac{\pi_\theta(\tilde{z}^{\geq h}|x,z^{<h})}{\pi_{\theta_{ref}}(\tilde{z}^{\geq h}|x,z^{<h})} - \beta\log\frac{\pi_\theta(z^{\geq h}|x,z^{<h})}{\pi_{\theta_{ref}}(z^{\geq h}|x,z^{<h})}\right)$$
   However, Equation 4 replaces $\pi_{\theta_{ref}}(\tilde{z}^{\geq h}|\dots)$ in the denominator of the first ratio with $\pi_\theta(\tilde{z}^{\geq h}|\dots)$, which is unusual. The resulting expression simplifies to a form where the preferred continuation's reference probability does not appear. The paper should clarify whether this is a typo or an intentional modification, and if the latter, explain the motivation and how it affects the gradient.

6. **The rollout-diversity analysis for GRPO (Figure 4) is conducted only on JailbreakBench.** Figure 4 shows that 36.2% of prompts yield zero safe reasoning paths, motivating the claim that low rollout diversity limits RL-based process supervision. However, this analysis uses only the least adversarial benchmark (JailbreakBench). The GRPO safety results in Table 1 show its largest shortfalls on StrongReject and WildJailbreak, but the causal diagnosis (low diversity) is not verified for those more challenging settings.

### Trivial
None.

## Nice-to-Haves

- **Confidence intervals or variance estimates** for the main safety results in Table 2 would strengthen individual comparisons, especially given the use of LLM-as-judge. The consistent pattern across three model families partially compensates, but readers cannot assess whether differences like IPO 16.7% vs STAR 21.9% on StrongReject reasoning are reliable.
- A **comparison of IPO against standard DPO on naturally occurring safe (non-intervened) trajectories** would help isolate the contribution of the intervention itself from the contribution of preference learning.
- **Computational cost of CSR estimation** (32 sampled continuations per token, potentially 16,000 generations per trajectory) and **sensitivity analysis for the threshold parameters** (μ=0.9, K=15) would strengthen the empirical characterization.

## Removed Points

These points from the input review were removed and are listed here for reference only; treat them with caution:

- *"Claim that prior work 'overlooks the unique significance of safe reasoning' is slightly overstated"* — Subjective opinion about framing, not a substantive weakness.
- *"Qwen3-8B shows much lower Unsafe Reasoning + Safe Response (3.7%) than DeepSeek models (40.5%, 51.3%) — this large variation is interesting but not discussed"* — An observation, not a weakness; the paper focuses on the general phenomenon, and Qwen3-8B results still show the same pattern.
- *"No statistical significance or confidence intervals are reported"* — Moved to Nice-to-Haves; this is standard practice in the field for LLM-as-judge evaluation and not a meaningful weakness.
- *"The comparison of 14 generations (IPO) vs 40 generations (GRPO) is somewhat apples-to-oranges because IPO uses GPT-4o API calls"* — The generation count comparison is for model inference cost specifically (which is the dominant cost in GRPO); the GPT-4o API calls are a separate, one-time data construction cost. This is a minor framing issue, not a substantive weakness.
- *"The paper does not discuss whether IPO affects reasoning length or style"* — Not essential; the paper focuses on safety and capability preservation.
- *"The CSR estimation cost and heuristic threshold choices (μ=0.9, K=15) are not discussed"* — Addressed in the Nice-to-Haves section above; too minor to list as a weakness.

## Novel Insights

The reviews surface one genuinely novel perspective: the paper's central finding—that safety in reasoning is consolidated at a small number of critical tokens, rather than distributed uniformly—has implications beyond the IPO method itself. It suggests that process supervision for safety can be dramatically more efficient than dense or sparse reward schemes, because only a few decision points need to be corrected. The reviews also highlight an informative nuance: the JailbreakBench result (GRPO outperforming IPO) suggests that corrective intervention methods and RL-based methods may have complementary strengths—IPO for robustness under attack, GRPO for simple refusal. This interplay is worth deeper investigation.

## Suggestions

1. Provide details on trigger pool construction: total unique triggers identified, selection criteria for the six "representative" triggers, and a sensitivity study varying the number.
2. Add a human evaluation on a representative subset (e.g., 100 prompts) comparing IPO against the strongest baseline, to break the GPT-4o-evaluates-GPT-4o-detected-data loop.
3. Clarify the IPO training objective (Equation 4) and verify that it is intentionally non-standard; if so, explain the design rationale and its effect relative to standard partial-trajectory DPO.
4. Add a brief discussion of the JailbreakBench result (GRPO 0.3% vs IPO 5.7%) to acknowledge where IPO is not the top performer and to frame the paper's contribution more precisely.
5. Extend the rollout-diversity analysis (Figure 4) to at least one adversarial benchmark (StrongReject or WildJailbreak) to verify that low diversity is the mechanism behind GRPO's relative weakness there.

## Score and Decision

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>