## Summary

ASPEC proposes a framework for creating stateful specialist agents that accumulate expertise through a two-stage lifecycle: (I) evolutionary discovery of specialist agent archetypes via an LLM-based Architect, and (II) experiential cultivation of persistent memories through reflection on a training corpus. A lightweight "retain-then-escalate" meta-controller decides per query whether to reuse the current architecture or resample a new one, reconciling the stability of task-level optimization with the flexibility of per-query adaptation. The method achieves strong results on GPQA (62.8%, +1.5% over prior best AFlow) while being substantially more cost-efficient ($1.38 training cost vs. $20.14 for AFlow).

## Strengths

- **Cost-accuracy Pareto improvement on GPQA (Table 2)**: ASPEC achieves the highest GPQA accuracy (62.8%) among all compared methods while incurring the lowest inference cost ($0.88) — lower than even single-agent baselines like CoT-SC ($0.85) — and a training cost of $1.38 (roughly 1/15th of AFlow's $20.14 and 1/2.5 of MaAS's $3.43). This directly substantiates the paper's central claim of reconciling effectiveness with efficiency.

- **Component-level ablation cleanly isolates each mechanism's contribution (Table 6, lines 197–209)**: Removing specialist operators drops accuracy by 5.4% (62.8% → 57.4%) and nearly triples cost ($0.88 → $2.26); removing the meta-controller keeps accuracy flat (62.7%) but raises cost 2.3×; removing specialist memory drops accuracy to 61.4%. These ablations quantify each claimed benefit — persistent specialist expertise (accuracy gain), lightweight gating (cost saving), and memory (additional accuracy) — with no confounded component.

- **Cross-trial convergence of discovered archetypes on narrow domains (Figure 7, lines 232–237)**: Over five independent runs on GPQA, the discovery process independently converges on the same core roles (chemistry, biology, physics), while on broad-domain MMLU it appropriately diverges. This provides direct evidence that the evolutionary discovery process is reproducible and adapts its behavior to domain specificity.

- **Cross-model and cross-domain transferability (Figure 5, lines 158–165)**: ASPEC improves accuracy over three different backbone LLMs (Gemini 2.0 Flash, GPT-4o-mini, Llama 3.3 70B), showing the framework's benefits are not tied to a particular base model.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
- **The ONLYSPEC transfer result (Figure 5, right) is discussed too briefly and the explanation is thin.** The paper shows that when the operator pool is "restricted exclusively to specialists trained on a different source domain" (e.g., MATH-trained specialists for HumanEval), this ONLYSPEC configuration "matches or even slightly exceeds the performance of the full system" (lines 171–173). The paper's explanation — "T-shaped reasoning strategies" and "forcing utilization of these expert reasoning archetypes" — is speculative and does not seriously analyze what this implies about the nature of specialization. If cross-domain specialists match the full system (which includes both specialists and generalist base operators), the role of domain-specific cultivation needs sharper qualification. This does not invalidate the paper's contributions but warrants a more nuanced discussion.

- **Main results (Table 1) lack statistical significance or variance estimates.** Many of ASPEC's gains over strong baselines are modest: +1.5% over AFlow on GPQA (61.3 → 62.8), +1.3% over EvoAgent (61.5 → 62.8), +1.2% on average score over AFlow (68.4 → 69.6). No confidence intervals, standard deviations, or number of runs are reported for the primary benchmark comparisons. The sensitivity analysis (Figure 6) reports means over 4 runs for parameter sweeps, but this practice is not extended to Table 1. Given that ASPEC involves stochastic components (LLM-based Architect, evolutionary search, learned policy), variance estimates would significantly strengthen the reader's confidence in the reported improvements.

- **The Architect's LLM backbone is not explicitly identified.** Line 133 states "Gemini 2.0 Flash" is the "standard execution model across all methods," while the Architect is separately described as "an in-context learning LLM" (line 55). Since the Architect's generative and evaluative capabilities directly determine the quality of discovered specialists, it should be stated unambiguously whether the same Gemini 2.0 Flash model plays this role. "Standard execution model across all methods" strongly implies it does, but the separate framing creates unnecessary ambiguity.

### Trivial
None.

## Nice-to-Haves
- A more detailed analysis of specialist memory contents (e.g., comparing domain-specific vs. domain-general knowledge stored) would strengthen the specialization claim and could clarify the ONLYSPEC result.
- The meta-controller's reward function, while presumably detailed in Appendix Algorithm 2 (stripped by parser), could be briefly specified in the main text for improved self-containedness.

## Removed Points
The following points from the Harsh Critic were considered but removed:
- **Meta-controller training procedure not described (removed)**: The paper explicitly references "trains the meta-controller (Figure 3 and Algorithm 2)" — Algorithm 2 is in the appendix, which is stripped by the parser. Per guidelines, appendix content should not be penalized.
- **Training data for Discovery/Cultivation not clearly scoped (removed)**: The paper references "Further details on the dataset statistics are in Appendix F." Details about train/evaluation splits for each benchmark are in the stripped appendix.
- **ONLYSPEC "undermines the paper's core claim" framing (removed)**: The characterization that this result "undercuts the central claim" is an overreach. The paper offers a plausible explanation; the result is better framed as an interesting finding warranting deeper analysis rather than a fatal contradiction.
- **Confusion matrix formatting issue (removed)**: The critic themselves noted this "may be a parsing artifact."

## Novel Insights
None beyond the paper's own contributions. The reviews did not surface additional novel observations beyond what the paper presents.

## Suggestions
1. **Add variance reporting to Table 1**: Report confidence intervals, standard deviations, or at minimum state the number of runs and report the range observed. This is especially important given the modest margins over strong baselines.
2. **Expand analysis of the ONLYSPEC result (Figure 5, right)**: Investigate whether cross-domain specialists learn domain-general reasoning strategies or whether the cultivation process produces prompts that happen to transfer. A memory content comparison (in-domain vs. out-of-domain) would be illuminating.
3. **Explicitly identify the Architect LLM** and confirm if it is the same as the "standard execution model" (Gemini 2.0 Flash).
4. Briefly describe the meta-controller reward function and training algorithm in the main text.

## Score and Decision

**Calibration note**: The calibration dataset was not accessible for retrieval-based anchoring. The score below is based on direct assessment of the paper against ICLR standards.

This paper makes a genuine contribution: it tackles a well-motivated problem, proposes a clean architecture, supports it with thorough ablations, and demonstrates a meaningful cost-accuracy Pareto improvement. The weaknesses are minor (thin discussion of one ablation, missing variance estimates, one ambiguous specification) and do not threaten the core claims. The paper is clearly above the borderline threshold.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>