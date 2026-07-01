Now I have all the calibration data I need. Let me produce the final review.

**Calibration Analysis:**
- **Strong Reject (<1.5):** None of the retrieved papers in this band are remotely relevant — they are near-nonsensical or off-topic submissions. PIRN is clearly far above this.
- **Reject band (1.5–3.5):** CLIP-LAD (3.0, rejected) — criticized for limited novelty, unfair comparison, and simple combination of existing techniques. PIRN is substantially stronger in method design, experimental scope, and evaluation fairness.
- **Borderline band (3.5–5.5):** PTAD (4.25, rejected) — prototype-based AD with OT, similar technique mix. PTAD was criticized for reproducibility issues, missing variance, and complexity. PIRN shares the variance gap but has clearer motivation, more thorough ablation, and a convincing efficiency advantage.
- **Accept band (5.5–7.5):** H-PAD (5.6, accepted) — prototype-based time-series AD, accepted despite writing and detail issues. One-for-All Few-Shot AD (6.4, accepted) — introduced a new task paradigm but had missing baselines and ablation concerns. PIRN has comparable experimental rigor and more datasets.
- **Strong Accept (>7.5):** Papers at 8.0 have cleaner methodology, stronger novelty, and no unresolved evidential gaps. PIRN is not at this level.

**Round 1 bracket: 4.5–6.5.**

**Narrowing:** PIRN's core method is well-motivated, ablations are thorough, and the efficiency result is a genuine advantage. The two main weaknesses (FIND omission, no variance reporting) are real but addressable. Against H-PAD (5.6, accepted) and PTAD (4.25, rejected), PIRN sits closer to the accept band. **Final score: 5.5, Decision: Accept** (with revisions to address the major issues).

---

## Summary

The paper proposes PIRN, a prototype-driven reconstruction framework for few-shot multimodal anomaly detection (MAD). It combines three components: Balanced Prototype Assignment (BPA) using optimal transport to prevent codebook collapse, Adaptive Prototype Refinement (APR) for test-time prototype updates, and Multimodal Normality Communication (MNC) for cross-modal knowledge transfer. Evaluated on MVTec-3D-AD, Eyecandies, and Real-IAD D3, the method shows consistent gains over baselines and a substantial computational efficiency advantage.

## Strengths

- **Well-motivated problem framing.** The paper concretely explains why both cross-modal alignment and memory-bank approaches fail in the few-shot regime (Section 1), tying each failure mode directly to the proposed solution.
- **Each component targets a specific failure mode.** BPA addresses codebook collapse, APR addresses static coverage of normality, and MNC addresses modality isolation. This logical coupling between problem and design is clear and principled.
- **Consistent and non-trivial gains across few-shot settings.** On MVTec-3D-AD and Eyecandies (Table 1), PIRN outperforms all listed baselines at 5, 10, and 50 shots across all metrics. The gains over the strongest included baseline (INP-Former) are 3–4 points AUROC_I, which is practically meaningful.
- **Computational efficiency is a genuine practical advantage.** Table 4 shows PIRN achieving the best accuracy while using 85% fewer FLOPs and running 4.35× faster than FIND, a significant advantage for deployment.
- **Ablations confirm each module's contribution.** Tables 2, 3, 5, 6, and 7 systematically validate that removing each component or varying key hyperparameters degrades performance in the expected direction.

## Weaknesses

### Major

1. **FIND (the SOTA baseline) is excluded from the main results table, and the accuracy advantage over it is negligible.** FIND achieves 0.921 AUROC_I on 10-shot MVTec-3D-AD (reported in Table 4) vs. PIRN's 0.922 — essentially tied. Yet FIND does not appear among the baselines in the main results (Table 1), making the headline "consistently superior performance" (Abstract) overstated relative to the actual competitive landscape. The paper's real strength against FIND is efficiency, not accuracy; this should be transparently reflected in the main comparison.

2. **No variance or statistical significance reporting for few-shot results.** Few-shot settings (5-shot, 10-shot) are sensitive to which specific samples are drawn. The paper reports a single number per setting with no standard deviation, confidence intervals, or mention of multiple seeds. Consequently, the 3–4 point AUROC_I gains cannot be assessed for robustness. Few-shot AD papers in this area commonly report variance over multiple runs.

