## Summary

This paper investigates whether the "counterintuitive phenomenon" of deep generative models (where OOD data receives higher likelihood than in-distribution data) occurs in tabular anomaly detection. It proposes a new definition of this phenomenon based on relative model performance (Definition 3.3), then conducts extensive experiments on 47 tabular datasets and 10 CV/NLP embedding datasets from ADBench with 12 baselines. The main finding is that NF-SLT (a normalizing flow with a simple likelihood test) achieves average AUROC 0.8575 with Fail Ratio 0.02, substantially outperforming all comparison methods. The paper provides theoretical analysis (Theorem 5.4, Corollary 5.6) linking the phenomenon to dimensionality and feature correlation, supported by dimensionality-reduction experiments and intrinsic dimension analysis.

## Strengths

- **Comprehensive empirical scope**: Uses all 47 tabular datasets and 10 CV/NLP embedding datasets from ADBench without selective exclusion, benchmarked against 12 baselines (6 shallow + 6 deep anomaly detection methods). This directly addresses the Shwartz-Ziv & Armon (2022) critique about cherry-picked benchmarks.

- **Main experimental result is clear and striking**: NF-SLT achieves average AUROC 0.8575, average rank 3.43 (out of 13), Top2 Ratio 0.45, and most importantly a Fail Ratio of 0.02 — substantially outperforming all 12 baselines by a wide margin (next-best ICL: 0.8208 AUROC, 5.17 avg rank). The gap is not incremental; it is sizable.

- **Dimensionality analysis (Section 5.1) is a substantive intellectual contribution**: Theorem 5.4 extends Caterini & Loaiza-Ganem (2022) by showing that when ℍ(P) > ℍ(Q), the lower bound on the likelihood gap shrinks linearly with dimension d. Corollary 5.6 translates this into an inverse relationship between dimension and AUROC upper bound. The dimensionality-reduction experiments (Tables 2 and 3 with ICA and bilinear resizing) provide supporting empirical evidence that reducing dimension raises AUROC when the entropy condition holds.

- **Intrinsic dimension analysis (Section 5.2) creatively operationalizes "feature correlation"**: The d Ratio (intrinsic dimension / ambient dimension) provides a quantitative proxy for global feature correlation. Showing that image datasets have d Ratio ~0.002–0.019 while tabular datasets have 0.389–0.810 (Table 4) cleanly quantifies a qualitative difference often stated only informally.

## Weaknesses

### Fatal
None.

### Major

- **Definition 3.3 conflates the original phenomenon (likelihood inversion) with relative model performance.** The original counterintuitive phenomenon (Nalisnick et al., 2019a) is a specific property of likelihood assignment: OOD data receives *higher* likelihood than in-distribution data. Definition 3.3 redefines this in entirely different terms — whether most comparison models outperform the generative model by a sufficient margin. These are logically distinct: likelihood inversion could occur without poor relative performance (if all other methods are even worse), and poor relative performance could occur without inversion (if a non-flow method has a better decision boundary while likelihoods remain well-behaved). The paper's central claim — that the phenomenon is "consistently rare in general tabular data" — primarily answers the question "does NF-SLT rank well against other methods?" rather than the original question "are likelihoods sometimes inverted in tabular data?" The main empirical evidence (Table 1) speaks to relative performance, not likelihood inversion per se. The dimensionality analysis in Section 5.1 addresses the inversion question more directly, but the headline claim rests on Definition 3.3 and Table 1. This does not invalidate the paper's contributions, but it does mean the paper's framing overstates what the primary experimental results demonstrate.

### Minor

- **The independence assumption in Theorem 5.4 is not rigorously characterized for real tabular data.** The theoretical analysis assumes P and Q are products of independent 1D distributions. The bilinear interpolation experiments (Table 3) produce results that the paper acknowledges "conflict with the theorems in Appendix D," and the offered explanation (entropy changes from resizing) is post-hoc rather than derived from the theory. A more thorough characterization of when the independence assumption approximately holds (and what happens when it does not) would strengthen the analysis.

- **NF-SLT failures on embedding datasets deserve more substantive discussion.** On the imdb embedding dataset, NF-SLT achieves only 0.5013 AUROC (near random chance) and ranks last among deep methods (GOAD: 0.5398). On SVHN embeddings, it achieves only 0.5842. The paper dismisses these via Definition 3.3 (the performance gap is small), but these are precisely the kind of failures the paper's framing claims are rare, and the embedding datasets are described as non-image inputs "more similar to tabular data." These cases should be discussed as meaningful caveats rather than dismissed through an unparameterized threshold.

- **No standard deviations or confidence intervals in Table 1.** The paper states that 10 repeated experiments were conducted but reports only averages. Variance information would be useful for evaluating the robustness of fine-grained rank comparisons, particularly since Definition 3.3 depends on threshold-based comparisons (e.g., whether a 0.02 gap on the 'yeast' dataset is meaningful).

### Trivial
None.

## Nice-to-Haves

- Directly measure likelihood inversion per dataset (e.g., compute the fraction of anomalies whose log-likelihood exceeds a quantile of normal-data log-likelihood) to directly answer the original Q1 rather than relying solely on relative AUROC as a proxy.
- Specify β and γ (from Definition 3.3) with principled justification if they are set in the appendix, or clarify that the definition is qualitative.
- Compare whether non-flow methods also degrade on low-d-Ratio datasets to confirm the degradation is specific to flow-based likelihoods.
- Show per-dataset histograms of log-likelihoods for normal vs. anomalous data on a few representative datasets.

## Removed Points

