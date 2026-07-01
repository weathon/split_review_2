Now let me read the remaining sections to verify the specific claims about Figure 2 and related work more carefully.Now I have all the information I need to draft the review. Let me submit my draft and then proceed with calibration.Now let me run calibration Round 1 — bracketing pass.Let me read a couple of the most relevant anchors to calibrate properly.Now I have enough calibration data. Let me form my bracket and finalize the review.

**Round 1 Bracket Assessment:**
- The paper is clearly above the 1.5–3.5 range (fundamentally flawed papers with no real contribution).
- It is comparable to TPO (6.33, accepted) in contribution type — both propose fine-grained preference optimization for reasoning — but TPO has slightly better baseline coverage, while ST has better model diversity.
- It is comparable to General Preference Modeling (5.0, rejected) in terms of having a good idea but significant experimental gaps.
- It is below the 8.0 range papers which have more comprehensive and rigorous evaluations.

**Initial bracket: 4.5 to 6.0**

The key discriminator is the absence of training-time baselines, which is a structural gap since the paper's method operates at a fundamentally different resource level than all compared methods. The selective OOD reporting and missing variance further weaken the evidence. However, the consistent improvements across 3 model scales and the informative ablation are genuine strengths.

Now let me write the final review.

---

## Summary
SteadyThought (ST) proposes a three-stage thought-level preference optimization framework to mitigate "under-thinking" in Large Reasoning Models — the tendency to switch reasoning thoughts excessively rather than committing to promising ones. The pipeline segments responses into thoughts via entropy spikes, generates switch-suppressed completions for each thought, and constructs fine-grained preference pairs for optimization (STPO, a SimPO variant conditioned on thought-level prefixes). Experiments on three models (1.5B, 8B, 14B) across math and code benchmarks show accuracy improvements up to 5.3% and token reductions up to 39.3%.

## Strengths
- **Clean problem formulation with principled pipeline.** The formalization of under-thinking as a thought-level preference problem (Section 2.1, Equations 1–2), defining commit vs. switch trajectories and optimizing via the Bradley-Terry model, provides a principled and elegant foundation. The three-stage pipeline flows logically from this formulation.
- **Consistent improvements across three model scales.** Table 1 shows ST simultaneously improves accuracy (+1.9% to +3.12% average) and reduces token count (−17.3% to −24.9%) across DeepSeek-R1-Distill-Qwen-1.5B, Qwen3-8B, and DeepSeek-R1-Distill-Qwen-14B — this is not a single-model result.
- **Informative ablation isolating design choices.** Table 4 clearly demonstrates that SFT reduces tokens but drops accuracy (80.4% / 22.9%), DPO maintains accuracy but barely reduces tokens (82.6% / 30.8%), while STPO achieves both (84.4% / 31.2%). This directly validates the need for length-normalized preference optimization at the thought level.
- **Entropy-based thought segmentation with threshold sensitivity analysis.** Table 3 shows performance is reasonably stable across thresholds (2.8, 3.0, 3.2) while validating the chosen threshold is near-optimal.

## Weaknesses

### Fatal
None

### Major
1. **No training-time baselines compared.** All three baselines (NoThink, NOWAIT, SEAL) are inference-time methods requiring no training or additional data, while ST fine-tunes via preference optimization on omni-math training data. This asymmetry is never acknowledged in the paper. The paper cites training-time approaches in Section 5.1 (e.g., L1 from Aggarwal & Welleck 2025) but does not compare against any. Without at least one training-time baseline, we cannot assess whether STPO's gains come from the thought-level formulation or simply from having access to a training budget. The Table 1 comparison overstates ST's relative advantage by comparing across fundamentally different resource levels.

2. **Missing variance/confidence reporting on small benchmarks.** AIME 2024 has only 30 problems. The paper reports averaging over 8 runs (Section 4.2) but provides no standard deviations or confidence intervals anywhere in Table 1. For DeepSeek-1.5B on AIME, the improvement is 27.5% → 31.2% (3.7pp on 30 problems) — this is approximately 1 additional correct problem, which could easily be noise. LiveCode uses only 2 runs, yet the headline claim "up to 5.3% accuracy improvement" is drawn from this benchmark (Qwen3-8B on LiveCode). The statistical evidence as presented does not establish the claims with confidence.

