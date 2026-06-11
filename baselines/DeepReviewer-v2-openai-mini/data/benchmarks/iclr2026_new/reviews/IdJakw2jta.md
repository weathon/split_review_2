## Summary
# Final Review Report

## Summary

This paper introduces Long-Form Spatio-Temporal Video Grounding (LF-STVG), extending the conventional STVG task to videos of 1–5 minutes, significantly longer than existing benchmarks (20–35 seconds). The authors propose ART-STVG, an autoregressive transformer framework that processes video frames sequentially with two memory-augmented decoders (spatial and temporal). Three key technical contributions are claimed: (1) memory selection strategies that retrieve relevant historical context for each frame, (2) a cascaded spatio-temporal decoder design that uses spatial grounding features to assist temporal localization, and (3) the autoregressive architecture itself, which avoids the computational bottleneck of processing long videos all at once. On extended HCSTVG-v2 benchmarks, ART-STVG outperforms existing STVG methods (TubeDETR, STCAT, CG-STVG, TA-STVG) across all video lengths (1–5 min), with m.tIoU gains of 0.7% (1 min) to 9.1% (3 min) over the best prior method. Ablation studies confirm the contribution of each component. On short-form STVG (20-second videos), ART-STVG achieves competitive results (59.2 m.tIoU vs. 60.4 SOTA). The paper addresses a relevant practical gap and provides systematic evaluation, but has notable limitations in experimental scope (single dataset), missing implementation details (loss function, memory threshold), notation issues in key equations, and a conclusion that lacks limitations and future work.

## Strengths
1. **Well-motivated problem.** The paper identifies a genuine gap between current STVG research (focused on <1 minute videos) and real-world applications (minutes to hours). The LF-STVG problem formulation is timely and practically relevant for video surveillance, retrieval, and long-form video understanding.

2. **Clean architectural design.** The autoregressive streaming approach is a natural fit for long videos — processing one frame at a time with constant per-step memory. The separation of spatial and temporal decoders with a cascaded connection is conceptually intuitive: spatial localization provides object-level cues that inform temporal event boundary detection.

3. **Comprehensive experimental evaluation.** The paper extends HCSTVG-v2 to five video length regimes (1–5 min) and compares with four prior STVG methods plus an ablated baseline. The ablations systematically cover: temporal memory selection, spatial memory selection, cascaded vs. parallel decoder design, number of selected memories (N_s), and training video length. This level of ablation is thorough and helps validate individual design choices.

4. **Clear and consistent performance trend.** ART-STVG outperforms all baselines on all LF-STVG benchmarks, with the gap increasing as videos grow longer (from +0.7%/0.9% at 1 min to +9.1%/6.8% at 3 min in m.tIoU/m.vIoU). This monotonic improvement pattern provides compelling evidence that the autoregressive design with selective memories is increasingly beneficial for longer videos.

5. **Reproducibility-conscious.** The paper specifies backbone choices (ResNet-101, VidSwin-tiny, RoBERTa-base), training hyperparameters (learning rates, frame rate, image size), and commits to releasing code and models. The baseline architecture is also described (though in supplementary material).

## Weaknesses
### W1. Notation inconsistencies in key equations (Major)
**Location:** Page 1 — Section 3.1, Eq. (1); Section 3.2, Eq. (5).

Eq. (1) uses the same token indexing (f_i^1 through f_i^{H×W}) for both appearance and motion features without distinguishing them, which is ambiguous. After concatenation and self-attention, the paper "deconcatenates" to obtain \tilde{f}_i^a, \tilde{f}_i^m, \tilde{f}_i^t, but the tilde notation collides with the earlier \tilde{f}_i^t used for the concatenated multimodal feature in Eq. (1). More critically, Eq. (5) defines \tilde{f}_i^m = RoI(\tilde{f}_i^m, b_i), using the same symbol for both the input (full-frame motion feature) and output (pooled target feature). This notation collision could cause implementation confusion.

