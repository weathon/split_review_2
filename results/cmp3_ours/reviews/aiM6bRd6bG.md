## Summary

This paper introduces the problem of PPI candidate ranking: given a target protein and its known interactors, rank novel candidates by likelihood of interaction. The proposed two-stage framework first uses predicted contact maps from D-SCRIPT/Topsy-Turvy to extract "active residue regions" from known interactors, then computes cosine similarity between these regions and sliding windows over candidate embeddings. A second re-ranking stage incorporates interaction scores, structural (pDockQ), semantic (TF-IDF/overlap), and LLM-based (PubMedBERT) signals. Evaluation is on a prospective STRING v11→v12 setup (279,568 new positives). Results show large improvements over raw PPI probabilities.

## Strengths

- **Prospective evaluation design (Sec 5.1).** Using STRING v11 interactions as the retrieval set and STRING v12 novel interactions as ground truth avoids within-release circularity and tests whether the method can anticipate future discoveries. This is the paper's clearest methodological strength and sets a good standard for the field.
- **Large-scale, ecologically valid problem framing (Sec 4, 5.1).** The PPI candidate ranking problem is well-motivated — experimental validation is the bottleneck, and prioritization tools are practically valuable. The scale (279K+ additional positives) is substantial.
- **Systematic pairwise re-ranking comparison (Table 2).** The rank-shift matrix across 10 scoring methods is informative. Findings such as PubMedBERT providing the most consistent improvements, and lightweight heuristics (Token, Location, KeyTerm overlap) yielding surprisingly strong results, are useful empirical observations for practitioners.

## Weaknesses

### Major

- **Missing ablation isolates the effect of active-region selection from the known-interactor advantage.** The proposed method uses (a) known interactors as anchors AND (b) contact-map-based active residue selection. The baseline uses raw D-SCRIPT/Topsy-Turvy interaction probabilities with neither (a) nor (b). The paper never tests a baseline that uses known interactors but replaces contact-map-based region selection with simpler alternatives such as full-embedding cosine similarity to known partners or BLAST sequence similarity. If such a baseline matches the proposed method, then the active-region mechanism does no useful work, and the claimed contribution reduces to "using known interactor information helps" — which is expected. This ablation is essential to support the central claim (Sec 5.3) that "exploiting active embedding regions repositions rediscoveries where they matter most for candidate screening."

- **Re-ranking analysis does not demonstrate absolute improvement in system-level metrics.** The re-ranking evaluation (Table 2, Sec 4.2) reports only pairwise rank-shift fractions — what fraction of *already rediscovered* pairs maintain or improve their position when switching re-rankers. Three specific problems: (i) No absolute retrieval metrics (Recall@10, MAP@10, Success@10) are reported *after* re-ranking, so we cannot determine whether re-ranking actually improves the final ranking. (ii) Re-ranking is restricted to top-10 candidates per protein. D-SCRIPT's Success@10 is 0.1277 (Table 1), meaning only ~12.8% of target proteins have a true novel partner in the top-10 at all; for the remaining ~87%, re-ranking can never improve recall because no true partner exists in the candidate set. (iii) The "Cosine" baseline in Table 2 is the proposed method's own initial ranking, not raw D-SCRIPT scores, so the comparison measures which re-ranker least disrupts the proposed method's ranking rather than which produces the best absolute ranking. The paper's claim that re-ranking is "crucial to refine the initial embedding-based ranking" (Sec 1) is not supported by evidence that it improves any system-level metric.

### Minor

- **"Two orders of magnitude" claim is overstated.** The abstract states "we improve ranking metrics by two orders of magnitude"; the conclusion softens to "up to two orders of magnitude." The largest observed improvement is Recall@5 for D-SCRIPT (0.0071 → 0.1832, ~25.8×), which is between one and two orders of magnitude. "Two orders of magnitude" typically means ~100×. The abstract should be calibrated to the actual factor.

- **No statistical uncertainty reported.** Table 1 gives only point estimates with no confidence intervals, standard deviations, or significance tests. For the large improvements this is unlikely to change the qualitative conclusion, but in Table 2, small differences between methods (e.g., BioBERT 79.7% vs BioMedRoBERTa 79.4% for the PubMedBERT column) cannot be assessed for reliability without variance estimates.

- **Threshold for "highly activated residues" in active-region selection is not specified.** Section 4.1 describes selecting "maximal contiguous segments of highly activated residues" but does not state what activation value constitutes "highly activated." This is a critical reproducibility detail.

- **Cross-encoder PubMedBERT may learn annotation correlations rather than functional coherence.** The cross-encoder is trained on STRING v11 interactions and tested on v12 novel interactions. If v12 novel interactions involve proteins whose UniProt annotations (GO terms, pathways) were already present in v11, the model could learn to associate annotation patterns with interaction status rather than true functional coherence. The paper should discuss this potential confound.

- **No breakdown by number of known interactors.** The method's performance depends heavily on the availability of known partners (acknowledged in limitations). A breakdown of results by |KP(p)| would help assess practical applicability.

### Trivial

- **Embedding dimension d = 6165 for Bepler & Berger (Sec 3).** This value appears unusually high for a per-residue embedding. The paper should clarify whether this is the raw encoder output dimension, a concatenated representation, or if there is a typographical error.
- **Prediction Coverage metric (Table 1).** This metric is very high (~95%+) for all methods and is not cutoff-dependent. It adds little information beyond what the other ranking metrics already capture.

## Nice-to-Haves

