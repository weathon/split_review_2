## Summary

This paper addresses the underexplored problem of run-to-run length volatility in LLM long-form generation through three stages: benchmarking, probing, and mitigation. It proposes VOLTBench (a multi-dimensional benchmark covering unstructured and structured tasks, two languages, and up to 100k-word length scales), an attention-trace analysis identifying two failure patterns (Attention Collapse and Attention Instability), and SELB (a lightweight, training-free decoding strategy that enforces section structure via logit boosting). Experiments on VOLTBench confirm that volatility is a real problem in mainstream models and show that SELB achieves strong length accuracy and low volatility.

## Strengths

- **The problem is well-motivated and genuinely underexplored.** Section 1 and Figure 1 make a convincing case that existing long-form generation benchmarks evaluate single-generation quality while overlooking run-to-run consistency. The observation that LongWriter-8B's output standard deviation reaches 103% of its mean length (Figure 1 caption) is a striking quantitative demonstration of the volatility problem.

- **VOLTBench's multi-dimensional design is a meaningful step forward.** The benchmark covers unstructured (story, diary) and structured (code, math) tasks, two languages, varying instruction complexity, and a scalable chapter-based format up to 100k words (Table 1). This provides a richer evaluation surface than existing benchmarks (HelloBench, LongGenBench, LifeBench, etc.) which lack multiple-sampling and stability evaluation.

- **SELB is lightweight and training-free.** Operating entirely at decoding time via logit modification, it can be dropped into existing pipelines without fine-tuning. The three-component design (structural enforcement via logit boosting, filler-phrase banning, and EOS blocking) is clearly described in Section 6.

## Weaknesses

### Major

- **The headline claims (148% length improvement, 69% volatility reduction) are computed against LongWriter-8B — a *different* model — but the abstract and contributions (lines 9, 28, 234) describe this as improving "the base model."** The paper never explicitly states which base model SELB is applied to for the 15,651-word / 14.02% LVC / 78.25% MLA results. Section 6.3 (line 218) writes "our model" without identifying the underlying base model. Figure 5 shows SELB applied to Qwen2.5-7B, Qwen3-8B, and Llama-3.1-8B, but the text does not attribute the headline numbers to any specific one. Moreover, no within-model ablation is reported (e.g., SELB+Qwen2.5-7B vs. Qwen2.5-7B alone, whose mean is 445 words from Table 2). The paper's core quantitative claim is therefore ambiguous — readers cannot tell whether the improvement is over the same model or a different model.

- **SELB results are not included in Table 2 alongside the other decoding strategies.** Table 2 lists Repetition Penalty, Entropy-Stopping, Length Constraint, and Lookahead Decoding — all applied to Qwen2.5-7B under the same 100-section simple setting — but SELB is absent. SELB results are reported separately in Section 6.3 with different formatting. Without a side-by-side comparison in the same table, readers cannot directly evaluate whether SELB outperforms simpler training-free alternatives on an apples-to-apples basis (same base model, same task, same metrics).

### Minor

- **The attention trace analysis (Section 5) claims to identify "common internal patterns" of length volatility but presents only two examples** (Qwen2.5-7B and Qwen2.5-3B on one diary task with 40 required sections, Figure 4). There is no quantitative evidence of how prevalent these patterns are across models, tasks, or length requirements, nor statistical testing of the relationship between attention patterns and output volatility. The claim of "common patterns" is broader than the two-case evidence supports.

- **SELB is motivated as "targeting the identified internal patterns" (line 28, line 210), but it does not actually modify or respond to attention dynamics.** SELB forces section transitions via logit boosting, bans filler phrases, and blocks the EOS token — all behavioral interventions that address symptoms (premature termination, filler text) rather than the attention patterns described in Section 5. The causal claim connecting attention analysis to method design is overstated — SELB could have been designed without any attention analysis simply by observing that models stop early.

- **The paper's framing emphasizes volatility as the widespread problem, but Table 2 shows many models are consistently under-generating with low variance** (e.g., Claude-3.5-Sonnet LVC=1.9%, mean=176 words; Qwen2.5-1.5B LVC=19.6%, mean=142 words). The primary failure mode across most models is *systematic under-generation* (low length accuracy, often low volatility). Only LongWriter-8B exhibits high volatility alongside long output. The benchmark is valuable, but the narrative oversells volatility relative to the length-accuracy problem, which prior work already documents.

- **The benchmark uses N=5 generations per prompt to estimate volatility (line 108).** A sample of 5 is small for reliable standard deviation estimates, especially for genuinely unstable models like LongWriter-8B. The paper does not justify this choice or provide a sensitivity analysis with varying N.

- **The paper does not report sensitivity to SELB's hyperparameters (τ_max and β) or explain how they were set.**

- **Lowering temperature is a natural minimal baseline for reducing volatility that the paper does not evaluate.** This would be a straightforward comparison point for a volatility-reduction claim.

### Trivial

None.

## Nice-to-Haves

- A sensitivity analysis with varying N (e.g., N=3, 5, 10, 20) to validate that the volatility estimates are stable.

## Removed Points

