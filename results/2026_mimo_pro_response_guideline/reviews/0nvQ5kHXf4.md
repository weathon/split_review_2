Now I have all the calibration data I need. Let me finalize the review.

## Summary

This paper proposes WASI (Weight-Activation Subspace Iteration), a method for efficient on-device fine-tuning of transformer models that jointly compresses both weight matrices and activation maps using low-rank subspace iteration controlled by an explained variance threshold. The method builds on the observation that essential parameter subspaces remain stable during fine-tuning, enabling SVD bases to be computed once and iteratively refined. WASI is evaluated on ViT, SwinT, and TinyLlama across six datasets, claiming up to 62× memory reduction, 2× FLOPs reduction, and 1.4× wall-clock speedup on a Raspberry Pi 5.

## Strengths

- **First unified weight-activation low-rank compression for transformer training**: WASI combines WSI and ASI into a single framework (Eqs. 8–11, Section 3.3). Critically, the paper shows that ASI alone exceeds vanilla training cost at ε=0.9 (Section 4.3, confirmed in Tab. 2), demonstrating that joint compression is genuinely necessary — not just a sum of parts.

- **Real-world latency validation on resource-constrained hardware**: Section 4.4 (Fig. 8) reports actual wall-clock timing on a Raspberry Pi 5, showing ~1.4× faster training and inference even at ε=0.9. This provides concrete evidence that the theoretical compression translates to practical gains on the paper's stated target hardware.

- **Massive memory reductions without accuracy degradation**: On SwinT across five datasets, WASI matches vanilla accuracy at ε=0.9 while reducing memory by up to 62× (Section 4.3, Fig. 6). On TinyLlama, activation memory drops by up to 953.86× and weight memory by 30.12× (Fig. 7).

- **Algorithmic improvement via dynamic programming for rank selection**: WASI redesigns ASI's rank selection with a DP strategy (Appendix A.2) that reduces search cost from exponential to linear, addressing a concrete scalability limitation of the prior ASI method.

- **Broad architectural and task coverage**: Evaluated on three distinct transformer architectures (ViT, SwinT, TinyLlama) across six datasets (CIFAR-10/100, CUB, Flowers, Pets, BoolQ), demonstrating generality beyond vision transformers.

## Weaknesses

### Fatal
None.

### Major

