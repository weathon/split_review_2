Now let me compile my final review with the calibration done.

**Round 1 bracket analysis:**

I examined anchors across all score bands. The most directly comparable papers are:
- **HelloBench** (4.75, rejected) — long-text generation benchmark; criticized for limited novelty. My paper's VOLTBench has greater novelty (multi-generation volatility is genuinely new).
- **LongWriter** (6.00, accepted) — long-form generation via data augmentation; accepted despite evaluation relying solely on GPT-4 judge.
- **Quantifying Variance** (4.17, rejected) — about variance in evaluation; narrow scope.
- **Controllable Generation via Constrained Resampling** (6.00, accepted) — constrained decoding; accepted despite serious weaknesses (-10.00 for no error bars, -10.00 for insufficient baselines) because theoretical novelty was strong.

My Round-1 bracket: **3.5–5.5**. The paper has stronger contribution novelty than HelloBench but weaker than LongWriter/Controllable Generation due to a major framing issue with SELB results.

**Round 2 narrowing:**

Comparing itemized impact scores: The paper's two decisive weaknesses (headline claims misleading at -10.00, SELB absent from Table 2 at -9.62) are comparable in magnitude to HelloBench's "limited novelty" (-10.00) but of a different nature — they're about presentation/reporting rather than fundamental contribution. The paper's strengths (VOLTBench design +9.32, attention analysis +8.77) are stronger than HelloBench's best strength (+9.71 for experiments across many models). Placing this between HelloBench (4.75, rejected) and LongWriter (6.00, accepted): the benchmark and analysis are solid, but the misleading central claim about SELB's effectiveness drags the paper down. **Final score: 4.5.**

---

## Summary

This paper addresses the underexplored problem of length volatility in long-form LLM generation — the inconsistency in output length and content across multiple generations of the same prompt. It makes three contributions: (1) VOLTBench, a multi-dimensional benchmark covering structured/unstructured tasks, multiple languages, instruction complexities, and up to 100k-word scales; (2) an attention trace analysis identifying "Attention Collapse" and "Attention Instability" as internal precursors to generation failures; (3) SELB (Structural Enforcement via Logits Boosting), a training-free decoding strategy to mitigate volatility.

## Strengths

- **VOLTBench's multi-dimensional design is thoughtful and genuinely novel.** The benchmark spans language (EN/ZH), instruction complexity (simple/complex/fine-grained), output format (structured/unstructured), and length scale (up to 100k words via a chapter-based format). The inclusion of fine-grained constraints (character-level, keyword, theme) that enable *automated* quality evaluation for unstructured tasks is a practical and well-motivated design choice (Section 3).

- **The attention trace analysis provides concrete internal patterns linked to failure modes.** Identifying "Attention Collapse" (attention to constraints dropping to near-zero, leading to premature termination) and "Attention Instability" (erratic attention spikes preceding section-skipping) moves beyond purely behavioral observation of long-form generation failures. The methodology for computing constraint attention (averaging over heads and layers) is clearly described (Section 5).

- **The paper correctly identifies a genuine gap.** Existing long-form generation benchmarks (HelloBench, LIFEBench, LongGenBench) evaluate single generations in isolation, systematically overlooking consistency across multiple runs of the same prompt — a real limitation for reliable deployment (Section 1, para 3).

## Weaknesses

### Fatal
None.

### Major

- **Headline quantitative claims compare against the wrong baseline and frame a cross-model comparison as an ablation.** The abstract and contributions state SELB "improves the mean output length of the *base model* by 148% and reduces the length volatility by 69%." Tracing the numbers in Section 6.3: LongWriter-8B has LVC=45.4% and mean=6,320 words (Table 2); a 69% reduction yields ~14.07% (matching SELB's 14.02%) and a 148% increase yields ~15,674 (matching SELB's ~15,651). So the comparison is **SELB+Qwen2.5-7B vs. LongWriter-8B** — a cross-model comparison against a specialized long-generation model, not an ablation against the actual base model SELB is applied to (Qwen2.5-7B produces 445 words and LVC=17.0%). Furthermore, the paper never specifies which base model the Section 6.3 numbers correspond to ("our model" is used repeatedly without identification; Figure 5 shows three different base models + SELB). [Verified: Section 6.3 text, Table 2, Figure 5.]

