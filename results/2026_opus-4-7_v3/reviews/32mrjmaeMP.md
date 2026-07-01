Now I have thoroughly read the paper. Let me draft the review before calibration.Now let me begin calibration. Round 1 — Bracketing:Now I have enough calibration data. Let me form my assessment.

**Round 1 Bracket:**

The most directly comparable accepted papers are:
- τJp (avg 6.0) — TAK's main baseline; TAK matches/beats it while being dataless, directly addressing τJp's key weakness (requiring all tasks' data)
- Attention-Only FT (avg 6.25) — TAK builds on this and adds principled regularization with stronger results
- MAP (avg 6.33) — model merging with quadratic approximation, accepted

Rejected papers in the domain: ATM (3.0, fundamental framing issues), SUPERMERGE (4.33, insufficient baselines), "Realistic Evaluation" (5.33, analysis paper). The paper under review has none of these flaws.

**Initial bracket: 6.0–7.5.** The paper clearly outperforms its two direct competitors (τJp, Attention-Only FT) which scored 6.0 and 6.25. Its weaknesses are bounded and non-fatal, but the non-linear regime overclaiming and limited model scale prevent it from reaching 8+.

Now I'll write the final consolidated review.

---

## Summary
This paper proposes TAK (Task Arithmetic with KFAC regularization), a dataless regularizer for improving weight disentanglement in task arithmetic. The key insight is that, under model linearization, representation drift reduces to a quadratic form in the Jacobian Gramian — an instance of the Generalized Gauss-Newton (GGN) matrix under squared loss — which can be efficiently approximated via Kronecker-Factored Approximate Curvature (KFAC). The method achieves state-of-the-art results in task addition and negation on standard benchmarks (CLIP, T5) while eliminating the need for other tasks' data, and proposes a merging heuristic yielding O(1) complexity in the number of tasks.

## Strengths

- **Novel theoretical bridge (Sections 3.1–3.2).** The identification of the Jacobian Gramian used for representation drift regularization as a special case of the GGN under squared loss (Section 3.2: "If we choose squared error… the GGN becomes the Jacobian Gram matrix exactly, since ∇²cₙ = I_C") is a genuinely novel conceptual connection that enables direct transfer of well-established KFAC machinery from optimization to task arithmetic. Each step in the chain (linearization → quadratic form → GGN → KFAC) is mathematically clean and well-justified.

- **Strong linearized regime results with α-robustness (Table 1, Figure 4a).** TAK matches or exceeds the data-dependent baseline τJp across all three CLIP backbones (e.g., 85.8 vs. 85.0 at α=1 on ViT-B/32; 91.6 vs. 90.9 on ViT-L/14) while being dataless. Figure 4a shows TAK maintains near-constant accuracy across α ∈ [0.3, 2.0], while all other methods (TIES, TSV, ISO) are highly sensitive — a practically valuable property that eliminates held-out tuning in this regime.

- **Task negation results (Table 2).** TAK achieves clearly stronger unlearning than all baselines (target accuracy 3.4–3.5 vs. τJp's 3.7–6.7 across three backbones) while maintaining comparable or better control accuracy (62.4 vs. 60.8 on ViT-B/32). Given that TAK is dataless while τJp requires ImageNet data, this is the paper's most practically compelling finding.

- **Thorough ablation battery.** The paper systematically examines data budget and MC samples (Figure 7a), KFAC compression strategies (Figure 7b), the gap between per-task and accumulated regularizers (Table 3), computational overhead (Figure 6), and step-wise application frequency (Figure 8). These ablations collectively paint a clear operational picture.

## Weaknesses

### Fatal
None

### Major
1. **Overclaimed α-robustness in the non-linear regime.** The abstract states TAK "eliminat[es] the need for held-out tuning" without qualification. This holds cleanly in the linearized regime (Figure 4a), but Table 1 shows TAK + Attention-Only FT at α=1 achieves 60.3%/59.0%/82.1% vs. best-α of 83.1%/84.3%/89.9% on ViT-B/32, B/16, L/14 — gaps of up to 25.3 absolute points. The paper does note "the choice of the α coefficient has a stronger impact" (Section 4), but the abstract's unqualified claim is misleading. Since the paper extends TAK to the non-linear regime and presents it as a key setting, readers may incorrectly believe the α-robustness property generalizes.

### Minor
1. **Kronecker-factor merging heuristic (Eq. 8) lacks error analysis.** The approximation replaces ∑λₜBₜ⊗Aₜ with (∑Bₜ)⊗(∑λₜAₜ), which is exact only in degenerate cases. Table 3 shows the empirical gap is small (~0.5 points on ViT-B/32, negligible on ViT-B/16 and T5), but there is no analysis of when this approximation would degrade — e.g., with highly heterogeneous task domains where activation statistics differ substantially. The asymmetric weighting (λ on A factors only, not B) is also unmotivated. Since the O(1) complexity claim is central to the paper's practical contribution, understanding failure modes matters.

2. **Limited theoretical grounding for non-linear extension.** The regularizer is derived under linearization (Eq. 1). The paper justifies non-linear use by pairing with Attention-Only FT, which "has been shown to induce approximately linear fine-tuning dynamics." The empirical results show TAK helps in this setting (Attention-Only FT improves from 78.2 to 83.1 at best α on ViT-B/32), but there is no analysis of *why* the regularizer remains effective when its derivation assumptions are only approximately satisfied. Even a brief empirical investigation (e.g., measuring how much the true representation drift deviates from the quadratic approximation under Attention-Only FT) would strengthen this extension.

3. **Unexplained MC sample behavior (Figure 7a).** Performance deteriorates and variance increases beyond 1–2 MC samples. The paper notes this is "surprising" but offers no explanation. Understanding whether this reflects implicit regularization from MC noise, curvature overestimation, or another mechanism would guide practitioners and deepen understanding of the method.

### Trivial
None

## Nice-to-Haves
- Quantitative OOD detection metrics (AUROC, FPR95) for the task localization finding (Figure 5), which is currently qualitative and could constitute a concrete secondary contribution.
- Discussion of β hyperparameter sensitivity in the main text; the regularization strength β (Eq. 7) is introduced but its selection procedure is not discussed.
- Evaluation on larger-scale models (e.g., ViT-G or larger LLMs) to test whether the KFAC approximation quality and merging heuristic hold at scale.
- Discussion of how TAK interacts with parameter-efficient fine-tuning (LoRA, adapters), explicitly scoped out as future work in the conclusions.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Circular reasoning" about non-linear regime.** The reviewer framed the Attention-Only FT justification as circular ("if Attention-Only FT already achieves approximate linearization, then the linearized regime should already be well-served by it alone, and the added value of TAK should be small"). This mischaracterizes the argument: Attention-Only FT provides approximate linearization of the fine-tuning *dynamics*, but does not itself regularize for weight disentanglement — TAK adds value by penalizing representation drift on top of the approximate linearity. The empirical improvement (78.2→83.1 on ViT-B/32) confirms the two are complementary, not redundant. Removed as factually wrong.

- **Language task gap with τJp.** TAK achieves 78.7 vs. τJp's 81.3 on T5-base, a 2.6-point gap. However, TAK is dataless while τJp requires access to all tasks' data during training. A 2.6-point cost for eliminating data dependency is a reasonable trade-off and is acknowledged by the paper ("textual domains may still benefit from even more accurate curvature estimation"). This is not a weakness — it is an expected consequence of the method's design constraints.

- **"Dataless" framing nuance.** The method requires 128–256 examples per task for KFAC computation (Figure 7a), but what is eliminated is access to *other tasks'* data during fine-tuning. The paper clarifies this in Section 3.1 ("after initial pre-computation — does not require further data access") and the distinction is consistent with the method's privacy/decentralization motivation. The terminology is appropriate for the setting.

- **Limited experimental scope.** CLIP ViT-B/32, B/16, L/14 and T5-base are standard benchmarks in the task arithmetic literature and match the experimental scope of the two direct competitor papers (τJp, Attention-Only FT). Broader evaluation would be nice (see Nice-to-Haves) but the current scope is sufficient for the claims.

## Novel Insights
The identification of the Jacobian Gramian as a special case of the GGN under squared loss is a genuinely novel conceptual bridge between two previously separate literatures — representation drift regularization in task arithmetic and curvature approximation in second-order optimization. This enables direct and principled transfer of KFAC machinery, transforming what would be an intractable P×P matrix computation into a practical, block-diagonal Kronecker-factored approximation. The emergent task localization property (Figure 5), where regularized task vectors produce cleanly separated normalcy scores for in- vs. out-of-distribution inputs, is an interesting finding that suggests curvature-aware regularization may have applications beyond task arithmetic, such as principled OOD detection.

## Suggestions
- Qualify the abstract's α-robustness claim to explicitly state it applies to the linearized regime, and acknowledge that the non-linear regime still requires coefficient tuning.
- Provide a brief error analysis or controlled experiment for the Kronecker merging heuristic (Eq. 8) with deliberately heterogeneous tasks to characterize failure modes.
- Investigate why M=1 MC samples is optimal — e.g., measure curvature estimate quality as a function of M to determine if MC noise provides implicit regularization.
- Report quantitative OOD detection metrics (AUROC) for the task localization finding to strengthen it as a secondary contribution.
- Motivate the asymmetric weighting in Eq. 8 (λ applied to A factors but not B factors).

## Score and Decision

**Anchor papers retrieved (all rounds):**

| Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| `5lUdTogEL3.md` (Clothing-Irrelevant L-ReID) | 1.0 | R1 | Unrelated; far weaker paper |
| `nSDOkm0SKo.md` (Financial News NN) | 1.0 | R1 | Unrelated; minimal research contribution |
| `gwZ90hFSL2.md` (Chinese NLP Humanoid) | 1.0 | R1 | Unrelated; pseudoscience-level |
| `lNtio1tdbL.md` (ATM: Alternating Tuning and Merging) | 3.0 | R1 | Task arithmetic but fundamental framing issues (merging vs. MTL); TAK is far stronger |
| `WM5G2NWSYC.md` (Projected Subnetworks) | 2.0 | R1 | Weak methodology; not competitive |
| `XVHXVdoV11.md` (Compatible Specialization) | 3.4 | R1 | Model merging but with limited evaluation; TAK is substantially stronger |
| `yx8bU8T5ZN.md` (Unified View Delta Params) | 2.33 | R1 | Weak paper; TAK far superior |
| `lIdc5DUplq.md` (SUPERMERGE) | 4.33 | R1 | Gradient-based merging; insufficient baselines and unclear motivation; TAK is stronger methodologically |
| `Bq3fEAGXUL.md` (Realistic Eval Model Merging) | 5.33 | R1 | Evaluation paper, not a method contribution; TAK offers a novel method with stronger results |
| `fvUVe2gJh0.md` (What Matters Merging at Scale) | 5.33 | R1 | Analysis paper, rejected; TAK has a concrete novel method |
| `4wuvmJRAU4.md` (Blind Shuffling Superposition) | 5.0 | R1 | Random mechanisms for interference reduction; TAK's principled curvature approach is stronger |
| `dj0TktJcVI.md` (Attention-Only FT) | 6.25 | R1 | Directly comparable accepted paper; TAK builds on this and adds principled regularization with stronger results |
| `1VwWi6zbxs.md` (τJp) | 6.0 | R1 | Directly comparable accepted paper; TAK matches/beats it while being dataless, addressing τJp's key weakness |
| `1v7SRWsYve.md` (MAP: Amortized Pareto Fronts) | 6.33 | R1 | Model merging with quadratic approximation; comparable quality level |
| `q3ztjJRQuJ.md` (Trust Region TA) | 5.75 | R1 | Task arithmetic in trust region; rejected; TAK has stronger theory and results |

**Round 1 bracket: 6.0–7.5.** The paper clearly outperforms its two most directly comparable accepted competitors (τJp at 6.0, Attention-Only FT at 6.25) in both methodology and results, while addressing key limitations of each. The weaknesses are bounded and non-fatal. No score-8+ anchors in this domain were found, and the paper's limitations (overclaimed α-robustness in non-linear regime, no error analysis on merging heuristic, limited model scale) prevent it from reaching that tier.

**Final calibration:** The paper makes a genuine methodological contribution with a novel theoretical bridge, achieves state-of-the-art results while being dataless, and provides thorough ablations. Its primary weakness (overclaimed α-robustness) is a framing issue rather than a methodological flaw. Compared to τJp (6.0) and Attention-Only FT (6.25), which it outperforms, and MAP (6.33), which operates in a similar quality tier, the paper deserves a score at or slightly above these anchors.

**Score: 7.0** — Accept. The paper makes a clean, novel contribution connecting representation drift regularization to curvature approximation, achieves strong empirical results while eliminating data dependency (a practical improvement over τJp), and provides thorough experimental validation. The weaknesses (non-linear regime overclaiming, missing error analysis on merging heuristic) are addressable in revision and do not undermine the core contribution.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>