- Add the critical ablation: full-embedding cosine similarity (and/or BLAST sequence similarity) to known interactors, without contact-map-based active-region selection. This would isolate whether the contact-map mechanism contributes beyond the advantage of using known partners.
- After applying each re-ranker to the top-10 candidate set, report absolute metrics (Recall@10, MAP@10, Success@10) so the reader can directly assess whether re-ranking improves the final ranking.
- Report bootstrap confidence intervals or standard deviations for all metrics, particularly for Table 2 where between-method differences are small.
- Provide a breakdown of results by the number of known interactors per target protein.

## Removed Points

These points were flagged in the input review but are removed with justification:

- **"Interpretability-guided" framing is inconsistent:** The paper explicitly addresses this in Sec 1 ("we do not frame interpretability here as a means to generate explanations") and Sec 6 (limitations section). The authors acknowledge the tension, so this criticism is not a valid weakness.
- **xCAPT5 comparison is incomplete:** The critic claims xCAPT5 was not tested with the interpretability-guided framework. However, the proposed method requires contact maps produced by D-SCRIPT/TT; xCAPT5 does not provide these. Comparing raw probabilities is the only feasible cross-model comparison. Removed as scope creep.
- **pDockQ underperforms and should be presented differently:** The paper already acknowledges this in Sec 5.3 ("pDockQ underperforms for early ranking"). The presentation choice is editorial, not a methodological flaw.
- **Missing appendix details:** The paper states "Details of experimental setup and parameter choices are reported in Appendix A.1." The parser strips appendices; these exist in the original submission. Removed per filtering rules.
- **Pure formatting/typos/grammar issues:** These are parser artifacts from the PDF extraction, not author errors. Removed per filtering rules.

## Novel Insights

The harsh critic's most valuable observation is the missing ablation isolating active-region selection from the known-interactor advantage. This is a structural gap: the paper's core claim is about contact-map-guided region selection, but the improvement could be entirely explained by the trivial benefit of conditioning on known partners. The critic also correctly identifies that the re-ranking analysis, while comprehensive in pairwise comparisons, does not connect to system-level absolute metrics — making the re-ranking evaluation inconclusive about whether it actually improves the final system. These two insights point to a well-motivated paper whose empirical evidence is weaker than its claims suggest. Notably, neither issue is fatal: both are addressable with additional experiments, and the prospective evaluation framework itself remains a valuable contribution regardless.

## Suggestions

1. **Run the critical ablation:** Rank candidates by full-embedding cosine similarity to known interactors (without contact-map-based region selection). Also consider BLAST sequence similarity as an even simpler baseline. If the proposed active-region method outperforms these, the core claim is supported.

2. **Report absolute metrics after re-ranking:** After applying each re-ranker to the top-10 candidate set, report Recall@10, MAP@10, and Success@10. This would directly show whether re-ranking improves the final ranking.

3. **Calibrate claims:** Replace "two orders of magnitude" in the abstract with the specific improvement factor (e.g., "up to ~25× improvement in Recall@5").

4. **Add statistical uncertainty:** Add confidence intervals or bootstrap estimates to Table 1 and Table 2.

5. **Specify the activation threshold** used to define "highly activated residues" in Section 4.1.

## Score and Decision

**Bracket determination (Round 1).** I queried six score bands using calibration search on the deepreview corpus. The strongest topical matches in the 1.5–3.5 band (scKGOT 2.50, DrugAgent 2.50, Comparing PLMs 3.00) have fundamental methodological issues or trivial contributions — our paper clearly outranks these. In the 3.5–5.5 band (ProtIR 5.25, Improving Multimodal 4.75, Benchmark on DTI 4.00), papers have similar patterns of real strengths undercut by incomplete evidence — our paper is comparable. In the 5.5–7.5 band (MAPE-PPI 5.67 accepted, LLaPA 6.00 rejected, BioDiscoveryAgent 6.40 accepted), papers have stronger evidence chains. **Initial bracket: 4.0–5.5.**

**Narrowing.** Comparing directly: ProtIR (avg 5.25, rejected) had 8 reviews ranging 3–6, with its main weaknesses being missing baselines and dataset clarity — similar in severity to our missing ablation and incomplete re-ranking analysis. MAPE-PPI (avg 5.67, accepted) had stronger theoretical grounding and more complete experiments. Our paper's combination of a genuinely novel problem formulation and prospective evaluation design is distinctive, but the two Major weaknesses sufficiently reduce confidence. **Final score: 4.5.**

| Anchor Paper | Avg Human Score | Round | Comparison |
|---|---|---|---|
| scKGOT (cellular signaling) | 2.50 | R1 | Weaker contribution and methodology; our paper is clearly above this |
| DrugAgent (DTI) | 2.50 | R1 | Methodological issues more severe; our paper is above |
| Comparing PLMs for phages | 3.00 | R1 | Narrow benchmark contribution; our paper has broader scope |
| Benchmark on DTI | 4.00 | R1 | Similar pattern of strengths with evaluation gaps |
| Improving Multimodal Protein Function | 4.75 | R1 | Similar quality tier — both have fixable gaps |
| ProtIR (Protein Function) | 5.25 | R1 | Comparable weakness severity; both rejected despite merits |
| MAPE-PPI | 5.67 | R1 | Stronger evidence chain; accepted |
| LLaPA (PPI prediction) | 6.00 | R1 | More extensive evaluation despite being rejected |
| BioDiscoveryAgent | 6.40 | R2 | Stronger empirical support; accepted |
| Redefining Bioactivity Prediction | 7.00 | R2 | Much stronger evaluation; accepted |

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>