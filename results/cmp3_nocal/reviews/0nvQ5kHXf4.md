Now I have a thorough understanding of the paper and can verify each claim by the harsh critic against the actual text. Let me write the final consolidated review.

## Summary

This paper proposes WASI (Weight-Activation Subspace Iteration), a method for jointly compressing both weights and activations into low-rank subspaces during transformer fine-tuning, enabling on-device training on resource-constrained hardware. WASI combines weight subspace iteration (WSI) with activation subspace iteration (extending prior work on ASI) under a unified information-loss control framework. The method is evaluated on ViT, SwinT, and TinyLlama across multiple downstream tasks, with wall-clock measurements on a Raspberry Pi 5.

## Strengths

1. **Practical deployment validation on commodity hardware.** Figure 8 reports real wall-clock training and inference speed measurements on a Raspberry Pi 5 (~1.4× speedup over vanilla at ε=0.9). This goes beyond FLOP-counting and demonstrates that the compressed computation translates to actual runtime gains on a genuine resource-constrained device — a rare and valuable data point.

2. **Joint weight and activation compression.** Prior work (ASI, Nguyen et al., 2025) compressed only activations during training, leaving the architecture unchanged for inference. WASI's joint compression of weights and activations means inference can also run on the compressed representation, which is a genuine practical improvement over ASI for deployment scenarios where both training and inference memory budgets are tight.

3. **Multi-architecture evaluation across vision and language domains.** The method is tested on ViT, SwinT (vision transformers), and TinyLlama (a decoder-only LLM), providing broader evidence than prior work that focused primarily on compact convolutional models.

## Weaknesses

### Fatal

None.

### Major

1. **Main text lacks numerical accuracy values, standard deviations, and multi-seed reporting.** Every accuracy claim in the main body is supported only by qualitative descriptions of figures. For example, Section 4.3 states WASI "matches vanilla accuracy" at ε=0.9 on SwinT, but the reader cannot determine the actual accuracy numbers — whether this means 92.3% vs 92.5% or 90.0% vs 92.0%. The paper reports no absolute accuracy figures, no standard deviations, and mentions no multi-seed experiments. On downstream fine-tuning tasks (CIFAR-10, Pets, Flowers, CUB), run-to-run variance is non-trivial, and the absence of any variance reporting means the reader cannot assess whether observed patterns are robust. The paper defers numerical results to Appendix B.3 and Table 2, but the main text should present at least the headline accuracy numbers to support its central claim that WASI "maintains accuracy comparable to vanilla training."

2. **SVD-LLM is used as a baseline despite the paper itself acknowledging it is not suited for this setting.** Line 47 states that SVD-LLM "cannot be directly applied to all vision transformer-based models with activation maps of four or more dimensions." Despite this, Figure 5 compares WASI against SVD-LLM on ViT (a vision transformer), and SVD-LLM performs poorly as would be expected. This creates a staged comparison. The paper should include baselines that are designed for or adaptable to this setting — most notably LoRA, which is discussed in the related work but never compared against experimentally.

3. **TinyLlama experiment at ε=0.1 is difficult to interpret.** The paper sets the explained variance threshold to ε=0.1, retaining only 10% of weight variance — an extremely aggressive compression level. The reported accuracy range is 64–66% on BoolQ (a 50/50 yes/no task), which is barely above random guessing. The paper claims WASI achieves this "without accuracy loss" but does not report the vanilla accuracy numerically. At this compression level, it is unclear whether the method preserves model quality or whether the task is simply too easy for degradation to be detectable. Running at more standard ε values (e.g., 0.8 or 0.9) would clarify this.

4. **Subspace stability is validated on only one layer and one dataset.** Figure 3a shows singular value evolution for a single layer (W₆) on a single dataset (Pets). From this, the paper concludes that "ranks exhibit remarkable stability across epochs" (Section 4.2) as a general claim. Multi-layer and multi-dataset evidence would be needed to support this foundation of the method.

### Minor

