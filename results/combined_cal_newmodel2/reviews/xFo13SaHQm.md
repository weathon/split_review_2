Now I have all the information needed for a calibrated final review. Let me write it.

## Summary

This paper identifies the "copy-paste" failure mode in identity-consistent image generation, where models replicate the reference face rather than generating the identity with natural variation. It makes three contributions: (1) MultiID-2M, a large-scale paired multi-ID dataset (500k group photos with references); (2) MultiID-Bench, a benchmark with the Copy-Paste (CP) metric that quantifies bias toward the reference versus ground truth; and (3) WithAnyone, a diffusion model trained with paired data and a contrastive ID loss to reduce copy-paste while maintaining identity fidelity. Results show WithAnyone achieves near-best scores on both Sim(GT) and CP, deviating from the trade-off curve observed across other methods.

## Strengths

- **Well-motivated problem.** The "copy-paste" failure mode is a genuine, underappreciated issue. The paper's observation (Section 1, Fig. 2) that real images of the same person vary substantially in face similarity (0.77 down to 0.30) while models like InstantID produce a sharp peak at 1.0 is compelling and correctly identifies a gap between what metrics reward and what users actually want.

- **Copy-Paste metric (Eq. 2) is well-designed.** The metric M_CP = (θ_gt − θ_gr) / θ_tr cleanly captures whether a generated image is biased toward the reference versus toward the ground-truth target, normalized by the natural angular distance between reference and GT. This addresses a real deficiency in prior work which primarily reported Sim(Ref) and thus implicitly rewarded copying.

- **Large-scale dataset effort.** MultiID-2M — 500k paired multi-ID images, 1.5M unpaired group photos, ~25k identities — is a substantial resource. The four-stage construction pipeline (single-ID collection, multi-ID retrieval via name queries, face matching, post-processing) is sensible and well-documented.

- **Ablation study is informative.** Table 3 cleanly isolates each component's contribution: Phase 3 (paired tuning) reduces CP from 0.239 to 0.161 while maintaining Sim(G) near 0.405; the GT-aligned ID loss improves Sim(G) from 0.385 (w/o GT-Align) to 0.405. These demonstrate each design choice contributes positively and in the intended direction.

## Weaknesses

### Fatal
None.

### Major

- **Sim(GT) as the primary identity metric has an unacknowledged limitation.** The paper rightly criticizes Sim(Ref) for rewarding copying, then adopts Sim(GT) as its primary metric. But Sim(GT) also has a fundamental issue: the GT image is one specific physical instantiation of the prompted scene. There exist infinitely many valid renderings that preserve identity and match the prompt but differ in low-level facial details (lighting, micro-expression, exact head angle). The paper never defines what the *correct* Sim(GT) for a given prompt should be, and implicitly treats higher Sim(GT) as uniformly better. While the CP metric (measuring relative bias toward ref vs GT) partially addresses this, the paper should acknowledge this limitation directly rather than replacing one imperfect proxy (Sim(Ref)) with another (Sim(GT)) without discussion.

### Minor

- **The claim of "breaking the trade-off" is overstated.** The paper uses "breaking the long-observed trade-off between fidelity and artifacts" in the Abstract, Introduction, and Conclusion. Table 1 shows WithAnyone achieves second-best on both Sim(GT) (0.460 vs. InstantID's 0.464) and CP (0.144 vs. OmniGen2's 0.142) — a strong Pareto point but not a qualitative discontinuity where the trade-off no longer applies. The trade-off still visibly exists across methods; WithAnyone occupies a better position on it. The paper's own Fig. 5 description ("Except for WithAnyone, all other models lie approximately on a fitted curve") supports "deviating from" or "improving," not "breaking." Calibrating to "substantially improving" or "achieving a superior Pareto point" would better match the evidence.

- **The ablation on extended negatives (Table 3) reveals an unacknowledged tension within the method.** Removing extended negatives (w/o Ext. Neg.) yields CP = 0.074 vs. the full model's CP = 0.161 — a ~2.2× increase in copy-paste artifacts from adding them. Extended negatives improve Sim(G) (0.368 → 0.405) but substantially worsen CP (0.074 → 0.161). The paper frames extended negatives as uniformly beneficial ("the effectiveness of ID contrastive loss is greatly reduced" without them) but does not discuss that they introduce a copy-paste trade-off at the within-method level. This should be acknowledged and discussed.

- **The user study is too weak to provide convincing evidence.** Only 10 participants were recruited for 230 groups of rankings. While the paper notes that statistical analysis is in Appendix H (stripped by the parser), a sample of 10 participants is small for making claims about "consistently achieving the highest average ranking across all dimensions." The evidence from this study is suggestive at best.

