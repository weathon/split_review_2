Now I have all the information I need. Let me write the final consolidated review.

## Summary

LoLoRA proposes combining local unsupervised updates (HPCA) for the LoRA A matrix during the forward pass with standard backpropagation for the B matrix, avoiding the need to store activations for A's backward pass. The paper also derives a theoretical result (Theorem 4.4) showing that, under a random regression model, the optimal A initialization spans the top PCA subspace of the input covariance. Experiments are conducted on NLU (GLUE/RoBERTa-large), math reasoning (LLaMA-3.1-8B/GSM8K), and multimodal (LLaVA-v1.5-7B) settings.

## Strengths

1. **Clean theoretical result (Theorem 4.4).** The paper derives the optimal initialization for the LoRA A matrix under a random regression assumption: any nonsingular linear transformation of the top-r principal components of the input covariance. This formalizes and extends the empirical EVA approach (Paischer et al., 2024). The proof structure (Theorems 4.4, 4.5, 4.6) is logically sound and provides a clear characterization of the asymmetry between A and B.

2. **Broad evaluation across multiple domains.** The paper tests on three distinct setups: NLU (RoBERTa-large on 8 GLUE tasks), mathematical reasoning (LLaMA-3.1-8B on MetaMathQA/GSM8K), and multimodal (LLaVA-v1.5-7B). Many PEFT papers test on only one setting.

3. **Thorough ablation study (Section 5.4, Tables 5-6).** The ablation on TinyLlama/Alpaca systematically compares four initialization strategies (uniform, orthogonal, PiSSA, EVA) across ranks r=2,4,8 and five local update rules (HPCA variants, AE, SoftHebb). This is well-designed and informative: it shows that all methods converging to the PCA subspace perform similarly.

## Weaknesses

### Major

1. **Central empirical claim — that LoLoRA improves over standard LoRA-FA — is not supported by the evidence.** The paper claims "HPCA consistently outperforms standard LoRA-FA in two out of three experimental setups" (Conclusion), but the data does not bear this out:

   - **GLUE (Tables 1-2):** LoLoRA HPCA is *worse* than LoRA-FA (uniform — the standard variant from Zhang et al., 2023b) on 5/8 tasks (CoLA: 66.3 vs 67.9; RTE: 84.6 vs 86.4; MNLI: 90.3 vs 90.6; QQP: 90.6 vs 90.8; SST-2: 96.4 vs 96.7), tied on 2/8 (MRPC, STS-B), and better on only 1/8 (QNLI: 94.7 vs 94.6). The paper's summary selectively compares to LoRA-FA (EVA) rather than the standard LoRA-FA (uniform).
   - **Math reasoning (Table 3):** LoLoRA HPCA (0.829±0.004) vs LoRA-FA uniform (0.826±0.005) — the 0.003 gap is well within 1 standard deviation and not statistically meaningful.
   - **Multimodal (Table 4):** LoLoRA HPCA (perplexity 2.93) improves over LoRA-FA uniform (2.97), but LoRA-FA (EVA) achieves 2.92 — *better* than LoLoRA.

   Taking all three settings together, the method does not convincingly outperform the simpler baseline it is designed to replace.

2. **Dynamic local updates add no demonstrated value over a good static initialization.** The ablation (Tables 5-6) shows that LoRA-FA (EVA) at r=8 achieves 2.536 perplexity while LoLoRA HPCA achieves 2.535 — essentially identical. Table 4 shows the same: LoLoRA HPCA (EVA) (2.93) is not better than LoRA-FA (EVA) (2.92). The paper itself acknowledges "all local update rules that converge to the optimal PCA subspace of the inputs perform equally well. Similarly, LoRA-FA with EVA initialization achieves comparable performance" (Section 5.4). The claimed advantage of online HPCA tracking over one-shot PCA initialization is not empirically supported. The main novelty over EVA — iterative adaptation — appears superfluous under the conditions tested.

### Minor

3. **Memory advantage over LoRA-FA is marginal or nonexistent.** LoLoRA uses 24.1 GB vs LoRA-FA's 23.9 GB on multimodal (Table 4), and both use 26 GB on math (Table 3). LoLoRA is never more memory-efficient than LoRA-FA. The abstract's claim of "further reducing the memory required for fine-tuning" is misleading if the comparator is LoRA-FA, which uses equal or less memory. The paper's own Conclusion acknowledges "our method introduces a small amount of extra optimizer state for the local updates, unlike standard LoRA-FA" — this caveat should appear much earlier.

4. **Theory-method gap.** Theorem 4.4 analyzes optimal *static initialization* of A under a model with stationary targets and i.i.d. Gaussian ΔW₀. The method's claimed novelty is *online* HPCA tracking during fine-tuning, motivated by "adapting to input distribution shifts." These are different regimes. The paper does not show that input distributions shift enough during fine-tuning to warrant online adaptation, nor does it measure whether HPCA-updated A actually diverges meaningfully from the EVA-initialized A over training. The gap is acknowledged in the Conclusion ("each submodule isolated with stationary targets, which is not strictly the case") but not bridged.

