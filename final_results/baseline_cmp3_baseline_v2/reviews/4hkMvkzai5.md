## Summary
The paper proposes **DeCodec**, a neural audio codec that learns a hierarchical disentangled representation of speech and background sound, and further decomposes speech into semantic and paralinguistic components. Two technical innovations enable this: a **Subspace Orthogonal Projection (SOP)** module that factorizes the encoder output into orthogonal subspaces, and a **Representation Swap Training (RST)** procedure that enforces the subspaces to correspond to speech and background sound. The model additionally uses semantic supervision (HuBERT) within the speech quantization to separate semantic and paralinguistic information. DeCodec is evaluated on reconstruction, speech enhancement, one-shot voice conversion, ASR, and TTS, showing competitive performance across tasks while enabling novel feature selection capabilities from a single model.

## Strengths
- **Novel problem framing and methodology.** The paper reframes the audio codec as a universal disentangled representation learner, which is a conceptually appealing and practically useful direction. The combination of orthogonal projection with a representation swap training loss is a clever and technically sound approach to enforce decoupling of speech and background sound.
- **Comprehensive evaluation.** The experimental suite covers reconstruction, speech enhancement, voice conversion, and downstream tasks (ASR/TTS in appendices). The results demonstrate that DeCodec can serve as a unified front-end for multiple audio tasks without task-specific fine-tuning, reducing the need for cascaded pipelines.
- **Theoretical and empirical support for decoupling.** The paper provides a theoretical argument (mean value theorem) for why RST forces the quantized vectors to be content-specific, and the ablation study confirms that both SOP and RST are necessary for effective decoupling.
- **Practical flexibility.** The model offers both causal and non-causal variants, and the disentangled representations allow controllable suppression or preservation of background sound, which is valuable for real-world applications.

## Weaknesses

### Major
- **Trade-off between reconstruction fidelity and disentanglement.** On clean speech reconstruction (Table 1), DeCodec achieves lower SDR than EnCodec and substantially worse Mel distance than DAC (0.89 vs. 0.65), suggesting that the decoupling mechanism may come at a non-trivial cost in acoustic quality. This trade-off is not thoroughly discussed.
- **High WER in one-shot voice conversion.** Even with noise removal, the converted speech WER (50.46%) is very high, far beyond what is considered usable for speech conversion. The authors acknowledge voicing mismatch as a cause, but this severely limits the practical value of the VC application. More analysis or mitigation would be needed.
- **Heuristic theoretical justification.** The proof using the mean value theorem (Equations 13–16) relies on a linear approximation of the decoder and assumes the existence of $\xi$ in a way that is not rigorous for a deep neural network. The argument is more intuitive than formal, which weakens the claimed theoretical guarantee.

### Minor
- **Reliance on clean speech for HuBERT supervision.** The semantic guidance loss (Equation 7) requires clean speech signals $\mathbf{s}$ during training. This limits the training data to mixtures where clean reference is available, which may constrain generalization to in-the-wild noisy data.
- **Limited evaluation metrics for speech enhancement.** Only DNSMOS non-intrusive metrics are reported. Adding PESQ or STOI would strengthen the speech enhancement comparison, especially since baseline models (e.g., SELM) were originally evaluated on these metrics.
- **Single HuBERT layer (L9) used.** The choice of which layer and model size is not ablated. The semantic guidance may be sensitive to this choice, and the robustness of the decomposition to different semantic targets is not explored.

### Trivial
- Some figure descriptions are overly detailed (e.g., Figure 1 caption repeats the illustration text in full).
- The paper uses many acronyms; a table of abbreviations would improve readability.

## Nice-to-Haves
- Ablation of the number of RVQ layers for speech and background sound individually, to study the impact on reconstruction and decoupling quality.
- A direct comparison with a simple alternative: using a speech separation model (e.g., Conv-TasNet) as a front-end followed by a standard codec (e.g., DAC) on the separated streams. This would isolate the benefits of representation-domain decoupling.
- Analysis of the orthogonality measure $\mathcal{L}_\perp$ during training and inference to verify that the subspaces remain orthogonal when the model encounters real noisy data.

## Novel Insights
The paper’s core insight—that an audio codec can be trained to produce factorized, task-selectable representations by imposing structure through orthogonal projection and swap training—extends beyond the specific setting. It suggests that other forms of mixture decomposition (e.g., music and voice, different instrument streams) could be achieved within a similar codec framework, turning the codec from a compression tool into a general purpose representation learner. The hierarchical disentanglement (speech–background, then semantic–paralinguistic) is a natural extension of the human auditory cortical organization mentioned in the introduction, and the paper demonstrates its feasibility with a single model.

## Suggestions
1. Provide a more thorough discussion of the reconstruction quality trade-off and consider whether the disentanglement can be made less costly (e.g., by increasing codebook size or adjusting the orthogonality weight).
2. Investigate the high WER in VC more systematically—e.g., by performing controlled experiments with synthetic mixtures at known SNR or by allowing the source and reference representations to be aligned in time before swapping.
3. Include a simple baseline that replaces the SOP+RST module with two separate codec encoders (one for speech, one for noise) to empirically show the advantage of shared encoder with orthogonal projection.
4. Add supplementary experiments with alternative semantic guidance models (e.g., WavLM or different HuBERT layers) to demonstrate robustness.

## Score and Decision
**Score:** 6.5  
**Decision:** Accept  

**Rationale:** The paper presents a novel and well-motivated framework for disentangled audio representation learning at the codec level. The technical contributions (SOP, RST, SG) are clearly described and empirically validated. The evaluation is broad and shows DeCodec’s potential as a unified front-end. However, the reconstruction quality trade-off and the very high WER in voice conversion are significant limitations that prevent the work from being a strong acceptance. The paper is at the borderline between borderline accept and accept; given the novelty and the thoroughness of the experiments, I lean toward acceptance. The authors should address these concerns in the final version to strengthen the practical impact.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>