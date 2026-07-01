Now I have all the evidence I need. Let me write the final comprehensive review.

## Summary

This paper introduces a new task formulation — PPI candidate ranking — where, given a target protein and its known interaction partners, the goal is to rank novel candidate proteins for experimental validation. The proposed method uses interpretability (contact maps from D-SCRIPT/Topsy-Turvy) to identify "active residues" of known interactors, then ranks candidates by cosine similarity to those regions. A re-ranking module further refines the top-10 candidates using interaction scores, structural plausibility (pDockQ), and biomedical language features. The evaluation uses the STRING v11→v12 transition as a prospective test bed, where v12 novel interactions serve as ground truth. Results show substantial improvements over ranking by raw PPI prediction probabilities.

## Strengths

1. **Prospective evaluation design (Section 5.1).** Evaluating on the STRING v11→v12 transition — where v12 interactions are entirely unseen to models trained on v11 data — is a genuine methodological strength. Most PPI benchmarks use random holdout splits within a single database release, which do not test whether models can anticipate genuinely new discoveries. This paper directly addresses that gap.

2. **Conceptually interesting core idea (Section 4.1).** Using the contact maps from D-SCRIPT/Topsy-Turvy to identify which residue regions of known interactors are "active," and computing similarity only over those regions, is a non-obvious way to repurpose model internals for a downstream ranking task. The biological intuition (novel interactions likely engage similar binding regions as known ones) is plausible and well-motivated.

3. **Large-scale and practically motivated.** The evaluation spans the full human proteome with ~280k novel v12 interactions as ground truth and thousands of target proteins. The candidate-ranking formulation directly addresses the practical bottleneck of prioritizing interactions for costly experimental validation.

## Weaknesses

### Fatal
None.

### Major

