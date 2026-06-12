## Summary

This paper addresses the underexplored problem of output volatility in LLM long-form generation—where models produce inconsistent outputs across multiple runs from the same prompt. The authors introduce VOLTBench, a heterogeneous-task benchmark that quantifies length volatility across structured and unstructured tasks in multiple languages. Through attention trace analysis, they identify internal failure patterns (Attention Collapse, Attention Instability), and propose SELB, a training-free decoding strategy that boosts logits to enforce structural constraints and suppress failure tokens, reporting 148% improvement in mean output length and 69% reduction in volatility.

## Strengths

- **Genuinely novel problem framing.** The paper convincingly argues that existing long-form generation research focuses almost exclusively on single-generation quality while overlooking multi-sample volatility. This is a real and practically important gap—unpredictable output lengths directly impact computational costs and deployment reliability. Figure 1 and the experimental results (e.g., LongWriter-8B with standard deviation at 103% of mean length) provide compelling evidence that this is a widespread and severe issue.

- **Well-designed benchmark with clear differentiation from prior work.** VOLTBench's multi-dimensional design (task type × language × instruction complexity × output format) and its explicit inclusion of multiple sampling and stability evaluation represent genuine advances over existing benchmarks as summarized in Table 1. The inclusion of structured tasks (code, math) with execution-based verification addresses a real limitation of prior work that relied on subjective LLM-as-a-Judge evaluation. The chapter-based scalability design enabling 100k-word evaluation is ambitious and useful.

- **Effective and practical mitigation method.** SELB is elegant in its simplicity—it requires no additional training, operates purely at decoding time, and combines structural enforcement with proactive failure prevention. The empirical results are strong: on Qwen2.5-7B, LVC drops from 45.4% to 14.02% and MLA improves from 31.6% to 78.25%. The method generalizes across multiple base models (Qwen2.5-7B, Qwen3-8B, Llama-3.1-8B) as shown in Figure 5, and the SELB-Hybrid extension for free-form generation (Appendix I) demonstrates meaningful generalization.

- **The attention trace analysis provides useful mechanistic insight.** Identifying "Attention Collapse" and "Attention Instability" as distinct failure signatures, with visual evidence in Figure 4, offers interpretable explanations for why models fail at long-form generation. The connection between periodic attention spikes and section-boundary maintenance is a genuinely interesting observation.

## Weaknesses

### Fatal
None.

### Major

- **Limited experimental scope for SELB evaluation.** The main SELB results (Section 6.3) are reported only on "a 100-section task under simple settings." This is a narrow evaluation given that VOLTBench spans multiple task types, languages, complexity levels, and length scales. The paper does not provide systematic results across different tasks, languages, or instruction complexities for the proposed method. The generalization claims would be substantially stronger with broader evaluation, especially since the benchmark was designed with this multi-dimensional coverage in mind.

- **The hyperparameter sensitivity and design choices of SELB are underexplored.** Key parameters like τ_max (target section length threshold), β (boosting constant), and the banned token set V_banned are not thoroughly analyzed. How sensitive is performance to these choices? What happens with different values of β? The method essentially requires the user to specify section-level structure, which limits applicability to tasks without explicit section divisions (though SELB-Hybrid partially addresses this). The "proactive failure prevention" component relies on a manually curated ban list of conversational filler phrases, which raises questions about portability across models and domains.

- **Quality evaluation methodology has limitations.** For unstructured tasks, UCA relies on LLM-as-a-Judge, which is acknowledged as standard practice but introduces potential bias. More importantly, the quality metrics are reported for only a single task type per category (Story for unstructured, Code Function for structured in Table 2), making it unclear whether quality improvements hold consistently across VOLTBench's diverse tasks.

### Minor

- **The connection between attention traces and SELB is not tight.** The paper identifies attention patterns (Section 5) as root causes of volatility, but SELB (Section 6) does not directly use attention signals at inference time—it uses structural enforcement and token banning. The logical chain from "we observed attention collapse" to "we boost logits for section titles and ban filler phrases" has a gap. A more direct connection—for instance, monitoring attention traces at inference and triggering interventions—would strengthen the narrative.

- **N=5 for multiple sampling seems low.** Computing volatility metrics (LSD, LVC) with only 5 samples provides limited statistical reliability. The paper does not discuss whether results are stable across different random seeds or how many samples would be needed for reliable volatility estimation.

- **The free-form generation results (Section 6.4) are deferred entirely to the appendix.** Given that this is a significant generalization claim, the main paper would benefit from at least a summary table of these results.

### Trivial
None.

## Nice-to-Haves

- A comparison of SELB against reinforcement-learning-based approaches like LongWriter-Zero in terms of computational cost and effectiveness.
- Analysis of whether the identified attention patterns correlate with specific model architectures or sizes.
- Discussion of how SELB interacts with different context window sizes, particularly as outputs approach context limits.

## Novel Insights

The identification of distinct internal volatility patterns—"Attention Collapse" (gradual loss of constraint attention leading to premature termination) and "Attention Instability" (sudden anomalous attention spikes leading to structural skipping)—through systematic attention trace analysis across multiple generation runs is a genuinely novel contribution. The observation that periodic attention spikes serve as "refocusing signals" at section boundaries, and that the failure of these signals precedes generation breakdown, provides an interpretable mechanistic framework that could inform future work on controllable generation beyond just the length volatility problem studied here.

## Suggestions

- Expand SELB evaluation to cover all dimensions of VOLTBench (language, complexity, structured vs. unstructured, varying lengths) to justify the generalization claims implied by the benchmark design.
- Include hyperparameter sensitivity analysis for τ_max, β, and the banned token set in the main paper.
- Strengthen the connection between the diagnostic (attention traces) and the intervention (SELB) by either using attention signals in the decoding strategy or explicitly discussing why a simpler heuristic approach suffices despite the attention-level diagnosis.

## Score and Decision

The paper presents a well-motivated, practically important problem with a thoughtfully designed benchmark and an effective, lightweight solution. The problem of output volatility in long-form generation is genuinely underexplored, and VOLTBench with its multi-dimensional design represents a meaningful contribution. SELB is effective and practical, though its evaluation is narrower than the benchmark it was designed for. The attention trace analysis provides useful mechanistic insight even if the bridge to the mitigation method is not fully tight. The main weakness is the limited scope of SELB's experimental evaluation relative to the benchmark's breadth.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>