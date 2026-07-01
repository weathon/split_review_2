## Summary
The paper proposes DeCodec, a neural audio codec that learns to hierarchically disentangle audio representations into orthogonal subspaces for speech and background sound, and further decompose speech into semantic and paralinguistic components. The key technical contributions are a Subspace Orthogonal Projection (SOP) module, a Representation Swap Training (RST) procedure, and semantic guidance (SG) within the quantizer. Experiments show that DeCodec achieves competitive reconstruction quality while enabling controllable feature selection for speech enhancement, one-shot voice conversion, and downstream ASR/TTS tasks.

## Strengths
- **Clear and well-motivated problem**: The paper identifies a genuine limitation of existing audio codecs—they entangle speech and background sound—and proposes a principled solution inspired by human auditory processing. The motivation for a unified disentangled representation is compelling.
- **Novel combination of techniques**: The SOP module enforces orthogonal subspaces, the RST procedure forces those subspaces to correspond to speech and background sound, and SG further decomposes speech. This combination is novel and the ablation study convincingly shows that all three components are necessary for effective decoupling.
- **Comprehensive experimental evaluation**: The paper evaluates DeCodec on multiple tasks (reconstruction, speech enhancement, one-shot VC) with strong baselines, and includes an ablation study that isolates the contribution of each module. The results demonstrate that DeCodec can match or exceed specialized models in several settings.
- **Practical impact**: The ability to selectively retain or suppress background sound in the representation domain without cascaded front-end separation has clear advantages for multi-task audio processing and could simplify system design.

## Weaknesses
### Fatal
None.

### Major
- **The theoretical justification for the RST procedure is not rigorous.** The argument in Equations (13)–(16) relies on the mean value theorem for vector functions and assumes that the decoder’s Jacobian with respect to Zn is well-behaved and that the subtraction of outputs cancels the dependence on Zs. For a nonlinear neural decoder, this reasoning is heuristic at best and does not constitute a proof that Zs is independent of background sound. The paper’s core claim of guaranteed decoupling is therefore not fully supported.
- **Bitrate mismatch in reconstruction comparisons.** DeCodec uses 8 kbps (4.0+4.0) while baselines use lower bitrates (EnCodec 6.0, HiFi-Codec 2.0, DAC 4.5, SpeechTokenizer 4.0). Higher bitrate naturally improves reconstruction quality, so the reported SDR advantage may partly reflect bitrate rather than architectural superiority. The paper does not control for this or discuss the limitation.
- **Ablation study reveals a significant trade-off.** Adding SG (full DeCodec) degrades SDR-B (background sound SDR) from 0.49 to -1.11 and SDR-S (speech SDR) from 7.90 to 5.70 compared to Ablation-3 (SOP+RST without SG). The paper calls this a “slight decrease,” but the drop is substantial and indicates that semantic guidance interferes with the decoupling of speech and background sound. This trade-off is not adequately analyzed or addressed.

### Minor
- **Overclaim of “first time.”** The paper states it achieves “explicit decoupling representation of speech and background sound in the feature domain for the first time.” Prior work on factorized codecs (e.g., FACodec) and latent speech separation methods has explored disentanglement in the feature domain, albeit with different goals. The claim should be more carefully qualified.
- **One-shot VC results remain high WER (50.46).** While DeCodec improves over baselines, the converted speech is still far from intelligible. The paper acknowledges voicing mismatch but does not provide a clear path to making the method practical for voice conversion.
- **Dependence on a large pre-trained model.** Semantic guidance uses HuBERT-L9, a large self-supervised model. This adds a dependency that may limit the “universality” of the approach and increase computational cost.

### Trivial
- Table 4 column headers (“SDR-O”, “SDR-B”, “SDR-S”) are not explicitly defined in the main text; the reader must infer their meaning from the ablation description.

## Nice-to-Haves
- Include a reconstruction comparison with a codec baseline at a matched bitrate (e.g., EnCodec at 8 kbps) to isolate the effect of the decoupling mechanism.
- Provide a quantitative analysis of how well the orthogonality constraint (L_perp) is satisfied during training (e.g., plot of the cosine similarity between S and N over training steps).
- Discuss the computational overhead of the SOP module and RST procedure relative to a standard codec.

## Novel Insights
The paper’s central insight is that a codec’s reconstruction objective can be leveraged to learn disentangled subspaces for speech and background sound without requiring explicit time-domain separation. By combining orthogonal projection with a representation swap training procedure, the model is forced to allocate separate subspaces to the two sources, and the decoder learns to recombine them. This is a more elegant and unified approach than cascaded pipelines, and it opens the door to using a single codec as a universal front-end for multiple audio tasks.

## Suggestions
- Strengthen the theoretical analysis of the RST procedure by either providing a more rigorous proof under realistic assumptions (e.g., Lipschitz continuity of the decoder) or clearly stating the heuristic nature of the argument.
- Add experiments with matched bitrate to ensure fair comparison with baselines.
- Investigate the trade-off between decoupling quality and semantic decomposition more thoroughly, and consider alternative ways to incorporate semantic guidance (e.g., a separate loss term that does not affect the orthogonality constraint).

## Score and Decision
MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>