## Summary

This paper proposes HiSo, a Hessian-informed zeroth-order federated optimization method that accelerates convergence while preserving scalar-only communication (i.e., transmitting only scalars, not model-dimensional updates). The key insight is that the gradient scalars Δx already communicated for model reconstruction in ZO-FL (e.g., DeComFL) can be repurposed as a *free* signal to estimate a diagonal Hessian. The paper contributes: (1) a generalized scalar-only communication framework decoupled from ZO-SGD, (2) a convergence analysis showing dimension-independent rates under a "well-approximated" Hessian condition, and (3) consistent empirical speedups (1.4–5.4× in rounds) over DeComFL across OPT-125M to 2.7B on SST-2, QQP, and SQuAD.

## Strengths

- **Clever and well-motivated core idea.** The paper identifies a real tension in ZO-FL: methods like DeComFL achieve dimension-free communication but cannot incorporate second-order information. The insight that scalar gradient values Δx already communicated for model reconstruction can be repurposed as a *free* signal to estimate a diagonal Hessian (Section 4.2, Eq. 12) is genuinely novel and not an incremental extension.

- **Generalized scalar-only communication framework (Section 3.3, Algorithm 1).** By decoupling scalar-only communication from ZO-SGD specifically, the paper enables future methods to be plugged into this framework without redesigning the communication protocol. This is a useful conceptual contribution independent of HiSo itself.

- **Non-trivial convergence analysis.** The paper extends DeComFL's analysis to support multiple local updates (τ > 1), which DeComFL could not handle (Corollary 3). The whitening-rank analysis (Section 5.1) provides a theoretical mechanism for how Hessian-informed preconditioning can remove *d* and *L* dependence from convergence rates — the first such result for ZO methods in FL. The analysis correctly identifies DeComFL as a special case of HiSo (H_r ≡ I, Corollary 2).

- **Consistent empirical results across model scales.** HiSo outperforms DeComFL across OPT-125M, 350M, 1.3B, and 2.7B on SST-2, QQP, and SQuAD (Table 2, Table 3) with 1.4–5.4× round speedup. The empirical comparison against DeComFL is the right apples-to-apples baseline and is fairly conducted with matched per-round communication costs.

## Weaknesses

### Fatal

None.

### Major

- **The Hessian approximation rule (Eq. 12) is not theoretically or empirically justified as a Hessian estimator, creating a gap between the theory's driving assumption and the algorithm's actual mechanism.** The Hessian update H_{r+1} = (1−ν)H_r + ν·(1/m)Σ_i Diag(|Δx_{r,τ}^{(i)}|² + εI) is based on |Δx|² where Δx is the ZO gradient estimate, not the Hessian. The paper provides no derivation or evidence that Diag(|Δx|²) approximates the Hessian diagonal. Footnote 2 candidly states "our method resembles RMSProp" — an adaptive first-order method, not a second-order one. The convergence acceleration in Corollaries 1–3 depends on the "well-approximated condition" (Definition, Eq. 17): Tr(H^{-1/2}ΣH^{-1/2}) ≤ ζ where ζ is dimension-independent. The paper directly acknowledges (line 285): "Although it is hard to determine if this approximation holds in the context of LLMs." This means the headline theoretical result (dimension-independent convergence) is conditional on an assumption that is not linked to the algorithm's actual H update. The numerical simulation (Fig. 4) assumes H is already a good approximation — it does not simulate the actual |Δx|²-based update. **Crucially, this does not invalidate the empirical results**, which stand independently. Theorem 1 itself does not require the well-approximated condition. But the theoretical contribution is framed around the accelerated rate in Corollaries 1–3, and the gap between the needed condition and the algorithm's mechanism is unresolved.

### Minor

