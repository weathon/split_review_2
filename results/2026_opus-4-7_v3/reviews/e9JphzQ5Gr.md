Now let me verify a few more specific claims in the paper before drafting my review.Now I have enough information to draft the review. Let me compile my findings and create the draft.Now let me run calibration search Round 1 to bracket the score:Let me read a few of the most relevant anchor papers to calibrate:Now I have enough calibration data. Let me form my bracket and write the final review.

**Round 1 bracket analysis:**
- Score < 3.5 (reject band): Papers like "Weak-to-Strong CLIP" (3.33) with single-dataset evaluation and unclear contribution. CaPT is far stronger.
- Score 3.5-5.5 (borderline reject): Papers like "Cleaning label noise with VLMs" (4.50) with results inferior to SOTA. CaPT's results are substantially better.
- Score 5.5-7.5 (borderline accept): SemiCLIP (5.80) — also semi-supervised CLIP training with moderate gains, accepted. CaPT shows stronger empirical gains and more thorough evaluation.
- Score 7.0+ (accept): "Black Sheep" (7.0), "CLIPSelf" (7.0) — strong novel insights with extensive evaluation.

**Initial bracket: 5.5–7.0.** CaPT has stronger results than SemiCLIP (5.80) but the framing overclaim and missing CLIP-based baselines in main tables are real issues. 

Now let me write the final consolidated review.

---

## Summary
CaPT proposes an asymmetric-modalities co-training framework that integrates a parameter-efficiently fine-tuned CLIP model with a fully fine-tuned unimodal vision network for semi-supervised learning (SSL). Entropy-weighted co-pseudo labels enable bidirectional knowledge exchange between the two branches. The paper motivates the problem with both a theoretical result (Theorem 1.1) and compelling empirical evidence showing SSL's label dependency, and demonstrates strong gains in extreme low-label regimes (e.g., +21.38% on CIFAR-100 with 1 label/class over RegMixMatch).

## Strengths
- **Label-dependency observation is well-grounded and insightful.** Figure 1c's heatmap showing that SSL's accuracy gain from unlabeled data nearly vanishes in the one-label-per-class regime on CIFAR-100 goes beyond the trivial "less labels = worse" observation. It demonstrates the *coupling* between labeled data quality and unlabeled data utility, which is the paper's core motivation.

- **Framework achieves strong gains with modest overhead.** Table 4 shows only 8% additional memory (5050 vs 4676 MiB) and 11% additional training time (0.1044 vs 0.0939 sec/iter) over FreeMatch, while gaining +6.23% accuracy on CIFAR-100 at 2 labels/class. The design choice to freeze CLIP encoders and use lightweight adapters combined with feature-level Mixup is pragmatic and well-justified.

- **Ablation study (Table 6) is thorough and well-designed.** It isolates five distinct design axes: co-training structure (CaPT-Uni: −0.88%), adapter-tuning (CaPT-Deb: −3.80%/−12.73%), CLIP-Adapter only (CaPT-Ada: −16.40%), individual modules (only UPM: −6.23%, only MPM: −16.51%), feature augmentation (−0.57%), and entropy weighting (−0.87%). These clearly demonstrate that both CLIP's prior and the co-training design are necessary.

- **Performance in extreme low-label regimes is substantial and practically meaningful.** +21.38% on CIFAR-100 with 1 label/class (Table 3: 82.51% vs 61.13%), +9.33% on ImageNet with 10 labels/class (Table 2: 67.68% vs 58.35%). Results span CIFAR-10/100, STL-10, EuroSAT, ImageNet, and 6 fine-grained datasets, providing broad coverage.

## Weaknesses

### Fatal
None

### Major
- **The "breaking label dependency" framing overstates the contribution.** The title and abstract claim CaPT "breaks" label dependency, but the FGVCAircraft results (Table 5) demonstrate that dependency is *transferred* to CLIP's prior quality rather than eliminated. With CLIP zero-shot accuracy at only 18.97% on FGVCAircraft, CaPT underperforms FreeMatch at 5 labels/class (50.12% vs 51.43%) and RegMixMatch at 10 labels/class (64.33% vs 66.21%). The paper acknowledges this limitation only briefly in Section 5 ("CLIP's prior is less informative on certain fine-grained datasets such as FGVCaircraft"), but the title and abstract's central framing remains unqualified. The contribution is real and valuable — efficient integration of VLM priors into SSL — but "mitigates" or "reduces" would be accurate where "breaks" is not.