- **No dedicated discussion of limitations or failure cases.** There is no analysis of when WithAnyone fails — e.g., when identities are visually similar, when there are many people in the scene, or when reference and target differ dramatically in lighting or resolution. A limitations section would strengthen the paper.

- **No hyperparameter sensitivity analysis.** The loss weights λ_ID and λ_CL are both set to 0.1 across all phases without any study of how results change with these values. Given the ablation reveals a tension between CP and Sim(G) when changing negative pool size, the loss weights may also move along this frontier.

### Trivial
None.

## Nice-to-Haves

- Acknowledge the Sim(GT) limitation directly and discuss what it does and does not measure, plus how the CP metric partially compensates.
- Discuss the extended-negatives tension explicitly: why they increase CP and whether a better operating point exists.
- Expand the user study or present its findings more cautiously given the small sample size.
- Add hyperparameter sensitivity analysis for λ_ID and λ_CL.

## Removed Points

These points are flagged to be removed; treat them with caution:
1. **Criticism about "no statistical significance tests" in user study** — The paper states "Further details... are provided in Appendix H" including statistical analysis. Since the appendix was stripped by the parser, this claim cannot be verified, and the paper itself says such analysis exists.
2. **Criticism about garbled method names in Fig. 8** — This is a PDF parsing artifact, not a paper issue.
3. **Criticism about architecture description being thin in main text** — The paper explicitly refers to Fig. 4 and Appendix E. Main text space constraints are standard.
4. **Criticism about missing training compute details** — The paper cites Appendix F.1 for implementation details.
5. **Criticism about BU/PF/SC metrics undefined** — The paper states metrics are formally defined in Appendix D.

## Novel Insights

The most insightful observation from the review is the identification of the Sim(GT) limitation mirroring the very issue the paper diagnoses in prior work: the paper criticizes Sim(Ref) for being a flawed proxy that rewards copying, then adopts Sim(GT) as its primary metric without acknowledging that Sim(GT) is also a proxy — one that penalizes any valid variation from a particular ground-truth instantiation. The paper would be stronger if it explicitly framed its evaluation around *both* metrics (Sim(GT) and CP) as complementary signals rather than positioning Sim(GT) as the "correct" replacement.

## Suggestions

1. Calibrate the "breaking the trade-off" language throughout to better match the evidence (e.g., "deviating from the trade-off curve," "achieving a superior Pareto point").
2. Add a forthright discussion of what Sim(GT) does and does not measure, and how the CP metric partially addresses this.
3. Acknowledge and discuss the extended-negatives tension shown in the ablation; consider exploring whether a different negative pool size yields a better CP/Sim(G) operating point.
4. Add a dedicated limitations section covering failure cases and scope boundaries.
5. Include hyperparameter sensitivity analysis for the loss weights in the final version.

---

### Calibration Report

**All anchors retrieved:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `/home/.../NWvsm2VxAM.md` (ID-Booth) | 3.00 | R1 | Yes | Much weaker; limited novelty, marginal improvements. This paper has far more substance. |
| `/home/.../88Qm4fGWzX.md` (Event-Customized) | 5.00 | R1 | Yes | Weaker method novelty (combining existing techniques). This paper stronger. |
| `/home/.../vQxqcVGrhR.md` (DisEnvisioner) | 6.00 | R1 | Yes | Comparable quality; some overclaiming. This paper has similar strengths. |
| `/home/.../riieAeQBJm.md` (UIFace) | 6.00 | R1+R2 | Yes | Similar quality level. Solid contributions with minor issues. |
| `/home/.../ZkFMe3OPfw.md` (InstantPortrait) | 6.67 | R1 | Yes | Stronger visual results. This paper slightly below. |
| `/home/.../DblHBgD0GR.md` (Protective Perturbations) | 5.75 | R2 | No | Different topic, lower quality. |
| `/home/.../WNzy9bRDvG.md` (Consistency Models) | 7.00 | R2 | No | Different topic, higher quality. |
| `/home/.../FTpdQBoBd0.md` (Fine-tuning T2I) | 3.00 | R2 | No | Much weaker. |
| `/home/.../rH6IZIXqZG.md` (Diff Preference) | 4.67 | R2 | No | Weaker. |

**Round 1 bracket**: 5.0–6.5 (above Event-Customized at 5.0, comparable to DisEnvisioner/UIFace at 6.0, below InstantPortrait at 6.67).

**Final placement**: The paper's draft items show very high favorability on all strengths (12–13) and moderate favorability on most weaknesses (0.6–5.9), with only the user study at -2.72. This profile aligns most closely with DisEnvisioner (6.00) and UIFace (6.00), which had similar strength/weakness patterns. The paper has genuine contributions (problem identification, dataset, metric, method) that are well-supported, and its weaknesses are fixable presentation/scope issues rather than fatal flaws.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>