Now I have all the evidence needed. Let me compile the final review.

## Summary

This paper presents CausalNovo, a model-agnostic training framework for de novo peptide sequencing that uses a gating module (CEM) and auxiliary training objectives to make existing sequencing models focus on signal fragment ions rather than noise peaks. Signal peaks are identified via theoretical spectrum matching against the ground-truth peptide, and noise peaks are perturbed through a replacement-based augmentation. The method is evaluated on three public datasets across three strong baselines (CasaNovo, AdaNovo, π-HelixNovo), showing consistent and practically meaningful improvements of 5–14% on harder datasets.

## Strengths

- **Consistent and substantial empirical improvements across all baselines and datasets.** Tables 1–3 show that every baseline improves on every dataset at the amino acid, peptide, and PTM levels. Gains of 5–14% on the Seven-species and HC-PT datasets are practically meaningful in a domain where incremental gains are hard-won. The cross-species validation (Table 3) further shows generalization across diverse organisms.

- **Thorough analysis beyond headline numbers.** The paper includes vulnerability analysis (Figures 1, 3), generalization across varying noise-signal ratios (Figure 4), attention analysis (Table 7), component ablation (Tables 4–5), and analysis of different peak-distinguishing strategies (Table 6). This breadth of analysis gives confidence that the observed improvements are not spurious.

- **The attention analysis (Table 7) directly links the mechanism to the outcome.** CausalNovo increases the proportion of predictions attending to three causal peaks from 19.26% to 32.87%, and reduces "zero causal peak" cases from 12.73% to 10.76%. This provides direct, interpretable evidence that the framework shifts model behavior toward signal peaks rather than improving metrics through unrelated means.

- **Clear problem motivation.** The vulnerability study (Figure 1, Section 1) demonstrates that existing models degrade under noise peak perturbations, establishing a genuine practical need for noise-robust training.

## Weaknesses

### Major

1. **The causal framing is substantially overclaimed relative to what the method actually does.** The paper is framed in terms of Structural Causal Models, Reichenbach's Common Cause Principle, and do-calculus interventions (Sections 3.2–3.4, Figure 2A), but the practical implementation is considerably simpler. Specifically: (a) Identifying "causal" vs. "non-causal" peaks (Section 3.4.1, Eq. 4) relies entirely on matching experimental peaks against a theoretical spectrum computed from the *ground-truth peptide sequence* — this is supervised feature labeling using domain knowledge (b/y/a ion types), not causal discovery. (b) The "do-intervention" (Section 3.4.1) replaces identified noise peaks with other noise peaks from the batch — this is data augmentation, not a Pearlian intervention on structural equations. (c) The independence objective (Eq. 5) is contrastive learning, and the sufficiency objective (Eq. 6) is cross-entropy loss; both are standard techniques. (d) The SCM-derived independence C⟂S (Eq. 2) is never directly enforced — the method enforces invariance of z_c under perturbations to S, which is a different condition. The gap between the causal rhetoric (SCM, RCCP, do-calculus) and the actual mechanism (supervised peak gating + contrastive regularization) is significant and not acknowledged. This is a framing problem — the underlying method works — but the claims need recalibration.

2. **No uncertainty quantification for any result.** All metrics across all tables (1–7) are point estimates with no standard deviations, confidence intervals, or significance tests. Several improvements are small in absolute terms (e.g., +0.6% from the replace-based perturbation in Table 5, +0.4% from symmetric training in Table 4, +2.4% AA precision for CasaNovo on Nine-species in Table 1). Without variance estimates, the reliability of these smaller improvements cannot be assessed. This is a standard expectation for experimental ML papers.

3. **The purification objective (maximizing I(z_s; Y)) is insufficiently motivated and its mechanism is unclear.** The paper states that maximizing I(z_s; Y) "can indirectly lead to the purification of z_c" (Section 3.3) but does not explain the mechanism. Training the non-causal representation z_s to also predict Y appears contradictory on its face — if z_s is meant to capture noise, training it to be label-predictive could encourage z_s to contain signal information. The cited work (Chen et al., 2022) may provide grounding, but the paper's own explanation is too brief (one sentence) to be convincing, and no analysis is provided showing what z_s actually encodes.

### Minor

4. **Key hyperparameter α (noise replacement fraction) is not reported.** Section 3.4.1 states "a fraction α of peaks in x_non-causal is randomly replaced" but α is never given anywhere in the paper. This is a reproducibility gap, particularly since the ablation (Table 5) shows the replace perturbation contributes +0.6% to AA precision.

