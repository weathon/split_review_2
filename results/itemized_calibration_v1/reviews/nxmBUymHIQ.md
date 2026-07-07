Excellent — I now have strong calibration anchors. Let me compile the final review.

## Summary

This paper proposes LoLoRA, a hybrid method that combines local (forward-pass, gradient-free) Hebbian PCA (HPCA) updates to the LoRA A matrix with end-to-end gradient updates to the B matrix. It aims to reduce activation memory beyond LoRA-FA while avoiding the performance degradation of freezing A. The paper also provides a theoretical analysis (Theorem 4.4) characterizing the optimal set of A matrices as nonsingular linear transformations of the top-\(r\) eigenvectors of the input covariance matrix.

## Strengths

- **Theorem 4.4 is a genuine theoretical contribution.** The paper formally characterizes the set of optimal A matrices (under random regression assumptions) as nonsingular linear transformations of the top-\(r\) eigenvectors of the input covariance matrix. This generalizes the EVA heuristic (Paischer et al., 2024) and provides a clean theoretical justification for why PCA-based A initialization is principled. The proof of asymmetry between A and B (Theorems 4.4 vs. 4.5) is also a nice finding.

- **Diverse experimental evaluation.** The paper tests across NLU (GLUE/RoBERTa-large), math reasoning (LLaMA-3.1-8B/MetaMathQA), and multimodal (LLaVA-v1.5-7B) settings, providing reasonable breadth for a PEFT paper.

- **Well-executed ablation study (Tables 5 and 6).** The paper compares multiple initialization methods (Uniform, Orthogonal, PiSSA, EVA) and multiple local update rules (HPCA variants, AE, SoftHebb), giving a clear picture of what works and what does not.

## Weaknesses

### Major

**1. The proposed method does not outperform its simpler baseline (LoRA-FA with EVA initialization) in any experiment.**

The paper's central narrative is that LoRA-FA (freezing A with random initialization) underperforms, and LoLoRA's local updates fix this. However, against the relevant baseline — LoRA-FA with **EVA initialization**, which the paper's own theory suggests should be optimal — the results tell a different story:

| Setting | LoRA-FA (EVA) | LoLoRA HPCA |
|---|---|---|
| GLUE (8 tasks, Tables 1-2) | Best in 0/8 | Best in 0/8 |
| Math reasoning (Table 3) | **0.829±0.005** | **0.829±0.004** (tie) |
| Multimodal PPL (Table 4) | **2.92±0.01** | 2.93±0.01 (worse) |
| Ablation r=8 (Table 5 vs 6) | **2.536±0.010** | 2.535±0.011 (tie) |

LoLoRA **ties or underperforms** LoRA-FA (EVA) in every single experimental setting. The conclusion claim that "HPCA consistently outperforms standard LoRA-FA in two out of three experimental setups" overstates the evidence — against uniform-initialized LoRA-FA on GLUE, LoLoRA wins on at most 1 of 8 tasks, and most differences are within one standard deviation. This undermines the core practical motivation for the method.

**2. The theoretical analysis justifies static initialization, not iterative updates — the method and theory are decoupled.**

Theorem 4.4 proves that optimal A (when A is *fixed* and B is optimized) should span the top eigenvectors of the input covariance *under stationarity*. This is a result about *initialization*, not about iterative training. But LoLoRA's claimed contribution is about *iteratively updating A during training*. The paper never demonstrates a setting where the non-stationarity of inputs during training (the one thing that would justify online updates over one-shot PCA) actually matters. The limitation is acknowledged in Section 6 ("we considered each submodule isolated with stationary targets"), but this is a fundamental disconnect: the theoretical framework justifies EVA-style initialization more directly than it justifies LoLoRA's iterative updates. If the input distribution is stationary (as the theory assumes), computing PCA once before training is strictly cheaper and achieves the same result. If it is non-stationary, the theory does not apply.

### Minor

**3. The memory advantage over LoRA-FA is essentially zero (or slightly negative).**

The paper claims memory reduction as a key benefit. On the math reasoning task (Table 3), LoRA-FA and LoLoRA both use 26 GB — identical. On the multimodal task (Table 4), LoLoRA uses **24.1 GB** while LoRA-FA uses **23.9 GB** — LoLoRA uses *more* memory. The paper acknowledges this ("our method introduces a small amount of extra optimizer state for the local updates, unlike standard LoRA-FA"), but the abstract and introduction claim "further reducing the memory required for fine-tuning" without qualification. The memory savings relative to standard LoRA (~13-20%) are the same savings that LoRA-FA already achieves; LoLoRA adds nothing on this front.

