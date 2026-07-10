Now I have all the information. Let me synthesize the final review.

---

## Summary

This paper investigates how to maximize reasoning capabilities in sub-billion-parameter language models through principled data curation. The authors propose a pipeline combining: (1) leave-one-out analysis to identify which data sources matter for reasoning, (2) influence-based data mixing that uses cross-capability influence scores on curated probing datasets rather than benchmark test sets, and (3) iterative mid-training compression that discards negative-influence samples. The resulting MobileLLM-R1 models (140M–950M parameters) substantially outperform existing fully-open-source models at similar scales, and the controlled SFT comparison (Table 2) provides clean evidence that the pre-training/mid-training recipe drives these gains.

## Strengths

- **Non-obvious empirical findings from the leave-one-out analysis (Section 2.1.2, Figure 3).** The observation that FineWeb-Edu acts as a "glue" connecting heterogeneous domains across math, code, and knowledge is a concrete and useful insight. The finding that StarCoder benefits math more than OpenWebMath benefits code reverses a commonly held assumption from Lewkowycz et al. (2022) and is a genuine empirical contribution.

- **Controlled SFT comparison (Table 2) provides clean causal evidence.** Under *identical* reasoning SFT data, MobileLLM-R1-950M achieves 57.8% MATH vs 41.4% for SmolLM2-1.7B-Instruct and 53.0% for OLMo-2-1.48B-SFT, despite having fewer parameters. This is the paper's strongest evidence that the pre-training/mid-training recipe, not post-training data quality, drives the gains.

- **Substantial transparency commitment.** The paper releases weights, data provenance, and training recipes for all three model scales (140M, 360M, 950M), enabling direct reproducibility and community follow-up work.

## Weaknesses

### Fatal
None.

### Major

- **The headline token-efficiency comparison ("4.2T vs 36T, just 11.7%") conflates two confounds that are never properly disentangled.** First, MobileLLM-R1-950M (949M params) is compared to Qwen3-0.6B (~600M params) — a 58% capacity advantage — so the comparison mixes model-scale efficiency with data efficiency. Second, the 4.2T is obtained by resampling ~2T unique tokens approximately 2×, while Qwen3's 36T is described as a proprietary corpus (it is unclear whether this figure is unique or total tokens). The paper does disclose the resampling ("resampled from these ~2T tokens," Abstract) but never separates unique-vs-unique from total-vs-total in the headline comparisons, making the apparent ~9× gap potentially overstated. The core claim (the method is data-efficient) is directionally correct, but the framing overstates the case in a way that could mislead a casual reader.

- **No statistical variance or significance is reported anywhere.** Despite a complex multi-stage pipeline (LOO analysis with multiple dataset removals, influence computation at 10 checkpoints, iterative mid-training compression, two-stage SFT ablation), no result reports variance across seeds, no learning curves show error bands, and no claim is accompanied by a significance test. For a paper whose central contribution is a *methodology* for data curation — as opposed to a single best-result benchmark paper — this is a significant evidential gap. Single-run results from a pipeline with many design choices do not demonstrate that the method is robust.

### Minor

- **The "benchmark-free" framing is technically accurate but practically overstated.** The paper never uses benchmark *test sets* for data selection, which is principled. However, the capability-probing datasets are explicitly constructed via hierarchical rejection sampling to be "faithful proxies for reasoning performance" (line 105) from the same domains as the benchmarks (code from StarCoder, math from OpenWebMath, knowledge from FineWeb-Edu/Wikipedia). Calling this "benchmark-free" implies a stronger separation from benchmark optimization than actually exists; a more honest framing would be "we avoid optimizing on test set distributions while optimizing for correlated proxy distributions."

- **The iterative mid-training data compression (Section 3) has a self-reinforcing bias that is not discussed.** The procedure discards samples with zero or negative influence (Eq. 6), but early in training the model may not recognize the value of hard but ultimately beneficial examples. The filtered-out data could include samples that would become valuable later, after the model has acquired prerequisite knowledge. The "convergence" shown in Figure 5 could equally indicate that the model has been trained on a narrowing distribution that no longer provides novel signal — not that the original dataset's information is exhausted, but that the *selected subset's* information is.

- **The base model (MobileLLM-R1-950M-base) shows a striking asymmetry:** 46.3% HumanEval (highest among sub-1B models) but only 5.0% GSM8K (vs Qwen3-0.6B-base at 61.6%). This suggests strong specialization toward code at the expense of math in the base model, which the post-training SFT must correct. The paper notes this asymmetry but does not analyze why it occurs or whether the pre-training data curation causes it.

### Trivial

- The observation in Table 1 that adding *both* math and code reduces MMLU more than adding either alone (Tulu-3+M+S vs Tulu-3+M+C+S drops MMLU from 45.0 to 43.7) is noted but not explored. A brief discussion would strengthen the analysis.

## Nice-to-Haves

- Adding a simpler data curation baseline (e.g., heuristic upweighting of code/math data) would help show whether the sophisticated influence-based method adds value over reasonable heuristic mixtures.
- Running the full pipeline with 2–3 seeds for the main results would substantially increase confidence.
- The controlled SFT comparison (Table 2) could be foregrounded more prominently as the paper's cleanest evidence.

## Removed Points

- Generic/problem-importance strength ("the paper tackles a genuinely important problem") — removed as it lacks specific content about the paper itself.
- Concern about LOO equal-probability sampling — the paper transparently discloses this design choice (line 137); it is a deliberate normalization, not a flaw.
- Concern about incremental novelty over AutoMixer — the paper clearly describes its extension (capability-probing datasets, cross-capability influence), which is a reasonable contribution.
- Various formatting and style nitpicks — parser artifacts, not author errors.

## Novel Insights

The reviewer's identification of the parameter mismatch in the headline token-efficiency comparison (949M vs ~600M) is a genuinely useful calibration point that the paper should address responsibly. The observation that the paper's strongest evidence (controlled SFT in Table 2) is structurally under-emphasized relative to the more confounded Qwen3 comparison is a helpful framing insight. The self-reinforcing bias in the mid-training compression is a real limitation that is absent from the paper's discussion.

## Suggestions

- **Restate the Qwen3 comparison more honestly:** separately report unique-token and total-token ratios, acknowledge the parameter-size gap (949M vs ~600M), and do not let this single comparison carry the paper's central narrative.
- **Add variance reporting** (at minimum 2–3 seeds) for the main benchmark results (MATH, GSM8K, HumanEval).
- **Add a non-trivial baseline** to the datamixing comparison (e.g., heuristic upweighting of code/math data) to demonstrate that the influence method adds value.
- **Explicitly discuss** the limitation of iterative influence-based filtering discarding potentially valuable hard examples.
- **Foreground Table 2** (controlled SFT comparison) more prominently in the evaluation as the strongest evidence for the core claim.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>