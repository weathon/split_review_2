## Summary

SpatialBoost enhances pre-trained vision encoders (DINOv3, SigLIPv2, etc.) with 3D spatial understanding by converting geometrically extracted spatial information (depth, segmentation, 3D point clouds) into hierarchical multi-turn Chain-of-Thought QA pairs, then fine-tuning the vision encoder through an LLM with dual-channel attention. The method is evaluated across an unusually broad set of tasks: depth estimation, semantic segmentation, 3D scene understanding, robot control, classification, and retrieval.

## Strengths

- **Experimental breadth is unusually thorough.** The paper evaluates on 8+ distinct task families (monocular depth, semantic segmentation, 3D vision-language reasoning, visual grounding, geometric understanding, 3D semantic understanding, robot control over 4 domains, classification, and retrieval) using 4 different vision encoder families (OpenCLIP, SigLIPv2, DINOv2, DINOv3). This scope demonstrates serious empirical effort.

- **The ablation studies are informative and well-structured.** Table 7 cleanly shows that the forward hierarchical ordering (pixel → object → scene) outperforms reverse and random orders, and that combining single-view and multi-view data is beneficial. Table 8 provides a direct comparison against "Simple FT" (fine-tuning on the same data with original pre-training objectives), and Figure 6 systematically evaluates the dual-channel attention mechanism against full fine-tuning and LoRA.

- **Consistent positive results across diverse settings.** SpatialBoost improves nearly every evaluated metric across all backbones and tasks, including tasks not requiring spatial understanding (ImageNet classification, image retrieval), which the paper's dual-channel attention mechanism explains as preservation of pre-trained knowledge.

- **The multi-turn hierarchical spatial reasoning dataset is a principled contribution.** The three-level hierarchy (pixel-level positions → object-level 3D bounding cubes → scene-level inter-object distances) is a well-motivated design for structured spatial knowledge injection through language.

## Weaknesses

### Fatal

None.

### Major

1. **ScanNet training/evaluation overlap is unaddressed in the main text.** The multi-view VQA training data (Stage 2, Section 4.1) is constructed from "3D dataset (Jensen et al., 2014; **Dai et al., 2017**; Mildenhall et al., 2021; Barron et al., 2022)" — Dai et al., 2017 is ScanNet. Table 3 evaluates on ScanNet scenes (via the Lexicon3D benchmark). The paper states no explicit separation protocol between ScanNet images used for training and those reserved for evaluation. The improvements for models with initially poor 3D understanding are very large (OpenCLIP 3D semantic mIoU: 6.9→54.9; SigLIPv2: 9.2→55.5). While standard practice would be to use official train/val splits, the paper must state this explicitly in the main text. Table 3 results cannot be properly interpreted without this clarification. *The appendix (Section D, stripped by the parser) may address this, but the main text should be self-contained on this point.*

2. **The spatial-content vs. additional-data confound is only partially addressed.** SpatialBoost trains on 300K images with rich QA supervision, and tasks that do not require spatial understanding also improve (e.g., DINOv3 ImageNet linear probing: 88.4→90.2). Table 8 ("Simple FT") provides a control using the same data with original pre-training objectives, which shows much smaller gains, supporting the claim that the spatial content matters. However, the cleanest control — training on an equivalent volume of *non-spatial* VQA data at the same scale — is missing. Table 7 partially mitigates this by showing that the ordering of multi-turn data (forward > reverse > random) affects quality, which suggests spatial structure is causal. But the core concern remains: some fraction of the gains may come from additional training on any well-structured supervision, not specifically from spatial knowledge.

### Minor

3. **No standard errors or confidence intervals in Tables 1, 2, 3, and 5.** Only Table 4 (robot learning) reports ± ranges. For a paper making comparative claims about relative improvements across multiple backbones and tasks, readers need some measure of variability to assess whether improvements are significant.

4. **The generated spatial training data relies on imperfect off-the-shelf models without quality analysis.** The pipeline extracts depth (Depth Pro), segmentations (SAM), and 3D point clouds (VGGT), then feeds these into GPT-4o to generate QA pairs. Each component has well-documented failure modes (depth errors on reflective surfaces, segmentation boundary errors, reconstruction drift). The paper does not report agreement rates against human annotations, calibration statistics, or any error analysis of the generated training signal. This is a gap in establishing the fidelity of the injected spatial knowledge.

5. **No limitations section.** The paper concludes without discussing any limitations. Important limitations include: reliance on imperfect off-the-shelf models for generating spatial ground truth; the computational cost of the three-stage pipeline; the unresolved ScanNet split question; and the fact that the spatial-content vs. data-volume confound is not fully resolved.

6. **Table 6 ("Effect of LLM-based fine-tuning") compares across unequal supervision formats.** The LLM-based decoder is trained on the full multi-turn spatial QA dataset, while the linear/SAM/VGGT decoders are trained on single-task objectives (depth or segmentation). It would be fairer to provide the pixel-level decoders with the same multi-turn information (e.g., converted into pixel-level targets). As presented, the comparison conflates supervision format with supervision quality.

### Trivial

7. **Factual error in Section 4.3.** Line 199 states "SigLIPv2's 3D semantic segmentation dramatically improves from 6.9 to 54.9 mIoU," but Table 3 shows these values are for OpenCLIP (SigLIPv2 goes from 9.2 to 55.5).

## Nice-to-Haves

- A controlled experiment training on an equivalent volume of non-spatial VQA data (e.g., generic scene captions) would cleanly disambiguate spatial-content effects from additional-training effects.
- Error analysis of the generated spatial dataset, including agreement rates with human annotations on a held-out sample.
- Analysis of which spatial reasoning level (pixel/object/scene) contributes most to each downstream task.

## Removed Points

These points appeared in the input review but are removed with justification:

- **"12 multi-turn conversations" concern** — The critic noted the number "12" seems small, but correctly inferred that each of the 300K images yields one 12-turn conversation. This is not a substantive issue; the paper's Figure 2 caption already states this.
- **Dual-channel attention attribution** — The critic notes the paper attributes dual-channel attention to Hong et al., 2023a, and suggests readers might infer it's novel. The paper clearly cites the source; no confusion exists.
- **"Existing methods fail to learn 3D relationships" is too broad** — This is a framing nuance in the abstract, not a technical weakness. The paper also acknowledges DINOv2/DINOv3 baselines already have moderate 3D understanding.
- **Multi-modal claim about joint pre-training overstated** — This concerns a sentence in Related Work, not the paper's core claims.
- **Critical Issue 3 (imperfect models) upgraded from major concern** — The critic framed this as a major methodological gap. It is standard practice in data-generation pipelines to use off-the-shelf models, and the paper's approach does not claim the generated data is perfect ground truth. Downgraded to Minor (point 4 above) and Nice-to-Have.

## Novel Insights

None beyond the paper's own contributions. The input review does not surface any observation about the method or results that the authors themselves do not provide.

## Suggestions

1. In the main text, explicitly state whether any ScanNet scenes used for evaluation were also present in the multi-view training data, and describe the separation protocol. If standard dataset splits were used, say so.
2. Add a control experiment where the vision encoder is fine-tuned on an equivalent volume of non-spatial VQA data (e.g., VQAv2 captions or generic scene captions at the same 300K scale). This would directly test whether spatial content is causal.
3. Report standard deviations or confidence intervals for the main results tables.
4. Add a limitations section discussing: reliance on imperfect off-the-shelf models, computational cost, and the spatial-content vs. data-volume confound.
5. Correct the factual error in Section 4.3 (line 199: OpenCLIP, not SigLIPv2, achieves the 6.9→54.9 improvement).

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Reject</decision>