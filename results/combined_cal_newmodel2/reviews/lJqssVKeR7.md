## Summary

This paper proposes HiSo, a Hessian-informed zeroth-order federated optimization algorithm that preserves scalar-only communication while incorporating curvature information. It extends DeComFL's dimension-free communication framework by introducing a diagonal preconditioner H that is learned from local ZO updates, and provides a generalized scalar-only communication framework (Algorithm 1) that decouples dimension-free communication from vanilla ZO-SGD. The paper reports 1.4–5.4× communication-round speedups over DeComFL and provides convergence theory under a "well-approximated" Hessian condition.

## Strengths

- **The generalized scalar-only communication framework (Algorithm 1, Section 3.3) is a clean contribution.** It decouples scalar-only communication from its tight coupling with vanilla ZO-SGD, enabling broader classes of optimizers within the same communication-efficient infrastructure. The paper demonstrates this by instantiating HiSo as one such optimizer. [favorability=11.76]

- **The variance analysis chain in Section 5.1 (Eq. 13 → Eq. 14 → Eq. 15 → Eq. 16) provides a clear reasoning path for why Hessian-informed ZO can reduce gradient variance.** Moving from the standard Ld bound through low-effective rank Lκ to the whitened quantity ζ gives a structured argument, and the synthetic eigenvalue simulation in Fig. 4 makes the intuition concrete. [favorability=12.43]

- **The empirical speedup over DeComFL is consistent across 3 model sizes (OPT-125M, 350M, 1.3B, 2.7B) and 3 tasks (SST-2, QQP, SQuAD),** with 1.4–5.4× round speedup and 29%–80% communication savings (Table 2). Final test accuracy is consistently higher than all ZO baselines (Table 3), with standard errors reported. Communication costs are quantified concretely in KB. [favorability=13.53]

## Weaknesses

### Fatal

None.

### Major

- **The Hessian estimation mechanism does not have a clear mathematical connection to the actual Hessian.** The H update (Eq. 12) accumulates Diag([Δx]²) where Δx ∝ g·H^{-1/2}u (Eq. 8). Taking expectations, the update depends on H^{-1} (through uuᵀ) scaled by the squared directional derivative g² — not directly on curvature. At a fixed point of the expected dynamics, H collapses to a scaled identity, carrying no curvature information. The paper acknowledges the method is "akin to Adam's per-coordinate scaling" (line 138) and "resembles RMSProp" (footnote 2), which track gradient second moments — a fundamentally different mechanism from Hessian estimation. Yet the abstract, introduction, and experimental section (Section 6, line 289) frame H as a "diagonal Hessian approximation" without resolving this tension. [favorability=-0.17]

- **The convergence rate comparison between HiSo and DeComFL is across different norms.** Theorem 1 bounds the preconditioned gradient norm ‖∇F(x̄_{r,k})‖²_{H_r^{-1}}, while DeComFL's rate (Corollary 2, H=I) recovers the standard gradient norm. A small preconditioned norm does not imply a small gradient norm when H has disparate eigenvalues — the claimed L-independent acceleration may be partially an artifact of the metric choice. Additionally, the learning rate condition in Theorem 1 includes a factor √(1/(L(d+2))) that depends on dimension d, so even with the well-approximated condition, practical step sizes shrink with dimension. [favorability=4.43]

- **The well-approximated condition (Definition, Eq. 17) required for the clean theoretical rates has no proof or argument that HiSo's H update actually satisfies it.** The paper acknowledges this ("it is hard to determine if this approximation holds," line 285) and claims poor H "at worst case, degenerates into DeComFL" (line 286), but this claim is unsubstantiated — a poorly estimated H could in principle hurt more than I. The theory's clean rates (Corollaries 1–3) are therefore decoupled from the algorithm's demonstrated behavior. [favorability=-1.54]

### Minor

- Inconsistency in the Hessian update definition: the main text (line 140, Eq. before the algorithm block) uses Δx^{(i)}_{r,τ} (last local step), while the algorithm block (Eq. 12 / line 174) uses Δx_{r,0} (first local step). The discrepancy is not explained. [favorability=3.99]

- The FL evaluation setup (6 clients, 2 sampled per round) is small-scale; only OPT model variants are used (no Llama, Mistral, or other architectures). [favorability=0.60]

- The speedup metric in Table 2 measures rounds for HiSo to match DeComFL's best accuracy, which inflates the apparent improvement since HiSo's final accuracy is also higher. Accuracy gaps over DeComFL are modest in several cases (e.g., OPT-1.3B SST-2: 90.34% vs 90.22%; SQuAD F1: 57.58 vs 57.14), where differences could fall within hyperparameter tuning noise. Full learning curves for LLM experiments would aid assessment. [favorability=4.55]

- No ablation varying τ (local update steps) is provided, despite Corollary 3 claiming an advantage for τ>1. Learning rate sensitivity is also not reported, though the Theorem 1 learning rate condition is restrictive. [favorability=1.33]

