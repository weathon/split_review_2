Now I have a thorough picture of the paper. Let me compile the draft review and run calibration.Now I can produce the final calibrated review.

**Round 1 Bracket:** Based on the calibration anchors, the paper sits between the 3.5–5.5 band and the lower end of the 5.5–7.5 band. The closest topical anchor is "Harnessing Orthogonality to Train Low-Rank Neural Networks" (OIALR, avg 4.25) which also exploits SVD stability during training. WASI is more comprehensive (real edge-device evaluation, multi-model, joint framework) but lacks a critical LoRA baseline. My bracket is **4.5–6.0**.

**Round 2 Narrowing:** WASI is more practically grounded than OIALR (4.25) and "Memory-Efficient Backpropagation" (3.75), but less rigorously evaluated than ReLoRA (5.75) or LORO (6.0) which include LoRA comparisons and better scale. I place WASI at **5.0**.

---

## Summary

WASI (Weight-Activation Subspace Iteration) is an efficient on-device fine-tuning framework for transformer models that jointly compresses weight matrices and activation maps into stable low-rank subspaces. Leveraging the empirical insight that fine-tuning perturbs these subspaces only minimally, WASI replaces expensive per-iteration SVD with warm-started subspace iteration for both weights and activations. A dynamic-programming rank-selection algorithm replaces ASI's exponential brute-force search. Experiments span ViT and SwinT across five image classification datasets and TinyLlama on BoolQ, with on-device validation on a Raspberry Pi 5 showing 1.4× speedup over vanilla training.

## Strengths

- **Real on-device deployment (Sec. 4.4, Fig. 8):** Unlike most memory-efficient training papers that report simulated or theoretical speedups, the authors execute ViT fine-tuning on a Raspberry Pi 5 and report actual wall-clock iteration times. The 1.4× speedup at ε=0.9 is conservative and credible.

- **DP-based rank selection (Sec. 3.3 / Appendix A.2):** Replacing ASI's exponential brute-force search with a linear-time DP formulation is a concrete, useful improvement that directly reduces the pre-tuning overhead — a real bottleneck in resource-constrained settings.

- **WSI vs. full SVD ablation (Fig. 3b):** The comparison shows WSI achieves 1.36× fewer FLOPs than repeated full SVD at the same accuracy, and ~35% higher accuracy at matched FLOPs, directly validating the subspace-reuse argument.

- **Multi-model, multi-dataset coverage (Figs. 5–7):** Results span ViT and SwinT across five downstream datasets and extend to TinyLlama, providing non-trivial breadth for an efficiency method paper.

## Weaknesses

### Fatal
None.

### Major

- **No LoRA comparison at matched training-memory budgets.** The paper's central claim is that WASI sets a new accuracy-efficiency frontier for on-device transformer fine-tuning. LoRA is the dominant practical baseline for memory-efficient fine-tuning. Sec. 2 correctly notes that LoRA does not reduce inference memory (because adapters are merged at inference), but WASI also targets training memory, and the paper provides no comparison against LoRA at matched training memory. Without this, a reader cannot judge whether WASI's Pareto frontier is actually better than a readily available alternative in the training dimension. This is the most important evidential gap.

- **TinyLlama experiment is underspecified (Sec. 4.3, Fig. 7).** The experiment: (i) fixes ε=0.1 without sweeping other values; (ii) compresses only 5 of TinyLlama's 22 transformer blocks; (iii) reports activation/weight memory only over those 5 layers, so the stated 953× and 30× compression ratios are not system-level numbers; (iv) reports accuracy of 64–66% on BoolQ — a binary classification task — without providing the majority-class baseline or the pre-fine-tuning accuracy. As written, it is impossible to determine whether any of the compared configurations is learning anything above chance. This is the paper's weakest experiment.

### Minor

- **Stability assumption validated on a single layer of one model (Fig. 3a).** The entire subspace-reuse mechanism rests on the claim that K_i is stable across training iterations. Figure 3a shows only W6 of ViT fine-tuned on Pets. Whether this holds across early layers, SwinT, and TinyLlama — all of which WASI is applied to — is asserted but not evidenced.

- **Attention layers excluded from main results (Sec. 4.1).** The paper focuses on MLP blocks only, with attention results deferred to Appendix B.3. In LLM settings, attention layers (with KV caches) often dominate memory. This scope limitation is not clearly flagged in the main text.

- **On-device latency at batch size 128 (Fig. 8 caption).** Edge devices typically operate at small batch sizes; large-batch matmuls benefit from BLAS optimizations unavailable at batch size 1. Whether the 1.4× speedup holds at batch sizes ≤16 is not reported.

### Trivial
None.

## Nice-to-Haves

