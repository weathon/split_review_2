Now I have enough calibration context. Let me produce the final consolidated review.

**Round-1 bracket**: Based on calibration anchors (L-MSA 3.0, LoRA-FA 5.33, Merging Feed-Forward Sublayers 3.5, EigenLoRA 5.0), this paper sits between 3.5 and 5.0. The method has more novelty than the 3.0-3.5 papers, but the evaluation gaps are more significant than the 5.0-5.3 papers. Narrowed to **4.0–4.5**.

---

## Summary

This paper proposes WASI (Weight-Activation Subspace Iteration), a method that jointly compresses both weight matrices and activation maps into low-rank subspaces during transformer fine-tuning. The key ideas are: (1) leveraging subspace stability to apply cheap subspace iteration for weights (WSI) rather than full SVD recomputation, and (2) combining this with activation subspace iteration (ASI) for a unified low-rank training framework. Experiments on ViT, SwinT, and TinyLlama show memory and FLOPs reductions, with a 1.4× speedup measured on a Raspberry Pi 5.

## Strengths

- **Joint compression of weights and activations is a genuine design contribution.** Prior work addresses either weights (SVD-LLM, LoRA) or activations (ASI, AMC) but not both in a unified training framework. The paper clearly distinguishes itself from these lines of work (Sec. 2), and the formalization of the forward/backward pass in the low-rank space (Eq. 8–11) is a sound technical contribution.

- **Real hardware evaluation on Raspberry Pi 5.** The on-device latency experiment (Sec. 4.4, Fig. 8) measures actual wall-clock time rather than FLOPs alone, providing concrete evidence of practical speedup (1.4×) on an edge device. This is directly relevant to the stated application domain.

- **Clear method presentation and reproducibility effort.** Algorithm 1 for WSI, the forward/backward pass derivations (Eq. 8–11), and the stated hardware/software environment (PyTorch 1.13.1, Quadro RTX A4500, Raspberry Pi 5) make the method reproducible. The paper commits to open-sourcing the code.

## Weaknesses

### Major

- **Missing LoRA baseline.** LoRA (Hu et al., 2022) is discussed extensively in Sec. 2 as a related approach, with specific critiques about its memory overhead during training and uncompressed inference. Yet WASI is never compared against LoRA experimentally. Given that LoRA is the *de facto* standard for efficient transformer fine-tuning and is directly relevant to the paper's stated goal of enabling on-device training, this is a critical omission. The SVD-LLM baseline partially involves LoRA adapters, but that comparison has its own issues (see below).

- **SVD-LLM baseline is not adequately justified.** The paper states in Sec. 2 that SVD-LLM "cannot be directly applied to all vision transformer-based models with activation maps of four or more dimensions" (citing Appendix A.4). Yet SVD-LLM is used as a baseline for ViT on CIFAR-10 (Fig. 5) without explaining how it was adapted to work in this setting. The paper also states that "for fairness, the same compression ratios are applied to SVD-LLM" but does not describe how compression ratios are equated between WASI's explained-variance threshold ε and SVD-LLM's decomposition. Without this information, the reader cannot assess whether SVD-LLM is being evaluated fairly or in a degraded configuration. *The paper should clarify whether ViT's 3D activations avoid the 4D-tensor issue cited in Appendix A.4, and should explain the compression-ratio mapping.*

