## Summary
The paper introduces FASTer, a framework for efficient autoregressive vision-language-action (VLA) models comprising two components: FASTerVQ, a transformer-based residual vector quantization (RVQ) action tokenizer that compresses action chunks into structured discrete codes, and FASTerVLA, a VLA model that uses block-wise autoregressive (BAR) decoding and a lightweight action expert for fast inference. The framework is evaluated across 9 benchmarks spanning 5 embodiments in both simulation and real-world settings, achieving state-of-the-art performance with significantly reduced inference latency.

## Strengths
- **Comprehensive and rigorous evaluation**: The paper evaluates across 9 benchmarks, 5 embodiments (single-arm, bimanual, whole-body control), 3 VLM backbones, and both simulation and real-world settings. This is substantially more thorough than most prior VLA work and provides the community with a valuable reference for action tokenization design.
- **Strong empirical results**: FASTerVLA achieves 97.9% on LIBERO (new SOTA), 87.9% on Simpler-Bridge (12.9% over second-best), and consistently outperforms baselines. Inference latency is reduced to 112ms on LIBERO vs. 176–556ms for π₀-FAST, a practical improvement.
- **Cross-embodiment generalization of the tokenizer**: Training FASTerVQ solely on single-arm delta-EEF data and testing on bimanual, whole-body, and different action representations (velocity, absolute/delta joint positions) is a strong and surprising result, suggesting a transferable action prior exists in normalized action space.
- **Data scaling behavior**: Figure 5 demonstrates that FASTerVQ scales well with data, achieving near-lossless reconstruction at σ=10⁻³ with the XL variant, which is important for the long-term viability of this approach.
- **Well-motivated design**: The action patchifier grouping by physical semantics to handle distributional imbalance, the DCT+time-domain dual loss, and the coarse-to-fine decoding order aligned with RVQ structure are all sensible and well-justified design choices.

## Weaknesses
### Fatal
None.

### Major
- **BAR contribution is modest in accuracy**: Looking at Figure 7, the improvement from FASTer w/o BAR to FASTer is small (e.g., 94.0→94.8 for PaliGemma, 95.4→95.45 for Qwen). The headline gains appear driven primarily by FASTerVQ rather than the block-wise decoding. The speed benefit is real but the accuracy contribution needs clearer justification.
- **Ablations deferred entirely to appendix**: The paper claims contributions from the action patchifier, RVQ design, codebook size, residual depth, action expert, and BAR decoding, yet the main text provides almost no ablation evidence. At minimum, a summary table of key ablation findings should appear in the main paper to help readers assess which components matter most.
- **VRR metric not validated against downstream performance**: The paper introduces VRR as a reconstruction quality metric but does not demonstrate that VRR actually correlates with task success rate. Without this validation, it is unclear whether optimizing VRR is the right objective. A simple correlation analysis would substantially strengthen this contribution.

### Minor
- **Comparison fairness**: Most experiments initialize FASTerVLA from π₀-FAST pretrained checkpoints, which may give an advantage over baselines initialized differently. The paper partially addresses this for Bridge/Droid but the concern persists for other settings.
- **"First systematic analysis" claim is strong**: Prior work (e.g., Pertsch et al. 2025 with FAST) has also analyzed action tokenization trade-offs. The claim should be more precisely scoped.
- **Spacing augmentation under-explained**: The position jittering trick in Section 3.2 is interesting but lacks motivation or ablation. Why does this help, and how sensitive is performance to the jitter range k?

### Trivial
None.

## Nice-to-Haves
- A correlation plot between VRR and downstream task success rate across tokenizers
- A summary of key ablation results in the main text (even a single table)
- Analysis of failure cases—when does FASTerVLA still fail, and is it related to tokenizer limitations?

## Novel Insights
The most genuinely novel finding is that action chunks from diverse robot platforms share a transferable structure in normalized action space: a tokenizer trained on single-arm data can reconstruct bimanual and whole-body actions with high fidelity, and this generalization improves with data scale. This suggests that a universal action tokenizer is feasible, which has significant implications for scaling VLA models. The connection between codebook utilization entropy and downstream generalization (Table 8 analysis) is also a useful empirical observation for the community.

## Suggestions
- Add a summary ablation table in the main text showing the marginal contribution of each component (patchifier, RVQ, BAR, action expert)
- Validate VRR against task success by computing correlation across tokenizers and tasks
- Clarify the pretraining and data conditions for each comparison in Table 1 to ensure fairness
- Discuss failure modes and when the tokenizer's compression becomes a bottleneck

## Score and Decision
The paper presents a well-engineered framework with strong empirical results across an impressively broad evaluation suite. The cross-embodiment generalization of the tokenizer is a genuinely valuable finding. However, the individual technical components (RVQ, block-wise generation, mixture-of-experts) are relatively well-known techniques combined in a straightforward manner, the BAR contribution to accuracy is modest, and the main text lacks ablation evidence for the claimed contributions. The work is solid and practically useful but falls short of a clear accept at a top venue.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>