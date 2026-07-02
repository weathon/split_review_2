## Summary
This paper presents USR 2.0, a semi-supervised framework for unified audio, visual, and audiovisual speech recognition (ASR/VSR/AVSR) that improves upon the prior USR system. The core contribution is CTC-driven teacher forcing, where greedily-decoded CTC pseudo-labels (PLs) are fed into the attention decoder to generate attention-based PLs in a single forward pass, replacing slow autoregressive (AR) decoding. Because CTC and CTC-driven attention PLs share the same sequence length after collapse, the student decoder can predict both simultaneously, coupling the two branches. A mixed-sampling strategy (randomly alternating between CTC-driven mode and AR mode with probability 0.5) mitigates exposure bias from relying solely on CTC inputs during training.

The method achieves approximately 2x faster training than USR, strong robustness to out-of-distribution inputs (long utterances beyond 155 frames, additive noise down to -5 dB SNR, and cross-dataset evaluation on LibriSpeech/WildVSR/AVSpeech), and competitive or state-of-the-art WER on LRS3, LRS2, and WildVSR benchmarks across all three tasks with a single unified model. Ablations confirm that both CTC and attention-based PL targets contribute to in-distribution accuracy and out-of-distribution robustness.

The paper is clearly written, the technical contribution is well-motivated, and the empirical coverage (long utterances, noise, OOD datasets, model scaling) is broader than typical speech recognition papers. However, several issues limit the strength of the claims: the absence of statistical significance testing (no variances or confidence intervals on WER), unspecified architectural details about how CTC tokens condition the decoder, and insufficient decomposition of training time savings (per-step vs. convergence). Novelty assessment is deferred as external literature verification was unavailable in this run.

## Strengths
1. **Well-motivated technical contribution.** The paper identifies a genuine bottleneck in USR—autoregressive pseudo-label generation—and proposes a clean, conceptually elegant solution: CTC-driven teacher forcing. The insight that globally incoherent attention outputs are still useful for pseudo-labeling as long as teacher and student share the same conditioning is non-trivial and practically valuable.

2. **Comprehensive robustness evaluation.** Unlike many speech recognition papers that focus exclusively on in-distribution benchmarks, USR 2.0 evaluates robustness across three distinct OOD dimensions: long utterances (up to 600 frames, well beyond the 155-frame training maximum), additive noise at multiple SNR levels (10 dB to -5 dB), and cross-dataset shifts (LibriSpeech, WildVSR, AVSpeech). This multi-axis evaluation substantially strengthens the paper's core claim of improved robustness.

3. **Unified model across all three tasks.** USR 2.0 maintains a single set of parameters for ASR, VSR, and AVSR, unlike most prior work that trains separate models per task. This is a practically meaningful contribution for deployment efficiency, and the results show that unification does not come at a significant accuracy cost.

4. **Training efficiency improvement.** The approximately 2x reduction in wall-clock training time is practically significant for scaling semi-supervised learning to larger models and datasets. The efficiency gain comes from both faster per-step decoding (CTC-driven mode avoids AR) and faster convergence (fewer epochs), and the improvement is demonstrated across multiple model scales (Base, Base+, Large, Huge).

5. **Clear ablation design.** Table 4 systematically ablates the contribution of each PL type (CTC vs. attention-based) for each branch (CTC head vs. decoder) under both CTC-driven and AR modes. This provides a clear understanding of which components drive ID vs. OOD performance.

6. **Transparency about limitations of prior work.** The paper explicitly analyzes two failure modes of USR (AR bottleneck and decoupled supervision leading to cascading errors) and validates these empirically, grounding the motivation for USR 2.0 in both logical argument and data (Figure 1).

## Weaknesses
### W1. Missing statistical significance and variance reporting (Major)
All WER results in Tables 1-3, Figure 3, and Table 2 are reported as point estimates without standard deviation, confidence intervals, or significance tests. It is unclear whether results are averaged over multiple seeds (and if so, how many) or from a single run. For in-distribution comparisons where the delta is small (e.g., USR 2.0 AVSR 2.9% vs USR 3.0% on Base LRS3, Table 2), the absence of variance makes it impossible to determine statistical reliability. This is particularly important for the paper's core claim of "improved robustness"—readers need to know whether gains are stable across training runs. The paper should report mean ± std over at least 3 random seeds for all key experiments.

**Impact:** Without statistical evidence, the significance of some reported improvements cannot be assessed, weakening the paper's central claims.

### W2. Training efficiency claim lacks decomposition (Major)
The paper claims "approximately 2x faster training" but does not decompose the speedup into per-step decoding efficiency vs. faster convergence (50 vs. 75 epochs). These are mechanistically different: per-step speedup comes from CTC-driven teacher forcing avoiding AR decoding; faster convergence suggests a learning advantage that should be explained. The current text conflates the two factors (Page 1, Sections 6, "Training efficiency"). Moreover, the 2x figure may depend on hardware (H200 GPU), model size, and the 50% AR-mode probability. Without decomposition, readers cannot assess which aspect of the method drives efficiency improvements or how generalizable the savings are to different configurations.

