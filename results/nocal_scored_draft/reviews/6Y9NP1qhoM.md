Now I have all the evidence I need. Let me write the final consolidated review.

---

## Summary

This paper tackles misinformation injection in LLM-based Multi-Agent Systems (MAS), introducing ARGUS — a two-stage, training-free defense framework that first adaptively localizes critical communication channels where misinformation may flow and then uses goal-aware Chain-of-Thought reasoning to rectify the misinformation. The authors also contribute MISINFOTASK, a dataset of 108 complex multi-step tasks with curated misinformation arguments and ground truth. Experiments across 4 LLMs, 3 attack types, and 5 topologies show consistent improvements in reducing misinformation toxicity and improving task success rates under attack.

## Strengths

- **Well-motivated problem with clear differentiation.** The paper correctly identifies that prior MAS injection research focuses on overtly malicious/jailbreak content, while the more subtle threat of covert misinformation (semantically benign but factually wrong) is under-studied. This distinction is clearly articulated in Section 1 and Figure 1.

- **Principled two-stage defense design.** Decomposing the problem into adaptive localization (spatial analysis + dynamic re-localization based on inferred misinformation goals) and goal-aware persuasive rectification is a coherent approach to the chicken-and-egg problem of not knowing where misinformation will flow before it flows. The spatial→temporal framing is well-structured.

- **MISINFOTASK fills a genuine gap.** The dataset provides 108 realistic multi-step tasks with 4–8 curated misinformation arguments across five categories (Conceptual Reasoning, Factual Verification, Procedural Application, Formal Language Interpretation, Logic Analysis), moving beyond the simple QA tasks used in prior MAS injection evaluations.

- **Ablation studies are present and reasonably thorough.** Table 2 ablates three submodules (Dynamic Localization, CoT Revision, Multi-Turn Correction), and Table 3 ablates the three scoring weights. The "w/ Ground Truth" condition (Table 2) provides a useful upper bound showing clear room for improvement.

- **Consistent improvement across diverse conditions.** Across 4 LLMs (including non-OpenAI models DeepSeek-V3, Gemini-2.0-flash), 3 attack types, and 5 topologies, ARGUS consistently improves over both baselines (Self-Check, G-Safeguard). The pattern is clear and systematic.

## Weaknesses

### Fatal
None.

### Major

- **Same-model-family evaluation confound.** The LLM judge (GPT-4o-2024-08-06) is from the same model family as two of the four tested core LLMs (GPT-4o, GPT-4o-mini). LLM-as-judge systems are known to exhibit self-enhancement biases, preferring outputs from their own model family. The paper does not acknowledge or discuss this concern. *Mitigation:* Results are consistent across non-OpenAI models (DeepSeek-V3, Gemini-2.0-flash), suggesting the bias is not the sole driver. But a clean evaluation requires either an independent evaluator from a different family or an explicit analysis of the potential bias magnitude.

- **Key hyperparameters undisclosed, preventing full reproducibility.** The following values are never specified in the paper: **k** (number of monitored edges, used throughout Section 4.1), **θ_m** (TSR threshold in Eq. 1), **θ_sim** (similarity threshold in Eq. 6), and the **default values for α, β, γ** (the composite score weights ablated in Table 3 but never given as defaults). These are not minor implementation details — they are essential design parameters that determine the method's behavior and cost-effectiveness trade-off.

- **No variance or statistical significance for main results.** The subscripts in Table 1 are deltas from the Attack-only baseline, not measures of variance. The paper mentions "three independent experimental trials" only for Figure 2, not for Table 1. With N=108 tasks, the reader cannot assess whether the reported improvements (e.g., 10.33% TSR improvement) are statistically reliable or driven by a small number of outlier tasks.

### Minor

- **Figure 5 contradicts the "contagious amplification" narrative.** The paper claims (Section 5.2) that "the system's MT progressively escalates with an increasing number of rounds, which underscores the contagious and insidious nature of misinformation attacks." However, for **Tool Injection without any defense**, MT drops from ~4.5 (Round 1) to ~2.2 (Round 3+), showing substantial natural recovery. This directly contradicts the blanket "progressive escalation" claim and is never discussed. It also raises a question about how much of ARGUS's apparent benefit for Tool Injection is genuine correction versus coinciding with natural recovery.

- **Adaptive re-localization has an inherent one-round lag.** Eq. 9 selects top-k edges for round *r* using scores computed from round *r-1*. If misinformation propagates rapidly (in a single round), the defense is always one step behind. The paper does not discuss this latency or its practical consequences.

