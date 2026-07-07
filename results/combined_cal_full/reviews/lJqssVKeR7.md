Now I have a clear picture. Let me compile the final review.

## Summary

This paper proposes HiSo, a Hessian-informed zeroth-order federated optimization method that accelerates convergence by reusing the already-communicated global update Δx to build a diagonal preconditioner via EMA of squared elements, all while preserving scalar-only (dimension-free) communication. The paper contributes a generalized scalar-only FL framework decoupled from vanilla ZO-SGD, convergence analysis covering multiple local updates (τ > 1), and empirical results showing 1.4–5.4× speedup over DeComFL across LLM fine-tuning tasks (OPT-350M to OPT-2.7B on SST-2, QQP, SQuAD).

## Strengths

- **Clever reuse of already-communicated information to estimate curvature (Section 4.2).** The paper observes that the global aggregated update Δx is already needed for reconstruction in the scalar-only communication framework. Squaring its elements and applying EMA gives a free diagonal preconditioner — no extra communication or function evaluations. This is the paper's sharpest insight.

- **Consistent empirical improvement over DeComFL across all settings (Tables 2, 3).** HiSo beats DeComFL in both convergence speed (1.4–5.4× fewer rounds) and final accuracy on all 9 (model, task) configurations tested. The improvements are not dramatic but they are systematic, which is more credible than a big win on one cherry-picked setting.

- **The generalized scalar-only framework (Section 3.3, Algorithm 1).** Decoupling the dimension-free communication mechanism from the specific choice of ZO-SGD is a real contribution. It makes the framework extensible to other optimizer designs.

- **Extending convergence analysis to τ > 1 (Corollary 3).** DeComFL's theory only handles τ = 1 with the low-effective-rank assumption. HiSo's analysis covers multiple local updates, which is the practically relevant case. This is a genuine theoretical advance over the prior state of the art.

- **The paper is generally honest about limitations.** It acknowledges (line 285) that the well-approximated condition is hard to verify and that Theorem 1 does not require it. It also acknowledges (footnote 2) that the method resembles RMSProp. This candor is commendable.

## Weaknesses

### Major

1. **The theory's central "well-approximated" condition (Definition, Eq. 17) is not connected to the proposed update rule (Eq. 12).** The paper defines a well-approximate matrix H of Hessian Σ as one satisfying Tr(H^{-1/2}ΣH^{-1/2}) ≤ ζ (a dimension-independent quantity). The clean dimension-independent convergence rates in Corollaries 1–3 depend on this condition holding. However, the paper never shows — theoretically or empirically — that the EMA of squared global updates (Eq. 12) produces an H that satisfies this condition. The synthetic experiment (Fig. 4) tests whitening of a known Σ by an externally chosen H, not the recursive update rule (Eq. 12). The paper acknowledges this gap ("it is hard to determine if this approximation holds in the context of LLMs"), but this means the most eye-catching theoretical claims (dimension-independent rates) rest on an unverified assumption. This substantially weakens the theory section.

2. **The fallback claim that poor preconditioning "at worst case, degenerates into DeComFL" (line 285) is not justified.** A bad preconditioner can actively hurt convergence relative to identity preconditioning; the paper provides no theoretical or empirical support that performance cannot degrade below the DeComFL baseline. This claim, while intuitive in the sense that H ≈ I when no curvature structure is captured, is not proven.

### Minor

3. **The convergence metric in Theorem 1 is the preconditioned gradient norm ‖∇F(·)‖²_{H^{-1}}, not the standard gradient norm ‖∇F(·)‖².** When comparing with DeComFL (H=I) the norms coincide, so internal comparisons are valid. However, the paper does not remark on this distinction. Since ‖∇F(·)‖²_{H^{-1}} ≤ β_ℓ^{-1}‖∇F(·)‖² (by Assumption 4), the rates in Corollaries 1–3 are for a weaker metric than what is standard in ZO theory. This does not invalidate the results but should be explicitly discussed.

4. **Notation ambiguity for the Hessian update.** Line 140 writes H_{r+1} using per-client local Δx_{r,τ}^{(i)} after τ local steps, while Eq. 12 (line 174) uses the global aggregated Δx_{r,0}. The simplified τ=1 case (Section 4.3) follows the latter pattern. This ambiguity should be resolved with unambiguous pseudocode (currently deferred to Appendix D, which the parser has stripped).

5. **No comparison with adaptive ZO methods that require no extra communication.** Adding a ZO-SGD with momentum baseline would help isolate the benefit of Hessian-inspired preconditioning from any generic adaptive mechanism, clarifying what HiSo's specific contribution is.

6. **Small client count (6 total, 2 sampled per round).** While not required to run large-scale FL, the claims about "federated" applicability would be strengthened by at least a small sensitivity study with more clients (e.g., 20, 50) on one task.

### Trivial

None.

## Nice-to-Haves

