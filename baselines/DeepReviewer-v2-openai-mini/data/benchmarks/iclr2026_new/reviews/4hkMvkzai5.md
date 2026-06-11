## Summary
# Final Review Report

## Summary

This paper presents DeCodec, a neural audio codec designed to learn disentangled representations that separate speech from background sound, and further decomposes speech into semantic and paralinguistic components. The key technical innovations are: (1) a Subspace Orthogonal Projection (SOP) module that uses trainable linear projections to separate speech and background sound into orthogonal subspaces, (2) a Representation Swap Training (RST) procedure that encourages the subspaces to correspond to speech and noise respectively, and (3) Semantic Guidance (SG) using HuBERT features to decompose speech into semantic and residual paralinguistic streams. The system is evaluated on audio reconstruction, speech enhancement, one-shot voice conversion, and downstream ASR/TTS tasks. Results show competitive reconstruction SDR at 8 kbps total bitrate, DNSMOS improvements in speech enhancement under a blank-audio-reference setting, and improved robustness for voice conversion on noisy speech compared to SpeechTokenizer-based baselines.

The paper addresses a relevant and underexplored problem: enabling controllable feature selection across speech and background sound components within a single codec framework. The hierarchical disentanglement idea is conceptually interesting and the ablation study confirms that both SOP and RST are necessary for effective decoupling. However, the paper has several significant weaknesses: (1) the mathematical derivation for the SOP orthogonality and the RST "theoretical proof" contain logical gaps that undermine the claimed guarantees, (2) the speech enhancement comparison is fundamentally unfair because DeCodec requires a separate blank audio as noise reference while baselines operate blindly, (3) the bitrate comparison in Table 1 is unequal (DeCodec uses 8 kbps vs 2-6 kbps for baselines), and (4) the one-shot VC still achieves only 50% WER, which is far from practical usability. Novelty conclusions are deferred for manual verification due to Retrieval-Disabled Mode in this run.

## Strengths
**1. Novel problem framing and architecture design.** The paper tackles a genuinely challenging problem: designing a single codec that can disentangle speech from background sound and semantic from paralinguistic content in a hierarchical manner. This goes beyond prior work in audio codecs, which either encode everything into a single stream (EnCodec, DAC) or only decompose clean speech (SpeechTokenizer). The three-module architecture (SOP + RST + SG) is well-motivated and each component addresses a specific sub-problem.

**2. Comprehensive ablation study (Table 4).** The ablation systematically evaluates the contribution of each module. The results clearly show that neither SOP nor RST alone achieves effective decoupling (SDR-B of -13.15 and -10.67 dB respectively), while their combination (Ablation-3) jumps to SDR-B=0.49 dB. This provides strong evidence that the proposed joint design is necessary. The progressive addition of SG then demonstrates the expected trade-off between reconstruction fidelity and semantic preservation.

**3. Broad multi-task evaluation.** The paper evaluates DeCodec on reconstruction, speech enhancement, one-shot voice conversion, and reports downstream ASR/TTS performance in appendices. This breadth demonstrates the versatility of the disentangled representation approach and its potential as a universal front-end. The inclusion of causal and non-causal variants (DeCodec-c and DeCodec) shows awareness of deployment constraints.

**4. Neuroscience-inspired motivation.** The connection to the secondary auditory cortex (A2) processing speech and background sounds in separate regions provides an engaging biological motivation. While the mapping to algorithmic components is metaphorical rather than mechanistic, it helps readers intuitively grasp the design philosophy behind SOP and RST.

## Weaknesses
### W1. Mathematical flaws in the orthogonality claim (SOP module, Section 3.4)
The paper asserts that SOP achieves "complete decoupling between speech and background sound representations" through orthogonal projection matrices. However, the derivation contains several problems: (i) The inner product notation in Eq. (5) is ambiguous for tensor-valued S and N—whether it denotes a Frobenius inner product, vector dot product, or something else is unspecified. (ii) The term "angular matrix" for the covariance matrix YY^T is not a standard linear algebra concept and is neither defined nor cited. (iii) The claim $\mathbf{P}_S + \mathbf{P}_N = \mathbf{I}$ (complementarity) is asserted without proof, but two independently trained linear projection layers will not automatically satisfy this property. Without complementarity, Y ≠ S + N, which means the encoder output is not fully decomposed into the two subspaces. (iv) The derivation attempting to show $\mathbf{P}_S \mathbf{P}_N^T = \mathbf{0}$ from $\mathcal{L}_\perp$ is circular: the loss enforces S·N = 0, which already encodes the orthogonality condition. These issues mean the "theoretical guarantee" of complete decoupling is not mathematically established. **Impact: The foundational claim of the paper—guaranteed orthogonal disentanglement—is not supported by the presented mathematics.**
- **Severity: Major | Fixability: Fixable by reframing claims as soft constraints and removing unsubstantiated theoretical statements.**
- **Required action:** Rewrite Section 3.4 to present SOP as an *encouragement* of orthogonality rather than a guarantee. Remove the "angular matrix" statement. Add a residual connection or explicit complementarity loss to ensure Y ≈ S + N.

