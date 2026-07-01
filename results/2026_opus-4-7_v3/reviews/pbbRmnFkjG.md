Now let me verify several specific reviewer claims more carefully.Now I have a thorough understanding of the paper. Let me draft the review.Now let me proceed with calibration. Round 1 — Bracketing:Let me read the most relevant anchor papers for calibration.Now I have enough data for calibration. Let me form my bracket and finalize the review.

**Round 1 Bracket Analysis:**

- **Strong reject anchors (< 1.5)**: P49gSPmrvN (1.0), gwZ90hFSL2 (1.0), 5lUdTogEL3 (1.0) — all trivially weak papers with no real contribution. The paper under review is vastly superior.

- **Reject anchors (1.5–3.5)**: Wxl0JMgDoU (2.5, chess SAE), 89wVrywsIy (3.4, hierarchical tracing) — narrow scope, lack of rigor. The paper under review is substantially stronger in both novelty and execution.

- **Borderline reject anchors (3.5–5.5)**: Ch8s4FdUXS (4.4, SDXL Turbo SAE), F76bwRSLeK (4.8, foundational SAE paper), J9eKm7j6KD (4.8, motion SAE) — limited scope, mixed reception. The paper under review has richer empirical findings and greater ambition.

- **Borderline accept anchors (5.5–7.5)**: imT03YXlG2 (6.5, PatchSAE for CLIP adaptation), XAjfjizaKs (6.5, multi-layer SAE), 9ca9eHNrdH (7.0, SAEs not canonical), 1Njl73JKjB (7.0, principled SAE evaluation). These are the most comparable papers. The paper under review has more novel empirical findings than imT03YXlG2 but also over-promises with MRH.

- **Accept anchors (7.5–8.5)**: 5Ca9sSzuDp (8.0, CLIP decomposition — decomposes per-head, finds head roles, has downstream applications), I4e82CIDxv (8.0, sparse feature circuits), 2dnO3LLiJ1 (8.0, ViT registers). These are cleaner, more complete contributions. The CLIP decomposition paper notably does what the paper under review does NOT: it actually identifies per-head roles, connecting architecture to interpretation — exactly the missing analysis in MRH.

**Initial bracket: 5.5 to 7.0**

The empirical work pushes the paper above borderline reject papers (4-5), but the under-evidenced MRH headline prevents it from reaching the cleaner 7+ papers.

Now let me write the final review.Now I have all the information needed. Let me write the final consolidated review.

---

## Summary
This paper applies stable sparse autoencoders (SAEs) to DINOv2, extracting a 32,000-concept dictionary and studying how downstream tasks recruit concepts from it. The empirical analysis (Sections 3–5) reveals functional specialization: "Elsewhere" concepts for classification that implement conditional negation, border detectors for segmentation, and three monocular depth cue families for depth estimation. Geometric analysis documents departures from the Linear Representation Hypothesis (LRH). Motivated by these departures, the paper proposes the Minkowski Representation Hypothesis (MRH), positing that token embeddings lie in Minkowski sums of convex polytopes spanned by archetypal landmarks.

## Strengths

- **The task-specific concept analysis (Section 3) produces genuinely novel, well-characterized findings.** The "Elsewhere" concepts are a standout discovery: they fire off-object, vanish when the object is causally removed via masking, and implement conditional negation—"the object exists elsewhere, but this token is not the object" (Figure 2, left). The paper appropriately hedges this as "evidence suggestive of a causal effect." The finding that all top-50 segmentation concepts are border detectors forming a tight cluster in embedding space (Figure 2, right; Figure 11) is specific and informative. The depth-cue taxonomy (projective geometry, shadow-based, frequency-transition families; Figure 3) aligns with established monocular cue categories from visual neuroscience and is validated through controlled perturbation experiments. These are concrete, non-obvious findings about DINOv2's internal organization.

- **Geometric diagnostics (Section 4) are thorough and properly baselined.** Comparisons against Grassmannian frames, random dictionaries, and shuffled baselines (Figure 4) establish meaningful reference points. The quantitative demonstration that task-aligned concept subsets break global quasi-orthogonality (Figure 11, Middle) and exhibit faster-decaying eigenspectra (Figure 11, Right) is well-grounded. The distinction between statistical structure (Z) and geometric structure (D) is clearly maintained throughout.

- **MRH is formally defined with precision (Definition 1) and states three testable conditions.** Proposition 1 connecting multi-head attention to Minkowski sums is mathematically clean. The connection to Gärdenfors' conceptual spaces is apt.

- **Honest epistemic framing.** The paper explicitly calls MRH "a working hypothesis whose testable predictions we outline" (abstract), and conditions its implications with "If, and this is an assumption, the Minkowski Representation Hypothesis holds" (Section 6). This mitigates concerns about overclaiming.

## Weaknesses

### Fatal
None

### Major

