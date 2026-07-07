Now I have enough calibration data. Let me synthesize the final review.

**Bracket Analysis:**
Round 1 bracket: My paper sits between the 3.67 anchor (NGVljI6HkR, programmatic vs latent spaces) and the 5.75 anchor (tuEP424UQ5, MORL generalization).

- The 3.67 anchor has a -9.59 fatal-level weakness (missing the main point of latent spaces) and modest strengths (+4.88 max). My paper has no comparable fatal weakness (max negative = -4.41), and comparable strengths (+4.15 max).
- The 5.25 anchor (R6klub5OXr) has weaknesses at -10.13 and -6.26 — far worse than my paper's worst (-4.41).
- The 5.50 anchor (EBT0oymkZb) has -8.16 weakness.
- The 5.75 anchor (tuEP424UQ5) has -8.44 and -8.03 weaknesses — substantially more severe than any in my paper.

My paper's weighted profile is clearly better than the 3.67 and 5.25 anchors. It's in the 5.5–6.5 range. The strengths (expressivity/discoverability framework, TORCS re-evaluation) are genuine but the KAREL comparison issue (-4.41) and proof-of-concept thinness (-2.57) prevent a higher score.

Let me write the final review now.

Also important: I need to check that the "3 seeds" for NDPS and DRL (β=1.0) vs "30 seeds" for DRL (β=0.5) — this is a real asymmetry. The NDPS results come from prior work with only 3 seeds. Let me verify from the paper: Table 1 footnote says "For NDPS and DRL (β=1.0), we used the data from (Verma et al., 2018), which is over three models." So only 3 seeds for the baselines. This is a meaningful weakness but the reviewer didn't highlight it explicitly — it's part of the seed count critique.

OK now finalizing the review.## Summary

This paper re-evaluates prior claims that programmatic (DSL-based) policies generalize better than neural policies in RL, across three benchmarks (TORCS, KAREL, PARKING). It introduces an expressivity/discoverability framework to distinguish whether a generalizing solution *exists* in a policy class versus whether training can *find* it. The TORCS re-evaluation traces the reported programmatic advantage to the reward function encouraging speed, which programmatic policies are less effective at optimizing—reducing the speed incentive closes the gap. On KAREL, PPO with last-action augmentation matches or exceeds LEAPS on some tasks, but the comparison uses different observation spaces. The paper also argues theoretically that programmatic representations provide a genuine advantage when tasks require instance-growing memory (e.g., BFS), supported by a proof-of-concept using FUNSEARCH to synthesize BFS for a wall-sparse KAREL variant.

## Strengths

- **The expressivity/discoverability framework (Definitions 2 and 3, Section 5) provides a clean conceptual lens** for analyzing comparisons between programmatic and neural policies, separating whether a solution *exists* from whether training can *find* it. Weight: +4.15 (strong positive).

- **The TORCS re-evaluation (Section 4.1, Table 1) is a well-controlled demonstration** tracing the reported programmatic generalization advantage to a specific mechanism: programmatic policies are less effective at optimizing the speed term in the reward, which inadvertently helps OOD generalization on tracks with sharper turns. Reducing β from 1.0 to 0.5 eliminates most of the gap while keeping the same architecture and training pipeline. Weight: +3.11.

- **The theoretical argument about instance-growing memory (Section 5) is sound and principled.** The lower-bound argument (Ω(log |V|) bits just to index a vertex in a graph) grounds the claim that feedforward and recurrent networks with fixed capacity provably cannot represent algorithms requiring memory that scales with input size, such as BFS. Weight: +4.06.

## Weaknesses

### Fatal
None.

### Major

- **The KAREL re-evaluation (Section 4.2) compares PPO with a_{t-1} against LEAPS under different observation spaces.** LEAPS receives high-level boolean sensor readings (frontIsClear, leftIsClear, etc.—see Figure 2a grammar non-terminal *h*), while PPO with a_{t-1} receives raw local grid cells plus the last action (lines 219–222). These differ in information content and abstraction level, making the comparison not properly controlled. The paper's own analysis (Section 4.4, line 270) notes that "providing fewer input features...helped with generalization," yet the neural policy here receives *more* information (raw cells) than the programmatic baseline. Additionally, LEAPS results use 5 seeds (from prior work) while PPO uses 30 seeds, with different training procedures. This weakens the claim that neural policies match programmatic ones on KAREL. (Weight: -4.41)

