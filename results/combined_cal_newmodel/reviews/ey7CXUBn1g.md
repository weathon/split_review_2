## Summary

AdaSVD proposes two improvements to SVD-based LLM compression: (1) **adaComp**, which uses Moore-Penrose pseudoinverse-based alternating updates to compensate for SVD truncation errors, and (2) **adaCR**, which assigns layer-specific compression ratios based on input-output cosine similarity. The paper targets genuine limitations in prior work and the adaComp component is technically well-motivated.

## Strengths

- **Clear problem identification and targeted method design.** The paper correctly identifies two genuine limitations of prior SVD-based LLM compression: (a) the lack of post-truncation re-optimization of U and V matrices, and (b) the use of uniform compression ratios across layers. The two proposed components (adaComp and adaCR) map directly onto these problems, giving the method a coherent internal logic.

- **Technical soundness of adaComp.** The use of the Moore-Penrose pseudoinverse to reformulate the U/V update as a stable least-squares problem (Section 3.1, Equations 8-13) is a reasonable and principled choice. The comparison in Figure 3(a) between naive gradient-based update and the pseudoinverse update supports the claim that this reformulation reduces numerical instability. This is the paper's strongest technical contribution.

- **Evaluation across multiple model families and compression ratios.** The experiments cover LLaMA2-7B, OPT-6.7B, Vicuna-7B, and Mistral-7B, at compression ratios from 40% to 80%, on both language modeling and common-sense reasoning benchmarks. The ablation study in Table 3 systematically isolates the contributions of adaComp and adaCR. The integration with GPTQ (Table 4) demonstrates orthogonality to quantization.

## Weaknesses

### Fatal

None.

### Major

1. **Baseline evaluation implausibility and internal inconsistency.** The original (uncompressed) LLaMA2-7B model's C4 perplexity is reported as **45.30** in Table 1 but as **7.34** in Table 4 — these should be the same value, and 7.34 is the expected perplexity for LLaMA2-7B on C4 (the C4 confusion matrix row in Table 4 correctly shows 7.34 for the original model at 0%). Additionally, the same model's MMLU accuracy is reported as **7.34%** in Table 1, which is below random guessing (25% for 4-choice) and far below the expected ~45%. These anomalies strongly suggest an evaluation pipeline error or data-entry mistake. If the baseline numbers are unreliable, the practical significance of all reported improvements is uncertain, even if relative rankings among compressed methods are preserved.

2. **Percentage improvement notation is undefined.** Throughout Table 1, perplexity values for AdaSVD are annotated with parenthetical percentages (e.g., "14.76 (18%)", "304.62 (158%)", "113.84 (112%)"). The paper never defines what these percentages represent. Attempting to reconstruct them as relative improvement over SVD-LLM gives inconsistent values (e.g., (16.11-14.76)/16.11 ≈ 8.4%, not 18%). Attempting to interpret them as gap-to-baseline closure also fails. Readers cannot interpret the claimed improvement magnitudes.

3. **Iteration-number claim contradicts the presented data.** Section 4.3 states: "under higher compression ratios, additional iterations lead to performance improvements." However, Table 3(c) shows that **1 iteration gives the best perplexity at ALL three compression ratios shown** (40%, 50%, 60%). Moving from 1 to 3 iterations consistently worsens results (e.g., WikiText-2 at 60%: 1 iter = 50.33, 3 iter = 64.12, 15 iter = 62.34; C4 at 60%: 1 iter = 239.18, 3 iter = 301.19, 15 iter = 267.29). The text's claim is directly contradicted by the data in the same table. (If the claim refers to 70%/80% results in the appendix, this must be explicitly qualified.)

### Minor

4. **adaCR's independent contribution is not well validated.** Table 3(a) shows that AdaSVD with adaCR but **without** adaComp is sometimes **worse** than the prior SOTA (SVD-LLM) — e.g., on C4 at 40%: 66.29 vs. 61.95; at 50%: 166.02 vs. 129.66. Only when adaComp is also present does adaCR consistently help (Table 3b). This suggests the two components are interdependent, and adaCR is not independently beneficial on its own, weakening the paper's framing of adaCR as a standalone contribution ("further enhancing performance").

