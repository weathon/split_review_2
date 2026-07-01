## Summary

This paper re-evaluates claims from prior work (Verma et al., 2018; Trivedi et al., 2021; Inala et al., 2020) that programmatic policies generalize better OOD than neural policies in RL. Through controlled experiments on TORCS, KAREL, and PARKING, the authors show that much of the reported gap stems from experimental confounds (e.g., reward shaping in TORCS, observation design in KAREL) rather than representational differences. They introduce an expressivity/discoverability framework and argue that genuine programmatic advantages arise only when tasks require instance-scaling memory, providing a proof-of-concept using FUNSEARCH to synthesize BFS for a modified Karel maze.

## Strengths

1. **TORCS reward confound is cleanly identified and convincingly demonstrated.** The paper shows that neural policies failed OOD generalization not because of representation but because they optimized speed too aggressively on the training track. Reducing β from 1.0 to 0.5 causes neural policies to generalize at comparable lap times to NDPS on most OOD tracks (Table 1: G-TRACK-2: 1:48 vs NDPS 1:40; E-ROAD: 1:54 vs NDPS 1:51). This is a genuine experimental insight that future work comparing programmatic and neural policies must account for.

2. **KAREL last-action-augmentation result directly challenges a central claim from Trivedi et al. (2021).** A feedforward network with the observation augmented by the previous action (PPO with a_{t-1}) achieves perfect generalization on 4/5 KAREL tasks at 100×100 scale (mean return=1.00 on STAIRCLIMBER, MAZE, TOPOFF, FOURCORNER), while LEAPS fails on TOPOFF (0.21) and HARVESTER (0.00), and PPO+ConvNet fails on all five tasks (Table 2). This demonstrates that the reported programmatic advantage in KAREL was largely an artifact of baseline choice.

3. **Expressivity/discoverability framing (Definitions 2–3) is a useful conceptual tool.** It forces clarity on whether a generalization failure is due to the policy class lacking a generalizing solution (expressivity) or the search algorithm failing to find one (discoverability). This distinction is genuinely clarifying for the literature.

4. **Intellectual honesty in reporting.** The paper does not cherry-pick favorable metrics in PARKING — it reports both "Successful-on-100" and "Success Rate" and acknowledges the ambiguity (Section 4.3). It also explicitly reports that only 13/30 (G-TRACK-1) and 4/15 (AALBORG) neural models even learned the training task in TORCS.

## Weaknesses

### Major

1. **The FUNSEARCH proof-of-concept lacks a neural baseline on the same task and does not connect to the programmatic methods studied.** The paper's positive thesis — that programmatic representations provide a genuine advantage when instance-scaling memory is required — rests on a single proof-of-concept: FUNSEARCH with Qwen 3-Coder synthesizing BFS for a wall-sparse Karel maze (Section 5). No neural policy is evaluated on this task. The paper claims neural policies "cannot generalize OOD in pathfinding problems" (line 298) based on a theoretical memory-capacity argument, but the wall-sparse maze might admit heuristic solutions that avoid full BFS. Additionally, FUNSEARCH (an LLM-based metaheuristic) is a different technology than the programmatic methods studied (NDPS, LEAPS, PSM), so the proof-of-concept does not bridge to the re-evaluation. Three runs showing success provides feasibility but not reliability.

2. **The NetHack/nested-subproblems claim is asserted without experimental support.** Section 5 argues that benchmarks with nested subproblems (NetHack) require stack-like memory that fixed-capacity networks cannot provide, and presents this as part of the paper's answer to "when do programmatic representations provide an inherent OOD generalization advantage?" Yet there are zero experiments on NetHack or any nested-subproblem domain. The claim is supported only by citations to prior work on LSTM limitations. A paper making this argument as a central finding should provide at minimum experiments on a simplified nested-subproblem domain or a more rigorous formal argument.

### Minor

3. **Abstract overclaims on the TORCS result by not caveating the low training success rate.** The abstract states neural policies "can match or exceed" programmatic OOD generalization. In TORCS, this conclusion compares generalization rates of *only the successful seeds*: 13/30 for G-TRACK-1 (of which 76% generalized to G-TRACK-2) and 4/15 for AALBORG (of which 100% generalized). An unconditional generalization rate would be roughly (13×0.76)/30 ≈ 33% for G-TRACK-2 — far below NDPS's 100%. The paper does report these numbers transparently in the table caption, so this is a framing issue, but the abstract's wording is stronger than warranted.

