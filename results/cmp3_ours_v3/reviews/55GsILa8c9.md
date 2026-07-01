Now I have all the information needed. Let me compose the final review.

## Summary

This paper presents CausalNovo, a plug-in framework for de novo peptide sequencing that improves noise robustness through label-guided noise peak identification, data augmentation (replacing noise peaks with other noise peaks), contrastive learning for representation invariance, and attention-based peak weighting. The framework is evaluated on three public datasets across three strong baseline models (CasaNovo, AdaNovo, π-HelixNovo). Results show consistent improvements at the amino acid, peptide, and PTM levels, with several gains in the 5–14% range. The evaluation is unusually thorough, including cross-species validation, NSR-stratified analysis, and attention analysis.

## Strengths

1. **Unusually thorough and broad evaluation.** The paper evaluates across three datasets (Nine-species, Seven-species, HC-PT), three baseline architectures, and three metric levels (amino acid, peptide, PTM). It additionally includes cross-species validation (Table 3), NSR-stratified analysis (Figure 4), attention analysis (Table 7), and sensitivity analysis with 18 ion types (Table 6). This breadth credibly supports the claim that the framework generalizes across models and conditions.

2. **Consistent and frequently non-trivial improvements.** Across virtually every combination of baseline, dataset, and metric, CausalNovo improves over retrained baselines. Several gains are practically meaningful in a field where benchmark improvements are often incremental: +12.0% (Seven-species, CasaNovo amino acid precision), +14.2% (HC-PT, AdaNovo amino acid precision), and +15.1% (Seven-species, π-HelixNovo PTM precision).

3. **The vulnerability analysis (Figure 1) provides direct empirical motivation.** The paper cleanly demonstrates that when noise peaks in test-set spectra are replaced, baseline models drop in precision, and the drop sharpens as the m/z tolerance tightens. This grounds the problem in an actual measurement rather than a generic concern about noise.

## Weaknesses

### Major

1. **The causal framing is substantially oversold relative to what the implementation delivers.** The paper builds its narrative around Structural Causal Models (SCMs), Pearlian *do*-interventions, and the disentanglement of causal vs. non-causal latent factors. However, the actual mechanism is a well-engineered noise-robust training recipe combining: (a) label-supervised identification of noise peaks via theoretical spectrum matching (Eq. 4), (b) data augmentation by replacing noise peaks with other noise peaks from the same batch, (c) a contrastive objective encouraging invariance under this specific augmentation (Eq. 5), and (d) attention-based feature weighting via element-wise masking (Eq. 3). The "intervention" is a data augmentation strategy, not a Pearlian *do*-operation; the "disentanglement" is soft attention, not a factorization of latent space into independent subspaces; and the invariance objective ensures robustness under one specific perturbation, not general independence of C and S. The paper does not include a control experiment (e.g., permuting the causal/non-causal peak labels during training) that would distinguish whether the causal formalism adds value beyond the well-engineered training pipeline. **This gap between the paper's strongest interpretive claims and the evidence weakens the narrative considerably, but does not invalidate the empirical results themselves.**

### Minor

2. **The "causal" supervision uses ground-truth labels to label peaks as causal, creating circularity in interpretive claims.** The method identifies which peaks are "causal" by computing a theoretical spectrum from the ground-truth peptide sequence and thresholding on m/z deviation (Eq. 4). The model then learns to attend to these labeled peaks. The attention analysis (Table 7) confirms the model focuses more on peaks labeled as causal — which is largely a consistency check that the training objective was optimized, not independent evidence of discovered causal structure. The baseline already attends to at least one "causal" peak in 87.27% of predictions, and CausalNovo improves this to 89.24% (though a bigger jump occurs in the 3-causal-peaks category: 19.26% → 32.87%). This does not invalidate the method as a training technique but limits the claim that the model is doing something causally distinct from standard supervised learning.

3. **The "disentanglement" via element-wise masking (Eq. 3) is not a proper separation of latent factors.** The CEM computes importance scores that are multiplied element-wise with the representation z. If the encoder's latent space already mixes causal and non-causal information within individual dimensions (which is typical of deep representations), scalar masking cannot separate them into independent subspaces. The terminology overstates what the mechanism achieves.

4. **The value of α (fraction of noise peaks replaced during causal intervention) is not reported anywhere in the paper.** This hyperparameter controls the aggressiveness of data augmentation and should be stated. Its sensitivity is also not tested.

5. **No statistical significance or variance reporting.** All reported results appear to be point estimates. Given the variability of deep learning training, reporting standard deviations across multiple runs would substantially strengthen the reliability of the claims, especially for smaller gains (~1–2%).

6. **The purification objective (maximizing I(z_s; Y)) is counterintuitive and not clearly justified.** If z_s is supposed to contain non-causal noise information, training it via cross-entropy to predict Y (Section 3.3) requires more explanation. The claim that this "indirectly leads to the purification of z_c" is stated but not theoretically or empirically justified.

