**Round 1 bracket: 5.5–7.0**

The most relevant anchors:
- `zLHP6QDWYp` (avg 3.80, reject): LTSSL + logit adjustment, dual-stage post-hoc approach, rejected for weak writing, limited novelty, and insufficient experiments. CoLA is clearly superior in scope, ablation quality, and baselines.
- `OeKp3AdiVO` (avg 6.25, accept): Long-tailed logit retargeting with theoretical analysis, SOTA on multiple datasets, clean ablations. Comparable in scope to CoLA; CoLA has more breadth (semi-supervised setting + 5 distributions × 4 benchmarks).
- `II81zQUS1x` (avg 5.67, accept): Multiplicative logit adjustment theory for long-tail. Comparable theoretical depth; CoLA has stronger empirical coverage.

CoLA sits above the 3.8 reject (more principled, broader baselines, better ablation) and is at least comparable to the 6.25 accept. The Table 1 bolding error is real but does not undermine the core contribution—CoLA wins 4/5 CIFAR-10-LT distributions, all 5 CIFAR-100-LT distributions, STL-10-LT, and SIN-127. The minor weaknesses (linear LA not ablated, LCGC missing) are standard-level fixable issues. Final score: **6.0**.

---

## Summary
CoLA is a framework for Long-Tailed Semi-Supervised Learning (LTSSL) that co-designs two components of Logit Adjustment (LA): (1) De-Duplicated Distribution Estimation (DDDE) uses the effective rank of class representations to produce a redundancy-aware class-frequency estimate, addressing head-class over-suppression; (2) Logit Meta-Calibration (LMC) meta-learns the overall adjustment strength τ on a proxy validation set matched to the estimated distribution. The method is supported by a generalization bound, validated on CIFAR-10/100-LT, STL-10-LT, and SIN-127 against a broad set of baselines, and ablated with unusually clean design.

## Strengths
- **Figure 1b is a concrete, actionable insight**: The finding that optimal τ is non-monotone in γ_l (on CIFAR-10-LT, optimal τ for γ_l=100 exceeds that for γ_l=150) is a novel empirical observation that directly motivates the LMC design and distinguishes this work from prior fixed-τ LA methods.
- **Ablation design is unusually rigorous**: Table 4 isolates DDDE and LMC with a three-way comparison (fixed-τ, LMC-only without DDDE, and full system), confirming bidirectional interaction. Table 5 provides a direct L₂-distance comparison of DDDE against MCA and NWGMA alternatives, giving independent evidence for the distribution estimation component.
- **CIFAR-100-LT results are strong**: CoLA surpasses runner-up by more than 1 percentage point across nearly all five distributions on CIFAR-100-LT, with the improvement consistent rather than cherry-picked.
- **Evaluation breadth is above average for LTSSL**: Four benchmarks, five unlabeled distribution types, and up to 20 independent runs per distribution (4 settings × 5 seeds) with variance estimates. The SIN-127 large-scale results (Table 3: 24.18 vs. 23.66 for ABC at 32×32; 37.49 vs. 36.28 for ACR at 64×64) extend coverage to a more challenging setting.

## Weaknesses

### Fatal
None.

### Major
- **Table 1 bolding error on CIFAR-10-LT CON undermines the headline claim**: ADSH (a resampling method) reports 83.35±3.86 in the CON column while CoLA reports 81.87±2.70, yet CoLA is bolded as best. The paper explicitly states "CoLA achieves the highest accuracy across all five distributions on both CIFAR-10-LT and CIFAR-100-LT datasets" (Section 6.2.1). This is directly contradicted for CIFAR-10-LT CON. The discrepancy should be explained: ADSH collapses on other distributions (REV: 68.09, MID: 65.45), so the CIFAR-10-LT CON number likely reflects ADSH's specialization in the consistent setting, while CoLA is uniformly strong. If so, the paper should clarify this and either correct the SOTA claim or explicitly argue that uniform cross-distribution superiority is the criterion — not per-column maximality.

### Minor
- **Linear LA functional form not isolated in ablation**: Section 4.2 adopts −τ·**p** (linear in class probability) instead of the standard −τ·log **p**̂, citing Mor & Carmon (2025). Table 4 compares LMC against fixed-τ variants using empirical frequency (not log-space LA) but does not include a variant with fixed τ and linear LA form. It is therefore unclear whether the improvement of LMC over fixed-τ baselines is attributable to the meta-learned τ, the change in functional form, or both.
- **LCGC absent from comparison tables**: Section 2 describes LCGC (Xing et al., 2025) as providing a theoretical foundation for LA in LTSSL and positions it as a peer method, yet it does not appear in Tables 1–3. No explanation for its exclusion is given in the main text.
- **Warm-up phase sensitivity not discussed**: Section 4.3 describes an initial warm-up phase where τ is configured according to ACR before LMC takes over. No ablation or sensitivity analysis is provided for the warm-up duration or for ACR's design choices that this phase inherits.

### Trivial
None.

