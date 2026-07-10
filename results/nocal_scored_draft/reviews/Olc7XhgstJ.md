Now let me finalize the review with my assessment weighted by these signals.

## Summary

This paper proposes Steady Thought (ST), a framework to mitigate the "under-thinking" phenomenon in large reasoning models — where models excessively switch between reasoning thoughts before fully developing promising ones. ST operates in three stages: segmenting model responses into thought sequences via entropy-based detection, forcing the model to complete reasoning from each thought without switching (via logit suppression of trigger words), and performing thought-level preference optimization (STPO) to teach the model to commit to promising reasoning trajectories. Experiments on three model sizes (1.5B, 8B, 14B) across math and coding benchmarks show consistent accuracy improvements (up to 5.3%) with substantial token reductions (up to 39.3%), including on out-of-distribution code tasks.

## Strengths

- **Novel framework design.** ST is genuinely different from prior under-thinking mitigation methods: instead of suppressing switching globally (at the token or representation level), it uses thought-level preference optimization to teach the model *when* to commit vs. explore. The three-stage pipeline (segmentation, completion, preference optimization) is a coherent and non-obvious design.
- **Compelling out-of-distribution generalization evidence.** On LiveCode (code tasks), despite training only on math data, ST improves Qwen3-8B accuracy by 5.3% while reducing token count by 19.0%. This suggests the method teaches a generalizable reasoning pattern rather than dataset-specific memorization.
- **Multi-scale validation.** Testing on three model sizes (1.5B, 8B, 14B) and four datasets (MATH-500, AIME 2024, GSM8K, LiveCode) shows consistent accuracy improvements (up to 5.3%) and token reductions (up to 39.3%) across architectures and scales.
- **Well-motivated problem with empirical grounding.** Figures 1a/1b provide evidence that models often discover correct reasoning early yet fail to commit, establishing the under-thinking phenomenon concretely before introducing the method.

## Weaknesses

### Fatal
None.

### Major

- **Conditioning mismatch between theoretical framing and the STPO loss.** The paper formalizes the problem using the full prefix $\mathbf{P}_i = (\mathbf{x}, T_1, \dots, T_i)$ (Section 2.1, Equations 1-2), defining the steadiness score $S_\pi(\tau|\mathbf{P}_i)$ over this full prefix. However, the actual STPO loss (Equation 7) conditions both the chosen and rejected responses on $(Q, T_i)$ alone. The rejected trajectory $\mathbf{y}_l = (T_{i+1}, \dots, T_n)$ was originally generated from the full prefix $(Q, T_1, \dots, T_i)$; evaluating its likelihood under the truncated conditioning $(Q, T_i)$ can artificially lower its probability if $T_{i+1}$ references earlier context. This introduces a potential confound into the preference margin — the model could learn that continuations without their preceding context are improbable, a shortcut unrelated to reasoning quality. The paper neither acknowledges nor justifies this discrepancy. While the chosen response (generated via forced completion from $(Q, T_i)$) is correctly conditioned, the asymmetric conditioning means the preference comparison may partly reflect context-mismatch artifacts. This is a significant methodological gap that should be addressed (e.g., by conditioning on the full prefix, or providing analysis showing that the truncation does not materially affect the results).

### Minor