- Provide empirical evidence connecting the learned H to the actual Hessian (e.g., on a small model where the true diagonal Hessian can be estimated via Hutchinson traces). This would bridge the gap between the well-approximated condition and the algorithm's behavior.
- Report full convergence curves (test accuracy vs. communication rounds) alongside Table 2's speedup numbers, so the reader can see the full trajectory rather than a single asymmetric comparison point.
- Analyze or at least discuss the memory overhead of storing H for billion-scale models (~2.6 GB in FP16 for 1.3B parameters). Consider whether H can be restricted to trainable parameters in a PEFT setup.
- Discuss the storage and reconstruction cost for clients that miss many rounds (the number of historical scalars grows linearly with missed rounds).

## Removed Points

These points were flagged by the harsh critic but are removed for the following reasons:
- *"Hessian-informed label is misleading — closer to RMSProp"*: The paper already addresses this in footnote 2 ("More accurately, our method resembles RMSProp as it currently is without a momentum term") and footnote 1 ("does not imply that we calculate the full Hessian matrix"). The paper is transparent about what it does.
- *"The step where (uᵀH⁻¹u)⁻¹ is absorbed into the learning rate is glossed over"*: This is a standard approximation for diagonal H that the paper explicitly mentions; it is not a flaw.
- *"Assumption 4 bounding H is doing heavy lifting without proof"*: The boundedness of H follows routinely from the EMA update's boundedness given bounded Δx, which is standard in adaptive method analysis.
- *Missing related works*: Excluded per policy (cannot be externally verified).
- *"The P=5 setting is stated but not justified"*: This is a standard detail in ZO literature.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the core strengths (clever reuse of communicated scalars, consistent empirical gains, generalization of the scalar-only framework) and surface the main weakness (the gap between the theoretical well-approximated condition and the actual update rule, which the paper partially acknowledges but does not resolve).

## Suggestions

1. Resolve the notation/algorithm-specification inconsistency between Hessian updates defined in Section 4.2 (line 140 vs Eq. 12) and provide unambiguous pseudocode.
2. Add a controlled experiment on a small model where the true diagonal Hessian can be estimated, to support the claim that Eq. 12 produces a meaningful Hessian approximation.
3. Replace or supplement Table 2's asymmetric speedup metric with full convergence curves. At minimum, add rounds-to-each-method's-own-convergence alongside the current matching metric.
4. Qualify the fallback claim about degenerating to DeComFL — either provide a proof sketch or soften it to a statement about empirical observations.
5. Discuss the memory overhead of storing H for billion-scale models.

## Score and Decision

**Calibration anchors used:**
| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| DeComFL (ZO-FL, dimension-free) | omrLHFzC37.md | 6.25 | R1/R2 | Yes | Foundational paper HiSo builds on. DeComFL's novelty was greater (first dimension-free FL), and its theory was cleaner (no unresolved well-approximated condition). HiSo extends DeComFL with a clever curvature reuse idea but has weaker theory. HiSo should score below 6.25. |
| HiZOO (Hessian-informed ZO, single-node) | bEqI61iBue.md | 5.67 | R1 | Yes | Shares similar Hessian estimation issues (estimator doesn't provably estimate Hessian). HiZOO is single-node; HiSo extends to FL with consistent empirical gains. Comparable quality, HiSo slightly below due to additional theory gaps. |
| FedAda2 (adaptive FL) | AbJWZp4THG.md | 5.00 | R1 | Yes | Weaker empirical results (marginal improvements). HiSo's empirical story is stronger (consistent improvement across all settings). HiSo should score above 5.00. |
| FedZOO (trajectory-informed ZO-FL) | ZAMoxm86KV.md | 3.67 | R1 | Yes | Different approach with fairness concerns in comparisons. Not directly comparable. |
| FeedSign (1-bit FL communication) | DJRd4IQHGQ.md | 5.25 | R2 | No | Another communication-efficient FL paper. HiSo's empirical results are more comprehensive. |
| FedDA (adaptive FL) | kjn99xFUF3.md | 6.00 | R2 | No | Clean theory, less relevant to ZO setting. |

**Round 1 bracket:** [5.0, 6.0]

**Weighted-item comparison:** My draft's heaviest positive items (+5.37 for τ>1 analysis, +4.38 for clever reuse of Δx) are comparable to HiZOO's strongest positives (+5.50 for interesting problem, +3.62 for convergence guarantee) and slightly weaker than DeComFL's (+7.80 for addressing important problem, +6.30 for novelty). My draft's strongest negatives (-4.50 for fallback claim, -2.87 for unverified well-approximated condition) are roughly comparable to DeComFL's (-4.59 for limited baselines, -4.28 for theory replication) but apply to the core theory rather than peripheral issues. The unverified well-approximated condition (-2.87 weight) is the main factor keeping this paper below DeComFL (6.25) and closer to HiZOO (5.67).

**Final score determination:** 5.5. The paper has a genuinely clever core idea and solid empirical results, placing it clearly above 5.0 (reject). However, the theory section's central assumption is unverified for the proposed algorithm, bringing it below DeComFL (6.25) and to a level comparable with HiZOO (5.67), which had analogous Hessian-estimation verification issues. The honest acknowledgment of limitations is positive but does not resolve the gap. A borderline-accept score reflects a solid contribution that would benefit from tightening the theory-experiment connection.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>