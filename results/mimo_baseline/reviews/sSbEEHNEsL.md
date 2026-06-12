## Summary
This paper presents USR 2.0, an improved version of the Unified Speech Recognition framework that addresses two key limitations of the original USR: the computational bottleneck of autoregressive pseudo-label generation and the vulnerability of decoupled CTC/attention supervision under distribution shifts. The core contribution is CTC-driven teacher forcing—feeding greedily decoded CTC pseudo-labels into the decoder to generate attention pseudo-labels in a single forward pass—combined with mixed sampling to mitigate exposure bias, yielding ~2× faster training, improved robustness, and state-of-the-art results across ASR, VSR, and AVSR on LRS3, LRS2, and WildVSR.

## Strengths
- **Strong practical impact with clear empirical validation.** USR 2.0 halves training time (Figure 5), achieves state-of-the-art WER on LRS3 (0.8% AVSR, 0.9% ASR, 17.6% VSR with Huge model), and demonstrates large OOD gains (e.g., LibriSpeech greedy WER drops from 25.3% to 15.4% vs. USR, Table 3). These are substantial improvements with real-world relevance.
- **Well-motivated core insight.** The observation that globally incoherent CTC-driven pseudo-labels are nonetheless effective for self-training because of matched conditioning between teacher and student is novel and theoretically grounded (Section 4.1). This insight enables a practical speedup without sacrificing quality.
- **Thorough and diverse evaluation.** The paper evaluates robustness across three distinct distribution shift axes—long utterances (Figure 3), noise (Table 1), and unseen datasets (Table 3)—as well as in-distribution across multiple model sizes and resource settings (Table 2). Ablation studies (Table 4, Figure 4) systematically validate each design choice.
- **Principled coupling of CTC and attention branches.** By aligning the pseudo-label lengths from both heads, the student decoder can predict both simultaneously, inheriting CTC's robustness while preserving attention's expressiveness. This addresses a genuine architectural limitation of USR.

## Weaknesses
### Fatal
None.

### Major
- **Limited comparison to other pseudo-labelling or self-training approaches.** The comparison focuses heavily on USR and self-supervised methods (AV-HuBERT, BRAVE_n), but does not compare against other semi-supervised speech recognition systems that use different pseudo-labelling strategies (e.g., Noisy Student, InterCTC-based self-training). While the USR lineage is clear, a broader comparison would better contextualize the contributions.

### Minor
- **The mixed sampling probability of 0.5 is selected heuristically.** While Figure 4 shows the sensitivity to this hyperparameter, the paper does not provide a principled criterion for choosing it. The adaptive schedule mentioned in a footnote performs similarly, but more analysis of why 0.5 works well would strengthen the contribution.
- **Some OOD evaluations rely on automatic transcriptions** (VoxCeleb2 transcribed by Whisper, AVSpeech transcribed by Whisper). While this is practically reasonable, it introduces a dependency on Whisper's quality as the evaluation oracle, which could confound WER comparisons, especially on hard OOD samples.

### Trivial
None.

## Nice-to-Haves
- A qualitative analysis of CTC-driven attention pseudo-labels (e.g., examples showing where they diverge from AR pseudo-labels and how this affects training) would enrich the paper's insights.
- Discussion of failure modes or cases where CTC-driven teacher forcing might not transfer well (e.g., languages with very different phoneme inventories, or tasks with non-monotonic alignment).

## Novel Insights
The key genuinely novel insight is that global coherence of pseudo-labels is unnecessary in a self-training setting when teacher and student share the same conditioning signal. This is a non-obvious observation: conventional wisdom holds that teacher outputs should be as accurate as possible, but the paper shows that even "locally valid but globally incoherent" sequences suffice because the student learns a stable mapping from CTC prefix to next-token prediction. This insight has implications beyond speech recognition for any self-training system where parallel pseudo-label generation is desired over autoregressive generation.

## Suggestions
- Add a comparison to at least one additional semi-supervised baseline (e.g., Noisy Student or a CTC-only self-training variant) to better contextualize the gains from the CTC-driven teacher forcing approach specifically.
- Consider analyzing whether the OOD robustness gains are primarily from (a) the CTC-driven pseudo-labels being more robust than AR pseudo-labels, or (b) the joint CTC-attention supervision during training. The ablation in Table 4 partially addresses this, but a targeted experiment separating these two effects would be informative.

## Score and Decision
This paper presents a well-motivated, practically important improvement to a recognized speech recognition framework. The core insight about pseudo-label coherence is novel, the experimental evaluation is thorough and convincing, and the practical gains (2× faster training, improved robustness, SOTA results) are substantial. The methodological contribution is incremental in that it refines an existing framework rather than introducing an entirely new paradigm, but the improvements are significant and well-validated. The paper would be a valuable contribution to the ICLR community.

MY FINAL SCORE: 7.0
MY FINAL DECISION: Accept