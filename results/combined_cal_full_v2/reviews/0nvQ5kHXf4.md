## Summary

This paper proposes Weight-Activation Subspace Iteration (WASI), a method for memory-efficient on-device fine-tuning of transformer models. The core idea is to jointly decompose both weight matrices and activation maps into low-rank subspaces using warm-started subspace iteration, reducing memory and computational costs during training and inference. Experiments on ViT, SwinT, and TinyLlama across multiple datasets show up to 62× memory reduction and 1.4× speedup on a Raspberry Pi 5 while maintaining accuracy comparable to vanilla training.

## Strengths

- **Well-motivated problem and clear methodological extension (Section 3.1).** The paper addresses a genuine need — enabling on-device fine-tuning of transformer models — and the motivation for why joint weight-activation compression matters (both are stored during backpropagation) is clearly laid out. The extension of subspace iteration from activations (ASI) to weights is a natural and sensible progression. **[weight: 9.69]**

- **Empirical support for the rank-stability assumption (Fig. 3a).** The paper provides direct evidence that the singular values of weight matrices remain stable across fine-tuning epochs, which underpins the core premise that a precomputed subspace can be reused via iteration rather than recomputed via costly SVD each step. **[weight: 9.34]**

- **Real-world deployment validation (Fig. 8).** The Raspberry Pi 5 timing experiments give concrete evidence that the method translates to actual speedups (~1.4×) on resource-constrained hardware, bridging the gap between simulated FLOPs counts and practical benefit. **[weight: 8.92]**

- **Substantial resource reductions demonstrated across multiple architectures.** The method achieves up to 62× memory savings and 1.5× FLOPs reduction at ε=0.9 while matching vanilla accuracy on SwinT, and 953.86× activation memory reduction on TinyLlama, making a strong case for the approach's practical impact. **[weight: 9.26]**

## Weaknesses

### Fatal
None.

### Major
- **No ablation study separates the contribution of weight compression (WSI) from activation compression (ASI) (Sections 3.3, 4.3).** Since ASI-predecessor work already exists, the novel component is WSI and its interaction with ASI. The paper compares against ASI as a baseline, but ASI uses a different rank-selection criterion (perplexity-based rather than ε-based), so it does not serve as a controlled ablation. Without a WSI-only condition and an ASI-only condition matched on the same compression criterion, the reader cannot determine whether the observed gains come from the weight decomposition, the activation decomposition, or their combination. This is the most consequential gap in the evaluation. **[weight: 2.04]**

### Minor
- **Exact accuracy numbers are not reported in tabular form.** The paper reports resource consumption (memory, FLOPs, time) in figures but almost never states the actual accuracy values numerically, making it difficult for readers to precisely evaluate the accuracy-efficiency trade-offs at each compression level. A single table with accuracy, memory, and FLOPs at each ε would resolve this. **[weight: 4.37]**

- **The overhead of the initial full SVD is not discussed or accounted for (Algorithm 1).** The method computes a full SVD at iteration 0 to establish the subspace, then uses cheaper subspace iteration thereafter. The cost of this initial SVD is significant and relevant for on-device scenarios, but it is neither reported nor factored into the efficiency comparisons. **[weight: 5.59]**

- **The reported '35% higher accuracy' for WSI over full SVD at iso-FLOPs (Section 4.2, Fig. 3b) is ambiguous.** It is unclear whether this is a relative or absolute improvement. The comparison mechanism (aligning different ε values to match FLOPs) is not explained in enough detail for the reader to assess the claim. **[weight: 7.25]**

- **The complexity analysis assumes the same optimal rank for weights and activations without validation (Section 3.4).** The paper acknowledges this as a simplification but never validates it. Weights and activations have different dimensional structure and information content, so their optimal ranks may differ, which would affect the quantitative predictions in Fig. 2. **[weight: 5.82]**

- **The rank stability evidence (Fig. 3a) shows only one layer (W6) of one model (ViT) on one dataset (Pets).** This is limited evidence for the general claim that "the intrinsic subspace remains relatively stable after each training iteration." Showing stability for multiple layers and model variants would strengthen this central premise. **[weight: 1.18]**

### Trivial
None.

## Nice-to-Haves
- Include LoRA as a direct baseline (with adapters merged/unmerged for inference comparison) to more clearly contextualize WASI's advantages relative to the dominant practical alternative for efficient fine-tuning. The paper currently compares against SVD-LLM (which incorporates LoRA adapters), partially mitigating this, but a standalone LoRA comparison would strengthen the evaluation.
- Show rank stability for additional layers and models beyond ViT layer W6 to generalize the claim.