- **DebiasPL, the most directly comparable CLIP-in-SSL method, is absent from all main comparison tables.** DebiasPL (Wang et al., 2022a) appears only as CaPT-Deb in the ablation (Table 6) on 2 datasets (CIFAR-100, EuroSAT). It is not included in Tables 1–3 or Table 5. This prevents readers from isolating how much of CaPT's advantage over pure SSL methods comes from accessing CLIP at all versus CaPT's specific co-training design across all benchmarks. The ablation partially addresses this (CaPT outperforms CaPT-Deb by 3.80% on CIFAR-100 and 12.73% on EuroSAT), but the limited dataset coverage and the absence from the main experimental narrative weaken the evidential strength of the paper's claimed design contribution.

### Minor
- **STL-10 results reveal an undiscussed anomaly.** In Table 1, CLIP zero-shot achieves 97.18%, adapter-tuned CLIP achieves 96.86%/97.15% (4/10 labels), but CaPT's reported unimodal network result is 96.07%/96.34% — lower than CLIP without any labeled data. The co-training appears to degrade CLIP's performance on this dataset, and the reporting convention (unimodal branch only, per Section 4.1) obscures that the system contains a better-performing branch. This anomaly is worth discussing, as it reveals a regime where the co-training framework may not produce synergy.

- **Missing variance/confidence intervals for 1-label-per-class results (Table 3).** Tables 1 and 2 report standard deviations across random seeds, but Table 3 — the paper's headline results — does not. The 1-label-per-class setting is precisely where variance matters most, since results are highly sensitive to which specific sample is selected as the sole labeled example.

- **Batch-level entropy weighting (Eq. 11–12) lacks justification over per-sample alternatives.** All samples in a batch receive identical module weights Γᵃ and Γᵇ, regardless of per-sample confidence variation. The paper does not discuss why batch-level averaging was chosen over per-sample weighting, which would be a natural alternative for samples with heterogeneous confidence.

### Trivial
None

## Nice-to-Haves
- Testing with an alternative VLM (e.g., SigLIP, EVA-CLIP) would substantiate the Section 5 claim that CaPT is "future-proof" and that "more powerful VLMs can be seamlessly incorporated."
- An empirical curve showing the entropy weights Γᵃ and Γᵇ over training iterations would directly verify the claimed dynamic shift from CLIP-dominated to unimodal-dominated supervision.
- Theorem 1.1 motivates the problem but does not guide the solution design (nothing in CaPT's architecture — entropy weighting, adapters, feature Mixup — follows from the theorem's structure). The paper would be equally well-motivated by Figure 1 alone; connecting the theorem to specific design choices would strengthen its relevance.
- Discussion of adaptive branch selection (when CLIP already dominates on a dataset, should the system report the better-performing branch?) would provide practical deployment guidance.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Asymmetric baseline resources as unfair comparison:** While CaPT brings CLIP's ~400M-pair pre-training against methods using only ImageNet-pretrained ViTs, the paper's explicit contribution is about integrating VLM priors into SSL — comparing against standard SSL methods is the natural evaluation for this premise. The ablation (Table 6) partially isolates the design contribution. This would only be a real issue if the paper claimed to be a better SSL method *without* additional resources, which it does not.

- **Textual adapter naming (Section 3.2.1):** The reviewer noted that Aₜ is "just a learnable bias" rather than an architectural adapter. The paper accurately describes it as "a learnable parameter initialized to zero and of the same shape as W" (Eq. 7) — this is a terminology preference, not a substantive issue.

- **Missing FGVCAircraft discussion in main text:** The paper does address this: "Except for FGVCAircraft (discussed in Appendix N)" (Section 4.4) and "CLIP's prior is less informative on certain fine-grained datasets such as FGVCaircraft" (Section 5). The appendix discussion was stripped by the parser.

- **Demand for comparison with CLIP linear probing or CLIP pseudo-label augmentation:** These are reasonable alternative approaches but are outside the paper's stated contribution of a co-training framework. The ablation variants (CaPT-Ada, CaPT-Deb) already cover CLIP-only and CLIP-as-preprocessor baselines.

- **Reproducibility concerns about CLIP model variant, text templates, adapter bottleneck dimension:** These details are noted as being in Appendix F, which was stripped by the parser.

## Novel Insights
The paper's key novel insight is that asymmetric-modality co-training (vision-language + unimodal vision) naturally avoids the pattern-homogeneity bottleneck of same-architecture co-training, providing a principled rationale grounded in Blum & Mitchell's (1998) co-training theory for why CLIP integration via co-training outperforms simpler integration strategies like DebiasPL. The attention map visualization (Figure 3) concretely demonstrates that CLIP's representations diverge substantially from unimodal ViTs, validating the theoretical motivation. The entropy-based fusion mechanism that transitions supervision dynamically from CLIP-dominated to unimodal-dominated training is a practically useful design pattern for future VLM-SSL integration work.