1. **"First method" claim is overstated.** The paper calls WASI "the first method for efficient model-activation-decomposition-aware training." ASI (Nguyen et al., 2025) already performs activation decomposition during training; WASI adds weight decomposition to ASI. While the combination is new, the framing as "first" overstates the novelty.

2. **The abstract's "up to 2×" FLOPs reduction is inconsistently mapped to experimental results.** The main text reports 1.5× FLOP reduction on SwinT (Section 4.3) and much larger factors on TinyLlama (13–30×). The 2× figure is not explicitly tied to a specific experiment, making the abstract's claim imprecise.

3. **Complexity analysis assumes equal ranks for weights and activations without justification.** Section 3.4 states "For simplicity, we assume that the same optimal rank is applied to both A_i and W_i" for the memory and speed projections in Figure 2. This assumption is not empirically motivated; in practice optimal ranks for weights and activations could differ substantially.

### Trivial

None.

## Nice-to-Haves

- A breakdown of the overhead of subspace iteration itself (Gram-Schmidt orthogonalization, mode-wise unfoldings) relative to the savings in a WASI training iteration would help readers understand where time and memory are actually spent.
- Wall-clock and peak-memory measurements on GPU (beyond the Raspberry Pi 5 results) would connect the theoretical FLOP/memory reductions to actual runtime on the hardware used for the bulk of the experiments.

## Removed Points

These points were flagged during review but are removed with justification:

- **"WSI vs SVD comparison is a straw man."** The comparison in Figure 3b is a standard validation in the subspace iteration literature — it shows that the cheaper subspace iteration approximates the gold-standard full SVD well. This is not a straw man; it is a necessary sanity check. The reviewer's characterization is too harsh. *(Removed: factually inaccurate as a criticism.)*

- **"Equation 3 reference is misplaced."** The paper references Eq. 3 (∂L/∂A_i = ∂L/∂A_{i+1} · W_i) to justify that truncating W_i introduces error into the gradient computation. This reference is correct, as the equation shows the computation where W_i directly appears. *(Removed: the criticism misreads the paper.)*

- **"LoRA critique is unfair because LoRA wasn't designed for on-device training."** The paper's target scenario is on-device learning, and critiquing LoRA's memory footprint (frozen weights + adapters both in memory) from that perspective is legitimate even if LoRA was designed for a different setting. *(Removed: scope creep — the paper is entitled to evaluate methods against its own target setting.)*

- **"Underlying principles apply broadly is speculation."** This is a routine "broader impact" sentence in a conclusion section, not a substantive claim. *(Removed: trivial and standard for conclusion sections.)*

- **"100× memory efficiency claim conflates different design choices."** The comparison against SVD-LLM is apples-to-oranges by design (different architectures, different settings). The paper is transparent about what is being compared and why. *(Removed: the paper is clear about what the comparison entails.)*

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a table in the main text reporting absolute accuracy values (with standard deviations over multiple seeds) for all experimental conditions at all ε values tested. This is the single highest-impact change the authors can make.
2. Add a LoRA baseline to the vision transformer experiments. LoRA is the most directly related weight-compression method and its absence is the most conspicuous gap in the evaluation.
3. Run the TinyLlama experiment at more standard ε values (e.g., 0.8, 0.9) and report vanilla accuracy to allow meaningful comparison.
4. Expand the subspace stability analysis to cover multiple layers and at least two datasets.

## Score and Decision

The paper addresses a real and practically important problem and proposes a reasonable method. The Raspberry Pi 5 measurements are a genuine strength. However, the main text's complete reliance on figures rather than numerical accuracy values, the absence of any statistical rigor (no multiple seeds, no standard deviations), and the weak baseline selection (SVD-LLM, which the paper itself acknowledges is unsuitable) constitute significant evidential gaps. These issues prevent the paper from supporting its central claim that WASI "maintains accuracy comparable to vanilla training" with sufficient clarity and rigor.

MY FINAL SCORE: 4.0
MY FINAL DECISION: Reject