- A clean ablation showing WSI alone vs. ASI alone vs. WASI on the same accuracy-vs-training-memory curve (WSI alone is never isolated in the main comparison).
- Stability heatmaps (Fig. 3a style) for at least one SwinT and one TinyLlama layer to substantiate the core assumption more broadly.
- BoolQ majority-class and pre-fine-tuning accuracy in Fig. 7 to interpret the TinyLlama results.
- On-device latency at batch sizes 1 and 16.

## Removed Points

*These points are flagged to be removed, treat them with caution.*

- **SVD-LLM as a straw-man baseline:** The harsh critic argues that using SVD-LLM (acknowledged as ill-suited for vision transformers) flatters WASI. However, the asymmetry *disfavors the baseline*, not WASI — which per the hard rules means this cannot be a weakness. The paper also explicitly acknowledges the limitation (Sec. 2, Appendix A.4). Removed per hard rule.
- **Eq. 11 implicit symmetry / convergence concern:** Speculation that simultaneous L_i, R_i updates create a symmetry that may slow convergence. No evidence in the paper that this is an actual problem. Removed as speculative.
- **"Surpasses vanilla on CUB" regularization effect:** Interesting observation but not a flaw. Removed.
- **Abstract overclaims 62× memory reduction:** The figure is clearly tied to a specific model/setting (SwinT at ε=0.9, Sec. 4.3). Not a meaningful overstatement.

## Novel Insights

The DP formulation for rank selection converts an exponential combinatorial problem into a linear-cost one while preserving the perplexity-controlled information-loss guarantee — a small but practically impactful improvement. The joint coupling of weight and activation subspaces (Eqs. 8–11), where the weight low-rank factors directly shape gradient flow through compressed activations, is non-trivial and not addressed by prior work on either component in isolation.

## Suggestions

1. Add a LoRA comparison at matched training-memory budgets on at least one dataset (CIFAR-10 with ViT would suffice) to anchor WASI against the baseline practitioners actually use.
2. Sweep ε values in the TinyLlama experiment; report majority-class and pre-fine-tuning BoolQ accuracy; report system-level (all 22 layers) memory numbers alongside the fine-tuned-layers numbers.
3. Report on-device latency at batch sizes 1 and 16 in addition to 128.
4. Extend Fig. 3a to include one early layer (e.g., W1) and one layer from SwinT, to substantiate the stability assumption more broadly.

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| gwZ90hFSL2.md | 1.0 | R1 | Not applicable (humanoid robots NLP) |
| nSDOkm0SKo.md | 1.0 | R1 | Not applicable (finance) |
| 5lUdTogEL3.md | 1.0 | R1 | Not applicable (person re-ID) |
| eqKHuxIpp5.md | 2.5 | R1 | On-device TL mixed-precision — less novel, no real edge experiments |
| 04RLVxDvig.md | 3.0 | R1 | NanoMoE parameter efficiency — narrower contribution, no edge deployment |
| 49ti6LOUw5.md | 3.0 | R1 | UnoLoRA multi-task — narrower, GLUE-only, no real deployment |
| FVgizbs3o2.md | 3.75 | R1 | TensorGPT tensor decomposition compression — no training experiments |
| 17ZbByq95E.md | 3.75 | R1 | Memory-efficient backprop via randomized matmul — narrower, RoBERTa only |
| 0tsJ7Nv5hk.md | 4.25 | R1 | OIALR orthogonality + SVD stability — closest topical match; WASI more comprehensive but lacks LoRA comparison similarly |
| 0qexTTfnmH.md | 3.75 | R1 | ME-LoRA Bayesian LoRA — narrower |
| DLJznSp6X3.md | 5.75 | R1 | ReLoRA — broader scale (1.3B), stronger comparison set |
| pAVJKp3Dvn.md | 5.67 | R1 | Differentiable structured matrices — more theoretical grounding |
| i0zzO7Hslk.md | 6.0 | R1 | LORO Riemannian optimization — theoretically stronger |
| s7DkcgpRxL.md | 6.2 | R1 | LoRAM memory-efficient LoRA — includes LoRA comparison, comprehensive |
| TwJrTz9cRS.md | 8.0 | R1 | HiRA high-rank adaptation — stronger experimental design, rigorous baselines |

**Round 1 bracket: 4.5–6.0.**

WASI sits clearly above the 3.0–3.75 papers (it has real edge-device experiments, a joint framework, multi-model coverage). It sits below the 5.75–6.2 papers (ReLoRA, LORO, LoRAM), which all include LoRA comparisons and more rigorous or broader evaluations. The closest paper topically is OIALR (4.25), which WASI exceeds in practical validation. Accounting for the missing LoRA baseline (major gap) and the weak TinyLlama experiment, I place WASI at **5.0** — borderline reject.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>