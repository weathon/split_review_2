## Summary

This paper introduces Long-Form Spatio-Temporal Video Grounding (LF-STVG), a new task that extends STVG to videos of 1–5 minutes, and proposes ART-STVG, an autoregressive transformer framework that processes frames sequentially with spatial and temporal memory banks. The method employs memory selection strategies to retain only relevant context and a cascaded spatio-temporal decoder that uses fine-grained spatial cues to assist temporal localization. On extended HCSTVG-v2 benchmarks, ART-STVG substantially outperforms existing short-form STVG methods, while remaining competitive on short-form STVG.

## Strengths

- **Novel and practical problem formulation.** LF-STVG addresses a clear gap between existing STVG research (videos <1 minute) and real-world applications (videos spanning minutes to hours). The paper is the first to systematically study this setting.
- **Well-motivated architectural design.** The autoregressive, frame-by-frame processing naturally scales to long videos and avoids the computational bottleneck of processing all frames at once. The memory banks with selection strategies are intuitively justified and shown to be critical through ablations.
- **Strong empirical results.** ART-STVG achieves large and consistent improvements over all compared methods across five LF-STVG benchmarks (e.g., +9.1% m.tIoU on 3min, +7.3% on 5min). The gains increase with video length, confirming the method’s suitability for long-form videos.
- **Thorough ablation study.** The paper systematically validates each component (temporal memory selection, spatial memory selection, cascaded design, number of selected memories) and provides qualitative attention visualizations that support the design choices.

## Weaknesses

### Fatal
None.

### Major
- **Dataset extension validity is insufficiently justified.** The LF-STVG benchmarks are created by extending the HCSTVG-v2 validation set to 1–5 minutes. The original textual queries and ground-truth annotations (spatial boxes and temporal intervals) were designed for 20-second clips. It is unclear whether these annotations remain correct or unambiguous when the video is extended. For example, a query like “the man in the blue suit stands up” may describe an event that occurs only in the original 20-second segment; in a longer video, the same query could refer to a different occurrence or become ambiguous. The paper does not describe any re-annotation or verification process beyond “manually review[ing] the extended videos to ensure their quality.” Without a clear protocol for how annotations were adapted (or confirmed to still be valid), the reliability of the evaluation is questionable.
- **The baseline is weak and not fully comparable.** The baseline is described as having a “similar architecture to our ART-STVG but without memory and memory selection modules.” However, on short-form STVG (Table 7), this baseline achieves only 46.2 m.tIoU, far below existing methods (e.g., TubeDETR 53.9). This suggests the autoregressive architecture without memory is inherently weak, making the improvement from memory less surprising. A stronger baseline—such as an autoregressive model with full (unselected) memory—would better isolate the benefit of memory selection.
- **Temporal memory selection is heuristic and unvalidated.** The method uses cosine similarity between adjacent memory features to detect event boundaries and then selects only the nearest event. While intuitive, this approach is not compared to any alternative temporal segmentation technique, and its accuracy is not evaluated. The paper would benefit from an analysis of boundary detection quality or a comparison with a simpler fixed-window selection.

### Minor
- **Evaluation is limited to a single source dataset.** All LF-STVG benchmarks are derived from HCSTVG-v2. While this is understandable given the lack of existing long-form STVG datasets, the paper would be strengthened by also evaluating on a subset of a different long-term video dataset (e.g., ActivityNet or Charades) with adapted annotations, or by demonstrating that the method generalizes beyond the specific characteristics of HCSTVG-v2.
- **The number of selected spatial memories (N_s=32) is chosen without strong motivation.** The ablation shows that 32 works best, but the performance differences are small (≤0.5%). A more principled selection criterion (e.g., based on a similarity threshold) could be more robust.

### Trivial
None.

## Nice-to-Haves

- Provide a detailed description of the dataset extension process, including how longer videos were sourced, whether queries were re-annotated, and inter-annotator agreement statistics.
- Compare with a baseline that uses all memories (no selection) to directly measure the impact of the selection strategy.
- Evaluate on an existing long-term video dataset (e.g., ActivityNet-1.3) by converting it to a spatio-temporal grounding task, even if only for a subset.
- Analyze the computational cost (GPU memory, inference time) of ART-STVG relative to full-video methods, especially as video length grows.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that for long-form spatio-temporal grounding, an autoregressive approach with selective memory is far more effective than processing the entire video at once. The finding that using *all* historical memory hurts performance (Table 2, ❷ vs ❸) is particularly informative: it suggests that irrelevant context from distant events actively degrades localization, and that simple selection heuristics (text similarity for spatial, boundary detection for temporal) can recover substantial gains. This principle may generalize to other long-form video understanding tasks.

## Suggestions

- Clarify the dataset extension protocol in detail: how were the longer videos selected from the original YouTube sources? Were the original temporal annotations (start/end frames) adjusted to account for the longer video? If not, provide evidence that the original annotations remain correct in the extended context.
- Add a baseline that uses all memories (no selection) for both spatial and temporal decoders, to directly quantify the benefit of the selection strategies.
- Consider evaluating on a subset of a different long-term video dataset (e.g., VidOR or ActivityNet-Entities) to demonstrate generalization beyond HCSTVG-v2.

## Score and Decision

The paper addresses a novel and important problem with a well-designed method and strong empirical results. The main concern is the validity of the extended dataset, which could affect the reliability of the evaluation. If the authors can convincingly address this issue (e.g., by providing annotation verification or additional experiments on a different dataset), the paper would be a strong accept. Based on the current content, the contribution is significant enough to warrant acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>