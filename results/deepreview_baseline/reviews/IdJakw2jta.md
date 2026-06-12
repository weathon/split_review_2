## Summary
This paper introduces Long-Form Spatio-Temporal Video Grounding (LF-STVG), a new task that aims to localize an object described by a text query in videos lasting minutes rather than the typical tens of seconds. The authors propose ART-STVG, an autoregressive transformer framework that processes frames sequentially, uses spatial and temporal memory banks with selection strategies to retain relevant context, and employs a cascaded decoder where spatial grounding aids temporal localization. Experiments on extended HCSTVG-v2 benchmarks (1–5 minutes) show ART-STVG significantly outperforms existing STVG methods, with the performance gap widening for longer videos, while remaining competitive on short-form benchmarks.

## Strengths
- **Novel problem formulation and practical relevance** – The paper identifies and formalizes LF-STVG, a realistic extension of STVG that bridges a clear gap between current research (videos <1 minute) and real-world applications (minutes to hours). This problem framing is timely and likely to inspire further work.
- **Principled autoregressive design for long videos** – ART-STVG’s frame-by-frame processing with memory banks naturally handles arbitrary-length videos, avoids the memory bottlenecks of processing all frames at once, and leverages selective spatio-temporal context. This is a clean, well-motivated departure from existing parallel methods.
- **Effective memory selection strategies** – The spatial selection (text-guided similarity) and temporal selection (adjacent-frame similarity for event boundary detection) are simple yet demonstrate large gains in ablation studies (e.g., 13.4% m.tIoU improvement over using all temporal memories). The attention map visualizations in Figure 5 convincingly show how selection focuses on target regions.
- **Cascaded spatio-temporal decoder** – Connecting the spatial decoder to the temporal decoder via ROI-pooled target features is a novel and effective design; the ablation in Table 4 shows consistent improvements over a parallel baseline, validating that fine-grained spatial cues help temporal localization in long videos.
- **Strong and consistent empirical results** – ART-STVG substantially outperforms four state-of-the-art methods (TubeDETR, STCAT, CG-STVG, TA-STVG) across all five LF-STVG benchmarks (1–5 minutes), often by large margins (e.g., 9.1% m.tIoU on 3-minute videos vs. the next best). The gap grows with video length, confirming the method’s specific advantage for long-form videos. Competitive performance on short-form STVG further demonstrates generality.

## Weaknesses
### Fatal
None.

### Major
- **Evaluation on a single base dataset** – The LF-STVG benchmarks are extended only from HCSTVG-v2. While the authors justify that this is the only dataset with available source videos, the absence of evaluation on other long-video datasets (e.g., those from surveillance or egocentric domains) limits the evidence for broad generalizability. The extensions are also only on the validation set, and manual review may introduce subtle biases.
- **Baseline definition is unclear** – The “Baseline (ours)” in Table 1 is described as having a similar architecture but without memory and memory selection modules. It is not specified whether it still uses the autoregressive frame-by-frame processing and the cascaded decoder. If the baseline removes memory along with other components, the large gains attributed to memory could be confounded. The paper should provide a precise definition and an ablation that isolates the effect of memory while keeping the autoregressive and cascaded structure fixed.

### Minor
- **Heuristic temporal memory selection** – The temporal selection uses cosine similarity between adjacent memory features to detect event boundaries. While effective, this is a relatively simple heuristic; more principled or learned boundary detection could potentially improve robustness, especially in videos with gradual transitions.
- **Low absolute performance on longer videos** – For 5-minute videos, even ART-STVG achieves only 15.0% m.tIoU and 10.0% m.vIoU. This reflects the extreme difficulty of the task, but it also indicates that current results are still far from practical deployment. The paper could more explicitly discuss this limitation as a direction for future work.

### Trivial
None.

## Nice-to-Haves
- A comparison of inference memory/FLOPs between ART-STVG and existing methods on a fixed long video (e.g., 5 minutes) would concretely demonstrate the computational advantage of the autoregressive design.
- Investigating more sophisticated memory update or removal strategies (e.g., learnable attention-based selection) could further improve performance and would be an interesting extension.
- If other long-form video datasets with STVG annotations become available in the future, validating ART-STVG on them would strengthen the claims.

## Novel Insights
The paper demonstrates that processing video frames autoregressively with selective memory banks is a highly effective paradigm for spatio-temporal grounding in long videos. The key insight is that not all past frames are equally relevant to the current frame; by selecting only the most text-relevant spatial memories and temporally coherent event-based memories, the model can maintain useful context without being overwhelmed by irrelevant information. The cascaded decoder further shows that spatial localization provides fine-grained target cues that improve the more challenging temporal boundary prediction, a dependency that existing parallel methods do not exploit.

## Suggestions
- Clarify the baseline architecture precisely: state explicitly whether it uses autoregressive processing and the cascaded decoder, and provide an ablation that removes only the memory banks and selection while keeping all other design choices fixed.
- Consider adding a discussion of the limitations of the current dataset extension (e.g., single-domain, manual review) and outline steps toward more comprehensive LF-STVG benchmarks.

## Score and Decision
MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>