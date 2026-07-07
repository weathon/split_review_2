Now I have enough anchors to write the final review.

**Bracket after Round 1:**
- LoRA-FA (the direct baseline, score 5.33) is the closest anchor — it achieved 5.33 despite clear memory savings. LoLoRA adds theory but fails to demonstrate clear empirical improvements over LoRA-FA.
- ALLoRA/HoLoRA/UnoLoRA (score 3.0–3.4): LoRA variants with weaker contributions than LoLoRA's theoretical results.
- VeRA (score 7.25): Clear parameter efficiency gains and robust empirical support.

LoLoRA sits between the 3.5–5.5 band. Its genuine theorems (Theorem 4.4/4.5/4.6) and multi-setting evaluation push it above the pure-noise LoRA variants (3.0–3.4), but the marginal/within-noise empirical improvements and misleading memory framing keep it below the LoRA-FA baseline (5.33). I anchor at **4.5**.

---

## Summary
LoLoRA is a hybrid LoRA fine-tuning method that applies gradient-free HPCA updates to the A matrix during the forward pass, allowing A to track the principal subspace of the input covariance without retaining activations for backpropagation. The paper provides a formal theoretical justification (Theorem 4.4) showing that under a Gaussian random-regression assumption, the optimal frozen A is a nonsingular transformation of the top-r principal components of the input covariance, and evaluates the method on GLUE (RoBERTa), GSM8K (LLaMA-3.1-8B), and LLaVA-v1.5-7B.

## Strengths
- **Theorem 4.4 is a genuine, exact theoretical result.** It characterizes the full set of optimal A initializations as nonsingular linear transformations of the top-r eigenvectors of the input covariance matrix, providing a formal post-hoc justification for the empirically-motivated EVA initialization. The asymmetry result (Theorem 4.5: any full-rank B is equally good; only A has a privileged initialization) is clean and consistent with prior empirical findings (Zhu et al., 2024).
- **Algorithm 1 is mechanically sound and requires no separate pre-training PCA pass.** A is updated in the forward pass via HPCA using the current input, the input is freed before backprop, and only the low-dimensional bottleneck u = Az is retained for B's gradient. This correctly eliminates A's activation storage, unlike EVA which requires a separate data pass before training.
- **Three-setting evaluation** (encoder NLU, decoder math reasoning, multimodal instruction tuning) provides appropriate breadth for the generalizability claim.

## Weaknesses

### Fatal
None.

### Major
- **The empirical case for LoLoRA over LoRA-FA is not statistically supported across any experiment.** In GSM8K (Table 3), LoLoRA HPCA (0.829 ± 0.004) ties LoRA-FA EVA (0.829 ± 0.005); its margin over LoRA-FA uniform (0.826 ± 0.005) is smaller than 1σ. In LLaVA (Table 4), LoLoRA HPCA (2.93 ± 0.01) is worse than standard LoRA (2.90 ± 0.01) and within noise of LoRA-FA EVA (2.92 ± 0.01); it beats only LoRA-FA uniform (2.97 ± 0.01) by one overlapping standard deviation. On GLUE (Tables 1–2), LoLoRA underperforms LoRA-FA uniform on CoLA (66.3 vs 67.9), RTE (84.6 vs 86.4), and MNLI (90.3 vs 90.6). The conclusion's claim that "HPCA consistently outperforms standard LoRA-FA in two out of three experimental setups" is technically against LoRA-FA uniform only and even then the differences are within measurement noise. This is an overstatement of the evidence.

- **LoLoRA uses more memory than LoRA-FA in every reported experiment.** In Table 4, LoLoRA requires 24.1 GB vs LoRA-FA's 23.9 GB. In Table 3, both show 26 GB (tied at best). The "13% extra memory reduction" (26 GB vs 30 GB for standard LoRA) is computed relative to standard LoRA, not relative to LoRA-FA. The paper itself concedes "our method introduces a small amount of extra optimizer state for the local updates, unlike standard LoRA-FA." The headline trade-off — better performance than LoRA-FA at comparable or lower memory — is not demonstrated.

### Minor
- **Assumption 4.1 introduces a gap between the theory and practice.** Theorem 4.4 assumes ΔW₀ has i.i.d. Gaussian entries, meaning the fine-tuning target is completely task-agnostic in direction. In practice ΔW₀ is highly structured and task-correlated, which is the whole reason LoRA works. The paper's limitations section (Section 6) mentions stationarity but does not address this assumption; the Gaussian assumption is arguably a more fundamental concern than stationarity for the theory's practical relevance.

- **EVA underperformance on GLUE is unexplained.** Since EVA is the data-driven initialization that the theory identifies as optimal, its consistent underperformance vs. uniform initialization on GLUE (LoRA-FA EVA CoLA: 64.7 vs LoRA-FA uniform: 67.9) deserves analysis. The paper simply notes "EVA initialization underperforms on this setting" without comment.

- **Memory accounting is incomplete.** Peak extra memory = total peak − model storage conflates optimizer state for A, gradient buffers, and activation memory. Since activation memory elimination is LoLoRA's core claim, a breakdown by component would substantiate it directly, rather than requiring inference from total peak numbers.

