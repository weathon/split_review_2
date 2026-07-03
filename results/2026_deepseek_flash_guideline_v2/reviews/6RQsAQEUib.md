## Summary

This paper proposes GHPO (Guided Hybrid Policy Optimization), a difficulty-aware RL framework for LLM fine-tuning with verifiable rewards. GHPO detects when a problem is too hard for the current policy (all G sampled responses are wrong → zero group reward), and then appends a partial ground-truth solution trace to the prompt, switching from pure RL to guided imitation for that instance while continuing standard RL for easier problems. The method is evaluated on six math benchmarks using Qwen2.5-7B (base and math-specialized variants), showing consistent gains over GRPO and curriculum-learning baselines.

## Strengths

1. **Empirically grounded problem diagnosis**: The paper quantifies the capacity-difficulty mismatch — Qwen2.5-7B-Instruct fails on 52% of NuminaMath-1.5 (Section 2.3) — directly substantiating the reward-sparsity motivation rather than just asserting it.

2. **Clean difficulty detection mechanism**: The method reuses the group-level reward computation already performed by GRPO (Section 3.3): if all G responses yield zero reward, the query is flagged as difficult. This avoids auxiliary models, manual labeling, or offline preprocessing, distinguishing it from curriculum learning (heuristic difficulty partitioning) and DAPO (which discards hard examples).

3. **Consistent empirical gains across six benchmarks on two backbones**: Table 1 (Math dataset) shows GHPO outperforming GRPO on all six benchmarks (AVG 39.8% → 44.2%), with particularly large gains on GPQA-Diamond (+8.6%) and AMC23 (+10.0%). Table 2 (Mixed dataset) shows GHPO also improves over GRPO starting from Qwen2.5-Math-7B (AVG 47.28% → 50.76%), demonstrating the mechanism is not merely compensating for a weak base model.

4. **Partial evidence for adaptive guidance via GRPO-CL-H(0.5) comparison**: Table 2 includes a GRPO-CL-H(0.5) baseline (fixed 50% hints on hard problems + curriculum learning, AVG 42.2%) vs. full GHPO (AVG 44.2%), providing some evidence that the adaptive mechanism adds value beyond simply injecting static hints.

5. **Training dynamics analysis**: Figure 4(d) shows GHPO maintains smaller gradient norms than GRPO, and Figure 3 tracks the persistent proportion of difficult problems (~60% remain difficult after substantial training), supporting the claim that reward sparsity is not just an early-training issue.

## Weaknesses

### Fatal
None.

### Major

1. **No variance or statistical significance reporting** (evidential gap). Every result in Tables 1 and 2 is reported as a single point estimate with no confidence intervals, standard deviations, or number of independent runs. RL training is notoriously high-variance. Several comparisons show differences of less than 0.01 (e.g., Math-500: GRPO-CL=0.774, GRPO-CL-H(0.5)=0.774, GHPO=0.776). Without any measure of variance, the reliability of the claimed improvements cannot be assessed. This is the most significant weakness and needs to be addressed for the paper's empirical claims to be convincing.

2. **Insufficient ablation of core components**. GHPO has at least three distinct design elements: (a) the difficulty detection threshold (all-zero rewards), (b) the adaptive multi-stage hint ratio ω, and (c) the cold-start strategy (N=20 steps of pure GRPO). None are systematically ablated. The GRPO-CL-H(0.5) baseline provides a partial probe of (b) but it confounds curriculum learning with fixed hints, so it does not cleanly isolate the adaptive ω mechanism. The cold-start parameter N=20 is used throughout with no analysis of sensitivity (what happens with N=0, N=10, N=50?). A cleaner ablation — e.g., GHPO with fixed ω vs. adaptive ω, GHPO without cold-start — would substantially strengthen the evidence for the paper's claimed novelties.

### Minor

1. **Single model family limits generalizability claims**. Both base models are Qwen2.5 variants (Base-7B and Math-7B). The paper claims "generalizability and robustness" (Section 4.3) but has tested only within one model family. An experiment on a Llama-3-8B or Mistral-7B would substantially strengthen this claim, especially since the method is framed as beneficial for "smaller, more resource-efficient LLMs."

