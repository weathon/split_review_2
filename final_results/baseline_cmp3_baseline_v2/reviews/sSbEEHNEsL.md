## Summary

This paper proposes USR 2.0, a semi-supervised framework for unified speech recognition (ASR, VSR, AVSR) that improves upon the prior USR method. The core innovation is CTC-driven teacher forcing, where greedily decoded CTC pseudo-labels are fed into the attention decoder to generate attention targets in a single forward pass, replacing slow autoregressive decoding. Combined with a mixed sampling strategy that intermittently uses standard autoregressive decoding, this approach halves training time, improves robustness to out-of-distribution inputs (long utterances, noise, unseen domains), and achieves state-of-the-art results on LRS3, LRS2, and WildVSR benchmarks.

## Strengths

- **Significant practical improvement in training efficiency**: The paper convincingly demonstrates ~2x faster training across multiple model scales and data settings (Figure 5), which is a substantial practical contribution for semi-supervised learning at scale. The speedup comes from both faster per-step decoding and faster convergence (fewer epochs needed).

- **Strong empirical evidence for OOD robustness**: The paper provides thorough evaluation across multiple distribution shifts—long utterances (Figure 3), additive noise at various SNRs (Table 1), and cross-dataset generalization (Table 3). The improvements are consistent and often large (e.g., 15.4% vs 25.3% on LibriSpeech under greedy decoding).

- **Well-motivated and clearly explained method**: The paper clearly identifies the two key limitations of USR (computational cost of AR decoding and decoupled supervision leading to error reinforcement) and proposes a principled solution. The CTC-driven teacher forcing idea is well-motivated by the observation that CTC is fast and robust, and the argument that global coherence is unnecessary in the pseudo-labelling setting is insightful.

- **Comprehensive ablation studies**: The ablations in Table 4 and Figure 4 systematically validate the design choices, showing the contribution of each component (CTC vs attention PLs for each branch, mixed sampling probability) and their interaction with ID vs OOD performance.

## Weaknesses

### Fatal
None.

### Major
- **The claim of "state-of-the-art" is not fully supported for all settings.** In Table 2, for the Base model on LRS3 (low-resource), USR 2.0 achieves 36.2% (VSR) vs USR's 36.0% — this is a *worse* result, contradicting the claim of improvement. For ASR and AVSR, the gains are marginal (3.0 vs 3.2, 2.9 vs 3.0). The paper's central claim of "state-of-the-art" is only clearly supported for larger models and with additional unlabelled data (VoxCeleb2). The paper should be more precise about where improvements are and are not observed.

- **The mixed sampling strategy introduces a significant hyperparameter (AR mode probability) with no clear guidance on tuning**: Figure 4 shows that ID and OOD performance have opposite trends with respect to this probability, and the optimal value likely depends on the specific data distribution. The paper uses 0.5 as a default but provides no principled way to set this hyperparameter for new datasets or tasks. This is a practical concern for adoption.

- **The claim that "global coherence is unnecessary" in the pseudo-labelling setting is not rigorously justified.** The argument in Section 4.1 relies on the student learning a "stable mapping from a coherent CTC prefix to the teacher's conditionally valid next-token prediction." However, the teacher's attention-based PLs are themselves generated from a potentially incoherent prefix (since CTC outputs may lack global coherence). The paper does not provide a formal analysis or controlled experiment to demonstrate that the student indeed learns a useful mapping despite this, beyond the empirical results. A clearer theoretical or empirical justification would strengthen the paper.

### Minor
- **The comparison to USR in Table 2 for the Base model on LRS3 shows USR 2.0 is worse for VSR (36.2 vs 36.0)**, which contradicts the claim of improvement. While the difference is small, it should be acknowledged and discussed.
- **The paper does not report confidence intervals or statistical significance for any of the results.** Given the small differences in some comparisons (e.g., 0.1-0.2% WER), it is unclear whether these are meaningful.
- **The OOD evaluation on AVSpeech uses only 1,000 manually filtered samples transcribed by Whisper.** The filtering and transcription process could introduce biases, and the small sample size raises questions about reliability.

### Trivial
None.

## Nice-to-Haves
- An analysis of the types of errors that CTC-driven teacher forcing corrects compared to AR decoding (e.g., substitution vs deletion vs insertion errors) would provide deeper insight into the method's behavior.
- A discussion of the limitations of the approach, particularly scenarios where CTC-driven teacher forcing might underperform (e.g., very high-resource settings with clean in-distribution data).

## Novel Insights

The paper's key insight is that in a pseudo-labelling (self-training) setting, the global coherence of teacher-generated sequences is not necessary for effective knowledge transfer, because the student is conditioned on the same (coherent) CTC prefix as the teacher. This observation allows the authors to replace expensive autoregressive decoding with a single forward pass using CTC-driven teacher forcing, while still benefiting from the expressiveness of attention-based modeling. This is a clever and non-obvious insight that challenges the conventional wisdom that teacher outputs must be high-quality sequences for effective self-training.

## Suggestions
- Acknowledge and discuss the VSR result on Base LRS3 where USR 2.0 is slightly worse than USR (36.2 vs 36.0), and clarify the conditions under which improvements are expected.
- Provide guidance on how to set the AR mode sampling probability for new datasets or tasks, perhaps based on the degree of distribution shift between labelled and unlabelled data.
- Report confidence intervals or statistical significance for key results, especially where differences are small.

## Score and Decision

This paper makes a solid contribution to the field of unified speech recognition. The core idea of CTC-driven teacher forcing is clever and well-motivated, and the empirical results convincingly demonstrate improved training efficiency and OOD robustness. However, the paper overstates its claims in some places (e.g., "state-of-the-art" for settings where gains are marginal or negative), and the lack of statistical significance reporting is a concern. The method is sound and the experiments are thorough, but the contribution is incremental over USR rather than a breakthrough. The paper is clearly written and the ablations are informative. Overall, this is a good paper that makes a clear, practical improvement, but it is not exceptional.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>