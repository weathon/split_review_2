Now I have a solid calibration picture. Let me finalize my review and score.

**Calibration Summary:**

Round 1 retrieved papers across the full spectrum:
- Strong reject (<1.5): Clearly off-topic papers (Chinese NLP, financial analysis) — our paper is far above this.
- Reject (1.5–3.5): FeDeRA (3.00), HoLoRA (3.00) — simpler PEFT variants with weak evaluation.
- Borderline reject (3.5–5.5): AutoTrunc (4.00, rejected) — SVD for LLM compression, similar topic but narrower than our paper. TensorGPT (3.75, rejected), Decomposed Learning (5.00, rejected).
- Borderline accept (5.5–7.5): AdaRankGrad (7.00, accepted) — stronger theory but similar evaluation gaps. LDAdam (7.00, accepted). ROSA (6.00, rejected) — good theory but incremental. ASVD (6.25, rejected) — very relevant, our paper directly improves on it. MCNC (6.00, accepted). Network Memory Footprint (6.33, accepted).
- Accept (7.5–8.5): HiRA (8.00, accepted) — cleaner contribution with fewer weaknesses.

Round 1 bracket: 5.5–6.5.

Round 2 narrowed with more specific queries:
- TinyTrain (5.25, rejected) — edge training, narrower than our paper.
- ASVD (6.25, rejected) — closest topical match; our paper improves on ASVD with training-time compression and hardware validation.
- MCNC (6.00, accepted) — compression via reparameterization.
- Zeroth-Order Fine-Tuning (5.80, accepted) — memory-efficient fine-tuning.

Round 2 confirms the bracket: 5.5–6.5, with 6.0 as the center.

**Positioning:** Our paper improves on ASVD (6.25, rejected) by incorporating activation-aware SVD into training-time compression and adding weight compression jointly, with real hardware validation. It's weaker than AdaRankGrad (7.00, accepted) in theoretical depth and evaluation breadth (stability validated on one config, TinyLlama limited). It's comparable to ROSA (6.00, rejected) and MCNC (6.00, accepted). The genuine joint compression contribution and hardware validation push it above the weaker anchors, but the evaluation gaps prevent it from reaching 7+.

**Final score: 6.0** — a solid borderline paper with a genuine practical contribution that needs more thorough evaluation to fully support its claims.

## Summary
This paper proposes WASI (Weight-Activation Subspace Iteration), a method for efficient transformer fine-tuning on resource-constrained devices by jointly compressing weight matrices (via SVD-initialized subspace iteration) and activation maps (via improved ASI) into low-rank representations under a controlled explained-variance threshold. Experiments span ViT, SwinT, and TinyLlama across image classification tasks and BoolQ, with on-device latency validated on a Raspberry Pi 5.

## Strengths
- **Joint weight-activation compression fills a genuine gap.** Prior methods compress either weights (LoRA, SVD-LLM) or activations (ASI, AMC) but not both jointly during training. Fig. 5 shows WASI achieves up to 100× higher memory efficiency than SVD-LLM at comparable accuracy on ViT/CIFAR-10, because SVD-LLM requires LoRA adapters that keep full weights in memory while WASI compresses both into low-rank subspaces. This directly addresses the dual memory bottleneck in backpropagation.
- **Empirical validation of the subspace stability assumption.** Fig. 3a demonstrates remarkable stability of singular values across 40 training epochs. Fig. 3b shows WSI requires 1.36× fewer FLOPs than recomputing full SVD to reach the same accuracy, and outperforms SVD by ~35% at equal FLOP budgets — validating that subspace reuse does not degrade convergence.
- **Principled information-loss control.** The rank choice K_i is governed by an explained variance threshold ε (Eq. 5–7), directly linking truncation to information loss — more grounded than prior approaches like ASVD and FWSVD that "lack a theoretical link between the truncation loss and model performance loss" (Sec. 2).
- **Validation on actual resource-constrained hardware.** Fig. 8 reports wall-clock measurements on a Raspberry Pi 5 (Cortex-A76 CPU, 8GB RAM): even at the least aggressive compression (ε=0.9), WASI is ~1.4× faster than vanilla for both training and inference — demonstrating real deployment viability rather than just simulated FLOP counts.
- **Two algorithmic improvements over ASI.** A dynamic-programming rank selection strategy reduces search cost from exponential to linear (Appendix A.2), and an extension to 3D activation tensors (Appendix A.1) enables application to transformer architectures.

