Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper proposes WASI (Weight-Activation Subspace Iteration), a low-rank training framework that jointly compresses both weight matrices and activation maps during transformer fine-tuning for on-device learning. The key insight is that weight subspaces remain stable across fine-tuning iterations due to small learning-rate updates, enabling cheap subspace iteration (one SVD at initialization + Gram-Schmidt per step) to replace expensive per-iteration full SVD for weights, while activation maps are compressed via Tucker decomposition. WASI is evaluated on ViT, SwinT, and TinyLlama across multiple datasets, with real hardware measurements on a Raspberry Pi 5. The paper reports memory reductions up to 62× and a 1.4× wall-clock speedup on the Pi.

## Strengths

- **Joint compression of weights and activations under a unified framework.** Unlike prior work targeting either weights (LoRA, SVD-LLM) or activations (ASI, AMC) in isolation, WASI simultaneously compresses both. The method is clearly presented in Sec 3.3 (Eqs 8–11 and Algorithm 1), showing forward/backward passes operating directly on low-rank representations. This enables memory reductions that neither weights-only nor activations-only methods can achieve on their own.

- **Subspace iteration for weights (WSI) that avoids per-iteration full SVD.** Prior weight-decomposition methods (ASVD, FWSVD, SVD-LLM) require a fresh truncated SVD at each training step. WSI computes the SVD once at initialization and then applies cheap Gram–Schmidt orthogonalization per iteration (Algorithm 1). The paper validates this empirically (Fig 3b, Sec 4.2): WSI requires 1.36× fewer FLOPs than per-iteration SVD at the same accuracy and outperforms SVD by ≈35% accuracy when both are given equal FLOPs.

- **Real hardware evaluation on a Raspberry Pi 5 with measured wall-clock speedups.** Sec 4.4 (Fig 8) reports actual per-iteration timing on a Pi 5. At ε=0.9, WASI is ≈1.4× faster than vanilla training for both training and inference. This provides tangible evidence that the method delivers real latency improvements on the constrained hardware it targets, going beyond simulated FLOPs/memory numbers.

- **Extension of subspace-based on-device training from CNNs to multiple transformer architectures.** WASI is evaluated on ViT, SwinT, and TinyLlama (Sec 4.3), demonstrating domain extension beyond the convolutional models that prior on-device subspace methods (ASI, Gradient Filter) were limited to.

- **Ablation evidence that activation energy concentrates across all tensor modes.** Fig 4 (Sec 4.2) shows explained variance across modes 1–3 for all layers of ViT activation tensors, confirming that most energy concentrates in the first few singular values and justifying the Tucker decomposition compression strategy.

## Weaknesses

### Fatal

None. The method is sound and the core claims are supported by evidence, albeit with presentation gaps.

### Major

1. **No numerical accuracy values in the main paper.** Every experimental result is conveyed exclusively through figures plotting accuracy against memory or FLOPs. There are no tables reporting actual accuracy numbers, standard deviations, or information about number of runs. The paper references "Tab. 2" (line 223) and "Appendix B.3" (line 247) for numerical results, but these are absent from the main text. For a paper whose central claim is that WASI preserves accuracy while reducing cost, the absence of concrete accuracy values prevents the reader from precisely quantifying the accuracy-efficiency trade-off. This is the single most important weakness to address.

2. **LoRA is not included as a baseline.** LoRA (Hu et al., 2022) is discussed extensively in the related work (lines 41–45) and acknowledged in the main results discussion (line 221: "owing to its avoidance of LoRA adapters"). Yet it is never directly compared against WASI. Since LoRA is the most widely used parameter-efficient fine-tuning method, this omission limits the paper's ability to position WASI relative to the dominant approach. The paper's critique of LoRA (memory overhead from co-existing weights, no inference savings) would be substantially strengthened by direct experimental comparison.

### Minor

3. **Ambiguity in the 35% accuracy improvement claim (Sec 4.2, Fig 3b).** The paper states "WSI outperforms SVD by approximately 35% in terms of accuracy" (line 199) and Fig 3b annotates "35.36% higher in Acc." It is not clarified whether this is relative improvement or absolute percentage points. This is a preliminary experiment comparing WSI vs per-iteration SVD at equal FLOPs, so the context is understandable, but the metric definition should be explicit.