## Removed Points
(These were raised in the input review but are removed after cross-checking against the paper. They are flagged for caution if needed.)

- "35% accuracy advantage not credible": The comparison is WSI vs full SVD at iso-FLOPs, which is valid — WSI uses cheaper subspace iteration, so at the same FLOPs budget it can use a higher ε (less compression). Not a fatal flaw; demoted to minor clarity issue above.
- "Missing LoRA as baseline": The paper discusses LoRA in related work and compares against SVD-LLM which uses LoRA adapters. LoRA does not address activation compression or inference cost reduction, so its absence does not invalidate the evaluation. Moved to Nice-to-Haves.
- "TinyLlama experiment doesn't support conclusions": The experiment compares WASI vs vanilla training under the same constrained setup (fine-tuning last 5 layers), which is a properly controlled comparison. The "without accuracy loss" claim is relative to vanilla under identical constraints. Removed as based on a misunderstanding of the control condition.
- "First method claim overreach": The specific framing "model-activation-decomposition-aware training" is narrow enough that the claim is defensible.
- "LoRA inference cost characterization": The paper accurately states that merged LoRA has the same cost as the original model. This is a neutral description.
- "Equation 9 f_LR not defined in main text": Standard practice; paper references Appendix A.1.
- "Singular value color bar -1 to 4": Parser artifact from image description extraction, not from the paper's actual figure.
- Various formatting/style nitpicks and missing appendix references: Removed per hard rules.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add a controlled ablation experiment** (WSI-only, ASI-only, WASI) using the same ε-based compression criterion on CIFAR-10 with ViT to quantify each component's contribution. This is the single most important addition to validate the paper's core claim.
2. **Include a table** with exact accuracy values at each ε level alongside memory and FLOPs numbers for the main experiments.
3. **Clarify the 35% claim**: explicitly state whether the improvement is relative or absolute and describe the iso-FLOPs alignment procedure in detail.
4. **Account for the initial SVD overhead** in the efficiency analysis, or at minimum acknowledge it as a one-time cost and discuss its amortization over training.
5. **Validate or discuss the equal-rank assumption** for weights and activations with empirical evidence.

## Score and Decision

### Calibration Anchors

| Anchor Paper | Path | Avg Score | Round | Itemized | Comparison to WASI |
|---|---|---|---|---|---|
| On-Device TL via Mixed Precision Partitioning | eqKHuxIpp5.md | 2.50 | 1 | Yes | Weaker method, much less experimental scope, negative-weight weaknesses |
| SubTrack your Grad | nR0n4R1Ck2.md | 4.75 | 1 | Yes | Similar domain (subspace tracking), but has negative-weight weaknesses (missing validation at -2.81); WASI has stronger strengths and milder weaknesses |
| SubZero | FK6T0U4Mg1.md | 4.25 | 1 | No | Zeroth-order subspace method, similar score band |
| Activations Aren't Cheap in LoRA | 3ylNuZXtMg.md | 4.25 | 2 | Yes | Similar focus on activation memory; has novelty concerns and negative-weight weaknesses |
| Memory-Efficient via Structured Pruning | JMgxtZqkvO.md | 4.50 | 2 | Yes | PEFT via pruning; has negative-weight weaknesses (-3.89 novelty, -3.47 missing baselines) |
| TinyTrain | xNdE7RiRyP.md | 5.25 | 2 | Yes | On-device training with deployment; comparable strength profile, some negative-weight weaknesses |
| ROSA | cgCKm5DOnu.md | 6.00 | 1 | Yes | Higher-quality subspace PEFT paper; stronger theoretical analysis and broader experiments |

**Round 1 bracket:** 4.0–6.0 (above the 2.50 reject band, below the 7.5+ strong accept band).

**Round 2 narrowing:** WASI's weighted strengths (avg ~8.8) are stronger than SubTrack's (~8.1) and comparable to ROSA's (~8.5). Critically, all of WASI's weakness items carry positive weights (the most concerning at 2.04 for the missing ablation), whereas SubTrack, TinyTrain, and Memory-Efficient via Pruning each have negative-weight weaknesses that indicate more fundamental issues. This places WASI above 4.75 (SubTrack) and 5.25 (TinyTrain). However, the missing ablation is a genuine methodological gap that prevents full validation of the core claim, keeping the paper below ROSA (6.00).

**Final score:** 5.5 — a borderline paper with a clear and sensible methodological contribution, strong empirical results on resource reductions and real hardware, but held back by the missing ablation study that separates the novel component from prior work, along with several reporting clarity issues that reduce the strength of the evidence.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>