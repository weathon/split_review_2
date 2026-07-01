## Summary

The paper proposes Agentic Reinforced Policy Optimization (ARPO), an RL algorithm tailored for multi-turn LLM agents that use external tools. ARPO introduces an entropy-based adaptive rollout mechanism that branches sampling at high-entropy tool-call steps to encourage step-level exploration, combined with advantage attribution estimation for finer-grained credit assignment. Experiments across 13 benchmarks (mathematical reasoning, knowledge-intensive QA, and deep search) show consistent improvements over trajectory-level RL baselines (GRPO, DAPO, REINFORCE++) while using roughly half the tool-use budget.

## Strengths

- **Novel and well-motivated problem framing.** The paper identifies a genuine gap: current agentic RL methods treat tool-use trajectories as monolithic sequences, ignoring the increased uncertainty that tool feedback introduces. The entropy pilot experiment (Section 2) clearly demonstrates that token entropy spikes after tool calls, providing a strong motivation for step-level exploration.
- **Consistent empirical gains across diverse settings.** ARPO outperforms GRPO, DAPO, and REINFORCE++ on 10 benchmarks with Qwen2.5-7B and Llama3.1-8B, and on 4 deep search benchmarks with Qwen3-8B/14B (Tables 1 and 2). The improvements are not limited to one backbone or task type, supporting the method’s generality.
- **Impressive tool-use efficiency.** Figure 7 shows ARPO achieves higher accuracy than GRPO while using about half the number of tool calls during training. This is practically important because tool calls are computationally expensive in real agent deployments.
- **Clear exposition and visual aids.** Figures 3, 4, and 7 nicely illustrate the adaptive rollout mechanism, advantage attribution, and the diversity advantage of ARPO. The writing is generally easy to follow.

## Weaknesses

### Major

1. **Lack of statistical rigor.** Primary results (Tables 1, 2) are reported as single numbers without error bars, standard deviations, or multiple random seeds. RL training is inherently noisy; without variance estimates, the reported gains (often 1–4%) may not be statistically significant. This weakens confidence in the conclusions.

2. **Theoretical contribution is thin.** The Generalized Policy Gradient Theorem (Eq. 6) restates that policy gradient applies to macro-actions (contiguous token segments). This is a standard observation from hierarchical RL/macro-action literature and does not uniquely justify ARPO’s entropy-based adaptive branching. The connection between the theorem and the specific branching rule (Eq. 2) is not formally established; the theory is presented as justification after the fact.

3. **Hyperparameter sensitivity is not explored in the main text.** The entropy-based branching depends on α, β, τ, and the branching budget Z. The paper references an ablation appendix, but the main paper provides no analysis of how these choices affect performance or tool-use cost. A method that introduces several new hyperparameters should include sensitivity analysis to demonstrate robustness.

4. **Limited scope of the entropy analysis.** The pilot experiment (Section 2) measures entropy for only two agents (search engine, Python interpreter) and does not systematically vary the model size, the type of tool feedback, or the task domain. The generality of the “high entropy after tool calls” observation across diverse scenarios is asserted but not thoroughly validated.

### Minor

5. **Inconsistent benchmark labels in Figure 1.** The bar chart labels (e.g., “General M. Answer (SQuAD)”, “Primary + Last Exac (SQuAD)”, “W.W. WalkerQV”) do not match the dataset names in the main tables (WebWalkerQA, HLE, GAIA, etc.), causing confusion.

6. **LLM-as-Judge evaluation.** Several deep search results use a judge model for evaluation, which can introduce systematic bias. The paper does not provide human correlation or agreement analysis for this metric.

7. **Overstated phrasing.** The word “pioneeringly” for quantifying token entropy in agents is too strong given existing entropy-based analyses in RLVR (Wang et al., 2025b;c; Cheng et al., 2025), which the paper itself cites.

### Trivial

8. Code link is a placeholder. This is minor but should be resolved for camera-ready.

## Nice-to-Haves

- Add error bars (e.g., over 3–5 seeds) to Tables 1 and 2.
- Include a sensitivity study for α, β, τ, and Z in the main paper.
- Compare ARPO with a variant that uses random branching (instead of entropy-based) to isolate the benefit of the entropy signal.
- Show entropy histograms for more models (e.g., Llama3.1) to strengthen the generality of the motivation.
- Provide a small human evaluation for the LLM-as-Judge results on deep search tasks.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that token-level entropy after tool feedback is a useful, inexpensive signal for identifying decision points where the LLM’s uncertainty is high, and that branching at those points leads to more diverse and effective tool-use behaviors. This insight connects a simple uncertainty measure (token entropy) to a concrete algorithmic improvement in agentic RL, and it is convincingly supported by the rollout diversity analysis (Figure 7b) showing denser, more separated clusters with ARPO.

## Suggestions

- Report all main results with mean and standard deviation across at least 3 random seeds.
- Add a hyperparameter sensitivity table in the main paper (even if brief) covering α, β, τ, and Z, showing impact on accuracy and tool-call count.
- Clarify the normalization step in the entropy variation calculation (ΔH_t) and the selection of the threshold τ.
- Replace the vague benchmark labels in Figure 1 with the actual dataset names used in the tables.
- Provide a brief discussion of when ARPO might underperform (e.g., very short trajectories, deterministic tool feedback) to set expectations.

## Score and Decision

The paper tackles an important, practical problem (training multi-turn tool-use agents) with a well-motivated and empirically effective solution. The entropy-driven adaptive rollout is novel, and the results consistently beat strong baselines with better tool efficiency. However, the lack of statistical rigor (no error bars) and limited hyperparameter analysis are notable weaknesses that reduce confidence. The theoretical contribution is incremental but not harmful. On balance, the paper is a solid contribution that merits acceptance.

MY FINAL SCORE: 7<score>7</score>
MY FINAL DECISION: Accept