## Summary

This paper investigates length volatility in LLM long-form generation through three stages: benchmarking (VOLTBench), probing (attention trace analysis), and mitigation (SELB decoding strategy). VOLTBench is a multi-dimensional benchmark covering structured and unstructured tasks, English and Chinese, and multiple complexity/length scales. SELB is a rule-based decoding method that forces section transitions and suppresses EOS/filler tokens. The benchmark contribution is solid, but the method has significant reporting and framing issues that undermine the headline claims.

## Strengths

- **VOLTBench fills a genuine gap in the benchmark landscape.** The problem of length volatility across multiple generations is underexplored, and Table 1 makes a credible case that no existing benchmark covers multi-sampling stability evaluation. The multi-dimensional design (structured + unstructured tasks, English + Chinese, multiple complexity levels, chapter-based scalability from 5 to 500 sections) is more comprehensive than prior work on the volatility axis. The inclusion of structured tasks (code, math) with execution-based verification is a particular strength.

- **The empirical finding that volatility is severe and widespread across models is important.** Table 2 shows that even LongWriter-8B, a model specifically designed for long-form generation, has LSD of 2866.3 and LVC of 45.4%, and that models including GPT-4o mini, Deepseek-R1, and Qwen2.5-7B all exhibit non-trivial volatility. This finding is clearly presented and has practical significance for deployment reliability and cost predictability.

- **The attention trace analysis provides a plausible qualitative link between internal dynamics and volatility.** The observation that periodic attention spikes correspond to section boundaries in well-behaved generation, and that their collapse or disruption precedes failures (Figure 4), is intuitively reasonable and worth reporting as a preliminary qualitative observation.

## Weaknesses

### Major

- **SELB results are not reported in Table 2.** The paper's primary results table lists 9 models and 4 decoding strategies across all metrics (LSD, LVC, MLA, FAD, SCA, UCA), but SELB — one of the paper's three claimed contributions — is absent from this table. Its results are reported only in prose in Section 6.3. This prevents the reader from directly comparing SELB against all baselines on the same task with the same columns, which is a basic reporting omission for a proposed method.

- **The headline claims ("148% improvement in mean output length," "69% reduction in length volatility") are attributed to "the base model" without specifying which model serves as the base.** Section 6.3 compares SELB's 15,651 words to LongWriter-8B's 6,320 words (giving ~148%) and SELB's LVC of 14.02% to LongWriter-8B's 45.4% (giving ~69%). But Figure 5 shows SELB applied to Qwen2.5-7B, Qwen3-8B, and Llama-3.1-8B — not LongWriter-8B. If SELB is applied to Qwen2.5-7B (mean 445 words, LVC 17.0% from Table 2), the actual increase over the same model without SELB would be ~3,418%, not 148%, and the LVC reduction would be ~18%, not 69%. The paper never clarifies which model SELB is applied to for these figures, and the comparison basis is ambiguous between cross-model and within-model. This undermines the paper's most prominent quantitative claims.

### Minor

- **N=5 samples per condition (Section 3.2) is small for a benchmark whose core purpose is measuring variability across runs.** With 5 samples, the standard error of the estimated standard deviation is approximately 30% of the SD itself. This means the LSD and LVC values in Table 2 have wide confidence intervals, and many cross-model comparisons may be within the noise floor. For a benchmark designed around measuring variability, this is a methodological limitation.

- **The attention trace analysis (Section 5) is entirely qualitative.** It is based on visual inspection of two model variants on one task (Figure 4). The paper claims that "the output volatility is not random but closely linked to and preceded by measurable failures in the model's internal attention dynamics," but provides no quantitative metrics (e.g., variance of attention over time, correlation between attention-derived measures and output volatility), no demonstration that the patterns precede rather than merely accompany failures, no controlled experiments, and no ablation showing that stabilizing attention patterns reduces volatility. SELB itself does not detect or respond to these attention patterns dynamically — it overrides logits unconditionally. The connection between the probing analysis and the mitigation method is asserted rather than demonstrated.