- **The first-order method comparison is framed in a way that overstates the practical advantage.** The abstract claims "up to 90 million times communication savings" compared to first-order baselines. However, first-order methods achieve substantially higher accuracy — e.g., on OPT-1.3B SST-2, FedAdam reaches 92.86% vs HiSo's 90.34%; on SQuAD, FedAdam reaches 61.56 F1 vs HiSo's 57.58 (Table 3). These accuracy gaps are larger than the differences among ZO methods themselves. The "90 million times" figure is a consequence of fundamentally different communication paradigms (ZO transmits scalars, first-order transmits full gradients), not a measure of algorithmic efficiency. The paper does acknowledge the accuracy gap in the text (line 319) but the abstract and introduction present the communication savings claim without this qualification.

- **The FL experimental setup is very small-scale (6 clients total, 2 sampled per round) for LLM experiments.** This limits generalizability to practical FL deployments where communication efficiency matters most (tens to thousands of clients). With only 6 clients, data heterogeneity and communication contention patterns are minimal. The MNIST experiment uses 64 clients, but that is a simpler task.

- **The convergence guarantee in Theorem 1 is for the preconditioned norm** E[||∇F(̄x_{r,k})||_{H_r^{-1}}²], not the standard gradient norm. Since DeComFL (H_r ≡ I) is recovered as a special case, the comparison is internally consistent. However, this choice of metric means the bound depends on H_r, which is learned from data and changes during training. If H_r has large entries, H_r^{-1} has very small entries and the preconditioned norm can be small even if the actual gradient is not. The paper does not discuss this limitation or provide bounds in the standard gradient norm.

- **The model-reset mechanism's computational cost on the client side is not discussed.** Each round, clients must reconstruct the model from historical scalars (lines 82–85). For clients that participate infrequently, this requires O(rounds_since_last_participation) computation. The paper discusses memory overhead but not this reconstruction cost.

### Trivial

None.

## Nice-to-Haves

- Add an empirical validation showing correlation between Diag(|Δx|²) and the true Hessian diagonal (e.g., scatter plot) on a small model where full Hessian computation is tractable — this would directly address the most significant theoretical gap.
- Relax the well-approximated condition by providing convergence bounds that depend on the actual H produced by the algorithm, even if messier. The empirical results suggest robustness that the theory should reflect.
- Include wall-clock time measurements to demonstrate net runtime improvement given ZO's additional forward passes.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *No wall-clock time comparison.* The paper states computation time is discussed in Appendix E. The appendix is stripped by the parser but exists in the original submission (per policy, points about missing appendix content are not assessed).
- *Missing comparison with LoRA-based FL.* This is outside the paper's stated scope (scalar-only ZO communication vs. low-rank adapter transmission are different paradigms).
- *Missing related work on diagonal Fisher preconditioning.* The paper acknowledges the RMSProp/Adam connection in footnote 2.
- *P=5 not defined in main text.* This hyperparameter is likely defined in the experimental appendix (stripped by parser).
- *No ablation isolating the Hessian component.* This is partially addressed by the DeComFL comparison, which the theory treats as HiSo with H=I (Corollary 2).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **(Highest priority)** Provide empirical evidence connecting Diag(|Δx|²) to the true Hessian diagonal on a small model, or provide a theoretical argument linking the squared ZO gradient to curvature information.
2. Qualify the "90 million times" communication savings claim in the abstract and introduction by noting the accuracy gap with first-order methods.
3. Scale the FL setup to more clients or add an explicit discussion of this limitation.
4. Add wall-clock time to show that round-speedup translates to real time savings, given ZO's additional forward passes.

---

## Calibration Report

**All anchors retrieved across rounds:**