5. **The layer-importance measure for adaCR lacks validation.** The paper defines layer importance as cosine similarity between input X and output Y of a weight matrix (Equation 17), with higher similarity → higher importance → less compression. This logic is not validated: the opposite intuition (that layers which barely transform their input are redundant and can be compressed more) is equally plausible. No experiment shows that this cosine-similarity measure correlates with actual sensitivity to SVD truncation (e.g., by comparing against an oracle allocation or a sensitivity sweep).

### Trivial

None.

## Nice-to-Haves

- Reporting variance across multiple calibration data seeds would strengthen the evidence, given the sensitivity of perplexity to calibration sample selection.
- A wall-clock time comparison vs. SVD-LLM would help practitioners assess the computational cost of the alternating update procedure.

## Removed Points

These points were considered but removed after verification against the paper:

- **"Table 3b shows adaCR sometimes hurts performance"** — factually incorrect; Table 3b shows adaCR (Adapt) consistently beats constant CR across all settings.
- **"Quantization reverses rankings in Table 4"** — the criticism compared AdaSVD+GPTQ vs SVD-LLM without GPTQ (apples-to-oranges); the fair comparison (AdaSVD+GPTQ vs SVD-LLM+GPTQ) shows AdaSVD+GPTQ winning consistently.
- **"Stack-of-batch memory motivation is questionable"** — difficult to verify without running the code; a minor engineering-convenience issue.
- Missing statistical significance, missing Table 2 in main text, and missing wall-clock time — typical nice-to-haves, not core flaws.
- Formatting/parser-artifact nitpicks.

## Novel Insights

The harsh critic's observation that the cosine-similarity importance measure has a logical tension (high similarity could indicate either importance or redundancy) is a genuinely insightful point that the paper does not address. The critic's cross-check between the iteration-number claim and the data in Table 3(c) is also a specific, verifiable finding that reveals a factual error in the paper's claims.

## Suggestions

1. **Fix the evaluation pipeline.** Reconcile the C4 perplexity inconsistency between Table 1 (45.30) and Table 4 (7.34) for the original model. Verify all baseline numbers against published reference values (e.g., LLaMA2-7B should achieve ~45% on MMLU, not 7.34%). Report corrected values in Table 1.

2. **Define or remove the percentage notation.** If these are relative improvements, state the formula explicitly. If they are parser artifacts, remove them. As presented, they are uninterpretable.

3. **Correct the iteration-number discussion.** The text claims more iterations help at higher ratios, but the data shows 1 iteration is best across all ratios in the main paper (40-60%). Either correct this claim or qualify it explicitly as referring to appendix results at 70-80%.

4. **Provide validation for the adaCR importance measure.** Show that the cosine-similarity measure correlates with actual sensitivity to SVD truncation, or replace it with a validated alternative.

5. **Acknowledge the interdependence of adaComp and adaCR.** The paper should honestly state that adaCR's benefit is contingent on adaComp being present, and that adaCR alone can underperform SVD-LLM.

## Score and Decision

**Round 1 bracket:** 3.5–5.5 (based on comparison with ASVD at 6.25, MoE-SVD at 5.00, AutoTrunc at 4.00).

**Round 2 narrowing:** Compared against ASVD (6.25) and Low-Rank Correction (5.00). AdaSVD's favorability profile: strengths at 9.5–12.4, weaknesses at –0.28 to 1.45. ASVD had similar strength favorability (10.7–12.7) but its most severe weakness (lack of memory/speedup experiments) had favorability –3.56 — the evaluation pipeline errors in AdaSVD (baseline inconsistency) are verifiable and more central to the paper's claims. Low-Rank Correction (5.00) had a clean evaluation setup. AdaSVD's baseline implausibility and the factual error about iteration number push it below both anchors.

**Final score:** 4.0. The paper has a genuine technical contribution (adaComp) that addresses a real gap in SVD-based LLM compression, and its method is technically sound. However, three major issues — baseline evaluation implausibility/inconsistency, undefined percentage notation, and a factual error in the iteration-number claim — collectively prevent acceptance in the current form. The paper would benefit from a corrected evaluation and a more honest presentation of adaCR's role.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>