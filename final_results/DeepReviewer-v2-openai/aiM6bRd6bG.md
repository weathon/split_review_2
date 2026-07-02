## Summary
# Final Review Report

## Summary

This paper introduces the problem of PPI Candidate Ranking — prioritizing novel protein-protein interactions for experimental testing — and proposes a two-stage framework combining interpretability-guided retrieval with multi-source re-ranking. The core methodological idea is to use predicted contact maps from D-SCRIPT and Topsy-Turvy to identify "active" residue regions from known interactions, then use embedding similarity over those regions to rank candidate proteins. A re-ranking stage then refines the top candidates using interaction scores, structural plausibility (pDockQ from AlphaFold2-based SpeedPPI), functional annotation similarity (GO terms, domains, pathways), and language model-based semantic similarity (BioBERT, PubMedBERT).

The evaluation uses a prospective design: known interactions from STRING v11 serve as the training/anchoring set, while novel interactions appearing in STRING v12 provide the test set. Results show substantial improvements over raw interaction probabilities — Recall@10 rises from ~1.2% to ~26% for D-SCRIPT, and MRR increases by 4-6x. The re-ranking analysis finds that PubMedBERT-based semantic similarity provides the most consistent ranking improvements (75.5% maintain-or-improve rate), though simpler annotation overlap baselines also achieve 64-70% gains.

**Strengths:** The paper addresses a practically important problem (guiding experimental PPI validation), proposes a clean prospective evaluation design using sequential STRING releases, and provides a systematic comparison of 10 different re-ranking signals. The interpretability-guided retrieval idea is technically sound and produces meaningful ranking gains.

**Core Weaknesses:** (1) The active-region extraction threshold is not quantitatively specified, making the core method step non-reproducible. (2) The re-ranking analysis lacks statistical significance testing — claims of PubMedBERT's superiority over other signals are unsupported by confidence intervals or hypothesis tests. (3) The "two orders of magnitude" claim in the abstract and conclusion is not consistent with the reported results (observed gains are 5-26x, not 100x). (4) Potential label circularity exists between STRING v12 ground-truth interactions (which may include structure-based predictions) and the AlphaFold2-derived pDockQ re-ranking signal. (5) The cross-encoder PubMedBERT training task (predicting v11 known interactions) differs from the evaluation task (predicting v12 novel interactions), and this generalization gap is not discussed. (6) The re-ranking analysis is restricted to top-10 candidates, limiting practical impact to the very top of the ranked list.

## Strengths
1. **Important problem formulation:** The paper shifts from PPI classification (does this pair interact?) to PPI candidate ranking (which candidate should be tested first?). This framing directly addresses the practical bottleneck of experimental validation and provides a clear evaluation paradigm that is more actionable than traditional binary classification metrics.

2. **Prospective evaluation design:** Using consecutive STRING releases (v11 known interactions as training/anchor, v12 novel interactions as ground-truth) is a well-conceived methodology. This avoids the retrospective evaluation pitfall common in PPI benchmarks, where models are tested on interactions already available in the same database release. The temporal gap design genuinely tests whether computational methods can anticipate future discoveries.

3. **Systematic multi-signal comparison:** The re-ranking module compares 10 distinct biological signals (interaction scores, pDockQ, TF-IDF, token overlap, localization, key terms, BioBERT, BioMedRoBERTa, PubMedBERT) under a consistent evaluation framework. This provides useful empirical evidence about which types of biological information are most predictive of novel interactions, and the finding that simple annotation overlap baselines (Token, Location, KeyTerm) achieve 64-70% maintain-or-improve rates alongside more complex LLM-based methods is informative for practitioners.

4. **Clear improvement over baselines:** The main retrieval results (Table 1) show consistent gains across all ranking cutoffs. The improvement from 1.2% to 26.4% Recall@10 (D-SCRIPT backbone) is practically meaningful — it means that experimentalists screening the top 10 candidates would find ~2.6 true positives on average instead of ~0.1, which is a substantive operational improvement.

5. **Interpretability as a methodological tool:** The decision to use contact-map activations not for explanation generation but as a representation-selection mechanism (focusing similarity computation on residues with high predicted contact probability) is clever. This repurposing of model internals for ranking is technically interesting and differentiates the work from standard interpretability applications.

