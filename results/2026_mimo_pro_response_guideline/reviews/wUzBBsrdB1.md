Now I have enough calibration data. Let me finalize the review.

**Calibration Analysis:**

Anchors retrieved across all rounds:

| Paper | Avg Score | Decision | Round | Comparison |
|-------|-----------|----------|-------|------------|
| "Scaling and evaluating SAEs" (tcsZt9ZNKD) | 1.75 | Accept | R1 | Not comparable (anomalous score) |
| "Automatically Identifying Sparse Circuits" (89wVrywsIy) | 3.40 | Reject | R1 | Our paper has much cleaner evidence and stronger insight |
| "SAEs Find Highly Interpretable Features" (F76bwRSLeK) | 4.80 | Accept | R1 | Foundational SAE paper; our paper extends this by showing L0 matters |
| "Compute Optimal Inference in SAEs" (ghH6YYDs15) | 4.67 | Reject | R1 | Our paper has cleaner evidence and more actionable findings |
| "Applying SAEs to Unlearn Knowledge" (ZtvRqm6oBu) | 5.25 | Reject | R1 | Our paper has more fundamental contribution |
| "Incidental Polysemanticity" (OeHSkJ58TG) | 5.67 | Reject | R2 | Less impactful than our sparsity-reconstruction tradeoff critique |
| "Everything Everywhere All at Once" (FxLxbJTm7F) | 5.75 | Reject | R2 | Different area, less comparable |
| "Residual Stream Analysis with Multi-Layer SAEs" (XAjfjizaKs) | 6.50 | Accept | R1/R2/R3 | Our insight (L0 matters, tradeoff critique) is more fundamental |
| "Mechanistic Permutability" (MDvecs7EvO) | 6.50 | Accept | R2/R3 | Our contribution is more impactful for the field |
| "Towards Principled Evaluations of SAEs" (1Njl73JKjB) | 7.00 | Accept | R1/R2 | Very comparable scope; both critique SAE evaluation; our toy model evidence is cleaner |
| "SAEs Do Not Find Canonical Units" (9ca9eHNrdH) | 7.00 | Accept | R1/R2/R3 | Both challenge fundamental SAE assumptions; comparable contribution |
| "Not All Features Are Linear" (d63a4AM4hb) | 7.00 | Accept | R2 | Different but comparable novelty level |
| "A is for Absorption" (LC2KxRwC3n) | 7.50 | Reject | R3 | Closely related (feature absorption); rejected at 7.50 |
| "Sparse Feature Circuits" (I4e82CIDxv) | 8.00 | Accept | R1 | Higher contribution; our paper is more focused |

**Initial bracket:** 6.5–7.0. The paper is clearly better than the 4.5–5.5 reject papers and comparable to the 6.5–7.0 accept papers. The sparsity-reconstruction tradeoff critique is more fundamental than the contributions in the 6.5 papers, but the c_dec metric limitations and limited LLM validation hold it back from 7.5+.

**Final score:** 6.5. The paper makes a genuinely important contribution (sparsity-reconstruction tradeoff critique, clean toy model evidence that L0 is not a free parameter), but the practical contribution (c_dec metric) is imprecise on real LLMs, and the LLM validation relies on a single proxy (sparse probing) across only 2 small models. The core insight is strong enough for acceptance, but the practical tooling needs more development.

---

## Summary
This paper demonstrates that the L0 hyperparameter in sparse autoencoders (SAEs) is not a free parameter governing a sparsity-reconstruction tradeoff, but must be set correctly to recover disentangled features. Using toy models with ground-truth features, the authors show that too-low L0 causes SAEs to mix correlated features to improve reconstruction, while too-high L0 produces degenerate solutions. They demonstrate that the standard sparsity-reconstruction tradeoff plot is misleading—an incorrect SAE with polysemantic latents can outperform a ground-truth SAE on reconstruction—and propose a decoder pairwise cosine similarity metric (c_dec) to diagnose incorrect L0, validating it on Gemma-2-2b and Llama-3.2-1b.

