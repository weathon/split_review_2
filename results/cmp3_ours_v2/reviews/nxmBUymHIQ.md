Now I have all the information I need for calibration. Let me compile my final review.

**Round 1 Bracket**: Based on the calibration anchors, this paper sits between 3.5 and 5.0. The closest comparisons are:
- EVA paper (4.75, reject) — similar topic, both provide data-driven initialization; LoLoRA has stronger theory but weaker empirical results
- "Singular Value Adaptation" (3.75, reject) — similar theoretical ambitions with mixed empirical support
- LoRA-FA (5.33, reject) — the core baseline this paper builds on; LoLoRA adds complexity without clear benefit

The theory is genuinely stronger than EVA, but the method's failure to outperform LoRA-FA (EVA) is a critical weakness. The paper sits below LoRA-FA (which at least demonstrated a clear memory-accuracy trade-off) and near EVA in quality.

**Final Score: 4.0** — The paper has genuine theoretical contributions (Theorem 4.4) and a novel methodological direction, but the core empirical claim is unsupported: LoLoRA does not demonstrate a clear advantage over the simpler LoRA-FA (EVA) baseline it aims to improve upon.

Here is the final consolidated review:

## Summary

LoLoRA proposes to use local learning rules (HPCA/SNL, autoencoder loss) to update LoRA's A matrix during the forward pass, avoiding backpropagation through A and its associated activation storage. The paper provides a theoretical analysis (Theorem 4.4) showing that optimal A spans the top r eigenvectors of the input covariance matrix under a random regression model, and evaluates LoLoRA on GLUE (RoBERTa-large), MetaMathQA (LLaMA-3.1-8B), and LLaVA-v1.5-7B.

## Strengths

1. **Clean theoretical result (Theorem 4.4).** The paper derives the exact set of optimal A matrices under a random-regression model, showing they correspond to nonsingular linear transformations of the top r eigenvectors of the input covariance matrix. Assumptions are stated clearly, and the result provides a mathematical justification that was previously missing from the empirical EVA initialization work. This is the paper's strongest contribution.

2. **Genuinely novel direction for LoRA fine-tuning.** Using local learning rules (HPCA/SNL, autoencoder loss) to update the A matrix during the forward pass — avoiding activation storage for backprop — is a direction that has been underexplored in LLM fine-tuning. The paper bridges local learning and end-to-end backprop in one method.

3. **Multi-domain evaluation with proper statistical reporting.** Experiments span NLU (GLUE with 8 tasks), mathematical reasoning (MetaMathQA), and multimodal fine-tuning (LLaVA), with multiple random seeds and standard deviations. The ablation study (Tables 5, 6) comparing different initializations and local rules is informative and well-structured.

4. **The autoencoder formulation (Theorem 4.6) provides theoretical grounding** for why the local AE loss converges to the same optimal subspace as HPCA, connecting the local update literature to the LoRA setting.

## Weaknesses

### Fatal
None.

### Major

1. **LoLoRA does not demonstrate a clear advantage over LoRA-FA (EVA) — the simpler baseline it aims to improve upon.** Across all experiments, LoLoRA is either statistically tied with or worse than LoRA-FA (EVA), while adding implementation complexity (local update rules, extra optimizer state, per-layer forward-pass computations) and, in one setting, using *more* memory (24.1 GB vs 23.9 GB on LLaVA, Table 4):

   - **GLUE (Tables 1-2):** LoLoRA HPCA is never the best method on any of the 8 tasks. It is worse than LoRA-FA (uniform) on CoLA (66.3 vs 67.9), RTE (84.6 vs 86.4), MNLI (90.3 vs 90.6), and QQP (90.6 vs 90.8), and ties within error bars on the remaining four tasks.
   - **MetaMathQA (Table 3):** LoLoRA (0.829 ± 0.004) ties with LoRA-FA (EVA) (0.829 ± 0.005) and is within error bars of LoRA-FA (uniform) (0.826 ± 0.005).
   - **LLaVA (Table 4):** LoLoRA HPCA (loss 1.075) sits between LoRA-FA (EVA) (1.070) and LoRA-FA (uniform) (1.087), within standard deviation.
   - **Ablation (Table 6 vs Table 5):** Best LoLoRA variant (HPCA, 2.535 at r=8) is essentially identical to LoRA-FA with EVA initialization (2.536 at r=8). The gap to standard LoRA (2.521 at r=8) is not discussed.

   The conclusion claims "HPCA consistently outperforms standard LoRA-FA in two out of three experimental setups" — but this refers only to LoRA-FA with *uniform* initialization, not the stronger EVA variant. For a method that adds complexity and optimizer state, the burden of proof for a clear accuracy or memory advantage over LoRA-FA (EVA) is not met.

