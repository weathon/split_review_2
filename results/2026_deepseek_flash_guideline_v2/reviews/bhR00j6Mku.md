Now I have all the information needed to write the final consolidated review.

---

## Summary
This paper systematically evaluates existing benchmark contamination detection methods against Large Reasoning Models (LRMs) under two realistic scenarios. Stage I shows that contamination introduced during SFT (initially detectable) can be concealed by subsequent PPO-style RL training (GRPO, RAFT++). Through theoretical analysis (Theorem 3.1) and causal ablations (Table 3 removing the clipping term), the paper identifies importance sampling and clipping as the root mechanism. Stage II shows that contamination with CoT applied to already-capable LRMs leaves detection methods performing weakly (average ~60% AUROC for the best method), because LRMs generalize to similar unseen questions rather than memorizing specific trajectories.

## Strengths
1. **Mechanistic identification of concealment via controlled ablations.** The paper does not merely observe that RL conceals contamination—it identifies *why*. Theorem 3.1 decomposes the effect, and Table 3 provides causal evidence: removing the clipping term from GRPO and RAFT++ eliminates concealment (AUROC drops of only −2.20% and −1.09% vs. −14.22% and −17.91% with clipping). The contrast with plain RAFT (no concealment) cleanly isolates the importance-sampling/clipping mechanism.

2. **Systematic evaluation across a broad range of methods, benchmarks, and models.** Tables 2 and 5 evaluate 10 detection methods spanning generation-based, perturbation-based, reference-based, and reference-free approaches on 6 reasoning benchmarks (Olympiad, GPQA, AIME25, AIME24, Minerva, AMC23) using 6 base models (Qwen2.5-7B-Instruct, Llama-3.1-8B-Instruct, three DeepSeek-R1-Distill variants, and OpenThinker-7B). This breadth substantially exceeds prior contamination detection studies.

3. **Evidence that LRM generalization undermines memorization-based detection assumptions.** Section 4 and Figure 4 show that after CoT contamination on LRMs, log-prob increases similarly for both members and non-members (e.g., R1 Distill Qwen: AUROC 0.479 clean → 0.498 contaminated after SFT contamination). This directly demonstrates that LRMs' reasoning capacity, not memorization, invalidates the core assumption behind existing detection methods—a finding with clear implications for future detection research.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
1. **Stage II "near random guess" characterization is somewhat overstated for a few method-model combinations.** The paper states that "almost all the detection approaches consistently perform near random guess in all the benchmarks" (abstract, Section 1, Section 4). However, Table 5 shows that LiRA achieves 65.55% AUROC on DS Qwen-14B and 62.74% on OpenThink-7B; Min-K% reaches 62.42% on DS Llama-8B; Loss reaches 62.59% on DS Llama-8B. These values are meaningfully above 50% and represent moderate detection signal on certain configurations. While the overall finding—that detection is substantially degraded and well below what would be considered reliable (e.g., the 89% LiRA achieved in Stage I)—is clearly supported, the blanket "near random" phrasing sacrifices precision. The paper would benefit from a more nuanced characterization.

2. **No uncertainty quantification.** Every AUROC in every table is reported as a single point without confidence intervals or variance estimates. The pipeline involves random member/non-member splits, random training seeds, and stochastic generation. While the key results involve large-magnitude differences (LiRA dropping from 89.13% to ~61% in Stage I, Table 2) and are consistent across conditions, the absence of error bars makes it impossible to assess whether smaller differences between configurations are within noise. This is a reporting gap that should be addressed.

### Trivial
None.

## Nice-to-Haves
- Adding a controlled comparison with a non-reasoning LLM (e.g., the base model without CoT fine-tuning) in the Stage II setup would help isolate whether the vulnerability is LRM-specific or driven by the CoT data format. Not required for the paper's claims, but would strengthen the story.
- The conclusion's recommendations (release intermediate checkpoints, move beyond memorization-driven detection) are reasonable but generic. More specific, actionable suggestions for new detection approaches would be valuable.

## Removed Points
The following criticisms from the reviewers were filtered after verification against the paper text:

- **"Broad class of RL methods extrapolation is unsupported"** — Removed. The paper tests two PPO-family algorithms (GRPO, RAFT++) and one non-PPO algorithm (RAFT), identifies the specific mechanism (importance sampling/clipping) via ablations, and uses appropriately hedged language ("may inherently," "suggests"). The extrapolation to other methods sharing the same mechanism is reasonable and properly scoped.
- **"Missing non-LRM baseline for Stage II"** — Removed. This is a scope-expansion request. The paper's contribution is quantifying detection difficulty in the LRM setting; a non-LRM comparison would be a nice addition but is not required to support the claims made.
- **"Not testing adaptive attacker strategies"** — Removed. Out of scope; the paper explicitly focuses on two specific, practically relevant contamination scenarios.
- **Formatting/typo nitpicks** — Removed per instructions (parser artifacts, not author errors).

## Novel Insights
None beyond the paper's own contributions. The two-reviewer inputs did not surface observations about the paper that go beyond what the authors themselves articulate.

## Suggestions
1. Report variance measures (e.g., 3 independent seeds with mean ± std) for the key experiments in Tables 2, 3, and 5, or at minimum acknowledge the absence as a limitation.
2. Calibrate the Stage II claim from "near random guesses" to a more precise characterization (e.g., "most methods show substantially degraded performance, often approaching chance levels, though a few method-model combinations retain moderate signal").
3. Consider adding a concrete proposal for what a non-memorization-based detection method could look like, rather than the generic "move beyond memorization-driven methods" recommendation.

## Score and Decision

**Calibration note:** The calibration retrieval tool was unavailable due to missing backend data. The score below is based on a careful assessment of the paper against ICLR standards, verified reviewer claims, and the paper's own text.

The paper makes a well-supported and important contribution. The Stage I finding—that PPO-style importance sampling and clipping can systematically erase the statistical signals that contamination detectors rely on—is convincingly demonstrated through careful ablations, theoretical analysis, and controlled experiments. The Stage II finding is less crisply novel (the conclusion that strong generalization weakens memorization-based detection follows logically from the nature of LRMs) but provides useful quantification. The two weaknesses identified are both minor and fixable: overstatement in one claim and missing error bars. Neither threatens the core contribution. The paper is clearly written, the experiments are thorough, and the findings have significant implications for LRM evaluation integrity.

**Score: 7.0**
**Decision: Accept**

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>