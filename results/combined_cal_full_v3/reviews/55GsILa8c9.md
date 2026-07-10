## Summary

This paper presents CausalNovo, a model-agnostic framework for de novo peptide sequencing that identifies noise peaks in mass spectra using domain knowledge (theoretical spectra), applies targeted replacement-based perturbation, and uses contrastive learning with a disentangled representation to make the model invariant to noise variations. Grounded in a structural causal model framing with independence and sufficiency principles, the approach is evaluated on three public datasets across three architecturally distinct baselines (CasaNovo, AdaNovo, π-HelixNovo), producing consistent improvements at amino acid, peptide, and PTM levels with gains of up to ~10%.

## Strengths

- **Well-motivated problem with clear preliminary evidence.** The vulnerability analysis (Figure 1) empirically demonstrates that existing models' predictions degrade when noise peaks are replaced, and tightening the m/z tolerance threshold amplifies the degradation. This convincingly establishes that models partially rely on spurious correlations, not just signal.

- **Model-agnostic framework with consistent gains across diverse baselines.** CausalNovo improves three architecturally distinct models (CasaNovo, AdaNovo, π-HelixNovo) across all three datasets and all metrics (Tables 1, 2), with every baseline+CausalNovo cell improving over its corresponding baseline and no regressions. This breadth of coverage is the paper's strongest empirical asset.

- **Multi-faceted evaluation beyond headline numbers.** The paper includes cross-species validation (Table 3), Noise-Signal-Ratio stratified analysis (Figure 4), attention analysis providing mechanistic insight (Table 7: 32.87% of CausalNovo predictions attend to three causal peaks vs. 19.26% for baseline), and ablation studies (Tables 4, 5).

- **Ablation isolates component contributions.** Table 4 credibly decomposes the method: the Independence objective provides the largest single gain (+1.2% AA precision), with Purification (+0.8%) and Symmetric contrast (+0.4%) contributing smaller but nonzero increments, preventing the method from appearing as a black box.

## Weaknesses

### Fatal
None.

### Major

- **Two critical hyperparameters are unreported, compromising reproducibility.** The fraction α of noise peaks replaced during training (Section 3.4.1: "a fraction α of peaks in x_non-causal is randomly replaced") and the tolerance threshold γ for identifying noise peaks (Eq. 4) are introduced in the main methodology but never given numerical values. The implementation details section (4.2) reports batch size, learning rate, warmup steps, temperature τ, and beam size, but omits α and γ. These parameters define the intervention strength and the noise/signal boundary; without them, practitioners cannot faithfully reproduce the method.

- **The causal SCM framework is used post-hoc to label components; the framing overstates conceptual novelty.** The paper builds an elaborate SCM (Figure 2A) with C (causal), S (non-causal), X (spectra), Y (peptides) and invokes Reichenbach's Common Cause Principle and do-calculus. However, the actual implementation — identifying noise peaks via theoretical spectra (Eq. 4), replacement-based perturbation, contrastive learning with positive pairing (Eq. 5), and cross-entropy on the causal sub-representation — can be described, justified, and executed as well-engineered robust representation learning adapted to mass spectrometry without invoking the causal machinery. The SCM does not generate algorithmic constraints that a non-causal approach would miss. The abstract and introduction contrast "causality-informed" against "statistical" models, overstating what is conceptually new. The technical contribution (careful augmentation design and multi-objective training applied to this domain) is legitimate and effective, but should be characterized more accurately.

### Minor

- **No variance or statistical significance is reported for any experimental result.** All tables show point estimates without standard deviations, confidence intervals, or multiple seed runs. This is especially concerning for the ablation components with sub-1% gains (e.g., +0.4% AA precision from the symmetric objective), where it is unclear whether these effects are within training stochasticity. Additionally, retrained baselines (†) differ substantially from published results (e.g., CasaNovo AA precision on Nine-species: 0.697 published → 0.741 retrained, a 4.4% gap exceeding several claimed improvements), suggesting training conditions matter and variance estimates are needed.

- **Figure 1's labels are not defined.** The caption refers to "Baseline +", "CausalNovo (Duo)", and "CausalNovo (Duo) +" as four series, but neither "+" nor "Duo" is explained in the text. The reader must infer that "Duo" refers to the two principles (Independence + Sufficiency) and "+" indicates evaluation on perturbed spectra. This should be spelled out.

- **The SCM's structural equations encode strong assumptions that are not discussed.** Eq. 2 encodes C ⟂ S (causal and non-causal factors are independent) and omits an edge from S to Y. In real mass spectrometry, signal and noise may be correlated (e.g., fragmentation conditions affect both), and noise patterns could correlate with peptide properties (e.g., certain contaminants co-elute with specific peptide classes), creating backdoor paths the SCM ignores. The method may still work under violations, but the paper does not discuss this.

