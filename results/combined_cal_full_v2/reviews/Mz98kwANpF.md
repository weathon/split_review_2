Now I have all the information I need. Let me write the final review.

## Summary

This paper challenges the prevailing multi-component paradigm for multi-task LoRA. It first conducts an empirical investigation showing that (1) a simplified multi-head variant (M-LoRA) with high inter-head similarity outperforms complex diversity-enforcing architectures, and (2) simply increasing the rank of a standard single-adapter LoRA matches or exceeds multi-component methods. Based on these insights, the paper proposes Align-LoRA, which adds an auxiliary KL-divergence (or MMD) loss to align task representations in the shared LoRA down-projection space, achieving consistent gains over baselines while preserving zero inference overhead.

## Strengths

- **The "increase rank" experiment (Section 4, Tables 2–3) is a clean, high-impact sanity check.** Reallocating the parameter budget of multi-component architectures into a single higher-rank LoRA adapter matches or nearly matches their performance across LLaMA2-7B/13B and Qwen2.5-7B/14B. This result genuinely calls into question whether the complexity of routed multi-head systems buys anything beyond extra parameters. This single experiment is a valuable contribution independent of the proposed method.

- **A-LoRA-K (KL-based alignment) achieves consistent and substantial gains across diverse settings.** On LLaMA3-8B evaluated on BBH (Table 4), A-LoRA-K reaches 48.84 vs. the next best (M-LoRA) at 45.35 — a 3.5-point gain using fewer trainable parameters. Improvements are replicated across model families (LLaMA2, LLaMA3, Qwen2.5) and scales (3B–14B), in both in-domain (8-task benchmark, Table 5) and OOD (BBH) settings.

- **Zero-inference-overhead property.** Unlike multi-component methods with dynamic routers that cannot be merged into the backbone, Align-LoRA introduces no additional modules and is fully mergeable — a genuine practical advantage for deployment.

- **The λ sensitivity analysis (Figure 3) is well executed.** It shows Align-LoRA outperforms baselines across a 50× range of λ values with a clear optimum and graceful degradation, addressing a common concern about auxiliary loss sensitivity.

## Weaknesses

### Major

- **Overclaiming about A-LoRA-M (MMD variant).** The paper repeatedly asserts that "both A-LoRA-K and A-LoRA-M significantly outperform the baselines" (Section 5.2, lines 225 and 251). This is contradicted by the paper's own data:
  - Table 4 (BBH): A-LoRA-M underperforms standard LoRA on Qwen2.5-7B (47.53 vs 48.36) and Qwen2.5-14B (52.24 vs 52.93).
  - Table 5 (8-task): A-LoRA-M underperforms M-LoRA on Qwen2.5-3B (78.35 vs 78.51) and Qwen2.5-7B (82.31 vs 82.46).
  
  Only the KL-based variant (A-LoRA-K) is consistently supported. The claim that "the principle of aligning representations is broadly applicable and not contingent on a single metric" (Section 5.1) is weaker than stated. The paper should either explain why MMD underperforms in these settings or qualify the central claim to the KL instantiation. This is a fixable error but needs to be addressed for the paper's evidential claims to be sound.

### Minor

- **No variance or significance reporting.** None of the tables include standard deviations or error bars, despite several claimed improvements being modest (e.g., A-LoRA-K vs M-LoRA on Qwen2.5-14B in Table 4: 55.11 vs 53.78, ~1.3 points; A-LoRA-M vs LoRA on LLaMA3-8B: 45.42 vs 44.89, ~0.5 points). Without multi-run statistics, it is impossible to assess whether these differences are meaningful. Multi-run evaluation with reported variance is standard for empirical PEFT papers.

- **Theoretical analysis is presented as novel but is a standard bound.** The generalization bound in Equation (5.3) is described as "a novel generalization bound for MTL" (Section 5.3) but is essentially the Ben-David et al. (2006) domain adaptation bound reformulated for the multi-task setting with no LoRA-specific analysis. The bound restates that minimizing distribution discrepancy tightens the bound, which follows directly from the method's design. Deferring the derivation to an appendix does not address this. Framing it as a "theoretical analysis" rather than a motivation for the alignment loss would be more accurate.

- **Gaussian assumption for KL divergence is unexamined.** The paper models task representations as multivariate Gaussians with diagonal covariance (Section 5.1) without justification or verification that the actual representations are approximately Gaussian. If the representations deviate substantially from this assumption, the KL value may be a poor proxy for alignment. A simple normality test or visualization would strengthen the methodological grounding.

- **Incomplete control for dropout attribution.** The claim that "multi-head dropout is the critical factor" (Section 3.3) for M-LoRA's success rests on comparing HydraLoRA w/o Router vs M-LoRA. Since HydraLoRA and R-LoRA (from which M-LoRA derives) use different head initialization schemes, the causal attribution to dropout specifically is not fully controlled. This does not invalidate the finding but weakens the mechanistic explanation.

