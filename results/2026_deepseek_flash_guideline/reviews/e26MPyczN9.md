## Summary

This paper re-evaluates three influential benchmarks (TORCS, KAREL, PARKING) where programmatic policies were reported to generalize better than neural policies in RL. Through controlled experiments, the authors show that the OOD generalization gap is partially attributable to experimental confounds (reward shaping in TORCS, observation design in KAREL) rather than inherent representational advantages. They introduce an expressivity/discoverability framework to formalize when representations succeed or fail at OOD generalization, and identify a class of problems (those requiring instance-scaling memory, such as general pathfinding) where fixed-capacity neural networks provably cannot match programmatic representations, with a FUNSEARCH proof-of-concept.

## Strengths

1. **TORCS reward ablation cleanly isolates a specific confound (Section 4.1, Table 1).** By reducing β from 1.0 to 0.5 in the intrinsic reward (Equation 2), neural DRL models that previously crashed on every OOD seed generalize to 76–100% of OOD tracks depending on the training track. The evaluation metric (lap time, crash) is unchanged, so the gap was demonstrably an optimization artifact, not a representational one. This is the paper's strongest empirical contribution — prior work did not perform this controlled comparison.

2. **Last-action augmentation enables a simple feedforward network to match or exceed LEAPS on 4/5 KAREL tasks at 100×100 scale (Section 4.2, Table 2).** PPO with a_{t-1} achieves 1.00 return on STAIRCLIMBER, MAZE, TOPOFF, and FOURCORNER, matching LEAPS on the first two and substantially exceeding it on TOPOFF (LEAPS: 0.21) and FOURCORNER (LEAPS: 0.45). This finding shows that a straightforward architectural modification — augmenting the observation with the previous action — can overcome generalization challenges that prior work attributed to programmatic representations.

3. **Information-theoretic argument for a principled limitation of fixed-capacity neural policies (Section 5).** The paper provides a concrete lower bound: indexing a vertex among |V| candidates requires Ω(log|V|) bits, and exact pathfinding algorithms use Θ(|V|) or Θ(d) memory, so any policy with a fixed-size hidden state (independent of |V|) cannot represent a generalizing solution for pathfinding. This goes beyond the paper's own experiments and identifies a principled class of problems where the programmatic advantage is inherent.

4. **Expressivity/Discoverability framework (Definitions 2 and 3) formalizes why prior comparisons were inconclusive.** By separating "does the space contain a generalizing solution?" from "can the search algorithm find it?", the paper gives a clear explanation: prior programmatic methods controlled discoverability (via brute-force enumeration or Bayesian optimization) while neural methods did not, but both satisfied expressivity. This conceptual contribution is reusable by future work.

## Weaknesses

### Major

- **FUNSEARCH proof-of-concept is too thin to carry the weight placed on it (Section 5).** Three runs of FUNSEARCH with a 30B LLM returned a BFS implementation for a single modified Karel task. There is: (a) no neural baseline on the same task to demonstrate that neural policies actually fail; (b) no comparison between FUNSEARCH's BFS and what prior programmatic methods (LEAPS, NDPS) would produce; (c) no discussion of computational cost (FUNSEARCH with a 30B LLM is orders of magnitude more expensive than standard RL training); (d) no evaluation of robustness across problem variations. The paper frames this as central evidence that "programmatic representations can express solutions with instance-scaling memory that provably generalizes OOD," but three runs on one task do not constitute a robust demonstration.

- **Seed count asymmetries and selective reporting weaken directness of comparisons.** In TORCS (Table 1), NDPS results use 3 seeds (from the original paper), while DRL (β=0.5) uses 30 seeds (G-TRACK-1) and 15 seeds (AALBORG). Moreover, only 13/30 and 4/15 DRL models that successfully learned the training track are evaluated on OOD tasks — the paper does not report what the full set of seeds achieved on OOD, which could introduce selection bias. In KAREL (Table 2), LEAPS and the original baselines use 5 seeds while PPO with a_{t-1} uses 30 seeds. The paper should either match seed counts or justify why the difference does not affect the comparison.

### Minor

- **KAREL re-evaluation demonstrates an architectural improvement rather than clearly identifying a confound.** The finding that a feedforward network augmented with the previous action generalizes well is a genuine and useful insight, but it differs in nature from the TORCS finding. The original claim (Trivedi et al., 2021) was that LEAPS outperformed *specific* neural baselines (ConvNet, LSTM), which Table 2 confirms. The paper introduces a new neural variant the original authors did not test. This is valuable but is better described as discovering a better neural architecture than as "controlling a confound," and the paper's framing of all three re-evaluations under a single narrative slightly overextends the central claim.

- **PARKING results are genuinely ambiguous and do not clearly favor either representation (Section 4.3, Table 3).** PSM has better "Successful-on-100" (2/30 models vs. 0/15), but DQN has a higher test "Success Rate" (0.18 vs. 0.16). The paper presents this ambiguity, which is honest, but it means PARKING does not add evidentiary weight to the paper's main thesis. The paper would benefit from acknowledging this more explicitly.

- **HARVESTER in KAREL remains unsolved by the neural baseline (Table 2).** PPO with a_{t-1} achieves only 0.04 return at 100×100 on HARVESTER, suggesting there are cases where even this architecture does not suffice. The paper does not discuss why HARVESTER resists generalization, leaving a gap in the analysis.

- **The functional-equivalence argument between programmatic and neural policy spaces is asserted rather than demonstrated (Section 5).** The paper claims that "the ReLU space can be made a superset of the TORCS language by providing the peek and fold functions as network inputs and varying the number of neurons," but does not build such a network, show that gradient descent can learn the needed weights, or address practical feasibility. This is a reasonable plausibility argument, but it is not a construction.