**Impact:** The efficiency claim is plausible but undersupported; the mechanism behind faster convergence is unclear.

### W3. Decoder token conditioning unspecified (Major)
The central technical contribution—CTC-driven teacher forcing—lacks architectural specificity. The paper does not specify how the collapsed CTC token sequence $\tilde{y}^{\text{CTC}}$ is fed into the decoder (Page 1, Section 4.1). Is it via token embedding + positional encoding used as decoder self-attention input, with cross-attention to encoder outputs as in standard AR decoding? Or is the conditioning mechanism different? This ambiguity affects reproducibility. Additionally, the collapse operation is described as "standard CTC post-processing" but different implementations (e.g., merging repeated non-blank tokens vs. keeping them) produce different $U_{\text{CTC}}$ lengths, which directly affects the decoder's input-output alignment.

**Impact:** Reproducibility is compromised; researchers cannot re-implement the core idea from the description alone.

### W4. Strong SOTA claims without comprehensive comparison (Moderate)
The paper makes "state-of-the-art" claims (Abstract, Introduction) but compares against a specific set of baselines under specific resource settings. The claim "achieves state-of-the-art WER in various semi-supervised settings across ASR, VSR, and AVSR" (Page 1) should be scoped to "outperforms prior semi-supervised methods on LRS3 under the evaluated settings" since a comprehensive literature survey was not provided. The Huge model additionally uses LRS2 labelled data, which differs from the smaller models' training set, making direct scaling claims ambiguous.

**Impact:** SOTA claims may be perceived as overreaching without broader contextualization.

### W5. Whisper-as-oracle evaluation limitation (Moderate)
The long-utterance evaluation (Section 5.1) uses Whisper transcriptions as ground truth for computing WER on VoxCeleb2 samples. Whisper itself has known limitations on long-form audio and diverse accents. The paper does not discuss this measurement noise or validate Whisper's accuracy on a human-transcribed subset. The OOD AVSpeech evaluation (Section 5.3) similarly uses Whisper for transcription. This introduces an uncontrolled source of error that could differentially affect methods.

**Impact:** The OOD numerical results may be partially confounded by Whisper transcription errors, which could favor methods whose error patterns align with Whisper's.

### W6. Conclusion over-extends beyond evidence (Minor)
The final paragraph of the Conclusion (Page 1, Section 8) speculates about applying CTC-driven teacher forcing to handwriting recognition, music transcription, and DNA/protein sequencing without any supporting evidence or analysis of domain-specific constraints (polyphonic output, non-monotonic alignment, different signal characteristics). While forward-looking statements are acceptable, these claims are presented as direct implications of the current work rather than speculative future directions.

**Impact:** Weakens otherwise strong conclusion with unsupported extrapolation.

### W7. Ablation analysis gap: ID/OOD uncorrelated trends (Minor)
The observation that "ID and OOD trends are largely uncorrelated" (Page 1, Section 7, AR mode) is significant but underexplored. It suggests that ID-optimized designs may fail under distribution shift, which is directly relevant to the paper's central thesis. A mechanistic explanation would strengthen the paper; e.g., does CTC-driven mode dominate OOD robustness even under mixed sampling because the coupled loss anchors decoder representations?

**Impact:** An interesting finding is left as an observation without attempted explanation.

### W8. Missing discussion of teacher-student input discrepancy (Minor)
USR's teacher generates PLs from unmasked inputs while the student operates on masked inputs. This creates a fundamental asymmetry: the teacher's PLs may reflect information unavailable to the student. The paper does not discuss how this affects PL quality or whether CTC-driven teacher forcing changes this dynamic.

**Impact:** Potentially important factor in understanding PL quality limitations is not addressed.

### Novelty Assessment
Due to external literature search being unavailable in this run, novelty and comparison conclusions are deferred for manual verification. The technical approach (CTC-driven teacher forcing with mixed sampling) appears to be a novel combination to the reviewer's internal knowledge, but a rigorous novelty assessment against concurrent work in CTC-conditioned decoding, scheduled sampling variants for speech, and non-autoregressive semi-supervised ASR is needed before final judgment.

## Score
**Final Score: 6.5/10**

**Rationale:** The paper presents a clean, well-motivated technical contribution (CTC-driven teacher forcing with mixed sampling) and backs it with broader-than-usual robustness evaluation across multiple OOD dimensions. The 2x training speedup and strong OOD results are practically valuable. However, the score is tempered by several factors: (1) the absence of statistical significance testing for all WER results, which is essential for a system claiming improved robustness; (2) underspecified architectural details that hinder full reproducibility of the core contribution; (3) SOTA claims that are not scoped precisely enough; and (4) training efficiency claims that conflate per-step speedup with convergence improvement. The novelty dimension could not be fully assessed due to unavailable external literature retrieval, so the score primarily reflects manuscript-internal evidence quality. The paper is solid and publishable with moderate revisions, but the current evidentiary gaps prevent a higher rating.