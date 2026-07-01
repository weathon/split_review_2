## Summary

This paper proposes HiSo, a method that extends Hessian-informed zeroth-order (ZO) optimization to federated learning (FL) while preserving scalar-only (dimension-free) communication. The key idea is to learn a global diagonal preconditioner from the scalar updates already being transmitted for model reconstruction in ZO-FL, avoiding any extra communication of second-order information. The paper contributes: (1) a generalized scalar-only FL framework decoupled from ZO-SGD, (2) the HiSo algorithm combining Hessian-informed ZO steps with dimension-free communication, (3) convergence theory covering multiple local updates (τ > 1, an open gap in prior work), and (4) empirical results showing 1.4–5.4× speedup over the state-of-the-art ZO-FL baseline (DeComFL) across LLM fine-tuning tasks.

## Strengths

1. **Clean, well-motivated resolution of a genuine tension.** The paper identifies that Hessian information could accelerate ZO-FL convergence, but transmitting it would reintroduce the dimensionality cost that ZO methods were designed to avoid. The resolution — using the scalar updates *already being transmitted* for model reconstruction to build a preconditioner — is clever and practically motivated (Section 4.2, Eq. 12, discussion at lines 138–141).

2. **Generalized scalar-only framework (Algorithm 1).** The observation that DeComFL's dimension-free communication does not depend on the specific choice of ZO-SGD but on the use of scalar representations is a useful abstraction. Algorithm 1 genuinely generalizes prior art and separates the communication mechanism from the optimization strategy (Section 3.3).

3. **Strong empirical results against the direct ZO baseline.** Table 2 shows a clear and consistent 1.4–5.4× speedup in rounds and 29–80% communication savings over DeComFL across model sizes (OPT-350M to 2.7B) and tasks (SST-2, QQP, SQuAD). HiSo matches or exceeds DeComFL's final accuracy across all settings.

4. **First convergence theory for ZO-FL with multiple local updates (τ > 1).** DeComFL could not provide convergence guarantees for τ > 1 under the low-effective rank assumption. HiSo fills this gap (Corollaries 1–3), and the rate that can become independent of d and L under the well-approximated condition is a genuine theoretical step for the sub-field.

## Weaknesses

### Fatal
None.

### Major

1. **The Hessian approximation heuristic (|Δx|² accumulation) is gradient-squared accumulation, and its connection to the true Hessian diagonal is not established.** The paper's headline convergence acceleration (Corollaries 1–3) relies on the "well-approximated condition" (Definition, Eq. 17), which assumes the learned diagonal matrix H accurately approximates the Hessian Σ. However, the update rule `H_{r+1} = (1−ν)H_r + ν·(1/m) Σ_i Diag(|Δx|² + εI)` accumulates squared ZO gradient estimates — the paper itself acknowledges this "resembles RMSProp" (footnote 2). The gap between this heuristic and the Hessian diagonal is not bridged theoretically or empirically (no comparison between learned H and the true Hessian is provided for any model). The paper is candid about this limitation (line 285: "it is hard to determine if this approximation holds in the context of LLMs"), but this means the claimed dimension-free convergence rates are conditional on an unverified assumption. **Crucially, this does not invalidate the paper's core empirical contribution** — HiSo's practical acceleration over DeComFL is demonstrated independently, and Theorem 1 itself does not require the condition. The contribution is narrower than the presentation suggests.

### Minor

