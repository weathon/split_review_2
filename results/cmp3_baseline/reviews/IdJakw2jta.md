## Summary
This paper introduces Long-Form Spatio-Temporal Video Grounding (LF‑STVG), where videos span minutes rather than the typical tens of seconds. To address the challenges of longer temporal spans and irrelevant content, the authors propose ART‑STVG, an autoregressive transformer that processes frames sequentially and maintains selective spatial and temporal memory banks. A cascaded spatio‑temporal decoder links spatial grounding to temporal grounding. Evaluated on extended HCSTVG‑v2 benchmarks (1–5 minutes), ART‑STVG substantially outperforms existing short‑form methods, while remaining competitive on the original short‑form setting.

## Strengths
- **Novel task formulation.** LF‑STVG is a practically motivated extension of STVG that bridges a clear gap between current research (sub‑minute videos) and real‑world applications (videos spanning minutes or hours). The paper is the first to systematically study this problem.
- **Well‑motivated and principled approach.** The autoregressive, frame‑by‑frame design naturally scales to long videos and avoids the computational bottleneck of processing all frames at once. The spatial and temporal memory banks with selective retrieval are sound and directly address the challenge of irrelevant information in long sequences.
- **Strong empirical results.** On the extended LF‑STVG benchmarks (1 min to 5 min), ART‑STVG achieves large and consistent gains over all previous methods (e.g., +6.5 → 9.1 m.tIoU on 2‑5 min videos). The performance gap increases with video length, confirming the effectiveness of the proposed design for longer videos.
- **Thorough ablation studies.** The paper isolates the contributions of each component: selective temporal memory, selective spatial memory, cascaded vs. parallel decoding, and the number of selected memories. Each ablation clearly demonstrates the benefit of the respective design choice.

## Weaknesses
### Fatal
None.

### Major
- **Training‑evaluation mismatch.** All main results (Table 1) are obtained by training on the original 20‑second HCSTVG‑v2 training set, while evaluation is on the extended 1–5 minute validation set. Although an ablation with 40‑second training is provided (Table 6), the primary results do not use training videos of comparable length. Training on longer videos could yield even stronger performance and would better reflect the full potential of ART‑STVG for LF‑STVG. This limitation weakens the conclusion that the method is “specially designed for LF‑STVG” when it is not trained on long examples.
- **Memory bank capacity and growth.** The update mechanism simply inserts the current query without removing any memories, implying unbounded growth. The paper uses a fixed selection size $N_s=32$ from the bank, but the bank itself could become arbitrarily large over long videos. The memory usage and potential degradation from storing all past memories are not discussed or ablated. This is a practical concern for very long videos.
- **Low absolute performance.** The best m.tIoU scores on 3‑5 min videos are 23.0 % and 15.0 %, while existing methods fall even lower. The paper does not discuss why these numbers are so low or whether they are practically meaningful. A brief analysis of the difficulty of the dataset or the expected upper bound would help contextualize the results.

### Minor
- **Temporal memory selection mechanism.** The temporal memory selection uses cosine similarity between adjacent memory features to detect event boundaries, inspired by TextTiling. It is unclear whether the memory features themselves encode event boundaries reliably, or whether this heuristic could fail for certain types of actions. An ablation with an alternative selection strategy (e.g., using the text query) would strengthen this component.
- **Short‑form baseline is weak.** The baseline (ART‑STVG without memory) achieves only 46.2 m.tIoU on HCSTVG‑v2, far below the full model (59.2). While this shows the importance of memory, it also suggests that the autoregressive structure alone is insufficient for short videos. The paper does not comment on why the baseline is so low relative to existing non‑autoregressive methods.

### Trivial
None.

## Nice-to-Haves
- Train ART‑STVG on the extended training set (e.g., 1‑minute videos) and report results to directly measure the benefit of long‑video training.
- Discuss or design a memory pruning or compression strategy to bound memory growth, and ablate its impact.
- Provide a more detailed qualitative analysis of failed cases on the LF‑STVG benchmarks to identify remaining challenges.

## Novel Insights
Beyond the paper’s own contributions, the key insight is that the “all‑at‑once” processing paradigm of existing STVG methods collapses on longer videos, not only because of computational limits but also because irrelevant information drowns out the target signal. The paper shows that autoregressive processing, combined with *selective* memory (not simply all past context), effectively addresses this issue, and that leveraging fine‑grained spatial cues to guide temporal localization (cascaded design) provides additional gains. These principles may generalize to other long‑form multimodal grounding tasks.

## Suggestions
- In a camera‑ready version, add an experiment where the model is trained on videos of the same length as the evaluation set (or at least longer than 20 s) to demonstrate the full potential of ART‑STVG for LF‑STVG.
- Clarify how the memory bank size is managed (e.g., does it have a maximum capacity? If not, discuss the memory and time overhead for very long videos).
- Provide a small-scale human‑performance baseline on the extended datasets to give context for the absolute m.tIoU values.

## Score and Decision
**Score:** 8

**Decision:** Accept

The paper makes a clear contribution by defining a new, practically important problem and proposing a principled, well‑evaluated solution. The weaknesses (training/evaluation mismatch, memory growth, low absolute scores) are real but not fatal; they can be addressed in future work or in a rebuttal. The strengths—novelty, soundness, and strong empirical gains—warrant acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>