## Weaknesses
### W1. Core Method Step Non-Reproducible (Major)
**Location:** Page 3 — Section 4.1 (Interpretability-Guided Retrieval)
**Evidence:** The active-region extraction procedure is described qualitatively: "identify all maximal contiguous segments of highly activated residues" without specifying the threshold for "highly activated."
**Impact:** The central methodological contribution — using contact-map-derived active regions for similarity computation — cannot be independently reproduced. Different thresholds would yield different active regions, different similarity scores, and potentially different ranking outcomes.
**Recommended Fix:** Specify the exact threshold $\tau$ used to define "highly activated" residues (e.g., residues with activation score $a_j = \max_i C(p,p_k)_{ij} \geq \tau$, with $\tau=0.5$). Report sensitivity of results to this threshold in the appendix. Update the Methods text to include precise definitions.

### W2. Missing Statistical Significance in Re-Ranking Analysis (Major)
**Location:** Page 8-9 — Section 5.3 (Table 2 and surrounding text)
**Evidence:** Table 2 reports pairwise "maintain-or-improve" percentages without confidence intervals, standard errors, or significance tests. Claims such as "PubMedBERT provides the most consistent positive signal" and comparisons like "79.7% vs. BioBERT" are presented as definite rankings despite being based on small absolute differences (~3-5 percentage points).
**Impact:** Without statistical grounding, readers cannot determine whether the observed rank-differences between re-ranking methods reflect genuine signal quality or random variation in a finite sample of 2,280 candidate pairs.
**Recommended Fix:** Add bootstrapped 95% confidence intervals around each percentage in Table 2. Include a paired McNemar test between selected method pairs (e.g., PubMedBERT vs. the next-best method) to support claims of superiority. Report the exact number of pairs where each method was applicable (some methods may have failed for certain protein pairs).

### W3. Unsubstantiated "Two Orders of Magnitude" Claim (Major)
**Location:** Page 1 — Abstract and Introduction; Page 9 — Conclusion
**Evidence:** The paper claims "improve ranking metrics by two orders of magnitude" and "improving early ranking performance by up to two orders of magnitude." Comparing against Table 1: MRR improves from 0.0340 to 0.1685 (~5x), Recall@10 from 0.0124 to 0.2641 (~21x), Recall@5 from 0.0071 to 0.1832 (~26x). None of these reach 100x ("two orders of magnitude").
**Impact:** This overstatement reduces the paper's credibility and invites unnecessary scrutiny. Reviewers and readers may question other claims if they detect inflation in the headline result.
**Recommended Fix:** Replace "two orders of magnitude" with precise bounded claims: "Our approach improves Recall@10 from 1.2% to 26.4% (a 21-fold relative improvement) and increases MRR by 5-fold compared to raw interaction probabilities." Apply this correction consistently in the Abstract, Introduction, and Conclusion.

### W4. Potential Label Circularity Between Ground Truth and Re-Ranking Signal (Major)
**Location:** Page 7 — Section 5.1 (Data Preprocessing)
**Evidence:** The data section states that new STRING v12 interactions include "high-confidence binding interactions, driven by high-throughput experiments and structure-based predictions." Meanwhile, the re-ranking module uses pDockQ scores from AlphaFold2-based SpeedPPI. If structure-based predictions contributed to the v12 labels, and the same type of structural signal (AlphaFold2) is used for re-ranking, the evaluation of pDockQ's effectiveness may be circular.
**Impact:** The comparison in Table 2 between pDockQ and other signals could be biased if structural predictions partially determine which interactions are in the test set. This would artificially inflate pDockQ's apparent performance.
**Recommended Fix:** (1) Clarify what fraction of new v12 interactions come from structure-based predictions vs. purely experimental validation. (2) If structural predictions are included, either exclude them from the test set when evaluating structural re-ranking signals, or explicitly discuss the circularity risk and bound the conclusions accordingly.

### W5. Cross-Encoder Training-Evaluation Task Mismatch (Major)
**Location:** Page 6 — Section 4.2 (LLM-based Re-Ranking)
**Evidence:** The PubMedBERT cross-encoder is trained on STRING v11 known interactions (to predict whether $p_c \in NP(p)$ for v11 data), but evaluated on STRING v12 novel interactions. The training task is "discriminate known interaction partners from negatives" while the evaluation task is "rank candidates for novel (unseen) interactions." These are fundamentally different tasks — one tests recognition of established patterns, the other tests generalization to genuinely new biological relationships.
**Impact:** The strong performance of PubMedBERT (75.5% maintain-or-improve) may partly reflect its ability to recognize co-annotation patterns that were already present in v11, rather than true generalization to novel biological relationships. This would overstate the semantic model's prospective value.
**Recommended Fix:** Add a control experiment: compare the PubMedBERT cross-encoder against a simple k-nearest-neighbor baseline based on v11 annotation similarity. If the cross-encoder's advantage over this baseline is small, its performance is primarily driven by annotation overlap rather than semantic generalization. Discuss the task mismatch explicitly in the limitations section.

