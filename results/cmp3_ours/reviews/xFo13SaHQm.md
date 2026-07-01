## Summary

This paper identifies and formalizes the "copy-paste" artifact in identity-consistent image generation, where models overly replicate reference faces instead of producing natural variation. The contributions are threefold: (1) **MultiID-2M**, a large-scale paired dataset of ~500k multi-person images with reference banks (~3k identities, ~400 images each) together with ~1.5M unpaired group photos; (2) **MultiID-Bench**, a benchmark that quantifies copy-paste via the M_CP metric (Eq. 2) and uses Sim(GT) rather than Sim(Ref) as the primary identity metric; and (3) **WithAnyone**, a FLUX-based model trained with paired data, a GT-aligned ID loss, and an ID contrastive loss with extended negatives, which substantially reduces copying while maintaining high identity similarity. Evaluation against 14 baselines (Tables 1–2) shows WithAnyone achieves a favorable position on the fidelity–copying Pareto frontier.

## Strengths

1. **The copy-paste artifact is a genuinely important and well-motivated problem.** The paper formalizes a phenomenon that prior work discussed only qualitatively, providing clear evidence (Fig. 2 density plot) that models like InstantID produce an unnatural spike at Sim=1.0 while real face pairs show a broad distribution. This problem framing is sound and fills a recognized gap.

2. **MultiID-2M fills a real data bottleneck.** The scarcity of paired multi-image-per-identity data has forced the field into reconstruction-based training, which the paper correctly identifies as a root cause of copy-paste. The four-stage collection pipeline (Sec. 3) is well-specified, reproducible, and yields a resource (~500k paired group photos with reference banks) that should benefit future work.

3. **MultiID-Bench's evaluation design is principled.** The insight that Sim(Ref) rewards copying is correct, and shifting to Sim(GT) as the primary metric (Sec. 4) is a meaningful methodological improvement. The M_CP metric (Eq. 2) formalizes the reference-bias vs. ground-truth-fidelity trade-off in a clean, normalized way that prior work lacked.

4. **The empirical evaluation is broad and transparent.** Tables 1 and 2 compare 14 models on both single- and multi-person subsets, covering general-purpose customization models, face-specific models, and proprietary systems (GPT-4o). The paper acknowledges where GPT-4o outperforms WithAnyone and explains why (GPT's prior knowledge of celebrity identities). The ablation study (Table 3) isolates key components.

## Weaknesses

### Fatal
None.

### Major

1. **The "breaking the trade-off" claim is overstated.** The paper asserts (Abstract, line 23; Conclusion, line 303) that WithAnyone "breaks the long-observed trade-off between fidelity and artifacts," implying a fundamentally different regime. The data does not support this. In Table 1 (single-person), WithAnyone (Sim(GT)=0.460, CP=0.144) achieves a *favorable Pareto point* — better CP than InstantID (0.337) at comparable Sim(GT) (0.464) — but this is a shift along the curve, not a departure from it. In the multi-person setting (Table 2), DreamID achieves CP=0.079 (2-people) and 0.116 (3–4 people) — far lower than WithAnyone's 0.161/0.171 — at the cost of lower Sim(GT). These are *different points on the same trade-off curve*. The paper's own Fig. 5 shows WithAnyone as an outlier from the regression line, which is a real achievement, but claiming the trade-off is "broken" is imprecise and invites unnecessary skepticism. A more accurate characterization is that WithAnyone achieves a **better Pareto frontier position** among face-specific models.

### Minor

2. **Selective reporting of the ablation's within-method trade-off.** In Table 3, removing extended negatives ("w/o Ext. Neg.") yields CP=0.074 — the *lowest* (best) copy-paste score in the entire ablation, substantially better than the full model's 0.161. The paper (line 285) describes the effect only as "the effectiveness of ID contrastive loss is greatly reduced" (referring to the Sim(G) drop from 0.405 to 0.368), without mentioning that CP improves markedly. This is the same fidelity-vs-copying trade-off the paper claims to have broken, now appearing inside the method's own loss components. The data is fully visible in the table, so this is a framing issue rather than a factual error, but it undermines the "breaking the trade-off" narrative.

3. **DreamID is not discussed in multi-person results.** In Table 2, DreamID achieves CP=0.079 (2-people) and 0.116 (3–4 people) — substantially lower than WithAnyone's 0.161/0.171 — while trading off Sim(GT) (0.389 vs. 0.405 for 2-people). DreamID is never mentioned in the text. Since it is the only face-specific baseline with CP near the 0.1 range in multi-person settings, some explanation of where its low CP comes from would clarify the comparison landscape.

4. **User study has limited reporting.** Only 10 participants were recruited, and no inter-annotator agreement metric is reported. Participants ranked 230 groups across four criteria, which is a substantial cognitive load. The bubble chart (Fig. 8) uses method names ("Cure", "iDetch", "Uniformal") that do not match the nomenclature in the main tables, making it unclear which methods were compared. The paper states the copy-paste metric shows "moderate positive correlation with human judgments" but reports no correlation coefficient.

5. **M_CP normalization limitation not discussed.** When the reference and ground-truth embeddings have very low similarity (large θ_tr in Eq. 2), the denominator becomes large and M_CP compresses toward zero regardless of the generated image's position. The paper conditions on Sim(GT)>0.40/0.35 to filter such cases, which is a pragmatic choice, but this behavior and its implications for score interpretation should be acknowledged.

6. **ArcFace matching threshold not justified.** The dataset construction pipeline (Sec. 3, line 63) uses a cosine similarity threshold of 0.4 for matching faces to reference identities, but no sensitivity analysis or validation of this threshold is provided. Dataset quality and composition depend on this choice.

7. **Identity count could be clarified.** The paper reports "~25k unique identities" (line 63) for the total dataset and "~3k identities" (line 51) for the reference bank. The distinction between reference-bank identities and total detected identities is present in the text but could confuse readers without careful parsing.

### Trivial

8. **Placeholder name in user study figure.** Fig. 8's caption and axis labels use "Cure" instead of "WithAnyone," and the other method names ("iDetch", "Uniformal") do not match the main tables. This appears to be a copyediting oversight.

## Nice-to-Haves

- **Finer-grained pipeline ablation.** The four-phase pipeline is presented as a core contribution, but only Phase 3 is ablated. Individual ablations of Phases 1, 2, and 4 would clarify which design decisions matter.
- **Isolating the dataset contribution.** A cleaner experiment would be: train the model with paired data but without the GT-aligned ID loss and contrastive loss, to isolate what the paired dataset alone achieves vs. what the losses add.
- **Failure case analysis.** The paper shows successful generations but does not discuss failure modes (e.g., extreme poses, heavy occlusion, out-of-distribution identities).
- **Inference cost comparison.** Reporting sampling steps, latency, and throughput relative to baselines would be useful for practitioners.

## Removed Points

These points were identified in the input review but are either factually incorrect, speculative, or not standard requirements for this paper type:

- **Fig. 2 evidence insufficient:** The critic claimed "a single example with substantial score variance is not robust evidence." The paper actually shows a 3D density plot comparing distributions across multiple models (InstantID, PuLID, etc.) alongside the example images. Removed because the criticism misreads the figure.
- **GT-aligned ID loss creates training-evaluation leak:** The critic argued this inflates evaluation metrics. The paper uses GT landmarks purely as a training-time technique to stabilize ArcFace embedding extraction from noisy diffusion outputs. The evaluation measures final generated images against GT using standard metrics — there is no information leak. Removed as speculative.
- **No inference cost comparison / Missing related work / Reproducibility nitpicks:** Removed per filtering rules as not standard requirements or not verifiable.

## Novel Insights

The most insightful observation from the review process is that the paper's own ablation (Table 3) inadvertently provides the strongest counter-evidence to its central claim: when the ID contrastive loss is weakened by removing extended negatives, copy-paste drops to CP=0.074 (the best in the table) while similarity drops modestly (Sim(G)=0.368 vs. 0.405). This reveals that the trade-off between fidelity and copying persists within the method itself — the extended negatives improve identity discrimination but worsen copy-paste. The paper would be stronger by acknowledging this and framing the contribution as managing this trade-off more effectively rather than claiming to eliminate it. Additionally, the fact that DreamID achieves CP=0.079 on 2-people (vs. WithAnyone's 0.161) suggests that very different architectural or training choices can also push CP very low at some similarity cost, which warrants discussion.