2. **The theory justifies one-shot PCA initialization, not online HPCA updates — and the ablation undermines the motivation for online updates.** Theorem 4.4 characterizes optimal A under the assumption that A is frozen and B is optimally chosen, with stationary inputs. This directly justifies EVA-style *one-shot* PCA initialization. The paper's claimed novelty is that it *updates* A during training to "adapt to input distribution shifts" (Section 3.2). However:
   - No theoretical analysis is provided for why online updates would outperform a good initialization under distribution shift.
   - No empirical evidence shows that input distributions actually shift during fine-tuning in a way HPCA tracks and exploits.
   - The ablation (Table 6) shows HPCA (svd first) — initializing via PCA then applying HPCA updates — achieves the same perplexity as HPCA (uniform) at r=2 (2.557 vs 2.557) and r=8 (2.535 vs 2.535). This directly suggests the online HPCA updates after initialization do little useful work, undermining the paper's central motivation.

3. **Rank not specified for the main experiments.** The paper does not state the rank (r) used for the GLUE, MetaMathQA, and LLaVA experiments in the main text. Only the ablation section explicitly specifies r=2,4,8. Since rank directly determines memory savings and comparison fairness, this is a significant reproducibility gap.

### Minor

4. **Memory reporting is incomplete.** The paper claims "up to 20% less GPU memory" (GLUE summary) but concrete reported numbers show ~13% for MetaMathQA (30→26 GB) and ~2% for LLaVA. The 20% figure is deferred to Appendix D. No breakdown of activation memory vs optimizer states vs adapter weights is provided, making it hard to assess where savings occur. LoLoRA also uses more memory than LoRA-FA on LLaVA (24.1 vs 23.9 GB), which the paper acknowledges in the conclusion but does not prominently discuss.

5. **Non-standard evaluation protocol for MetaMathQA.** The paper reports the best result over checkpoints taken every 0.2 epochs (Section 5.2: "the best result is reported for each method"). This can favor methods with higher variance or different convergence speeds. Reporting the final-checkpoint result alongside the best-checkpoint result would improve interpretability.

6. **The random regression assumption limits the theory's practical scope.** Assumption 4.1 (ΔW₀ entries i.i.d. Gaussian) removes all task-specific structure, making the theory essentially say "when you know nothing about the target, preserve maximal input variance." While the assumptions are stated clearly and the result is clean, this limits the theory's ability to guide the paper's actual method (updating A with task-specific gradients flowing through B during fine-tuning).

### Trivial

7. The conclusion states LoLoRA "consistently outperforms standard LoRA-FA in two out of three experimental setups," but this overstates the evidence given error-bar overlap and the fact that it refers only to LoRA-FA with uniform initialization.

## Nice-to-Haves

- Include a memory breakdown (activation memory vs optimizer states vs adapter weights).
- Report the final-checkpoint result alongside the best-checkpoint result for MetaMathQA.
- Demonstrate a setting (e.g., multi-epoch training, domain shift) where HPCA online updates clearly outperform one-shot EVA initialization.
- Discuss QLoRA or other quantization-based approaches as an orthogonal direction for memory reduction.

