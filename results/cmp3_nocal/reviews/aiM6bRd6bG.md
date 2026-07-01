## Summary

This paper introduces PPI candidate ranking as a task distinct from PPI classification, and proposes a two-stage framework that (1) uses D-SCRIPT's internal contact-map activations to identify "active residues" from known interactions and uses those to guide embedding similarity with candidate proteins, then (2) refines the top-10 candidates via multi-source re-ranking (interaction scores, structural plausibility, functional annotations, and LLM-based semantic signals). The method is evaluated prospectively on STRING v11→v12: models are given only v11 data and must rank candidates that appear as new interactions in v12.

## Strengths

1. **Prospective evaluation design (Section 5.1, Table 1).** Using consecutive STRING releases (v11→v12) means the test set consists of interactions that were *not yet known* at the time of the earlier release. This is genuinely stronger than retrospective random splits and should be adopted more widely in PPI research.

2. **Interpretability-guided retrieval is creative and biologically motivated (Section 4.1).** Exploiting D-SCRIPT's contact-map bottleneck to identify active residues from known interactions, then using those to compute targeted embedding similarities with candidates, goes beyond simple embedding concatenation or raw prediction scores. The idea of treating known interactors as anchors and measuring similarity only over the activated binding region is grounded in a mechanistic interpretation of how the model represents binding.

3. **Comprehensive multi-source re-ranking analysis (Section 4.2, Table 2).** The integration of nine different signals (interaction scores, pDockQ, TF-IDF, token/location/key-term overlap, BioBERT, BioMedRoBERTa, PubMedBERT) into a unified pairwise comparison is thorough. Table 2 provides practical guidance about which signals are complementary — e.g., PubMedBERT dominates but pDockQ underperforms for ordering.

4. **Large improvements in early ranking metrics (Table 1).** Recall@5 rises from 0.0071 (D-SCRIPT raw probability) to 0.1832 with the proposed method (~26×), MRR from 0.0340 to 0.1685 (~5×), and MAP@5 from 0.0103 to 0.2714 (~26×). These are practically meaningful for experimental screening: the first true positive appears much earlier in the candidate list.

## Weaknesses

### Fatal
None.

### Major

