## Summary

This paper proposes ScaPre, a closed-form framework for large-scale concept unlearning in diffusion models. The method combines a spectral trace regularizer and geometry alignment (conflict-aware stable design) to handle conflicting updates when unlearning many concepts simultaneously, plus an Informax Decoupler that uses mutual information to per-channel scale parameter updates, confining unlearning to concept-relevant subspaces. The core optimization reduces to a Sylvester equation solvable in closed form. Experiments on Imagenette, ImageNet-Diversi50, ImageNet-Confuse5, and artistic style unlearning show substantial improvements over baselines.

## Strengths

- **Novel closed-form core via Sylvester equation.** The core optimization (Eq. 9–10) reduces unlearning to a Sylvester equation solvable in closed form per layer without iterative gradient descent. This is a genuine algorithmic contribution to the concept unlearning literature, departing from the iterative fine-tuning paradigm used by most prior methods. [impact=+10.00]

- **Strong empirical performance across multiple benchmarks.** On Imagenette (Table 1), ScaPre achieves 0.8% residual accuracy — substantially lower than the closest non-collapsed baseline (UCE at 8.5%) — while maintaining a CLIP score of 30.43 (vs. SD v1.5's 31.43). On ImageNet-Diversi50 (Table 3), ScaPre achieves UQ of 65.30 versus the next best (ESD at 56.35). On the precise-unlearning benchmark ImageNet-Confuse5 (Table 4), ScaPre achieves Overall Acc of 84.3% vs. the next best 50.3%. [impact=+10.00]

- **The Informax Decoupler (Sec. 4.2) is a principled approach** to per-channel update scaling using mutual information between activations and target/non-target labels, providing a theoretically grounded alternative to heuristic masking. [impact=+9.99]

- **Well-motivated problem framing.** The paper identifies three concrete obstacles in large-scale concept unlearning (conflicting weight updates, collateral damage, dependency on auxiliary modules/data) and builds the method around addressing all three simultaneously (Sec. 1, lines 17–19). [impact=+4.44]

- **Good evaluation breadth.** The paper evaluates on object unlearning (Imagenette, ImageNet-Diversi50, ImageNet-Confuse5), artistic style unlearning (50 artists), and mentions explicit content (I2P). The ImageNet-Confuse5 precision benchmark is well-designed to directly test the paper's claim of precise disentanglement between visually similar concepts. [impact=+3.07]

## Weaknesses

### Major

- **Runtime inconsistency (120 seconds vs. ~1.5 hours).** The paper claims "completing the unlearning of 50 concepts within only 120 seconds" (intro line 25, Section 5.5 line 248), yet Figure 3 and its accompanying table list ScaPre's execution time as ~1.5 hours — a 45× discrepancy. The figure caption says "GPU-hours" while the table header says "Execution Time (Hours)," adding to the confusion. UCE and RECE, also closed-form methods, are listed at ~0.5 and ~1.5 hours respectively, suggesting the figure may include non-unlearning steps (e.g., evaluation), but the paper never clarifies. Since efficiency ("Lightweight Design") is one of the paper's four stated contributions, this inconsistency prevents the reader from evaluating a central claim. [impact=-10.00]

- **The "×5 more concepts" claim is unsubstantiated.** Both the abstract (line 9) and contributions list (line 29) state that ScaPre "can forget up to ×5 more concepts than the best baseline within the limits of acceptable generative quality." There is no definition of "acceptable generative quality," no experimental protocol that measures how many concepts each method can unlearn before crossing that threshold, and no direct comparison that yields a factor of 5. Figure 4 shows scalability curves, but the raw data supporting a ×5 multiplication is neither presented nor explained. A claim this precise requires correspondingly precise evidence. [impact=-10.00]

### Minor

- **No error bars or statistical significance reported anywhere in the main results (Tables 1–4).** Diffusion model sampling is inherently stochastic, and unlearning outcomes can vary with random seeds or initialization. Without variance estimates, the reader cannot assess whether ScaPre's numerical leads (e.g., UQ 65.30 vs. ESD's 56.35) are reliable or could fall within the noise of a single run. [impact=-9.85]

- **The proximal refinement (geometry alignment via Bures distance + Procrustes adjustment, Sec. 4.3) is described only at a conceptual level** in the main text — "moving partway along the Bures geodesic" — without specifying the interpolation parameter that controls how far the refinement moves toward the pretrained reference or how the refinement interacts with the Sylvester solution. These details are deferred to Appendix B.2 with no summary in the main text, making the method description incomplete for a reader of the main paper. [impact=-7.62]

- **Several implementation details of the Informax Decoupler (Sec. 4.2) are underspecified:** the total sample size K used to estimate empirical joint distributions, the method for selecting the adaptive threshold τ_i for each channel, and the nature of the "neutral inputs" (y=0) are not stated. These details affect reproducibility. [impact=-0.34]

- **The UQ metric is dataset-relative** — computed using means and standard deviations across all methods in a given table, so values depend on which baselines are included and are not directly comparable across papers. The sigmoid normalization also compresses differences in hard-to-interpret ways. However, the paper reports raw accuracy and CLIP scores alongside UQ, which mitigates this concern. [impact=-0.00]

### Trivial

- The abbreviation "SP" appears in all tables without explicitly linking it to "Sculpting Memory (Li et al., 2025a)," mentioned in the Related Work section. While inferable, this should be made explicit in table captions.

## Nice-to-Haves