## Nice-to-Haves
- A visualization showing how the meta-learned τ* varies across the five unlabeled distributions (consistent, reversed, uniform, middle, head-tail) would make the co-design story quantitatively vivid rather than implicit in ablation tables.
- A simple controlled experiment demonstrating that erank tracks visual diversity better than naive frequency for classes sampled at varying redundancy levels would strengthen the DDDE mechanism story beyond the indirect L₂ evidence in Table 5.
- A brief discussion of when DDDE's estimation diverges from ground truth (e.g., during warm-up when m_y is small for tail classes) would help practitioners understand the method's limitations.

## Removed Points
*These points are flagged as removed; treat with caution.*

- **"Effective rank to effective sample size connection is informal"** (originally framed as evidential gap): The paper explicitly states DDDE is "inspired by" Cui et al.'s effective number, not that it is the same quantity. The paper validates it empirically in Table 5 (lowest L₂ distance). For an empirical methods paper, this framing is appropriate; the concern about small-m_y tail behavior is speculative and not observed to cause failures. Removed.
- **"Proposition 1 is standard importance-weighted bound"**: The paper itself acknowledges this ("general to many domain adaptation scenarios") and highlights the convexity result in the appendix as its specific contribution. Criticizing a bound for generality that the authors explicitly acknowledge is not a weakness. Removed.
- **"B constant could be large when DDDE underestimates"**: This is speculative; Table 5 empirically shows DDDE produces the smallest distribution error among alternatives. Not verifiable as a flaw from the paper as written. Removed.
- **"Table 3 missing baselines (Meta-Expert, CPE)"**: No evidence is provided that these outperform CoLA on SIN-127; they may simply not be evaluated in the SIN-127 setting in prior work. Removed per hard rules.
- **Warm-up dependency on ACR as "inherited design choices"**: Framed originally as a structural issue; downgraded to Minor (warm-up sensitivity) and the "structural" framing removed.

## Novel Insights
The co-design framing is the paper's most conceptually significant contribution: prior work treats class-wise and overall LA adjustments independently, but CoLA demonstrates empirically that accurate class-wise estimation is a prerequisite for reliable overall adjustment learning, and that the interaction runs in both directions (Table 4). The finding in Figure 1b — that optimal τ is non-monotone in γ_l — is counterintuitive and previously unacknowledged in the LTSSL literature. The use of effective rank as a redundancy-aware proxy for unlabeled class prevalence is novel and practically motivated, with direct empirical validation against frequency-based and geometric-mean alternatives.

## Suggestions
1. Correct or explicitly explain the ADSH vs. CoLA bolding in Table 1 CON column for CIFAR-10-LT; revise the "highest accuracy across all five distributions" claim for CIFAR-10-LT if necessary.
2. Add one variant to Table 4 using a fixed τ with the linear LA form (−τ·**p**) to separate the functional form change from the meta-learning contribution.
3. Include a brief explanation in the main text for LCGC's absence from the comparison tables.

## Score and Decision

**Anchors retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| zLHP6QDWYp | 3.80 | 1 | Related LTSSL + logit adjustment paper, rejected for limited novelty and weak experiments; CoLA is substantially stronger |
| SRn2o3ij25 | 4.67 | 1 | Long-tail recognition with implicit knowledge, rejected |
| BLvCdxAi8W | 4.25 | 1 | Long-tail recognition via granularity; different approach, comparable contribution quality |
| BUDxvMRkc4 | 4.67 | 1 | Long-tail with CLIP guidance; similar tier |
| OeKp3AdiVO | 6.25 | 1 | Long-tailed logit retargeting, accepted; comparable in rigor and breadth |
| u1yvEwYfK9 | 5.67 | 1 | Label shift correction for long-tail; theoretical approach, rejected |
| II81zQUS1x | 5.67 | 1 | Multiplicative logit adjustment theory for long-tail, accepted; CoLA has more empirical coverage |
| Agx4RXuYUJ | 6.00 | 1 | Temperature scaling for multi-label logit distillation; borderline accept |
| 25kAzqzTrz | 8.00 | 1 | Theoretical analysis of FixMatch; stronger theoretical contribution |
| RvUVMjfp8i | 8.00 | 1 | Evaluation of SSL in open environments; broader scope |

**Round 1 bracket: 5.5–7.0**

CoLA clearly sits above the 3.8 reject (zLHP6QDWYp) given its principled design, broader baselines, rigorous ablation, and consistent SOTA results across 4 benchmarks. It is comparable to the 6.25 accept (OeKp3AdiVO) and 5.67 accept (II81zQUS1x) in rigor and empirical strength. The Table 1 bolding error is a real and notable issue that needs correction, but it does not invalidate the overall contribution since CoLA genuinely outperforms on 4/5 CIFAR-10-LT distributions, all 5 CIFAR-100-LT distributions, and both other benchmarks. The minor weaknesses (linear LA term not ablated, LCGC absent, warm-up not analyzed) are standard-level fixable issues. This places the paper at **6.0** — a borderline accept, primarily constrained by the Table 1 issue and the non-ablated functional form change.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>