- **The proof-of-concept in Section 5 (wall-sparse KAREL variant, FUNSEARCH synthesizing BFS) lacks neural baselines on the same task.** The paper argues that fixed-capacity neural networks cannot solve tasks requiring instance-growing memory (line 290–298), but never empirically verifies this by attempting to train a neural policy (PPO with a_{t-1}, PPO with LSTM) on the same wall-sparse KAREL variant. The paper's positive claim—that programmatic representations enable OOD generalization where neural ones cannot—rests on a theoretical argument plus this proof-of-concept, but the absence of a neural failure demonstration leaves the empirical support incomplete. (Weight: -2.57)

### Minor

- **The expressivity/discoverability framework's attributions are post-hoc and not independently verified.** For TORCS and KAREL, the paper claims neural and programmatic spaces are similarly expressive (both contain generalizing solutions) and the gap was due to discoverability. However, there is no independent verification that the neural space contains a generalizing solution—e.g., by training a neural network to imitate the programmatic policy and confirming it generalizes. The claim that "ReLU networks can approximate the DSL" (line 284, citing Orfanos & Lelis, 2023) is plausible but not empirically confirmed for these specific tasks. (Weight: -2.77)

- **The formal OOD generalization definition (Definition 1, line 43) requires solving *any* x' in X**, which demands formal guarantees. The paper immediately relaxes this to sampling from a test set (line 45). The gap between the formal definition and empirical practice is not discussed. (Weight: -3.94)

- **The TORCS re-evaluation changes β from 1.0 to 0.5**, changing what the agent optimizes during training. The paper argues this is an intrinsic reward that doesn't change "the problem" (lines 207–209), but the original programmatic advantage was an inherent consequence of the representation's inability to over-optimize speed. The paper's own Discussion (line 272) concedes: "We conjecture that NDPS and PROPEL would not generalize to OOD problems if they could find better optimized policies." This undercuts the framing that the original gap was purely a "confound"—it was partly a genuine representational property. (Weight: -0.66)

- **Selective evaluation in TORCS**: Only 13 of 30 seeds (G-TRACK-1) and 4 of 15 seeds (AALBORG) that successfully completed training were evaluated OOD (Table 1). The subset that succeeded may be qualitatively different from the full set, introducing selection bias. (Weight: -1.52)

- **PARKING results (Section 4.3, Table 3) are ambiguous** and do not advance the paper's thesis in either direction. PSM has a smaller generalization gap (0.10 vs 0.68) but lower absolute test performance (0.16 vs 0.18). The paper honestly presents this but the section adds no support for the core claims. (Weight: -1.25)

- **"Commonly used neural architectures" (Section 5) is vague**—it spans feedforward networks, CNNs, LSTMs, and GRUs, but does not discuss transformers with large context windows, which could approximate instance-dependent memory for practical problem sizes. (Weight: -0.69)

### Trivial
- Figure 7 (the wall-sparse KAREL maze used in the proof-of-concept) is only cursorily described in the text (line 304: "wall-sparse version...so that wall-following strategies cannot be implemented") without sufficient detail to assess what the task requires or whether simpler constant-memory heuristics could suffice.

## Nice-to-Haves
- **Add neural baselines to the wall-sparse KAREL variant** (PPO with a_{t-1}, LSTM) to empirically demonstrate neural failure on the task designed to showcase programmatic advantage.
- **Control the observation space in KAREL**: compare programmatic and neural policies using the same input features (e.g., the same boolean sensor readings) to isolate representation from observation.
- **Test NDPS with β=0.5** to see whether programmatic policies also lose their generalization advantage when speed is de-emphasized, directly testing the mechanism claim.
- **Acknowledge FUNSEARCH's computational cost** (30B LLM + evolutionary search) explicitly.

## Removed Points
These points are flagged to be removed; treat them with caution:

