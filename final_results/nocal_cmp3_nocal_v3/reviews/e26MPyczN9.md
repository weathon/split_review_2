## Summary

This paper re-evaluates claims that programmatic policies generalize better than neural policies in RL. It revisits three benchmarks (TORCS, KAREL, PARKING), arguing that much of the reported gap stems from experimental confounds rather than inherent representational differences. It introduces an expressivity/discoverability framework (Section 5) to distinguish whether failures come from the policy class lacking a solution or the search procedure failing to find it, and argues that genuine programmatic advantages emerge when tasks require working memory that scales with input size. A proof-of-concept uses FUNSEARCH to synthesize BFS for a modified KAREL maze.

## Strengths

1. **The expressivity/discoverability framework (Section 5, Definitions 2–3) is genuinely useful.** It provides a clean language for disentangling whether a representation fails because it lacks a generalizing policy or because the search algorithm cannot find one. Prior work has been muddled on this distinction, and the framework productively organizes the paper's analysis (e.g., classifying the LSTM failure on KAREL as a discoverability failure, not an expressivity one).

2. **The KAREL re-evaluation (Section 4.2, Table 2) makes a clean empirical point.** "PPO with a_{t-1}" (a feedforward network with the last action appended to the observation) generalizes perfectly from 8×8/12×12 to 100×100 grids on four of five tasks, while the previously-used ConvNet and LSTM baselines fail. This is the paper's strongest evidence that architectural choices within the neural family can dramatically change OOD generalization outcomes, and that prior comparisons were not controlling for the right variables.

3. **Honest engagement with PARKING ambiguity.** The paper transparently reports mixed results (PSM has 2/30 seeds solving all 100 test cases vs. DQN's 0/15, while DQN has higher average success rate: 0.18 vs 0.16) and acknowledges the domain is challenging for both representations (lines 266–267, 274). This candor is a strength even though the results complicate the paper's narrative.

## Weaknesses

### Fatal

None.

### Major

1. **TORCS comparison is asymmetric.** The TORCS experiment (Section 4.1) reduces β from 1.0 to 0.5 in the intrinsic reward (Equation 2) for the neural policy, while the NDPS results in Table 1 are from the original β=1.0 setup from Verma et al. (2018). The paper argues this "is not changing the problem, but only how the agent learns to complete a given track" (line 209) because evaluation is on lap time and crashes. However, this comparison does not control for the training objective across representations. A clean test would compare neural and programmatic policies under identical reward conditions (both β=1.0 and β=0.5), or at least show that NDPS under β=1.0 owes its generalization to producing cautious behavior. As designed, the experiment shows that reward shaping affects neural generalization — a known phenomenon — but does not isolate representation as the variable of interest. Additionally, only 13/30 and 4/15 seeds successfully learned the training task under β=0.5, making the comparison a selected subset. This weakness undermines the paper's marquee result. **(Severity: Major — the experiment's design does not support the specific claim it is asked to carry.)**

### Minor

2. **Abstract overstates PARKING results.** The abstract claims neural policies "can match or exceed" programmatic ones across all three benchmarks, but for PARKING the neural policy (DQN) was trained with no modifications analogous to those used in TORCS or KAREL. The body presents the results honestly as mixed, but the abstract's framing is too assertive for this domain. Seed counts are also asymmetric (30 PSM, 15 DQN) without explanation.

3. **FUNSEARCH proof-of-concept is too thin.** The experiment (lines 304–308) shows that FUNSEARCH can synthesize a Python BFS implementation for a wall-sparse maze variant. However: (a) No neural policy is trained on the same task to empirically demonstrate failure — the paper relies solely on a theoretical fixed-capacity argument, which is sound but would benefit from a concrete baseline. (b) Key experimental details are absent from the main text (maze topology, LLM prompt structure, evaluation protocol). Three runs is a minimal sample. (c) The experiment uses FUNSEARCH (LLM-based synthesis in Python) rather than a domain-specific language with bounded expressivity like the KAREL DSL, making the "programmatic vs neural" comparison less direct than the paper's framing implies.

4. **HARVESTER remains unsolved.** "PPO with a_{t-1}" achieves only 0.04 on 100×100 HARVESTER (Table 2), even though it solves the other four KAREL tasks perfectly. The paper does not discuss why this task resists the approach, leaving a meaningful exception unaddressed.

5. **Uneven seed counts across comparisons.** KAREL uses 5 seeds for LEAPS/ConvNet/LSTM (from Trivedi et al., 2021) vs. 30 seeds for "PPO with a_{t-1}" (the paper's own runs). PARKING uses 30 PSM vs. 15 DQN. TORCS uses 3 seeds for NDPS (from Verma et al., 2018) vs. 30/15 for DRL (β=0.5). The paper does not discuss whether these asymmetries could affect the comparisons.

### Trivial

None.

## Nice-to-Haves

- A controlled TORCS experiment training NDPS under β=0.5 to isolate whether the programmatic advantage is purely speed-driven.
- Hyperparameter sensitivity analysis for β (TORCS) and the action-augmented observation (KAREL).
- Details of the SparseMaze variant, LLM prompt, and evaluation protocol for the FUNSEARCH experiment (may be in the stripped appendix).
- Discussion of computation cost comparison between programmatic synthesis and neural training.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **"The paper's two halves are in tension"** — The paper draws a clear boundary: tasks solvable with constant memory (KAREL maze via wall-following, TORCS, PARKING) show no representational advantage; tasks requiring instance-scaling memory (general pathfinding, nested subproblems) do. The structure is coherent.

2. **"Expressivity argument is muddled by universality acknowledgment"** — The paper explicitly acknowledges RNN universality (lines 302–303) and cites work on practical limitations (Nowak et al., 2023; Delétang et al., 2023). It provides a clear basis for the expressivity vs. discoverability distinction: KAREL maze uses constant memory (discoverability failure), general pathfinding requires Ω(log|V|) bits (expressivity failure).

3. **"The LLM itself is a neural network, undermining the claim"** — The LLM is the search mechanism, not the resulting policy representation. The comparison is about the policy representation (program vs. neural weights), not the search method.

4. **Miscellaneous formatting and reproducibility nitpicks** — These reflect parser artifacts or reviewer knowledge gaps, not author errors.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the peripheral point that the paper's strongest argument for programmatic advantage (instance-scaling memory) could be reframed more sharply as "guaranteed correctness via verifiable programs" rather than "expressivity," but this is a framing choice the paper already touches on.

## Suggestions

1. Fix the TORCS comparison: either retrain NDPS under β=0.5, or train neural policies under β=1.0 with significantly more tuning effort to match programmatic generalization. Without this, the TORCS experiment does not cleanly separate representation from training objective.
2. Tone down the abstract's claim about PARKING to match the mixed results presented in the body.
3. Either substantially strengthen the FUNSEARCH experiment (add a neural baseline on SparseMaze, provide full experimental details) or remove it and rely on the theoretical expressivity argument alone.
4. Discuss the HARVESTER exception and why "PPO with a_{t-1}" fails on this task while succeeding on the others.
5. Equalize or justify the asymmetric seed counts, or discuss how they might affect the comparisons.

## Score and Decision

The paper has genuine contributions: the expressivity/discoverability framework is a useful conceptual advance, and the KAREL re-evaluation is a clean empirical finding. However, the marquee TORCS experiment has an asymmetric design that weakens its central conclusion, and the proof-of-concept is too thin to carry its assigned weight. The paper would be substantially stronger with a fixed TORCS comparison. In its current form it makes a worthwhile but incomplete case.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>