- A main-text ablation study showing the contribution of each component (spectral regularizer, Informax Decoupler, geometry alignment) would substantially strengthen the paper, especially at scale where conflicts are most acute.
- Clarifying the source of "contextual features" c_{k,t} for the S matrix (text embeddings vs. U-Net activations) would address an ambiguity about whether the "no additional data" claim requires qualification.
- A comparison of how many concepts each baseline can handle before crossing a defined quality threshold would substantiate (or replace) the ×5 claim.

## Removed Points

These points appeared in the input review but were removed per the filtering rules:

1. **"S matrix requires forward passes / contradicts 'no additional data' claim"** — REMOVED because c_{k,t} are likely text-token embeddings from the CLIP text encoder (derived from concept prompt text only, not requiring images or U-Net forward passes). The criticism is not clearly verifiable as a real problem given what is on the page.

2. **"Spectral regularizer rationale insufficiently justified"** — REMOVED as a subjective methodological taste concern. The regularizer's intuition (penalizing directions with high concept overlap) is a reasonable engineering design choice that does not require formal proof.

3. **"Missing main-text ablation"** — REMOVED because relegating ablation studies to the appendix is standard practice, especially under page limits. This is a nice-to-have, not a weakness.

4. **"Paper does not report inference cost for forward passes needed to compute S and MI estimates"** — REMOVED as a nitpick about implementation details. The ~5 GB memory figure and 120-second runtime claim refer to the unlearning step itself, which is standard.

5. **"Method is 'first closed-form framework specifically for large-scale concept unlearning'"** — REMOVED because the paper's own results show UCE/RECE collapsing at scale, making the "first" claim defensible in spirit.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Resolve the efficiency inconsistency definitively.** Clarify exactly what Figure 3 measures versus the 120-second claim. If 120 seconds is for the closed-form Sylvester solve only, state that explicitly and separately report the full pipeline time (including forward passes for computing feature statistics). If the figure or the text is wrong, correct it.

2. **Either substantiate or remove the ×5 claim.** Define a quality threshold (e.g., a minimum CLIP score or maximum FID), measure how many concepts each method handles before crossing it, and report the results. If the data does not support ×5, remove the claim entirely — the paper's empirical results are strong enough without it.

3. **Add error bars** (e.g., over 3 random seeds) to the main tables.

4. **Add a main-text ablation** showing the contribution of each component at scale (e.g., 50 concepts on ImageNet-Diversi50).

5. **Specify K, τ_i selection, and neutral inputs** for the MI estimation.

## Score and Decision

**Round 1 bracket**: 4.0 – 6.5

**Anchors consulted**:

| Path | Avg Score | Decision | Round | Itemized? | Comparison |
|------|-----------|----------|-------|-----------|------------|
| `caY45V0dYt.md` (RealEra) | 3.40 | Reject | R1 | Yes | Weaker method and results; ScaPre clearly stronger |
| `4aWzNhmq4K.md` (CORE) | 4.00 | Reject | R1 | Yes | Method described as trivial by reviewers; ScaPre more novel |
| `88wyP257x4.md` (SGU) | 4.25 | Reject | R2 | No | Score-based generative unlearning, less topical |
| `Ox2A1WoKLm.md` (Robust Erasure) | 4.33 | Reject | R2 | No | Weaker empirical results |
| `eVpjeCNsR6.md` (EraseDiff) | 5.60 | Reject | R2 | Yes | Quality concerns (−9.83) led to rejection; ScaPre's results are stronger but has internal consistency issues |
| `kSdWcw5mkp.md` (ConceptPrune) | 5.75 | Accept | R1 | Yes | Missing SOTA baselines (−10.00, −10.00); ScaPre has stronger method novelty and results but has internal contradictions |
| `SuHScQv5gP.md` (Data Unlearning/SISS) | 5.75 | Accept | R2 | Yes | Experimental inconsistency (−9.82) similar to ScaPre's runtime issue, but less central to a claimed contribution |
| `gjwhDHeAsz.md` (SFD) | 6.50 | Accept | R1 | Yes | Missing related work (−10.00), weak baselines (−9.99); internal consistency concerns of ScaPre are more damaging |

**Narrowing**: ScaPre's top strengths (+10.00 closed-form core, +10.00 empirical results, +9.99 Informax Decoupler) are comparable to accepted papers like ConceptPrune (5.75) and Data Unlearning (5.75). However, ScaPre's two -10.00 weaknesses are about *internal consistency* (paper contradicts itself on runtime; makes an unsupported quantitative claim), which is more central to credibility than the missing-baselines weakness patterns seen in the accepted anchors. The runtime inconsistency directly undermines one of the four claimed contributions ("Lightweight Design"). Data Unlearning (5.75) had a similar-magnitude experimental inconsistency (−9.82) but that concerned different finetuning steps across tables, not a self-contradictory claim about the method's own performance.

**Final placement**: The paper has genuine contributions (novel closed-form core, strong results) that would normally support a score around 5.75. But the unresolved runtime inconsistency and unsubstantiated ×5 claim — both central claims of the paper — prevent proper evaluation of the contribution. Score is pulled down to 5.0.

**Final Score**: 5.0  
**Final Decision**: Reject

The paper addresses an important problem with a well-designed method and strong empirical results. However, the unresolved runtime inconsistency (120 seconds vs. ~1.5 hours) and the unsupported ×5 quantitative claim prevent acceptance in the current form. Both issues are fixable: clarifying what the runtime numbers measure and either substantiating or removing the ×5 claim would significantly strengthen the paper. With these fixes and the addition of error bars, the paper could become a strong candidate for acceptance.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>