- **"β and γ are never specified or justified anywhere in the text"**: REMOVED per hard rule. The paper states "The fully rigorous formulation of Definition 3.3 is provided in Appendix B." The parser strips appendices; the reviewer's claim that parameters are absent from the appendix cannot be verified from the available text.
- **"The theoretical analysis assumes feature independence... this creates circularity"**: DEMOTED to Minor (retained as the independence assumption point above). Characterizing a theory's assumptions is standard practice; the paper's argument that tabular data satisfies the assumptions (low dimension + approximate independence) is a valid application of the theory, not a circular argument. The retained minor weakness focuses on the uncharacterized cases where the assumption is violated.
- **"The embedding experiments partially undermine the paper's framing"**: DEMOTED to Minor (retained as the imdb/SVHN failures point above). The reviewer's framing as a "methodological gap" overstated the concern; the failures affect only 2 of 10 embedding datasets and do not contradict the tabular-data results.

## Novel Insights

The most penetrating observation from the review process is the logical gap between Definition 3.3 (defined on relative model performance) and the original phenomenon of interest (likelihood inversion). This gap is not merely philosophical — it has concrete consequences for how the paper's evidence should be interpreted. The paper's headline results (Table 1) convincingly show that NF-SLT outperforms other methods on tabular AD, but this does not directly establish whether likelihood inversion (the original puzzle) is rare in tabular data. The dimensionality analysis (Section 5.1) provides indirect evidence on the inversion question by showing that low-dimensional, weakly-correlated data mitigates the mechanism that causes inversion in high-dimensional, strongly-correlated data. A direct diagnostic of likelihood ordering per dataset would bridge this gap cleanly.

## Suggestions

- Reframe the paper's contribution to distinguish clearly between (a) the finding that NF-SLT outperforms baselines on tabular AD, and (b) the finding that likelihood inversion appears rare in tabular data. The latter is better supported by the dimensionality theory than by the main experimental results.
- Add per-dataset direct diagnostics of likelihood inversion (e.g., fraction of anomalies with log-likelihood above the normal median) to at least a subset of datasets.
- Report standard deviations alongside the averages in Table 1, or provide a per-dataset variance table in the appendix.
- Discuss the imdb and SVHN embedding failures as meaningful caveats, including analysis of why NF-SLT fails when other methods succeed on these datasets.
- Clarify the qualitative nature of Definition 3.3's parameters (or specify them if they are set somewhere) to make the reasoning in Section 4 reproducible.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/jQ596tXT3k.md` | 5.67 | R1 | Yes | Addresses same likelihood-paradox phenomenon; has stronger theoretical framing but similar scope limitations. My paper's empirical contributions are larger in scale (47 vs. ~8 datasets) but has a more central definitional weakness. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/7QDIFrtAsB.md` | 5.75 | R1 | Yes | Tabular AD with generative model; similar scale of experimentation. My paper's worst weakness (1.51 favorability) is less extreme than this anchor's (-3.44), but my paper's definitional issue is more structural. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/6Z8rZlKpNT.md` | 3.40 | R1 | Yes | NF-based OOD detection; less comprehensive experimentation. My paper is clearly stronger in empirical scope and theoretical depth. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/X8XQOLjLX6.md` | 4.50 | R2 | Yes | Questions fundamental assumptions of an AD method (like my paper). My paper has stronger empirical evidence and less severe worst-weakness (1.51 vs. -4.16). |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/LjygLD0AkT.md` | 5.00 | R2 | Yes | Likelihood-based OOD detection with theoretical guarantees but strong assumptions. Closest match: worst weakness favorability 0.78 vs. my 1.51; strength favorabilities 9.70 vs. my 10.65. My paper has slightly stronger empirical results but a similarly structural core weakness. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/SabhfFUfA1.md` | 4.67 | R1 | No | VAE reinterpretation for OOD detection; similar mid-range quality. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Vi6p2TeujL.md` | 4.25 | R1 | No | Tabular AD with mask modeling; no likelihood-related analysis. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/7VkHffT5X2.md` | 6.75 | R1 | No | LLM-based tabular AD (AnoLLM). Accepted paper with stronger novelty. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/lNZJyEDxy4.md` | 6.67 | R1 | No | MCM tabular AD; accepted with clean framing. |

**Round 1 bracket**: 4.0–6.0.
**Round 2 narrowing**: The closest anchor is "Rethinking Test-time Likelihood" (5.00, Reject), which shares a similar structure: a core methodological contribution to likelihood-based OOD detection, strong theoretical claims, but a central assumption/definitional weakness. My paper's strengths have slightly higher favorability (10.65, 10.38 vs. 9.70, 9.51, 7.59) but the core weakness (Definition 3.3 conflating relative performance with likelihood inversion, favorability 1.51) is similarly structural. The paper sits just above the "Autoencoders are Unreliable" anchor (4.50) whose weaknesses were more extreme, but below the "OOD Paradox" anchor (5.67) whose theoretical contribution was more novel. Placing it at 5.0 reflects a paper with genuine empirical and theoretical value but a definitional gap that limits what the central claim can assert.

**Final score: 5.0 — Borderline. Decision: Reject.** The paper's empirical scope and main results are substantial, and the dimensionality analysis is insightful. However, the central weakness — that Definition 3.3 operationalizes the "counterintuitive phenomenon" in terms of relative model performance rather than likelihood inversion — means the paper's headline claim ("the counterintuitive phenomenon is rare in tabular data") is not fully supported by the primary experimental evidence. The paper would benefit from directly measuring likelihood inversion per dataset or reframing its contribution to match what the evidence actually supports. With these changes, the paper could be competitive for acceptance.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>