4. **Limited validation of weight subspace stability.** The claim that "the essential information of a model parameters resides in a stable subspace throughout fine-tuning" (line 33) is validated on a single weight matrix (W₆ from ViT on Pets, Fig 3a). The paper states it "monitor[s] the layer ranks K_i throughout the course of training" (line 197) but only W₆ is shown. While the activation-side analysis (Fig 4) covers all layers, the weight-side evidence is narrow. Broader validation across layers, models, and tasks would strengthen the paper's foundational assumption.

5. **TinyLlama experiment is too limited to establish generality.** The LLM experiment (Sec 4.3, Fig 7) fine-tunes only the last 5 layers at a single aggressive compression level (ε=0.1) on a single dataset (BoolQ). Resource consumption is logged "only at the layers that are fine-tuned" (line 227), so the 953.86× activation memory reduction applies only to those layers, not the full model. While the paper is transparent about these caveats, the scope is insufficient to convincingly demonstrate generality to decoder-only LLMs.

### Trivial

6. **Abstract claims "up to 2×" FLOPs reduction** while the specific experiment cited (SwinT at ε=0.9, line 225) achieves 1.5×. The abstract value appears to be a theoretical ceiling estimate, but the discrepancy should be reconciled.

7. **Complexity analysis assumes same rank for weights and activations** (line 165), which is a simplification since W_i and A_i have different dimensionalities and structure.

## Nice-to-Haves

- A breakdown of memory savings (weight compression vs. activation compression vs. optimizer states) would strengthen the method analysis.
- Analysis of why 62× memory compression translates to only 1.4× wall-clock speedup — attributing overhead from orthogonalization, I/O, or Tucker decomposition costs — would help guide future work and sharpen the contribution.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Criticisms about missing appendix content.** The parser strips appendices from all papers; the authors included detailed results in Appendix B.3 (attention layers, extended baselines, numerical results). These are not missing from the submission.
- **Complaints about PyTorch 1.13.1 being outdated or the GPU not being modern.** The paper targets edge devices (Raspberry Pi 5), not H100-class hardware. The GPU choice is irrelevant to the paper's core claims.
- **Request for comparison with subnetwork training methods** (Lin et al., 2022; Quelennec et al., 2024). The paper's scope is explicitly low-rank decomposition (line 39), not subnetwork training. Criticizing its absence is scope creep.
- **Complaint that "ASI was designed for CNNs" makes it an unfair baseline.** WASI builds on ASI; comparing against the prior method it extends is standard practice, and the paper makes no claim that ASI should perform optimally on transformers.
- **Complaint that the paper's framing of LoRA's drawbacks is incomplete** (missing discussion of optimizer-state savings). The paper's claim about memory overhead from co-existing weights is correct in its context; optimizer-state memory is a separate argument.
- **Formatting nitpicks** (undefined overline notation, complexity analysis simplification). The notation is standard and inferable from context; the analysis simplification is explicitly stated.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add a table with numerical accuracy values** (with standard deviations over multiple runs) for all main experiments in the paper, especially ViT on CIFAR-10 (Fig 5), SwinT across datasets (Fig 6), and TinyLlama on BoolQ (Fig 7).
2. **Include LoRA as a baseline** in at least the main ViT experiment on CIFAR-10. This is the most important comparison missing from the evaluation.
3. **Clarify whether the 35% accuracy improvement** (Fig 3b) is relative or absolute, and report the actual accuracy values for this comparison.
4. **Broaden weight subspace stability validation** to multiple layers and at least one additional model-dataset pair.
5. **Either extend the TinyLlama experiment** to more datasets and compression levels, or explicitly qualify the generality claims to acknowledge the limited scope.
6. **Reconcile the abstract's "up to 2× FLOPs" claim** with the experimental value of 1.5× reported in the body.

## Score and Decision

The calibration database was inaccessible, so I rely on direct assessment. The paper presents a well-motivated method (WASI) with a clear algorithmic contribution — joint weight-activation subspace iteration — and demonstrates real hardware speedups on a Raspberry Pi 5. The main weaknesses are in evaluation presentation: no numerical accuracy tables, missing LoRA baseline, and a few ambiguous or narrow claims. These are substantive but fixable. The method itself is sound and the core contribution (subspace iteration for weights + joint compression framework) is novel.

Relative to the ICLR scale, this paper sits between borderline reject (4) and borderline accept (6). It has a genuine contribution that could be accepted with reasonable revisions, but the evaluation gaps as presented prevent full endorsement. Score 5.5 reflects a borderline paper with real strengths and fixable weaknesses.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>