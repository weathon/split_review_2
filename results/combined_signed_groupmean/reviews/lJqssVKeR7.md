Now let me write the final consolidated review.

## Summary

This paper proposes HiSo, a method that integrates Hessian-informed preconditioning into zeroth-order (ZO) federated optimization while preserving scalar-only communication. It builds on the DeComFL framework by adding a global diagonal Hessian approximation estimated from squared ZO gradient updates, and provides a generalized scalar-only communication FL framework. The paper reports 1.4×–5.4× speedups over DeComFL on OPT model fine-tuning (125M–2.7B) and proves convergence rates that can be independent of dimension *d* and Lipschitz constant *L* under an unverified well-approximated Hessian condition.

## Strengths

- **Clean conceptual contribution (Section 3.3).** The observation that scalar-only communication does not require ZO-SGD specifically — only the ability to reconstruct updates from scalars — is a genuine insight. The generalized framework (Algorithm 1) cleanly separates the communication substrate from the optimization algorithm, and this abstraction is what enables HiSo to incorporate Hessian information without additional communication.

- **Consistent empirical improvement over DeComFL (Tables 2 and 3).** Across 3 models × 3 tasks, HiSo consistently uses fewer communication rounds to reach or exceed DeComFL's best accuracy, achieving 1.4×–5.4× speedup and 29%–80% communication savings. The trend is unambiguous, and the baseline (DeComFL) is the correct one for the paper's framing.

- **Theoretical analysis generalizes DeComFL (Corollaries 2 and 3).** Corollary 2 recovers DeComFL's rate as a special case (H_r = I), and Corollary 3 extends to τ > 1 local updates, which DeComFL's analysis did not handle. This is a genuine technical improvement.

## Weaknesses

### Major

- **Disconnect between "Hessian-informed" framing and actual algorithm.** The method constructs H via an EMA of squared ZO gradient estimates (Eq. 12) — essentially ZO-RMSProp — yet the paper's strongest theoretical claim (dimension-free convergence) depends on the "well-approximated condition" (Eq. 17), which requires H to be a good preconditioner for Σ (the actual Hessian). The paper provides no evidence that HiSo's learned H satisfies this condition. The simulation in Fig. 4 uses an idealized H = Diag(Σ+ε), not HiSo's learned H. While the paper acknowledges this limitation (line 285: "Although it is hard to determine if this approximation holds in the context of LLMs"), the headline theoretical result remains a conditional claim whose antecedent is unverified. This gap undermines the paper's core advertised contribution.

- **Missing comparison against the most practical competitor for communication-efficient LLM fine-tuning — PEFT methods like LoRA — in the main experimental tables.** Tables 2 and 3 compare only against full-parameter first-order methods (where TB vs KB savings are trivially large) and other ZO methods. While the paper mentions FL+PEFT baselines in Appendix E (line 347), their absence from the central narrative means a practitioner reading the main paper cannot evaluate where HiSo sits relative to LoRA on the accuracy-communication Pareto frontier — the most natural decision point for the claimed application.

### Minor

- **Notation inconsistency in the Hessian update rule.** Line 140 uses |Δx_{r,τ}^{(i)}|^2 (all local steps), while line 174 / Eq. (12) uses [Δx_{r,0}]^2 (first step only). This ambiguity affects reproducibility.

- **The parameter P = 5 (line 301) is never defined.** If P refers to the number of function evaluations per ZO gradient estimate (a multi-point estimator), this matters for understanding the computational cost trade-off.

- **The number of local update steps τ is not explicitly specified for the LLM experiments** beyond the simplified τ = 1 presentation (line 182).

- **No convergence curves are shown for the main LLM fine-tuning experiments** (Tables 2, 3 only provide endpoint results). Convergence trajectories would help illustrate the claimed acceleration.

- **The FL setting uses only 6 clients with 2 sampled per round** — a very small configuration. Scalability to larger client pools is not examined.

- **Table 1's bound of "2d" under L-smoothness for E||z||^2_Σ** is given as a "safety factor" rather than derived from the stated assumptions, which weakens the theoretical tightness.

## Nice-to-Haves

- A direct estimate (even on a small model) of whether HiSo's learned H actually reduces the whitening rank ζ during training, to bridge the theory-practice gap.
- Including FL+LoRA in the main comparison would make the paper's practical significance assessment complete.
- Reporting wall-clock time alongside communication cost would clarify the real-world trade-off between ZO computation and communication savings.

