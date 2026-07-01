## Summary

This paper proposes **Agentic Reinforced Policy Optimization (ARPO)**, an RL algorithm for training LLM-based agents that interact with external tools across multiple turns. The key insight — supported by a pilot entropy study — is that token-level entropy spikes sharply after tool-call feedback, and this signal can be used to trigger adaptive branching during rollout. ARPO combines an entropy-based adaptive rollout mechanism (which balances global trajectory-level sampling with step-level branching at high-entropy points) with advantage attribution estimation. Experiments across 13 benchmarks (math reasoning, knowledge-intensive QA, deep search) show ARPO consistently outperforming trajectory-level RL methods such as GRPO, DAPO, and REINFORCE++, while using fewer tool calls.

## Strengths

1. **The entropy-based motivation is genuinely novel and well-supported.** The pilot experiment (Section 2, Figure 2) showing that token entropy spikes in the first 10–50 tokens after tool-call feedback — and that this spike often exceeds the initial prompt uncertainty — is a clean, reproducible observation that directly motivates the method. This is a real insight about LLM-agent behavior that prior work has not exploited.

2. **The adaptive rollout mechanism is technically sensible and concretely specified.** The design (Section 3.1) — reserving a budget for partial sampling, monitoring entropy variation after each tool call, and branching when ΔH_t exceeds a threshold — is a clear, implementable proposal. The use of a linear probability model P_t = α + β·ΔH_t with threshold τ is simple and appropriate for a first exploration of this idea.

3. **The evaluation is broad and internally consistent.** Evaluation across 13 benchmarks spanning math reasoning, knowledge-intensive QA, and deep search is genuinely comprehensive. Comparisons use the same backbone models (Llama3.1-8B, Qwen2.5-7B, Qwen3-8B/14B) against GRPO, DAPO, and REINFORCE++, plus prompted baselines for deep search. Results show a consistent advantage for ARPO across nearly all settings.

4. **The tool-call efficiency result is practically significant.** Figure 7a shows ARPO using substantially fewer tool calls than GRPO during training while achieving higher accuracy. Given that tool calls are expensive, this is the kind of finding that would directly influence practitioners.

5. **Reporting Pass@3 and Pass@5 alongside Pass@1** (Figure 6) for search-heavy tasks is good practice and the scaling trends are informative.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **The "half the tool-use budget" claim is overstated.** The paper states in the abstract, contributions, Section 5.2, and conclusion that ARPO uses "only half" the tool calls of GRPO. However, Figure 7a shows ARPO using ~250–300 tool calls versus GRPO using ~400–450 — a reduction of roughly 30–40%, not 50%. While ARPO is clearly more tool-efficient, the repeated "half" framing overstates the measured advantage.

2. **No statistical significance or variance measures are reported.** Results in Tables 1 and 2 (and all figures) are presented as single numbers without standard deviations, confidence intervals, or multiple-seed runs. For comparisons with narrow margins (e.g., Qwen2.5 on GSM8K: ARPO 92.2 vs. GRPO 92.8; on MATH: ARPO 88.8 vs. GRPO 87.8), the reader cannot assess whether these differences are meaningful or within noise. The tool-call efficiency plot (Figure 7a) and rollout diversity analysis (Figure 7b) are also presented as single observations. *Note: single-run evaluation is common in large-scale RLVR, which tempers the severity of this issue, but given the paper's fine-grained claims about efficiency and diversity, some variance estimate would substantially strengthen confidence.*

3. **The Advantage Attribution framing somewhat overclaims novelty.** The paper presents advantage attribution estimation as a core contribution (abstract and contribution list). However, the adopted "soft" setting (Section 3.2) retains the original GRPO loss formulation, as the paper itself acknowledges (line 142: "While we retain the original GRPO loss formulation…"). The "hard" setting is a genuinely different formulation but is rejected as less stable (Figure 5). The paper would be more accurate framing the contribution as "GRPO combined with entropy-based adaptive rollout" rather than suggesting a new credit-assignment method.

