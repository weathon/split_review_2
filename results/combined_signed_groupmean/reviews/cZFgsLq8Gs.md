## Summary

DeepScientist is a large-scale LLM-based multi-agent system for automated scientific discovery, operating over month-long timelines across three frontier AI tasks (Agent Failure Attribution, LLM Inference Acceleration, AI Text Detection). It formalizes discovery as a search over program space guided by a persistent Findings Memory, generating ~5,000 ideas, validating ~1,100, and ultimately producing methods that reportedly surpass published human SOTA baselines. The system's progressive discovery trajectory on AI Text Detection (T-Detect → TDT → PA-TDT) is the most compelling evidence of genuine scientific advancement by an automated system.

## Strengths

- **Large-scale engineering effort with real empirical advances.** The system operates at a scale rarely seen in automated scientific discovery (~20,000 GPU hours, ~5,000 ideas, ~1,100 validated, month-long runs on 16 H800 GPUs). More importantly, it produced concrete methods — A2P, ACRA, and the T-Detect/TDT/PA-TDT series — that reportedly surpass published SOTA baselines from competitive venues. The AI Text Detection improvement (7.9% AUROC + 190% latency reduction) and the progressive trajectory T-Detect → TDT → PA-TDT (Figure 5) show the system genuinely building on its own prior discoveries, not just sampling randomly.

- **Principled architectural design.** Formalizing scientific discovery as search over a program space where the value function is expensive to evaluate, and structuring the system around a persistent Findings Memory that accumulates both successes and failures, is a well-motivated design choice. The three-stage pipeline (hypothesize → implement → analyze) with explicit promotion between stages is a reasonable operationalization.