2. **Missing comparisons to closely related methods**. The Related Work discusses DAPO (dynamic sampling to filter too-easy/too-hard prompts) and LUFFY (off-policy demonstrations) — both addressing the same reward-sparsity problem. The paper positions GHPO as more "data-efficient" than filtering approaches, but provides no empirical comparison to DAPO or similar methods. This is not fatal (the paper's primary comparison is against GRPO, which is appropriate), but it limits the assessment of relative contribution.

3. **Alternative interpretation of gradient norm evidence**. The paper interprets smaller gradient norms (Figure 4(d)) as evidence of "more stable optimization." An alternative interpretation is that the smaller gradients reflect the model making smaller updates because hints make the task artificially easier, rather than because training is more stable in a beneficial sense. The accuracy advantage of GHPO makes the "trivialized task" interpretation less likely, but the paper does not discuss this nuance.

4. **No discussion of computational overhead**. Appending partial solution traces to prompts increases prompt length for hard problems, likely increasing per-step training cost. The paper should quantify this overhead and compare it to any savings from improved sample efficiency.

5. **Cold-start parameter not justified**. Section 3.5 motivates the cold-start strategy (formatting non-compliance early in training) but does not explain why N=20 was chosen or provide any sensitivity analysis.

### Trivial
None.

## Nice-to-Haves
- Add a discussion of when hints might be "too strong" (making the problem trivial so the model merely copies the solution). The paper acknowledges the risk of "over-guiding" in Section 3.1 but provides no analysis.
- Consider using the mean group reward as an alternative difficulty threshold and discussing the trade-off.
- Include a separate section quantifying training overhead (tokens processed per batch, wall-clock time) for GHPO vs. GRPO.

## Removed Points

The following criticisms from the inputs were removed; treat them with caution if citing:

1. **"Equation (2) uses a weaker condition than the 'all zero rewards' criterion"** — This is a misunderstanding. The condition Σ_i f(a, o_i) > 0 means *at least one* response is correct, which is consistent with the difficulty detection criterion (all-zero = difficult). When at least one response is correct, non-zero advantages can be computed, so hints are unnecessary. The paper's design is coherent; this is not a flaw.

2. **"Section 3.4 relegates core details to the appendix"** — The parser strips appendix content from all papers. The original submission contains these details in Appendix B.3. This is not a valid criticism.

3. **"No ablation studies" (framed as completely absent)** — While systematic ablation is lacking, the GRPO-CL-H(0.5) vs. GHPO comparison in Table 2 does provide *some* evidence separating the adaptive mechanism from static hinting. The weakness has been downgraded from "no ablation" to "insufficient ablation" in the Major section above.

4. **"Figure 3 volatility suggests difficulty detection is noisy/unstable"** — The paper's interpretation (reward sparsity persists) and the alternative (detection is noisy) are both plausible and not mutually exclusive. This does not constitute a weakness.

5. **"GHPO vs GRPO comparison in Tables 1 and 2 differ for AIME24"** — The paper clearly states these are different training datasets (Math dataset vs. Mixed dataset), so different results are expected. This is not a contradiction.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Report variance**: Run all experiments with at least 3 random seeds and report mean ± standard deviation (or confidence intervals). This is essential for an RL paper and would immediately address the most significant weakness.

2. **Add systematic ablations**: Run (a) GHPO with fixed ω values (e.g., ω=0.3, ω=0.5, ω=0.7) vs. adaptive ω, (b) GHPO without cold-start (N=0), (c) GHPO with a mean-reward-based threshold instead of all-zero. These would isolate the effect of each design choice.

3. **Add a non-Qwen model**: Include at least one experiment on Llama-3-8B or Mistral-7B to support the generalizability claim beyond a single model family.

4. **Add DAPO comparison**: An empirical comparison to DAPO on the same benchmarks would validate the "data-efficient" claim made against filtering-based approaches.

5. **Quantify overhead**: Report the increase in tokens processed per batch and wall-clock time per training step for GHPO vs. GRPO.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>