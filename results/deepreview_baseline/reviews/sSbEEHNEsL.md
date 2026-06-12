## Summary
This paper proposes USR 2.0, a semi-supervised framework for unified speech recognition (ASR, VSR, AVSR) that addresses limitations of the prior USR method. The core innovation is CTC-driven teacher forcing, where greedily decoded CTC pseudo-labels are fed into the attention decoder to generate attention targets in a single forward pass, replacing slow autoregressive decoding. Combined with a mixed sampling strategy that intermittently uses standard autoregressive decoding, USR 2.0 achieves ~2x faster training, improved robustness to out-of-distribution inputs (long utterances, noise, unseen domains), and state-of-the-art results on LRS3, LRS2, and WildVSR benchmarks.

## Strengths
- **Significant practical improvement**: The paper demonstrates a clear and substantial reduction in training time (~2x faster) while simultaneously improving both in-distribution and out-of-distribution performance. This is a rare and valuable combination.
- **Well-motivated and principled approach**: The authors identify a genuine bottleneck in USR (autoregressive pseudo-labelling) and propose a clever solution (CTC-driven teacher forcing) that leverages the complementary strengths of CTC (speed, robustness) and attention (expressiveness). The reasoning about why global coherence is unnecessary in the pseudo-labelling setting is insightful.
- **Comprehensive and convincing experimental evaluation**: The paper includes extensive experiments across multiple modalities (ASR, VSR, AVSR), multiple datasets (LRS3, LRS2, WildVSR, LibriSpeech, AVSpeech, VoxCeleb2), multiple model scales (Base, Base+, Large, Huge), and multiple challenging OOD scenarios (long utterances, noise, domain shift). The ablations are thorough and clearly isolate the contributions of each component.
- **Strong empirical results**: USR 2.0 consistently outperforms strong baselines (USR, AV-HuBERT, BRAVEn) across nearly all settings, often by large margins, especially under distribution shift. The scaling results to a Huge model with ~2500 hours of unlabelled data are impressive.

## Weaknesses
### Fatal
None.

### Major
- **Limited novelty relative to USR**: While the paper presents a clear improvement over USR, the core architecture (encoder-decoder with CTC and attention heads, student-teacher framework, joint CTC-attention training) is inherited directly from USR. The main contributions—CTC-driven teacher forcing and mixed sampling—are incremental improvements to the pseudo-labelling strategy. The paper would be stronger if it demonstrated that these ideas generalize beyond the specific USR framework (e.g., to other CTC/attention models or other sequence-to-sequence tasks).
- **Potential concern about the "global coherence" argument**: The paper argues that global incoherence of CTC-driven attention PLs is not a problem because teacher and student are conditioned on the same CTC prefix. However, the student is trained to predict the teacher's next-token prediction under this prefix. If the teacher's predictions under the CTC prefix are themselves noisy or inconsistent (because the decoder was never trained to generate coherent sequences from CTC inputs), the student may learn a poor mapping. The paper's empirical results suggest this is not a major issue, but a more rigorous theoretical or empirical analysis of when and why this works would strengthen the contribution.

### Minor
- **Mixed sampling probability is a free parameter**: The choice of 0.5 for the AR mode sampling probability is justified empirically, but the optimal value likely depends on the specific dataset and domain shift. The paper shows that OOD performance degrades sharply with high AR probability, suggesting that tuning this parameter is important for robustness. A more principled way to set this parameter (e.g., based on a validation set or a measure of distribution shift) would be valuable.
- **Comparison with non-autoregressive methods**: The paper mentions non-autoregressive transformers (NATs) as an alternative to AR decoding but does not compare against them. Given that CTC-driven teacher forcing is a form of non-autoregressive pseudo-labelling, a comparison with NAT-based approaches (e.g., using a NAT decoder instead of the attention decoder) would help contextualize the contribution.

### Trivial
None.

## Nice-to-Haves
- An analysis of the types of errors made by USR 2.0 vs. USR (e.g., substitution, insertion, deletion rates) would provide deeper insight into the robustness improvements.
- A discussion of the memory footprint of USR 2.0 vs. USR during training, beyond just wall-clock time.
- An exploration of whether the CTC-driven teacher forcing idea can be applied to other modalities (e.g., text-to-speech, handwriting recognition) as suggested in the conclusion.

## Novel Insights
The key insight is that in a pseudo-labelling setting, the global coherence of teacher-generated sequences is not necessary for effective knowledge transfer. What matters is that teacher and student operate under the same conditioning, allowing the student to learn a stable mapping from a (potentially incoherent) prefix to a conditionally valid next-token prediction. This insight enables the use of fast, robust CTC outputs to drive the attention decoder, breaking the autoregressive bottleneck without sacrificing the expressiveness of attention. The paper also demonstrates that coupling the CTC and attention branches through shared pseudo-labels improves robustness to distribution shift, as the decoder inherits the monotonic alignment and conditional independence properties of CTC.

## Suggestions
- Consider adding a comparison with a variant that uses a non-autoregressive transformer (NAT) decoder instead of the attention decoder, to directly compare CTC-driven teacher forcing with other non-autoregressive approaches.
- Provide guidance on how to set the mixed sampling probability in practice, perhaps based on a validation set or a measure of domain shift between labelled and unlabelled data.
- Include an analysis of the types of errors (substitutions, insertions, deletions) to better understand the source of the robustness improvements.

## Score and Decision
The paper presents a clear, well-motivated, and empirically strong improvement over a state-of-the-art method. The contributions are incremental but practically significant, and the experimental evaluation is thorough and convincing. The paper is well-written and the ideas are clearly explained. I recommend acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>