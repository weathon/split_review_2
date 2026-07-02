Now I have enough information to finalize my score. Let me report the calibration anchors and finalize.

**Calibration Anchors Retrieved:**
1. `Uj0h13lVrR.md` — avg 1.00 (Round 1, band 0-1.5): Low-quality paper, not comparable.
2. `gwZ90hFSL2.md` — avg 1.00 (Round 1, band 0-1.5): Unserious submission.
3. `fvTaoyH96Z.md` — avg 2.33 (Round 1, band 1.5-3.5): Environmental generalization in RL, weaker experimental rigor.
4. `MpA6HMD7Wq.md` — avg 3.00 (Round 1, band 1.5-3.5): Thematically closest — "Do Symbolic or Black-Box Representations Generalise Better In Learned Optimisation?" (avg 3.00, all 3s). Compared to this paper, our paper has more extensive experiments across multiple domains, a clearer conceptual framework, and better presentation. Our paper is clearly stronger.
5. `NGVljI6HkR.md` — avg 3.67 (Round 1, band 3.5-5.5): "Reclaiming the Source of Programmatic Policies" — directly comparable. Our paper has stronger empirical work and a more novel framework.
6. `lUWf41nR4v.md` — avg 4.50 (Round 1, band 3.5-5.5): "Addressing Long-Horizon Tasks" — programmatic RL method paper.
7. `ehSQZa4vuk.md` — avg 5.25 (Round 2, band 4.0-7.0): "Bad Habits: Policy Confounding" — about confounds in RL generalization but only toy experiments. Our paper has more realistic benchmarks.
8. `X1p0eNzTGH.md` — avg 5.67 (Round 1, band 5.5-7.5): "Level Sampling for ZSG" — rejected despite 8,3,6 due to overclaiming and unsupported theory. Our paper's claims are better supported.
9. `tuEP424UQ5.md` — avg 5.75 (Round 2): "On Generalization Within MORL" — accepted.
10. `Y1XkzMJpPd.md` — avg 6.75 (Round 1, band 5.5-7.5): "OMNI-EPIC" — strong paper with comprehensive experiments.

**Round 1 Bracket:** [4.5, 6.5]

**Narrowing rationale:** The paper is clearly stronger than the 3.0–3.67 band (thematically identical papers scoring 3.0 and 3.67). It is stronger than the 5.0–5.25 band papers because its experiments use established benchmarks rather than toy domains, and its primary claims are well-supported by controlled experiments. However, the major weakness (missing counterfactual: programmatic methods not tested under modified conditions) and minor issues (thin FUNSEARCH, PARKING framing) prevent it from reaching the 6.75+ band. I narrow to **6.0**.

Here is my final review.

---

## Summary

This paper re-evaluates claims that programmatic policies generalize better than neural policies in RL, using three benchmarks (TORCS, KAREL, PARKING). The authors (1) show that experimental confounds (aggressive reward functions, overly rich observations) explain much of the reported gap, (2) introduce an expressivity vs. discoverability framework to structure analysis of OOD generalization, and (3) argue that programmatic representations provide a genuine advantage only when solutions require working memory that grows with input size.

## Strengths

- **Clean confound identification in TORCS (Section 4.1, Table 1).** The paper holds architecture, environment, and algorithm fixed and shows that simply reducing a reward weight (β=1.0 → β=0.5) makes DDPG match NDPS's OOD generalization. This directly demonstrates that the earlier reported gap was driven by over-optimizing speed rather than representational superiority. The fact that the reward is intrinsic (not changing the evaluation metric) is correctly noted and strengthens the result.

- **Useful conceptual framework (Section 5, Definitions 2–3).** The expressivity/discoverability distinction provides clear vocabulary for diagnosing why a representation succeeds or fails at OOD generalization. It cleanly explains a recurring confusion in the programmatic RL literature: attributing search failures (discoverability) to representational inadequacy (expressivity).

- **KAREL demonstration that a simple feedforward network with last-action augmentation matches or exceeds LEAPS (Table 2).** On MAZE (100×100), STAIRCLIMBER (100×100), TOPOFF (100×100), and FOURCORNER (100×100), the simple neural baseline achieves 1.00 return vs. LEAPS's 1.00, 1.00, 0.21, and 0.45 respectively. This is a clear disconfirmation that programmatic representations were necessary for OOD generalization in these tasks.

## Weaknesses

### Fatal
None.

### Major

