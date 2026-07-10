Now I have all the calibration data I need. Let me write the final review.

## Summary

This paper re-evaluates three benchmarks (TORCS, KAREL, PARKING) from the programmatic RL literature and argues that observed OOD generalization advantages of programmatic policies over neural ones stem from uncontrolled experimental factors rather than representational differences. It introduces an expressivity + discoverability framework for understanding OOD generalization and identifies memory-scaling tasks (where working memory must grow with input size) as the domain where programmatic representations provide a genuine structural advantage.

## Strengths

- **The expressivity/discoverability framework (Section 5, Definitions 2–3) is a genuinely useful conceptual tool.** It cleanly decomposes what it takes for a representation to enable OOD generalization into two individually checkable conditions: whether a generalizing policy exists in the space (expressivity) and whether the search algorithm can find it (discoverability). This provides a principled language for future work to discuss and design generalization experiments. [favorability=11.86]

- **The memory-scaling argument (Section 5, lines 298–302) is insightful and theoretically grounded.** The observation that constant-capacity neural architectures cannot represent solutions whose working memory grows with input size (e.g., BFS requires Θ(|V|) memory; vertex indexing requires Ω(log|V|) bits) is clearly articulated and well-supported by complexity-theoretic reasoning. This is the paper's most durable conceptual contribution and correctly identifies where programmatic representations have a genuine structural edge. [favorability=12.75]

- **The KAREL experiment (Table 2) provides a practically useful finding.** Showing that a simple feedforward network augmented with the previous action (PPO with a_{t-1}) matches or exceeds LEAPS on 4 of 5 tasks at 100×100 scale — achieving perfect generalization on STAIRCLIMBER, MAZE, TOPOFF, and FOURCORNER — is non-trivial and practically valuable. It demonstrates that architectural choices significantly impact neural policy generalization in this domain. [favorability=11.99]

- **The PARKING analysis (Section 4.3) is presented honestly.** The paper acknowledges mixed results (DQN has higher average test success rate 0.18 vs. 0.16; PSM has 2/30 models solving all 100 test cases vs. 0/15) and does not overclaim for either representation. Not every result needs to fit the narrative. [favorability=11.59]

- **The positive contribution — identifying memory-scaling tasks as the domain where programmatic representations have a genuine structural advantage — is well-motivated theoretically.** This provides a constructive path forward beyond the debunking narrative. [favorability=13.45]

## Weaknesses

### Major

- **TORCS experiment does not establish a confound in the way the paper claims (Section 4.1).** The paper changes the training reward (β=1.0 → β=0.5) and observes that neural policies then generalize. The paper asserts this is "not changing the problem, but only how the agent learns" (line 209), arguing that Equation 2 defines an intrinsic reward since evaluation is on lap time. However, changing β changes the MDP the agent solves — the optimal policy under β=0.5 differs from the one under β=1.0. The paper does not re-run NDPS under β=0.5 nor train neural policies under β=1.0 with an alternative intervention (e.g., regularization, early stopping). The comparison is asymmetric: programmatic policies optimized under one regime are compared against neural policies trained under a different regime. The experiment shows that under a different reward function, different results obtain — but it does not demonstrate that the original comparison was confounded by "uncontrolled experimental factors." Rather, it may confirm that the programmatic representation's harder-to-optimize nature (which the paper itself identifies as the mechanism) is itself a feature, not a confound. [favorability=1.80]

- **The FUNSEARCH proof-of-concept is too thin to support the weight placed on it (lines 304–308).** The paper's central positive claim — that programmatic representations have a genuine advantage on memory-scaling tasks — is supported by only three sentences describing a FUNSEARCH experiment. No details are provided on: the wall-sparse maze configuration, the prompt/specification given to FUNSEARCH, the number of attempted runs (3 runs, but 3 out of how many total attempts?), compute cost, runtime, or any comparison with neural baselines on the same task. The paper never empirically demonstrates that neural policies *fail* on such tasks — it argues they should by capacity but provides no experiment showing this failure. For a claim presented as the paper's answer to "when do programmatic representations matter," this is a major evidentiary gap. [favorability=-0.93]

- **KAREL comparison does not fully support the "confound" framing (Section 4.2).** The paper shows that PPO with a_{t-1} (a feedforward network with observation augmented by last action) generalizes well. However, this is a different neural architecture from what Trivedi et al. (2021) used (ConvNet for full observability, LSTM for partial observability). Showing that a *third* architecture works well demonstrates that better neural baselines exist, but it does not demonstrate that the original comparison was confounded. Moreover, the paper does not test whether LEAPS also benefits from the same modification (partial observability + last-action augmentation). It is possible LEAPS would generalize even better under this setting, which would not change the original conclusion. [favorability=0.00]

### Minor