### Minor

3. **APR's claimed mechanism is not directly validated.** The paper argues (lines 106–110) that anomalous patches are "assigned more diffusely across prototypes" and therefore "contribute weakly to each prototype context." The ablation in Table 7 shows APR helps (0.916 → 0.922), but this does not distinguish between the proposed explanation (APR captures novel normal variations) and a simpler one (APR is just a learned feature transformation). No experiment measures prototype drift separately for normal vs. anomalous test samples, which would directly support the claimed mechanism.

4. **On Real-IAD D3, PIRN is not top on the image-level metric.** Table 8 shows D³M achieves 0.890 AUROC_J vs. PIRN's 0.873. The paper correctly notes that D³M uses three modalities vs. PIRN's two, but this weakens the Abstract's blanket claim of "consistently superior performance."

5. **Sinkhorn regularization parameter not reported.** The BPA module uses entropic regularization in the Sinkhorn algorithm; the strength of this regularization directly affects assignment softness and codebook diversity. Omitting this parameter harms full reproducibility.

6. **The claimed train-test distribution gap that APR supposedly bridges is never measured.** The paper asserts APR "bridges the train-test distribution gap" (line 30) but provides no analysis (e.g., cosine distance between training-set prototypes and test-set token features, before and after APR) to support this.

### Trivial

7. **Naming inconsistency:** The text refers to baselines as "BTF" and "CFM" (line 150), but Table 1 labels them as "BIT" and "CTM." These should be harmonized.

## Nice-to-Haves

- The 60 vs. 8 epoch discrepancy (few-shot vs. all-shot training) deserves a brief rationale.
- Including FIND in the main results table would honestly calibrate the paper's accuracy claims.
- Direct measurement of prototype drift (e.g., cosine distance between pre-APR and post-APR prototypes) on normal vs. anomalous test samples would strengthen the APR mechanism claim.

## Removed Points

These points appeared in the input review but are removed with justification:

- **"Inference-time behavior of APR creates circular dependency"** — Removed. The architecture is sequential (APR→BPA→MNC); there is no circular flow. The critic's concern about anomaly contamination is a restatement of the APR validation issue (already covered in Minor #3).
- **"Stage 2 of MNC creates circular dependency"** — Removed. The gating mechanism (lines 118–119) uses already-computed intra-modal reconstruction as a mask over original tokens. There is no feedback loop; the critic appears to have misread the flow.
- **"Ablation Table 2 garbled checkmarks"** — Removed. PDF parser artifact, not an author error.
- **"No limitations section"** — Removed. A generic omission common in conference papers; not a substantive weakness.
- **""Less than 1%" claim not formally defined"** — Removed. This is a visual claim from Figure 1 (left plot), which shows the performance curve vs. training data percentage. A formal table would be nice but is not required for a figure caption claim.
- **"BPA is standard OT with limited novelty"** — Removed (demoted to observation). The paper never claims algorithmic novelty for the OT formulation itself. The contribution is the integrated framework.
- **"FIND exclusion is fatal"** — Downgraded from the critic's implicit "fatal" framing to Major. The information is reported in Table 4; the omission is in Table 1. This is an evidential and framing issue, not a structural flaw.

## Novel Insights

None beyond the paper's own contributions. The input reviews surface the FIND omission and missing variance as the two main actionable concerns, but these are standard review observations rather than novel analytical insights.

## Suggestions

1. **Include FIND in the main results table** (Table 1) and recalibrate the accuracy claims. The efficiency advantage is the real story against FIND; state this explicitly.
2. **Report mean ± std over at least 3 random splits** for the 5-shot and 10-shot settings.
3. **Add a direct analysis of APR's behavior:** measure prototype drift (cosine distance pre- to post-APR) on normal vs. anomalous test samples, or construct a synthetic test with a globally anomalous image and show that APR does not collapse prototypes toward it.
4. **Report the Sinkhorn entropy regularization coefficient.**
5. **Harmonize baseline naming** (BTF→BIT, CFM→CTM).

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>