2. **Inconsistent Hessian update specification.** The Hessian update is stated with different indexing across two locations: line 140 uses `Δx_{r,τ}^{(i)}` (client i's last local step) while Eq. 12 uses `Δx_{r,0}` (first local step/global update). These differ when τ > 1, creating ambiguity for reproducibility.

3. **The "up to 90 million times communication savings" claim (line 28) is not fully supported by the data in Table 3.** The largest ratio between first-order methods and HiSo in the table is ~33.5 million (OPT-350M, SST-2). The 90 million figure may derive from a different computation (e.g., comparing to FedZO at ~96 million), but the paper explicitly states "compared to first-order baselines." This is an overstatement.

4. **Undefined notation.** (a) `P = 5` is stated (line 301) but P is never defined. (b) `m` and `S_r` appear in Eq. 12 and line 140 without definition; from context they are |C_r| and the client set, but this should be explicit. These are small fixes but affect reproducibility.

5. **No conclusion or discussion section.** The paper ends abruptly after Section 6 (Experiments). A discussion addressing limitations, the gap between theory and practice regarding the well-approximated condition, and potential extensions would strengthen the paper.

### Trivial
None.

## Nice-to-Haves

- **FL+LoRA comparison is deferred to the appendix** (line 347). Including at least one LoRA-based FL baseline in the main paper would help practitioners contextualize HiSo against the dominant PEFT paradigm in communication-efficient LLM fine-tuning.
- **Small FL setup.** Using 6 clients (2 sampled per round) limits generality. Testing with larger client populations would strengthen the empirical findings, though the paper does not claim scalability beyond this setting.
- **No ablation of local steps τ.** The theory (Corollary 3) shows a non-monotonic dependence on τ, but experiments fix τ implicitly; understanding HiSo's behavior with larger τ would be practically informative.
- **No wall-clock comparison.** The paper focuses on communication rounds but does not report computational overhead (e.g., the cost of sampling from `𝒩(0, H^{-1})` vs. `𝒩(0, I)`).

## Removed Points

These points were flagged by the reviewer but are removed from the main weaknesses:

- **Model-reset mechanism concern.** Removed because the model-reset mechanism is inherited from DeComFL and is standard in this ZO-FL paradigm — clients start from the global model each round, which is how FL generally operates. This is not a weakness specific to HiSo.
- **"Well-approximated condition is circular."** The core concern (unverified connection between heuristic and Hessian) is retained as a Major weakness above. However, calling the condition "circular" overstates the issue: the condition is a standard theoretical assumption (analogous to smoothness), and the paper explicitly acknowledges it may not hold in practice (line 285). Theorem 1 does not require it.
- **"Non-standard convergence metric" (‖∇F‖²_{H_r^{-1}}).** This is the natural metric for preconditioned methods and the paper explains it. Removed.
- **Missing related work concerns.** Removed per guidelines (no external verification possible).
- **Formatting/presentation nitpicks.** Removed per guidelines (parser artifacts, not author errors).

## Novel Insights

None beyond the paper's own contributions. The reviewer's most insightful observation is the structural gap between the RMSProp-style |Δx|² accumulation and the Hessian-informed framing — a gap the paper partially acknowledges but does not fully address. The suggestion to either verify the Hessian connection or reframe the method as "adaptive per-coordinate ZO-FL" is constructive and specific.

## Suggestions

1. **Either justify the Hessian approximation or reframe the method.** Provide a theoretical argument connecting the |Δx|² accumulation to the diagonal Hessian (under specific loss assumptions), or add an empirical comparison between learned H and the true Hessian diagonal for at least one checkpoint. Alternatively, reframe the method as "adaptive per-coordinate ZO-FL" (RMSProp-style) and adjust the theoretical claims accordingly.
2. **Resolve the Hessian update inconsistency** between line 140 and Eq. 12, and define P, m, and S_r explicitly.
3. **Correct or clarify the "90 million times" claim** to match the data presented in Table 3.
4. **Add a conclusion/discussion section** addressing the gap between theory and practice regarding the well-approximated condition, and discussing limitations.
5. **Consider adding a FL+LoRA baseline** (from Appendix E) to the main comparison table.

## Score and Decision

### Calibration

**Round 1 bracket (5.0 – 6.5):** I compared the paper against human-scored anchors retrieved via topic-matched searches over the calibration corpus.

| Anchor | Path | Avg Score | Round | Comparison |
|--------|------|-----------|-------|------------|
| DeComFL (dimension-free ZO-FL) | omrLHFzC37 | 6.25 (5,6,6,8) — **Accepted** | 1,2 | Foundational ZO-FL paper. HiSo extends it with Hessian-informed preconditioning and τ>1 theory but has a weaker justification for its core mechanism. |
| HiZOO (single-node Hessian-informed ZO) | bEqI61iBue | 5.67 (6,5,6) — **Accepted** | 2 | Directly comparable: single-node precursor with similar Hessian-connection concerns. HiSo adds FL adaptation and τ>1 theory. |
| FeedSign (1-bit ZO FL) | DJRd4IQHGQ | 5.25 (5,5,5,6) — **Rejected** | 1 | Also ZO-based FL with extreme compression; rejected primarily for lack of novelty. HiSo has more novelty. |
| FZooS (ZO FL, surrogate gradients) | ZAMoxm86KV | 3.67 (5,3,3) — **Rejected** | 1 | More fundamental issues (computation cost, partial participation gaps). HiSo is substantially stronger. |
| Efficient Adaptive FL (FedAda²) | AbJWZp4THG | 5.00 (8,3,3,6) — **Rejected** | 2 | Communication-efficient adaptive FL, different approach. Comparable score tier. |
| SABER (second-order FL) | jkhVrIllKg | 4.25 (5,6,3,3) — **Rejected** | 2 | Second-order FL but different approach and weaker results. |

**Narrowing:** The paper's closest anchors are DeComFL (6.25, accepted) and HiZOO (5.67, accepted). HiSo is incremental over DeComFL but with clear additional contributions; however, the Hessian-connection gap is a more significant weakness than either anchor faced. The paper's empirical results are strong, the generalized framework is useful, and the τ > 1 theory fills a real gap. Balancing these factors positions HiSo slightly below DeComFL and roughly at the HiZOO level.

**Final score: 5.5.** This reflects a paper with genuine contributions and solid empirical evidence, held back from a higher score by the gap between the Hessian-informed framing and the RMSProp-style heuristic actually used — an issue the paper acknowledges but does not resolve.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>