### Trivial

None.

## Nice-to-Haves

- Provide a small-scale validation comparing the learned H against the actual diagonal Hessian for a small model (e.g., the CNN on MNIST already used in Fig. 5).
- Add ablations on τ and learning rate sensitivity.
- Provide full convergence curves for LLM experiments.

## Removed Points

These points from the input review were filtered according to the specified rules and are listed here for transparency:

- **"The research question is well-motivated"** — removed as generic/superficial, lacking specific content tied to this paper.
- **Synthetic simulation values "not grounded in actual LLM Hessian spectra"** — removed because the paper presents this as a synthetic illustration (200 log-normal eigenvalues), not a claim about real LLMs.
- **Criticisms about missing appendix content** (Appendix D, E, F.7.1, F.7.2, proofs deferred to appendix) — removed per rules: parser strips appendices from all papers.
- **"Convergence plots missing"** — folded into Minor weakness 6.
- **"The learning rate condition could make the bound quantitatively vacuous"** — folded into Major weakness 2.
- **Any mention of missing related works or unverifiable references** — removed.
- **The critic's claim that the paper's "H_r approximates the Hessian" claim is circular with a specific fixed-point calculation showing H = |g|I** — the general point about the mechanism not tracking the Hessian is retained in Major weakness 1, but the specific fixed-point derivation (which treats g² as a scalar constant independent of u, omitting fourth-moment effects) is overly simplified. The retained weakness does not rest on that specific calculation.

## Novel Insights

None beyond the paper's own contributions. The input review's primary novel insight — that the H update tracks something closer to an RMSProp-style gradient second moment than the Hessian — is already reflected in Major weakness 1 and in the paper's own footnotes.

## Suggestions

- Provide a small-scale validation comparing the learned H against the actual diagonal Hessian for a small model (e.g., CNN on MNIST) to substantiate the "Hessian approximation" claim, or reposition the contribution around "adaptive scalar-only ZO-FL" without claiming curvature estimation.
- Clarify what quantity H actually tracks via a fixed-point analysis of the update rule (Eq. 12).
- Unify convergence metrics: state DeComFL's rate in the same H^{-1}-norm and discuss what the rate improvement means in concrete terms.
- Add ablations on τ and learning rate sensitivity; provide full convergence curves for LLM experiments.

## Score and Decision

**Calibration summary.** All anchors retrieved across rounds (n=4 per band):

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| /home/.../omrLHFzC37.md (DeComFL) | 6.25 | R1 | Yes | Direct baseline; cleaner story, no Hessian issue. HiSo extends it but with significant caveats. |
| /home/.../bEqI61iBue.md (HiZOO) | 5.67 | R1 | Yes | Single-node Hessian-informed ZO. Similar Hessian estimation concerns; fewer compounded theoretical issues. |
| /home/.../uaGNerHa1J.md (FedNewton) | 4.67 | R1,R2 | Yes | Newton-type FL; only works for KRR. More limited scope. |
| /home/.../DJRd4IQHGQ.md (FeedSign) | 5.25 | R2 | Yes | ZO FL with 1-bit communication. Serious novelty concerns (-1.49, -2.95). |
| /home/.../jkhVrIllKg.md (SABER) | 4.25 | R1 | Yes | Second-order FL with limited novelty (-4.62). |
| /home/.../ZAMoxm86KV.md (FZooS) | 3.67 | R1 | Yes | ZO FL with impractical storage costs, small-scale experiments. |

**Round-1 bracket:** 4.5–6.0. The paper is clearly above FZooS (3.67) and SABER (4.25) due to cleaner experiments and the generalized framework, but below DeComFL (6.25) and HiZOO (5.67) because of compounded issues: the Hessian estimation mechanism is not justified, the theory uses a different convergence norm, and the well-approximated condition is disconnected from the algorithm.

**Round-2 narrowing:** FeedSign (5.25) is the closest topical anchor in the 4.5–6.0 band. FeedSign had damaging novelty-based weaknesses (favorability -1.49, -2.95, -3.50) and a bias-in-estimation concern (0.05). The current paper has two damaging soundness-based weaknesses (favorability -0.17, -1.54). Soundness issues are more fundamental than novelty issues, placing HiSo slightly below FeedSign. Against HiZOO (5.67): the single-node paper had the same Hessian estimation concern but fewer compounded problems (no norm mismatch, no condition disconnect). HiSo is weaker than HiZOO.

**Final score of 5.0** is grounded in: the paper's three major weaknesses all have negative or near-negative favorability (-1.54, -0.17, 4.43), substantially worse than DeComFL's least favorable items (which were all positive, 2.55–5.82). The paper has genuine strengths (generalized framework, consistent empirical improvement) that lift it above the 4.5 region, but the unresolved tension between the "Hessian-informed" framing and what H actually tracks, combined with the norm-mismatch in theoretical comparisons and the unsubstantiated well-approximated condition, prevent acceptance in current form.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>