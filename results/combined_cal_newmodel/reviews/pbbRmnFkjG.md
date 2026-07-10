## Summary

This paper trains a 32,000-atom stable sparse autoencoder (SAE) on DINOv2-B activations to build a large concept dictionary, then analyzes how different downstream tasks (classification, segmentation, depth estimation) recruit specialized concept subspaces. The empirical core documents genuine departures from the idealized Linear Representation Hypothesis (LRH) — higher coherence than Grassmannian baselines, sharp spectral decay, and dense positional signals. Building on these observations, the paper proposes the Minkowski Representation Hypothesis (MRH), where tokens are Minkowski sums of convex polytopes from attention heads, and shows that multi-head attention can realize this construction (Proposition 1).

## Strengths

- **Genuinely large-scale interpretability effort.** Trains a 32,000-atom stable SAE on DINOv2-B (768-dim activations, 1.4M images), credibly the largest such concept dictionary for a vision foundation model. The scale makes the empirical findings nontrivial. **[favorability=11.60]**

- **Honest diagnostics of departures from LRH (Section 4).** Systematically documents where the learned dictionary does *not* match the near-orthogonal, uniformly sparse ideal — heavier-tailed coherence than Grassmannian baselines (Fig. 4A), sharply decaying SVD spectrum of D (Fig. 4B), low Hoyer scores (Fig. 4C-D), and dense positional outliers. The paper does not sweep these under the rug. **[favorability=11.76]**

- **Interesting task-specific findings.** The "Elsewhere" concept in classification (off-object firing that depends on object presence) is a genuinely novel observation supported by a causal masking check. The segmentation border concept cluster forming a coherent low-dimensional subspace is well-supported by multiple diagnostics. The depth cue perturbation analysis identifying three families of monocular cues is clever and connects to neuroscience. **[favorability=11.44]**

- **Proposition 1 is a clean theoretical observation.** The connection between multi-head attention's headwise convex combinations and Minkowski sums is mathematically correct and clearly stated. It bridges a specific architectural mechanism to a geometric picture of representation. **[favorability=11.82]**

- **Proposition 2 (non-identifiability) is an important caveat.** The paper acknowledges that decomposing final activations into generating factors is underdetermined, a limitation many interpretability papers gloss over. **[favorability=11.32]**

## Weaknesses

### Fatal
None.

### Major

- **The SAE framework and the MRH thesis are in structural tension that the paper does not resolve.** The empirical backbone (Sections 3–4) relies on SAE-discovered dictionary atoms as "concepts," operationalizing the Linear Representation Hypothesis (LRH). But MRH, if correct, implies that an SAE-based factorization imposes an LRH-compatible prior on a representation that may not respect that structure. The "concepts" extracted could be artifacts of the factorization prior — one of infinitely many possible decompositions (as Proposition 2 itself warns). The departures from LRH documented in Section 4 could equally be signatures of the SAE struggling to fit MRH-structured data with an LRH-shaped model. The paper transitions from SAE to MRH without addressing this circularity — e.g., testing whether MRH-compatible decompositions (archetypal analysis constrained by attention head structure) produce different dictionaries with better properties. **[favorability=2.12]**

- **The empirical evidence for MRH is far too thin to carry the paper's central framing.** The direct evidence (Section 6) consists of three results: (1) geodesic comparison — straight-line interpolation leaves the data support while k-NN geodesics stay near it, consistent with MRH but also with many other non-convex or curved geometries (e.g., any set with positive reach, smooth manifolds); (2) Archetypal Analysis matching SAE reconstruction with ~10 archetypes per image, consistent with any low-rank or manifold structure; (3) a claimed "clear block structure" in the code Gram matrix described qualitatively with no quantitative measure, null model comparison, or evidence that blocks correspond to head partitions. None of these distinguish MRH from LRH+SAE, smooth manifold models, clustered representations, or many other geometric descriptions. The paper frames MRH as offering "testable predictions" but only gives conditional implications ("if MRH holds, then…") rather than experiments that could adjudicate between MRH and alternatives. Proposition 1 shows attention *can* realize Minkowski sums, not that DINOv2's representations *are* Minkowski sums. The paper honestly calls this "preliminary empirical evidence," but the abstract, title, and introduction center MRH as the headline contribution, creating a gap between framing and support. **[favorability=0.74 / -1.55]**

### Minor