These points were removed from the input review for the following reasons:

- *"Multiple Language with only English and Chinese is a stretch"* → Trivial nitpick; two languages covering distinct script families is a reasonable notion of "multiple" for an empirical paper.
- *"100% SCA is suspicious because SELB may force empty sections"* → The paper references lexical diversity analysis in Appendix G (stripped by the parser; rule prohibits penalizing for missing appendix content).
- *"Free-form generalization results deferred to appendix"* → Parser-stripped content; see rule above.
- *"Missing related work"* → Rule prohibits this criticism since I cannot confirm what work exists externally.
- *"Reproducibility / large artifacts not included"* → Rule prohibits nitpicks about reproducibility impractical for submission.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Clarify the headline comparison.** Explicitly state which base model SELB is applied to for the 15,651-word / 14.02% LVC / 78.25% MLA results. Report within-model ablation as the primary comparison (SELB + base vs. base alone) and present the LongWriter-8B comparison as supplementary context. Revise the abstract to avoid the ambiguous phrase "base model."

2. **Add SELB to Table 2** (or a companion table) applied to the same base model (e.g., Qwen2.5-7B) alongside the existing decoding baselines, so readers can make a direct, side-by-side comparison on identical metrics.

3. **Strengthen or reframe the attention analysis.** Either provide quantitative evidence (prevalence across models/tasks, correlation between attention-to-constraint values and output length, early prediction of section-skipping), or drop the causal framing and present the traces as qualitative illustrations that motivate — rather than empirically validate — the method.

4. **Report hyperparameter sensitivity** for τ_max and β, and add a temperature-ablation baseline to the volatility comparison.

5. **Separate the "volatility" narrative from the "length accuracy" narrative** more clearly in the framing, since most models fail by consistently under-generating (an accuracy problem) rather than by being unstable (a volatility problem).

## Score and Decision

**Calibration Anchors (retrieved across all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `5kMwiMnUip.md` (jailbreaking) | 1.40 | R1 | No | Topically unrelated, different problem. |
| `8QTpYC4smR.md` (survey) | 1.00 | R1 | No | Literature survey, not a technical paper. |
| `Uj0h13lVrR.md` (GFlowNets) | 1.00 | R1 | No | Unrelated topic. |
| `nSDOkm0SKo.md` (finance) | 1.00 | R1 | No | Unrelated topic. |
| `SaOxhcDCM3.md` (self-consuming loop) | 3.20 | R1 | No | Somewhat related (LLM failure analysis), much lower quality. |
| `2wwPG1wpsu.md` (LST-Bench) | 2.50 | R1 | No | Benchmark paper, but for time-series, not comparable quality. |
| `ly10tMV6cD.md` (structure-rich text) | 3.25 | R1 | No | Related (benchmark + structured output). Weaker coverage. |
| `KBixkDNE8p.md` (LLM psychology) | 3.00 | R1 | No | Unrelated. |
| **`vXf8KYTJmm.md` (MAP not dead)** | **5.25** | R1 | Yes | Decoding method paper. This paper has fewer severe negatives. |
| **`QM2WoPu1It.md` (HelloBench)** | **4.75** | R1 | Yes | Most directly comparable — long-text generation benchmark. HelloBench has massive novelty concerns (-7.81, -8.13) that this paper lacks. |
| `dNBE4ciYJF.md` (length representations) | 4.00 | R1 | No | Related (length control in LLMs). Less comprehensive. |
| `eNCyY81aW6.md` (FACTOR) | 5.00 | R1 | No | Long-context benchmark. Similar score range. |
| **`293V3bJbmE.md` (HELMET)** | **6.00** | R1 | Yes | Pure benchmark paper with only minor negatives (-1.90 max). This paper has more significant weaknesses. |
| **`kQ5s9Yh0WI.md` (LongWriter)** | **6.00** | R1 | Yes | Strong baseline paper. Clearer narrative and cleaner results than this paper. |
| **`EmQSOi1X2f.md` (Self-contradictory Hallucinations)** | **6.00** | R1 | Yes | Evaluation→detection→mitigation structure similar to this paper. Better executed. |

**Weighted-Item Comparison:** My draft's strongest negative is **-4.79** (headline ambiguity) and strongest positive is **+5.36** (VOLTBench). Compared to HelloBench (4.75) which has -7.81 and -8.13 negatives, this paper has weaker negatives but also weaker positives. Compared to LongWriter (6.00) which has a -8.89 negative but very strong positives (+5.03), this paper has more moderate weights on both sides. The critical difference is that this paper's -4.79 negative is about **presentation/clarity** (can be fixed) whereas HelloBench's and LongWriter's worst negatives are about **novelty** (cannot be fixed). However, this paper has a cluster of medium-weight negatives (-4.79, -4.11, -3.75, -3.00) that together indicate significant issues.

**Round 1 bracket:** Between 4.5 and 5.5 — above HelloBench (4.75) due to genuine novelty and stronger benchmark design, but below LongWriter/HELMET (6.00) due to the ambiguous headline claims, missing Table-2 comparison, and narrative disconnect between attention analysis and SELB.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>