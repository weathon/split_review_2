Now I have enough information to finalize. Let me write the consolidated review.

**Round-1 bracket**: Based on calibration anchors, the paper sits between RepCodec (5.50, Reject) and GenSE (6.00, Accept). It has stronger novelty than RepCodec but less rigorous evaluation than GenSE. The brackets are:
- Strong reject (< 1.5): No comparable papers  
- Reject (1.5-3.5): DM-Codec (3.00) - DeCodec has more novelty
- Weak reject (3.5-5.5): USC (4.80), Codec-LM (5.00), Vec-Tok (5.20), RepCodec (5.50) - all have more severe novelty or evaluation issues
- Borderline accept (5.5-6.5): GenSE (6.00) - comparable quality
- Accept (6.5+): FlowDec (7.00) - more rigorous evaluation

Narrow bracket: [5.0, 6.5], with the most likely range [5.5, 6.0].

Let me write the final review.

---

Let me verify a few more things about the paper before finalizing. The key question is: does the paper address the bitrate issue at all? Let me check if there's any discussion.

Looking at the paper, the reconstruction section (Table 1 and surrounding text) doesn't mention the bitrate mismatch. The paper simply presents the numbers and claims superiority. So the critic is correct that this is unaddressed.

Also let me verify that the paper indeed calls the SDR drop "slight." Looking at line 252: "On the basis of Ablation-3, DeCodec further introduces SG, resulting in a slight decrease in SDR but a significant reduction in WER*." - confirmed.

And the "complete decoupling" phrase - line 106: "thereby promoting a complete decoupling between speech and background sound representations." - confirmed.

Now let me compile the final review.## Summary

This paper proposes DeCodec, a neural audio codec that learns to disentangle representations into orthogonal subspaces for speech and background sound, and within speech further decomposes semantic from paralinguistic content. The key technical innovations are a Subspace Orthogonal Projection (SOP) module that factorizes embeddings into orthogonal subspaces, a Representation Swap Training (RST) procedure that enforces speech/background-sound separation via cross-mixture reconstruction, and semantic guidance (SG) for hierarchical quantization. The paper demonstrates that a single DeCodec model can serve multiple roles — reconstruction, speech enhancement, one-shot voice conversion, and (per references to appendices) downstream ASR and TTS.

## Strengths

- **Novel problem formulation with a genuine gap.** Rethinking neural audio codecs as *disentangled representation learners* rather than pure compression tools is well-motivated and non-obvious. The paper identifies and addresses a real limitation: existing codecs (EnCodec, DAC) encode everything jointly, while speech-specific codecs (SpeechTokenizer) handle only clean speech. Hierarchical disentanglement of speech/background and semantic/paralinguistic within a single codec is a novel contribution.

- **Creative and technically grounded design.** The three-component architecture (SOP → orthogonal subspaces, RST → content assignment via swap training, SG → semantic/paralinguistic decomposition) maps cleanly to the stated problem. The RST procedure (Section 3.6) — training the decoder to reconstruct s₁+n₂ from S₁+N₂ — is a genuinely novel training scheme that forces speech and background-sound quantizers to encode their respective sources, not an incremental modification of existing methods.

- **Broad empirical scope.** A single DeCodec model is shown to perform reconstruction (Table 1), speech enhancement with competitive DNSMOS scores (Table 2), and one-shot voice conversion with denoising (Table 3). This breadth — and the references to ASR/TTS in appendices — demonstrates the practical value of disentangled representations serving multiple tasks from one codec, which is the paper's central thesis.

## Weaknesses

### Fatal
None.

### Major

- **The reconstruction comparison (Table 1) is confounded by bitrate.** DeCodec operates at 4.0+4.0 = 8.0 kbps, while baselines are at 2.0–6.0 kbps. Higher bitrate directly improves reconstruction quality, so the claimed "maintains advanced signal reconstruction" (abstract) is not cleanly supported. A bitrate-matched ablation — e.g., a DeCodec variant without disentanglement at the same total bitrate, or baseline codecs scaled to 8 kbps — is needed to distinguish the effect of the disentanglement mechanism from the extra 2–6 kbps of bandwidth. Without this, the reconstruction experiment does not establish whether the disentanglement machinery helps or hurts signal fidelity relative to a comparable baseline.

