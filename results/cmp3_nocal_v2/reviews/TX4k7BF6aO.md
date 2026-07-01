Now I have all the information needed. Let me write the consolidated review.

## Summary

This paper proposes Agentic Reinforced Policy Optimization (ARPO), an RL algorithm for training multi-turn LLM-based tool-use agents. The key idea is to measure token-level entropy spikes that occur after tool-call feedback and use these as signals to adaptively branch sampling at high-uncertainty steps, promoting step-level exploration of tool-use behaviors. ARPO combines this entropy-based adaptive rollout with the GRPO update objective. Experiments across 13 benchmarks (mathematical reasoning, knowledge-intensive QA, and deep search) show consistent gains over trajectory-level RL algorithms (GRPO, DAPO, REINFORCE++) while using fewer tool calls.

## Strengths

1. **Novel and well-motivated empirical observation (Section 2, Figures 1–4).** The paper documents that LLM token entropy spikes sharply in the first 10–50 tokens after tool-call feedback, and that this effect is stronger for search feedback than Python feedback. This is a concrete, measurable phenomenon that provides a clear and plausible motivation for why trajectory-level methods may miss useful exploration opportunities. The paper shows a word cloud (Figure 4b) of frequent high-entropy tokens (e.g., "now", "information", "find", "start") that are content-bearing reasoning tokens, not format artifacts.

2. **Adaptive branching is conceptually sound and directly motivated by the entropy observation.** Rather than treating all rollout steps uniformly, branching at points of high predictive uncertainty—where exploration is most likely to discover useful alternatives—is a sensible and well-justified heuristic.

3. **Extensive evaluation across 13 benchmarks with multiple backbones.** The paper tests ARPO against GRPO, DAPO, and REINFORCE++ using Llama3.1-8B, Qwen2.5-7B, and Qwen3-8B/14B across mathematical reasoning, knowledge-intensive QA, and deep search tasks (Table 1, Table 2). The improvements are consistent: ARPO achieves the best or second-best result on 18 of the 20 reported rows in Table 1.

4. **Tool-use efficiency is practically meaningful.** Figure 7a shows that ARPO achieves comparable or better accuracy while using roughly 30–40% fewer tool calls per training step than GRPO. This addresses a real cost bottleneck in agentic RL training.

## Weaknesses

### Fatal

None.

### Major

1. **The complexity claim is incoherent as stated.** Line 116 claims ARPO "reduces the computational complexity of each rollout from the trajectory-level RL's $O(n^2)$ to between $O(n \log n)$ and $O(n^2)$." Standard autoregressive generation is $O(n)$ per sequence—there is no baseline $O(n^2)$ term for single-sequence rollout. The paper never explains what $O(n^2)$ refers to (pairwise group computation in GRPO? something else?), and under ARPO's own accounting complexity can still be $O(n^2)$. This claim should either be substantiated with a precise derivation or removed. It does not affect the empirical results but is a misleading efficiency claim as currently written.

2. **The "hard advantage" formulation is underspecified.** Equation (4) in Section 3.2 gives $\hat{A}_{i,t} = \frac{r_t - \text{mean}(\{R_i\}_{i=1}^d)}{\text{std}(\{R_i\}_{i=1}^d)}$, where $r_t$ appears to be a token-level reward. However, the paper states that rewards are sparse and trajectory-level (Equation 5 defines a single reward $R$ per trajectory). There is no explanation of how $r_t$ (per-token) is derived from $R_i$ (per-trajectory). This is a genuine gap in the method description. That said, ARPO's default method uses the "soft" version (standard GRPO), so this gap does not affect the main experimental results—but it makes the hard advantage baseline non-reproducible.

### Minor

3. **The theoretical foundation (Section 3.3) is vacuous.** The "Generalized Policy Gradient Theorem" states that the policy gradient can be expressed using macro-actions (grouped token segments). Since the log-probability of a macro-action is simply the sum of log-probabilities of its constituent tokens, this is a direct consequence of the standard policy gradient theorem and provides no insight into why entropy-based branching is optimal or what guarantees ARPO offers. This section is presented as a "theoretical foundation" but does not do any analytical work.