1. **LLM-based re-ranking results may be inflated by pre-training exposure to test interactions (Section 4.2, Table 2).** PubMedBERT, which yields the best re-ranking results (75.5% maintain-or-improve vs. cosine), is pre-trained from scratch on PubMed abstracts and full-text articles. These articles likely describe many interactions that later appear in STRING v12 — indeed, literature evidence is a primary channel through which interactions enter STRING. The paper acknowledges this risk for BioBERT/BioMedRoBERTa (lines 262–264: "it is uncertain if their gains reflect not only semantic generalization but also latent knowledge of interactions from the training data"), but the concern applies *even more strongly* to PubMedBERT because its representations carry information about v12 interactions encountered during pre-training. The paper offers no experiment to control for this (e.g., using a model with a known training cutoff before v11, or analyzing how many v12 interactions had PubMed entries before v12's release). This threatens the interpretation that semantic signals *generalize* to genuinely novel interactions rather than retrieving known facts from the pre-training corpus. The core retrieval results (Table 1) are unaffected, but the re-ranking conclusions are weakened.

### Minor

2. **"Two orders of magnitude" claim is unsupported by the reported numbers (abstract line 25, conclusions line 279).** The paper states "we improve ranking metrics by two orders of magnitude" and "improving early ranking performance by up to two orders of magnitude over existing models." Two orders of magnitude means 100×. The largest observed improvements in Table 1 are ~26× (Recall@5, MAP@5 for D-SCRIPT). MRR improves by ~5×. None of the metrics approach 100×. The actual improvements (5–26× on early ranking metrics) are substantial and do not need exaggeration. This overclaim undermines the paper's credibility and should be corrected.

3. **The re-ranking analysis (Table 2) does not measure whether re-ranking improves final retrieval quality.** Table 2 reports pairwise rank-shifts: whether known positives maintain or improve their rank when switching from one re-ranker to another. However, this only examines the 2,280 pairs *already retrieved* by the initial step, and rank-shifts among known positives do not account for what happens to false positives. A re-ranker could push all known positives up while also promoting false positives even more, degrading precision. Standard retrieval metrics from Table 1 (Recall@k, Precision@k, nDCG@k) should be recomputed for the full pipeline (initial retrieval + re-ranking) to demonstrate that re-ranking actually helps.

4. **Missing ablations make it difficult to attribute the source of improvements (Section 4.1, Table 1).** The proposed method differs from baselines in at least three ways: (a) using known interactors as anchors (which baselines lack), (b) using embedding similarity rather than prediction scores, and (c) the specific active-residue selection mechanism. Without ablations — e.g., (i) using full embeddings (no active-residue selection) with known-partner cosine similarity, (ii) using the active-residue region but with random segments as a control — it is unclear what fraction of the gain comes from the interpretability-guided mechanism versus simply having access to known partners and using embedding similarity. The ablated baselines are straightforward to compute and would substantially strengthen the paper's claims.

5. **Prediction Coverage decreases for the proposed method, but this trade-off is not discussed (Table 1).** For D-SCRIPT, Prediction Coverage drops from 0.9544 (baseline) to 0.9230 (proposed); for Topsy-Turvy, from 0.9683 to 0.9506. The method finds fewer novel partners overall but places them at higher ranks. This is a meaningful operational trade-off that the paper should acknowledge: some users may prefer higher coverage over early precision, or vice versa.

6. **The contiguous-segment assumption for active residue selection is not justified or ablated (lines 89).** The method identifies the *contiguous* sequence segment with highest average activation score and uses it for similarity computation. Binding interfaces are often composed of multiple non-adjacent residues brought together by 3D folding, and a contiguous segment in sequence space may not correspond to the full binding interface. Additionally, Equation 3 slides a window of length |I_k| across the candidate's embedding and takes max similarity, assuming the binding mechanism for novel partners will involve a region of the same length as the known partner's active region. Neither assumption is justified or tested against alternatives (e.g., top-k individual residues, all residues above a threshold, no window-length matching).

### Trivial

7. **Activation threshold underspecified (lines 89).** The method "scan[s] the resulting activation profile along the sequence of p_k and identify all maximal contiguous segments of highly activated residues." What constitutes "highly activated" is never defined — there is no stated threshold for inclusion. The paper should clarify whether this is a statistical threshold (e.g., top X% of activations) or a fixed value.

## Nice-to-Haves

- **Baseline with known-partner cosine similarity.** A natural baseline omitted from the paper: compute cosine similarity between target p and each candidate using *full* embeddings (no active-residue selection), with similarity aggregated over known partners. This would isolate the contribution of the active-residue mechanism.
- **Statistical significance / confidence intervals.** The paper reports point estimates only. For the scale of this evaluation (thousands of proteins), bootstrap confidence intervals on the key metrics would help assess reliability.
- **Failure case analysis.** The paper acknowledges that the method depends on having known partners, but does not analyze how performance degrades as a function of how many known partners a protein has (e.g., 1–5 vs. 6–20 vs. 21+).
- **Ablation of re-ranking set size (r).** The re-ranking uses a fixed top-10 candidate set. An ablation varying r ∈ {5, 10, 20, 50} would show how much of the improvement depends on this choice.
- **Temporal leakage control for LLM re-ranking.** Re-running Table 2 with a PubMedBERT variant that excludes articles published after STRING v11's release would resolve the temporal leakage concern definitively.

## Removed Points

These points were flagged in the input review but are removed or weakened here with justification:

1. **"Baseline comparison is structurally unfair."** The critic framed this as a fatal/structural flaw — that baselines lack access to known interactors makes the comparison invalid. This is too strong. The paper proposes a retrieval framework that uses known partners; comparing against raw prediction scores (which lack this information) is a valid way to demonstrate the framework's value. The real issue is missing ablations (captured in Minor weakness 4 above), not an invalid comparison. The core contribution is the framework itself, and the comparison is reasonable in kind, though incomplete in attribution.

2. **Parser artifact observations** (lines 73, 87, 89, 233). These are PDF extraction artifacts, not author errors. Removed per policy.

3. **Statistical significance as a weakness.** Demoted to Nice-to-Have. Single-run large-scale benchmark evaluation without error bars is standard practice in this area.

4. **Re-ranking set size as a weakness.** Demoted to Nice-to-Have. The paper explains computational constraints (SpeedPPI is expensive), and the choice is reasonable.

5. **Related-work scope comments.** The critic did not flag missing related work. No action needed.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the paper's claimed strengths and identify areas for improvement but do not surface a fundamentally different interpretation of the results.

## Suggestions

1. Correct the "two orders of magnitude" claim to "up to 26× on early ranking metrics" (or whatever the actual range is), which is impressive enough on its own.
2. Add a temporal-leakage control experiment for PubMedBERT (or at minimum, a post-hoc analysis of how many v12 interactions had PubMed entries before the v12 cutoff).
3. Run the ablated baselines suggested in Minor weakness 4 (full-embedding cosine similarity with known partners; random-segment control) and report results for Table 1.
4. Recompute Table 1's metrics after the full pipeline (retrieval + re-ranking) to directly measure re-ranking's contribution.
5. Discuss the coverage–ranking trade-off explicitly (Table 1: Prediction Coverage decreases 3–4% while early Recall increases 5–26×).
6. Justify or ablate the contiguous-segment and window-length-matching assumptions.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>