- **Narrow baseline set omits the most practically relevant competitors**: The main experiments compare only against ASI, SVD-LLM, and vanilla training (Section 4.1). For SwinT, the main paper shows only WASI vs. vanilla (Fig. 6), with other baselines deferred to Appendix B.3. Critically absent are LoRA and its variants — the dominant PEFT methods for on-device fine-tuning. While the paper discusses LoRA's trade-offs in the related work (Section 2: increased training memory from co-existing frozen weights and adapters, no inference benefit after merging), a direct experimental comparison would demonstrate whether WASI's training-memory-to-accuracy trade-off is actually superior in practice. Without this comparison, the claim of outperforming "state-of-the-art methods" is weakened. (The harsh critic's point about SVD-LLM being an imperfect baseline for vision transformers is addressed by the paper in Appendix A.4, so that specific concern is not retained.)

- **No ablation separating WSI and ASI contributions**: WASI combines two components — WSI (weight compression) and ASI (activation compression). The paper never reports WSI-only or ASI-only results side-by-side with WASI across the main experimental configurations. The paper notes that ASI alone exceeds vanilla training cost at ε=0.9 (Section 4.3), which is helpful but is a single data point. A systematic ablation across models and datasets would quantify the marginal benefit of adding weight compression to activation compression, clarifying whether the headline memory savings come primarily from one component or the synergistic combination.

- **Core stability hypothesis validated on a single configuration**: The foundational assumption — that the essential parameter subspace remains stable during fine-tuning, enabling SVD basis reuse — is validated in Section 4.2 using only one model (ViT), one dataset (Pets), and one weight matrix (W₆). Figure 3a shows singular value evolution across epochs for this single case. While the method's success across multiple models/datasets in Section 4.3 provides indirect evidence, direct validation of subspace stability across different layers, architectures, and datasets would substantially strengthen the core argument. The prior work cited (Radiya-Dixit & Wang, 2020; Li & Zhang, 2021) provides theoretical grounding, but the empirical validation in this paper is thin.

### Minor

- **Results reported exclusively as figures without tabular data or error bars**: All experimental results (Figs. 5–8) are presented as plots. The paper never reports specific accuracy numbers for any configuration in the main text. The claim that WASI "matches vanilla accuracy" at ε=0.9 is not backed by a table showing the accuracy difference is within some bound. Without error bars or variance across multiple runs, it is difficult to assess reliability, especially for the TinyLlama results where the y-axis ranges from 64% to 66% and differences appear within ~1%. (Note: Tab. 2 is referenced in the text but appears in the appendix.)

- **TinyLlama ε=0.1 choice unexplained and surprising results unaddressed**: Section 4.3 sets ε=0.1 for TinyLlama — dramatically lower than the ε∈{0.4,...,0.9} range for vision models — with no justification beyond "limited resources." Furthermore, WASI outperforms vanilla on TinyLlama (Fig. 7), which the paper does not discuss. If compression genuinely improves accuracy, this likely reflects regularization effects of low-rank approximation or suboptimal vanilla hyperparameters, both of which merit explicit discussion.

- **Key method details deferred to appendix**: The forward/backward pass operator f_LR (Eq. 9) and the dynamic programming rank selection strategy are deferred to Appendices A.1 and A.2. This means the main paper does not contain a fully self-contained description of the method, weakening readability.

### Trivial
None.

## Nice-to-Haves

- Energy measurements would strengthen the motivation: the introduction frames the problem in terms of energy consumption, and wall-clock time on Raspberry Pi is a proxy, but direct energy measurement would complete the picture.
- The abstract claims "up to 2× FLOPs reduction," but TinyLlama achieves 13–30× reductions. The abstract could be updated to reflect the full range of results.
- Justifying why WASI improves over vanilla accuracy on TinyLlama would strengthen that experiment.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Harsh critic's "apples-to-oranges" concern about Fig. 3b**: Checked against the paper — the WSI-vs-SVD comparison at the same FLOP budget across different ε values is a standard trade-off curve comparison. The criticism is not well-founded.
- **Harsh critic's SVD-LLM fairness concern**: The paper addresses this in Appendix A.4, noting SVD-LLM's limitation with 4D+ activation tensors. The comparison is still informative.
- **Harsh critic's claim about "the 2× FLOPs figure not being substantiated"**: The TinyLlama results actually show 13–30× FLOPs reduction, exceeding the "up to 2×" claim. The abstract understates the TinyLlama results.
- **Strength finder's claim about "principled compression via explained variance threshold"**: While true, this is a standard technique (used in prior work by the same authors), not a specific contribution of this paper. Dropped as generic.

## Novel Insights

The paper's genuinely novel insight is that joint weight-activation low-rank compression via subspace iteration is not merely additive — ASI alone at ε=0.9 exceeds vanilla training cost (Section 4.3), meaning that adding WSI is necessary to keep the combined method efficient. This demonstrates that treating weight and activation compression as a unified framework yields qualitatively different behavior than either alone. The DP-based rank selection improvement over ASI's brute-force search is also a concrete algorithmic advance.

## Suggestions

- Add LoRA as an experimental baseline for at least ViT/CIFAR-10 and SwinT to provide the most practically relevant comparison.
- Add a systematic ablation table showing WSI-only, ASI-only, and WASI results across all models/datasets.
- Validate the stability hypothesis (Fig. 3a) across at least 2–3 more layers of ViT and one layer each of SwinT and TinyLlama.
- Report tabular results with mean ± std across multiple runs for key configurations.
- Discuss why WASI improves over vanilla accuracy on TinyLlama (regularization effects? suboptimal vanilla hyperparameters?).

## Score and Decision

**Calibration anchors (all rounds):**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| On-Device Transfer Learning (eqKHuxIpp5) | 2.50 | 1 | Much weaker paper, limited scope — WASI is clearly stronger |
| TensorGPT (FVgizbs3o2) | 3.75 | 1 | Limited novelty, unconvincing experiments — WASI has stronger results |
| Memory-Efficient Backprop (17ZbByq95E) | 3.75 | 1 | Limited comparisons, limited scope — WASI has broader evaluation |
| OIALR (0tsJ7Nv5hk) | 4.25 | 1 | Very similar concept (SVD stability), similar weaknesses but weaker practical results — WASI is clearly better |
| Unlocking SVD-Space (8Agcic0csh) | 4.40 | 1 | SVD+DFA, no variance, limited real-world results — WASI has better practical evaluation |
| Decomposed Learning (7Cx05z4pUc) | 5.00 | 1 | SVD for grokking, different application — WASI has more practical impact |
| ReLoRA (DLJznSp6X3) | 5.75 | 1 | Low-rank training, accepted with similar weakness patterns — WASI comparable but slightly weaker scale |
| LORO (i0zzO7Hslk) | 6.00 | 1 | Low-rank Riemannian optimization, stronger theory — WASI is somewhat weaker |
| LoRAM (s7DkcgpRxL) | 6.20 | 1 | Memory-efficient LoRA, broader experiments — WASI has less comprehensive evaluation |
| LQ-LoRA (xw29VvOMmU) | 6.75 | 2 | Low-rank + quantized decomposition, stronger experiments — WASI is weaker |
| LoRAM (s7DkcgpRxL) | 6.20 | 2 | Memory-efficient LoRA, 70B models — WASI has narrower scale |
| ReLoRA (DLJznSp6X3) | 5.75 | 2 | Low-rank training, accepted — WASI comparable |
| LORO (i0zzO7Hslk) | 6.00 | 2 | Low-rank Riemannian optimization — WASI somewhat weaker |

**Round 1 bracket: 4.5 – 6.0**

WASI is clearly above OIALR (4.25) and the reject papers (3.75–5.00) due to its real device evaluation, joint weight-activation compression, and larger demonstrated memory savings. It's comparable to ReLoRA (5.75, Accept) but with narrower model scale and missing ablations, while having a more novel core idea and real hardware evaluation. It's below LORO (6.00) and LoRAM (6.20), which have stronger theoretical contributions or broader experiments.

**Final score: 5.5** — The paper has genuine novelty (joint weight-activation compression for transformers), strong practical results (62× memory reduction, real Raspberry Pi evaluation), and a concrete algorithmic improvement (DP rank selection). However, the evaluation gaps — narrow baselines missing LoRA, no WSI/ASI ablation, limited stability validation — are real and weigh against acceptance. The paper sits at the weak-accept boundary and would benefit substantially from a rebuttal addressing these concerns.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>