**4. On the LLaVA experiment (Table 4), the best-performing approach is standard LoRA with EVA initialization (2.89 PPL), which is better than both LoLoRA (2.93) and LoRA-FA (EVA) (2.92).** The paper does not discuss what this implies. If the best result comes from "LoRA with EVA initialization" (which stores activations for A's gradient), then the paper's motivation — that we need to save activation memory for A — is contradicted by the evidence on this task. A performance-memory tradeoff still exists, and LoLoRA does not eliminate it.

**5. On GLUE, LoRA-FA (uniform) outperforms LoRA-FA (EVA) on 6/8 tasks, which contradicts the paper's theoretical prediction that PCA-based initialization should be optimal.** The paper offers no explanation for this discrepancy.

**6. The conclusion overstates results.** The claim "HPCA consistently outperforms standard LoRA-FA in two out of three experimental setups" is misleading — on GLUE, LoLoRA does not clearly outperform, and most favorable comparisons are within error bars.

### Trivial

None.

## Nice-to-Haves

- A controlled experiment demonstrating non-stationarity (e.g., input distribution shift during training) where online HPCA updates outperform one-shot PCA would directly support the method's motivation.
- A memory-performance Pareto frontier including all variants (standard LoRA, LoRA-FA, LoLoRA, with various initializations) would give a clearer picture of tradeoffs.
- Systematic wall-clock time and total-compute comparison between one-shot PCA (EVA) and per-step HPCA.
- Investigation of why EVA initialization underperforms uniform on GLUE.

## Removed Points

These points were flagged by the harsh critic but are removed with justification:

- **"Paper does not discuss that u = Az must be stored for B's backward pass"** — Factual error. Algorithm 1 line 6 explicitly states "keep u for B." The paper correctly identifies the memory mechanism.
- **"Missing related works / missing appendix / missing proofs"** — The parser strips appendices; they exist in the original.
- **"Statistical significance should be more careful"** — Generic criticism without concrete anchor.
- **"Missing comparison with updating A via backpropagation on Pareto frontier"** — Moved to Nice-to-Haves; not a required baseline.
- **Missing baseline claims about fairness** — Several criticisms about baselines being unfair were determined upon verification to be misread or insufficiently grounded.

## Novel Insights

The most incisive observation from the reviews is that the theoretical contribution (Theorem 4.4) and the method's iterative updates serve different goals. The theorem justifies a static initialization strategy (one-shot PCA → EVA), while the iterative HPCA updates address a non-stationarity problem the paper never demonstrates exists. This fundamental disconnect means the paper's two main contributions — theory and method — are orthogonal: the theory supports a simpler approach than the one proposed, and the method's claimed advantages are over a baseline (LoRA-FA with random init) that the theory itself suggests is not the right comparator. The paper would be substantively stronger if honestly reframed as (a) a theoretical justification for PCA-based A initialization, plus (b) a demonstration that online HPCA can approximately reach the same subspace without pre-processing, with the caveat that for stationary distributions the simpler EVA suffices.

## Suggestions

- Reframe the paper's contribution honestly: Theorem 4.4 is a genuine theoretical contribution that justifies EVA-style initialization. Present LoLoRA's iterative HPCA updates as an *alternative* that avoids pre-processing (at some per-step cost) rather than a method that improves performance over frozen-A baselines.
- Either demonstrate a non-stationary setting where online adaptation matters, or explicitly acknowledge that the theory supports static initialization and the method is primarily about computational convenience (no pre-processing pass).
- Tone down or remove the claims about "further reducing memory" and "outperforming LoRA-FA" that are not supported by the data.

## Score and Decision

**Initial bracket:** After examining calibration anchors, the paper sits between ALLoRA (3.33, similar LoRA variant with theory claims but weak empirical support) and the EVA paper itself (4.75, similar topic with minimal improvements but no theory). The paper has a stronger theoretical contribution than both but a weaker empirical case for the method than EVA.

**Calibration comparison:**

| Anchor | Score | Comparison |
|--------|-------|------------|
| ALLoRA (7X65yoKl3Y) | 3.33 | Similar: LoRA variant with theory-empirical gap. This paper has better theory and broader experiments. |
| SiVA (VpeAsLmcvg) | 3.75 | Similar: theory-method disconnect. This paper's theory is stronger and cleaner. |
| EVA (DM6Q45HWSk) | 4.75 | Directly relevant: same initialization topic. This paper has stronger theory (Theorem 4.4), but the method's practical claims are less supported. |
| GLoRA (NXnNiT0fdp) | 4.75 | Had missing algorithm description, limited scope, but claimed improvements. This paper is more complete but method doesn't outperform baselines. |
| RoCoFT (EQZMx8Lc0n) | 5.00 | Method actually works empirically. This paper's method doesn't. |
| VeRA (NjNfLdxr3A) | 7.25 | Strong empirical results, simple method that works. Much stronger empirical case. |

**Narrowing:** The paper is stronger than ALLoRA (3.33) due to genuine theory and broader experiments, but weaker than EVA (4.75) because EVA at least demonstrates a practical benefit (rank redistribution) while LoLoRA's iterative updates deliver no improvement over the simpler EVA initialization. The central practical claim is not supported. Score: **4.0**.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>