- **Rigorous human evaluation of generated papers.** The five autonomously generated papers were reviewed by a program committee of three active LLM researchers (two ICLR reviewers, one ICLR Area Chair), with inter-rater reliability reported (Krippendorff's α = 0.739). This goes well beyond prior AI Scientist systems, which typically lack any human evaluation.

## Weaknesses

### Major

- **Misleading headline claim: "two weeks vs. three years of human research."** This claim (abstract, Figure 1) compares trajectories with fundamentally different starting conditions. DeepScientist starts from a *reproduced human SOTA codebase* (Section 4, line 120: "Each SOTA method is manually reproduced, and we preserve execution logs and test scripts to allow DeepScientist to focus on research advancement"), while the human trajectory includes the entire research process from scratch — problem formulation, dataset construction, baseline establishment, method invention. Furthermore, the human timeline spans 2019–2025 (~6 years), not three. The paper acknowledges the head start in Section 4 (line 120) but presents the comparison in the abstract and Figure 1 as if the starting conditions were equivalent. This claim should be retracted or substantially reframed.

- **No uncertainty quantification on any primary result.** All performance numbers in Figure 3 are single points with no confidence intervals, standard deviations, or number of trials reported. The LLM Inference Acceleration improvement of +1.9% (193.90 vs. 190.25 tok/sec) is likely within measurement noise for throughput benchmarks, which are notoriously variable depending on GPU thermal conditions and memory bandwidth contention. The Agent Failure Attribution baselines (12.07%, 16.67%) are also presented without error bars. Table 3 (human evaluation) does report variance, but the primary experimental results lack this.

- **Human supervision is underreported and conflicts with the "fully autonomous" framing.** Line 121 states: "Three human experts supervise the process to verify outputs and filter out hallucinations." This is the only mention, with no quantification of how often the humans intervened, what proportion of outputs were rejected, or what qualified as a hallucination. Meanwhile, the abstract claims "fully autonomous scientific discovery" and the conclusion claims "end-to-end autonomy from ideation to real progress." Without accounting for the human safety net, the autonomy claim is unverifiable and the comparisons to human researchers are not apples-to-apples.

- **"Bayesian Optimization" framing overclaims what is implemented.** The surrogate model is an LLM prompted to produce a valuation vector ⟨v_u, v_q, v_e⟩ on a 0–100 scale, followed by a UCB acquisition function with w_u = w_q = κ = 1 (Equation 1). There is no Gaussian process, no probabilistic posterior, no Bayesian update — the core machinery of Bayesian optimization is absent. The paper would be more accurate describing this as "LLM-guided retrieval-based hypothesis selection with an exploration bonus." The paper would also benefit from an ablation comparing this selection mechanism against simpler baselines (greedy selection, random selection). The one-sentence mention of a random-sampling ablation (line 208) lacks detailed numbers.

### Minor

- **Agent Failure Attribution baselines lack context.** The "All at Once" baseline achieves only 12.07% and 16.67% accuracy, but the paper does not report the number of classes or random-chance level for the Who&When benchmark. If the task has ~6 classes, the Algorithm-Generated baseline of 16.67% is at random chance, making it a weak test of the discovery system.

- **Automated review comparison (Table 2) lacks calibration explanation.** DeepScientist's papers achieve 60% simulated acceptance while every prior system achieves 0% across 28 papers. The acceptance threshold that produces this clean split is not explained, and Zochi (rating 4.63) also gets 0% while DeepScientist (rating 5.90) gets 60%. Understanding how the binary accept/reject decision maps to the rating score is essential for interpreting this result.

### Trivial

None.

## Nice-to-Haves

- Report the number of classes / random-chance baseline for the Who&When benchmark so the 12.07% and 16.67% baselines can be interpreted.
- Ablate the UCB exploration term (κ·v_e) against greedy selection to justify the exploration bonus.
- Break down the monetary cost (GPU + API calls to Gemini/Claude) for practitioners evaluating whether to use such a system.
- Provide a taxonomy of implementation errors (syntax errors, logical bugs, missing dependencies, etc.) from the 60% failure analysis — this would guide future work on executor robustness.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

1. **"DeepReviewer-14B from the same ecosystem as DeepScientist's authors"** — The reviewer speculates about authorship without evidence. DeepReview (Zhu et al., 2025a) is cited as external work; there is no information in the paper to support the claim that it comes from the same team.
2. **"Comparison to HUMAN Avg. (ICLR 2025) is misleading because it includes all submissions"** — Using the all-submissions average as a baseline is a legitimate and common comparison; it is not inherently misleading.
3. **"Implementation details deferred to Appendix D, which is not available"** — Parser strips appendices from all papers; the details exist in the original submission.
4. **"The 5,000 → 1,100 → 21 → 5 funnel is described qualitatively"** — This is actually shown quantitatively in Figure 4 with per-task breakdowns.
5. **"Scaling experiment confounds parallelism with total compute"** — The paper partially addresses this (line 230 mentions serial testing and differentiates wall-clock advantage from sample efficiency). The scaling claim is about wall-clock throughput, which is practically relevant.

## Novel Insights

The key tension across the reviews is between the paper's genuine engineering ambition and its rhetorical overreach. The progressive discovery trajectory on AI Text Detection (T-Detect → TDT → PA-TDT) is the most compelling evidence of genuine scientific advancement by an AI system — the methods demonstrably build on each other conceptually, shifting from distributional statistics to non-stationary time-frequency analysis. This specific result deserves more attention than the inflated comparative claims. The 60% implementation error rate as the dominant bottleneck (not flawed hypotheses) is a practically important finding that suggests where the field should focus its efforts. The paper's true contribution is as the largest-scale demonstration to date that an AI system can produce progressively improving, novel methods on real AI research tasks — not as a system that "compresses three years of human research into two weeks."

## Suggestions

1. **Replace the "two weeks vs. three years" framing** with an honest comparison: given the human SOTA codebase as starting point, how much did DeepScientist improve the metric, and what would a reasonable person-hour comparison look like?
2. **Report uncertainty on primary results.** Run each discovered method multiple times (even 3–5) and report mean ± std. For LLM Inference Acceleration, measure throughput over a sustained period with multiple seeds.
3. **Quantify the human supervision burden.** How many hours per day did the three experts spend? What fraction of outputs required filtering? This is essential for assessing the autonomy claim.
4. **Rename "Bayesian Optimization"** to a more accurate description (e.g., "LLM-guided exploration with UCB selection") and ablate the selection mechanism against simpler baselines.
5. **Report the number of classes or random-chance level** for the Who&When benchmark so the baseline numbers can be interpreted.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `8QTpYC4smR.md` | 1.00 | Bracket | No | Literature survey — far weaker than DeepScientist |
| `P49gSPmrvN.md` | 1.00 | Bracket | No | Visualization paper — far weaker |
| `5kMwiMnUip.md` | 1.40 | Bracket | No | LLM jailbreaking — different topic, weaker |
| `nSDOkm0SKo.md` | 1.00 | Bracket | No | Finance analysis — far weaker |
| `t9U3LW7JVX.md` | 3.00 | Bracket | No | Agentic system design — different topic, lower |
| `zlAUnwhE2v.md` | 3.00 | Bracket | No | Molecular property prediction — weaker |
| `zEPYCDaJae.md` | 2.50 | Bracket | No | Dataset processing framework — weaker |
| `PQrkWvQSL0.md` | 2.50 | Bracket | No | Drug-target interaction — weaker |
| `yYQLvofQ1k.md` | 4.00 | Bracket | Yes | Multi-agent idea generation — only generates ideas, no experimental validation. Weaker contribution. |
| `b89OyrljJD.md` | 3.67 | Bracket | No | Molecular retrosynthesis — weaker |
| `w0es2hinsd.md` | 5.25 | Bracket | Yes | R&D benchmark — very limited scope (financial only). Weaker. |
| `dhoCfPPjeZ.md` | 4.25 | Bracket | No | Scientific program discovery — weaker |
| `X9OfMNNepI.md` | 6.25 | Bracket | No | Chemistry hypothesis rediscovery — similar strength |
| `6z4YKr0GK6.md` | 6.00 | Bracket | Yes | Agent evaluation benchmark — strong benchmark but different contribution type |
| `HAwZGLcye3.md` | 6.40 | Bracket | Yes | LLM agent for biological experiments — most similar in contribution type. DeepScientist has larger scale and broader tasks but more severe rhetorical overclaims. |
| `9nUBh4V6SA.md` | 6.50 | Bracket | No | Self-driving lab protocols — different domain |
| `m2nmp8P5in.md` | 8.00 | Bracket | No | Scientific equation discovery — stronger/unified acclaim (all 8s) |
| `Q6a9W6kzv5.md` | 8.00 | Bracket | No | Physical world benchmark — different topic |
| `vrBVFXwAmi.md` | 8.00 | Bracket | No | Quantum property estimation — different topic |
| `OI3RoHoWAN.md` | 8.00 | Bracket | No | Robotic simulation — different topic |
| `mPdmDYIQ7f.md` | 6.00 | Narrow | Yes | LLM agent search — similar strength, comparable weakness profile |
| `kuhIqeVg0e.md` | 5.75 | Narrow | No | Chemical reasoning memory — weaker |
| `stolHkh6Nc.md` | 5.50 | Narrow | No | AutoML agent — weaker |
| `IwhvaDrL39.md` | 5.75 | Narrow | No | Research community simulator — weaker |

**Calibration reasoning:** Round 1 bracketing placed DeepScientist in the 3.5–7.5 range (stronger than idea-generation-only systems at 3–5, comparable to agent-based discovery systems at 5.5–6.5, but below the 8+ bracket where papers receive uniformly strong endorsement). Round 2 narrowed to 5.5–6.5 based on comparison with BioDiscoveryAgent (6.40, Accept) and AgentSquare (6.00, Accept). Like BioDiscoveryAgent, DeepScientist has high-impact strengths (scale +9.69, empirical advances +10.00, human evaluation +9.59) but also high-impact weaknesses (misleading claim -9.96, missing UQ -9.99, supervision gap -9.15, BO overclaim -10.00). Unlike BioDiscoveryAgent, DeepScientist's major weaknesses are primarily rhetorical/terminological rather than fundamental (lack of wet-lab validation in BioDiscoveryAgent was -8.62). However, the cumulative impact of four simultaneous -9+ weaknesses is substantial. The paper's core contribution is real and significant, but the presentation issues are severe enough to require revision before the claims can be accepted at face value.

**Score: 6.0** — borderline accept. The paper presents a genuinely impressive large-scale system with concrete results, but must address the misleading comparative claim, missing uncertainty quantification, unquantified human supervision, and terminological overreach before its conclusions can be fully trusted.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>