## Weaknesses

### Fatal
None

### Major
- **Stability assumption validated on a single model/dataset pair.** Section 4.2 states "In these experiments, we focus on fine-tuning ViT model using Pets dataset." The stability of the singular value structure — the foundational premise justifying SVD-once-then-reuse — is verified only for ViT/Pets (Fig. 3a). If this stability degrades under different conditions (larger learning rates, longer schedules, more distribution shift, or different architectures), the method's convergence guarantees weaken. The paper cites prior theoretical work (Radiya-Dixit & Wang, 2020; Li & Zhang, 2021), but the gap between "models are close in parameter space" and "singular value structure is stable enough for subspace iteration" is non-trivial and requires broader empirical verification. This is the paper's central assumption and should be tested across at least SwinT and a different dataset with varied learning rates.

- **TinyLlama experiment is too rudimentary to support the paper's broad positioning.** The experiment (Section 4.3, Fig. 7) uses a single ε=0.1, fine-tunes only the last 5 layers out of the full model, and compares only against vanilla training — acknowledged as due to "limited resources." Given that the title and abstract position WASI for "transformers" broadly, the LLM evaluation should match the rigor of the vision experiments: varying ε to show accuracy-efficiency tradeoff curves and including SVD-LLM as a baseline. As presented, this is a proof-of-concept rather than a convincing evaluation.

### Minor
- **SwinT main-paper comparison lacks baseline diversity.** Fig. 6 — the model where WASI's strongest headline claim of 62× memory reduction originates — compares only WASI vs. vanilla across datasets, with "additional baselines in Appendix B.3." Moving key comparative results to the appendix weakens the main narrative. ASI and SVD-LLM baselines for SwinT should be in the main paper to substantiate the "outperforms state-of-the-art" claim.

- **Only MLP linear layers evaluated in the main results.** Section 4.1 states the evaluation focuses on "linear layers within multi-perceptron blocks for fair comparison with previous methods (extended results with attention layers in Appendix B.3)." Attention layers are architecturally central to transformers; their inclusion in the main evaluation would strengthen the paper's claims about transformer training efficiency.

### Trivial
None