4. **PARKING results are ambiguous and do not clearly support the paper's overall narrative.** In PARKING, PSM (programmatic) achieves test Success Rate 0.16 vs DQN (neural) 0.18 — DQN is better in absolute test terms. The paper argues PSM generalizes better because the train-test gap is smaller (0.10 vs 0.68), but this metric depends on PSM also performing worse at training time. The paper honestly acknowledges this ambiguity, but the net result is that none of the three benchmarks demonstrate a scenario where programmatic representations clearly outperform neural ones, weakening the paper's stated goal of identifying when programmatic representations provide an advantage.

5. **Asymmetric evaluation budgets across methods are not discussed or justified.** NDPS is evaluated with only 3 seeds in TORCS while DRL uses 30 (G-TRACK-1) or 15 (AALBORG). In PARKING, PSM uses 30 seeds but DQN only 15. These asymmetries could affect the reliability of comparisons and are not addressed.

### Trivial

None.

## Nice-to-Haves

- Report unconditional generalization rates for TORCS (treating seeds that fail at training as also failing at generalization), which the authors already have the data to compute.
- Provide a direct neural-vs-programmatic comparison on the wall-sparse Karel maze to connect the re-evaluation and the positive proposal.
- Discuss computational cost trade-offs between programmatic and neural methods.

## Removed Points

- **"PARKING experiments undermine the paper's narrative"** (from Issue 4 in the input): Removed as a self-standing weakness and merged into Minor weakness 4. The paper handles PARKING honestly by reporting both metrics and acknowledging the ambiguity; this is a point of interpretation, not a flaw.
- **"Expressivity/discoverability definition softness"**: Removed. The "bounded time limit" reliance is acknowledged by the paper and is inherent to any practical notion of discoverability.
- **"FUNSEARCH synthesis details not reported"**: Removed. The paper states "the return of a policy rollout serves as the evaluation function in FUNSEARCH," which reasonably describes the protocol.
- **"No discussion of computational cost"**: Moved to Nice-to-Haves. This is a scope extension, not a core weakness.

## Novel Insights

The observation that the NDPS language (Figure 1) induces a policy space similar to ReLU networks, and that the generalization gap in TORCS is explained by neural policies optimizing speed (a confound) rather than representational limitations, is a clean and non-obvious finding. Similarly, demonstrating that augmenting observations with the last action (a_{t-1}) suffices to make feedforward networks match or exceed LEAPS on KAREL tasks is a striking result that the community should be aware of.

## Suggestions

1. Revise the abstract to either (a) add a caveat about the TORCS training success rates or (b) frame the claim as "can match or exceed *when they successfully learn the training task*."
2. Add a neural baseline on the wall-sparse maze, or reframe the FUNSEARCH result as purely a demonstration that programmatic *can* represent BFS (not that neural *cannot* solve the task).
3. Either add experiments on a nested-subproblem domain or remove the NetHack discussion from the central contribution and present it as speculation/future work.
4. Discuss or justify the asymmetric seed counts used across methods in the different benchmarks.

---

**Calibration Report**

Retrieved anchor papers (all rounds):

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| NGVljI6HkR.md "Reclaiming the Source of Programmatic Policies" | 3.67 | R1 | Less comprehensive scope; focuses on one comparison (programmatic vs latent space). Our paper is broader. |
| MpA6HMD7Wq.md "Do Symbolic or Black-Box Representations Generalise Better" | 3.00 | R1 | Similar spirit (comparing symbolic vs neural generalization) but weaker experiments and presentation. Our paper is substantially stronger. |
| QiUitwJDKI.md "InnateCoder" | 5.75 | R1 | Method paper with cleaner contribution but narrower scope. Our paper's positive proposal is weaker but the re-evaluation is stronger. |
| lUWf41nR4v.md "Program Synthesis and State Machines" | 4.50 | R1 | Method paper; less directly comparable. |
| fvTaoyH96Z.md "Non-Parameterized Randomization for Generalization" | 2.33 | R1 | Different approach to RL generalization; less relevant. |

Round 1 bracket: 3.5–6.0. The paper is clearly stronger than the score-3 anchors in execution and scope, but its positive proposal is weaker than method papers in the 5.5–6.0 range. The re-evaluation contribution on its own would warrant ~6.0, but the disconnected and incompletely tested positive proposal, combined with the abstract overclaiming, pulls the overall assessment down to 5.5.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>