- **SELB is a straightforward rule-based logit manipulation** (force section transition when a section reaches τ_max tokens; suppress EOS and conversational filler tokens until all P_total sections are generated). The paper presents the length and volatility improvements as empirical discoveries, but they are largely mechanical consequences of the method's design — suppressing EOS guarantees continued generation, and forcing section transitions at fixed intervals mechanically reduces length variability. The boosterish tone ("Our method marks a major improvement," "dramatically better") is mismatched with the method's simplicity. The real contribution of SELB would be if it demonstrably outperformed comparable decoding baselines (e.g., Lookahead Decoding, which achieves LVC 9.3% on the same Qwen2.5-7B base — better than SELB's 14.02%), but this comparison is not made because SELB is not in Table 2.

- **Free-form generation results (Section 6.4) — claiming MLA 97% and LVC 12.1% on 20k-word novel writing — are reported in text only, with no comparison table and details deferred entirely to the appendix.** This makes the claims unverifiable from the main paper.

### Trivial

- The paper lacks a Limitations section, which is notable given the strength of the empirical claims and the simplicity of the proposed method.

## Nice-to-Haves

- The VOLTBench contribution would be strengthened by reporting confidence intervals or bootstrap estimates for the volatility metrics, to account for the small N.
- The attention trace analysis could be substantially improved by computing quantitative metrics (e.g., variance of attention over time, frequency of attention spikes, minimum attention in a window) and correlating them with output volatility across many examples and models.
- SELB should be compared against its own base model (same architecture ± SELB) rather than cross-model to LongWriter-8B.

## Removed Points

These points are flagged to be removed, treat them with caution:
- "SELB does not outperform existing methods on volatility (several baselines have lower LVC)": This comparison is difficult to evaluate without knowing which base model SELB is applied to. Claude-3.5's 1.9% LVC comes with only 176 words output (excluded from quality eval). However, Lookahead Decoding (9.3% LVC on Qwen2.5-7B) is a fair comparison since it's a decoding baseline on the same architecture — SELB's 14.02% is worse. This point is partially absorbed into the "not in Table 2" weakness.
- "Table 1 checkmarks are self-serving": Minor nitpick about "Multiple Language" covering two languages and "~100k" being a maximum rather than typical tested range. These are standard benchmark framing choices.
- "The 100k words claim is not supported by experimental results": The benchmark is designed for scalability up to 100k; actual experiments at smaller scales are standard practice for feasibility.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Include SELB in the main comparison table** (Table 2) with the same column headers as all baselines, and clearly state which base model SELB is applied to.
2. **Explicitly state the base model** for the 148% and 69% claims, and provide within-model comparisons (same model ± SELB) rather than (or in addition to) cross-model comparisons.
3. **Increase N or provide stability analysis** — either increase samples to at least 20–30, or include bootstrap confidence intervals showing that the reported differences are reliable at N=5.
4. **Add quantitative grounding to the attention trace analysis** — compute a metric from attention traces and correlate it with output volatility across many examples, or show that the identified patterns predict failures above chance.
5. **Reframe the paper's narrative** around VOLTBench as the primary contribution, with SELB positioned as a simple rule-based baseline for future methods, not as a major methodological advance.

## Score and Decision

Anchors used for calibration (all from `deepreview_13k_calibration`):

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| HelloBench (QM2WoPu1It) | 4.75 | R1 | Yes | Benchmark for long text generation; comparable benchmark quality but cleaner presentation; our paper's more negative weakness items (-3.11 vs -2.23) place it slightly below |
| LongWriter (kQ5s9Yh0WI) | 6.00 | R1 | Yes | Long-form generation method with rigorous evaluation; significantly stronger method contribution |
| PRISM Decoding (A6juYCULJO) | 6.00 | R1 | Yes | Comprehensive decoding study; stronger experimental methodology |
| Length Representations (dNBE4ciYJF) | 4.00 | R2 | Yes | Internal mechanism analysis; comparable weakness severity (-3.61 vs -3.11) but fewer strengths |
| Integrating Planning (YONCcPQJoC) | 4.75 | R2 | No | Long-form generation with planning; stronger method evaluation |
| Self-Lengthen (gGElk5T8sD) | 3.75 | R2 | No | Training framework for long text; comparable overall quality |

**Round 1 bracket**: 3.0–5.5 (between weak reject and borderline accept)

**Round 2 narrowing**: The paper's benchmark contribution (VOLTBench) is comparable to HelloBench (4.75), but its most negative weakness items (SELB overselling at -3.11, attention trace qualitative at -2.19) are more negative than HelloBench's most negative (-2.23), while having fewer total strength items. The missing-Limitations and base-model-ambiguity issues further drag the score. The paper sits between Length Representations (4.00) and HelloBench (4.75), closer to Length Representations due to the number of unresolved reporting issues.

**Final score**: 4.0. The VOLTBench contribution is genuinely useful, but the paper's three-part structure ("benchmarking, probing, mitigation") claims equal weight for all three, and two of the three (probing and mitigation) have significant evidentiary and reporting weaknesses. The headline claims rest on ambiguous comparisons, the proposed method is not in the main results table, and the internal analysis is qualitative.

<score>4.0</score>
<decision>Reject</decision>