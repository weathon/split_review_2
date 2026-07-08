Now I have all the calibration data needed. Let me compile the final review.

## Summary

This paper re-evaluates claims that programmatic policies generalize better than neural policies in RL, using three benchmarks (TORCS, KAREL, PARKING). The authors demonstrate that the TORCS generalization gap was driven by a speed-optimization confound rather than representation, and that neural policies can match programmatic ones when observation and reward engineering are applied. The paper also proposes an expressivity/discoverability framework and argues theoretically that programmatic representations have an inherent advantage for tasks requiring instance-scaling working memory, with a proof-of-concept using FUNSEARCH.

## Strengths

- **The TORCS confound is cleanly demonstrated.** The observation that programmatic policies in TORCS generalized better because they moved more slowly (less optimized for speed on the training track), not because of representational superiority, is a genuinely useful finding. The experiment with β=0.5 vs β=1.0 (Table 1) is a simple but effective test of this hypothesis, and the results support it clearly. **[weight=10.35]**

- **The KAREL re-evaluation is solid.** Showing that a simple feedforward network augmented with the last action (PPO with a_{t-1}) matches or exceeds LEAPS on several tasks and generalizes to 100×100 grids is a clean contribution, demonstrating that observation engineering can substitute for more complex architectures. **[weight=9.29]**

- **The identification of growing working memory as a structural limitation of fixed-capacity neural architectures is theoretically well-motivated.** The argument that BFS requires Θ(|V|) memory and that feedforward/recurrent networks with fixed hidden states cannot encode such algorithms is sound as an in-principle limitation, backed by an information-theoretic argument (Ω(log|V|) bits for vertex indexing). **[weight=9.35]**

- **The expressivity/discoverability framing (Definitions 2–3) captures a real distinction** often conflated in the literature—that two representations can both contain a generalizing solution but differ in how searchable they are under a given algorithm. This provides a useful vocabulary for analyzing generalization comparisons. **[weight=8.71]**

## Weaknesses

### Major

- **The positive thesis about programmatic advantages for memory-scaling tasks rests on very thin evidence.** The FUNSEARCH proof-of-concept (Section 5, final paragraph) is described in just a few sentences with no details on the prompt used, no evaluation across multiple random seeds or problem instances, no comparison with neural baselines on the same task, and no quantitative analysis of generalization beyond the claim that the synthesized BFS "generalizes to any pathfinding problem." While the paper positions this as a "proof-of-concept," the abstract and introduction list this as one of the paper's three main contributions ("identify classes of problems... demonstrate that programmatic representations can express solutions with instance-scaling memory that provably generalizes OOD"), creating a mismatch between the strength of the claims and the evidence provided. **[weight=-2.50]**

### Minor

- **The PARKING experiment does not clearly support any narrative.** DQN has a higher test Success Rate (0.18 vs 0.16), while PSM has 2/30 models solving all 100 test instances vs DQN's 0/15. The smaller generalization gap for PSM (0.10 vs 0.68) could be a floor-effect artifact since PSM's training performance is already low (0.26). The paper acknowledges this ambiguity but still frames the results as "suggest[ing] that the PSM policies generalize better." **[weight=2.62]**

- **Statistical rigor is uneven across experiments.** The TORCS generalization fractions (Table 1) are based on effective sample sizes of n=13 (from 30 seeds for G-TRACK-1) and n=4 (from 15 seeds for AALBORG), yet reported without confidence intervals. The PARKING experiment compares PSM (30 seeds) vs DQN (15 seeds) but does not test whether the 0.06 vs 0.00 Successful-on-100 difference is statistically significant. **[weight=3.39]**

- **The claim that DSLs "induce spaces similar to those of neural networks" is supported only for TORCS.** Section 5 states "The domain-specific languages used in our three domains induce spaces similar to those of neural networks," but the formal connection via ReLU networks (Orfanos & Lelis, 2023) is only demonstrated for TORCS. For KAREL and PARKING, the similarity is asserted without formal or empirical support. **[weight=2.85]**

- **The "exceed" claim in the abstract overstates what the evidence supports.** The abstract states neural policies "can match or exceed the OOD generalization of programmatic policies." The exceed claim is demonstrated only against LEAPS on specific KAREL tasks (TopOff 100x100: 1.00 vs 0.21; FourCorner 100x100: 1.00 vs 0.45), which is a specific program synthesis method. This does not warrant the broader claim that neural policies can "exceed" programmatic policies in general. **[weight=3.13]**

- **The expressivity/discoverability framework is used post-hoc and not operationalized to be predictive.** Definitions 2 and 3 reference "there exists an algorithm" and "within a bounded time limit" — neither of which can be checked in practice. The paper acknowledges this limitation, but it restricts the framework's contribution to providing vocabulary for analysis rather than a tool for generating hypotheses or guiding representation design. **[weight=1.23]**

## Nice-to-Haves

- A controlled experiment that directly compares neural and programmatic policies on a task requiring growing memory (e.g., pathfinding on arbitrary graphs), using the same or comparable neural architectures from Section 4.2, would significantly strengthen the positive thesis. This is the paper's missing centerpiece.
- Discussion of the computational cost trade-offs between programmatic synthesis (brute-force search, Bayesian optimization, CEM) and neural RL would add practical value, especially if neural policies can match programmatic OOD performance with cheaper training.

