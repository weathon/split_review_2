## Summary

This paper presents GRAID, a framework for generating high-quality spatial reasoning VQA datasets by operating exclusively on 2D bounding boxes from object detectors, thereby avoiding the cascading errors from single-view 3D reconstruction and hallucinations from generative models. The authors generate over 8.5 million VQA pairs from three driving datasets (BDD100k, NuImages, Waymo) using 22 question templates, achieving 91.16% human-validated accuracy compared to 57.6% for a comparable existing method. Fine-tuning experiments demonstrate that models trained on GRAID data learn transferable spatial concepts that generalize across datasets, held-out question types, and established VQA benchmarks.

## Strengths

- **Principled approach to avoiding error propagation**: The core insight that qualitative spatial relationships can be reliably determined from 2D geometric primitives alone is well-motivated and directly addresses a fundamental limitation of existing methods that rely on noisy 3D reconstruction pipelines. The paper provides concrete evidence of this problem (57.6% human validation rate for SpatialVLM data).

- **Comprehensive human evaluation**: The human study is thorough, evaluating 317 GRAID VQA pairs across multiple dimensions (question validity, answer correctness, difficulty rating) and comparing against existing datasets. The 91.16% validity rate is a strong empirical demonstration of GRAID's quality advantage.

- **Strong evidence of concept transfer**: The RQ2 experiment showing that training on only 6 question types improves performance on over 10 held-out types, including a completely unseen topic (Size & Aspect), provides compelling evidence that the model learns genuine spatial reasoning primitives rather than template-specific patterns.

- **Scalable and practical framework**: SPARQ's predicate-based early rejection mechanism (up to 1400× speedups) addresses a real practical concern for large-scale dataset generation, and the framework's compatibility with standard object detectors makes it immediately usable by the community.

## Weaknesses

### Fatal
None.

### Major

- **Limited evaluation of non-driving generalization**: While the paper claims GRAID is "domain-agnostic" and demonstrates generalization to indoor scenes via BLINK benchmarks, the training data is exclusively from driving datasets. The paper would be significantly strengthened by generating GRAID data from a non-driving source (e.g., indoor scene datasets like NYUv2 or ScanNet) and showing similar quality and transfer results. As presented, it's unclear whether the framework's reliance on object detection annotations (which are most abundant in driving domains) limits its practical applicability.

- **Incomplete comparison with SpatialRGPT**: The human evaluation compares against OpenSpaces (SpatialVLM) but not against SpatialRGPT's dataset, with the stated reason being that "evaluators were unable to ascertain the quality" due to masked region queries. This is a significant gap, as SpatialRGPT is a key related work. The paper should either develop an evaluation protocol that works with region-based datasets or acknowledge this limitation more prominently.

- **RQ3 results lack statistical significance measures**: Tables 4, 5, and 6 are referenced but not included in the provided content. The reported improvements (e.g., 32.5% on A-OKVQA) are impressive, but without confidence intervals or multiple-run statistics, it's difficult to assess whether these gains are robust or potentially due to random variation in fine-tuning.

### Minor

- **The paper overclaims on "no VLM architecture changes needed"**: While GRAID itself doesn't require architectural changes, the fine-tuning experiments use LoRA adapters, which are architectural modifications to the VLM. This is a minor inconsistency in framing.

- **Waymo dataset size is very small**: The Waymo variant (16.4k pairs) is orders of magnitude smaller than the BDD and NuImages variants, yet the paper doesn't explain why this matters or whether results on Waymo-trained models would be meaningful.

### Trivial

- The acronym GRAID is defined twice in the paper (abstract and Section 3), which is redundant.

## Nice-to-Haves

- An analysis of which types of spatial questions are most/least improved by GRAID training, to guide future template design.
- A study of how the quality of the underlying object detector affects GRAID's output quality, since the framework's guarantees depend on detector accuracy.
- Ablation experiments showing the contribution of each component (e.g., training without SPARQ's predicate filtering to measure its impact on data quality).

## Novel Insights

The paper's key insight—that qualitative spatial relationships can be reliably determined from 2D bounding boxes alone, without any 3D reconstruction—is genuinely novel and practically important. This observation challenges the prevailing assumption in the field that spatial reasoning requires metric depth information. The empirical demonstration that models trained on 2D-geometry-derived questions learn transferable spatial concepts that generalize to unseen question types and domains provides strong evidence that qualitative spatial reasoning can be learned from purely 2D signals. This has implications beyond VQA: it suggests that many spatial reasoning capabilities may be achievable without the complexity and error-prone nature of 3D perception pipelines.

## Suggestions

1. Generate GRAID data from at least one non-driving dataset (e.g., indoor scenes from ScanNet or Matterport3D) and evaluate whether the same quality guarantees and transfer results hold. This would substantially strengthen the claim of domain agnosticism.

2. Develop a protocol for evaluating region-based datasets (like SpatialRGPT) in the human study, perhaps by overlaying the region masks on the image or using a consistent visualization scheme. This would enable a more complete comparison.

3. Report results with confidence intervals or standard deviations across multiple fine-tuning runs to establish statistical significance of the RQ3 benchmark improvements.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>