5. **GLUE experiments do not report the rank r used** (Tables 1-2), making it impossible to assess whether the comparison is affected by rank choice.

6. **Wall-clock time only reported for the multimodal experiment** (Table 4), not for GLUE or math, making runtime comparisons incomplete.

### Trivial

None.

## Nice-to-Haves

- A direct measurement of how much the HPCA-updated A diverges from the initial EVA-based A over training (e.g., cosine similarity or subspace distance), to validate whether the tracking mechanism is actually doing anything.
- A setting with deliberate non-stationary input distributions (e.g., curriculum learning, mixed-domain training) where online tracking might provide tangible benefits.
- A single accuracy-vs-memory Pareto figure aggregating results across all experiments.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Criticism that Section 3.2 citations are contradictory:** REMOVED — this is a misreading. The paper cites Zhang et al. (2023b) to show A is less critical (supporting the use of simpler local updates) and Zhu et al. (2024) for asymmetry. The paper then argues that *random* initialization is suboptimal, which does not contradict prior work showing that freezing A itself is acceptable.
- **Criticism that the "EVA underperforms" summary is selective:** REMOVED — data confirms EVA is worse than uniform on 7/8 GLUE tasks; the paper's statement is factually accurate.
- **Criticism about missing confidence intervals on memory measurements:** REMOVED — single-run GPU memory profiling is standard and generally deterministic; this is not a meaningful gap.
- **Criticism that Assumption 4.1 (i.i.d. Gaussian ΔW₀) is too strong:** RELEGATED to the "Nice-to-Haves" scope note. The paper explicitly acknowledges this limitation and the assumption is standard for tractable theoretical analysis.

## Novel Insights

None beyond the paper's own contributions. The reviewer's key observation — that LoLoRA's online tracking provides no measurable advantage over a one-shot PCA initialization (EVA), and that the paper's own ablation data shows this — emerges directly from the reported experiments.

## Suggestions

1. Reframe the paper's contribution as primarily the theoretical justification for PCA-based A initialization (Theorem 4.4), with LoLoRA positioned as a practical online variant that avoids a separate PCA pre-pass, rather than as a method that "improves over" LoRA-FA.
2. Report the rank used in the GLUE experiments.
3. Include runtime measurements consistently across all experimental setups.

## Score and Decision

**Bracket determination (Round 1):** After retrieving anchors across all score bands, the narrowest plausible range for this paper is 3.5–5.0. The paper has a genuine theoretical contribution and broader evaluation than most papers in the 3.0–3.5 range (HoLoRA: 3.00, ALLoRA: 3.33, UnoLoRA: 3.00), but its central empirical claim is unsupported, unlike the directly comparable LoRA-FA paper (5.33) which convincingly showed its method matches the baseline. The "Activations Aren't Cheap" paper (4.25) provides a useful midpoint: both have a simple core idea with limited novelty, but LoLoRA has stronger theory while having weaker empirical support. MoRA (4.75) had split reviews (8,3,3,5) and clearer advantages in specific settings.

**Round 2 narrowing:** Comparing against these anchors, the paper sits below LoRA-FA (5.33) — which demonstrated its method *matches* LoRA performance — because LoLoRA does not convincingly outperform its simpler baseline. It sits above ALLoRA (3.33) because the theory is cleaner and the evaluation broader. The score of 4.0 reflects a borderline-reject paper with genuine theoretical merit but a core empirical weakness that undermines the stated contribution.

**Anchors consulted:**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| LoRA-FA (RbKThNNFxr) | 5.33 | 1 | Stronger empirical support for simpler method |
| HoLoRA (igGeaxOiFM) | 3.00 | 1 | Narrower evaluation, no theory; LoLoRA stronger overall |
| ALLoRA (7X65yoKl3Y) | 3.33 | 1 | Similar marginal improvement but LoLoRA has cleaner theory and broader eval |
| MoRA (SxOrhLuuVz) | 4.75 | 1 | Split reviews; clearer advantage in specific tasks than LoLoRA |
| "Activations Aren't Cheap" (3ylNuZXtMg) | 4.25 | 2 | Similar level — useful idea with limited novelty; LoLoRA has better theory |
| UnoLoRA (49ti6LOUw5) | 3.00 | 1 | Narrower scope and less evaluation |
| L-MSA (xi3sDtf8A0) | 3.00 | 1 | Layer selection method, simpler scope |
| Me-LoRA (0qexTTfnmH) | 3.75 | 1 | Bayesian LoRA, different framing |
| ReLoRA (DLJznSp6X3) | 5.75 | 1 | Accepted; stronger empirical results with clear speedups |

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>