### Trivial

None.

## Nice-to-Haves

- **Add a LoRA (rank 8) baseline on the same 5-task→BBH setup as Table 4.** The current comparison pits A-LoRA-K (rank 8, 0.20% params) against LoRA (rank 10, 0.25% params). While the existing comparison is arguably stronger evidence (A-LoRA-K wins with fewer parameters and lower rank), a rank-matched control would cleanly separate alignment effects from rank effects and make the core claim unassailable.

- **Include a brief discussion of the tension between alignment and task-specific adaptation.** If the A matrix is forced to produce similar representations for all tasks, what handles task-specific variation? The paper references Appendix I for this, but the main text would benefit from acknowledging this question explicitly.

## Removed Points

These points from the reviews are flagged to be removed; treat them with caution:

- **Criticism about the "paradox" framing being misleading**: The paper uses "paradox" to describe the finding that a high-similarity model contradicts the prevailing assumption that diversity is necessary. This is a reasonable framing relative to the existing literature — the paper's own explanation in Section 3.3 provides a clear mechanism for why this occurs. Removed as a matter of framing taste rather than a substantive flaw.
- **Criticism that M-LoRA is not accurately described as a "minimal ablation" of R-LoRA**: Removing the router is the only architectural change from R-LoRA. Describing this as minimal is factually accurate. Removed.
- **Criticism about a missing "R-LoRA w/o Router vs M-LoRA" comparison**: M-LoRA is defined as R-LoRA without the router, so this comparison would be between identical models. The criticism misunderstood the setup. Removed.
- **Criticism about table captions not specifying evaluation metrics and other formatting points**: These are parser artifacts or minor presentation preferences. Removed per filtering rules.
- **The missing controlled comparison (LoRA rank 8 vs A-LoRA-K)**: The critic acknowledges the existing comparison is arguably stronger evidence. Demoted to nice-to-have.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Correct the overclaiming about A-LoRA-M.** Qualify the central claim to the KL-based variant, or explain why the MMD variant underperforms in several settings (and whether this reveals something about the nature of the alignment needed). If the MMD results cannot be explained, consider moving them to an appendix.
2. **Add variance/confidence estimates** to all main result tables.
3. **Examine or discuss the Gaussian assumption** behind the KL-based alignment loss.
4. **Reframe the theoretical analysis** as a motivation for the alignment approach rather than claiming theoretical novelty.
5. **Add the rank-matched control** (LoRA rank 8 on the same 5-task setup) to fully isolate alignment effects from rank effects.

## Score and Decision

**Score: 6.0 — Borderline Accept**

**Decision: Accept** (contingent on addressing the overclaiming about A-LoRA-M)

**Calibration summary:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|---|
| UnoLoRA | 49ti6LOUw5.md | 3.00 | 1 | Yes | Very similar topic (single shared LoRA for MTL) but only tested on T5 with weak eval. Current paper is substantially stronger — tests on LLaMA2/3, Qwen2.5 (3B-14B), has the impactful "increase rank" experiment. |
| MORE | LWvgajBmNH.md | 4.00 | 1 | Yes | MoE LoRA for MTL. Limited novelty, only GLUE evaluated. Current paper has stronger empirical contribution and broader evaluation. |
| CoLoRA | jFcNXJGPGh.md | 6.00 | 2 | Yes | Competitive LoRA training. Mixed reviews (5/6/8/5). Current paper has cleaner motivation and more principled method, but also has the overclaiming issue. Comparable overall. |
| C-Poly | G1Hlubz1fR.md | 6.00 | 2 | Yes | Skill-based multi-task PEFT. Consistent 6/6/6/6. Current paper has a stronger empirical motivation story but similar-level weaknesses. |
| Partial Linearization | iynRvVVAmH.md | 7.00 | 1 | Yes | Multi-task LoRA fusion. Stronger evaluation across modalities, cleaner presentation. Current paper has a more compelling empirical investigation but weaker theory. |
| VeRA | NjNfLdxr3A.md | 7.25 | 2 | Yes | Vector-based random matrix adaptation. Very clean, high-quality paper. Current paper has a more complex narrative with fixable issues, placing it below this anchor. |

The paper's strongest items (increase-rank experiment weight 8.77, A-LoRA-K gains weight 10.07) are comparable to those of the 6.0–7.0 anchors. However, the overclaiming about A-LoRA-M and the lack of variance reporting are weaknesses not present to the same degree in the higher-scoring papers. Placing the paper at 6.0 positions it alongside CoLoRA and C-Poly — papers with genuine contributions and some fixable issues — and clearly above the 3–4 range reject papers that had substantially weaker evaluations.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>