4. **The GPG Theorem (Section 3.3) is tenuously connected to the method's specific innovation.** The theorem states that any differentiable Transformer-based policy can be optimized using macro-action segments — a general statement about segment-level gradients that does not specifically justify entropy-based branching. The claim that "ARPO, as an advanced implementation of the GPG Theorem, provides a robust theoretical foundation" (line 170) overstates the theorem's role. The paper's real theoretical contribution is the entropy-based motivation, not this theorem.

5. **Key hyperparameter values are not reported in the main text.** The entropy-based adaptive beaming (Equation 2) depends on α (base sampling probability), β (stability entropy), τ (branching threshold), Z (number of branches per trigger), k (number of initial tokens for entropy computation), and rollout budgets M and N. None of these are given numerical values in the main text. Sensitivity to τ is particularly important, since it directly controls when branching occurs. These values are presumably in the appendix, but their absence from the main text weakens the paper's self-containedness.

### Trivial
- The abbreviation **"S-Co"** appears in the Figure 1 tool-call efficiency plot but is never defined in the paper body.

## Nice-to-Haves
- **Ablation of the entropy signal itself:** The core claim is that branching at high-entropy points helps. An ablation where branching is triggered by a random signal (same budget, same structure, not entropy-informed) would directly test whether the benefit comes from the entropy signal or simply from having finer-grained exploration at tool-call steps.
- **Behavioral analysis:** The rollout diversity analysis (Figure 7b) shows cluster counts, but it would be informative to know what specific tool-use behaviors ARPO discovers differently — different search queries? different tool orderings?

## Removed Points
These points were flagged by reviewers but are removed with justification:
- *"Advantage Attribution Estimation is not a novel contribution at all"* — The paper is transparent that soft=GRPO (line 142); the hard setting IS a distinct formulation even if not used as default. The criticism overstated the issue. A softened version about overclaiming is retained above.
- *"TIR prompting characterization is misleading"* — The paper says "marginal or even inferior." The results are mixed (Llama3.1 improves 28.8→36.3, Qwen2.5 slightly decreases 32.0→31.0). This is a reasonable characterization of mixed results.
- *"LLM-as-Judge may have evaluation bias"* — Speculative without evidence. Using a held-out judge model for open-ended tasks where exact matching is infeasible is standard practice.
- *"No analysis of what ARPO learns differently"* — A valid suggestion for future work, not a weakness of the current paper.
- *"Missing related works"* — Cannot be verified without external sources.
- *Formatting/style nitpicks and reproducibility complaints about undisclosed hyperparameters in the appendix* — The appendix is stripped by the PDF parser; these details exist in the original submission.

## Novel Insights
The most insightful observation from the review process is that the entropy-spike-after-tool-call phenomenon (Section 2) is the paper's strongest card — it is a genuinely underexplored signal in agentic RL, and the paper identifies it clearly. However, the review reveals that the paper could strengthen its case significantly by (a) running an ablation that replaces the entropy signal with a random branching signal of equal frequency, and (b) adding variance estimates for the small-margin comparisons. The overclaiming around the advantage estimation and GPG theorem is a presentation issue, not a method flaw — stripping those frames would make the entropy-driven rollout contribution stand out more clearly.

## Suggestions
1. **Correct the "half" claim** to something like "~30–40% fewer tool calls" or report the exact measured reduction.
2. **Add error bars or multiple-seed results** for the main comparisons in Table 1 and the tool-call efficiency analysis.
3. **Reframe the contributions** to center on the entropy-based adaptive rollout mechanism, and either cut Section 3.3 or honestly frame it as a general remark about segment-level gradients.
4. **Report hyperparameter values** (α, β, τ, Z, k, M, N) in the main text or add a brief sensitivity analysis.
5. **Add an ablation** with random (non-entropy) branching at the same frequency.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>