| Path | Avg Score | Round | Itemized | Comparison to Paper Under Review |
|------|-----------|-------|----------|----------------------------------|
| `Uj0h13lVrR.md` | 1.00 | R1 | No | GFlowNets paper; completely unrelated topic, strong reject |
| `5kMwiMnUip.md` | 1.40 | R1 | No | LLM jailbreaking; unrelated |
| `5lUdTogEL3.md` | 1.00 | R1 | No | Person re-identification; unrelated |
| `nSDOkm0SKo.md` | 1.00 | R1 | No | Financial markets; unrelated |
| `IsHWcsk4Fz.md` | 3.00 | R1 | No | Adaptive FL via dissimilarity; topic-related but low-scoring |
| `zqXANcFO9T.md` | 1.67 | R1 | No | Compressed decentralized learning; related topic, rejected |
| `Jl0aEFrp11.md` | 2.75 | R1 | No | Bidirectional communication FL; mixed scores, rejected |
| `Og7ZZd7hDm.md` | 3.25 | R1 | No | Adaptive momentum FL composition; rejected |
| **`ZAMoxm86KV.md`** | **3.67** | **R1** | **Yes** | Federated ZO with trajectory-informed gradients. Rejected; weaker empirical validation, GP assumption concern. My paper is stronger. |
| `jkhVrIllKg.md` | 4.25 | R1 | No | FL with second-order heterogeneity — different approach |
| `uaGNerHa1J.md` | 4.67 | R1 | No | Newton-type FL — similar second-order theme but different setting |
| `DdPeCRVyCd.md` | 4.00 | R1 | No | Communication-efficient federated low-rank |
| **`omrLHFzC37.md`** | **6.25** | **R1, R2** | **Yes** | **DeComFL — direct predecessor.** My paper is a clear improvement (adds Hessian-informed preconditioning, generalized framework, extended theory). Score anchor. |
| `ipQrjRsl11.md` | 6.20 | R1 | No | Connecting ADMM to Bayes in FL — different subfield |
| **`bEqI61iBue.md`** | **5.67** | **R1, R2** | **Yes** | **HiZOO — Hessian-informed ZO (single-node).** Similar Hessian estimator gap. My paper adds FL dimension and generalized framework. Score anchor. |
| `kjn99xFUF3.md` | 6.00 | R1 | No | Adaptive FL with constraints — different approach |
| **`e0rQRMUhs7.md`** | **6.60** | **R2** | **Yes** | **FRLoRA — federated LoRA for LLMs.** Different approach (PEFT vs ZO). Comparable in empirical scope. Score anchor. |
| `Cy5IKvYbR3.md` | 5.75 | R2 | No | Textual gradient in FL — different paradigm |
| `8HuLgtjqOD.md` | 6.00 | R2 | No | Gradient compression — different technique |
| **`myYzr50xBh.md`** | **5.80** | **R2** | **Yes** | ZO fine-tuning with static sparsity — ZO but single-node, different FL context |
| `ZuazHmXTns.md` | 7.60 | R1 | No | Problem-parameter-free FL — high score, different focus |
| `fMTPkDEhLQ.md` | 8.00 | R1 | No | Optimization lower bounds — theory paper, different content |
| `cc8h3I3V4E.md` | 8.00 | R1 | No | Nash equilibria — unrelated |
| `5t57omGVMw.md` | 8.00 | R1 | No | Linear system solvers — unrelated |

**Round-1 bracket:** [5.5, 7.0]

**Narrowing logic:** Comparing weighted items, my paper's strengths (weights 9.37, 9.02, 10.43, 10.76) are comparable to DeComFL's strongest items (weights 10.40, 11.30, 12.80) and above HiZOO's (weights 8.20, 8.41, 8.62). My major weakness (Hessian approximation gap, weight 2.38) is less negatively weighted than DeComFL's effective-rank concern (weight 8.65) and similar in character to HiZOO's Hessian estimator concern (weight 2.41). The empirical validation across model scales is stronger than either DeComFL or HiZOO. However, the unresolved theoretical gap prevents the score from exceeding the DeComFL anchor by more than a narrow margin. I place the score at **6.0** — a borderline accept reflecting a clever, empirically sound contribution whose theoretical claims are tempered by an unverified assumption at the heart of the acceleration result.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>