- **The NOWAIT baseline results on Qwen3-8B appear anomalous.** On MATH-500, accuracy drops from 91.4% to 61.0% while token count *increases* from 4,724 to 13,274 — the opposite of what NOWAIT is designed to do (suppress reflection tokens to reduce length). Similarly on GSM8K, tokens increase from 1,759 to 12,369 (a 7× increase). This suggests either an implementation issue or hyperparameter mismatch for this specific model, undermining the meaningfulness of ST's comparison against this baseline on Qwen3-8B. (This does not affect ST's core results, which are evaluated primarily against the Vanilla model.)
- **Variance not reported despite multiple runs.** The paper states it averaged 8 runs for AIME 2024 (30 problems) and 2 runs for LiveCode, but reports only point estimates. A 3.7-point gain on AIME 2024 (e.g., 62.1% → 65.8% on Qwen3-8B) corresponds to roughly 1 more problem correct. Without confidence intervals, the reader cannot assess statistical reliability.
- **The PCT metric conflates distinct explanations.** The paper interprets a lower percentage of correct intermediate thoughts as evidence of fewer invalid switches (Section 4.4.2). However, this could also indicate that the model generates fewer correct intermediate thoughts overall because its intermediate reasoning is less productive — the metric cannot distinguish between reduced switching and degraded reasoning quality. This ambiguity is compounded by the DeepSeek-R1-Distill-Qwen-1.5B AIME2024 case, where thought count increases (12.87 → 18.21) while PCT decreases.
- **The AIME2024/1.5B case is not fully reconciled with the central narrative.** For DeepSeek-R1-Distill-Qwen-1.5B on AIME2024, ST *increases* the number of thoughts (12.87 → 18.21) while *decreasing* the proportion of the last thought (18.96% → 15.66%). The paper's explanation is reasonable but leaves open the question of what mechanism produces more — not fewer — thoughts under a method designed to reduce switching.

### Trivial

- **Incomplete trigger word list.** Section 3.2 gives only "wait" and "alternatively" as examples. A complete list is important for reproducibility since the method's second stage depends critically on these words.

## Nice-to-Haves

- A direct evaluation of segmentation quality (e.g., agreement with human-annotated thought boundaries or comparison against alternative segmentation methods) would strengthen confidence in the first pipeline stage.
- A mechanistic analysis (e.g., probing switch-token probabilities or entropy patterns before/after ST) could demonstrate that the method actually alters switching behavior rather than shortening outputs through other means.
- Reporting training data size, number of preference pairs, and compute cost would help assess practical utility.

## Removed Points

These points from the harsh critic input were filtered out:

1. *"ST is compared only against inference-time baselines, not training-based alternatives"* — **Removed.** The paper includes SFT, DPO, and STPO as training-based ablations in Table 4, and the cited prior work does not provide an off-the-shelf training-based under-thinking method with a clear implementation to compare against.
2. *"Segmentation quality not directly evaluated"* — **Removed.** This is covered by Nice-to-Haves; tuning the entropy threshold via downstream performance is a standard approach.
3. *"Chosen training data produced under artificial constraints"* — **Removed.** This is a general property of most preference optimization pipelines (chosen responses are often constructed under different conditions than the model naturally generates), not a specific flaw in this paper.
4. Various generic/superlative strengths — **Merged** into the four concrete strengths listed above.

## Novel Insights

None beyond the paper's own contributions. The conditioning-mismatch observation (Major weakness) is a methodological insight that surfaced through review but is not addressed in the paper.

## Suggestions

1. **Address the conditioning mismatch.** Either modify the STPO loss to condition the rejected response on the full prefix $\mathbf{P}_i$ (and justify why the chosen response can remain conditioned on $(Q, T_i)$), or provide empirical analysis showing that the truncated conditioning does not materially distort likelihood estimates (e.g., by comparing log-probabilities under both conditionings on a sample).
2. **Report variance/confidence intervals** for AIME 2024 (8 runs) and LiveCode (2 runs) to establish statistical reliability.
3. **Clarify or fix the NOWAIT baseline** on Qwen3-8B — either report corrected results or explain the anomalous behavior.
4. **Provide the complete trigger word list** used in Stage 2 for reproducibility.
5. **Reconcile the AIME2024/1.5B case** with the paper's narrative of reduced switching — analyze why thought count increases under ST for this particular configuration.

## Score and Decision

The paper addresses a timely problem and proposes a genuinely novel approach with consistent empirical support across multiple models and datasets, including compelling OOD generalization. The primary concern is the conditioning mismatch in the STPO loss — a real methodological gap that the paper does not address. However, the empirical results (STPO > DPO > SFT across metrics) and the consistent improvements across diverse settings suggest the approach is working despite this imperfection, and the issue is addressable in revision. On balance, the contributions are sufficiently novel and well-supported to merit acceptance pending satisfactory rebuttal of the conditioning concern.

**MY FINAL SCORE: <score>6</score>**
**MY FINAL DECISION: <decision>Accept</decision>**