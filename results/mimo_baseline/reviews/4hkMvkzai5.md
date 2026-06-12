## Summary
The paper proposes DeCodec, a neural audio codec that disentangles audio into orthogonal subspaces representing speech and background sound via a Subspace Orthogonal Projection (S) module and a Representation Swap Training (RST) procedure, with further semantic/paralinguistic decomposition within the speech subspace using semantic guidance. This hierarchical disentanglement enables a single codec to serve as a universal front-end for reconstruction, speech enhancement, voice conversion, and downstream ASR/TTS tasks.

## Strengths
- **Novel problem framing and approach**: Disentangling speech and background sound at the representation level of a codec is a genuinely new idea that addresses a practical gap. Existing codecs either entangle all audio types (EnCodec, DAC) or only decompose clean speech (SpeechTokenizer, DualCodec). The SOP+RST combination is technically creative—orthogonal projection enforces structural disentanglement while RST ensures semantic correspondence to speech vs. background sound, with an intuitive theoretical argument (Section 3.6) connecting the two.
- **Broad multi-task evaluation**: The paper demonstrates reconstruction quality, speech enhancement via simple representation swapping, one-shot VC on noisy speech, and reports downstream ASR/TTS results, showing the codec's versatility as a universal front-end. The ablation study (Table 4) clearly isolates the contribution of each component: SOP alone or RST alone fails at decoupling (SDR-B < -10 dB), but their combination yields strong separation.
- **Competitive SE via representation manipulation**: Achieving top DNSMOS scores on the DNS Challenge test set by simply replacing the background sound subspace with blank-audio representations is elegant and avoids the error propagation of cascaded pipelines. The causal DeCodec-c model matches or exceeds non-causal SELM, suggesting practical value for real-time applications.
- **Strong reconstruction results**: DeCodec achieves the highest SDR on both clean (7.61) and noisy (5.21) speech, indicating that disentanglement does not sacrifice reconstruction quality—a key concern.

## Weaknesses
### Fatal
None.

### Major
- **Bitrate mismatch obscures fair reconstruction comparison**: DeCodec operates at 8.0 kbps (4.0+4.0), substantially higher than all baselines (2.0–6.0 kbps). The superior SDR likely reflects this extra capacity. The paper should either compare at matched total bitrate or explicitly acknowledge this advantage in the reconstruction discussion.
- **Missing comparison with DualCodec and Mimicodec**: These are the closest related methods—both decompose speech into semantic and residual components. Only SpeechTokenizer is compared quantitatively. DualCodec and Mimicodec comparisons would directly validate the claim that synergistic optimization with BGS decoupling enhances robustness in noisy environments.
- **Voice conversion WER is very high**: DeCodec's one-shot VC achieves WER=50.46, meaning converted speech is largely unintelligible. The paper attributes this to voiced/unvoiced misalignment but doesn't quantify this effect or propose mitigation. For a method claiming to enable "effective one-shot voice conversion," this weakens the central narrative.
- **Theoretical argument (Section 3.6) has gaps**: The mean value theorem argument concludes that Zs₁ must be independent of n₁, but this relies on the decoder's Jacobian being well-behaved and the assumption that the equations hold exactly rather than approximately. The claim that "the covariance matrix YY^T satisfies the angular matrix" is neither defined nor verified empirically. These theoretical claims should be stated more carefully.

### Minor
- **SE comparison fairness**: DeCodec is trained on reconstruction + disentanglement objectives, while baselines (SELM, StoRM) are trained specifically for SE with SE losses. Direct DNSMOS comparison conflates training objective differences with architectural advantages.
- **Neuroscience motivation is loose**: The A2 cortex analogy is motivating but doesn't constrain the technical design—the SOP module is simply a learnable linear projection with orthogonality loss. Presenting it as brain-inspired may overstate the connection.
- **Training data details are sparse**: It is unclear how clean references s and n are isolated during training for the RST loss computation, and how mixing proportions are balanced across SNR ranges.

### Trivial
Minor formatting inconsistencies in equation numbering and some repeated figure captions.

## Nice-to-Haves
- Analysis of what happens when speech and background sound overlap significantly in frequency (e.g., competing talkers vs. environmental noise).
- Perceptual evaluation (MOS) for reconstruction quality, not just SDR and mel distance.
- Demonstration of background sound preservation in TTS (the paper mentions this capability but doesn't show quantitative results in the main text).

## Novel Insights
The key insight is that disentangling speech and background sound at the representation level of a codec—rather than in the signal domain via separation—preserves signal integrity while enabling flexible task-specific feature selection. The RST procedure provides a training-time mechanism that exploits the additive signal model (y = s + n) to force subspace correspondence: by requiring that recombined representations from different inputs reconstruct valid mixtures, the model is compelled to isolate speech-only and noise-only information in separate subspaces. This is a principled way to exploit the physical structure of the problem within a learned codec.

## Suggestions
- Add DualCodec and Mimicodec as baselines, especially for noisy reconstruction and ASR robustness.
- Evaluate SE using intrusive metrics (PESQ, STOI) in addition to DNSMOS for more complete assessment.
- Conduct a matched-bitrate experiment (e.g., single RVQ at 8 kbps for baselines) to isolate the effect of disentanglement architecture from raw capacity.
- Tone down theoretical claims or provide empirical verification of the orthogonality conditions (e.g., measure cos(S, N) and P_S P_N^T during training).

## Score and Decision
The paper presents a genuinely novel approach to disentangled audio coding with broad practical implications. The core idea is sound, the ablation clearly validates the components, and the multi-task demonstrations are compelling. However, the bitrate mismatch, missing baselines, high VC WER, and somewhat loose theoretical claims prevent a stronger endorsement. This is a solid contribution that would benefit from more rigorous experimental comparison.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <score>Accept</score>