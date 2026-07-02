## Summary
This paper proposes SparseFW, a post-training LLM pruning method that relaxes the binary mask selection problem into a convex optimization over the convex hull of binary masks, solved via the Frank-Wolfe (FW) algorithm. The key idea is to replace the combinatorial $\ell_0$ constraint with an $\ell_1$ budget on continuous mask variables, enabling gradient-based optimization that accounts for weight interactions — unlike greedy heuristics (Wanda, SparseGPT, RIA) that prune one weight at a time. The method is warm-started from a Wanda or RIA mask and fixes a large fraction (typically 90%) of high-saliency weights as unprunable, optimizing only the remaining 10% via FW. Experiments across five modern GPT architectures (LLaMA-3.1-8B, Gemma-2-9B, Yi-1.5-9B, DeepSeek-7B, Qwen2.5-7B) at 50%, 60%, and 2:4 sparsity show consistent reductions in per-layer reconstruction error (20-80%) and modest perplexity/accuracy improvements over Wanda and RIA. A theoretical bound (Lemma 1) connects the FW solution to the original combinatorial problem.

**Novelty/comparison assessment (deferred):** External literature verification was unavailable in this run; novelty conclusions are deferred for manual verification. The core technical contribution — using FW for convex relaxation of the pruning mask problem — appears novel relative to the greedily described baselines (Wanda, SparseGPT, RIA), but the heavy reliance on Wanda's saliency prior (90% weight fixing) blurs the boundary between the proposed method and existing saliency-based approaches.

## Strengths
1. **Technically sound problem reformulation.** The paper's core idea — relaxing the combinatorial mask selection to a convex program over the convex hull of binary masks and solving via FW — is mathematically principled. The relaxation is well-motivated (Figure 1 provides a clear geometric illustration), and the use of FW is appropriate given the structure of the feasible set (projection-free optimization with efficient LMO).

2. **Clear exposition of greedy limitations.** Section 2.1 provides a clean derivation showing that Wanda, SparseGPT, and RIA all solve simplified per-weight subproblems that ignore weight interactions. This connection between heuristic methods and optimization principles is pedagogically valuable and strengthens the motivation for the proposed relaxation.

3. **Consistent empirical improvements at high sparsity.** At 60% unstructured sparsity and 2:4 semi-structured sparsity, SparseFW (with warm-start) consistently improves perplexity and zero-shot accuracy over Wanda and RIA across multiple model families. The per-layer reconstruction error reductions (20-80% in Figure 2) confirm that the FW optimization effectively minimizes its intended objective.

4. **Good iteration and sample efficiency analysis.** Figure 3 provides useful ablation showing that SparseFW benefits from more calibration samples (unlike Wanda which saturates) and that 2000 iterations are sufficient for convergence. The computational cost analysis (independence of FW iteration cost from sample count) is correctly reasoned.

5. **Architecture generality.** Experiments span five model families (LLaMA-3.1, Gemma-2, Yi-1.5, DeepSeek, Qwen2.5) from 7B to 14B parameters, demonstrating that the approach generalizes beyond specific architectures. Both unstructured and semi-structured (2:4) sparsity patterns are evaluated.

6. **Honest limitation disclosure.** The paper candidly admits that vanilla FW (α=0) degrades performance, that the local-global objective mismatch persists, and that inductive biases (saliency-based weight fixing) remain necessary. This transparency is commendable.

## Weaknesses
### W1 (Critical) — Vanilla FW degrades performance; success requires 90% weight-fixing from Wanda
The paper's central finding is that FW optimization alone (*α*=0) "consistently yields worse results than the baselines" (Page 5, Section 2.3). The best configuration fixes 90% of weights using Wanda's saliency scores and optimizes only the remaining 10%. This means the contribution is not FW-based pruning *per se*, but a hybrid method that relies almost entirely on the baseline's saliency ranking. The paper frames this as a minor caveat, but it fundamentally changes the interpretation: SparseFW is a refinement of Wanda (on 10% of weights), not an independent alternative to greedy methods.  

**Required action:** Restructure the contribution framing to honestly reflect the hybrid nature. Add analysis of *why* the local-global mismatch occurs — is it because the quadratic objective underestimates the importance of certain weights for cross-layer propagation? Include a scatter-plot comparison of Wanda saliency scores vs. FW's learned mask values.