- **MRH is under-evidenced relative to its prominence in the paper.** MRH is the headline contribution (title, abstract, all of Section 6), yet its empirical support consists of a single paragraph ("Empirical evidences" in Section 6) with all three pieces of evidence—geodesic paths staying near data support, archetypal analysis matching SAE with ~10 archetypes, and block structure in Gram matrices—deferred entirely to appendix Figure 26. Each is described in a single sentence. For a hypothesis proposed as an alternative to LRH, which was grounded in substantial empirical work before gaining community traction, this level of evidence is insufficient. The honest "working hypothesis" framing partially mitigates this, but the paper still places disproportionate weight on a claim it does not adequately support in the main text.

- **Proposition 1 establishes an architectural property, not an empirical finding about learned representations.** The observation that multi-head attention produces Minkowski sums follows from the definitions of softmax and linear summation—it holds for *any* transformer, including randomly initialized ones. The paper itself acknowledges this is "elementary" (Section 6). The critical question for MRH is whether DINOv2's *learned* representations exploit this structure meaningfully: whether specific heads encode specific factors (position, category, depth) and whether tiles align with interpretable concept families. No per-head analysis is provided, despite this being within reach given the paper's existing infrastructure (SAE dictionary, positional decoders from Section 5). Notably, Gandelsman et al. ("Interpreting CLIP's Image Representation via Text-Based Decomposition") demonstrated exactly this kind of per-head role identification for CLIP, showing it is feasible.

- **The logical bridge from "LRH departures" to "MRH is the right alternative" has a gap.** Section 4 documents legitimate departures from LRH (higher coherence than Grassmannian baselines, anisotropic spectral decay, dense positional features, smooth per-image token geometry). These are well-characterized observations. But many geometric frameworks could explain these departures—manifold hypotheses, mixture models, simplex-structured representations. The paper does not argue why MRH *specifically* is the right post-LRH framework, as opposed to merely one consistent alternative. Architectural compatibility (Proposition 1) is necessary but not sufficient to distinguish MRH from competitors.

### Minor

- **Non-identifiability (Proposition 2) undermines practical testability without resolution.** The paper proves Minkowski decomposition cannot be recovered from activations alone, then suggests exploiting intermediate signals (attention weights, per-head outputs) as a resolution, but does not actually perform this analysis. MRH thus sits in a state where it is consistent with observations but not tested by them—a weaker epistemic status than even a "working hypothesis" requires.

- **No quantitative MRH vs. LRH comparison.** The paper documents qualitative departures from LRH but provides no direct metric comparing MRH fit to LRH fit (e.g., reconstruction quality of block-convex codes vs. sparse linear codes, or degree to which data lies in a Minkowski sum vs. a cone). A quantitative comparison would make the hypothesis contrast meaningful rather than qualitative.

- **Disconnection between Sections 3 and 6.** The task-specific concepts (Elsewhere, border, depth cue families) are discovered under an SAE/LRH framework. The paper does not re-examine what these concepts look like under an MRH lens—are Elsewhere concepts archetypes, convex regions, or boundary points of tiles? Without this bridge, the empirical and theoretical halves of the paper feel structurally disconnected.

- **Single architecture limits MRH generality.** The paper acknowledges this ("While focused on a single architecture," Section 7). MRH is proposed as a general hypothesis about transformer representations but is tested only on DINOv2-B.

### Trivial
None

## Nice-to-Haves

- Directly test whether individual DINOv2 attention heads encode identifiable factors by analyzing per-head value polytopes and checking alignment with position, category, or texture. This is the single most important strengthening move for MRH.
- Expand the AA vs. SAE comparison from a single appendix sentence to a systematic study varying archetype count, testing across image categories, and comparing held-out reconstruction.
- Report results at 2–3 layers to establish whether findings are layer-specific or general.
- Specify which layer the SAE is trained on—given that geometric properties vary across layers (as Figure 6 demonstrates), this affects interpretation.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- **"Largest interpretability demonstration" oversells novelty.** The paper qualifies this as "for a vision foundation model" and adds "to our knowledge," which is a defensible and specific claim. Removed as a framing nitpick.

- **R² > 88% reported without variance or alternative dictionary size comparison.** The paper states it is "consistent with prior stability results." Removed as a reproducibility-level detail.

- **Weak Z^TZ / DD^T correlation may be a mathematical artifact.** The paper itself acknowledges this possibility in footnote 1 (page 7), noting the algebraic relationship. Removed because the paper already addresses the concern.

- **PCA smoothness doesn't necessarily imply Minkowski structure.** The paper uses this observation as *motivation* for MRH ("Toward interpolative geometry"), not as *evidence* for it. The framing is appropriately hedged. Removed.

- **Causal masking for Elsewhere concepts isn't airtight.** The paper already hedges this appropriately: "providing evidence suggestive of a causal effect" (Figure 2 caption). Removed because the paper addresses the limitation reasonably.

## Novel Insights