**Impact:** Reduces reproducibility; an implementer may misinterpret the variable roles.
**Suggested fix:** Use distinct notation for pre- and post-pooled features (e.g., \hat{f}_i^m = RoI(\tilde{f}_i^m, b_i)) and clarify the concatenation indexing.

### W2. Unbounded memory bank growth without eviction policy (Major)
**Location:** Page 1 — Section 3.3, Spatial Memory Selection.

The spatial memory bank grows by simply adding query features without removing any existing memories. For a 5-minute video at 3.2 FPS (~960 frames) with K decoder blocks, this yields K × 960 entries. While the selection mechanism picks only the top N_s memories for decoding, the raw bank continues to grow. The paper does not discuss memory eviction, storage costs for longer videos, or retrieval slowdown. For hour-long videos, this could become prohibitive.

**Impact:** Limits scalability claim for very-long videos; architectural detail missing.
**Suggested fix:** Either (a) specify a bound on memory size with an eviction policy (e.g., FIFO, score threshold), or (b) explicitly acknowledge this limitation and state the maximum tested video length where the current design is feasible.

### W3. Single-dataset evaluation with limited generalization evidence (Major)
**Location:** Page 1 — Section 4, Datasets.

LF-STVG evaluation is conducted only on extended HCSTVG-v2. The authors honestly state this is because it is "the only dataset which provides available source videos." However, this means all results come from a single domain (multi-person scenes from YouTube). The training set remains at 20 seconds (only validation is extended), creating a train-test domain shift that may favor ART-STVG's streaming design over methods designed for short videos. The manual review process for extended videos lacks quality criteria, inter-annotator agreement, or filtering statistics.

**Impact:** Limits external validity; results may not generalize to other long-video domains (surveillance, egocentric, movies).
**Suggested fix:** Acknowledge this as a limitation explicitly in the conclusion. Encourage creation of dedicated LF-STVG benchmarks. Report inter-annotator agreement for manual review.

### W4. Conclusion lacks quantitative summary, limitations, and future work (Major)
**Location:** Page 1 — Section 5, Conclusion.

The conclusion is only three sentences and does not mention any quantitative results, limitations, or future work directions. It claims "significantly outperforms other methods" without citing specific numbers. Key limitations (single dataset, low spatial precision at high IoU, unbounded memory, trailing TA-STVG on short-form) are not discussed.

**Impact:** Readers get an incomplete picture of the work's boundaries and next steps.
**Suggested fix:** Expand conclusion to include: (1) best quantitative results (e.g., "23.0% m.tIoU on LF-STVG-3min"), (2) 2–3 specific limitations, (3) concrete future directions.

### W5. Temporal memory selection threshold unspecified (Minor)
**Location:** Page 1 — Section 3.4, Temporal Memory Selection.

The temporal memory selection uses cosine similarities to detect event boundaries at "points with lower similarities." The paper does not specify: (a) the similarity function explicitly in text (though Fig. 4(b) mentions cosine), (b) the threshold or criterion for "lower similarities" (fixed? percentile? adaptive?), (c) what happens when boundary detection fails. This prevents reproduction and analysis of failure modes.

**Impact:** Reproducibility gap for the temporal memory component.
**Suggested fix:** Specify the threshold selection method and similarity metric in the main text or appendix. Add a failure-case analysis for incorrect event segmentation.

### W6. Related Work lacks critical technical positioning (Minor)
**Location:** Page 1 — Section 2, Related Work.

Each related-work subsection ends with a generic "Different from" statement that asserts distinction without technical specificity. For example, the long-term video understanding paragraph mentions memory banks in prior work but only states they are "unlike" the proposed method without explaining what makes the proposed memory design specifically suited for STVG versus prior memory architectures for video QA or captioning.

**Impact:** Weakens novelty positioning; readers may not see concrete differences from prior memory-augmented methods.
**Suggested fix:** For each related-work category, provide at least one sentence detailing the technical difference (e.g., "Unlike memory banks in VideoQA that store frame-level features for question answering, our spatial memory stores text-aligned query features specifically for instance-level grounding").

