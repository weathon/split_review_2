## Summary

The paper proposes USR 2.0, a semi-supervised framework for unified speech recognition (ASR, VSR, AVSR) that improves upon USR by introducing CTC-driven teacher forcing. Instead of slow autoregressive decoding to generate attention-based pseudo-labels, the teacher’s greedily decoded CTC outputs are fed into the decoder to produce attention targets in a single forward pass, halving training time. A mixed sampling strategy intermittently reintroduces autoregressive decoding to mitigate exposure bias. The method achieves state-of-the-art results on LRS3, LRS2, and WildVSR with a single model, while substantially improving robustness to long utterances, noise, and out-of-distribution datasets.

## Strengths

- **Novel and well-motivated idea**: CTC-driven teacher forcing is a clever way to leverage CTC’s efficiency and robustness for attention-based pseudo-labelling. The insight that global coherence of teacher outputs is unnecessary in pseudo-labelling because teacher and student share the same conditioning prefix is both original and convincingly supported.
- **Significant practical impact**: The method halves training time while improving performance, especially under distribution shift. This directly addresses a key bottleneck in scaling semi-supervised speech recognition.
- **Comprehensive evaluation**: Extensive out-of-distribution experiments (long utterances, additive noise, cross-dataset) and in-distribution benchmarks across multiple model sizes (Base, Base+, Large, Huge) are provided. Ablations clearly justify design choices (e.g., importance of both CTC and attention targets, effect of mixed sampling probability).
- **State-of-the-art results**: USR 2.0 achieves SOTA WERs on LRS3, LRS2, and WildVSR across ASR, VSR, and AVSR with a single unified model, outperforming modality-specific self-supervised baselines.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
- The paper could provide a deeper theoretical or intuitive analysis of why CTC-driven teacher forcing works despite the lack of global coherence in the generated attention pseudo-labels. The current explanation (matched conditioning) is plausible but somewhat brief; a more formal argument or a simple toy example would strengthen the contribution.
- The mixed sampling probability is fixed at 0.5; while the authors mention that an adaptive schedule performed similarly, a more systematic study of the trade-off between ID accuracy, OOD robustness, and training efficiency would be valuable for practitioners.
- The total computational cost (e.g., GPU hours) for the Huge model training is not reported, which would help readers assess the scalability claims more concretely.

### Trivial
- Some figures (e.g., Figure 3) have small text and could be improved for readability.
- The paper uses “USR 2.0” as a name; while clear, it is a minor incremental naming convention.

## Nice-to-Haves
- An oracle experiment comparing the quality of CTC-driven attention pseudo-labels versus autoregressive pseudo-labels (e.g., by measuring agreement with ground truth) would further validate the approach.
- Application of CTC-driven teacher forcing to other sequence-to-sequence tasks (e.g., handwriting recognition, music transcription) as mentioned in the conclusion could be explored in future work.

## Novel Insights

The key insight is that in a pseudo-labelling setting, the teacher and student can be conditioned on the same CTC-derived prefix, making global coherence of the teacher’s output sequence unnecessary for effective knowledge transfer. This decouples the need for coherent sequences during training from the need for coherent sequences during inference, enabling a fast and robust training procedure. The paper also demonstrates that coupling CTC and attention supervision through aligned targets improves robustness to distribution shift, as the decoder inherits CTC’s monotonic alignment and conditional independence properties.

## Suggestions
- Add a brief theoretical justification or a small-scale synthetic experiment to illustrate why matched conditioning suffices for learning despite incoherent targets.
- Report total GPU hours for the Huge model training to help practitioners assess scalability.

## Score and Decision
MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>