The paper's most distinctive contribution is the discovery and characterization of "Elsewhere" concepts—features that fire off-object but depend causally on the object's presence, implementing a form of conditional negation for classification. This is a genuinely novel observation about how classification-relevant features organize in vision transformers, with potential implications for how we interpret attribution maps (which assume concepts are tied to the tokens where they fire). The systematic categorization of monocular depth cues learned by DINOv2 without 3D supervision—and their alignment with established visual neuroscience categories—is also valuable, connecting self-supervised representation learning to computational theories of depth perception. The MRH framework, while under-evidenced, offers a thought-provoking conceptual lens connecting multi-head attention mechanics to conceptual space theory.

## Suggestions

1. Move MRH empirical evidence (currently Fig. 26) into the main text and expand it substantially—the headline contribution should receive headline treatment.
2. Directly test whether individual DINOv2 attention heads encode identifiable factors (e.g., position, category, texture) by analyzing per-head value polytopes.
3. Provide a quantitative comparison between LRH and MRH (e.g., block-convex reconstruction vs. sparse linear reconstruction quality).
4. Re-examine the task-specific concepts from Section 3 through the MRH lens to bridge the paper's two halves.
5. Specify the layer used for SAE training and replicate key findings at 2–3 layers to establish generality.

## Score and Decision

**Anchor comparison (all rounds):**

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| P49gSPmrvN | 1.0 | 1 | Trivially weak; paper under review is vastly superior |
| gwZ90hFSL2 | 1.0 | 1 | Pseudoscientific; no comparison |
| 5lUdTogEL3 | 1.0 | 1 | Weak lifelong re-ID submission; no comparison |
| Wxl0JMgDoU | 2.5 | 1 | Chess SAE, limited scope; paper under review is substantially stronger |
| 89wVrywsIy | 3.4 | 1 | SAE circuit tracing, lacks rigor; paper under review has more novel findings |
| UbLvSPMvMA | 1.67 | 1 | Sparse binary representations; very weak, no comparison |
| Ch8s4FdUXS | 4.4 | 1 | SDXL Turbo SAE; narrower scope, fewer novel findings than paper under review |
| ghH6YYDs15 | 4.67 | 1 | SAE methodology; paper under review has richer empirical contributions |
| F76bwRSLeK | 4.8 | 1 | Foundational SAE paper; mixed reviews, paper under review is more ambitious |
| J9eKm7j6KD | 4.8 | 1 | Motion SAE; paper under review has deeper analysis |
| imT03YXlG2 | 6.5 | 1 | PatchSAE for CLIP adaptation; comparable scope but paper under review has more novel empirical findings (Elsewhere concepts, depth cues), though also over-promises with MRH |
| 9ca9eHNrdH | 7.0 | 1 | SAEs not canonical; cleaner, more focused contribution than paper under review |
| XAjfjizaKs | 6.5 | 1 | Multi-layer SAE; comparable scope, paper under review has more novel findings but weaker theoretical grounding |
| 1Njl73JKjB | 7.0 | 1 | Principled SAE evaluation; cleaner methodology, paper under review has more empirical novelty but less methodological rigor |
| I4e82CIDxv | 8.0 | 1 | Sparse feature circuits; significantly more complete with downstream applications |
| 5Ca9sSzuDp | 8.0 | 1 | CLIP decomposition; notably does the per-head analysis that would validate MRH—much more complete |
| 2dnO3LLiJ1 | 8.0 | 1 | ViT registers; clean, focused finding with broad practical impact |
| STUGfUz8ob | 7.6 | 1 | Transformer reasoning theory; stronger theoretical-empirical integration |

**Round 1 bracket: 5.5–7.0**

The paper's empirical contributions (Sections 3–5) are genuinely novel and well-executed, placing it above the borderline reject band (4–5). The under-evidenced MRH headline prevents it from reaching the cleaner 7+ papers that either have tighter theoretical-empirical integration (STUGfUz8ob, 7.6) or do the kind of per-head analysis that would validate MRH (5Ca9sSzuDp, 8.0). The paper is most comparable to imT03YXlG2 (6.5) and XAjfjizaKs (6.5)—it has more novel empirical findings than both but also a weaker theoretical claim that drags it down.

**Final calibration:** The empirical work in Sections 3–5 is the paper's genuine strength—the Elsewhere concepts, border detectors, and depth cue taxonomy are concrete and novel. The geometric analysis is thorough. The MRH proposal is interesting and honestly framed as a "working hypothesis," but the gap between the evidence and the ambition is the paper's central weakness. The paper tries to do too much: a thorough empirical study *and* a new theoretical framework, each of which deserves full treatment. The empirical half earns a borderline accept; the theoretical half pulls toward borderline reject. On balance, the empirical novelty tips the scale.

**Score: 6.0** — Borderline accept. The empirical contributions are novel and well-supported, but the headline theoretical contribution (MRH) is under-evidenced for its prominence.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>