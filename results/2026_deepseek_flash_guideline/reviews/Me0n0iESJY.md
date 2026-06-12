## Summary

This paper introduces OptMerge, a model merging method for Multimodal LLMs, along with a benchmark that categorizes MLLM capabilities into 5 areas (VQA, Geometry, Chart, OCR, Grounding) and evaluates both capability merging (across specialized models) and modality merging (across vision, audio, and video encoders). The benchmark provides fine-tuned checkpoints for InternVL2.5-1B (full fine-tuning) and Qwen2-VL-7B (LoRA), evaluates 10 merging algorithms, and extends to real Hugging Face checkpoints and a 32B model. OptMerge improves upon WUDI Merging by adding SVD-based denoising of task vectors, replacing Adam with SGD, and using mean initialization, achieving modest absolute gains of 2.48 percentage points on average.

## Strengths

- **First fine-grained model merging benchmark for MLLMs with categorized capabilities.** The paper explicitly partitions MLLM capabilities into 5 categories with ≥100k training samples per category, provides fine-tuned checkpoints for two base models spanning full fine-tuning and LoRA paradigms, and evaluates 10 merging algorithms under a standardized protocol. This fills a gap: AdaMMS (Du et al., 2025b) can only merge two MLLMs at a time, and UQ-Merge (Qu et al., 2025) treats each fine-tuning dataset as a separate task without capability categorization. The benchmark is a tangible contribution to the community.

- **Comprehensive empirical evaluation.** The paper evaluates across multiple dimensions: capability merging (2 base models, 10 benchmarks), modality merging (vision, audio, video), real-world Hugging Face checkpoints from independent developers, and a 32B model scale extension. Table 7 also quantifies the computational efficiency advantage (0.15× GPU memory and time vs. mixture training), making the practical benefit concrete.

- **Theorem 3.1 provides a theoretical bound linking fine-tuning hyperparameters to merging quality.** The bound decomposes merging error into residual convergence O(γ^T), cross-task interference O(δηT), and curvature O(η²T²) terms. While asymptotic and not quantitatively actionable, it offers a principled motivation for the benchmark's design choices (controlled fine-tuning with minimal parameter drift).

- **Modality merging results point in an interesting direction.** Static merging of vision, audio, and video models (OptMerge: 67.00 average) outperforms individual modalities (best single modality: video at 64.11) and online composing methods (DAMC: 66.79, NaiveMC: 66.88), suggesting a data-free path toward Omni-language models.

## Weaknesses

### Major

1. **Numerical inconsistencies in Table 3 (Qwen2-VL, LoRA setting) for WUDI Merging and TSV Merging averages.** The stated averages for these two methods do not match recomputation from the individual scores in the same table. For WUDI Merging, the stated average is 63.65 but summing the 10 constituent scores gives 599.72 → 59.97 (Δ = −3.68). For TSV Merging, stated is 60.63 but computation gives 62.79 (Δ = +2.16). Other rows in the same table (Individual VQA, TIES, Weight Average) check out correctly, confirming this is not a systematic parsing error. The WUDI discrepancy is far too large for rounding. Additionally, the ablation study (Table 4) reports a WUDI baseline of 58.65 for Qwen2-VL, which differs from both the stated 63.65 and the computed 59.97 in Table 3 without explanation. These issues undermine confidence in the reported numbers and must be resolved before the paper can be properly evaluated.

2. **The claim that model merging "surpasses" mixture training is not supported by the best-controlled comparison.** On InternVL2.5 (Table 2), where the authors run a proper mixture training baseline, mixture training achieves 57.66 while OptMerge achieves 57.44 — mixture training wins by 0.22 points. For Qwen2-VL, the paper compares against Qwen2-VL-Instruct (62.23) as a proxy for mixture training rather than running actual mixture training on the same task data, making this an apples-to-oranges comparison. While the paper uses hedging language ("potentially surpasses," "closely match or even surpass"), the contribution listing states "model merging can outperform mixture training" without qualification. This claim should either be supported by a proper Qwen2-VL mixture training baseline or be substantially tempered.

3. **The method's gains over WUDI Merging are modest and inconsistent.** OptMerge improves over WUDI by +0.44% on InternVL2.5 (Table 2), +1.9% on Hugging Face checkpoints (Table 6). On modality merging (Table 5), OptMerge (67.00) is outperformed by TSV Merging (67.34). The Qwen2-VL comparison is ambiguous due to the numerical discrepancy — depending on which WUDI value is correct, OptMerge either wins by a large margin or loses. The paper should discuss this variability more transparently rather than uniformly claiming superiority.

### Minor

1. **No variance estimates or statistical significance.** Methods are separated by fractions of a percent (e.g., 0.44% on InternVL2.5), yet no error bars, standard deviations, or multi-run results are reported. While this is not unusual in the model merging literature, the small margins make it more relevant.

