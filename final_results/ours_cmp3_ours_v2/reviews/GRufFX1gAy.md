Now I have all the calibration data I need. Let me write the final consolidated review.

## Summary

This paper introduces InnoGym, a benchmark and framework for evaluating AI agents along two dimensions: performance gain (improvement over best-known solutions) and methodological novelty (dissimilarity from prior approaches). It includes 18 curated Improvable Tasks from real-world competitions and NP-hard problems, a unified execution environment (iGym), and experiments with three agent frameworks (MLAB, CODEACT, AIDE). The core novel contribution is a novelty metric computed via an LLM-as-judge pipeline using Codex for feature extraction and GPT-5 for dissimilarity rating.

## Strengths

- **Well-motivated gap.** The paper correctly identifies that existing agent benchmarks evaluate correctness but ignore methodological diversity — two agents can produce the same answer through radically different approaches, and current evaluation frameworks treat them identically. This is a genuine limitation, and the paper's core motivation is sound.

- **Clean formal framework.** The formalization of a task as (P, S, V, D) and the definitions of Performance Gain G(s) and Novelty N(s) (Section 2.2, Equations 1–3) are principled and clearly presented. The three-way categorization of innovation (breakthrough, performance, conceptual) is a useful conceptual contribution.

- **Systematic task curation pipeline.** The two-stage filtering from 197 initial items to 72 to 18 tasks (Section 3.1), with explicit criteria for resource availability, evaluator quality (Pearson ≥ 0.9, Kendall-τ ≥ 0.8 consistency checks), and domain balance, is more transparent than many benchmark papers provide.

## Weaknesses

### Fatal

None.

### Major

- **The novelty metric (N(s)) — the paper's central contribution — has unaddressed methodological fragilities.** The metric uses an LLM-judging-LLM pipeline (Codex for extraction, GPT-5 for rating) with no discussion of the risks this entails. Specifically: (a) **LLM-judging-LLM circularity** — the same class of models generating the solutions is used to evaluate their novelty, and errors in Codex's feature extraction propagate into the comparison; (b) **min-aggregation conflates proximity to one prior with lack of novelty** — using `min_{h in S_known} D(s, h)` means a solution that genuinely synthesizes ideas from multiple known approaches can receive low novelty if it happens to be close to any single prior, a known failure mode of min-aggregation that the paper does not discuss; (c) **false precision** — novelty scores in Table 2 are reported to two decimal places (e.g., 66.67) but the underlying signal is a Likert-scale judgment (0–4 per dimension) averaged over 6 dimensions from a single LLM judge, with no reliability evidence in the main text. While Appendix F is referenced for "behavior and reliability" analysis, none of these concerns are acknowledged or addressed in the main paper. Because the novelty metric is central to the paper's contribution, these issues substantially weaken the paper's claims.

- **Survivorship bias in the comparative evaluation.** Table 2 reports per-agent averages computed over different task subsets, because each agent failed to produce valid submissions on different tasks (marked "/"): MLAB averages over 7 tasks (failed on CDML, PTTALC, RCIC), CODEACT over 6 (failed on BEETL-MI, BEETL-Sleep, CDML, PTTALC), AIDE over 5 (failed on BEETL-MI, CDML, NPR, PTTALC, TrojanDetection). The agent that fails on the hardest tasks sees those failures excluded from its average but included in others' averages — e.g., RCIC (CODEACT: -99.67) is excluded from MLAB's average but included in CODEACT's. This is a classic survivorship-bias problem. The qualitative conclusion that "MLab leads" is still supported by per-task comparisons on the overlapping tasks (Belka, CirclePacking, OAG), but the paper's reported averages and the claim that novelty was "comparable" across agents rely on incomparable sets. This needs correction (report per-task without averaging, or restrict to common support, or count failures as the minimum observed score).

### Minor

- **iGym is claimed as a contribution but receives no experimental validation.** It is listed as contribution #3 and described as supporting "robust recovery for long-running tasks, native concurrency, and consistent tool management," but no experiments compare agents running in iGym vs. alternative environments (OpenHands, AutoGen). Since all agents are run in iGym, it serves a standardization role, but the claimed advantages over existing SDKs are unsubstantiated.

