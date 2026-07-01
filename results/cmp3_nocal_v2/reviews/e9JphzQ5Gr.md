## Summary

CaPT (CLIP as a Prior Teacher) is a framework that integrates CLIP into semi-supervised learning through asymmetric-modalities co-training between a fully fine-tuned unimodal vision network (UPM) and a parameter-efficiently adapted multimodal CLIP model (MPM). A prediction fusion module (PFM) combines their pseudo labels via entropy-based weighting to form co-pseudo labels that supervise both branches. The paper also provides theoretical analysis (Theorem 1.1) characterizing SSL's label dependency under a prototype-based model. Empirically, CaPT shows strong results on USB benchmarks, ImageNet, and fine-grained datasets, especially under extreme label scarcity.

## Strengths

1. **Well-designed co-training architecture with thorough ablations.** Table 6 systematically ablates CaPT against CaPT-Ada (CLIP-Adapter alone), CaPT-Deb (DebiasPL-style, no adapter tuning, no back-flow to CLIP), CaPT-Uni (no back-flow from ViT to CLIP), "only UPM," and "only MPM." The 12.73% gap between CaPT-Deb and CaPT on EuroSAT (83.87% vs. 96.60%) cleanly demonstrates that adapter-tuning to correct CLIP's biased prior is essential. These ablations, along with the "only UPM" and "only MPM" comparisons, constitute the paper's strongest evidence that the full co-training design adds value over simpler CLIP-integration strategies.

2. **Genuinely impressive efficiency.** Adding a full CLIP model (with adapters, feature-level Mixup augmentations) to the SSL pipeline costs only 8% more memory and 11% more time over FreeMatch alone (Table 4: 5050 MiB vs. 4676 MiB, 0.1044 s/iter vs. 0.0939 s/iter). The feature-level Mixup (rather than input-level) for CLIP's strong augmentations is a sensible design choice that avoids reprocessing images at CLIP's native resolution.

3. **Theoretical grounding of the label-dependency problem.** Theorem 1.1 formalizes how pseudo-label error in standard SSL is bounded by labeled-data quantity and quality under a prototype-based Gaussian mixture model. While the theorem analyzes the problem rather than the solution, it provides a clean motivation for why an external source of prior knowledge (such as CLIP) is needed.

4. **Consistent benefits across diverse benchmarks.** CaPT outperforms baselines on CIFAR-100, STL-10, EuroSAT, ImageNet, and five of six fine-grained datasets (Table 5). The one exception (FGVCAircraft) is honestly acknowledged in the conclusion.

## Weaknesses

### Major

- **The headline empirical claims compare across fundamentally different information regimes.** The abstract's "21.38% improvement" and the introduction's "state-of-the-art" framing rest on comparing CaPT (which uses CLIP, trained on 400M image-text pairs) against 12 SSL methods (FixMatch, FreeMatch, RegMixMatch, etc.) that use only a standard ViT backbone without any vision-language model. While the paper does provide CLIP-using ablations (CaPT-Ada, CaPT-Deb, CaPT-Uni) in Section 4.5 — which are the right kind of control — these are presented as secondary analysis rather than the primary evidence. The paper would be stronger if the CLIP-using ablations were the centerpiece of the experimental section and the non-CLIP baselines were presented as context. A **critical missing baseline** that would isolate the value of the co-training mechanism: independently train the UPM (with FreeMatch) and the MPM (adapter-tuned CLIP) separately, then combine their predictions at test time via the same entropy weighting. Without this, it is unclear whether CaPT's co-training loop provides meaningful benefit beyond a post-hoc ensemble of independently trained models.

### Minor

- **Theorem 1.1 does not analyze the proposed method.** The theorem bounds pseudo-label error under a prototype-based model for *standard SSL* — it identifies the label-dependency problem but says nothing about CaPT's error, does not bound how CaPT's co-training mechanism reduces effective bias, and does not predict when CaPT will succeed or fail. It is clean but purely motivational. The paper's contribution claim "We identify and theoretically establish the label dependency" is accurate, but the theory does not support the method itself.