## Strengths
- **The sparsity-reconstruction tradeoff critique challenges standard SAE evaluation practice**: Figure 4 (Section 3.4) shows that a ground-truth SAE with correct features achieves worse reconstruction than a trained SAE with polysemantic latents when L0 is below the true value. At L0=5, the trained SAE achieves MSE of 2.73 vs 4.88 for the ground-truth SAE (Section 3.3). This directly demonstrates that "sparsity-reconstruction tradeoff" plots—the dominant evaluation method for comparing SAE architectures (Gao et al., 2024; Rajamanoharan et al., 2024)—can actively mislead practitioners into selecting broken SAEs. This insight is arguably more impactful than the c_dec metric itself.

- **Clean causal evidence from controlled toy models with ground-truth features**: The experimental design is well-constructed: initializing an SAE to the ground-truth solution at L0=1.8 (below the true L0=2) and showing it *moves away* from correct features during training (Section 3.1) isolates the effect of gradient pressure from poor initialization. The positive/negative correlation inversion experiments (Figures 2–3) provide intuitive demonstration of the mechanism. The scaling to 50 features (Section 3.2) with random correlation matrix confirms the pattern generalizes.

- **Results validated across both major SAE architectures**: Section 3.6 and Figure 7 show the c_dec metric works for JumpReLU SAEs. The observation that JumpReLU's λ_s "sticks" near the correct L0 across a wide range of sparsity coefficients (Figure 7, left) is practically valuable—suggesting JumpReLU's per-latent threshold provides partial self-correction against incorrect L0 selection.

- **Practical c_dec metric grounded in clear intuition**: Equation 4 defines a simple, computable diagnostic based on decoder pairwise cosine similarity. The intuition is clean: latents should be more orthogonal when L0 is correct (fewer shared correlated features mixed in). The metric correctly identifies the true L0 in toy models (Figure 6) and the "elbow" region corresponds to peak sparse probing in LLMs (Figure 8).

## Weaknesses

### Fatal
None

### Major
- **c_dec metric behavior on real LLMs is inconsistent and imprecise, limiting practical utility**: For Gemma-2-2b layer 5 (Figure 8, top-left), c_dec drops sharply at low L0 then becomes essentially flat over a wide range (~250–2000), with the global minimum appearing deep in that flat region. For Llama-3.2-1b (Figure 8, top-right), there is a clear minimum. For Gemma layer 12 (Figure 9), the behavior is yet again different. The authors acknowledge this: "the metric can sometime remain nearly flat for a wide range of L0" (line 246). This means c_dec can reliably warn against clearly-too-low L0 but cannot pinpoint the correct value, and practitioners must resort to visual "elbow" identification rather than an algorithmic criterion.

- **LLM validation relies solely on k-sparse probing as a proxy for feature quality**: The paper's core thesis is that features are "wrong" at incorrect L0 (not merely less useful), but validation on real LLMs uses only k-sparse probing F1 scores (Section 4). Sparse probing measures supervised binary classification utility—a reasonable but imperfect proxy for monosemanticity. No interpretability evaluations (automated or human), causal intervention scores, or feature visualization assessments are reported. The evidence chain from "c_dec identifies correct L0" to "features are actually monosemantic" has a gap on real LLMs.

### Minor
- **Toy model features are exactly orthogonal; sensitivity to this assumption unexamined**: The toy models enforce f_i · f_j = 0 for i ≠ j (line 65). Real LLM features are approximately but not exactly orthogonal, and the degree of non-orthogonality could affect the dynamics. The paper does not examine what happens when features have small but non-zero overlap or hierarchical relationships. (Appendix A.6 is mentioned for theoretical justification but the main paper leaves this unaddressed.)

- **Limited model and layer coverage in LLM experiments**: Testing only Gemma-2-2b (layers 5, 12) and Llama-3.2-1b (layer 7) limits generalizability of claims like "most commonly used SAEs have too low an L0" (abstract). Appendix A.13 references Neuronpedia SAEs but this is supplementary rather than systematic validation.