### Trivial
- Section 3.2 states "freezing A matrix during fine-tuning does not influence much the overall LoRA's performance," yet Tables 1–2 show drops of up to ~2 points (CoLA: 69.6 → 67.9). The framing slightly overstates the benignness of freezing.

## Nice-to-Haves
- An analysis of how much A's row space actually shifts during LoLoRA training (e.g., cosine similarity between initial and converged subspace, per layer) would clarify whether HPCA provides genuine online adaptation or mainly approximates a good static initialization. This distinction is central to the paper's thesis.
- Empirical validation that the LoLoRA–LoRA-FA performance gap scales with spectral imbalance of the input covariance (as the theory predicts when λ₁ ≫ λ_r) would link theory to experimental outcomes.
- Significance tests or explicit reporting of whether confidence intervals overlap when comparing methods.

## Removed Points
*These points are flagged to be removed, treat them with caution.*

- **LLaVA memory explanation is "ad hoc"** — The paper's explanation (short text relative to image tokens) is a reasonable mechanical account and not a weakness. Removed.
- **Ablation tables have overlapping confidence intervals** — The ablations are framed as exploratory and the paper's conclusion ("perform equally well") is measured. The overlap is informative about null differences, not a flaw. Removed.

## Novel Insights
The most substantive implicit finding of the paper is that LoLoRA's online HPCA updates converge to approximately the same subspace that EVA finds via offline PCA, producing nearly identical performance across all three benchmarks. This empirically suggests the value of LoLoRA is primarily its initialization-free convenience — no separate PCA pass is required — rather than any dynamic advantage from online A adaptation during training. If that framing is correct, the paper would be more precisely described as: a theoretically grounded, computationally online substitute for EVA initialization, with the minor cost of extra local optimizer state and the minor advantage of not requiring a pre-training data pass.

## Suggestions
- Revise the conclusion to accurately state that LoLoRA matches (but does not clearly improve upon) LoRA-FA empirically, and that its primary practical advantage over EVA is eliminating the separate PCA pass.
- Address Assumption 4.1's Gaussian ΔW₀ restriction in the limitations; discuss when this is and is not reasonable relative to the task distribution.
- Provide a per-component memory breakdown (activation vs. gradient vs. optimizer state) to support the claim that activation memory is reduced.
- Include an analysis or discussion of why EVA underperforms uniform initialization on GLUE despite being theoretically motivated.

## Score and Decision

**Anchors used:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `7X65yoKl3Y.md` (ALLoRA) | 3.33 | 1 | LoRA variant with adaptive LR; rejected. LoLoRA's theory is stronger, but empirical case similarly weak. |
| `igGeaxOiFM.md` (HoLoRA) | 3.00 | 1 | LoRA + orthogonal fine-tuning; rejected for limited benefit. LoLoRA's theorems give it more substance. |
| `49ti6LOUw5.md` (UnoLoRA) | 3.00 | 1 | Shared LoRA for multi-task; rejected. Less theoretical depth than LoLoRA. |
| `RbKThNNFxr.md` (LoRA-FA) | 5.33 | 1 | The direct baseline; borderline reject at 5.33. LoLoRA adds theory but not clear empirical gains over LoRA-FA. |
| `SxOrhLuuVz.md` (MoRA) | 4.75 | 1 | LoRA variant with high-rank updates; borderline reject. Somewhat stronger empirical case than LoLoRA. |
| `3ylNuZXtMg.md` (Activations) | 4.25 | 1 | Analysis of LoRA memory; reject. Similar insight depth. |
| `qOqCXEXsX4.md` (LoTA) | 4.25 | 1 | Sparse adaptation; reject. |
| `DLJznSp6X3.md` (ReLoRA) | 5.75 | 1 | High-rank training via low-rank updates; borderline accept. Stronger empirical gains than LoLoRA. |
| `s7DkcgpRxL.md` (LoRAM) | 6.20 | 1 | Memory-efficient LoRA training with clearer gains; accept. LoLoRA's empirical case is weaker. |
| `NjNfLdxr3A.md` (VeRA) | 7.25 | 1 | Clear parameter efficiency + robust evaluation; strong accept. LoLoRA does not reach this bar. |
| `lR7rqLtsXZ.md` (Fira) | 5.75 | 1 | Low-rank memory efficient; borderline accept. Stronger empirical support than LoLoRA. |
| `TwJrTz9cRS.md` (HiRA) | 8.00 | 1 | Outperforms LoRA on multiple tasks with robust ablations; strong accept. LoLoRA does not approach this. |

**Round-1 bracket:** 4.0–5.5. The LoRA-FA paper (5.33) is the natural ceiling since LoLoRA is an incremental extension that doesn't clearly surpass its baseline empirically, while the 3.0–3.4 LoRA variants lack LoLoRA's theoretical content. The genuine Theorems 4.4/4.5 and multi-setting evaluation push LoLoRA above the weakest band; the weak and misleading empirical framing keeps it below LoRA-FA. Final score: **4.5**.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>