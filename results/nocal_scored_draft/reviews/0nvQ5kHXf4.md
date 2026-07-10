Now let me write the complete final review.

## Summary

This paper introduces WASI (Weight-Activation Subspace Iteration), a method for resource-constrained transformer fine-tuning that jointly compresses both weights and activations into low-rank subspaces using subspace iteration. The key idea exploits the stability of parameter subspaces during fine-tuning: SVD is computed once at initialization, and cheap subspace iteration updates the factors thereafter. WASI is evaluated on ViT, SwinT, and TinyLlama across five datasets, with on-device Raspberry Pi 5 experiments showing ~1.4× wall-clock speedup. The joint compression of weights and activations during training is a genuine contribution that addresses a real gap in prior work.

## Strengths

- **Joint compression of weights and activations within a unified training framework (Sec. 3.3).** Prior training-time compression methods target either weights (SVD-LLM, LoRA) or activations (ASI, AMC) but not both simultaneously. WASI's combination of WSI and ASI in a single training loop is a genuine technical contribution addressing a real gap: neither weight-only nor activation-only compression fully relieves the memory bottleneck of backpropagation for on-device transformer training.

- **Real on-device deployment measurement (Sec. 4.4, Fig. 8).** Raspberry Pi 5 experiments provide concrete evidence that the method's theoretical savings translate into actual wall-clock speedup (~1.4×) on resource-constrained hardware, which strengthens the paper significantly beyond simulated FLOPs/memory reporting.

- **Multi-architecture validation across ViT, SwinT, and TinyLlama on five datasets (CIFAR-10/100, CUB, Flowers, Pets, BoolQ).** This breadth demonstrates that the approach generalizes beyond a single model family.

## Weaknesses

### Major

- **Missing direct LoRA baseline comparison.** LoRA is the dominant parameter-efficient fine-tuning method for transformers and directly relevant to the paper's stated goal of on-device training. The paper discusses LoRA in related work (Sec. 2, lines 41–47) and critiques its drawbacks (frozen weights + adapters co-existing in memory; no inference speedup), but never directly compares against standard LoRA with rank sweeps analogous to WASI's ε sweeps. SVD-LLM (which internally uses LoRA adapters) is compared instead, but this is not a substitute for a direct LoRA comparison. The paper itself acknowledges (line 223) that "LoRA adapters allow SVD-LLM to achieve the lowest FLOPs," making this comparison particularly important for establishing WASI's relative merits. Without it, the paper's central comparative claims about improving on PEFT are not fully supported.

- **TinyLlama experiment (Sec. 4.3) has methodology issues that weaken its conclusions.** (a) ε=0.1 retains only 10% of variance — an extraordinarily aggressive compression level — and the reported accuracy (64–66% on BoolQ, a binary task where random is 50%) is reported without error bars, making the "outperforms vanilla" claim inconclusive. (b) Resource measurements are scoped to "only the layers that are fine-tuned" (line 227, last 5 layers), which inflates reported compression ratios by excluding the fixed cost of frozen layers that must also reside on the device. (c) The headline ratios (953.86× activation memory reduction, 30.12× weight memory reduction) apply only to the fine-tuned subset and do not translate to meaningful end-to-end savings when frozen layers are included.

- **No variance or statistical significance reported for any experimental result.** Throughout Sec. 4, every result is presented as a single point or curve with no error bars, no repeated runs, and no seed information. For fine-tuning on small datasets (CIFAR-100, CUB, Flowers, Pets) where accuracy can vary by several points across runs, this omission makes it impossible to assess whether reported accuracy differences (e.g., WASI "surpasses vanilla on CUB," line 225) are meaningful or within noise. The Raspberry Pi timing results (Fig. 8) report "average time" without specifying how many runs were averaged or what the variance was.

### Minor