### W2 (Major) — Missing SparseGPT comparison weakens empirical positioning
The paper explicitly excludes SparseGPT (the most popular LLM pruning method) with the justification that it "involve[s] a reconstruction step." However, the Introduction repeatedly contrasts SparseFW with "greedy heuristics" — a description that applies to SparseGPT. Without a direct perplexity comparison (even as a reference with appropriate caveats), claims of "outperforming strong baselines" and "drastic improvement upon state-of-the-art" are incompletely verified.  

**Required action:** Add SparseGPT perplexity results (at least for one representative model and sparsity level) in an appendix, with a clear note that SparseGPT combines mask selection with weight reconstruction while SparseFW focuses on mask quality alone. Report both the mask-only and the mask+reconstruction perplexity.

### W3 (Major) — Table 1 omits all variance/statistical significance metrics
The caption explicitly states "We omit standard deviations for legibility." Yet many improvements are within 0.1–0.3 perplexity points (e.g., DeepSeek-7 at 50%: Wanda 7.79 vs SparseFW-Wanda 7.89 — SparseFW is *worse*). Without standard deviations, confidence intervals, or multi-seed reporting, the statistical reliability of the claimed improvements cannot be assessed. Figure 3 reports min-max ranges (good), but the main results table lacks any uncertainty measure.  

**Required action:** Report mean ± std over ≥3 seeds for all entries in Table 1. Add a note in the caption: "Standard deviations are computed over 3 random calibration samples." If computational constraints prevent full multi-seed runs, at minimum add min-max ranges for a representative subset.

### W4 (Major) — Theoretical bound (Lemma 1) may be vacuous at LLM scale
The error bound contains a thresholding term $2\sqrt{2 d_{in} d_{out} k}$. For a typical 7B-layer ($d_{in}=d_{out}=4096$, $k \approx 6 \times 10^6$ at 60% sparsity), this term evaluates to $\sim 1.4 \times 10^7$. Without a concrete estimate of $\lambda_{\max}(Q)$ (which is never defined or bounded in terms of known quantities), the overall bound cannot be evaluated. At face value, the multiplicative combination $\lambda_{\max}(Q) \times 10^7$ likely produces a vacuous guarantee. The paper presents this as a "key benefit" but does not acknowledge the looseness.  

**Required action:** (a) Define $Q$ explicitly and provide an upper bound in terms of $\|W\|$, $\|X\|$, and $k$. (b) Acknowledge that the worst-case bound is loose at LLM scale. (c) Clarify whether the bound applies to global $\ell_0$ sparsity or row-wise sparsity (the experimental setup uses row-wise sparsity, while the theory assumes global $\ell_0$).