### Minor
3. **Selective OOD reporting.** The paper emphasizes OOD generalization via LiveCode, highlighting Qwen3-8B's +5.3% and DeepSeek-14B's +4.2% gains over vanilla (Section 4.3). However, from Table 1: SEAL achieves 83.4% vs. ST's 77.1% for Qwen3-8B, and SEAL achieves 75.1% vs. ST's 74.3% for the 14B model. The paper does not acknowledge that the strongest inference-time baseline outperforms ST on LiveCode for 2 of 3 models. The OOD generalization story is more nuanced than presented and the abstract's claim of "strong generalization" is partially contradicted.

4. **Thought completion relies on the mechanism the paper critiques.** Section 3.2 suppresses logits of "wait" and "alternatively" to near-zero during thought completion — the same mechanism used by NOWAIT. The introduction (Section 1, paragraph 3) criticizes such methods for "applying suppression globally, potentially limiting the model's flexibility." While ST applies this only during training data generation (not at inference), the paper frames ST as philosophically distinct from switching-suppression methods without acknowledging this dependency. This is an intellectual honesty gap rather than a methodological flaw, but it weakens the paper's positioning.

5. **Figure 2 anomaly partially contradicts the "deeper exploration" narrative.** For DeepSeek-1.5B on AIME2024, the average number of thoughts *increases* under ST (12.87 → 18.21), and the proportion of the last thought *decreases* (18.96% → 15.66%). The paper acknowledges this (Section 4.4.1) and attributes it to "smaller models tackling high-difficulty problems," but this explanation is post-hoc and untested. It undermines the generality of the "deeper exploration" claim.

### Trivial
None

## Nice-to-Haves
- Add at least one training-time baseline (e.g., L1 or RL with a thought-switching penalty) for a same-budget comparison.
- Report standard deviations across the 8 AIME runs and increase LiveCode runs for the OOD claim.
- Explicitly discuss the relationship between ST's thought completion stage and NOWAIT — framing ST as "NOWAIT for data generation, then preference optimization" would be more transparent.
- Failure analysis on problems where ST drops accuracy relative to vanilla.
- Response-level DPO using the same training data (beyond the Table 4 ablation) to better isolate thought-level granularity's contribution.

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **"Trigger word set ('wait,' 'alternatively') lacks justification for completeness"** — Minor implementation detail; the method works empirically across three models.
- **"'.\n\n' delimiter is format-dependent and brittle"** — Implementation detail that doesn't undermine the contribution; the method works across three differently-formatted models.
- **"Paper does not report training set size or number of preference pairs"** — Reproducibility nitpick likely addressed in supplementary materials.
- **"Cost of thought completion should be summarized in main text"** — The paper defers to Appendix E; this is a presentation preference, not a methodological flaw.
- **"Table 2 metric doesn't distinguish 'smarter switching' from 'less switching'"** — This is speculative and does not identify a specific error; the paper presents this as one piece of evidence among several.
- **"'Rank of first correct thought position' metric not rigorously defined"** — The figure caption explicitly defines it as "the percentile rank of the first correct thought in a thought sequence."
- **"STPO novelty is overstated (it's SimPO conditioned on thought prefix)"** — While the STPO loss itself is a modest modification of SimPO, the overall framework (three-stage pipeline) is the contribution. Inflated naming is a presentation issue, not a substantive flaw.
- **"'Any of the initial tokens' is vague — how many are checked?"** — Implementation detail.

## Novel Insights
The core insight of relocating thought-switching suppression from inference time to training-time preference data construction is genuinely novel and transferable. Rather than constraining the model at decode time, ST uses switching suppression as a tool to generate counterfactual trajectories (what would have happened if the model had committed?), then trains the model to internalize this preference. This "counterfactual completion → preference optimization" pipeline is a conceptual contribution that could apply beyond the specific under-thinking problem.