## Removed Points

The following points from the harsh review were excluded per the filtering rules:
- **Lack of wall-clock/compute time comparisons**: The paper states Appendix E contains computation time analysis. Per the hard rule about stripped appendices, this criticism is removed.
- **Missing statistical significance testing**: Generic criticism, removed per soft rules.
- **Section 4.1 derivation being "unnecessary window dressing"**: A stylistic opinion about presentation rather than a substantive flaw.
- **"90 million times communication savings" being a "framing artifact"**: While true that any communication-efficient method would show massive savings against full FedAvg, this is a factual statement about the method's properties, not a weakness the authors need to address.
- **Missing related works**: Per hard rules, removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Recalibrate the framing.** The term "Hessian-informed" over-promises relative to what the method actually does (squared-gradient diagonal preconditioning). Consider renaming to something like "adaptive ZO preconditioning" or acknowledging the RMSProp connection more prominently in the title/abstract.
2. **Bridge theory and practice.** Even a coarse estimate of Tr(H_r^{-1/2} Σ H_r^{-1/2}) during training on a small model would connect the well-approximated condition to the actual algorithm.
3. **Move FL+LoRA into the main comparison.** This is the most natural competitor for the claimed application, and its current relegation to the appendix weakens the paper's practical case.
4. **Show convergence curves** for the LLM experiments to visually demonstrate the claimed acceleration.
5. **Define P and specify τ** for all experimental configurations.

## Score and Decision

All calibration anchors:

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| /home/.../omrLHFzC37.md (DeComFL) | 6.25 | R1-Q4, R2-Q2 | Yes | Primary baseline — HiSo builds on this but adds a Hessian component with weaker theoretical grounding |
| /home/.../DJRd4IQHGQ.md (FeedSign) | 5.25 | R2 | Yes | Similar ZO-based FL fine-tuning paper; rejected due to overclaimed benefits and technical gaps |
| /home/.../ZU42Wrcqfm.md (FedSMU) | 5.75 | R1-Q4 | Yes | Communication-efficient FL with sign-based compression; rejected for novelty concerns |
| /home/.../Oqk1Ui6m0n.md (HF-NGD) | 5.00 | R1-Q3 | Yes | Hessian approximation in non-FL setting; rejected due to flawed lemma |
| /home/.../IsHWcsk4Fz.md (FedADM) | 3.00 | R1-Q2 | No | Lower-quality adaptive FL paper |
| /home/.../jkhVrIllKg.md (SABER) | 4.25 | R2-Q1 | No | FL under heterogeneity |
| /home/.../L9eEfwwUwU.md (SAFL) | 4.50 | R2-Q1 | No | Sketched adaptive FL |
| /home/.../AbJWZp4THG.md (FedAda²) | 5.00 | R2-Q1 | No | Efficient adaptive FL |

**Round 1 bracket:** 4.0–6.0. The paper has real contributions (generalized framework, consistent empirical gains, extended theory) that place it well above strong-reject territory, but significant weaknesses (theory-practice disconnect, missing key baselines) keep it below clear-accept quality.

**Round 2 narrowing:** Comparing impact-scored items against the closest anchors: HiSo shares DeComFL's strong empirical results (impact +10.00) and FeedSign's type of overclaiming gap (impact -10.00). DeComFL (6.25) and FeedSign (5.25) bracket the space. HiSo's two major weaknesses each carry impact scores near -10.00, comparable to the most severe weaknesses in these anchors. On balance, HiSo falls below its primary baseline DeComFL and near FeedSign, giving a final score of 5.0.

**Calibration justification:** My draft's two major weaknesses scored -10.00 and -9.99, both near-decisive pulls downward; the three strengths scored +9.93, +10.00, +10.00, all near-decisive pushes upward. This polar opposition is characteristic of borderline papers (avg 4–6 in this corpus), where net judgment depends on whether the core claim survives its most serious challenge. Here the core theoretical claim (dimension-free convergence) depends on an unverified condition that is not plausibly connected to the actual algorithm — the weakness strikes at the paper's advertised contribution, giving it decisive weight despite the real empirical gains.

**MY FINAL SCORE:** <score>5.0</score>
**MY FINAL DECISION:** <decision>Reject</decision>