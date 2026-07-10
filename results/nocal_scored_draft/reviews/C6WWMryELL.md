Now let me write the final consolidated review.

## Summary

This paper addresses the underexplored problem of length volatility in long-form LLM generation — i.e., the inconsistency in output length and content across multiple generations of the same prompt. It makes three contributions: (1) **VOLTBench**, a benchmark that systematically measures length volatility across structured and unstructured tasks with multiple dimensions (language, complexity, output scale up to ~100k words); (2) an **attention trace analysis** identifying "Attention Collapse" and "Attention Instability" as internal patterns preceding generation failures; and (3) **SELB** (Structural Enforcement via Logits Boosting), a training-free decoding strategy that enforces section boundaries and suppresses early termination.

## Strengths

- **The problem framing is well-motivated and identifies a genuine gap.** The paper convincingly argues that existing benchmarks focus on single-generation quality while overlooking multi-generation volatility — a practically important issue for production deployment (unpredictable token costs, reliability). This motivation is clearly articulated in Sections 1 and 3 and backed by concrete observations (e.g., Figure 1 showing LongWriter-8B's standard deviation reaching 103% of its mean length). [favorability: 1.00]

- **VOLTBench is a comprehensive benchmark with genuinely novel features.** The inclusion of multiple sampling (N=5 generations per prompt) and stability evaluation distinguishes it from all prior benchmarks (Table 1). Its design covers both structured tasks (code, math) and unstructured tasks, multiple instruction complexity levels, and bilingual (English/Chinese) evaluation — providing a significantly more complete evaluation framework than HelloBench, LIFEBench, LongGenBench, etc. The fine-grained constraint framework for automated quality assessment of unstructured tasks is a practical contribution. [favorability: 0.92]

- **The attention trace analysis offers an intuitively plausible qualitative account.** By plotting constraint-attention over token positions (Figure 4), the paper identifies "Attention Collapse" (near-zero attention → premature termination) and "Attention Instability" (erratic spikes → section skipping). These patterns provide a useful mechanistic story for otherwise opaque generation failures. [favorability: 1.00]

## Weaknesses

### Major

- **Misleading framing of SELB's headline improvement numbers.** The abstract and contribution list (Section 1, bullet 3) state that SELB "improves the mean output length of the base model by 148% and reduces the length volatility by 69%." However, Section 6.3 derives these numbers by comparing the SELB-equipped model against **LongWriter-8B** — a different model, not the same base model without SELB. SELB is applied to Qwen2.5-7B, Qwen3-8B, and Llama-3.1-8B (Figure 5), not to LongWriter-8B. Using within-model comparisons from Table 2 (e.g., Qwen2.5-7B: 445 words, 17.0% LVC), the actual improvements are ~3,418% length increase and ~17.5% volatility reduction — very different from the claimed 148% and 69%. Furthermore, Section 6.3 never specifies which model SELB is applied to for the reported metrics, using only the ambiguous phrase "our model." This framing does not meet the standard of clear, controlled experimental comparison and inflates the perceived effectiveness of the method. [favorability: 0.07]

- **No within-model controlled comparison or ablation of SELB's components.** The paper never presents a direct table comparing each base model (Qwen2.5-7B, Qwen3-8B, Llama-3.1-8B) with and without SELB on the same metrics and tasks. Table 2 shows base model results, Section 6.3 discusses SELB results, but there is no side-by-side controlled comparison. SELB has two components (structural enforcement via logit boosting and proactive failure prevention via negative bias) with no ablation isolating their individual contributions. Without this, it is impossible to determine whether SELB genuinely improves stability or simply enforces length by fiat, and whether the gains exceed simpler length-enforcement baselines already in Table 2 (e.g., Length Constraint, Lookahead Decoding). [favorability: 0.00]

### Minor

- **The attention trace analysis is qualitative and lacks systematic evidence.** The paper frames this as an "in-depth probe into the root causes" (Section 1) that "identifies several common internal patterns" (contribution list), but the evidence consists of two attention trace plots (Figure 4) for two model sizes on a single task (diary, 40 sections). There is no quantification of pattern frequency across models/tasks/seeds, no statistical test correlating attention patterns with output failures, and no predictive analysis. The patterns are visually plausible, but the evidence is thin relative to the claims. [favorability: 0.00]

- **N=5 for volatility estimation is small with no statistical grounding.** The core volatility metrics (LSD, LVC, MLA) are computed over N=5 generations (Section 3.2). For a benchmark built around measuring multi-generation volatility, N=5 yields high-variance estimates of the quantities being benchmarked. No confidence intervals, bootstrap estimates, or justification for N=5 are provided, weakening the statistical foundation of all volatility comparisons. [favorability: 0.12]

- **The connection between the attention analysis and SELB is asserted but not demonstrated.** The paper presents SELB as targeting the "identified internal patterns" (Section 1), but SELB does not detect or respond to attention signals. It uses hard-coded rules: boosting title tokens when a section reaches τ_max (structural enforcement) and suppressing EOS/conversational fillers (failure prevention). These rules would work identically regardless of whether the attention analysis existed. SELB pre-emptively prevents failures by brute force rather than by diagnosing and responding to the identified attention collapse or instability. [favorability: 0.05]

## Nice-to-Haves

- A clean within-model comparison table showing all metrics with and without SELB for each base model on the same task would directly validate (or refute) the method's claimed benefits.
- Ablating SELB's components (structural enforcement alone, failure prevention alone, combination) would clarify each mechanism's contribution.
- Quantifying the attention analysis (e.g., correlation between attention-to-constraint metrics and output volatility across models/tasks) would strengthen the causal argument.
- Increasing N or providing confidence intervals for volatility metrics would improve the benchmark's statistical foundation.

## Removed Points

These points from the input review are flagged for removal; treat with caution if encountered elsewhere:

- Criticism about LLM-as-a-Judge not being specified in main text: REMOVED (details are in Appendix C; hard rules prohibit penalizing missing appendix content that exists in the original submission).
- Criticism about execution-based verification (SCA) methodology not being described: REMOVED (details deferred to appendix; paper states "Execution-based Verification" in Section 3.2).
- Concerns about SELB assuming section-title format: REMOVED (paper explicitly addresses this with SELB-Hybrid in Section 6.4, showing generalization to free-form tasks).
- Criticism about τ_max and β lacking concrete values in main text: REMOVED (hyperparameter values are in appendix; reproducibility statement commits to code release).
- Speculation about SELB producing degenerate outputs or endless section titles: REMOVED (no evidence of such failures in the paper; this is speculative).
- Generic criticism about benchmark discriminative power at the upper length end: REMOVED (not a specific verified flaw; the benchmark surfaced clear failures at these lengths).
- Multiple generic/superficial strengths from the input review (e.g., "the paper addresses an important problem"): REMOVED (lack specific evidence or concrete content).

## Novel Insights

The reviews surface a structural observation that goes beyond the paper's own framing: the three contributions operate at markedly different levels of rigor. VOLTBench is carefully designed and empirically well-supported with comprehensive evaluation across 9 models. The attention analysis introduces a plausible conceptual framework but remains preliminary (two traces, no quantification). SELB is a straightforward rule-based method whose claimed effectiveness depends on a misleading comparison. The paper's narrative arc (benchmark → diagnose → mitigate) implies the three pieces build on each other, but the weakest link — the validation and framing of SELB — undermines confidence in the overall package. The benchmark is the strongest contribution and would stand on its own.

## Suggestions

1. Provide a clean within-model comparison table showing all metrics (LSD, LVC, MLA, FAD, SCA, UCA) with and without SELB for each base model (Qwen2.5-7B, Qwen3-8B, Llama-3.1-8B) on the same task.
2. Ablate SELB's components — structural enforcement alone, failure prevention alone, and their combination — to isolate each mechanism's contribution.
3. Either increase N (e.g., to 20) or provide confidence intervals/bootstrap estimates for the volatility metrics.
4. Quantify the attention analysis by computing the correlation between attention-to-constraint metrics (e.g., mean ᾱ over generation windows) and output volatility metrics across models, tasks, and seeds.
5. Clarify in Section 6.3 which model the headline SELB numbers (15,651 words, 14.02% LVC, 78.25% MLA) correspond to, and explicitly restate the improvements against the **same base model without SELB** alongside any cross-model comparisons.

## Score and Decision

Based on my assessment weighted by the favorability signals: the strengths are strongly positive (benchmark is a genuine contribution, problem framing is sound), but the weaknesses are severe — particularly the misleading framing of SELB's improvement numbers (favorability 0.07) and the complete absence of within-model controlled comparisons (favorability 0.00). The benchmark contribution is real and valuable, but the paper as a whole packages its contributions in a way that inflates the method's demonstrated effectiveness. The paper requires substantial revision in how SELB results are presented and validated before it can be accepted.

**MY FINAL SCORE: <score>4.0</score>**
**MY FINAL DECISION: <decision>Reject</decision>**