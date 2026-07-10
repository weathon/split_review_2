## Summary

This paper trains a 32,000-atom sparse autoencoder (RA-SAE) on DINOv2-B activations to extract interpretable concepts, then studies how downstream tasks (classification, segmentation, depth estimation) recruit these concepts. The authors discover several interesting qualitative patterns (e.g., "Elsewhere" concepts that fire off-object yet depend on the object's presence, segmentation concepts as near-exclusive boundary detectors, three families of monocular depth cues) and systematically characterize the dictionary's geometry (coherence, spectral decay, antipodal pairs, Hoyer scores). Motivated by departures from the Linear Representation Hypothesis, they propose the Minkowski Representation Hypothesis (MRH), where token embeddings lie in Minkowski sums of convex polytopes — a geometry realizable by multi-head attention.

## Strengths

- **Large-scale interpretability resource.** Training a 32,000-atom SAE on DINOv2-B activations is a significant engineering contribution. The planned interactive visualization raises the practical value as a community resource. [favorability=9.85]

- **Interesting qualitative discoveries about task-specific concept recruitment.** The "Elsewhere" concept (firing off-object yet dependent on the object's presence) is a genuinely surprising finding. The observation that segmentation concepts are almost entirely boundary detectors, and that depth estimation draws on three distinct monocular cue families (projective, shadow-based, frequency transitions), provides vivid intuition about DINOv2's internal organization. [favorability=9.15]

- **Multi-faceted geometric characterization.** The paper examines the SAE dictionary from multiple angles (coherence distribution, singular value spectrum, Hoyer scores, antipodal pairs, co-activation Gram matrix) with sensible baselines (random, Grassmannian, shuffled). This systematic approach goes beyond a typical "here are some features" presentation. [favorability=8.47]

- **Conceptually elegant theoretical proposal.** The Minkowski Representation Hypothesis — connecting multi-head attention (each head = convex combination, sum across heads = Minkowski sum) to a geometric theory of representation (Definition 1, Proposition 1) — is a genuinely insightful observation. The non-identifiability result (Proposition 2) has practical consequences for interpretability tool design. [favorability=9.29]

## Weaknesses

### Major

- **MRH is centrally positioned but empirically thin.** The paper's title and abstract present MRH as the culminating contribution ("we advance a different view... we call this the Minkowski Representation Hypothesis"), and Section 6 is a full section. Yet the entire empirical evidence occupies a single paragraph (line 163) referencing three appendix figures. The geodesic comparison is qualitative; the Archetypal Analysis comparison ("matches or exceeds SAE reconstruction") lacks the specific metric, data split, and variance; the "clear block structure" in Gram matrices is asserted without quantitative block-detection metrics. For a hypothesis that is argued to supersede the LRH, this is insufficient evidence for the prominence it receives. [favorability=0.18]

- **The SAE analysis is in unresolved tension with the MRH proposal.** Sections 3–4 use SAEs (an LRH-based tool) to extract concepts and characterize their geometry. Section 6 then argues that the true geometry is Minkowski rather than LRH, and Proposition 2 shows that "recovering the generating factors from final activations is ill-posed" — i.e., the SAE decomposition may be fundamentally non-identifiable under MRH. The paper does not address why the SAE findings in Sections 3–4 remain valid if MRH holds, nor does it show that the observed departures from LRH are *predicted* by MRH. [favorability=1.84]

- **Key qualitative claims lack quantification and statistical rigor.** The Elsewhere causal claim ("they vanish if the object is removed") is mentioned in passing without systematic quantification across images or classes. The segmentation analysis discusses only top-50 concepts out of 32,000 atoms. The depth cue clustering via UMAP identifies three clusters without quantitative validation (silhouette scores, stability analysis). Throughout, findings are reported as single numbers (R² > 88%) without confidence intervals, standard deviations, or sensitivity analyses. [favorability=0.03]

- **No comparison to alternative decomposition methods.** All findings derive from a single SAE variant (RA-SAE with specific hyperparameters: k=8, c=32,000, 50 epochs). There is no comparison to a standard unconstrained SAE, PCA, ICA, NMF, or any other dictionary learning method. This makes it impossible to tell whether observed properties (high coherence, sharp spectral decay, antipodal pairs, task-clustered subspaces) are intrinsic to DINOv2's representations or artifacts of the specific RA-SAE architecture/training. [favorability=-1.06]

### Minor

- The "largest interpretability demonstration for a vision foundation model" claim (abstract) is asserted without citing or discussing competing efforts. The paper should either substantiate this claim or remove it.

- The correlation vs. functional specialization concern: the paper measures alignment between SAE concepts and linear probes, but correlation with task output does not establish that a concept *implements* that function. The causal test (masking) is only demonstrated anecdotally.

### Trivial

None.

## Nice-to-Haves

- The paper could strengthen MRH by directly testing its three criteria (Definition 1) with quantitative metrics rather than qualitative appendix figures.
- Bridging the SAE and MRH analyses: showing that the departures from LRH (high coherence, task-specific subspaces) are actually *predicted* by MRH would make the narrative much tighter.
- Addressing the non-identifiability tension explicitly — either demonstrating that SAE findings are robust to alternative decompositions or using architectural signals (attention weights, per-head outputs) to disambiguate.
- Adding at least one standard SAE comparison to verify that observed geometric properties are not RA-SAE-specific artifacts.

## Removed Points

These points were flagged during the filtering process and are not included in the main weaknesses:

1. **Style nitpick about excessive citations** (lines 23-24 "12 citations in a single sentence") — removed per rules against formatting/style nitpicks.
2. **Appendix-dependence concern** — the paper's appendix figures were stripped by the parser; removed per rules about missing appendix being a parser artifact.
3. **"No hyperparameter sensitivity analysis"** — subsumed into the broader "lack of quantification" weakness.
4. **"The depth cue analysis is underspecified"** — subsumed into the broader "lacks quantification" weakness.
5. **"No statistical precision"** — subsumed into "key qualitative claims lack quantification."
6. **Criticism about footnote (line 123) "undercutting the significance"** — too granular; subsumed by broader structural critique.
7. **"Section 7 has no discussion of limitations"** — the paper acknowledges it is "focused on a single architecture" (line 179); the observation is too generic.

## Novel Insights

The observation about "Elsewhere" concepts implementing what looks like learned negation (firing off-object yet dependent on the object's presence) is genuinely novel and could drive further interpretability research even if the current evidence is anecdotal. The finding that positional information smoothly compresses from high-rank to low-dimensional across layers, combined with the observation that removing the positional subspace leaves PCA organization largely intact, is an interesting architectural insight that deserves more attention. The MRH connection between multi-head attention's convex-combination-per-head / Minkowski-sum-across-heads structure is a genuinely novel theoretical observation; its value will depend on follow-up work that tests it more rigorously.

None beyond the paper's own contributions.

## Suggestions

1. Rebalance the paper: present the SAE-based empirical analysis as the primary contribution, and scope MRH more clearly as a forward-looking proposal with preliminary evidence rather than a culminating result.
2. Add systematic quantification for the Elsewhere causal claim across many images and classes with proper baselines (e.g., comparison to shuffled controls).
3. Include at least one standard SAE comparison to confirm that the observed geometric properties (high coherence, sharp spectral decay) are intrinsic to DINOv2 and not RA-SAE-specific.
4. Address the non-identifiability tension explicitly — either show SAE findings are robust to alternative decompositions or use architectural signals to disambiguate.

## Score and Decision

**Calibration summary (all anchors retrieved across rounds):**

| Anchor | Avg Score | Round | Itemized? | Comparison to paper under review |
|--------|-----------|-------|-----------|----------------------------------|
| `5lUdTogEL3` (person re-ID) | 1.00 | R1 | No | Unrelated topic, much weaker paper |
| `u1cQYxRI1H` (illumination) | 10.00 | R1 | No | Unrelated topic |
| `gwZ90hFSL2` (robots/NLP) | 1.00 | R1 | No | Unrelated topic |
| `nSDOkm0SKo` (finance) | 1.00 | R1 | No | Unrelated topic |
| `tcsZt9ZNKD` (scaling SAEs) | 1.75* | R1 | No | LM SAE paper with mixed scores but relevant methodology |
| `89wVrywsIy` (SAE circuits) | 3.40 | R1 | No | LM circuit analysis, lower quality |
| `Wxl0JMgDoU` (chess SAE) | 2.50 | R1 | No | Niche application |
| `UbLvSPMvMA` (cosine loss) | 1.67 | R1 | No | Narrow contribution |
| `Ch8s4FdUXS` (SDXL SAE) | 4.40 | R2 | Yes | Vision SAE, rejected; similar issues (qualitative-heavy, limited experiments) but broader scope |
| `ghH6YYDs15` (SAE inference) | 4.67 | R1 | No | Theoretical SAE paper |
| `F76bwRSLeK` (interpretable features) | 4.80 | R1 | No | LM SAE interpretability |
| `J9eKm7j6KD` (motion transformers) | 4.80 | R1 | No | Different domain |
| **`imT03YXlG2` (CLIP SAE remapping)** | **6.50** | **R1+R2** | **Yes** | **Most similar anchor. Vision SAE concept analysis, accepted. Our paper has similar rigor issues but adds MRH (ambitious but thin) vs. their narrower focus.** |
| `9ca9eHNrdH` (no canonical units) | 7.00 | R2 | Yes | SAE limitations paper, very well-received. Our paper is less rigorous but addresses a different question. |
| `1Njl73JKjB` (principled evaluations) | 7.00 | R1 | No | SAE evaluation framework paper |
| `XAjfjizaKs` (multi-layer SAEs) | 6.50 | R1 | No | MLSAE, different focus |
| `I4e82CIDxv` (sparse circuits) | 8.00 | R1 | No | LM circuits, different domain |
| `2dnO3LLiJ1` (ViT registers) | 8.00 | R1 | No | Different contribution type |
| `5Ca9sSzuDp` (CLIP decomposition) | 8.00 | R1 | No | Higher quality, different approach |
| `STUGfUz8ob` (abstract symbols) | 7.60 | R1 | No | Different topic |
| `34SPQ6fbYM` (polytopal complex) | 4.50 | R2 | No | Relevant concept (polytope geometry) but lower quality |
| `OXfllUhjrJ` (tropical geometry) | 3.67 | R2 | No | Tangentially related |
| **`bVTM2QKYuA` (representation geometry)** | **6.75** | **R2** | **Yes** | **LRH + polytopes for LLMs. Strong theoretical + empirical paper. Our paper has similar theoretical ambition but weaker empirical validation.** |
| `fw1oizreEF` (convexifying transformers) | 5.00 | R2 | No | Optimization-focused |
| `uDIiL89ViX` (microscopy DL) | 5.60 | R2 | Yes | Dictionary learning for vision, rejected; limited novelty concerns |
| `ih3BJmIZbC` (representational similarity) | 6.80 | R2 | No | Concept comparison, different focus |
| `bkdWThqE6q` (interpretable transformer) | 6.00 | R2 | No | Different approach |

*\* Note: tcsZt9ZNKD's avg 1.75 hides a bimodal distribution (scores 3,10,10,8,10); the low avg is due to one outlier review.*

**Round 1 bracket (initial): 4.5–6.5** — based on topic similarity to imT03YXlG2 (6.50), Ch8s4FdUXS (4.40), and uDIiL89ViX (5.60).

**Round 2 narrowing:** The most comparable anchors are **imT03YXlG2** (6.50, accepted — vision SAE concept analysis with similar rigor concerns) and **bVTM2QKYuA** (6.75, accepted — representation geometry with LRH/polytopes). My paper shares imT03YXlG2's SAE-on-vision approach and bVTM2QKYuA's geometric theory ambition. However, imT03YXlG2's weaknesses included moderate-favorability items (5.08, 6.06, 6.28, 6.85) alongside its very low ones (-2.90), while all four of my paper's weaknesses cluster below 2.0 favorability. Additionally, bVTM2QKYuA had weaknesses at 7.66, 7.46, 7.38 — much higher. The structural mismatch between MRH's prominence and its thin evidence particularly distinguishes this paper from the accepted anchors. Placing the paper **below** imT03YXlG2 (6.50) and **above** Ch8s4FdUXS (4.40) and uDIiL89ViX (5.60), the narrowest plausible bracket is **5.0–6.0**.

**Final score: 5.5.** The paper has genuine value — the scale of the SAE analysis, the interesting qualitative discoveries, the systematic geometric characterization, and the elegant MRH theory. But the structural mismatch between MRH's prominence and its thin evidence, the unresolved non-identifiability tension, and the pervasive lack of quantification are significant issues that prevent a higher score.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Borderline Reject</decision>