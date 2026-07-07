Here is the final consolidated review.

## Summary

This paper proposes LoLoRA, a method that uses local (gradient-free) learning rules (HPCA/AE) to update the LoRA matrix A during the forward pass, avoiding the need to store activations for A's backward pass. The paper also provides a theoretical characterization (Theorem 4.4) of the optimal fixed A under a random linear model, showing it should span the top‑r PCA subspace of the input covariance. The method is cleanly designed and the theory is sound, but the central empirical claim — that iterative local updates provide a useful alternative to a one‑time PCA initialization — is not supported by the evidence. LoLoRA performs indistinguishably from the simpler LoRA‑FA with EVA initialization across all experiments.

## Strengths

- **Clean theoretical characterization of optimal A (Theorem 4.4).** Under a random‑regression model (Assumption 4.1), the paper proves that the optimal frozen‑A initialization is any nonsingular transformation of the top‑r eigenvectors of the input covariance matrix. This formalizes and extends the empirical finding in EVA (Paischer et al., 2024) to a mathematically precise statement. The proof structure — treating fine‑tuning as low‑rank linear regression with an unknown target — is a reasonable idealization that yields a clear, communicable result. This is the paper's most solid contribution.

- **Methodological coherence.** LoLoRA is consistently motivated: LoRA‑FA saves memory by freezing A but random initialization is suboptimal under the theory; therefore update A using local rules that converge to the principal subspace without storing activations. Algorithm 1 is cleanly designed.

- **Honest ablation analysis.** Section 5.4 transparently shows that all local update rules perform equally well and that LoRA‑FA with EVA initialization achieves comparable performance. The paper acknowledges this tension with its core narrative: "Overall, all local update rules that converge to the optimal PCA subspace of the inputs perform equally well. Similarly, LoRA‑FA with EVA initialization achieves comparable performance."

- **Diverse experimental evaluation.** Experiments span NLU (GLUE/RoBERTa‑large), mathematical reasoning (GSM8K/LLaMA‑3.1‑8B), multimodal fine‑tuning (LLaVA‑v1.5‑7B), and ablations on TinyLlama, providing a reasonably broad testbed.

## Weaknesses

### Major