- **The "Elsewhere concept implements object negation" claim is overstated relative to the evidence.** The causal masking experiment (concept disappears when the object is removed) is a good start, but it does not establish that the concept actively computes negation. An equally plausible account is that these concepts encode context features statistically correlated with object presence. Distinguishing these would require a more targeted causal intervention (e.g., activation patching to test whether perturbing the Elsewhere concept changes the classifier's output in the predicted direction). The Figure 2 caption acknowledges alternative interpretations ("another interpretation being distributed off-object evidence"), but the main text and abstract frame it more definitively as "implement learned negation." **[favorability=-0.25]**

- **No SAE hyperparameter sensitivity analysis.** The paper's findings depend on specific choices (c=32,000 atoms, k=8 active codes, 50 epochs, single-layer encoder with BatchTopK) that are not ablated. The coherence profiles, spectral decay, Hoyer scores, and task-specific subspace structures could all shift with different hyperparameters (e.g., larger dictionary, stricter sparsity, denser code). The paper treats these as properties of DINOv2's representation, but they could be properties of this specific SAE configuration. **[favorability=0.33]**

- **Several quantitative claims are stated without numerical values, effect sizes, or confidence intervals.** Examples: "significantly more aligned" (Section 3, Fig. 11), "decays much faster" (Section 3), and "R² > 88%" reported without variance or indication of whether this is on a held-out set. For an empirical paper whose main findings are descriptive statistics, this is a meaningful weakness. **[favorability=0.52]**

- **The depth cue perturbation analysis lacks sufficient control for confounds.** For instance, median blurring removes both shadows and fine texture simultaneously, so attributing the resulting activation change specifically to "shadow cues" rather than "texture cues" needs more careful controls. A comparison to a model not trained on depth (or a random initialization) would help confirm the clusters reflect depth-specific cues rather than generic low-level image statistics of the perturbations themselves. **[favorability=-0.06]**

### Trivial
None.

## Nice-to-Haves

- If MRH is to remain the headline contribution, articulate one or two specific, testable predictions that distinguish MRH from LRH and test them experimentally (e.g., testing whether deactivating individual attention heads removes a convex component of the representation rather than adding noise along a linear direction).
- Address the SAE/MRH circularity by testing whether MRH-compatible decompositions (e.g., archetypal analysis constrained by attention head structure) produce different concept dictionaries with better properties than the unconstrained SAE.
- Run even a limited SAE hyperparameter sweep (c ∈ {16k, 32k, 64k}, k ∈ {4, 8, 16}) to increase confidence that reported geometric properties are properties of DINOv2, not of a specific SAE configuration.
- Add numerical values, effect sizes, and confidence intervals for quantitative claims throughout Sections 3–4.
- Add control conditions to the depth cue perturbation analysis (e.g., comparing against a randomly initialized model).

## Removed Points

These points from the input review were removed with justification:

- *"The literature review reads more like an annotated bibliography than a selective argument"* — removed as a style nitpick.
- *"The paper does not calibrate its framing to match this modesty"* — removed as a subjective framing critique with no concrete anchor in the text.
- *"The paper over-reaches by centering the Minkowski Representation Hypothesis as its headline contribution"* — subsumed by the MRH evidence weakness above; redundant as a separate point.
- Various formatting/style complaints about parser artifacts — removed per hard rules.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Consider downgrading MRH from the central headline to a speculative discussion topic (its current evidential status) and letting the descriptive empirical findings (task-specific concept subspaces, departures from LRH geometry, per-image token geometry) stand as the main contribution — or substantially strengthen the empirical case for MRH with targeted discriminating experiments.
2. Explicitly address the SAE/MRH methodological circularity in the paper — this would significantly improve the argument's coherence regardless of which direction the evidence ultimately favors.

## Score and Decision

**Round 1 bracket:** 4.5 – 6.0. The paper is clearly above the reject-range SAE papers (avg 1.0–3.4) and the weaker SAE interpretability papers (avg 4.40–4.80) due to its larger scale, thorough diagnostics, and honest treatment of limitations. It falls below the well-executed representation-geometry paper at 6.75 (bVTM2QKYuA) because that paper has no negative-favorability items while this paper has structural weaknesses (SAE/MRH tension and thin MRH evidence) with items at -1.55 and 2.12.

**Round 2 narrowing:** Compared to the itemized 4.80 anchor (F76bwRSLeK, "Sparse Autoencoders Find Highly Interpretable Features in Language Models") which has multiple items below -1.5 (novelty concerns at -3.85, missing information at -1.92), this paper's worst item (-1.55 for conditional-implications-only framing) is less severe, and its strengths are better grounded in specific empirical diagnostics. Compared to the itemized 6.75 anchor (bVTM2QKYuA), that paper's weakest item is at 0.10 (a clarification request), while this paper has items near or below zero — placing it clearly below 6.75.

**Final score: 5.5.** The paper has a genuinely valuable empirical core (large-scale SAE on DINOv2, task-specific concept analysis, honest LRH diagnostics) that would constitute a solid contribution on its own. However, the MRH framing overextends relative to the evidence, and the unresolved SAE/MRH tension weakens the overall argument. A revision that either strengthens the MRH evidence or tones down the framing could raise the score.

**Anchors used:**

| Path | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| bVTM2QKYuA.md | 6.75 | R1 | Yes | Stronger: clean theoretical development with no negative-favorability items |
| 5Ca9sSzuDp.md | 8.00 | R1 | Yes | Stronger: cleaner execution with clear applications, no speculative overreach |
| Ch8s4FdUXS.md | 4.40 | R1 | Yes | Weaker: more limited scope, weaker evaluation, more severe negative items |
| F76bwRSLeK.md | 4.80 | R2 | Yes | Weaker: more severe novelty concerns and missing-information items |
| tcsZt9ZNKD.md | 1.75* | R1 | No | Lower-scored SAE paper, less relevant |
| Wxl0JMgDoU.md | 2.50 | R1 | No | Lower-scored SAE paper |
| 89wVrywsIy.md | 3.40 | R1 | No | Lower-scored circuit analysis paper |
| ghH6YYDs15.md | 4.67 | R2 | No | Theoretical SAE paper, different contribution type |
| J9eKm7j6KD.md | 4.80 | R2 | No | SAE for motion transformers, different domain |
| vogtAV1GGL.md | 5.75 | R1 | No | Concept representation paper, different approach |
| DZxU0q2S11.md | 5.75 | R1 | No | Data geometry theory, conceptually distant |
| gwZ90hFSL2.md | 1.00 | R1 | No | Unrelated topic |
| nSDOkm0SKo.md | 1.00 | R1 | No | Unrelated topic |
| u1cQYxRI1H.md | 0.50 | R1 | No | Unrelated topic (illumination) |
| 25kAzqzTrz.md | 8.00 | R1 | No | FixMatch theory, unrelated |
| I4e82CIDxv.md | 8.00 | R1 | No | LLM circuit discovery, unrelated |

*\*Note: tcsZt9ZNKD.md shows avg_score 1.75 in search metadata but 8.20 in document; likely a metadata artifact.*

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Borderline</decision>