- **Asymmetric treatment of too-low vs too-high L0**: The abstract promises balanced coverage ("If L0 is too low... If L0 is too high..."), but the paper is overwhelmingly focused on the too-low case. Too-high L0 is discussed in Sections 3.2 and 4.2 but receives less rigorous analysis. Section 4.2's observation about simultaneous per-latent too-high/low regimes is insightful but explicitly speculative ("we suspect"—line 226).

## Nice-to-Haves
- Automating c_dec elbow detection (e.g., finding the L0 where c_dec first drops below 110% of its running minimum over a sliding window) would make the metric actionable for practitioners and remove subjectivity.
- Sensitivity analysis of feature non-orthogonality in toy models would strengthen the generalizability claim to real LLMs.
- Connecting c_dec-identified L0 to actual feature interpretability (even for a handful of features using top-activating examples or automated interpretability methods) would directly test the "features are wrong" claim on real LLMs.
- Discussing whether alternative reconstruction metrics (beyond MSE) might avoid the sparsity-reconstruction tradeoff problem.

## Removed Points
These points are flagged to be removed, treat them with caution:
- The harsh critic's concern about "only two small models" is noted but weakened: the paper's core contribution is the toy model analysis and fundamental insight about L0, not comprehensive LLM benchmarking. LLM experiments serve as supplementary validation.
- The harsh critic's suggestion to "confirm convergence" in Section 3.1 is a minor nitpick—the paper explicitly states the SAE was initialized to ground truth and shows it moved away, which is the experimental point.
- Concerns about scaling from 50-feature toy models to 32K-latent real SAEs are a scope critique applicable to any toy model paper.

## Novel Insights
The paper's most novel insight is that the sparsity-reconstruction tradeoff plot—the dominant evaluation method for comparing SAE architectures—can actively mislead practitioners into selecting broken SAEs. If an SAE training method produced perfect features, standard evaluation methodology would cause us to reject it in favor of an incorrect, feature-mixing SAE. This challenges fundamental assumptions about how the field evaluates SAEs and is more impactful than the c_dec metric itself. A secondary insight is that JumpReLU's per-latent threshold provides partial self-correction against incorrect L0 selection, explaining its empirical advantages over fixed-K methods.

## Suggestions
- Add automated c_dec elbow detection to make the metric practically usable
- Validate feature quality on real LLMs using interpretability methods (e.g., top-activating examples, automated interpretability scores) for a small number of features
- Include a brief sensitivity analysis of how results change with feature non-orthogonality in the toy model
- Extend the sparsity-reconstruction tradeoff discussion by considering alternative reconstruction metrics

## Reporting

**Round 1 bracket: 6.5–7.0.** The paper is clearly stronger than the 4.5–5.5 reject papers (which have weaker evidence or less impactful insights) and comparable to the 6.5–7.0 accept papers ("Towards Principled Evaluations" at 7.00, "SAEs Do Not Find Canonical Units" at 7.00, "Residual Stream Analysis" at 6.50). The sparsity-reconstruction tradeoff critique is more fundamental than the contributions in the 6.5 papers, but the c_dec metric imprecision and limited LLM validation hold it back from 7.5+. "A is for Absorption" at 7.50 (rejected) is closely related work that our paper explicitly extends—though the reasons for that rejection are unclear from the anchors alone.

**Round 2 narrowing:** Confirmed 6.5–7.0. Comparing to "Towards Principled Evaluations" (7.00, accepted): both critique SAE evaluation methodology, our paper has cleaner toy model evidence but weaker LLM validation. Comparing to "Residual Stream Analysis" (6.50, accepted): our insight is more fundamental and directly actionable.

**Final score: 6.5.** The paper's core contribution—the sparsity-reconstruction tradeoff critique and clean demonstration that L0 is not a free parameter—is strong and practically important. The c_dec metric is useful but imprecise on real LLMs, and the LLM validation relies on a single proxy. This places the paper at the boundary of accept: strong enough in its core insight to warrant acceptance, but with practical contributions that need further development.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>