### W7. Conductance of gains decomposition (Minor)
**Location:** Page 1 — Section 4.2, Ablation Study.

The ablation compares ART-STVG against a baseline without memory/selection, but the baseline already has the autoregressive streaming and cascaded design. The improvement breakdown across four factors (autoregressive vs. parallel, streaming vs. full-video, memory vs. no-memory, selection vs. no-selection) is not fully disentangled. The cascaded vs. parallel ablation (Tab. 4) is informative but only shows a 1.5% gain; the remaining gains come from memory + selection. A full factorial design would strengthen causal attribution.

**Impact:** The importance of each individual component relative to the baseline is partially obscured.
**Suggested fix:** Provide a full ablation chain: (i) parallel non-autoregressive baseline, (ii) autoregressive only, (iii) +memory without selection, (iv) +memory with selection, (v) +cascaded design.

### W8. First-claim for LF-STVG needs verification (Deferred)
**Location:** Page 1 — Introduction paragraph 4.

The paper claims to be the "first to explore the LF-STVG problem" and the "first framework attempting to handle LF-STVG." Since external literature retrieval is unavailable in this run, this claim cannot be independently verified. Prior work on long-form video grounding with memory-augmented transformers may exist.

**Impact:** Novelty claim may be overstated if comparable prior work exists.
**Suggested fix:** Soften to "to our knowledge" and add a thorough related-work comparison with any relevant long-form video grounding, video highlight detection, or event segmentation methods that operate on minute-scale videos. Defer final verification to the authors' literature review.

### W9. Loss function and optimization details missing (Minor)
**Location:** Page 1 — Section 3.5, Optimization.

The entire loss function is deferred to supplementary material with "Due to limited space." The main paper does not specify whether the loss combines spatial (L1, GIoU) and temporal (cross-entropy for start/end) terms, their weighting, or any auxiliary losses. Without this, the training objective is not fully specified.

**Impact:** Reduces reproducibility of the training procedure.
**Suggested fix:** Provide at least the loss formulation in the main paper (it could be 2–3 equations). The weighting between spatial and temporal losses is critical for understanding the optimization trade-off.

## Score
**Final Score: 6/10**

**Scoring Rationale (Research Value + Novelty prioritized):**

The paper identifies a genuine and practical research gap (LF-STVG) and proposes a clean autoregressive architecture with selective memory banks. The empirical results on extended benchmarks are convincing and show a consistent trend. However, several factors limit the current score:

- **Novelty uncertainty (deferred):** The "first to explore LF-STVG" claim cannot be independently verified in this run due to unavailable external literature retrieval. While the autoregressive streaming + selective memory design appears novel in the STVG context, prior work on memory-augmented transformers for long-form video understanding exists and the paper's "different from" claims are not technically specific enough to fully establish differentiation. This is noted as a deferred verification item.

- **Experimental scope limitations:** Evaluation on a single dataset (HCSTVG-v2) with extended validation only (not training) limits generalization claims. The lack of variance reporting (multi-seed, confidence intervals) reduces statistical confidence, especially given that some improvements are modest (0.7% at 1 min).

- **Notation and implementation gaps:** Key equations have notation collisions (Eq. 5), memory selection thresholds are underspecified, and the loss function is deferred to supplementary material — all of which reduce reproducibility.

- **Incomplete conclusion:** The paper lacks limitations disclosure and future work directions, which is expected for a well-rounded submission.

The work makes a solid contribution to the STVG field by extending the problem scope to practically relevant video lengths. With stronger reproducibility documentation, expanded evaluation, and careful claim-bounding, the score could be improved in revision.

**External literature verification:** Deferred due to Retrieval-Disabled Mode in this run. Manual verification of novelty claims (especially the "first for LF-STVG" claim) and related-work completeness is recommended before final acceptance decision.