- **Headline memory numbers are based on MLP-block-only measurement.** The abstract claims "memory usage by up to 62×" — this number comes from SwinT experiments (Sec. 4.3, Fig. 6) where measurement is restricted to "linear layers within multi-perceptron blocks" (Sec. 4.1). The paper acknowledges extended results with attention layers in Appendix B.3, but the headline claim in the abstract (and the paper's main narrative) is based on partial measurement. For a transformer, attention layers (QKV projections, output projections), embedding layers, and normalization also consume memory. While MLP blocks are a substantial fraction of total parameters, the 62× figure would be materially lower on a total-model basis. The paper should either report total-model memory in the main text or clearly qualify the headline number.

- **TinyLlama experiment is not strong enough to support the broad claims drawn from it.** This experiment uses ε = 0.1 (an extremely aggressive compression threshold retaining at least 10% of variance), evaluates on BoolQ where accuracies cluster in a ~2 percentage-point range near random (64–66%), and reports memory/FLOPs reductions (953.86×, 30.12×) that compare WASI-compressed fine-tuning of the last 5 layers against vanilla fine-tuning of the same 5 layers. No standard LLM fine-tuning baselines (LoRA, QLoRA, AdaLoRA) are provided. The paper should either strengthen this experiment with meaningful compression settings (e.g., ε ≥ 0.8) and standard PEFT baselines, or scale back the claims made from it.

### Minor

- **WSI benefit over a fixed-initial-decomposition baseline is not established.** The stability hypothesis (Sec. 3.3) claims the weight subspace is stable across iterations. If so, a fixed SVD computed once at initialization (without further subspace iteration) should suffice. The paper compares WSI against "reapplying truncated SVD at every training iteration" (Fig. 3b), which is the expensive baseline — not against a fixed-initial-decomposition baseline. Without this comparison, it is unclear whether WSI's per-iteration subspace iteration provides any benefit over simply using the initial decomposition throughout training. Adding this baseline would cleanly isolate the value of the subspace-iteration component.

- **No error bars or variance reporting.** All experiments are reported without standard deviations or confidence intervals. Given that fine-tuning accuracy can vary with random seed, comparisons such as "WASI surpasses vanilla on CUB" (Sec. 4.3) cannot be verified as statistically meaningful.

- **No component ablation for WASI.** The paper does not ablate the contribution of WSI alone (without ASI) or ASI alone (without WSI) on the transformer setting. Since ASI was originally designed for CNNs, an ablation isolating each component's contribution would be informative.

- **The dynamic-programming improvement to ASI** is mentioned (Sec. 3.3) but not evaluated in isolation. How much does it improve over ASI's original brute-force search?

- **Abstract's "up to 2×" FLOPs claim** is not clearly tied to a specific experiment in the main text — the SwinT experiment reports 1.5× (Sec. 4.3), and the ViT experiment reports different numbers.

### Trivial

- Fig. 3b (WSI vs. SVD comparison) does not specify which marker corresponds to which ε value, making it difficult to verify the claimed 35% accuracy improvement at the same FLOPs.

## Nice-to-Haves

- Compare WASI against a version using a fixed initial SVD decomposition without per-iteration subspace iteration, to isolate WSI's contribution.
- Report total model memory (including attention, embeddings, normalization) alongside the MLP-block-only numbers.
- Include LoRA, QLoRA, and AdaLoRA as baselines for the TinyLlama experiment, using realistic ε values (≥ 0.8).
- For the Raspberry Pi experiment, include ASI as a comparison point since ASI was previously evaluated on the same hardware.
- Report standard deviations or confidence intervals for key accuracy numbers, especially for fine-grained comparisons (e.g., CUB, BoolQ).

## Removed Points

The following points from the input review were flagged for removal:

- **"WSI may be redundant under its own assumptions (structural)"** — The critic argued that if the subspace is stable, fixed initial SVD should suffice. However, the stability claim is about ranks being stable, not subspace basis vectors being identical. Subspace iteration tracks drifting bases cheaply. The comparison against full SVD recomputation is a reasonable standard baseline. This weakness is demoted to **Minor** rather than structural/fatal, as the fixed-initial-decomposition baseline would be nice to have but is not required to validate the method.

- **"The 2× FLOPs figure is not clearly traced"** — Demoted to **Minor** from a more severe classification; it's a presentation inconsistency, not a methodological flaw.

- **"The paper oversells the distinction between LoRA and Low-rank Models"** — Removed as this is a subjective opinion about framing; the paper's categorization is factually correct and the distinction is meaningful.

- **"Complexity analysis assumes same rank for weights and activations"** — The paper explicitly states this is a simplifying assumption ("For simplicity," Sec. 3.4), and the actual method does not require it. Demoted to **Trivial**.

- **"WSI vs SVD Figure 3b lacks error bars"** — Merged into the general "no error bars" Minor weakness above.

- **Various appendix-related criticisms** — Removed per policy: the appendix is stripped by the parser and exists in the original submission.

## Novel Insights

None beyond the paper's own contributions. The input reviews did not surface an unexpected synthesis or cross-cutting observation that the paper itself misses.

## Suggestions

1. **Add LoRA as a primary baseline** across the ViT, SwinT, and TinyLlama experiments. This is the comparison the community cares about most and is the minimum expectation for a paper discussing LoRA extensively.
2. **Clarify the SVD-LLM adaptation** — explain how it was made to work on ViT (does ViT's 3D activation structure avoid the 4D-tensor issue?), and describe how compression ratios were equated between methods.
3. **Report total-model memory** alongside the MLP-block-only numbers, or clearly qualify that the 62× figure reflects MLP blocks only.
4. **Strengthen or remove the TinyLlama experiment** — run with ε ≥ 0.8 and include standard PEFT baselines, or drop it if resources are insufficient.
5. **Add a fixed-initial-SVD baseline** for the WSI comparison to demonstrate whether subspace iteration actually adds value over keeping the initial decomposition fixed.
6. **Add error bars** (at least 3 random seeds) for key comparisons, especially those where the paper claims WASI "surpasses vanilla" (CUB dataset).

## Score and Decision

**Calibration anchors consulted** (all rounds):

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| L-MSA (xi3sDtf8A0.md) | 3.0 | R1 | Similar missing LoRA baseline, less novel method |
| Merging FF Sublayers (CgqnYqpYQh.md) | 3.5 | R2 | Similar compression theme, less novel method |
| Subspace Node Pruning (k9QklPhLCs.md) | 3.5 | R2 | Related subspace approach, limited evaluation |
| Memory-Efficient FT via Pruning (JMgxtZqkvO.md) | 4.5 | R1 | Similar evaluation gaps, comparable completeness |
| Activations Aren't Cheap (3ylNuZXtMg.md) | 4.25 | R2 | Similar topic (activation memory), comparable evaluation scope |
| LoRA-FA (RbKThNNFxr.md) | 5.33 | R2 | More complete evaluation, less novel method |
| EigenLoRA (KxGGZag9gW.md) | 5.0 | R2 | Better evaluation despite being about LoRA variants |
| ROSA (cgCKm5DOnu.md) | 6.0 | R1 | Better experiments and baselines, similar subspace idea |

**Round-1 bracket**: 3.5–5.0  
**Narrowed to**: 4.0–4.5  

The paper introduces a genuinely novel approach (joint weight-activation compression via subspace iteration) and includes a rare real-hardware evaluation. However, the evaluation has significant gaps: missing the most important baseline (LoRA), an inadequately justified SVD-LLM comparison, headline numbers from partial measurements, and a weak LLM experiment. These issues undermine confidence in the paper's strongest claims. The ideas are promising enough that a substantially revised version could be a solid contribution, but the paper in its current form does not provide sufficient evidence.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>