## Suggestions
- Add at least one training-time baseline (e.g., L1) to provide a same-budget comparison — this is the single most impactful improvement.
- Report confidence intervals for AIME (the 8 runs are already collected) and increase LiveCode runs to at least 4–5.
- Acknowledge SEAL's superiority on LiveCode for 8B and 14B models and discuss why the inference-time method generalizes better OOD.
- Reframe the relationship to NOWAIT transparently in Section 3.2.
- Test the "smaller models need more thoughts on harder problems" explanation (Section 4.4.1) with a controlled experiment rather than leaving it as post-hoc.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to SteadyThought |
|-------|------|-----------|-------|-----------------------------|
| NEMESIS (jailbreaking) | 5kMwiMnUip | 1.40 | R1 | Far below — fundamentally different quality level |
| Chinese NLP robots | gwZ90hFSL2 | 1.00 | R1 | Far below — no real technical contribution |
| KL Divergence GFlowNets | Uj0h13lVrR | 1.00 | R1 | Far below — lacks rigor |
| Soft Alignment (SPO) | 28TLorTMnP | 2.50 | R1 | Below — ST has clearer formulation and results |
| Reward Learning w/ Ties | fTdhM7q1o2 | 3.00 | R1 | Below — ST has more complete experiments |
| Scalable Pref. Learning (CVX-DPO) | EVZnnhtMNX | 3.00 | R1 | Below — ST has broader empirical validation |
| Supervised CoT | pXIbcRPxWR | 2.50 | R1 | Below — ST addresses a more specific, better-motivated problem |
| General Preference Modeling (GPM) | xS4XOS4NQ5 | 5.00 | R1 | Comparable — both have good ideas with experimental gaps; GPM more theoretical, ST more practical |
| Beyond One-Pref (MODPO) | 2BfZMh9td4 | 4.25 | R1 | Slightly below ST — MODPO has weaker empirical results |
| Generative Reward Models | MwU2SGLKpS | 4.50 | R1 | Comparable — both propose iterative training ideas with some gaps |
| Improve VLM CoT | XgYZT35N76 | 4.25 | R1 | Below ST — narrower contribution |
| Pref Opt for Combinatorial | 8QkpCRio53 | 5.75 | R1 | Comparable — both have clean formulations but limited baselines |
| **TPO (Tree Pref Opt)** | O0sQ9CPzai | **6.33** | R1 | **Most similar paper**. TPO has better baseline design but narrower model coverage; ST has 3 models but no training-time baseline. TPO accepted at 6.33. |
| OpenPRM | fGIqGfmgkW | 6.00 | R1 | Slightly above ST — broader utility and better evaluation design |
| Visual Contrastive + PO | wgRQ2WAORJ | 6.25 | R1 | Different domain; comparable quality |
| LLMs for Bayesian Opt | OOxotBmGol | 8.00 | R1 | Above — more comprehensive evaluation |
| Rethinking Reward Modeling | rfdblE10qm | 8.00 | R1 | Above — stronger theoretical + empirical contribution |
| MAP (Multi-Value Alignment) | NN6QHwgRrQ | 8.00 | R1 | Above — more rigorous formulation and evaluation |
| Syntactic/Semantic Control via SMC | xoXn62FzD0 | 8.00 | R1 | Above — more principled approach with broader evaluation |

**Round 1 bracket: 4.5 – 6.0**

The most informative comparison is with TPO (6.33, accepted), which also proposes fine-grained preference optimization for LLM reasoning. TPO was criticized for unfair data comparison and limited model diversity — ST shares the first concern (more severely, since all baselines are from a different category) but improves on the second (3 models vs. 1 family). TPO's main advantage is that it compares against DPO using the same data framework, which ST does (Table 4) but less thoroughly.

Compared to GPM (5.0, rejected), ST has a more practically grounded contribution with broader empirical evidence, but GPM has stronger theoretical novelty. ST is slightly above GPM.

**Final calibration reasoning:** The paper addresses a genuine problem with a well-structured solution showing consistent results across 3 model scales. However, two major gaps — the absence of any training-time baseline (making the central comparison structurally asymmetric) and the missing variance on small benchmarks — prevent the evidence from fully supporting the claims. The selective OOD reporting further undermines trust. These gaps are addressable in revision but currently present. The paper sits between borderline reject and borderline accept, closer to the middle.

**Final Score: 5.0** — A solid idea with encouraging but incomplete evidence. The experimental design gaps (no training-time baselines, no variance reporting, selective reporting) prevent confident assessment of the method's claimed advantages. With a training-time baseline comparison and statistical reporting, this could be a borderline accept.

**Decision: Reject** — The structural asymmetry in baseline comparison is a significant evidential gap that cannot be resolved without additional experiments.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>