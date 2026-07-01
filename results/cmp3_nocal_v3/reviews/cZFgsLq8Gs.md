## Summary

This paper presents DeepScientist, a large-scale autonomous AI system for goal-oriented scientific discovery that operates over month-long timelines. The system formalizes discovery as a Bayesian optimization problem with a persistent Findings Memory, iterating through a three-stage cycle (hypothesize, implement, analyze). Run on 16 H800 GPUs for ~20,000 GPU hours, it generated ~5,000 ideas, executed ~1,100 experiments, and produced methods that improved upon human-designed SOTA baselines on three AI tasks: Agent Failure Attribution, LLM Inference Acceleration, and AI Text Detection. The paper provides transparent analysis of the discovery funnel and reports that only ~21 ideas yielded genuine progress, with ~60% of failures due to implementation errors.

## Strengths

1. **Unprecedented scale of autonomous discovery demonstration.** The system ran a month-long autonomous cycle across 16 H800 GPUs, consuming 20,000 GPU hours, generating ~5,000 ideas, and executing ~1,100 experiments. This is a materially larger-scale demonstration than prior AI Scientist systems, which the paper correctly notes operate on narrower or more synthetic tasks (Section 4).

2. **Transparent accounting of the discovery funnel.** Section 4.3 transparently reports that only ~21 of ~1,100 implemented ideas produced real progress, and that ~60% of failures stemmed from implementation errors rather than flawed hypotheses. The paper also provides an ablation showing that random sampling of 100 ideas yields effectively zero success rate, validating the need for the selection mechanism.

3. **Genuinely novel discovery trajectories in AI Text Detection.** The progression from *T-Detect* → *TDT* → *PA-TDT* (Section 4.1), where each method identifies limitations of the previous one and shifts the conceptual framing from distributional statistics to time-frequency analysis, demonstrates the kind of progressive conceptual refinement one hopes to see from an automated discovery system. This trajectory achieves a 7.9% AUROC improvement (0.800 → 0.863) on the RAID benchmark with credible qualitative evidence (Figure 5 t-SNE visualization).

4. **Well-designed persistent memory architecture.** The Findings Memory that accumulates structured records across all stages (Idea, Implement, Progress) and supports periodic global synchronization across parallel instances (Section 4.3) is a sensible and non-trivial engineering contribution. The observation that shared knowledge across parallel threads yields super-linear wall-clock speedup is genuinely interesting.

## Weaknesses

### Fatal

None.

### Major

1. **The Bayesian optimization framing does not reflect the actual implementation (Section 3).** The paper claims to "formally model" discovery as a Bayesian Optimization problem with a "surrogate model" and "acquisition function." In practice, the surrogate model is an LLM prompted to assign three integer scores (0–100) for utility, quality, and exploration value — there is no Gaussian process, no posterior distribution, no uncertainty calibration, and no fitting of the surrogate to observed outcomes f(I). The "UCB" acquisition function uses all weights set to 1, removing any adaptivity. The system's actual value lies in its architectural choices (persistent memory, multi-stage filtering, parallel synchronized exploration), not in any Bayesian formalism. The paper should reframe its contribution around what the system actually does rather than claiming a mathematical rigor the implementation does not deliver.

2. **The "three years of human research in two weeks" comparison (Figure 1 and abstract) conflates incomparable quantities.** The left graph plots published methods from *multiple independent research groups* working over years with different compute budgets, team sizes, and methodological starting points. The right graph shows a single well-resourced system (16 H800 GPUs, two top-tier proprietary LLMs, 20,000 GPU-hours, three human supervisors) working on one problem for 15 days. These are fundamentally different quantities. A valid comparison would require measuring what a human research team with equivalent compute resources could achieve in two weeks on the same task. The current framing compares the field's cumulative output against a single focused effort and is misleading. This claim should be removed or substantially qualified.

3. **Missing error bars/variance on all main experimental results (Table 1, Section 4.1).** The central result table reports single point values for all three tasks with no confidence intervals, standard deviations, or multi-seed runs. For the LLM Inference Acceleration result (190.25 → 193.90 tokens/second, a 1.9% improvement), this is especially problematic — the improvement could easily fall within run-to-run noise. For the AI Text Detection result (the most credible finding), error bars would significantly strengthen the claim. Without uncertainty quantification, it is impossible to assess whether the reported improvements are statistically meaningful.