- **Limited task coverage in experimental analysis.** The detailed analysis of temporal dynamics, exploration-exploitation trade-offs, and base-model effects (Section 4.3) uses only the Circle Packing task. The generalizability of these findings to the other 9 tasks is unclear.

### Trivial

None.

## Nice-to-Haves

- A human validation study for the novelty metric — collecting human novelty ratings on a sample of agent-vs-reference solution pairs and reporting their correlation with the LLM-judge score.
- Reporting novelty evaluation computational cost (how many LLM calls per solution).
- Confidence intervals or variance reporting for the benchmark results.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"All results are negative, so benchmark is uncalibrated."** Removed because the paper explicitly acknowledges this finding ("no agent managed to surpass the state-of-the-art human solutions") and frames it as a discovery about current agent limitations, not a flaw in the benchmark. A benchmark measuring both dimensions and finding that one dimension always fails is still informative.
- **"First benchmark claim overstated due to InnovatorBench."** Removed because Table 1 shows InnovatorBench has "Eval Novelty: ✗" — it does not evaluate novelty, so the paper's claim about being the first to evaluate *innovation potential* (combining performance and novelty) is accurate.
- **"'Nears the state of the art' on CirclePacking is misleading."** Removed because the critic misread the metric. G(s) = V(s) - V*_known, so G = -0.008 means V(s) = 2.635 - 0.008 = 2.627, very close to the SOTA of 2.635 and far above the lowest leaderboard score of 0.96.
- **"Figure reference errors in Section 2."** Removed as a formatting/parser artifact; the original PDF likely has correct sub-figure references.
- **"Taxonomy plays no role in benchmark."** Removed as scope creep — the paper explicitly scopes to Improvable Tasks only, and the taxonomy justifies this design choice.
- **"iGym section lacks text."** Removed as a normal appendix deferral for space reasons, standard in conference papers.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Validate the novelty metric.** The highest-leverage improvement is to collect human novelty ratings on a sample of solution pairs, compute correlation with the LLM-judge scores, and report inter-rater reliability for both humans and the LLM judge. This evidence is essential for the paper's central claim.

2. **Fix the evaluation protocol.** Report per-task results without averaging across agents (the raw data in Table 2 already supports this), or restrict cross-agent comparisons to the common task support, or code failures as a penalty rather than excluding them.

3. **Acknowledge and discuss the fragility of LLM-as-judge novelty evaluation.** Add a paragraph in the main text discussing the circularity risk, the min-aggregation limitation, and the precision caveats.

## Score and Decision

Calibration anchors retrieved:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| MLE-Bench (6s5uXNWGIh.md) | 8.00 | R1 | More polished benchmark with rigorous medal-based evaluation, thorough experiments, but similar domain. InnoGym is substantially weaker: fewer tasks (18 vs 75), unvalidated central metric, fewer agents tested. |
| ScienceAgentBench (6z4YKr0GK6.md) | 6.00 | R1 | Similar benchmark paper with expert-validated tasks and thorough evaluation. InnoGym has comparable benchmark construction quality but a weaker central metric. |
| AgentBench (zAdUB0aCTQ.md) | 6.20 | R1 | Broad LLM-as-agent benchmark. InnoGym is more novel conceptually (innovation metrics) but weaker empirically. |
| MCU (IWC6zUEVcL.md) | 4.00 | R1 | Minecraft benchmark with unclear writing and missing code. InnoGym is better structured and clearer. |
| TeamCraft (nE3flbe88p.md) | 3.25 | R1 | Multi-agent Minecraft benchmark. InnoGym has a stronger conceptual contribution. |

**Initial bracket (Round 1):** 4.0–6.0. The paper has genuine conceptual contributions (clearer than MCU/TeamCraft) but lacks the validation rigor of MLE-Bench and ScienceAgentBench.

**Final score determination:** Anchored between ScienceAgentBench (6.0) and MCU (4.0). The paper's central novelty metric methodology has unaddressed fragilities, and the evaluation suffers from survivorship bias — issues that are more consequential than ScienceAgentBench's minor scope concerns but less severe than MCU's writing and reproducibility problems. The task curation is systematic and the formal framework is clean, but the core contribution lacks sufficient validation for a top venue.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>