- **The STL-10 result reveals an undiscussed dynamic.** On STL-10 with 4 labels/class (Table 1), CaPT's UPM (96.07%) underperforms both adapter-tuned CLIP alone (96.86%) and CLIP zero-shot (97.18%). Since the paper reports CaPT's final accuracy using the UPM, this means the UPM after co-training does not reach CLIP's level, even though it vastly outperforms the best non-CLIP baseline (RegMixMatch, 89.89%). The paper does not discuss this case, which would help characterize when the co-training mechanism successfully transfers all of CLIP's knowledge versus when it falls short.

- **The resource comparison against RegMixMatch is not fully controlled.** Table 4 shows CaPT using less memory and time than RegMixMatch (5050 vs. 6578 MiB; 0.1044 vs. 0.1484 s/iter), even though CaPT runs two models (UPM + CLIP) while RegMixMatch runs only one. The paper does not break down what each method's resource footprint includes (e.g., different optimizer components, augmentation pipelines, SAM usage — note that FlatMatch, not RegMixMatch, uses sharpness-aware minimization). An apples-to-apples comparison controlling for these factors would make the efficiency claim cleaner.

- **Main-paper support for the asymmetric-modalities claim is primarily qualitative.** Figure 3 shows attention maps suggesting CLIP attends to different regions than pure-vision ViTs. The paper references Appendix B for quantitative experiments (which the original submission contains), but the main paper would benefit from even a simple quantitative measure (e.g., prediction disagreement rates or representation similarity) to substantiate the claim that asymmetric modalities provide more diverse views than symmetric co-training.

### Trivial

- Figure 1a's legend includes "CaPT" alongside SSL methods in a motivating plot about SSL's limitations. Since CaPT uses CLIP, including it in this motivating comparison is slightly inconsistent with the text, which only discusses SSL methods.

## Nice-to-Haves

- Add the independent-ensemble baseline (train UPM and MPM separately, combine at test time) to isolate whether the co-training loop provides benefit beyond post-hoc combination.
- Include a quantitative measure of cross-modal complementarity (e.g., CKA similarity, prediction disagreement) in the main paper alongside the qualitative attention maps.
- Discuss the STL-10 result explicitly: why does the UPM not reach CLIP's level on this dataset, and what does this tell us about when CaPT's mechanism is most effective?

## Removed Points

These points were flagged for removal. Treat them with caution — they were not included in the main review above because they are incorrect, speculative, or reflect rules about parser-stripped content:

1. **"Threshold specification missing"** — REMOVED. The paper explicitly states: "We adopt the adaptive threshold strategy from FreeMatch to filter pseudo labels, as in RegMixMatch" (line 206).
2. **"No discussion of CLIP backbone choice"** — REMOVED. The paper states: "ViT-B/32 is employed as the visual encoder for CLIP" (line 206).
3. **"Number of runs not reported"** — REMOVED. The paper states: "Each algorithm is trained three times with different random seeds" (line 206).
4. **"Missing related work on pre-trained models in SSL"** — REMOVED per rules (no external sources to verify existence).
5. **"Asymmetric-modalities claim is quantitatively unsupported"** — REMOVED. The paper states experiments are in Appendix B, which the parser strips. However, the qualitative-only nature in the main paper was noted as a Minor weakness above.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Reframe the primary experimental evidence around the CLIP-using ablations (CaPT-Ada, CaPT-Deb, CaPT-Uni, only UPM, only MPM) and present non-CLIP SSL comparisons as context. This would better match the paper's actual contribution: "a framework for integrating VLMs into SSL."
2. Add the independent-ensemble baseline to demonstrate that the co-training loop itself adds value beyond post-hoc combination of separately trained models.
3. Include a brief discussion of the STL-10 case (UPM < CLIP) alongside the FGVCAircraft limitation, to characterize when co-training fully transfers CLIP's knowledge versus when it does not.
4. Provide a breakdown of what contributes to RegMixMatch's resource consumption so the efficiency comparison is transparent.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>