### Trivial
None.

## Nice-to-Haves

- Consider adding a control ablation that uses the same data augmentation (noise replacement + theoretical peak enhancement) and contrastive/sufficiency objectives but *without* the mask-based disentanglement into z_c and z_s. This would directly test whether the causal decomposition drives the improvement beyond the augmentation itself, sharpening the contribution claim.
- Clarify the "Drop" ablation (Table 5) comparison: the claim that dropping noise peaks "did not lead to performance improvement" is ambiguous — it improves over Baseline (0.741→0.753) but is comparable to Replace+Enhance (0.753). State explicitly what the comparison is.

## Removed Points

These points are flagged as removed; treat them with caution:
- **Table 4/5 checkmark rendering artifacts** — Parser formatting issue, not author error. Removed per hard rules.
- **Broken cross-reference "[approximately 2.3x training time](#)"** — Parser artifact. Removed per hard rules.
- **Distribution mismatch from adding theoretical peaks to intervened spectra** — Speculative concern with no evidence of a problem caused in practice. Removed.
- **Generic/superficial strengths** (e.g., "addresses an important problem") — Removed as insufficiently specific to this paper's content.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Report the numerical values of α (fraction of noise peaks replaced) and γ (tolerance threshold) used during training.
2. Add variance estimates (mean ± std over at least 3 seeds) to the main results (Tables 1, 2) and the ablation (Table 4).
3. Define "Baseline +", "CausalNovo (Duo)", and "CausalNovo (Duo) +" in the Figure 1 caption.
4. Tone down the causal framing in the abstract and introduction to match what the method actually delivers — a robust representation learning approach using domain-specific augmentation and contrastive objectives, motivated by causal principles but not constituting a methodological advance in causality.

---

## Calibration Anchors

All anchors retrieved across rounds:

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `I2ZYngkRW6.md` | 4.25 (Reject) | R1 | Yes | Same topic (de novo peptide sequencing via distillation). Rejected largely for "engineering without novelty" (-7.20 favorability). Our worst weakness is far less severe (-1.31 vs -7.20), and our empirical contributions are stronger. |
| `uQnvYP7yX9.md` | 6.50 (Accept) | R1+R2 | Yes | ReNovo: same topic (de novo peptide sequencing). Higher novelty (10+ favorability strengths). Similar weakness profile but better originality. Our paper is weaker on novelty but comparable on empirical rigor. |
| `78tc3EiUrN.md` | 6.00 (Accept) | R1+R2 | Yes | MADGEN: mass-spec de novo molecular generation. Similar weakness severity (-4.13, -3.27, -3.75). Our paper has slightly higher strength favorability (8.77-9.61 vs 6.68-9.82). |
| `qac43AwuL9.md` | 6.00 (Reject) | R2 | Yes | Causal Information Bottleneck: causal representation learning (different domain, but relevant to framing criticism). Rejected despite high strengths due to weak experiments. Our paper has stronger experiments but similar causal-framing concerns. |
| `G536mmC2HL.md` | 3.00 (Reject) | R1 | No | Molecular conformation — computational biology but not de novo sequencing. Lower quality. |
| `IZiKBis0AA.md` | 3.00 (Reject) | R1 | No | Antibiotic design — computational biology but different task. Lower quality. |
| `jqmptcSNVG.md` | 6.20 (Accept) | R2 | No | Peptide design. Related domain, similar tier. |
| Others (1.00, 2.00, 8.00) | — | R1 | No | Not topically comparable (finance NLP, robotics, protein generation). |

**Round 1 bracket:** [5.5, 6.5] — determined by comparing against the 4.25 (de novo sequencing, rejected) and 6.50 (ReNovo, accepted) anchors. Our paper has far stronger empirical evidence than the 4.25 paper (which was rejected for lacking novelty) but weaker originality than ReNovo.

**Round 2 narrowing:** Adding MADGEN (6.00, Accept) and CIB (6.00, Reject) confirms this range. Our paper's worst weakness (-1.31 for causal framing) is less severe than MADGEN's worst (-4.13 for presentation) and CIB's worst (-6.93 for missing baselines), while our strengths (8.77-9.61) are solid but lack the extreme 10+ favorability that pushed ReNovo to 6.50.

**Final score placement:** 6.0. The paper sits above the rejected 4.25 anchor due to much stronger weaknesses (favorability -1.31 vs -7.20) and genuine empirical contributions. It sits below the 6.50 ReNovo anchor because ReNovo has two strengths above 10.0 favorability (originality-driven) that this paper lacks, and our missing hyperparameters (1.87) represent a concrete reproducibility gap ReNovo did not have. The paper is on par with MADGEN (6.00), sharing similar weakness severity while having slightly higher strength favorability.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>