### Minor

- **The ablation reveals a real SG trade-off that the paper minimizes.** Comparing Ablation-3 (SOP+RST, causal) with DeCodec-c (SOP+RST+SG, causal) in Table 4: SDR-O drops from 6.68→4.62 (−31%), and SDR-B goes from +0.49→−1.11 (positive to negative). The paper calls this a "slight decrease," which understates a non-trivial degradation. While SG significantly improves WER* (41.9→25.8), the cost to decoupling quality should be acknowledged and discussed more honestly. The paper needs to explain why SG specifically hurts background-sound representation (SDR-B turning negative) and whether this trade-off is inherent or an artifact of the implementation.

- **The theoretical justification for RST (Section 3.6) does not constitute a valid proof.** The argument applies the mean value theorem for vector functions to claim that because the LHS of Eq. (16) depends on Zs₁ through ξ while the RHS is independent of Zs₁, Zs₁ must be independent of background sound. However: (a) the mean value theorem for vector-valued functions does not guarantee the single-point equality assumed at the level claimed; and (b) even under that form, the Jacobian's dependence on Zs₁ through ξ means the conclusion does not logically follow — the network could compensate through the Jacobian. The RST procedure remains a sensible and empirically supported training heuristic (the ablation data supports this), but the paper overclaims by presenting it as a formal theoretical guarantee.

- **Decoupling quality is modest relative to the paper's framing.** The best causal SDR-B (background decoupling) is 0.49 dB (Ablation-3) — barely above the 0 dB threshold where signal power equals distortion power. While DeCodec is not a dedicated separation system, the paper's language ("explicit decoupling," "complete decoupling" in the SOP section, *promoting a complete decoupling* on line 106) overstates what the numbers support. The framing should be calibrated to the measured disentanglement strength.

- **Several experimental details are missing.** (i) The total composite training loss is never stated — only L_⊥, L_RST, and L_SG are given, with no mention of whether standard codec losses (reconstruction L1/L2, adversarial losses from the DAC backbone) are used, nor their relative weights. (ii) The number of RVQ layers (K_s, K_n) and codebook sizes are not reported, preventing bitrate verification. (iii) The "blank audio" used for speech enhancement (Section 4.2.2, replacing BRVQ with "blank audio's BRVQ") is not defined — is it zero-valued samples, a silent recording of the same length, or something else? These gaps hinder reproducibility.

### Trivial
None.

## Nice-to-Haves

- **Direct representation analysis** (probing/visualization) would strengthen the decoupling claims beyond the SDR metric, which conflates reconstruction fidelity with separation quality. For example, linear probes to verify that Zs carries no background-sound-type information and Zn carries no speech-content information.
- **Bitrate-controlled reconstruction ablation** comparing DeCodec to a variant where SOP is removed and a single RVQ at 8 kbps encodes everything, isolating the cost/benefit of the disentanglement mechanism.
- **Comparison to a cascaded pipeline** (e.g., Conv-TasNet separation → EnCodec coding) for SE and reconstruction, which the introduction motivates against but never directly benchmarks.
- **SNR-dependent performance breakdown** to show whether decoupling quality degrades gracefully across the wide -5 to 40 dB SNR range used in training.

## Removed Points

These points were raised in the input review but are removed after verification:

- *"Mel distance shows DeCodec is not SOTA"* — The paper already acknowledges this, stating "the proposed algorithm does not show a significant advantage in clean speech" (line 202 area). Not a hidden weakness.
- *"SNR range is very wide (45 dB span)"* — A speculative concern about whether the model handles the range uniformly, without evidence that it causes a problem. Removed per the rule against speculative criticism without paper evidence.
- *"WER* column needs clarification"* — The paper clearly states it as "the WER of the downstream ASR model." Sufficiently clear.
- *"Inference cost not discussed"* — Valid but minor; the paper's contribution is methodological, not systems-oriented.
- *"No comparison to simple cascade for SE/reconstruction"* — Partially addressed via StoRM-SpeechTokenizer for VC. A nice-to-have, not a missing essential baseline.
- *One-shot VC producing 50% WER being called "effective"* — The paper acknowledges the voicing mismatch limitation (line 237 area). The framing is somewhat strong but the caveat is present.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add a bitrate-controlled reconstruction experiment.** Compare DeCodec to a "DeCodec-ablated" variant at the same total bitrate (8 kbps single RVQ without SOP). This isolates whether the disentanglement mechanism helps or hurts reconstruction fidelity, and directly addresses the most significant weakness.
2. **Add direct representation analysis.** Linear probing and/or t-SNE/UMAP visualization of Zs vs. Zn would decouple the evaluation from downstream task performance and provide clean evidence of disentanglement.
3. **Report the complete training objective** — all loss terms (reconstruction, adversarial, disentanglement) with their weights — and the codebook configuration (K_s, K_n, codebook size per layer).
4. **Discuss the SG trade-off openly.** The SDR-O drop of 31% and SDR-B turning negative when SG is added is a real finding that should be analyzed, not described as "slight." Consider ablating SG with different strengths.
5. **Define "blank audio" explicitly** for the SE procedure and report SDR-B/SDR-S broken down by input SNR to characterize the operating range of the decoupling.

## Score and Decision

**Calibration anchors (all rounds):**

| Paper | Path | Avg Score | Round | Itemized | Comparison |
|-------|------|-----------|-------|----------|------------|
| DM-Codec | /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/UFwefiypla.md | 3.00 | R1 | Yes | Less novel (incremental over SpeechTokenizer), more severe reproducibility flaws |
| USC | /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Id2JMVSQHZ.md | 4.80 | R1, R2 | Yes | Less novel (disentanglement already proposed), no clear quantitative advantage |
| Codec-LM Co-design | /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/KCVv3tICvp.md | 5.00 | R1, R2 | Yes | Engineering tricks without theoretical advancement; DeCodec has stronger novelty |
| Vec-Tok Speech | /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/C53xlgEqVh.md | 5.20 | R2 | Yes | Similar breadth but less technical novelty (combination of existing techniques) |
| RepCodec | /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/LfDUzzQa3g.md | 5.50 | R2 | Yes | Simple VQ-VAE on SSL features; DeCodec has substantially more technical novelty |
| GenSE | /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/1p6xFLBU4J.md | 6.00 | R3 | Yes | Comparable quality; some reviewers questioned novelty but accepted |
| FlowDec | /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/uxDFlPGRLX.md | 7.00 | R1 | Yes | More rigorous evaluation and theoretical grounding; DeCodec less polished on these axes |

**Bracket and final placement:** Round 1 bracketing placed DeCodec between RepCodec (5.50) and GenSE (6.00). DeCodec has genuinely higher technical novelty than RepCodec (which was criticized as "simply replaces input with SSL representations"), but its evaluation rigor — particularly the bitrate-confounded reconstruction comparison and missing experimental details — is weaker than GenSE's. The narrowest plausible range is [5.0, 6.0].

Comparing favorability-rated items: DeCodec's strengths (13.35–15.81) are very high, comparable to GenSE's top strengths (12.88) and FlowDec's (15.57). However, DeCodec's lowest weakness (bitrate confound, favorability=0.85) is more severe than GenSE's lowest (−4.78 was about the novelty debate, but the average sentiment was 6.00). The paper has real technical novelty and broad validation, but the bitrate issue and overclaimed theoretical proof lower confidence in the specific claims as written. With revisions addressing the reconstruction comparison and missing details, this could become a clear accept.

**Final calibrated score: 5.5** — a genuinely novel contribution with creative technical design and broad empirical scope, but held back by a confounded reconstruction comparison, overclaimed theoretical justification, and missing reproducibility details that prevent the evaluation from being convincing in its current form.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>