5. **The definition of Relative Improvement (RI) is ambiguous.** The paper defines it as "the relative performance reduction of CausalNovo compared to the baseline models" (Section 4.4, Vulnerability Analysis). The phrasing "reduction of CausalNovo" is unclear. From context and values, RI is clearly an improvement metric (CausalNovo − Baseline)/Baseline, but the wording should be corrected.

## Nice-to-Haves

- The "model-agnostic" claim would be strengthened by testing on at least one non-Transformer architecture (e.g., DeepNovo/PointNovo's CNN-based design), though this is not necessary given the three diverse Transformer baselines tested.
- The evaluation follows the NovoBench protocol; the paper honestly acknowledges that recent methods like ContraNovo/RankNovo use a different protocol (training on external corpora, evaluating on out-of-distribution test sets). Testing under that protocol would be a natural extension.

## Removed Points

The following points from the harsh review were removed with justification:
- **Retrained baselines outperforming original results:** Not a meaningful weakness — AdaNovo retrained is slightly *worse* than original, and π-HelixNovo is identical. All retrained baselines use consistent settings.
- **InstaNovo results being "surprisingly low":** These are from the NovoBench evaluation pipeline, not the authors' results; not a weakness of the paper.
- **Exclusion of ContraNovo/RankNovo comparison:** Self-acknowledged by the paper in the conclusion; this is a scope limitation, not a hidden weakness.
- **Inference-time CEM usage not explicit enough:** The paper states "negligible inference overhead (less than 1%)" and Figure 2B shows the full pipeline. This is sufficient.

## Novel Insights

None beyond the paper's own contributions. The harsh review correctly identifies the attention analysis (Table 7) as providing unusually direct mechanistic evidence linking the proposed training method to an interpretable shift in model behavior, which is a genuine methodological strength that goes beyond typical metric reporting.

## Suggestions

1. **Report uncertainty:** Re-run main experiments with at least 3 random seeds and report mean ± std for the headline results (Tables 1–3). This is the single most impactful improvement.
2. **Clarify the purification objective:** Either provide a formal justification for why maximizing I(z_s; Y) purifies z_c (citing the mechanism from the referenced Chen et al. 2022 work) or simplify the framework by removing this objective and showing the remaining components suffice.
3. **Report α** (the noise replacement fraction).
4. **Recalibrate the causal language** to match what the method actually delivers. The paper would be stronger, not weaker, by honestly describing the approach as "using domain knowledge to identify signal peaks via theoretical spectrum matching, then training models to focus on these peaks via a learned gating mechanism with contrastive robustness regularization" rather than claiming formal causal inference via do-calculus.

## Score and Decision

**Calibration anchors considered:**
- **ReNovo** (`uQnvYP7yX9`, avg 6.50, Accept) — Most directly comparable (de novo peptide sequencing). Had comparable strength profile (strongest strength 13.73) and more negative weaknesses (worst at -2.61). This paper's best strength (14.76) is stronger and worst weakness (-1.93) is less severe.
- **RankNovo** (`87B3zDRMjv`, avg 5.50, Reject) — Also de novo peptide sequencing. Had weaker strengths and weaknesses of similar magnitude. 
- **MADGEN** (`78tc3EiUrN`, avg 6.00, Accept) — Mass-spec molecular generation. Had much more negative worst weakness (-4.10) and weaker strengths.
- **Feature Matching Intervention** (`8GhwePP7vA`, avg 4.25, Reject) — Causal representation learning with similar framing-overclaiming issues, but weaker empirical results.

After itemized comparison: CausalNovo shares with accepted papers (ReNovo, MADGEN) the pattern of strong, well-documented empirical results, but like Feature Matching Intervention it has a gap between causal rhetoric and practical implementation. However, the empirical evidence here is substantially stronger than any of the lower-scored anchors. The paper's strengths (14.76, 14.35) are notably higher than ReNovo's best (13.73) while the weaknesses are comparable or less severe. Placing the paper at 6.5 reflects both the genuine contribution and the fixable framing/rigor issues.

**Round-1 bracket:** [6.0, 7.0] (narrowed from comparing CausalNovo's itemized favorability profile against anchors RankNovo 5.5, ReNovo 6.5, and MADGEN 6.0).

**Final score:** 6.5

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>