### W6. Re-Ranking Limited to Top-10, Scope Not Discussed (Minor)
**Location:** Page 5 — Section 4.2 (Re-Ranking Module)
**Evidence:** The re-ranking module explicitly states it operates on "the top 10 ranked candidates for each target protein." The evaluation in Table 2 covers only 2,280 candidate pairs. The practical implication — that re-ranking only affects the very top of the ranked list — is not discussed as a methodological limitation.
**Impact:** The paper's framing suggests that the re-ranking module broadly "refines prioritization," but in practice it only affects the top 10 candidates. For experimentalists considering hundreds of candidates, the embedding-based ranking (Section 4.1) carries most of the practical value.
**Recommended Fix:** Add a sensitivity analysis with re-ranking windows of size 20 and 50. If the results are stable, report this to strengthen the analysis. If not, explicitly bound the scope of re-ranking claims and state that the method is designed for top-of-list refinement.

### W7. Missing Key Methodological Details (Minor)
**Location:** Page 3 — Section 3 (Background); Page 4 — Section 4.1
**Evidence:** (a) The embedding dimension $d=6165$ is stated without verification against the original Bepler & Berger source. (b) The projection module reduces dimensionality, but the output dimension is never specified. (c) The sliding-window cosine similarity in Eq (3) uses flattened embeddings of length $|I_k| \cdot d$ without discussing the computational complexity or potential overfitting when $|I_k|$ is large.
**Impact:** These omissions reduce reproducibility. Readers cannot implement or verify the method without guessing critical hyperparameters.
**Recommended Fix:** State the projected embedding dimension explicitly. Add a brief complexity analysis for the similarity computation. Verify and cite the original source for $d=6165$.

### W8. Related Work Reads as Literature List Rather Than Structured Argument (Minor)
**Location:** Page 2 — Section 2 (Related Work)
**Evidence:** The three paragraphs in Related Work follow a chronological/taxonomic organization (early methods, learning-based, LLMs) but do not include explicit comparative statements linking each literature category to the paper's contribution.
**Impact:** The novelty of the proposed approach — particularly how it differs from standard PPI classification and existing re-ranking in biomedical text retrieval — is not clearly positioned against prior work within the Related Work section itself.
**Recommended Fix:** Add one comparative sentence at the end of each related-work paragraph that explicitly states the gap the paper addresses. For example: "However, these models are evaluated on static benchmarks and do not address the problem of ranking candidates for experimental validation."

## Score
**Final Score: 6/10**

**Rationale:** The paper addresses a practically important problem (prospective PPI candidate prioritization) with a well-conceived evaluation design (STRING v11→v12 temporal gap). The core methodological idea — using contact-map activations for embedding-guided ranking — is sound and produces meaningful improvements over baselines. However, the paper is held back by several issues that affect its scientific rigor and reproducibility:

- **Reproducibility concern (W1):** The active-region extraction threshold is undefined, making the core method step non-reproducible. This is a fundamental methodological weakness.
- **Incomplete statistical evidence (W2):** The re-ranking analysis, which is a major claimed contribution, lacks confidence intervals and significance tests. Claims about which re-ranking signal is "best" are not statistically grounded.
- **Overclaiming (W3):** The "two orders of magnitude" claim is inconsistent with the reported results, reducing the paper's credibility.
- **Unaddressed methodological concerns (W4, W5):** Potential label circularity in the structural re-ranking evaluation and training-evaluation task mismatch for the cross-encoder are not discussed.

The paper has clear strengths (prospective evaluation, systematic multi-signal comparison, practical relevance) and addresses a genuine need in the PPI field. The weaknesses are primarily in methodological reporting rigor and statistical completeness, which are fixable through revision. With substantial revisions to address the reproducibility issues, statistical gaps, and claim bounding, the paper could be a solid contribution.