## Summary

This paper proposes ASPD, a framework for adaptive serial-parallel decoding in large language models. It introduces (1) a data pipeline that uses a larger LLM to extract parallelizable structures from model responses, (2) architectural modifications (branch-invisible attention masks and shared position IDs) to enable parallel decoding within a single sequence, and (3) a hybrid decoding engine that switches between serial and parallel modes. The approach is evaluated on general tasks, RAG, and mathematical reasoning, reporting up to 3.10× speedup on Vicuna Bench with quality within ~1% of the sequential fine-tuned baseline.

## Strengths

- **The architectural design is technically coherent and novel.** The combination of branch-invisible attention masks (Eq. 2–3) and shared position IDs across parallel branches at the same timestamp (Eq. 4) is a clean solution to the parallel decoding problem, enabling parallel generation within a single sequence without batching, threading, or KV-cache reinitialization overhead. This differentiates ASPD from prior work (APAR, PASTA, SoT) in meaningful ways.

- **The evaluation is broad and covers multiple domains.** The paper tests on Vicuna Bench, MT Bench, RAG, and mathematical reasoning (MATH500, AMC23, GPQA, AIME2024/2025), with two base model architectures (Vicuna-1.3-7B and Qwen2.5-7B-Instruct) and a 32B model for math, demonstrating generalizability.

- **The reported speedup on Vicuna Bench (1.82× average, up to 3.10×) while maintaining quality within ~1% of the sequential fine-tuned baseline is practically meaningful** if the claims hold. This directly addresses a real latency bottleneck in LLM inference.

## Weaknesses

### Major

- **Section 4.4.2 contains a direct text–data contradiction.** The text claims that *Shared* masks "consistently outperform *Indep* masks across both *Seq* and *Max* position id configurations," but Table 4 shows the opposite: Indep achieves scores of 7.64 and 6.78 versus Shared's 4.64 and 3.70 — a 64–83% advantage. The data actually supports the ASPD design (branch-invisible = Indep), so this is a textual error, but it makes the ablation section unreliable as written and must be corrected. This is the single most serious issue in the paper.

- **Figure 1 reports exactly 44% Proportion of Parallel Data across all four listed datasets** (ShareGPT Vicuna, MRC, RAG, Math-220K). These are diverse datasets from very different domains; having identical PPD is implausible and suggests a copy-paste or calculation error. Since Figure 1 is presented as key motivating evidence, this undermines confidence in the paper's data analysis.

- **The Degree of Parallelism (DP) values in Figure 1 (5.2, 3.4, 4.2, 2.7) are inconsistent with the paper's own definition** of DP as "ratio of parallel to total tokens" (Section 4.1), which should be ≤1 (or ≤100%). Moreover, for three of four datasets the DP equals the Average Branch Number, further suggesting a data error. The authors must clarify what these values represent or correct them.

### Minor

- **The paper does not report error bars, confidence intervals, or statistical significance** for any quality or speed comparisons. Several key comparisons show differences <1% (e.g., V-Seq 7.70 vs V-ASPD 7.74 on Vicuna Bench), and variance estimates are needed to assess whether these are meaningful.

- **No discussion of failure cases or limitations** of the proposed method. For example, math reasoning speedups (1.04–1.17×) are substantially weaker than general-task speedups (1.30–1.82×), but the paper does not analyze why or discuss when parallelization might degrade quality.

- **V-Seq's TPS is not explicitly reported** in the main results, making it harder to directly isolate the speedup attributable to parallelization versus fine-tuning effects. (V-Seq should decode at similar speed to V-Ori since both are sequential, but reporting it would strengthen the comparison.)

### Trivial

None.

## Nice-to-Haves

- Report V-Seq's TPS explicitly in the main results table.
- Add an analysis of which response types (lists, explanations, step-by-step reasoning) benefit most from parallelization.
- Conduct a sensitivity analysis for the data pipeline parameter N=3 (number of parallel rewrites per sample).

## Removed Points

These points from the input review are flagged for removal — treat them with caution:

- *V-APAR* baseline confounding data/architecture contributions*: The paper's claim is about *maintaining* quality during parallel decoding, not improving it. V-Seq (same data, sequential) scores comparably to V-ASPD, confirming the architecture does not degrade quality. The comparison against V-APAR* is a standard baseline comparison. Not a weakness.

- *Evaluation compares against wrong baselines*: The paper explicitly states "maintaining response quality within 1% difference" — the parallel architecture is not claimed to improve quality. This criticism misreads the paper's stated goal.

- *Data pipeline circular validation*: Using a larger LLM to generate and verify training data for a smaller model is standard practice (data distillation). The pipeline is described accurately.

- *Missing speculative decoding comparison / related work gaps*: Speculative decoding is discussed in Related Work with a rationale for exclusion. Per instructions, missing related works are not included.

- *Formatting/style nitpicks* and *reproducibility nitpicks*: Parser artifacts or standard community practice.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the text–data contradiction in Section 4.4.2.** The text should correctly state that Indep (branch-invisible) masks outperform Shared masks, which is what the data shows and what validates the ASPD design.
2. **Investigate and correct the Figure 1 data.** Verify whether all datasets truly have 44% PPD and clarify what the DP values represent relative to the formal definition.
3. **Add variance estimates** (e.g., multiple runs or confidence intervals) for key comparisons to establish that the reported differences are meaningful.
4. **Add a limitations section** discussing when and why parallelization is less effective (e.g., math reasoning) and potential failure modes.
5. **Report V-Seq TPS** explicitly in the main results to enable direct speed attribution.

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>