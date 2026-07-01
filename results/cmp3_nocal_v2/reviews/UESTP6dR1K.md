## Summary

ASPEC proposes a framework for creating adaptable multi-agent systems that sit between two existing paradigms: fully static task-level optimization and fully dynamic per-query adaptation. It achieves this through (1) offline evolutionary discovery of specialist agent archetypes, (2) cultivation of their expertise through persistent memory built from post-execution reflection, and (3) a lightweight "retain-then-escalate" meta-controller that decides when to reuse the current architecture versus rebuild it. The headline results show competitive or state-of-the-art accuracy on five benchmarks (MATH, HumanEval, MMLU, GPQA, SciCode) at dramatically lower cost than existing automated agent design methods like AFlow and MaAS.

## Strengths

1. **Well-motivated problem framing (Section 1).** The paper correctly identifies a genuine limitation in the current agent design landscape: task-level methods (ADAS, AFlow) are rigid at inference, while query-level methods (MaAS, FlowReasoner) regenerate architectures per query and prevent accumulation of persistent expertise, incurring high "rediscovery" cost. The notion of stateful specialists that sit between these extremes is a genuine conceptual contribution.

2. **Impressive cost-accuracy trade-off (Table 2).** ASPEC achieves the highest GPQA accuracy (62.8%) at a training cost of $1.38 and inference cost of $0.88 — dramatically cheaper than AFlow ($20.14 training, $1.58 inference) and MaAS ($3.43 training, $2.07 inference). These efficiency numbers are the paper's strongest empirical contribution and represent a meaningful advance for practical deployment.

3. **Thorough ablation study (Section 5.1, Figure 6).** The ablation covers five system components (specialist operators, base operators, meta-controller, Architect, specialist memory) and three alternative control policies (random, cosine-similarity heuristic, LLM-as-gate). The finding that removing specialists costs 5.4% accuracy and triples cost is informative, and the comparison against LLM-as-gate (62.5% at $3.74 vs. 62.8% at $0.88) cleanly demonstrates the value of the lightweight meta-controller.

4. **Convergence analysis of discovery process (Section 5.3, Figure 7).** The comparison of specialist embeddings across 5 independent trials on GPQA (narrow domain, converging to chemistry/biology/physics archetypes) vs. MMLU (broad domain, more diverse compositions) is a creative methodological check that provides real insight into the discovery process.

## Weaknesses

### Fatal
None.

### Major

1. **"Training corpus" for cultivation is never specified.** The paper states in the abstract and Section 3.2 that specialists "cultivate their expertise on a training corpus" through "post-execution reflection," but never defines what this training corpus is for any of the five benchmarks. This is not an appendix-level detail — it is a central specification problem. GPQA (Rein et al., 2024) is a test-only benchmark with no canonical public train split. If the cultivation data includes GPQA test questions or overlapping questions, the headline results (62.8%, +6.5% over vanilla) would be compromised by data leakage. Even if the corpus is a non-overlapping set of similar questions or a held-out subset, the paper must disclose this to allow the reader to assess the risk. The same question applies to MATH, HumanEval, MMLU, and SciCode. Without this information, the paper's central empirical claims cannot be properly scoped.

2. **Meta-controller training procedure is underspecified.** Equation 4 formulates the meta-controller's objective as maximizing expected discounted reward, but the reward function \( R_t(s_t, a_t) \) is never defined — is it task accuracy? A cost-accuracy trade-off? A learned proxy? No RL algorithm is named (PPO? REINFORCE? policy gradient?), no training data distribution is described, and no training steps or convergence criteria are reported. The meta-controller is claimed to be a trained neural policy, but the paper provides no information that would allow a reader to reproduce or evaluate its training. This is a reproducibility gap.

### Minor

3. **Cross-benchmark transfer results create tension with the domain-specificity narrative.** In Figure 5, the paper reports that the ONLYSPEC configuration (specialists trained on a different domain, e.g., MATH specialists used on HumanEval) "matches or even slightly exceeds the performance of the full system." If MATH-cultivated specialists are equally effective on HumanEval as HumanEval-cultivated specialists would be, this suggests the cultivation process produces generic reasoning improvements rather than domain-specific expertise. The paper's explanation ("T-shaped reasoning strategies") is plausible but post-hoc, and the results sit somewhat uneasily with the paper's core framing of "deep, persistent domain expertise."

4. **No statistical uncertainty reported for main results (Table 1).** All 13 baselines × 5 benchmarks are reported as single-point estimates with no standard deviations, confidence intervals, or significance tests. The margins between ASPEC and the second-best method are small: 1.5% on GPQA (62.8% vs. 61.3%), 0.8% on MATH (77.3% vs. 76.5%), and 1.0% on SciCode (26.6% vs. 25.6%). The sensitivity analysis (Figure 6) reports "mean performance over 4 runs" for some plots, making the absence of equivalent variance reporting for the main results a notable inconsistency. With LLM sampling temperature at \( T = 0.3 \), these differences could fall within noise.

### Trivial

5. **Confusion matrix presentation issues (Figure 8).** In the GPQA matrix, the raw counts (20 + 149 + 20 + 149 = 338) do not match the GPQA test set size (448), and row percentages sum to 111.2%, suggesting inconsistent denominators or that these numbers cover a subset of queries not clearly described. The MMLU matrix totals 809, whereas MMLU has ~14,000 questions, confirming this is a subset. The paper should clarify what subset these matrices cover.

## Nice-to-Haves

- Clarify the confusion matrix percentages in Figure 8 with consistent denominators.
- Include a discussion of whether the LLM adjudicator used in the creation/crossover process introduces bias or additional cost (the "without human intervention" framing paper over this mechanism).
- Future work could include static ablation comparing "w/o Architect with memory" vs. "w/o Architect without memory" to isolate the effect of memory in the static setting.

## Removed Points

These points were flagged in the input review but are removed with justification:

- **"Memory appears to hurt in the static-architecture setting."** The reviewer compares "ASPEC w/o Architect" (static + memory, 61.0%) with "ASPEC w/o specialist memory" (dynamic + no memory, 61.4%). These configurations differ in both the presence of memory AND the presence of the Architect/meta-controller. There is no "static without memory" condition, so the comparison does not isolate the effect of memory. Removed as factually unsupported by the presented data.

- **"Overstates novelty relative to prior work."** The reviewer notes that evolutionary search, identity specialization, and persistent memory all appear in prior work. The paper explicitly frames its novelty as the *integration* and *lifecycle framing*, which is genuine. This is a generic critique that does not identify an actual error in the paper. Removed.

- **"LLM adjudicator as source of bias or cost."** This is a valid observation but is a nice-to-have discussion point, not a weakness of the paper. Every LLM-based system has this concern. Removed per filtering rules (does not harm the core claim).

- **General concerns about scope** (e.g., "should address more diverse environments") — mentioned in the Limitations section and outside the paper's stated scope. Removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Specify the cultivation corpus for each benchmark.** For GPQA (test-only), describe exactly what data was used, how it was obtained, and how overlap with the test set was prevented. This is the single most impactful addition the authors could make.
- **Define the meta-controller reward function** explicitly and state the RL algorithm, training data, and training procedure.
- **Add error bars or confidence intervals to Table 1**, or at minimum report the number of runs and variance for the key margins (GPQA, MATH, SciCode).
- **Reconcile the cross-benchmark transfer results with the specialization framing**, or explicitly reframe the claim if the cultivation produces generalizable reasoning strategies rather than domain-specific knowledge.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>