### W2. Unfair comparison for speech enhancement (Section 4.2.2)
DeCodec's speech enhancement procedure replaces the background sound representation Zn of the noisy mixture with the Zn extracted from a "blank audio with the same length." This means DeCodec has access to a clean noise reference recording, while the competing SE baselines (InterSubNet, StoRM, SELM) operate blindly—they receive only the noisy mixture and must separate speech from noise without a separate noise sample. This is a fundamentally easier setting for DeCodec. The paper does not disclose this limitation when comparing DNSMOS scores and claiming "superior speech enhancement." Furthermore, in real-world deployment, a blank reference recording is rarely available. **Impact: The claim of SOTA speech enhancement is misleading because the evaluation setting is not comparable.**
- **Severity: Major | Fixability: Fixable by clearly disclosing the blank-audio assumption and adding a blind SE experiment.**
- **Required action:** (a) Explicitly state in the main text that SE comparison is under a blank-reference condition, (b) add a blind SE experiment where Zn is set to zero or estimated, (c) remove or qualify the claim of "superior" SE.

### W3. Unequal bitrate in reconstruction comparison (Table 1)
DeCodec operates at 4.0+4.0 = 8 kbps total bitrate (two parallel 4 kbps streams for speech and background sound). The baselines in Table 1 use substantially lower bitrates: EnCodec (6 kbps), HiFi-Codec (2 kbps), DAC (4.5 kbps), SpeechTokenizer (4 kbps). The SDR metric is highly sensitive to bitrate—higher bitrate almost always translates to higher SDR, particularly on noisy signals. The paper's claim that "DeCodec achieves the highest SDR" and "performs comparably to existing codec models" is therefore misleading because the comparison is at unequal bitrates. The 2-5 dB SDR advantage over baselines may be largely attributable to the 2-4x bitrate difference rather than architectural superiority. **Impact: Core performance claims are confounded by bitrate disparity.**
- **Severity: Major | Fixability: Fixable with matched-bitrate experiments.**
- **Required action:** (a) Add a footnote clearly stating total bitrate for all models, (b) train DeCodec variants at 4 kbps and 6 kbps for fair comparison, (c) report SDR per bitrate to isolate architectural gains from rate gains.

### W4. The RST "theoretical proof" (Section 3.6) is logically unsound
The paper claims to theoretically prove that the RST loss forces Zs and Zn to contain only speech-only and noise-only information. The proof attempts to use the vector-valued mean value theorem, but: (i) The MVT for vector functions does not guarantee a single ξ for all output dimensions simultaneously. (ii) The decoder takes the sum Zs+Zn, so ∂Dec/∂Zn depends on Zs through the decoder nonlinearity—the claim that "the left side depends on Zs₁ through ξ, while the right side is independent of Zs₁" is based on an incorrect factorization. (iii) Equations (13)-(14) are approximate equalities from training, not mathematical identities, so subtracting them yields an approximate equality that cannot support rigorous deduction about independence. (iv) The conclusion "Zs must be independent of n₁" is a non-sequitur: the equation only shows the decoder output difference does not depend on Zs₁, which does not prove Zs₁ itself contains no noise information. **Impact: The claimed theoretical guarantee of disentanglement is not valid.**
- **Severity: Major | Fixability: Fixable by removing the word "proof" and reframing as intuitive motivation supported by ablation.**
- **Required action:** Replace the "theoretical proof" with an intuitive explanation of why the swap mechanism empirically encourages disentanglement, citing the ablation study (Table 4) as evidence.

### W5. SG loss function has numerical issues and incomplete design (Eq. 7)
The SG loss $\mathcal{L}_{\text{SG}} = \|\log \sigma(\cos(\mathbf{WZc}, \mathcal{H}))\|_1$ is needlessly complex. The three-step composition (cosine→sigmoid→log→L1) can produce numerical instability if sigmoid saturates to exactly 0 or 1, and the log of sigmoid for cosine values in [-1,1] produces outputs in [-1.31, -0.32] whose L1 norm is just a negative sum—effectively reweighting cosine similarity in a non-intuitive way. Furthermore, there is no loss term to ensure that the residual paralinguistic representation Zr does not contain redundant semantic information. This means the semantic-paralinguistic decomposition is only enforced on the first RVQ layer, with no guarantee that later layers don't reconstruct the same semantic content. **Impact: The hierarchical disentanglement within speech is incompletely supervised.**
- **Severity: Major | Fixability: Fixable with a simpler loss and a redundancy reduction term.**
- **Required action:** (a) Replace log-sigmoid-cosine with a direct cosine distance loss $1 - \cos(\mathbf{WZc}, \mathcal{H})$, (b) add a redundancy reduction loss between Zc and Zr, (c) verify numerical behavior across training.

