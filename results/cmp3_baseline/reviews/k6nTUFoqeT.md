## Summary

The paper introduces **FASTer**, a framework for efficient autoregressive Vision-Language-Action (VLA) modeling. It consists of two components: **FASTerVQ**, a neural action tokenizer using residual vector quantization (RVQ) with an action patchifier and hybrid transformer encoder, and **FASTerVLA**, an autoregressive policy built on FASTerVQ that employs block-wise autoregressive (BAR) decoding and a lightweight action expert. The tokenizer achieves high compression ratios while preserving reconstruction fidelity, and the policy delivers faster inference and strong task performance across simulated and real-world benchmarks spanning multiple embodiments, backbones, and task types.

## Strengths

- **Comprehensive and well-designed evaluation.** The paper evaluates on nine benchmarks across four real robots and four simulated environments, covering a wide range of tasks (deformable manipulation, whole-body control, long-horizon, instruction following) and embodiments (single-arm, bimanual, whole-body). This is one of the most thorough experimental studies in the VLA tokenization literature.
- **Clear and practical efficiency gains.** FASTerVLA achieves meaningful speedups over prior autoregressive VLA models (e.g., 112ms vs 176ms for π₀ on LIBERO, and 237ms vs 1,100–3,000ms for π₀-FAST on whole-body control) without sacrificing task performance. BAR decoding reduces autoregressive steps while maintaining quality.
- **Strong empirical results.** FASTerVLA sets new state-of-the-art on LIBERO (97.9% average success rate) and on Simpler-Bridge (87.9%), outperforming both diffusion-based and autoregressive baselines by clear margins. The gains persist across multiple VLM backbones (PaliGemma, Qwen2.5, InternVL3.5), demonstrating robustness.
- **Well-motivated tokenizer design.** The action patchifier non-uniformly groups dimensions by physical semantics, which mitigates distribution imbalance. The use of DCT frequency loss alongside time-domain loss is a sensible choice for capturing both local details and global trends. Ablation results (in appendix) support these choices.
- **Analysis of codebook utilization.** The paper shows that FASTerVQ achieves 100% codebook utilization and higher normalized entropy than prior tokenizers, and correlates this with improved zero-shot generalization on Bridge and Droid. This provides useful insights for future tokenizer design.

## Weaknesses

### Fatal
None.

### Major
- **Some claims are overstated.** The paper asserts it provides "the first systematic analysis of action tokenization for VLAs," but prior works (e.g., VQ-VLA, RT-2 with binning, DCT+BPE in FAST) have already analyzed tokenization strategies. The claim is not critical to the paper's value but should be toned down. Similarly, "near-lossless reconstruction" is imprecise—the VRR metric only measures reconstruction within a tolerance, and perfect reconstruction is not achieved even for σ=10⁻³.
- **Limited novelty of individual components.** The tokenizer borrows heavily from audio codec designs (RVQ, transformer-based VQ, frequency-domain loss). Block-wise autoregressive decoding is an adaptation of existing ideas from language and video models. The lightweight action expert resembles the approach in π₀. The main contribution is the combination and careful adaptation to the action domain, which is valuable but incremental.
- **Lack of theoretical grounding for BAR decoding order.** The paper advocates a coarse-to-fine decoding order (codebook-wise before temporal) based on the RVQ structure, but does not provide an ablation comparing this ordering with alternatives (e.g., temporal-first). This would strengthen the claim about stability and efficiency.

### Minor
- **VRR metric validation is incomplete.** VRR is introduced as a task-relevant fidelity metric, but its correlation with actual task success is not empirically verified. The threshold σ is not systematically justified across different action dimensions and embodiments. A simple experiment showing VRR correlates with policy performance would be helpful.
- **Inference timing comparison limited to one hardware setup.** All latency numbers are on RTX 5090 with PyTorch. Results may differ across hardware and software stacks, and no comparison with TensorRT or other optimized deployments is provided. The claim of "practically usable regime" would be stronger with broader evidence.
- **Evaluation of scaling behavior could be deeper.** While Figure 5 shows scaling trends for the tokenizer (S, L, XL variants), the downstream policy is only evaluated with one tokenizer scale. It is unclear how the scaling of the tokenizer translates to policy performance gains.

### Trivial
- The paper uses "FASTer" and "FASTerVLA" interchangeably, causing minor confusion.

## Nice-to-Haves

- An ablation comparing the proposed codebook-wise decoding order with temporal-first or other orderings, to validate the coarse-to-fine hypothesis.
- A direct experiment confirming that VRR improvements lead to downstream policy improvements, e.g., by comparing policies trained on tokenizers with different VRR but same code length.
- A discussion on the sensitivity of inference latency to block size B and a practical guideline for selecting B.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Tone down the "first systematic analysis" and "near-lossless" claims to avoid overstatement.
- Add an ablation on BAR decoding order (codebook-wise vs temporal-first vs mixed) to justify the design choice.
- Include a simple correlation plot between tokenizer VRR (at a fixed σ) and downstream task success rate on a few representative tasks.

## Score and Decision

The paper makes a solid empirical contribution to the important problem of efficient action tokenization and inference for autoregressive VLA models. The evaluations are comprehensive, the results are strong, and the practical speed gains are clear. While the individual components are not highly novel, the carefully engineered combination and thorough experimental validation represent a meaningful advance. The weaknesses are manageable and do not invalidate the core claims.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>