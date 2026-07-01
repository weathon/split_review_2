## Summary

This paper introduces Continuous Online Action Detection (COAD), a new task formulation that combines online action detection with single-pass, on-the-fly adaptation from streaming egocentric video. The authors curate Ego-OAD, a large-scale benchmark derived from Ego4D Moment Queries, and propose training strategies—state continuity, orthogonal gradient projection, and non-uniform loss—that improve both adaptation to in-stream data and generalization to held-out out-of-stream data. Experiments on Ego-OAD and EPIC-KITCHENS show that COAD outperforms a naive online learning baseline, with gains of up to 20% in Top-5 Recall on in-stream data and up to 7% on out-of-stream data.

## Strengths

- The problem of continuous adaptation for online action detection is practically important and timely, especially for personalized egocentric AI on wearable devices. The COAD formulation correctly identifies the gap between offline-trained OAD models and the dynamic, user-specific environments they must operate in after deployment.
- Curating a large-scale egocentric OAD benchmark (Ego-OAD with 87 classes, 263 hours) from Ego4D is a useful community contribution that could stimulate further research in this direction. The dataset includes multi-label annotations with overlapping actions, reflecting realistic ambiguity.
- The proposed training strategies (orthogonal gradient decorrelation, state continuity, non-uniform loss) are well-motivated for the streaming, single-pass setting and are clearly explained. The ablation study in Table 3 provides a clean analysis of each component’s contribution.
- The paper is well-structured, the figures (especially Figure 2) clearly convey the difference between standard offline OAD training and the proposed COAD training pipeline.

## Weaknesses

### Major

1. **No comparison to existing state-of-the-art OAD models.** The paper evaluates COAD only against its own baselines (Pretrained Only and w/o COAD). There is no comparison to established OAD methods such as LSTR, TeSTra, IDN, or GateHub, even when adapted to the continuous setting (e.g., by fine-tuning them on the in-stream set). Without such comparison, it is unclear whether the COAD framework offers a net benefit over simply deploying existing offline OAD models with online fine-tuning. This omission significantly limits the paper’s contribution to the OAD literature.

2. **Unrealistic assumption of online supervision during streaming.** The COAD method requires frame-level or window-level ground-truth labels during the continuous training phase. In real-world deployment on wearable devices, such labels are generally unavailable. The paper does not discuss how supervision could be obtained (e.g., via self-supervision, weakly supervised signals, or human feedback). This is a critical gap between the proposed formulation and practical applicability. The non-uniform loss mitigates label density but does not remove the need for labels.

3. **Weak baselines for the continuous learning setting.** The “w/o COAD” baseline performs naive SGD on the stream without any of the proposed tricks, which is known to suffer from catastrophic interference. A stronger baseline would include standard continual learning methods (e.g., Elastic Weight Consolidation, replay buffers, or online EWC) applied to the same RNN head. The paper’s claimed improvements may be largely due to the orthogonal gradient and non-uniform loss addressing issues that well-established continual learning techniques could also handle. The lack of such baselines makes the contribution less distinctive.

### Minor

- The paper freezes the video backbone and only updates the RNN head. This limits the model’s ability to adapt its visual representations to new environments or user-specific appearance patterns. The authors should discuss this limitation and its impact on the method’s adaptation capacity.
- On EPIC-KITCHENS, COAD underperforms the Pretrained Only baseline on some in-stream metrics, and the gains over the baseline are marginal. The paper attributes this to fine-grained actions, but the observation raises questions about the method’s robustness across different domains.
- The Ego-OAD curation merges multiple annotation passes and manually groups semantically similar descriptions. The details of this grouping (referred to Appendix A, which is outside the main text) are not described, making it hard to assess label quality and potential noise.

### Trivial
- Table 2 has “Verb / Noun / Action” columns but the out/in notation is not fully explained in the caption; the reader must infer from the text.
- Figure 1 contains duplicate caption text due to the PDF extraction process.

## Nice-to-Haves
- Include a comparison with at least one transformer-based OAD method (e.g., LSTR) adapted to the stream setting, even if it requires modifications for computational feasibility on a simulated stream.
- Discuss how the method could be extended to unsupervised or self-supervised scenarios, and whether the visual backbone could also be updated during streaming.
- Provide an analysis of catastrophic forgetting in the w/o COAD baseline (e.g., measuring performance on previously seen segments after further training) to better illustrate the benefit of orthogonal gradient projection.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Replace the weak w/o COAD baseline with competitive continual learning baselines (e.g., online EWC, experience replay with a small memory, or SI). This would isolate the effect of the orthogonal gradient method from standard continual learning techniques.
- Compare COAD with state-of-the-art OAD models (e.g., TeSTra or LSTR) that are either fine-tuned on the in-stream set or used as the temporal head in the COAD pipeline. This comparison is essential to demonstrate that COAD is useful beyond the specific RNN-based architecture.
- Explicitly address the online supervision assumption in the text and, if possible, present a small experiment where labels are only partially available (e.g., 10% of frames labeled) to probe the method’s sensitivity.
- Release the Ego-OAD dataset splits and benchmark code to facilitate reproducibility and community adoption.

## Score and Decision

Score: 4

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>