- **No direct ablation running NDPS/PROPEL with the cautious reward (β=0.5).** The paper's hypothesis is that the reward confound affected neural policies more than programmatic ones. Running NDPS with the cautious reward and checking whether its OOD advantage shrinks or disappears would directly test this mechanism. Without this, the claim that NDPS "would not generalize... if they could find better optimized policies" (Section 4.4) is speculative.

### Trivial

None.

## Nice-to-Haves

- A direct comparison of NDPS/PROPEL with the cautious reward function to test whether the confound also affects programmatic methods
- Analysis of what the neural policies actually learn (feature usage, internal representations) to substantiate the "spurious correlations" claim
- Discussion of computational cost tradeoffs between programmatic synthesis and neural training
- Investigation of why HARVESTER resists generalization

## Removed Points

Points flagged for removal (treat with caution):

- *Criticism that the "sparse observations" claim in KAREL is misleading because "the original work used a fully observable setting"*: The original work (Trivedi et al., 2021) tested both fully observable (ConvNet) and partially observable (LSTM) settings; the paper acknowledges this. The criticism is partially inaccurate.

- *Criticism that the paper sidesteps modern neural architectures (transformers)*: The paper explicitly discusses transformers, stack-RNNs, and neural Turing machines in Section 5's final paragraph as a "promising research direction." The paper's scope is "commonly used neural architectures" (feedforward, ConvNet, LSTM), which is a reasonable scope for this work.

- *Criticism about missing appendix content and reproducibility (code after review)*: Standard practice for anonymous submissions; the parser strips appendix content.

- *Strength Finder's claim about FUNSEARCH being a strong contribution*: Downgraded to a weakness because the evidence (three runs, no neural baseline) is too thin to constitute a strength.

- *Various formatting/style nitpicks*: These are parser artifacts, not author errors.

## Novel Insights

The most valuable observation emerging from the reviews is the heterogeneity of the paper's three re-evaluations. The TORCS finding cleanly demonstrates a specific confound mechanism (reward shaping). The KAREL finding is structurally different — it shows that a simple architectural modification (last-action augmentation) enables generalization, which is more of an architectural insight than a confound exposure. The PARKING finding is genuinely ambiguous. This heterogeneity is itself informative: it suggests that the OOD generalization gap between programmatic and neural policies is not monolithic but depends on specific, identifiable mechanisms (reward function design, observation sparsity, policy sparsity). The paper's expressivity/discoverability framework provides a useful vocabulary for discussing these distinctions, but the paper would be stronger if it leaned into this heterogeneity rather than unifying all three cases under a single "confound" narrative.

## Suggestions

1. Substantially expand the FUNSEARCH proof-of-concept with neural baselines on the wall-sparse maze, cost comparisons, and robustness evaluation across multiple problem variations.
2. Run NDPS/PROPEL with the cautious reward (β=0.5) to directly test whether the reward confound affects programmatic methods as well.
3. Match seed counts across comparisons or statistically justify asymmetry where it exists.
4. For TORCS, report the full 30/15 seed OOD results including failed learners to address selection bias concerns.
5. Discuss why HARVESTER resists generalization with PPO + a_{t-1}, as this would inform the analysis.
6. Reframe the KAREL finding more precisely as an architectural insight rather than grouping it under "confound control."

## Score and Decision

**Calibration anchors (all rounds):**

| Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| KL Divergence Optimization for GFlowNets | Uj0h13lVrR.md | 1.00 | R1 | Strong reject — not comparable; poor-quality paper |
| Systematic Review of LLMs | 8QTpYC4smR.md | 1.00 | R1 | Strong reject — survey paper with no novel contribution |
| Reclaiming the Source of Programmatic Policies | NGVljI6HkR.md | 3.67 | R1 | Topically related rebuttal paper, mixed reviews (3,3,5); current paper is more ambitious and has stronger evidence |
| Addressing Long-Horizon Tasks... | lUWf41nR4v.md | 4.50 | R1 | Rejected method paper with unclear presentation; current paper is clearer |
| On Generalization Within MORL | tuEP424UQ5.md | 5.75 | R1 | Benchmark + framework paper, accepted; comparable ambition and rigor |
| The Generalization Gap in Offline RL | 3w6xuXDOdY.md | 6.50 | R1 | Re-evaluation/benchmark paper, accepted; closest in genre — current paper has a stronger single finding (TORCS) but weaker proof-of-concept |
| How the Level Sampling Process... | X1p0eNzTGH.md | 5.67 | R1 | Re-evaluation of generalization in RL, accepted with mixed scores |
| SYMPOL: Symbolic Tree-Based On-Policy RL | qpXctF2aLZ.md | 7.20 | R1 | Stronger methodological contribution; current paper is more of a re-evaluation study |
| Interpreting Emergent Planning | DzGe40glxs.md | 8.00 | R1 | Strong accept — far stronger theory and evidence than current paper |

**Round 1 bracket:** 4.0 – 7.0 (narrowed to 5.5 – 6.5 after examining the most comparable anchors — "The Generalization Gap" at 6.50 and "On Generalization Within MORL" at 5.75)

**Final score:** 6.0

This paper makes a genuine contribution (particularly the TORCS reward confound and the expressivity/discoverability framework), and the KAREL finding is a useful architectural insight. However, the FUNSEARCH proof-of-concept is too thin, the PARKING results are ambiguous, seed count asymmetries weaken the comparisons, and the framing overclaims relative to the evidence (especially by grouping KAREL under "confounds"). These issues are real but addressable; they do not invalidate the core contributions. Score is calibrated against comparable re-evaluation/benchmark papers that received borderline accept decisions.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>