## Summary
DeCodec rethinks neural audio codecs as universal disentangled representation learners by introducing a subspace orthogonal projection (SOP) module and a representation swap training (RST) procedure to explicitly decouple speech and background sound in the feature domain. Within speech, semantic guidance further separates semantic and residual paralinguistic information, enabling a single codec to support speech enhancement, one-shot voice conversion, and downstream ASR/TTS tasks through controllable feature recombination.

## Strengths
- **Novel and well-motivated framework**: The paper identifies a clear gap—existing codecs entangle speech and background sound—and proposes a principled approach inspired by auditory cortical processing (A2). The combination of SOP, RST, and SG is technically innovative and moves beyond simple cascaded pipelines.
- **Convincing empirical results on multiple tasks**: DeCodec achieves competitive SDR on noisy speech reconstruction, outperforms dedicated SE models (e.g., StoRM, SELM) on DNSMOS OVL and BAK scores, and lowers WER in one-shot VC on noisy speech compared to SpeechTokenizer with front-end denoising. The ablation study (Table 4) cleanly demonstrates that both SOP and RST are necessary for effective decoupling, and SG enables hierarchical semantic/paralinguistic separation.
- **Unified front-end for diverse tasks**: The paper shows that a single trained DeCodec can serve speech enhancement, voice conversion, and potentially ASR/TTS without task-specific fine-tuning. This universality is a strong value proposition, reducing the need for separate front-end processing modules.
- **Sound theoretical motivation and rigorous formulation**: The orthogonal subspace decomposition is formalized with projection operators and a concrete orthogonality loss (ℒ⊥). The RST proof, while heuristic, provides intuitive justification for why the swapped reconstruction forces subspace specialization.

## Weaknesses
### Fatal
None. The core claims are supported by experiments, and no result invalidates the overall contribution.

### Major
1. **Limited baselines for disentanglement and VC tasks**: The one-shot VC comparison (Table 3) only includes SpeechTokenizer and a cascaded StoRM-SpeechTokenizer. Many recent disentangled speech codecs (e.g., FACodec, Mimicodec, DualCodec) are mentioned in related work but not compared directly in VC or SE under noise. Without these comparisons, it is unclear whether DeCodec’s hierarchical disentanglement provides an advantage over existing speech-only decoupling methods when combined with a separate denoising front-end.
2. **Heuristic theoretical justification for RST**: The mean-value-theorem argument (Section 3.6) is mathematically informal and relies on a linearization assumption that may not hold for a complex nonlinear decoder. While the empirical ablation (Table 4) strongly supports RST’s importance, the paper markets the theory as a rigorous proof. This mismatch weakens the paper’s theoretical contribution.
3. **Missing efficiency analysis**: The paper claims “computational efficiency via feature selection” (in the introduction) but provides no FLOPs, parameter count, or inference time comparisons with baselines. Given that DeCodec uses two separate RVQs (4+4 kbps) and both SOP and RST require forward passes for two inputs during training, a complexity analysis is necessary to substantiate the efficiency claim.
4. **No objective metrics for background sound extraction quality**: The decoupling performance is only reported via SDR-B and SDR-S in the ablation (Table 4), not in the main SE or reconstruction tables. For a paper claiming “universal disentangled representation”, the quality of the extracted background sound (e.g., ISR, SAR, or PESQ) should be evaluated separately to confirm that the background representation is indeed informative and not merely discarded noise.

### Minor
- The computational graph during RST training is somewhat unclear: two mixed samples are fed separately, and only one combination is used in the swap loss. The paper could better explain how the soft orthogonality loss ℒ⊥ interacts with the RST loss when both are applied per iteration.
- The DNSMOS SIG score for DeCodec on real recordings (3.45) is lower than SELM (3.59). The paper attributes this to quantization loss, but an ablation with higher bitrate would strengthen the analysis of the reconstruction–decoupling trade-off.
- The WER for one-shot VC (50.46%) is still very high. The authors mention timing mismatches but do not analyze whether semantic-paralinguistic decomposition is clean enough to transfer speaker identity without artifacts.

### Trivial
- The text references a footnote on “Hubert-L9” but the footnote content is omitted; such minor formatting issues do not affect the technical evaluation.

## Nice-to-Haves
- A direct comparison with other orthogonal decomposition or disentanglement methods (e.g., dropout-based separation, information bottleneck) applied to the codec backbone.
- A plot showing decoupling quality (SDR-B, SDR-S) as a function of input SNR to demonstrate robustness.
- An analysis of the subspaces (e.g., PCA or cosine similarity) to visually confirm that S and N representations lie in orthogonal subspaces after training.

## Novel Insights
None beyond the paper’s own contributions.

## Suggestions
1. Add a computational efficiency comparison (model size, FLOPs per second of audio, total parameters) against EnCodec, DAC, and SpeechTokenizer to support the efficiency claim.
2. Evaluate the quality of the extracted background sound representation (e.g., by decoding only the BRVQ output and measuring SDR/STOI against the ground-truth noise).
3. Replace the heuristic RST proof with a more rigorous argument or clearly state it as an intuitive justification; the current presentation over-claims rigor.
4. Include comparisons with other disentangled speech codecs (e.g., FACodec, Mimicodec) on the same VC and SE tasks, ideally with a noise-aware variant of those baselines.

## Score and Decision
**Score**: 7.0 – The paper presents a novel, well-motivated, and empirically strong contribution that rethinks audio codecs as universal disentangled representation learners. While a few comparisons and theoretical formalities could be strengthened, the core idea and experimental validation justify acceptance at a top venue.

**Decision**: Accept

MY FINAL SCORE: <score>7.0</score>  
MY FINAL DECISION: <decision>Accept</decision>