### W6. One-shot VC evaluation issues (Section 4.2.3)
The one-shot VC experiment shows WER of 50.46%, meaning every other word is incorrect. This is far from practical usability. The paper's explanation ("different speech segment voicing times") is speculative—no spectral analysis, pitch analysis, or ablation controlling for voicing mismatch is provided. Additionally, the speaker similarity (SIM) metric is confusing: the "Reference" row shows SIM=0.69, but the converted speech achieves SIM=0.83 (higher than the reference itself). This suggests either the SIM metric is not measuring what it claims, or the "Reference" baseline uses a different definition. The comparison also bundles VC with SE (noise removal), making it unclear whether the improvements come from better voice conversion or better noise suppression. **Impact: The VC results are not convincingly analyzed and may not support the claim of effective semantic-paralinguistic decomposition.**
- **Severity: Major | Fixability: Partially fixable with additional analysis and controlled experiments.**
- **Required action:** (a) Disentangle SE and VC: report pure VC on clean speech separately, (b) clarify the SIM metric definition, (c) add voicing/pitch analysis to support the proposed failure explanation, (d) acknowledge the practical limitation of 50% WER.

### W7. Writing quality and grammatical errors
The manuscript contains several grammatical errors and awkward phrasings that reduce readability and professional polish:
- "an universal" (should be "a universal") — appears multiple times including in the title and abstract.
- "These allows" (subject-verb disagreement) in the abstract.
- "we proposes" in Section 1 instead of "we propose".
- "SOP vlock" in the ablation text (likely a typo for "SOP block").
- "inferior apply to" should be "inferior when applied to".
While these are minor individually, their cumulative effect suggests insufficient proofreading.
- **Severity: Minor | Fixability: Fully fixable through careful revision.**
- **Required action:** Careful copy-editing pass throughout.

### W8. Conclusion is too brief and avoids discussing limitations
The conclusion section is only two sentences long. It does not list any quantitative findings (SDR, DNSMOS, WER values) and defers all limitations to Appendix H. A conclusion should summarize key validated outcomes and explicitly state bounded limitations so readers can quickly assess the paper's contributions and scope without consulting appendices.
- **Severity: Minor | Fixability: Easily fixable.**
- **Required action:** Expand conclusion to 4-5 sentences with key quantitative results, main limitations, and future directions.

## Score
**Final Score: 5/10**

**Score Rationale:** The score reflects the paper's balance between a compelling central idea (hierarchical disentanglement in audio codecs) and significant weaknesses in theoretical rigor, experimental fairness, and evidence completeness.

**Positive factors supporting the score:**
- The hierarchical disentanglement problem is important and timely.
- The three-component architecture (SOP+RST+SG) is well-motivated and the ablation study convincingly demonstrates their joint necessity.
- Multi-task evaluation (reconstruction, SE, VC, ASR, TTS) shows versatility.
- Both causal and non-causal variants are provided, demonstrating deployment awareness.

**Negative factors constraining the score:**
- The mathematical claims of guaranteed orthogonality and disentanglement (SOP, RST) are not supported by the presented derivations, which contain logical gaps and undefined terminology (W1, W4).
- The speech enhancement comparison is fundamentally unfair—DeCodec uses a blank audio reference while baselines operate blindly (W2). This makes the claimed SOTA SE performance misleading.
- The reconstruction comparison (Table 1) is confounded by unequal bitrates (DeCodec 8 kbps vs baselines 2-6 kbps), undermining the core performance claim (W3).
- The SG loss function is numerically fragile and the semantic-paralinguistic decomposition lacks a redundancy reduction constraint (W5).
- The VC evaluation has WER=50% (too high for practical use) and the analysis of failure modes is speculative (W6).
- Minor but noticeable grammatical errors reduce readability (W7).

**Revision potential:** With substantial revisions—fixing the mathematical claims, adding matched-bitrate and blind-SE experiments, redesigning the SG loss, and expanding the conclusion—the paper could reach a 7-8/10 level. The core idea is solid; the main issues are in the execution and evidence presentation.

**Novelty statement (deferred):** Due to Retrieval-Disabled Mode in this run, external literature verification was not performed. Novelty claims (e.g., "first to achieve explicit decoupling of speech and background sound in the feature domain") are marked for manual verification.