Now I have all the information needed to construct the final consolidated review.

## Summary

This paper identifies "copy-paste artifacts" as a distinct failure mode in identity-consistent generation — where models achieve high similarity scores by directly replicating the reference face rather than synthesizing identity across natural variations in pose, expression, and lighting. The paper makes three contributions: (1) **MultiID-2M**, a large-scale paired dataset (500k group photos with matched references, ~25k identities); (2) **MultiID-Bench**, a benchmark with a copy-paste metric (M_CP) that quantifies the trade-off between identity fidelity and variation; and (3) **WithAnyone**, a diffusion-based model trained with a contrastive identity loss on paired data that substantially reduces copy-paste while maintaining competitive identity fidelity.

## Strengths

- **Formalization of "copy-paste artifacts" as a distinct failure mode (Sec. 1, Fig. 2).** The paper identifies a genuinely under-appreciated problem: models achieving high similarity by directly replicating reference features rather than synthesizing identity. The distribution analysis in Fig. 2 makes this concrete — InstantID produces a sharp peak at Sim=1.0 while real image pairs span a broader range. Naming and formalizing this phenomenon is a useful contribution to the field.

- **The Copy-Paste metric M_CP (Eq. 2, Sec. 4).** The proposed metric measures whether the generated image is biased toward the reference or the ground truth, normalized by how far apart those two are. A score of 1 → perfect copy-paste, −1 → perfect agreement with GT. This is more informative than reporting only Sim(Ref), which rewards copying.

- **MultiID-2M dataset (Sec. 3).** The paper constructs a large-scale paired dataset (500k group photos with matched references, 1.5M additional unpaired images, ~25k identities) that fills a genuine gap — existing datasets lack paired references per identity, forcing reconstruction-based training. The four-stage construction pipeline is clearly described, and the use of CC-licensed public data with ethical safeguards is responsible.

- **Ablation study design (Table 3).** The ablations cleanly isolate the contributions of (a) paired training phase, (b) GT-aligned ID loss, (c) extended negatives, and (d) the dataset itself. Each ablation produces the expected effect, strengthening confidence in the method.

## Weaknesses

### Fatal

None.

### Major

- **The central claim of "breaking" the trade-off is overstated relative to the evidence (Abstract, line 23; Conclusion, line 303).** In Table 1, WithAnyone's Sim(GT)=0.460 is essentially tied with InstantID (0.464), UMO (0.458), and PuLID (0.452) — differences of 0.004–0.008. No confidence intervals or statistical significance tests are reported. The paper's real contribution — substantially reducing copy-paste (CP=0.144 vs. InstantID's 0.337) while maintaining competitive identity fidelity — is valuable and should be framed as an *improvement to the trade-off operating point* rather than a "break" of a general principle. The fitted regression curve in Fig. 5 is an empirical observation over a small set of methods, not a theoretical barrier that requires "breaking."

### Minor

- **Missing comparison against DynamicID (Sec. 2, footnote 1).** The paper discusses DynamicID as the most relevant concurrent method for multi-ID generation with controllability but excludes it due to unavailability of code/models. While the paper is transparent about this gap, its absence means readers cannot assess how WithAnyone compares to the closest related work in the multi-ID setting.

- **The user study (Sec. 6.3, Fig. 8) has limited evidentiary weight as reported.** Only 10 participants ranked 230 groups, and no inter-annotator agreement metric (e.g., Fleiss' kappa) is reported. The appendix (stripped in this version) may address some of these details, but the small participant pool is a genuine limitation of the evidence presented in the main text.

- **The GT-aligned ID loss (Sec. 5.1) uses ground-truth landmarks at training time, which are unavailable at inference.** The paper claims this "implicitly supervises generated landmarks" but provides no direct evidence that the model learns to produce well-aligned faces at inference without explicit landmark conditioning. While the ablation (Table 3) shows the loss helps identity fidelity, the "implicit supervision" claim could be strengthened with targeted analysis.

- **No ablation of the 50% paired-sample ratio in Phase 3 (Sec. 5.2).** This is a critical design choice directly affecting the copy-paste vs. fidelity trade-off. Varying this ratio (e.g., 0%, 25%, 50%, 75%) would directly test whether more paired data monotonically improves the trade-off.

- **No false-positive/false-negative analysis for the ArcFace threshold (0.4) used in identity matching during dataset construction (Sec. 3).** False positive matches would introduce label noise in the paired training data, potentially undermining the ID contrastive loss. A small validation experiment with manually verified matches would substantially strengthen confidence in the paired data quality.

### Trivial

- **Fig. 2 caption does not specify which face recognition model produced the reported similarity values (0.77, 0.46, 0.46, 0.30).** Since different embedding models produce different distributions, this should be stated.

- **The "BU ↓" column in Table 2 appears undefined in the main text.** The paper references Appendix D, which is stripped in this version, but a brief definition in the caption would improve readability.

## Nice-to-Haves

- Provide a distribution analysis of θ_tr across the 435 test cases to demonstrate that the CP metric's normalization does not systematically advantage/disadvantage any method (though all methods use the same test cases, so cross-method bias from this source is impossible).
- Report estimated precision/recall of the identity matching pipeline (ArcFace threshold 0.4) on a manually verified validation set.
- Add a failure case analysis of WithAnyone (e.g., identity blending in group photos, degradation for extreme poses).

## Removed Points

These points are flagged to be removed; treat them with caution:

1. **CP metric denominator instability concern:** Removed. The criticism argued that M_CP's sensitivity varies with θ_tr, potentially biasing comparisons across methods. However, all methods are evaluated on the same 435 test cases (same θ_tr per case), so the hypothesized cross-method bias cannot arise. The normalization operates as designed.
2. **User study method name corruption ("Cure", "iDetch", "Uniformal"):** Removed as parser artifacts per the hard rules. These are clearly corrupted versions of "Ours", "ID-Patch", and "UniPortrait" that do not appear in the original submission.
3. **Abstract vs. body statistics inconsistency:** Removed. Abstract says "hundreds of individual images" per identity; body reports ~400 per identity. These are consistent.
4. **GPT-4o prior knowledge / fair comparison concern:** Removed. The paper itself acknowledges this caveat in the Table 2 caption and still transparently includes GPT-4o in the tables.
5. **Missing appendix content criticisms:** Removed per hard rules — the appendix exists in the original submission and is stripped by the parser, not omitted by the authors.

## Novel Insights

None beyond the paper's own contributions. The reviews converge on the paper's central framing issue: the "breaking the trade-off" narrative overstates what the evidence supports. The paper's real strength — demonstrating that paired-data training with contrastive losses can substantially reduce copy-paste while maintaining competitive identity fidelity — is a meaningful but more modest result than the headline claims.

## Suggestions

1. Replace the "breaking the trade-off" framing with a more precise characterization (e.g., "substantially improves the trade-off operating point").
2. Add statistical significance analysis (confidence intervals or bootstrap tests) for the key comparisons in Table 1.
3. Add an ablation varying the paired-sample ratio in Phase 3.
4. Specify the face recognition model used for similarity values in Fig. 2.
5. Add a brief definition of "BU" in the Table 2 caption or footnote.

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>