- **LoLoRA does not outperform the simpler LoRA‑FA with EVA initialization, which provides the same memory savings without the complexity of iterative local updates.** Across every experiment, LoLoRA performs indistinguishably from LoRA‑FA with EVA initialization:
  - **GSM8K (Table 3):** LoLoRA HPCA = 0.829 ± 0.004, LoRA‑FA (EVA) = 0.829 ± 0.005 — identical within precision.
  - **LLaVA (Table 4):** LoLoRA HPCA perplexity 2.93 ± 0.01 vs LoRA‑FA (EVA) 2.92 ± 0.01 — marginally worse.
  - **Ablations (Tables 5 vs 6):** LoRA‑FA (EVA) at r=8 gets 2.536; the best HPCA variant gets 2.535 — essentially identical.
  - **GLUE (Tables 1‑2):** Differences between LoLoRA and LoRA‑FA (EVA) are small and inconsistent (e.g., CoLA: 66.3 vs 64.7; MRPC: 89.9 vs 90.0).
  
  The iterative local updates — the entire algorithmic contribution of LoLoRA beyond the simpler LoRA‑FA — provide no measurable benefit. Since LoRA‑FA (EVA) requires no per‑step update rule, no extra optimizer state for A, and no forward‑pass computation for local steps, the added complexity of LoLoRA is not justified by the evidence. (The paper's conclusion claims "HPCA consistently outperforms standard LoRA‑FA in two out of three experimental setups," but "standard LoRA‑FA" refers to uniform initialization, not the EVA‑initialized variant which is the more informative baseline.)

- **The claim of "comparable performance to standard LoRA" in the abstract is not fully supported.** On 6 of 8 GLUE tasks, standard LoRA numerically beats LoLoRA, often with non‑overlapping error bars:
  - CoLA: 69.6 vs 66.3 (3.3 points)
  - MRPC: 90.9 vs 89.9 (1.0 points)
  - QQP: 91.7 vs 90.6 (1.1 points)
  - MNLI: 90.8 vs 90.3 (0.5 points)
  
  While LoLoRA matches or exceeds LoRA on GSM8K and LLaVA, the GLUE results contradict an unqualified claim of comparable performance. The paper does note this in Section 5.1 ("On GLUE, classical LoRA remains the strongest overall") but the abstract and conclusion would benefit from the same nuance.

### Minor

- **The theory (Theorem 4.4) characterizes the optimal *fixed* A under a random linear model — it does not provide a theoretical reason why iteratively updating A during training would be better than a one‑time PCA initialization + freeze (i.e., EVA).** The theorem's natural implication is: initialize A to span the PCA subspace, then freeze it. The paper then grafts on iterative HPCA updates as a way to reach this subspace online, but no theoretical result shows that iterative tracking helps over fixing. The paper's own ablation section confirms the two approaches perform equally. This gap between the theory and the method's central claim is a structural concern.

- **The rank r used in the GLUE, GSM8K, and LLaVA experiments is not stated in the main text.** The ablation experiments on TinyLlama use r ∈ {2,4,8} but the main experiments on RoBERTa‑large and LLaMA‑3.1‑8B do not specify the rank. Since performance and memory savings scale with rank, this is a significant omission for reproducibility.

- **LoLoRA's memory savings come from the same mechanism as LoRA‑FA (not storing activations for A), and LoLoRA adds extra optimizer state for the local updates.** On LLaVA, LoLoRA uses 24.1 GB vs LoRA‑FA's 23.9 GB — slightly *more* memory than the simpler baseline. The paper acknowledges this ("our method introduces a small amount of extra optimizer state for the local updates, unlike standard LoRA‑FA"), but it undercuts the narrative of "further reducing the memory required for fine‑tuning" relative to LoRA‑FA.

### Trivial

None.

## Nice‑to‑Haves

- Report the rank used for all main experiments in the main text.
- Include computational cost (FLOPs, wall time) of the local updates vs. a one‑time EVA initialization + freeze.
- Frame the theoretical characterization (Theorem 4.4) as the primary contribution, with LoLoRA presented as one practical implementation that achieves the same subspace online without requiring a separate PCA pass, rather than claiming it improves over EVA.

## Removed Points

The following points from the input review are removed per policy:

- **"No theoretical result shows that iteratively tracking helps over fixing"** — Moved to Minor (theory doesn't support the iterative claim) because the paper does not actually claim such a result; it claims the theory motivates *what* A should converge to, and HPCA achieves that convergence iteratively.
- **Section‑by‑section notes about best‑checkpoint reporting, in‑distribution validation, and "slightly better" framing** — Removed as these are observations about standard experimental practices and minor phrasing choices, not substantive weaknesses.
- **Criticisms about missing appendix content** — Removed per policy (parser strips appendices; they exist in the original submission).
- **"Missing related works"** — Removed per policy; I cannot verify which works are missing.
- **Formatting and style nitpicks** — Removed per policy; these are parser artifacts, not author errors.

## Novel Insights

The key tension exposed by this review is that the paper contains a genuine theoretical contribution (characterizing the full family of optimal A under a random linear model, which formalizes EVA's empirical finding) but the method built on this theory does not outperform the simpler baseline that the theory also validates (EVA initialization + freeze). The paper's own ablation section honestly acknowledges this. This creates an unusual scenario where the theoretical contribution is solid but the proposed method's claimed advantage over the baseline is not empirically supported — the theory validates the simpler baseline as much as (if not more than) the proposed iterative method.

## Suggestions

1. **Reframe the paper** around the theoretical characterization of optimal A (Theorem 4.4) as the primary contribution, with LoLoRA presented as a practical online implementation that matches EVA without requiring a separate PCA pass, rather than claiming iterative updates provide a performance advantage.
2. **State the rank for all experiments** explicitly in the main text.
3. **Either identify a setting where iterative local updates provide a statistically significant benefit** over one‑time EVA initialization + freeze, or present LoLoRA honestly as an alternative that trades simplicity (no separate PCA pass) for slightly more online complexity.
4. **Qualify the "comparable performance to standard LoRA" claim** to reflect that on GLUE specifically, LoLoRA consistently underperforms standard LoRA.

## Score and Decision

**Calibration.** My draft's weighted items were compared against four anchors:

| Anchor | Avg Score | Comparison |
|--------|-----------|------------|
| LoRA‑FA (RbKThNNFxr.md) | 5.33 | LoLoRA has stronger theory (+4.65 vs +3.77 top strength) but same core weakness: incremental method with unclear benefit. LoLoRA's top weakness (−6.26) is slightly less severe than LoRA‑FA's (−8.03). |
| EVA (DM6Q45HWSk.md) | 4.75 | LoLoRA directly builds on EVA by adding the theoretical justification EVA was criticized for lacking. But LoLoRA's method does not outperform EVA, which was itself criticized for minimal improvement (−6.52). |
| ALLoRA (7X65yoKl3Y.md) | 3.33 | LoLoRA is stronger: it has cleaner theory, more coherent motivation, and better experimental coverage. |
| HoLoRA (igGeaxOiFM.md) | 3.00 | LoLoRA is significantly stronger: the theory is original, not a trivial application of existing tools. |

**Round 1 bracket: 3.5–5.5.** The paper is clearly better than the 3‑point papers (HoLoRA, ALLoRA) which have weaker theory and experiments. It is comparable to the EVA paper (4.75) but adds the theoretical justification EVA lacked. However, like the LoRA‑FA paper (5.33), the method's contribution is incremental. The decisive factor is that LoLoRA's iterative updates provide no measurable benefit over the simpler LoRA‑FA (EVA) — the very baseline the theory also validates. This places the paper near the lower end of its bracket.

**Final score: 4.5.** The theoretical contribution (Theorem 4.4) is genuine and advances understanding of LoRA initialization. But the paper's framing and central claim about LoLoRA's iterative method are not supported by the evidence. The method does not outperform a simpler existing baseline, and claims of "comparable performance to standard LoRA" are overstated on the GLUE benchmark.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>