1. **Missing ablation isolating the active-residue mechanism (the paper's central technical claim).** The paper's claimed technical novelty is the *active-residue selection* — using interpretability to identify which residue regions of known interactors participate in binding, and computing similarity only on those regions (Section 4.1, Eq. 3–4). However, the main comparison (Table 1) pits the full method (known partners + active-residue similarity) against raw PPI prediction probabilities from D-SCRIPT/Topsy-Turvy/xCAPT5, which do not use known partners at all. This comparison conflates two effects: (a) the benefit of *having* known partners to anchor the ranking, and (b) the benefit of the *active-residue selection* specifically. Without a baseline that uses known partners in a simpler way (e.g., computing full-embedding cosine similarity between each candidate and the average of all known partners), it is impossible to determine whether the active-residue mechanism adds value beyond the trivial approach of "candidates that look like proteins that already interact with the target are good candidates." This is not a minor oversight — the paper's core technical claim cannot be validated from the presented evidence.

2. **The "two orders of magnitude" claim is materially overstated.** The abstract states "we improve ranking metrics by two orders of magnitude" (line 25) and the conclusion repeats "improving early ranking performance by up to two orders of magnitude" (line 278–279). From Table 1, the best improvement over D-SCRIPT is Recall@10 at ~21× (0.0124 → 0.2641), and MRR at ~5× (0.0340 → 0.1685). For Topsy-Turvy, improvements are even smaller. These are roughly one order of magnitude, not two (~100×). This overstatement misrepresents the results.

### Minor

3. **Re-ranking evaluation measures rank shuffling within an already-enriched set, not discovery of new interactions.** The re-ranking analysis (Table 2) operates strictly on the top-10 candidates already retrieved by the cosine-similarity baseline. The metric "fraction of rediscoveries whose ranking was maintained or improved" measures rank changes *within this pre-filtered, highly enriched set*. It does not measure whether re-ranking brings *new correct interactions* into the top-10 that were previously outside it, nor whether it pushes non-interacting candidates down. The reported 75.5% (PubMedBERT) could reflect useful refinement or merely noise within an already saturated list. Reporting recall/precision after re-ranking would strengthen the analysis.

4. **MAP@k = Recall@k equality for k ≥ 50 in Table 1 requires clarification.** For both D-SCRIPT and Topsy-Turvy (proposed method and baseline), MAP@k equals Recall@k exactly at k = 50, 100, 200, 500. Under standard MAP definitions this is unexpected — e.g., D-SCRIPT Our Approach at k=100 has Recall=0.5960 and Precision=0.0263, yet MAP also equals 0.5960. This pattern holds for the baselines too, so it may reflect a non-standard metric definition rather than an error, but the paper should explain or correct it.

5. **The prospective ground truth includes computationally predicted interactions.** The paper notes (line 194) that v12 novel interactions include "structure-based predictions Szklarczyk et al. (2023)." This means some fraction of the "ground truth" positive interactions are themselves computationally predicted rather than experimentally validated, partially weakening the prospective framing of anticipating genuine experimental discovery.

### Trivial
None.

## Nice-to-Haves

- **Full-embedding and random-region ablations** (as described in Weakness 1) would cleanly isolate the contribution of the active-residue selection mechanism. This is the single most important addition for validating the paper's core claim.
- **Reporting recall/precision after re-ranking**, not just rank-shift fractions, would clarify whether the re-ranking step has practical value.
- **Clarifying the MAP definition or fixing the computation** would resolve the MAP@k = Recall@k concern.

## Removed Points

These points were raised in the input review but are removed after cross-checking against the paper:

- **"The baseline comparison is fundamentally unfair"** — Removed. The paper defines a *new task* (PPI candidate ranking using known partners). Comparing to raw PPI prediction probabilities is legitimate: it shows the value of reformulating the problem. The real issue (covered as Major Weakness 1) is the absence of an ablation that uses known partners with full-embedding similarity, not unfairness in the task-level comparison.
- **Missing pretrained weights info** — Removed as a minor implementation detail; the appendix (stripped by the parser) likely contains experimental details.
- **pDockQ recalibration constants** — Removed as a minor implementation detail.
- **Missing discussion of STRING v11/v12 systematic bias** — Removed. The paper acknowledges the limitation of depending on known partners; the systematic bias point is beyond the stated scope.
- **Missing confidence intervals** — Removed as a nice-to-have that is not standard practice for this type of evaluation at this scale.
- **Formatting and grammar nitpicks** — Removed per parser artifact policy.

## Novel Insights

The most interesting observation — beyond the paper's own contributions — is the asymmetry between the two backbone models in Table 1. D-SCRIPT achieves better early-ranking performance (higher Recall@5/10, Precision@5/10, MAP, Success) while Topsy-Turvy achieves better coverage at large k (higher Prediction Coverage and lower Average Rank). This suggests that Topsy-Turvy's network-derived training signal produces embeddings that spread positive interactions broadly across the ranked list, while D-SCRIPT's structure-only training concentrates them at the top. The paper notes this trade-off (lines 237–242) but does not fully explore why the network-aware training objective of Topsy-Turvy appears to hurt early-ranking precision in this ranking task, which is the opposite of what one might expect. This could be a fruitful direction for future work on designing embedding spaces specifically for candidate-ranking tasks.

## Suggestions

1. **Add a simple known-partner baseline:** For each target protein \(p\), rank candidates by their maximum (or average) full-embedding cosine similarity to all known interactors \(\text{KP}(p)\), without any active-residue selection. This directly isolates whether the active-residue mechanism improves over the trivial "find candidates similar to known partners" approach.
2. **Tone down the "two orders of magnitude" claim** to reflect the actual ∼5–20× improvements shown in Table 1.
3. **Clarify the MAP definition** or verify the computation; provide a brief worked example if using a non-standard variant.
4. **Report recall/precision after re-ranking** to establish practical value beyond rank shuffling.

## Score and Decision

**Score: 5.0**  
**Decision: Reject (borderline)**

The paper introduces a genuinely useful new task formulation and a clever prospective evaluation design. The active-residue-guided similarity idea is conceptually interesting. However, the core technical contribution — whether the interpretability-guided active-residue selection adds value over simply using known-partner information — cannot be assessed from the presented experiments because the baselines do not receive known-partner information. The "two orders of magnitude" claim overstates the empirical results by roughly a factor of 5–20. These issues are addressable with additional experiments, and the paper's strengths (new task, prospective evaluation, scale) are real. I would support a revised version that adds the missing ablation and corrects the overstated claims.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>