## Nice-to-Haves
- The interaction between the low-rank weight representation and optimizer state (e.g., Adam's first and second moment estimates) is not discussed. If Adam maintains state for the full L_i R_i product, memory savings from weight compression are partially offset. A brief discussion or measurement would clarify practical savings.
- A brief sensitivity analysis on what happens at higher learning rates or with more aggressive fine-tuning schedules would strengthen confidence in robustness.
- The complexity analysis assumes "the same optimal rank is applied to both A_i and W_i" for simplicity (Section 3.4). Noting how this simplification affects real-world predictions would be helpful.

## Removed Points
These points are flagged to be removed, treat them with caution:
- The harsh critic raised concerns about "up to" figures in the abstract coming from different experimental settings. While technically a valid observation, this is standard practice in ML papers and not misleading.
- The harsh critic questioned whether Eq. 11's weight update breaks the low-rank constraint. Algorithm 1 explicitly re-projects via subspace iteration each iteration, addressing this concern. The method is internally consistent.
- The harsh critic raised an "optimizer state" concern as a methodological gap — this is more of a nice-to-have clarification than a real weakness, as the paper's memory accounting can be verified from the reported numbers.
- Formatting/presentation nitpicks flagged by the harsh critic are parser artifacts.

## Novel Insights
The paper's genuinely novel contribution is the joint compression of both weights and activations during transformer fine-tuning via unified subspace iteration, combined with the empirical validation that weight subspace stability enables SVD-once-then-reuse. This bridges the gap between prior work that addressed only one side of the memory bottleneck (weights via LoRA/SVD-LLM or activations via ASI/AMC). The demonstrated 100× memory efficiency gain over SVD-LLM on ViT/CIFAR-10 concretely shows the benefit of addressing both sides simultaneously, and the Raspberry Pi 5 validation demonstrates real-world deployment feasibility.

## Suggestions
- Expand stability validation (Fig. 3a-style) to at least SwinT/Pets and ViT/CIFAR-100 with a few learning rates — minimal compute, high impact on claim support.
- Expand the TinyLlama experiment to include varying ε and SVD-LLM as a baseline, matching the vision experiment protocol.
- Move SwinT ASI/SVD-LLM comparison from Appendix B.3 into Fig. 6 in the main paper.
- Briefly discuss or measure the optimizer state memory overhead when maintaining Adam moments for the low-rank weight factors.

## Reporting

**All retrieved anchors:**

| Round | Path | Avg Score | Comparison |
|-------|------|-----------|------------|
| 1 | gwZ90hFSL2 | 1.00 | Off-topic (Chinese NLP) — our paper far above |
| 1 | nSDOkm0SKo | 1.00 | Off-topic (financial analysis) — our paper far above |
| 1 | P49gSPmrvN | 1.00 | Off-topic (text visualization) — our paper far above |
| 1 | ZTvUT49JjL | 3.40 | Implicit bias in matrix factorization — weaker topic match |
| 1 | GtlRN48XYA | 3.00 | FeDeRA — federated PEFT, narrower contribution |
| 1 | igGeaxOiFM | 3.00 | HoLoRA — LoRA variant, incremental |
| 1 | 3KEwJGYNzH | 4.00 | AutoTrunc — SVD for LLM compression, narrower evaluation |
| 1 | 7Cx05z4pUc | 5.00 | Decomposed Learning — SVD for grokking, different focus |
| 1 | FVgizbs3o2 | 3.75 | TensorGPT — tensor decomposition, training-free |
| 1 | LvNROciCne | 7.00 | AdaRankGrad — stronger theory, similar evaluation gaps |
| 1 | Zkp1GuHerF | 7.00 | LDAdam — low-dim optimizer, accepted |
| 1 | cgCKm5DOnu | 6.00 | ROSA — subspace adaptation, similar quality, rejected |
| 1 | TwJrTz9cRS | 8.00 | HiRA — cleaner PEFT, fewer weaknesses |
| 1 | Tzh6xAJSll | 7.60 | Scaling Laws for Associative Memories — theoretical |
| 1 | f4gF6AIHRy | 8.00 | DiSF — data selection, less relevant |
| 2 | xNdE7RiRyP | 5.25 | TinyTrain — edge training, narrower scope |
| 2 | Svt3SGy0yd | 5.80 | GEARnn — growing networks on edge |
| 2 | myYzr50xBh | 5.80 | Zeroth-Order Fine-Tuning — memory-efficient, accepted |
| 2 | 1RrOtCmuKr | 6.33 | Network Memory Footprint — compression via codebooks |
| 2 | pAVJKp3Dvn | 5.67 | Differentiable Structured Matrices — accepted |
| 2 | VMV8gefvq8 | 6.00 | MCNC — manifold-constrained compression, accepted |
| 2 | HyPofygOCT | 6.25 | ASVD — very relevant, our paper improves on it directly |

**Bracket:** Round 1 established 5.5–6.5. Round 2 confirmed this range. ASVD (6.25, rejected) is the closest topical match — our paper improves on it with training-time compression, joint weight-activation compression, and hardware validation, but adds its own weaknesses (narrow stability validation, limited LLM eval). AdaRankGrad (7.00, accepted) is stronger in theory and evaluation breadth. The paper sits at the borderline, slightly below AdaRankGrad but above AutoTrunc (4.00) and TinyTrain (5.25).

**Final score: 6.0** — a solid paper with a genuine practical contribution and real hardware validation, held back by evaluation gaps (stability assumption validated on one config, TinyLlama too limited) that should be addressable in a revision.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept