## Summary

This paper introduces ConCuR, a curated dataset of 4,892 CUDA kernels with reasoning traces, and KernelCoder, a QwQ-32B model fine-tuned via LoRA on this dataset. The authors observe that shorter reasoning traces correlate with higher correctness in kernel generation while being uncorrelated with speedup, and operationalize this into a data curation pipeline that selects kernels where the shortest CoT coincides with the highest speedup, adds high-speedup kernels, and balances task types. KernelCoder achieves strong results on KernelBench Level 1 and 2 (e.g., 58/59 Pass@1 Exec, 91/95 Pass@10 Exec) using only 64 A100 GPU hours, demonstrating that careful SFT data curation can make a 32B model competitive with 685B frontier models.

## Strengths

1. **Well-controlled ablation study (Table 4)**: KernelCoder (trained on the full ConCuR) is compared against four controlled ablations — random, max-length-first, min-length-first, and speedup-first — keeping all other training variables fixed. KernelCoder substantially outperforms every ablation (Level 1 Pass@1 Exec: 58 vs. 34–42; Level 2 Pass@1 Exec: 59 vs. 50–53), providing strong evidence that the specific combination of conciseness, speedup, and task-type balancing drives improvement.

2. **Efficiency advantage with concrete resource accounting (Table 3)**: KernelCoder uses only 4,892 samples and 64 A100 GPU hours (9 hours on 8 A100s), contrasted explicitly against Kevin (>600 H200 GPU hours), AutoTriton (640 A100 GPU hours), and KernelLLM (192 A100 GPU hours). The complete training recipe is provided, making the work reproducible with modest hardware.

3. **Cross-model generality (Table 5)**: Fine-tuning on ConCuR improves three different base models — Qwen3-8B (Level 1 Exec: 31→47), Qwen3-32B (68→72), and QwQ-32B (55→91) — demonstrating the dataset's value is not architecture- or training-recipe-specific.

4. **Empirical observation of the conciseness–correctness relationship (Figures 2 & 3)**: The paper documents that shorter reasoning traces are associated with higher correctness (accuracy drops from ~0.65 at the shortest bin to ~0.04 at the longest), while reasoning length and speedup are virtually uncorrelated (Pearson r = −0.047, p < 0.01). This provides a concrete data-driven foundation for the curation strategy.

## Weaknesses

### Fatal
None.

### Major

1. **Overstated claims about surpassing frontier models, with an internal inconsistency.** Section 4.2 states: "Moreover, it surpasses all frontier models, including DeepSeek-R1-0528." This is contradicted by the paper's own data in several places:
   - Table 2: On Level 2, DeepSeek-R1-0528 outperforms KernelCoder on Exec (97 vs. 95) and substantially on fast₁ (82 vs. 68).
   - Table 7: DeepSeek-R1-0528 achieves geometric mean speedups of 1.869/2.515/1.276 across Easy/Medium/Hard, while KernelCoder achieves 1.319/0.831/0.410.
   - Section 6.2 (line 265) itself states: "DeepSeek-R1-0528, although the best-performing model overall, fails to achieve a perfect score on the Easy level."
   
   A more honest characterization is that KernelCoder is *competitive* with DeepSeek-R1-0528 on correctness metrics while being a 32B model trained with far fewer resources — a genuinely interesting finding that does not need inflated framing.

2. **Misidentification of QwQ-32B in the abstract.** The abstract states: "our model achieves significant improvements over the existing top-performing model, QwQ-32B." Per Table 1, Kevin-32B (50/46 Pass@1 Exec on Levels 1/2) substantially outperforms QwQ-32B (18/17). QwQ-32B is the *base model* used for fine-tuning, not the top-performing existing model. This is either a writing error or a misrepresentation and must be corrected.

### Minor

1. **Causal claim about conciseness is only correlational.** The curation criterion (Section 3.5, part (a)) selects tasks where the shortest CoT coincides with the highest speedup, which explicitly retains only tasks that align with the hypothesis. The ablation study shows the combined criterion works, but does not disentangle whether conciseness *itself* causes improvement versus simply removing low-quality data that happens to produce long CoTs. The paper frames this as an "argument" and "observation" rather than a proven mechanism, so it is not a fatal flaw, but the causal language should be moderated.

2. **No confidence intervals or statistical significance tests.** With ~100 tasks per level (Table 6: 37+114+49 = 200 total), single-percentage-point margins (e.g., 17 vs. 18 on Level 1 fast₁) may not be statistically significant. Reporting confidence intervals (e.g., via bootstrap) would substantially strengthen the evaluation.

3. **Data contamination not discussed.** KernelBench tasks may overlap with KernelBook, which is the source of the generation tasks. The paper should address whether the evaluation tasks are sufficiently distinct from the training data distribution.

### Trivial
None.

## Nice-to-Haves

- A controlled experiment holding data quality fixed while varying CoT length (e.g., shortest vs. longest CoT from correct, fast kernels) to directly test whether conciseness itself drives improvement.
- Explicit discussion of inference cost comparison (32B vs. 685B models), which would further strengthen the efficiency argument.
- Task count breakdown per KernelBench level.

## Removed Points

The following weaknesses from the input reviews are removed with justification:

- **"Paper bolds its own numbers but not DeepSeek-R1-0528's strong results"** — Factually incorrect. In Table 2, DeepSeek-R1-0528's 97 (Exec) and 82 (fast₁) on Level 2 are both bolded. The critic misread the table.
- **"Existing top-performing model is misidentified as QwQ-32B"** — Kept as Major weakness #2 above (it is a real issue).
- **General area sweeps by the harsh critic about "could the metric be measuring a proxy"** — These were speculative framings, not concrete criticisms of the paper's content, and are removed.
- **Strength Finder's generic or duplicate strengths** (e.g., "the paper addresses an important problem") — These are general statements that any paper could claim and do not provide specific evidence.

## Novel Insights

None beyond the paper's own contributions. The reviews did not surface observations about the paper that the authors themselves do not already discuss.

## Suggestions

1. **Calibrate the claims.** Replace "surpasses all frontier models" with a precise characterization such as: "KernelCoder achieves competitive or better correctness on KernelBench Levels 1 and 2 compared to frontier models like DeepSeek-R1-0528, while using 32B parameters and only 64 A100 GPU hours of training — demonstrating the effectiveness of SFT on carefully curated data."

2. **Correct the QwQ-32B identification.** Change "existing top-performing model" to "base model" or a similar accurate descriptor.

3. **Add confidence intervals** for the main results (Tables 1, 2, 4) via bootstrapping over tasks.

4. **Discuss data contamination** between KernelBench and KernelBook, noting any precautions taken.

5. **Add a controlled experiment** that isolates conciseness from data quality — e.g., compare training on the shortest vs. longest CoT from a pool of only correct, high-speedup kernels.

## Score and Decision

**Round 1 Bracket:** 5.0–7.0 (based on calibration anchors)

**Calibration Anchors:**

| Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| Unearthing Domain-Specific Knowledge (8EM1A6qfX5) | 5.00 | R1 | Domain-specific data curation; less thorough evaluation than our paper |
| Rethinking Data Selection at Scale (qUJsX3XMBH) | 4.40 | R1 | Negative result paper about data selection; our paper has more positive contributions |
| Curated LLM for Tabular Data (ynguffsGfa) | 6.33 | R1 | Data curation with learning dynamics; cleaner presentation but less directly comparable domain |
| Automatic Dataset Construction (GcJE0HPy4X) | 6.00 | R1 | Dataset construction pipeline; similar scope but different domain (images) |
| LintSeq: Synthetic Edit Sequences (AqfUa08PCH) | 6.50 | R2 | Code SFT data generation; similar paper structure, stronger claims with cleaner presentation |
| VERT: Hardware Verification (rZmQ2z7MPA) | 5.33 | R2 | Dataset for specialized domain (hardware); similar setting, less thorough evaluation |
| Arctic-SnowCoder (X9JU2gKEkR) | 5.50 | R2 | Code data quality study; similar thoroughness of experiments but different framing |
| LongWriter (kQ5s9Yh0WI) | 6.00 | R2 | SFT data generation for long outputs; cleaner claims about contributions |

**Final Score Determination:** The paper's core contribution (ConCuR dataset, curation pipeline, thorough ablation) is genuine and practically useful — comparable in substance to papers scoring 5.5–6.5 in the calibration set. However, the overclaimed results relative to DeepSeek-R1-0528 and the factual error about QwQ-32B being the "top-performing model" are significant presentation issues that need major revisions. These issues are fixable but non-trivial—the paper currently says things directly contradicted by its own tables. This places it below papers with cleaner presentation (like LintSeq at 6.5) but above papers with weaker contributions (like VERT at 5.33). Score: 5.5.

### Score: 5.5
### Decision: Reject

The paper has a solid empirical contribution, but the overstated claims and factual inaccuracies in the abstract and Section 4.2 need to be corrected before the paper can be accepted.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>