4. **No statistical significance or variance reporting.** Several benchmarks have very small test sets (AIME has 30 problems, HLE has small questions), where a few correct answers shift percentages substantially. No confidence intervals, standard deviations, or multi-seed results are reported anywhere. The "average accuracy gain of 4%" claim (line 212) would benefit from some measure of variance given the small-n datasets.

5. **The "half the tool-use budget" claim is slightly overstated.** Figure 7a shows ARPO using roughly 250–350 tool calls vs. GRPO's 400–450 (a ~30–40% reduction, not exactly half). Furthermore, this analysis is only shown for one model (Qwen2.5-7B) against one baseline (GRPO), with no breakdown by dataset. The result is still practically meaningful, but the framing as "half" is imprecise.

6. **Missing hyperparameter values in the main paper.** The adaptive branching mechanism depends on $\alpha$ (base sampling probability), $\beta$ (stability entropy), $\tau$ (threshold), $k$ (number of initial tokens), $Z$ (branch paths), $N$ (global rollouts), and $M$ (total rollout budget). None of these values are reported in the main paper. While the appendix (which is stripped here) may contain them, the main text should at minimum summarize key values to allow readers to assess sensitivity.

### Trivial

None.

## Nice-to-Haves

- An ablation controlling for total sampling budget (matching total generated tokens rather than trajectory count) would cleanly isolate the benefit of adaptive branching from the benefit of having more total samples at high-entropy points.
- An analysis showing whether branched trajectories actually differ in their *tool-use choices* (tool selection, query formulation) vs. simply surface-form variations would strengthen the link between the entropy signal and the claimed exploration benefit.

## Removed Points

These points were raised in the input review but are removed as invalid, speculative, or not verifiable:

- **"Entropy may reflect format uncertainty rather than tool-use strategy uncertainty"** — Removed. This is speculative. The paper shows a word cloud (Figure 4b) with content-bearing tokens dominating, and explicitly attributes the effect to distributional shift (line 66–67). The entropy signal is used as a heuristic exploration criterion, not as a theoretical guarantee about what it "really" represents, so this does not undermine the method.

- **"Soft advantage estimation is just GRPO"** — Removed. The paper openly acknowledges this (line 142: "While we retain the original GRPO loss formulation"). The claimed contribution is the adaptive rollout mechanism, not a new loss function. The soft advantage is presented as the default choice for a reason.

- **"Figure 1 comparison across different model families/sizes is meaningless"** — Removed. The caption states the comparison is "using only 1k RL samples," so the purpose is to show sample efficiency, not controlled algorithmic comparison. The context clarifies the intent.

- **"DeepSearch evaluation: base model matches RAG"** — Removed. This is an observation about the data, not a methodological weakness. The base model may have been exposed to tool-use data during pre-training.

- **"Figure 7a lacks axis labels"** — Removed. The caption explicitly states: "Total Calls (Y-axis, 200 to 500) vs Step (X-axis, 0 to 100)." Axis labels are present in the caption.

- **"Entropy normalization dividing by V is problematic"** — Removed. The relevant text is garbled by the PDF parser and cannot be evaluated as written. This is a formatting artifact, not an author error.

- **"Missing ablation of entropy threshold τ"** — Removed. The paper states "More ablation and scaling analyses can be found in Appendix A.2." The appendix is stripped by the parser; penalizing the paper for missing appendix content is not appropriate.

- **"Computational overhead of entropy computation is not negligible"** — Removed. The paper explicitly notes this overhead is minor (footnote 1). Whether this is acceptable is a design judgment, not a factual error.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the complexity analysis or remove it.** Either provide a clear derivation of the claimed $O(n^2)$ baseline and how ARPO improves on it, or remove the complexity claim entirely. The empirical efficiency results (Figure 7a) are sufficient.

2. **Clarify the hard advantage formulation.** Specify how $r_t$ is derived from the trajectory-level reward $R_i$ (or acknowledge that it is not used in the default setting and provided only as an illustration).

3. **Report key hyperparameter values in the main paper.** At minimum: $\alpha$, $\beta$, $\tau$, $k$, $Z$, and the global/partial budget split.

4. **Remove or substantially revise the theoretical section.** The current GPG theorem is a trivial restatement. Either derive a nontrivial property of the entropy-based branching rule or drop the section entirely.

5. **Soften the "half the tool-use budget" claim** to reflect the actual ~30-40% reduction shown, or provide more comprehensive evidence.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>