## Removed Points

- **Criticism about LSTM baseline being "notably weak"** (0.13 on Stairclimber small) — REMOVED: factually wrong. The rows marked with † ARE from Trivedi et al. (2021), not from the authors' experiments. The paper is reporting existing results, not training weak LSTMs.
- **Criticism that PARKING results "contradict rather than support the paper's narrative"** as a fatal issue — REMOVED: The paper explicitly acknowledges the ambiguity ("Independent of the metric considered, our results show that PARKING is a challenging domain for both types of representation"). The paper's framing is more cautious than the reviewer suggests.
- **Criticism about Section 6 being "largely speculative"** — REMOVED: The paper frames this as "Our findings may have implications..." and "Although a careful investigation is needed..." so it is clearly flagged as speculative.
- **Criticism that the expressivity argument has a theory/empirical gap about in-principle expressivity** — REMOVED as a standalone weakness: The paper does present an information-theoretic in-principle argument (Ω(log|V|) bits needed for vertex indexing). The argument about neural limitations blends in-principle and empirical evidence but this is stated transparently.
- **"The relationship between the intrinsic reward change and the problem definition needs clarification"** — REMOVED: The paper explicitly addresses this in a footnote at Equation 2.
- **"The paper does not discuss the computational cost trade-offs"** — REMOVED: moved to Nice-to-Haves.
- **Missing appendix content / missing related works** — REMOVED per hard rules.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's framing of the tension between the two paper thrusts (re-evaluation vs. positive claim about programmatic advantages) is a useful observation that the paper would benefit from addressing explicitly.

## Suggestions

1. Either strengthen the memory-scaling claim with a controlled experiment (directly comparing neural and programmatic policies on a task requiring growing memory) or downscope the claim to match the evidence.
2. Clarify the PARKING experiment's role in the paper's narrative — it currently sits uncomfortably between supporting and challenging both representation types.
3. Add confidence intervals for the TORCS generalization fractions and a significance test for the PARKING Successful-on-100 comparison.
4. Provide explicit support for the claim that KAREL and PARKING DSLs induce spaces similar to neural networks, or weaken the claim.

---

**Calibration Summary**

| Anchor | Avg Score | Round | Itemized? | Comparison to paper under review |
|--------|-----------|-------|-----------|----------------------------------|
| NGVljI6HkR (Programmatic vs Latent Spaces) | 3.67 | R1 | Yes | Topically similar, but weaker empirical contribution; current paper is stronger |
| lUWf41nR4v (POMPs) | 4.50 | R1 | Yes | Similar domain, comparable strength; current paper has stronger re-evaluation evidence |
| QiUitwJDKI (InnateCoder) | 5.75 | R1, R2 | Yes | Similar topic and quality; current paper has cleaner weight profile (fewer negative-weighted items) |
| tuEP424UQ5 (MORL Generalization) | 5.75 | R1, R2 | Yes | Different topic; comparable strength profile but with more negative-weighted weaknesses |
| JlSyXwCEIQ (CodeIt) | 5.75 | R2 | No | Program synthesis topic; similar score band |
| YKvBiRWdQC (Overcooked Generalization) | 5.75 | R2 | No | RL generalization benchmark; variable reviewer scores (8,3,6,6) |
| upzyG4wRBr (Program Synthesis Benchmark) | 5.80 | R2 | No | Related topic; variable scores (5,5,3,8,8) |
| Y1XkzMJpPd (OMNI-EPIC) | 6.75 | R1 | Yes | Higher variance (3,8,8,8); has deep negative-weight weaknesses (-7.38) absent from current paper |
| Zk9guOl9NS (Code Generation Reasoning) | 7.00 | R2 | No | LLM code generation, less topical |

**Round-1 bracket**: 5.5–7.0 (based on comparison with NGVljI6HkR at 3.67, lUWf41nR4v at 4.50, QiUitwJDKI at 5.75, tuEP424UQ5 at 5.75).

**Narrowing**: The current paper's weighted items show four very strong strengths (8.71–10.35) and only one negative-weight weakness (-2.50 for the thin FUNSEARCH proof-of-concept). All minor weaknesses carry positive weights (indicating they are seen as addressable observations rather than score-dragging flaws). This profile is cleaner than the 5.75-level anchors (tuEP424UQ5 has -2.44, -3.44; QiUitwJDKI has -3.01), suggesting a score slightly above 5.75. However, the -2.50 negative weight reflects a genuine structural issue — the paper's claims about programmatic advantages outpace the evidence — which prevents the score from reaching the 6.5–7.0 range of papers like Y1XkzMJpPd (which despite having deep weaknesses had strong novelty and ambition).

**Final score grounded in weighted-item comparison**: The paper shares with QiUitwJDKI (5.75) the presence of strong positive-weighted strengths (~8-10 range) and a single meaningful negative-weighted weakness. It differs from higher-scored papers in lacking the kind of "breakthrough" positive weight (>11) or system-level novelty that those papers possess. The paper's core empirical contributions (TORCS confound, KAREL re-evaluation) are solid and valuable, but the overclaiming on the memory-scaling thesis limits its overall impact.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>