- "The code is not available for review" — REMOVED per hard rules: The paper states (line 328) code will be made available after review, which is standard for double-blind submissions.
- "The word 'exceed' in the abstract is not supported" — REMOVED: factually incorrect. Table 2 shows PPO with a_{t-1} exceeds LEAPS on TOPOFF (100×100: 1.00 vs 0.21) and FOURCORNER (100×100: 1.00 vs 0.45).
- "FUNSEARCH is not an RL algorithm" — REMOVED: The paper explicitly calls it a "proof-of-concept" (line 304) and does not claim it integrates into an RL training loop. The criticism misreads the paper's stated scope.
- "The wall-sparse KAREL maze (Figure 7) is not shown" — REMOVED: this is a parser limitation (figures stripped from the text extraction); the figure exists in the original submission.
- Generic-strength claims about the problem being "important" or the topic being "interesting" — REMOVED: not specific to this paper's concrete contributions.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the key tension: the negative claims (confounds in prior work) are well-supported for TORCS but less so for KAREL (uncontrolled observation space) and PARKING (ambiguous). The positive claims (instance-growing memory as a genuine differentiator) are theoretically rigorous but empirically thin. The paper's own expressivity/discoverability framework is the most durable contribution, but its application to the three benchmarks is more suggestive than definitive.

## Suggestions

1. Add neural baselines (PPO with a_{t-1}, PPO with LSTM) on the wall-sparse KAREL variant to empirically validate the claim that fixed-capacity networks fail.
2. In the KAREL re-evaluation, run the neural policy with the *same* boolean sensor inputs as LEAPS to control for observation representation.
3. Test NDPS with β=0.5 to directly test whether programmatic policies lose their advantage when speed is de-emphasized, strengthening the mechanism claim.
4. Discuss the gap between Definition 1 (requiring *any* x') and empirical sampling from a test set.
5. Disclose the selection-bias limitation for TORCS (only completing seeds evaluated OOD) and report full-set statistics where possible.

## Score and Decision

**Calibration Summary:**

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| NGVljI6HkR | Programmatic vs Latent Spaces | 3.67 | R1 | Yes | Fatal-level flaw (-9.59) missing main point of latent spaces; my paper has no comparable weakness |
| MpA6HMD7Wq | Symbolic vs Black-Box Optimizers | 3.00 | R1 | Yes | Multiple fatal weaknesses (-11.48, -7.32); my paper's weighted profile is substantially stronger |
| fvTaoyH96Z | Non-Parameterized Randomization | 2.33 | R1 | Yes | Fatal weaknesses (-8.23, -7.52), unclear method; not comparable quality |
| R6klub5OXr | Analysis of DRL Algorithm Design Premises | 5.25 | R2 | Yes | Has -10.13 fatal weakness; my paper's worst is -4.41 |
| EBT0oymkZb | Zero-Shot Generalization in Offline RL | 5.50 | R2 | Yes | Has -8.16 weakness (missing SOTA baselines); my negative weights are milder |
| tuEP424UQ5 | MORL Generalization | 5.75 | R2 | Yes | Has -8.44 and -8.03 weaknesses (limited novelty), plus -7.44; my worst is -4.41 |

**Weighted-Item Comparison:** My draft's largest negative weight (-4.41, KAREL uncontrolled comparison) is milder than the worst weakness in every anchor from 3.00 to 5.75 (range: -8.03 to -11.48). My three strengths (+4.15, +3.11, +4.06) are comparable to or stronger than the positive weights in the 5.25–5.75 anchors. The weighted profile places this paper solidly above the 5.75 anchor, which had severe novelty and contribution criticisms. However, the two Major weaknesses (KAREL uncontrolled comparison, thin proof-of-concept) prevent a score at the Accept (8) level.

**Round 1 bracket:** 4.0 – 7.0  
**Final score:** 6.0 — The paper makes a genuine conceptual contribution (expressivity/discoverability framework) and the TORCS re-evaluation is solid. Both Major weaknesses are addressable but real: the KAREL comparison is uncontrolled on observation space, and the positive claim about programmatic advantage on memory-scaling tasks lacks empirical neural baselines.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>