- **SELB is absent from the main comparison table (Table 2).** Table 2 is the paper's central results table for the 100-section simple task, covering 9 baselines and 4 decoding strategies (Repetition Penalty, Entropy-Stopping, Length Constraint, Lookahead Decoding). SELB results are described only in Section 6.3 text, under the same experimental condition ("Evaluation was done on a 100-section task under simple settings"). The reader cannot directly compare SELB against the Length Constraint baseline (MLA=22.4%, mean=4,470) or other decoding strategies. The incremental benefit of SELB's specific design choices over a generic length constraint is not shown.

### Minor

- **N=5 generations for volatility measurement is insufficient for reliable statistics.** LVC and LSD are computed over N=5 runs. The standard error of the sample standard deviation at n=5 is ~29% for normal distributions, and worse for the heavy-tailed distributions typical of LLM output lengths. No confidence intervals or bootstrap estimates are reported, which weakens the reliability of the paper's central measurements.

- **SCA=100% reported without error bars or distribution information.** Baselines in Table 2 are consistently reported with standard deviations (e.g., Qwen2.5-7B SCA=99.8%±0.4%, LongWriter-8B SCA=32.6%±31.9%). Reporting 100% for SELB without any measure of variance is suspicious and undermines confidence in the result.

- **Conflation of variance and accuracy under the term 'volatility.'** The paper defines volatility as "inconsistency in length and content across multiple generations" (abstract). However, LVC measures relative variance across runs (genuine volatility), while MLA measures whether the *mean* output hits the target — an accuracy/bias measure, not a volatility measure. Claude-3.5-Sonnet (Table 2) has LVC=1.9% (very stable) but mean=176 words on a 100-section task — a length *accuracy* problem, not volatility. These are distinct phenomena and conflating them weakens conceptual clarity.

- **UCA uses LLM-as-a-Judge without discussing known biases.** The paper relies on an LLM judge for unstructured quality assessment (Section 3.2) but does not discuss calibration, position bias, or self-enhancement bias — well-documented issues in the literature. Details are deferred to an appendix (stripped by parser), but the main text should at minimum acknowledge these limitations.

- **The attention trace analysis is correlational, not causal.** Section 5 identifies attention patterns that *precede* failures, which is interesting, but does not demonstrate causation. Moreover, SELB modifies logits, not attention; the paper would benefit from showing that SELB's logit modifications measurably affect the attention patterns it claims to address.

### Trivial
None.

## Nice-to-Haves

- Ablation isolating SELB's components: (a) EOS suppression only, (b) section-title boosting only, (c) both, (d) full SELB.
- Causal analysis connecting the identified attention patterns to SELB's effectiveness.
- SELB-Hybrid (free-form) quality evaluation beyond LLM-as-a-Judge.

## Removed Points

These points from the harsh critic input were filtered out:

- **"SELB's improvements are largely a direct consequence of the method's design, not an empirical discovery"**: Partially accurate but the paper's contribution is that quality holds up under the constraints — an empirical finding. The framing concern is already captured in the Major weakness about the misleading comparison baseline.
- **Section-by-section notes** (Introduction novelty, Section 3 confound, Section 4.3 failure criteria, Section 6.1 limitation): Too minor, speculative, or partially addressed by the paper.
- **Criticisms about missing appendix content**: Removed per hard rules — the parser strips these sections from all papers.
- **Generic "important problem" strengths**: None present in the input; all retained strengths are specific and evidence-backed.

## Novel Insights

None beyond the paper's own contributions. The three-stage structure (benchmark → probe → mitigate) is well-executed in concept, but the evaluation limitations are significant enough that no synthesis-level insight emerges beyond what the paper itself articulates.

## Suggestions

1. Place SELB results directly in Table 2 alongside existing decoding-strategy baselines, specifying which base model each SELB row uses (Qwen2.5-7B+SELB, Qwen3-8B+SELB, Llama3.1-8B+SELB).
2. Reframe the headline claims honestly: e.g., "outperforms the specialized LongWriter-8B by 148% in length and 69% in volatility when applied to Qwen2.5-7B" — an explicit cross-model comparison.
3. Report which base model produced the Section 6.3 numbers, and provide paired ablation results for all three base models with and without SELB.
4. Provide an ablation isolating which SELB components drive the improvements.
5. Add confidence intervals or bootstrap estimates for LVC/LSD given the small sample size.
6. Report SCA with error bars and clarify the test programs used.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>