## Suggestions
- Include DebiasPL as a baseline in Tables 1–3 and 5. This is the single most impactful change — it would let readers isolate CaPT's co-training design contribution from the contribution of simply having access to CLIP.
- Address the STL-10 anomaly directly: discuss when co-training adds value vs. when CLIP already saturates performance, and consider an adaptive branch-selection mechanism.
- Report variance for 1-label-per-class results (Table 3) across multiple seed/sample selections.
- Reframe the title and abstract from "breaking" to "mitigating" or "reducing" label dependency — the FGVCAircraft results make the current framing indefensible.
- Show Γᵃ/Γᵇ curves over training iterations to empirically verify the claimed supervision transition dynamics.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to CaPT |
|-------|------|-----------|-------|---------------------|
| Semi-Supervised CLIP Training (SemiCLIP) | 97D725GJtQ | 5.80 | R1 | Most similar topic; CaPT has stronger gains (+21% vs +6.58%), broader evaluation, better ablation |
| Cleaning label noise with VLMs | 1rgMkDWfYV | 4.50 | R1 | Uses CLIP for noise labels; weaker results, less clear method. CaPT is substantially better |
| Weakly Supervised Learning with Pre-Trained Models | RgWATMmWmz | 4.75 | R1 | Also uses CLIP for weak supervision with dual heads; CaPT has clearer contribution and stronger results |
| Weak-to-Strong CLIP Classification | FwkYeLovHk | 3.33 | R1 | Single-dataset, unclear practical value; far below CaPT's quality |
| Annotation Bootstrapping | PD8JVDg8mB | 4.25 | R1 | Uses pre-trained models for visual learning; more limited evaluation than CaPT |
| ClipGrader | 1GPN2oa7P7 | 4.20 | R1 | CLIP for label quality assessment; narrower scope, CaPT is stronger |
| Image Clustering via Rate Reduction | ptCIlV24YZ | 5.80 | R1 | Uses CLIP features for clustering; different task, similar quality level but CaPT has more practical impact |
| Black Sheep (Spurious Attributes) | g1fkhbhHjL | 7.00 | R1 | Strong novel insight + extensive experiments; CaPT has comparable experimental breadth but framing issue prevents it from reaching this level |
| CLIPSelf | DjzvJCRsVf | 7.00 | R1 | Novel distillation approach; clear contribution without overclaiming. CaPT's overclaimed framing is a disadvantage |
| Compositional Entailment Learning | 3i13Gev2hV | 8.00 | R1 | Highly novel contribution; CaPT does not reach this level of novelty |
| Two Effects One Trigger | uAFHCZRmXk | 8.00 | R1 | Deep analysis paper; different genre from CaPT |
| Interpreting CLIP's Image Representation | 5Ca9sSzuDp | 8.00 | R1 | Strong interpretability work; different scope |
| Visual Data-Type Understanding | WyEdX2R4er | 8.00 | R1 | Benchmark/analysis paper; different scope |
| Strong reject anchors (gwZ90hFSL2, 5lUdTogEL3, 5kMwiMnUip) | various | 1.0-1.4 | R1 | Fundamentally flawed papers; CaPT is far above this level |
| IC-Light (misscored in retrieval) | u1cQYxRI1H | 10.0 | R1 | Retrieved anomalously; not comparable |

**Round 1 bracket:** 5.5–7.0

**Narrowing rationale:** CaPT clearly exceeds SemiCLIP (5.80) in empirical strength: broader evaluation, larger gains, better ablation, and practical efficiency analysis. However, CaPT falls short of the 7.0-scored papers (Black Sheep, CLIPSelf) which present cleaner contributions without overclaimed framing. The two major weaknesses — overclaimed "breaking" framing contradicted by FGVCAircraft, and missing DebiasPL from main tables — are real but addressable in revision. The contributions are solid: the label-dependency observation is well-grounded, the framework is efficient and well-designed, the ablation is thorough, and the results are impressive. The paper is a borderline accept that would benefit from honest reframing and one additional baseline.

**Final score: 6.0**

The paper presents a practical and well-engineered framework with strong empirical results, but the overclaimed central framing and the missing most-comparable baseline in main experiments prevent a higher score. The contribution is genuine — integrating VLM priors into SSL efficiently via asymmetric co-training — but the evidence as presented does not fully isolate CaPT's design contribution from the contribution of simply having access to CLIP. A revised version with honest framing and DebiasPL in main tables would likely be a clear accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>