2. **The λ search range [0.1, 0.3, 0.5, 0.7, 1.0, 1.5] has only 6 values.** The paper notes that Iso-C may need larger λ values but says increasing λ "only marginally improves results." A single shared λ range for all methods may penalize methods with different optimal schedules. The paper should clarify whether λ was tuned independently per method.

3. **The ablation study (Table 4) uses a WUDI baseline (58.65) that differs from Table 3's values** without explaining why. If the ablation is on a different data subset or evaluation configuration, this should be stated.

### Trivial

- The modality merging experiments (Table 5) use Vicuna-7B + separate encoders, while the capability merging experiments use InternVL2.5 / Qwen2-VL. These are different architectures, so the two settings are not directly comparable. This is a limitation that should be noted explicitly.

## Nice-to-Haves

- A proper Qwen2-VL mixture training baseline (training on combined task data, as was done for InternVL2.5) would either confirm or refute the "surpasses mixture training" claim.
- Reporting the un-merged average performance of the 4 Hugging Face checkpoints would clarify the value added by merging.
- Discussing failure cases (e.g., why Iso-C collapses to 26.69 on Qwen2-VL) would provide useful insights.

## Removed Points

*These points are flagged to be removed — treat with caution.*

**From Harsh Critic (removed or downgraded):**
- Claim that Theorem 3.1 is "best viewed as an illustrative framework rather than a core result" — this is a framing opinion, not a weakness. The paper clearly presents it as motivation for the benchmark's design.
- Criticism that scope is "limited (2 base models, 5 tasks)" — a first benchmark in a new area naturally starts with limited scope; the paper acknowledges this.
- Complaint about the "first benchmark" claim regarding AdaMMS/UQ-Merge — the paper already cites and distinguishes these works. AdaMMS merges only 2 MLLMs, and UQ-Merge treats each dataset as a task without capability categorization. The claim is precise enough.
- Complaint about missing "un-merged average" for Hugging Face experiment — moved to Nice-to-Haves.

**From Strength Finder (removed):**
- Generic strengths like "addressed an important problem" — removed for being too generic to add value.
- Overstated framing of Theorem 3.1 as a core strength — kept as a qualified strength but noted its asymptotic nature.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the paper's main claims (benchmark utility, method plausibility, modality merging potential) while highlighting specific issues that need correction — they do not surface a new perspective that the paper itself misses.

## Suggestions

1. **Critically: resolve the numerical inconsistencies in Table 3.** Verify all averages against the individual scores and correct any errors. Explain why the ablation WUDI baseline (58.65) differs from Table 3.
2. **Either run a proper mixture training baseline for Qwen2-VL or qualify the "surpasses mixture training" claim.** The current comparison against Qwen2-VL-Instruct is not a controlled baseline.
3. **Add variance estimates** across multiple runs or seeds, especially for the ablation where gains are small (0.44% on InternVL2.5).
4. **Report whether λ was tuned independently per method** and discuss the sensitivity of results to this choice.

## Score and Decision

**Calibration anchors** (all retrieved from the human-review corpus, topically similar):

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `fvUVe2gJh0` ("What Matters for Model Merging at Scale?") | 5.33 | R1 | Pure empirical study of model merging scaling; no method contribution, no numerical errors — slightly stronger execution than OptMerge |
| `Bq3fEAGXUL` ("Realistic Evaluation of Model Merging") | 5.33 | R1 | Evaluation-focused benchmarking paper; rejected despite clear presentation and no data errors |
| `t73rC2GJQJ` ("DMM: Distillation-Based Model Merging") | 4.50 | R1 | Method paper with modest gains; limited scope — most similar in profile to OptMerge |
| `Rc8z5wLzBF` ("OmniBench") | 5.75 | R1 | Benchmark paper with high-quality human annotations; less methodological contribution |
| `TE0KOzWYAF` ("VLM2Vec") | 6.00 | R1 | Multimodal embedding benchmark + method; accepted |
| `2rWbKbmOuM` ("MEGA-Bench") | 7.00 | R1 | Large-scale multimodal evaluation benchmark; accepted |

**Round 1 bracket:** I bracketed this paper between 4.0 and 5.5. "What Matters for Model Merging at Scale?" (5.33) is a cleaner empirical study, and OptMerge has more contributions (method + benchmark + theory) but also has numerical inconsistencies that the anchor lacks. DMM (4.50) is the closest profile — a method paper with modest gains — and OptMerge is slightly stronger due to its more comprehensive evaluation.

**Final score rationale:** The benchmark contribution is genuine and useful, and the modality merging experiments point in an interesting direction. However, the numerical inconsistencies in Table 3 (particularly the 3.68-point discrepancy for WUDI Merging) erode confidence in the core experimental results, and the "surpasses mixture training" claim is not supported by the best-controlled comparison. These are fixable issues, but as written they prevent acceptance. The paper is comparable to DMM (4.50) but slightly stronger in scope — hence 4.5.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>