## Suggestions

1. **Reframe the central claim.** Replace "breaking the long-observed trade-off" with a precise statement about achieving a better Pareto frontier position among face-specific models. This is not a weaker claim — it is more defensible and better supported by the evidence.
2. **Acknowledge the within-method trade-off openly.** In the ablation discussion, note that removing extended negatives reduces CP (from 0.161 to 0.074) while also reducing Sim(G) (from 0.405 to 0.368), and explain this as the expected behavior of the trade-off the method operates within.
3. **Discuss DreamID in the multi-person results.** Even a brief sentence explaining what DreamID does and why its CP is so much lower would clarify the comparison.
4. **Report an inter-annotator agreement metric** for the user study (e.g., Fleiss' kappa) and fix the mismatched names in Fig. 8.
5. **Add a brief limitation paragraph** (beyond the ethics statement) discussing when WithAnyone might fail or underperform.

## Score and Decision

**Calibration anchors (retrieved from corpus):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| ID-Booth (NWvsm2VxAM) | 3.00 | R1, reject | Minor extension of PortraitBooth with marginal gains; our paper has far more substance |
| Event-Customized (88Qm4fGWzX) | 5.00 | R1, reject | New task + dataset but limited novelty; our paper has stronger evaluation and clearer problem |
| Subject-Diffusion (qZB7KDN4L1) | 5.00 | R2, reject | Dataset + method, but concerns about limited novelty and overclaiming; our paper has more principled evaluation metrics |
| UIFace (riieAeQBJm) | 6.00 | R1, accept | Solid face recognition data generation; comparable to our paper in substance |
| InstantPortrait (ZkFMe3OPfw) | 6.67 | R1, accept | One-step portrait editing with impressive results; slightly more polished than our paper |

**Bracket:** R1 bracketing placed the paper in the 5.5–7.5 range. R2 narrowed to 5.5–6.5 based on comparison with Subject-Diffusion (5.00) and UIFace (6.00). Our paper is stronger than Subject-Diffusion due to more principled evaluation and clearer problem framing, and comparable to UIFace in overall substance. The overclaiming issue is the primary factor preventing a higher score.

**Final score:** 6.0 — The paper makes genuine, practically useful contributions (dataset, benchmark, method) with a thorough evaluation. The core findings are reproducible in spirit and the approach is well-motivated. However, the central narrative claim ("breaking the trade-off") is overstated and not fully supported, and the ablation reporting is selectively framed. These are framing and presentation issues, not structural flaws, and are addressable in revision.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>