### W5 (Major) — Theory-practice gap in sparsity formulation
The theoretical analysis (Section 4, Lemma 1) assumes a global $\ell_0$ constraint ($\|M\|_0 \leq k$), while the algorithm and experiments enforce row-wise sparsity (pruning a fixed number of weights per row, following Wanda's convention). The LMO and FW updates in Algorithm 1 use the global $\ell_1$ relaxation, but the thresholding step (line 7) and evaluation use row-wise sparsity. This disconnect means the theory does not formally justify the empirical results.  

**Required action:** Either extend the theoretical analysis to the row-wise setting (where the problem decouples across rows and the LMO becomes separable) or explicitly state that the theory covers the global-sparsity variant and the experimental setup uses row-wise sparsity as a practical approximation. Discuss whether the bound improves in the row-wise setting (since each row has a smaller effective dimension $d_{in}$ rather than $d_{in} \times d_{out}$).

### W6 (Major) — No runtime/cost comparison
The paper admits SparseFW is "clearly more compute-intensive than Wanda and RIA" (requiring 2000 FW iterations per layer) but provides no wall-clock time, FLOP count, or GPU-hour comparison. For a 32-layer model with ~60 weight matrices, 2000 FW iterations per matrix is substantial. Without cost data, readers cannot evaluate the practical trade-off between the improved perplexity and the increased pruning time.  

**Required action:** Add a table comparing per-matrix and total pruning time (in seconds or GPU-hours) for SparseFW vs. Wanda vs. RIA on one representative model. Also report peak memory usage.

### W7 (Minor) — Percentage inconsistency (80% vs 70%)
The Introduction claims "reduces the per-layer pruning error by up to 80%" while the Contributions list claims "up to 70%." These should be harmonized with a clear statement of which metric (max vs. average vs. median) is reported.

### W8 (Minor) — Claim-evidence alignment in abstract
The abstract states "Our method drastically reduces the per-layer pruning error, outperforms strong baselines" without acknowledging the weight-fixing prerequisite. Since vanilla FW alone underperforms baselines, the abstract's wording is misleading.

### W9 (Minor) — Related work lacks concrete illustration
The related-work paragraph contrasts greedy methods with the proposed relaxation but does not provide a concrete example of *when* ignoring weight interactions causes failure. Adding a illustrative example (two weights with low individual salience but high joint importance) would strengthen the motivation.

### W10 (Minor) — Ablation of α is in appendix only
The key hyperparameter α (fraction of fixed weights) is ablated only in the appendix. Given that α=0.9 is the best value and α=0 yields failure, this sensitivity analysis should appear in the main paper.

---
**ASCII Diagram — Paper Structure & Evidence Map**
```text
[Problem: LLM pruning methods use greedy heuristics that ignore weight interactions]
    |
    v
[Proposed Solution: Convex relaxation + FW optimization (SparseFW)]
    |
    ├── Claim C1: FW-based convex relaxation of mask selection (method)
    │   └── Evidence: Algorithm 1, LMO efficiency argument
    │   └── Gap: The theory assumes global L0, experiments use row-wise sparsity
    |
    ├── Claim C2: Strong empirical performance (20-80% error reduction)
    │   └── Evidence: Table 1, Figures 2-3
    │   └── Gap (W3): No variance reported; many gains are <0.3 perplexity points
    │   └── Gap (W2): No comparison with SparseGPT, the strongest baseline
    |
    ├── Claim C3: Theoretical guarantees (Lemma 1 bound)
    │   └── Evidence: Bound in Section 4
    │   └── Gap (W4): Bound is O(sqrt(d_in*d_out*k)) ~ 10^7 at LLM scale — potentially vacuous
    │   └── Gap (W5): Mismatch between global L0 theory and row-wise practice
    |
    └── Critical caveat (W1): Vanilla FW (α=0) underperforms Wanda.
        Success requires 90% weight-fixing from Wanda warm-start.
        => The contribution is a hybrid, not a pure FW method.
```

---
**ASCII Diagram — Revision Strategy Roadmap**
```text
Priority 0 (Must-fix before publication):
    W1: Restructure contribution narrative to reflect hybrid nature
    W2: Add SparseGPT comparison (at least in appendix)
    W3: Add variance metrics to Table 1
    W4: Acknowledge bound looseness; define Q explicitly

Priority 1 (Should-fix):
    W5: Align theory with row-wise sparsity or clarify the gap
    W6: Add runtime/cost comparison
    Harmonize 70%/80% inconsistency

Priority 2 (Nice-to-have):
    W7-W10: Concrete related-work illustration, α ablation in main paper, etc.
    
Expected impact after fixes:
    [W1+W2] -> Honest positioning + stronger empirical validation
    [W3+W6] -> Verifiable, reproducible empirical claims
    [W4+W5] -> Honest theoretical contribution assessment
```

## Score
**Final Score: 6/10**

**Rationale:** The paper presents a technically sound reformulation (convex relaxation + FW) for LLM pruning and demonstrates consistent improvements at high sparsity regimes. However, the score is capped by three major issues: (1) The core contribution is substantially weakened by the finding that vanilla FW alone underperforms baselines — the method's success depends on fixing 90% of weights via Wanda's saliency prior, making it a hybrid refinement rather than an independent approach. (2) The theoretical guarantee (Lemma 1) has limited practical value at LLM scale due to $O(\sqrt{d_{in}d_{out}k})$ terms that dominate the bound, and the theory-practice gap (global $\ell_0$ vs. row-wise sparsity) is not addressed. (3) The empirical evaluation omits variance metrics and excludes comparison with SparseGPT, the most relevant strong baseline. The paper's strengths — clear exposition, honest limitation disclosure, consistent high-sparsity gains, and multi-architecture validation — prevent a lower score, but the identified weaknesses limit the contribution's impact and verifiability.

**Scoring breakdown (novelty + research value as primary dimensions):**
- Research value: 6/10 (useful hybrid method with modest but consistent improvements)
- Novelty: 5/10 (FW for pruning mask is novel, but heavy reliance on Wanda prior reduces novelty)
- Validity/soundness: 6/10 (theory is incomplete; empirics lack variance)
- Reproducibility: 6/10 (algorithm description is clear; missing runtime/cost data)
- Presentation: 7/10 (well-written, clear derivations, honest limitations)
- Overall: 6/10

**External literature verification deferred:** Novelty conclusions relative to the broad pruning literature cannot be fully assessed without retrieval capabilities. The score reflects manuscript-grounded evaluation only; external verification may adjust the novelty assessment.