- **Missing counterfactual: programmatic methods are not tested under the modified conditions.** The paper's central thesis is that the reported generalization gap arose from uncontrolled experimental factors. However, the paper never runs NDPS with the cautious reward (β=0.5) in TORCS, nor LEAPS with the last-action observation augmentation in KAREL. The NDPS and LEAPS results are taken from the original papers (3–5 seeds), while the proposed neural baselines use 30 seeds. The paper *conjectures* that NDPS "would not generalize to OOD problems if they could find better optimized policies" (Section 4.4), but does not test this. Without this control, the argument is asymmetric: we see that neural policies can match programmatic ones, but we do not see whether the programmatic advantage disappears when both are evaluated under the same conditions. The paper's contribution remains valuable (demonstrating that neural policies *can* work), but the central causal claim about confounds is weakened by the missing 2×2 design.

### Minor

- **PARKING results do not cleanly support the paper's narrative.** The abstract claims neural policies "can match or exceed" programmatic ones across "three core benchmarks," but PARKING is essentially a null result: neither PSM nor DQN generalizes reliably (test success rates: 0.16 vs 0.18). The paper tries to argue both sides ("PSM policies generalize better" via the smaller train-test gap, and "DQN is the winner" via higher absolute test success), making the result appear spun rather than honestly inconclusive. Presenting this as a null finding (both representations struggle) would be more coherent and would not detract from the TORCS and KAREL results.

- **FUNSEARCH proof-of-concept is too thin.** The paper reports that "three runs of FUNSEARCH returned a correct implementation of breadth-first search" (Section 5) in two sentences with no quantitative evaluation — no return values, no deployment in the KAREL RL environment, no comparison with neural baselines on the wall-sparse maze, no analysis of failure modes. The abstract calls this a demonstration of "provably generaliz[ing] OOD," which is disproportionate to the evidence. This does not undermine the main contributions, but the experiment should either be developed into a proper evaluation or presented with more modest language.

- **Scope is narrower than the framing suggests.** The title ("Do Programmatic Policies Really Generalize Better?") and abstract ("Re-evaluating three core benchmarks") imply a systematic reproduction study. In practice, the paper tests one neural algorithm per domain (DDPG, PPO, DQN), takes programmatic baselines from original papers with different seed counts, and does not re-run those baselines under the modified conditions. The contribution is better described as a targeted identification of confounds rather than a comprehensive re-evaluation.

### Trivial

- In the TORCS experiment, only 13/30 DDPG(β=0.5) models on G-TRACK-1 and 4/15 on AALBORG completed a lap; OOD generalization is evaluated only on these successful models. The paper discloses this (Table 1 caption) but does not discuss potential selection bias.
- No behavioral analysis (probing, attention visualization) is provided to confirm the conjecture that the KAREL neural policies implement wall-following.

## Nice-to-Haves

- Running NDPS with β=0.5 and LEAPS with a_{t-1} augmentation would complete the 2×2 design and substantially strengthen the causal claim.
- Deploying the FUNSEARCH-synthesized BFS in the KAREL wall-sparse maze with quantitative results and neural baselines.
- Presenting PARKING as a clear null result rather than attempting to extract a positive narrative.

## Removed Points

- "Missing baseline: larger neural networks" — This criticism misunderstands the paper's theoretical argument about fixed memory capacity. A larger feedforward network still has fixed capacity; the argument is about architecture, not parameter count. **Removed as a strawman.**
- "FUNSEARCH uses Qwen 3-Coder (a neural network), complicating the programmatic vs. neural dichotomy" — The synthesis method does not change the nature of the output (a program). This is a philosophical observation, not a weakness of the paper's claims. **Removed as not a real weakness.**
- Various formatting/style nitpicks — These are parser artifacts, not author errors. **Removed per hard rules.**

## Novel Insights

The harsh review insightfully identifies that the paper's central evidential gap is the missing 2×2 experimental design: showing neural policies work under modified conditions is necessary but not sufficient to prove the confound hypothesis — one must also show that programmatic methods lose their advantage when evaluated under the same conditions. This framing, while implicit in the review, is a sharper characterization of the paper's limitation than the paper itself provides. The review also correctly notes that the PARKING results, if honestly presented as a null finding, would actually strengthen the paper's overall credibility.

## Suggestions

1. **Run the missing counterfactual controls.** Test NDPS with β=0.5 in TORCS and LEAPS with a_{t-1} augmentation in KAREL. This would turn the asymmetric comparison into a proper 2×2 design and directly test the confound hypothesis.
2. **Either expand or downscope the FUNSEARCH demonstration.** Deploy the synthesized BFS in the KAREL wall-sparse maze with quantitative evaluation, or remove it and restructure the positive contribution around the theoretical memory-scaling argument.
3. **Re-frame PARKING as a null finding.** Drop the attempt to extract a positive narrative and present it honestly as a domain where both representations struggle, highlighting the limits of the confound hypothesis.
4. **Adjust the abstract and title** to match the paper's actual scope: a targeted identification of confounds rather than a systematic re-evaluation.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>