- **Stability evidence mismatch (Sec. 4.2, Fig. 3a).** The text (line 197) claims "the ranks exhibit remarkable stability across epochs," but the supporting figure is a heatmap of singular values with a color bar spanning -1 to 4. Singular values and ranks are different objects; the figure does not directly show rank over epochs, and the color range indicates substantial evolution of singular magnitudes. Even if rank remains constant under ε=0.8, a rank-stable matrix whose singular values shift meaningfully could affect whether the subspace learned at iteration 0 remains appropriate at iteration T. The evidence should directly plot rank \(K_i\) vs. epoch.

- **Abstract numbers not clearly anchored.** The abstract claims "up to 62× memory reduction" and "up to 2× computational cost (FLOPs) reduction." At ε=0.9 (the setting that preserves accuracy), the main text (line 225) reports 62× memory reduction but only 1.5× FLOPs reduction for SwinT. The claimed 2× FLOPs reduction in the abstract lacks a clear anchor in the reported results.

- **SVD-LLM applicability claim vs. experiments.** The paper states (line 47) that SVD-LLM "cannot be directly applied to all vision transformer-based models with activation maps of four or more dimensions" but then compares against SVD-LLM on ViT and SwinT. The paper should clarify how SVD-LLM was adapted for these experiments, since the statement in related work implies a limitation that the experiments appear to contradict.

### Trivial

- None.

## Nice-to-Haves

- Add a supplementary table reporting exact numerical accuracy, memory, and FLOPs values for every configuration shown in the figures (currently the resource-efficiency plots are difficult to read exact values from).
- The complexity analysis (Sec. 3.4) assumes the same optimal rank for weights and activations, which the paper acknowledges as a simplifying assumption but limits the analysis's predictive value for the actual method.

## Removed Points

These points were filtered out after verification against the paper and should be treated with caution if referenced:

- *WSI-vs-SVD comparison is a straw-man experiment*: REMOVED. The experiment compares WSI (subspace iteration) against recomputing full SVD at every iteration — a standard validation technique for subspace iteration methods. The paper's main results (Fig. 5, 6) already compare against vanilla training, so this specific experiment serves its stated purpose of validating the subspace iteration component independently. The critic's framing as a "straw-man" misunderstands the experimental design.
- *"First method" claim overstated*: REMOVED. WASI combines weight and activation decomposition in a unified training framework, which neither ASI (activation-only) nor SVD-LLM (weight-only) does. The "first" claim is defensible in this combined context and is a minor framing issue at most.
- *Circular dependency in WSI design*: REMOVED. The critic themselves notes this "is not itself a flaw." The experiments are designed to validate the stability assumption that the method relies on.
- *100× comparison is apples-to-oranges*: REMOVED. The paper states (line 219) that "the same compression ratios are applied to SVD-LLM," indicating an attempt at fair comparison. Without access to the precise operating points, this criticism cannot be substantiated as a specific problem.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a direct LoRA baseline to the main comparisons at matched accuracy or matched compression budget.
2. Run experiments with 3–5 seeds and report mean accuracy ± std for all configurations.
3. For the TinyLlama experiment, report end-to-end memory including frozen layers or clearly scope the claims to the fine-tuned subset; consider using a more standard ε value (e.g., 0.6–0.9) for comparability.
4. Replace or supplement Fig. 3a with a direct plot of rank \(K_i\) vs. epoch to directly support the rank stability claim.
5. Clarify how SVD-LLM was adapted for ViT/SwinT experiments given the stated limitation in Sec. 2.

## Score and Decision

The paper presents a well-motivated idea — jointly compressing both weights and activations into low-rank subspaces during transformer fine-tuning — and provides real on-device validation on a Raspberry Pi 5. However, the evaluation has three significant gaps: the missing LoRA baseline (the most relevant PEFT comparison), the complete absence of variance reporting, and methodological issues in the TinyLlama experiment that weaken its conclusions. These are addressable in revision but currently prevent the contribution from being fully established. The core contribution is real, and with a more rigorous evaluation the paper could be a solid contribution to the on-device learning literature.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>