7. **The SCM assumption that C ⟂ S (causal and non-causal factors are independent) is likely violated in practice.** Co-eluting contaminants, trypsin autolysis products, and matrix effects can create correlations between the peptide (C) and background noise (S). While the paper notes that noise variables are omitted for simplicity, this is a significant idealization that limits the connection between the formal causal model and the actual data.

### Trivial

None.

## Nice-to-Haves

1. A non-causal control experiment where the causal/non-causal peak labels are permuted during training; if the causal labeling genuinely matters, this should degrade performance.
2. Measuring the mutual information or correlation between z_c and z_s for trained models to test whether the claimed independence property actually holds.
3. Sensitivity analysis for the α hyperparameter (fraction of noise peaks replaced).

## Removed Points

These points from the input review were removed after verification against the paper:

- **"Introduction presupposes causal mechanisms without defending the claim"** — This is critique of a modeling choice (using SCM as a framework). The paper uses SCM as a modeling tool, not as a claim about physical laws of nature. Scope creep.
- **"Related work section is underdeveloped for causal ML"** — The paper is primarily about de novo sequencing; the causal ML section is appropriately brief for context-setting. Scope creep.
- **"The paper reports 'up to 10%' from the largest gain"** — Standard practice across machine learning papers. Not a weakness.
- **"Baseline results differ between original and retrained versions"** — The paper transparently marks retrained baselines (†) and explains that retraining ensures fair comparison. This is good practice, not a weakness.
- **"Ablation gains are small"** — Subsumed under the Major weakness about the causal framing; individual component gains being small is common in ablation studies and doesn't independently weaken the paper.

## Novel Insights

The most valuable insight from the review process is that the paper's empirical contribution (a well-tested noise-robust training recipe with consistent improvements) is stronger than the paper's claimed contribution (a causal disentanglement framework). The vulnerability analysis (Figure 1) genuinely motivates the problem, and the systematic evaluation across 3 baselines, 3 datasets, and multiple metric types sets a high bar for thoroughness in this area. The paper would benefit from aligning its narrative with what the method actually does.

## Suggestions

1. **Reframe the paper.** Either (a) add a controlled experiment demonstrating that the causal labeling adds value over standard noise-robust training (e.g., permuting causal/non-causal labels), or (b) significantly dial back the causal claims to better match the evidence. The paper's empirical contribution stands on its own as a well-engineered noise-robust training framework with thorough evaluation.

2. Report the α value and test its sensitivity.

3. Add standard deviations across multiple runs for key results.

4. Clarify the theoretical justification for the purification objective (maximizing I(z_s; Y)).

5. Report mutual information or correlation between z_c and z_s for trained models to support the independence claim.

---

## Score and Decision

**Calibration Anchors Used (from /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/):**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| CrossNovo (I2ZYngkRW6) | 4.25 | Round 1 (band 3.5–5.5) | Similar in that it combines existing techniques (AT+NAT distillation) and was criticized for limited novelty and lack of theoretical grounding. CausalNovo has stronger/ more thorough empirical evaluation but also an overclaimed causal framing. |
| RankNovo (87B3zDRMjv) | 5.50 | Round 2 (band 4.5–6.5) | A reranking framework with novel metrics but modest improvements. CausalNovo's gains are larger and more consistent, but RankNovo had clearer novelty in its approach. CausalNovo's oversold framing is a bigger weakness. |
| ReNovo (uQnvYP7yX9) | 6.50 | Round 1 (band 5.5–7.5) | A genuinely novel retrieval-based de novo method with strong results. CausalNovo's empirical thoroughness is comparable but ReNovo has clearer methodological novelty without an overclaimed narrative. |
| MADGEN (78tc3EiUrN) | 6.00 | Round 1 (band 5.5–7.5) | Two-stage molecular generation from MS data. Accepted despite concerns about predictive retrieval. CausalNovo's evaluation is more thorough, but MADGEN has clearer framing. |

**Round 1 bracket:** Initially bracketed between 4.5 and 6.5 based on comparison with CrossNovo (4.25, rejected — less thorough evaluation) and ReNovo (6.50, accepted — stronger novelty).

**Round 2 narrowing:** RankNovo (5.50, rejected) provides the closest anchor — similar profile of solid empirical work with some framing/implementation concerns. CausalNovo's empirical results are stronger than RankNovo's, but the oversold causal framing adds a notable weakness that RankNovo did not have. The bracket narrows to 5.0–6.0.

**Final score:** 5.5 — The paper has real empirical merit and unusually thorough evaluation, but the gap between the strong causal claims and the actual mechanism (a noise-robust training pipeline using known techniques) is a significant weakness that the current version does not adequately address. The paper would benefit from either adding controlled experiments to support the causal claims or reframing to align narrative with evidence.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>