## Removed Points
- **"Missing QLoRA baseline":** QLoRA is quantization-based — an orthogonal approach to activation memory reduction within the LoRA framework. Criticizing its absence is scope creep. *Removed as scope creep.*
- **"20% memory claim is misleading":** The 20% figure is deferred to Appendix D which is stripped by the parser and unavailable for verification. The concrete numbers in the main text (13%, ~2%) are honestly reported. *Removed as unverifiable given missing appendix.*
- **"Theory and method pointing in different directions" (overstated framing):** The theory identifies the optimal subspace; HPCA converges to it. They are consistent. What's actually problematic is that online updates don't show advantage over one-shot initialization — this is properly captured in Weakness #2. *Merged into Weakness #2 with corrected framing.*
- **"Strong assumptions limit practical relevance":** Every theoretical model makes simplifying assumptions; the paper states them clearly. The Gaussian-on-ΔW₀ assumption is standard for expectation-based arguments. *Removed as a generic criticism applicable to all theoretical models, not specific to this paper's failings.*
- **Section-by-section presentation nitpicks** (e.g., "Figure 1 caption is underspecified"): These are formatting-level observations that don't affect the core evaluation. *Removed as formatting-level noise.*
- **"Theorem 4.5 at odds with practical experience about B initialization":** The theorem refers to the *expected* loss under random ΔW₀ with *optimal* A, not about training dynamics. The paper's framing of the result is correct. *Removed as factually incorrect criticism.*

## Novel Insights
The reviewer's key insight — which goes beyond what the paper itself acknowledges — is that the ablation in Table 6 (HPCA (svd first) achieving the same perplexity as HPCA (uniform) at all ranks) provides direct evidence that the online HPCA updates do not improve over a good one-shot initialization. This single finding from the paper's own data undermines its core motivation for online local updates more effectively than any external critique could. Coupled with the fact that LoLoRA never outperforms LoRA-FA (EVA) across any of the three experimental setups, the paper's primary empirical claim is unsupported by its own evidence.

## Suggestions

1. Clearly specify the rank used in all main experiments (r for GLUE, MetaMathQA, LLaVA).
2. Add a multi-epoch experiment or a domain-shift scenario to demonstrate when online HPCA updates provide benefit over one-shot EVA initialization.
3. Provide a memory breakdown showing where the ~13% savings come from.
4. Report final-checkpoint accuracy alongside best-checkpoint accuracy for MetaMathQA.
5. Tone down the narrative from "LoLoRA improves upon LoRA-FA" to "LoLoRA offers a principled alternative that avoids separate PCA pre-processing, with comparable performance."

## Score and Decision

**Round 1 bracket**: 3.5–5.0. Anchors used in calibration:

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| EVA (DM6Q45HWSk) | 4.75 (reject) | 1 | Both papers address LoRA initialization; LoLoRA has stronger theory but weaker empirical results |
| Singular Value Adaptation (VpeAsLmcvg) | 3.75 (reject) | 2 | Similar theoretical ambitions with mixed empirical support |
| RAC-LoRA (VSKV3GykuE) | 5.00 (reject) | 2 | Theoretical optimization framework; stronger empirical validation |
| LoRA-FA (RbKThNNFxr) | 5.33 (reject) | 1 | Core baseline; demonstrated clear memory-accuracy trade-off |
| ALLoRA (7X65yoKl3Y) | 3.33 (reject) | 1 | LoRA variant with marginal improvements and missing baselines |
| Activations Aren't Cheap (3ylNuZXtMg) | 4.25 (reject) | 2 | Related work on LoRA activation memory; similar scope |
| Local Control Networks (wYVP4g8Low) | 3.00 (reject) | 2 | Local learning in different context |

The paper has genuine theoretical contributions (stronger than EVA's empirical-only approach) and a novel methodological direction. However, the core method does not demonstrate a clear advantage over the simpler LoRA-FA (EVA) baseline, and the ablation data (Table 6) indicates the online updates contribute little beyond a good initialization. This places it below the LoRA-FA paper (which cleanly demonstrated its method's trade-off) and near the EVA paper's quality level — a meaningful contribution undermined by insufficient empirical support.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>