- **Seed selection in TORCS weakens the comparison (Table 1, lines 213–215).** For G-TRACK-1, only 13 of 30 DRL(β=0.5) models learned to complete the training track, and generalization statistics are reported only for these 13 successful models. The paper reports "76% of the models" generalized to G-TRACK-2 (line 215), but this is 76% of 13 (≈10 models), not 76% of 30. An intent-to-treat analysis would show approximately 33% (≈10/30) generalization — far below the 3/3 (100%) of NDPS. The paper is transparent about the numbers in the table caption, but the main-text framing is ambiguous and masks this attrition. [favorability=3.52]

- **Definition 3 (Discoverability) is underspecified (line 282).** The definition includes the clause "within a bounded time limit" but provides no guidance on how this bound is set relative to the search process, the complexity of the space, or what counts as "bounded." As written, any representation is discoverable given enough time, and none is discoverable given too little. The definition needs to relate the time bound to the search space's complexity to be operational. [favorability=3.55]

- **The memory-scaling argument's novelty is somewhat overstated.** Works such as Delétang et al. (2023) and Weiss et al. (2018) — which the paper itself cites — have previously documented the limitations of fixed-capacity neural networks for algorithmic and memory-scaling tasks. The paper's framing of this as a novel contribution could be moderated. [favorability=-0.53]

### Trivial

None.

## Nice-to-Haves

- Reframe the TORCS experiment as a demonstration of the discoverability problem (the neural space contains generalizing solutions but gradient search doesn't find them under the original reward) rather than as evidence of an experimental confound.
- Expand the FUNSEARCH proof-of-concept into a systematic experiment with neural baselines on the wall-sparse maze, evaluation of the synthesized BFS program across maze sizes, and analysis with limited search budgets.
- Add an intent-to-treat analysis for TORCS showing both conditional and unconditional generalization rates.
- Test whether LEAPS also benefits from the last-action augmentation in KAREL.
- Sharpen Definition 3 by relating the time bound to a property of the search space (e.g., number of policy evaluations, search space size).

## Removed Points

These points from the input review were removed with justification:
- **"TORCS experiment claims could be refuted more completely"** — The demand that the paper "would need to show neural policies trained with the *same* reward function (β=1.0) with some other modification" is a request for a different experiment; the core asymmetry criticism is retained above.
- **"Code availability only after review"** (lines 326–328) — Standard practice for double-blind review; removed as a reproducibility nitpick.
- **"DQN choice in PARKING needs elaboration"** — The paper states preliminary experiments showed DQN outperformed PPO/DDPG (line 260); this is a sufficient explanation.
- **"Abstract/Introduction framing too strong"** — Subjective presentation preference rather than a verifiable weakness.
- **"No comparison between LEAPS and PPO(a_{t-1}) under same observation setup"** — Partially retained in the KAREL weakness but the full version is too demanding; both methods operate under different search/optimization paradigms.

## Novel Insights

The key insight from the synthesis of the harsh critic and strength finder is that the paper's two parts (debunking prior work vs. building a positive framework) are in tension: the debunking narrative demands rigorous experimental controls that the paper does not fully provide, while the positive framework (expressivity/discoverability + memory-scaling) is well-supported conceptually but lacks empirical depth for its key positive claim. The paper would be significantly stronger if restructured around the positive framework rather than the debunking narrative.

## Suggestions

1. Restructure the paper around the positive argument (expressivity/discoverability framework → identifying memory-scaling as the genuine differentiator → empirical demonstration on memory-scaling tasks) rather than the debunking narrative.
2. Expand the FUNSEARCH experiment to include systematic neural baselines on the wall-sparse maze, demonstrating their failure empirically.
3. Reframe the TORCS experiment as a discoverability demonstration rather than a confound claim.
4. Add intent-to-treat statistics alongside the conditional statistics in Table 1.

**Calibration Report:** Anchors used across rounds: (1) *Reclaiming the Source of Programmatic Policies* (3.67, round 1) — topically similar but weaker contributions; (2) *Do Symbolic or Black-Box Representations Generalise Better* (3.00, round 1) — similar framing but significantly poorer presentation; (3) *Bad Habits: Policy Confounding* (5.25, round 2) — similar pattern of novel concept with overclaimed empirical support; (4) *How the Level Sampling Process impacts Zero-Shot Generalisation* (5.67, round 2) — stronger theory but mixed reviews; (5) *GRAM* (6.00, round 2) — well-executed but more incremental. Our paper's favorability profile (very high for the framework and memory argument: 11.86–13.45; very low for FUNSEARCH: −0.93) resembles the *Policy Confounding* anchor (5.25), which also had high-favorability conceptual contributions alongside low-favorability empirical limitations. However, our paper has broader empirical scope and a stronger conceptual contribution, placing it slightly above that anchor but below well-executed method papers like GRAM (6.00).

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>