- **Frequency score (β) contributes negligibly.** Table 3 shows that removing β barely changes MT (3.76 vs. 3.73 with full ARGUS) — a ~0.03 difference that is likely within noise. The paper notes that "information relevance is the most critical factor" but does not discuss the near-irrelevance of the frequency dimension, despite it being a named component of the scoring framework.

- **MT metric operationalization gap.** The Misinformation Toxicity metric (Eq. 1) measures alignment with the misinformation's *intent-driven goal* (was the output what the misinformation wanted?), not divergence from factual truth. While this is a reasonable operationalization of "being successfully misled," the gap between these two constructs deserves explicit discussion given the paper's definitional emphasis on factual incorrectness.

### Trivial

- **Two different numbers for MT reduction given without explanation.** The Abstract reports "approximately 28.17%" (which matches Section 5.2's average across attack types: 28.18%, 20.38%, 35.95%), while Section 1 reports "approximately 38.24%" (which uses a per-LLM aggregation). Explaining the aggregation method would avoid reader confusion.

## Nice-to-Haves

- A cross-check using an evaluator LLM from a different family (e.g., Claude, Gemini) would resolve the self-enhancement bias concern cleanly.
- Sensitivity analysis for **k** (number of monitored edges) would clarify the cost-effectiveness trade-off and help practitioners configure the method.
- At least one qualitative example of a corrected message and one failure case of ARGUS would significantly improve reader understanding of the rectification process.
- Adding variance estimates (even across 3 trials with N=108 tasks) would substantially strengthen the quantitative evidence.

## Removed Points

The following points from the input review were removed after cross-verification against the paper:

- *"Blurred distinction between misinformation and injection attacks"* — **Removed:** This misunderstands the paper. The three injection methods (Prompt Injection, RAG Poisoning, Tool Injection) are delivery mechanisms; the *content* injected is the misinformation arguments from MISINFOTASK. The paper does not claim these attacks are specific to misinformation — they are standard attack vectors used to introduce the misinformation content.

- *"Dataset is too small (108 tasks)"* — **Removed:** Generic criticism not well-justified for a specialized, hand-curated dataset of complex multi-step tasks with 4–8 argument sets each. Each task involves multi-round MAS interactions generating substantial evaluation data. The paper is explicit about the dataset's scope and construction methodology.

- *"Section 2.3 defines truth relative to LLM beliefs"* — **Removed:** Over-extrapolated. The definition is operational for LLM-based systems (aligning with the paper's focus), and the dataset provides explicit human-curated ground truth. The scenario where an LLM's parametric knowledge contradicts the dataset's ground truth is a corner case not central to the paper's claims.

- *"Explicit calculation of per-attack averages should be shown"* — **Removed:** The calculation is straightforward from Table 1; the paper's claim (28.18%, 20.38%, 35.95%) is verifiable.

## Novel Insights

Beyond the paper's own contributions, the reviews surface an important nuance: the Tool Injection temporal pattern (Figure 5) shows that not all misinformation in MAS amplifies monotonically — some attack types naturally recede through agent deliberation. This undermines the paper's simple "contagious amplification" narrative and suggests that future work on MAS misinformation defense should contextualize defense gains against natural recovery baselines rather than assuming monotonic deterioration.

## Suggestions

1. **Use an evaluator from a different model family** (e.g., Claude or Gemini) as a cross-check for MT and TSR scoring, to rule out self-enhancement bias.
2. **Disclose all withheld hyperparameters:** k, θ_m, θ_sim, and default α, β, γ values. Additionally report variance across multiple trials.
3. **Explicitly discuss the Tool Injection temporal pattern** from Figure 5 — either explain why natural recovery occurs, or acknowledge that the defense's measured benefit for this attack type is partially coincident with it.
4. **Add at least one qualitative example** showing a corrected message and a case where ARGUS failed.
5. **Clarify the aggregation method** for the two MT reduction numbers (28.17% vs 38.24%).

## Score and Decision

The paper addresses a timely and genuine problem with a well-structured defense framework and a useful dataset. The experimental results are impressively consistent across multiple LLMs, attack types, and topologies. However, the evidence is weakened by three substantive issues: the evaluator self-enhancement confound, missing hyperparameters that prevent full reproducibility, and the absence of variance or significance reporting. These are evidential and methodological rather than structural — the approach itself is sound and the contributions are real — but in its current form the paper does not provide fully convincing quantitative support for its claims. With the suggested additions (independent evaluator, full parameter disclosure, variance reporting), this could become a solid contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>