4. **The 183.7% improvement framing exploits a very weak baseline (Section 4.1, abstract).** The headline "surpassing human SOTA by 183.7%" corresponds to an absolute improvement from 16.67% → 47.46% accuracy on the Algorithm-Generated setting of Agent Failure Attribution. While the paper does report absolute numbers in the table, the abstract and introduction foreground only the relative percentage, which makes a weak baseline (16.67%) look like a major achievement. The paper should acknowledge that the "SOTA" baseline is itself quite weak and frame the improvement in absolute terms when stating headline results.

### Minor

5. **The scaling analysis (Figure 6) does not support the "near-linear" claim.** The experiment uses 5 data points (1, 2, 4, 8, 16 GPUs), of which the first two produce zero Progress Findings. The "near-linear" trend is therefore based on three non-zero points, and the data (0, 0, 1, 4, 11) looks plausibly *superlinear* (jumping from 4 to 11 when doubling from 8 to 16 GPUs). With only three informative data points and no error bars on this stochastic process, the "near-linear" claim is not robust. The paper should report this as suggestive rather than establishing a scaling law.

6. **No component-level ablations of the selection mechanism.** The paper provides one ablation showing the selection mechanism outperforms random sampling of 100 ideas (Section 4.3), which is useful. However, there are no ablations isolating the individual components: the surrogate model scores vs. simpler heuristics, the acquisition function weighting, or the memory synchronization scheme. Without these, it is unclear which architectural choices drive the system's performance.

7. **The human evaluation (Section 4.2) does not clearly establish reviewer independence.** The paper states it convened "a dedicated program committee consisting of three active LLM researchers: two volunteers who have served as ICLR reviewers and one senior volunteer who has been invited to be an ICLR Area Chair." It is not stated whether these volunteers are independent of the project or are collaborators/co-authors. Additionally, the cross-system comparison (Table 2) uses DeepScientist's 5 best papers (selected from 21 Progress Findings) against other systems' publicly available papers, which the paper itself acknowledges "may be curated." This double-curation issue means the 60% simulated acceptance rate is not a fair comparison.

### Trivial

None.

## Nice-to-Haves

- Conduct a proper component-level ablation study of the surrogate model, acquisition function, and memory synchronization to identify which design choices matter.
- Report multi-seed runs or confidence intervals for all main experimental results.
- Separate the compute cost of LLM inference (backbone model calls) from the cost of executing experiments.
- For the Agent Failure Attribution task, report the random-chance baseline so readers can contextualize the absolute accuracy numbers.

## Removed Points

*"The 12% baseline is barely above random."* — Speculative; the paper does not report the random-chance baseline for the Who&When benchmark, so this cannot be verified.
*"The paper mentions 'ablations' in passing (line 114) but presents none."* — Partially incorrect; Section 4.3 does contain an ablation (selection vs. random sampling). What is missing is component-level ablations, which is noted in Minor weaknesses above.
*Reviewer misattributed 183.7% improvement to the Handcraft setting (12.07% → 29.31%).* — The table shows 183.7% corresponds to the Algorithm-Generated setting (16.67% → 47.46%). The broader point about framing is retained.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Reframe the contribution around the system architecture (persistent Findings Memory, multi-stage filtering, parallel synchronized exploration) rather than the cosmetic Bayesian optimization framing.
2. Remove or substantially qualify the "three years of human research" comparison — present the AI Text Detection trajectory on its own merits with proper baselines.
3. Add confidence intervals or multi-seed variance to all main experimental results; if the LLM Inference Acceleration improvement is not statistically significant, demote it to supporting evidence.
4. Center the AI Text Detection trajectory as the flagship demonstration; the abductive reasoning around A2P for Agent Failure Attribution is also interesting but needs to acknowledge the weak baseline.
5. Clarify the independence (or disclose the relationship) of the human program committee reviewers.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>