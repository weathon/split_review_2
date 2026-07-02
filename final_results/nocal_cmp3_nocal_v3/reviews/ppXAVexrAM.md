## Summary

ARSS proposes the first decoder-only autoregressive (AR) transformer for novel view synthesis (NVS) from a single image with camera control. The method uses a video tokenizer for temporally consistent visual tokens, a camera autoencoder that encodes Plücker raymaps into 3D positional guidance tokens, and a hybrid permutation strategy that randomly shuffles spatial token order while preserving temporal causality. Experiments on RealEstate10K, ACID, and zero-shot DL3DV show competitive results against diffusion-based and transformer-based baselines.

## Strengths

**1. Novel framing of NVS as causal next-token prediction with camera control.** The paper is the first to apply a GPT-style decoder-only AR model to NVS with explicit camera trajectory conditioning. Prior AR visual generation work focused on single-image generation without camera control, and prior NVS work has been dominated by diffusion models that generate views jointly. This reframing is well-motivated by the goal of causal world modeling where views must be processed sequentially.

**2. Well-designed camera autoencoder for 3D positional guidance.** Encoding Plücker raymaps into latent tokens with explicit geometric losses (ray direction reconstruction, orthogonality regularization) is a clean way to inject 3D awareness into an AR token sequence. Interleaving camera tokens with visual tokens as "positional instruction tokens" is a natural fit for the shuffled-token AR paradigm.

**3. Hybrid permutation strategy is convincingly ablated.** The ablation in Table 2 and Figure 7 shows that spatial-only permutation (preserving temporal order) substantially outperforms both raster-scan order (PSNR 16.29) and full spatiotemporal permutation (PSNR 18.76), achieving PSNR 19.22. This validates the core architectural insight that spatial context should be bidirectional while temporal causality must be preserved.

## Weaknesses

### Fatal
None.

### Major

**1. Inflated claims inconsistent with evidence.** The abstract accurately says "achieves overall comparable to state-of-the-art view synthesis approaches" (line 9), but the introduction (line 88) and Discussion (line 281) say "outperforms state-of-the-art methods." Against SEVA (the strongest competitor), ARSS wins on PSNR (+1.1% on Re10K) and LPIPS (−21% on Re10K) but loses on SSIM (0.624 vs 0.670, a 7.4% relative deficit) and FID (47.60 vs 46.98 on Re10K; 47.76 vs 33.16 on ACID — a 44% FID gap). On ACID, the FVD scores are also similar (54.60 vs 53.69). The results show competitive but mixed performance, not clear superiority. The paper would be stronger by adopting the abstract's measured tone throughout.

**2. Camera autoencoder is not ablated.** The camera autoencoder is presented as a core contribution (Section 3.2.2), but there is no experiment removing it or replacing it with a simpler conditioning mechanism (e.g., directly feeding Plücker coordinates or sinusoidal camera embeddings). Without this ablation, it is impossible to assess how much the autoencoder's complex design and pretraining contribute vs. simpler alternatives. This is the most direct way to validate a central design choice.

**3. Error accumulation analysis excludes the strongest competitor.** The per-frame analysis in Figure 6 claims "better long-horizon behavior than all baselines," but SEVA — the strongest diffusion-based method — is not included. Since SEVA generates all views jointly (not autoregressively), it would not accumulate error over frames; this is precisely the structural trade-off the paper argues about. Including SEVA would either validate the AR approach (if ARSS matches SEVA's flat error profile) or reveal a genuine limitation. Its absence is a significant evidential gap.

### Minor

**1. Zero-shot comparison on DL3DV is incomplete.** SEVA is excluded from the DL3DV evaluation (Table 1) with the note that "DL3DV was part of its training data" (line 196). The paper is transparent about this, but the consequence is that the zero-shot evaluation compares ARSS only against weaker baselines (MotionCtrl, Genwarp, LVSM), not against the strongest diffusion competitor. This limits what the zero-shot results can demonstrate about generalization relative to diffusion approaches.

**2. VidTok tokenizer training status unspecified.** The paper states "We apply VidTok... as our video tokenizer" (line 210) but never clarifies whether it is frozen or fine-tuned during ARSS training. This affects reproducibility and interpretation of the ablation in Table 3 (video tokenizer vs. VQ image tokenizer), since the comparison may conflate architectural differences with differences in pretraining data scale.

**3. Notation issues in Eq. 5 and Eq. 7.** In Eq. 5 (line 151–153), the variable "d" is used for both the normalized ray direction and the momentum term (which should be "m"), and the ray origin "o" in "m = o × d" is not defined. In Eq. 7 (line 171), the cross-entropy loss is written with a single argument — the targets are missing from the notation, unlike Eq. 3 which shows both arguments.

**4. Parallel decoding claim is unsupported.** The paper mentions that shuffled tokens "allows parallel decoding" and the model "has the capacity to predict multiple tokens at one time" (line 177), citing prior work. However, no experiments or latency measurements are provided to demonstrate this capability in ARSS. If parallel decoding is implemented, results should be reported; if speculative, it should be identified as such.

**5. Tokenizer ablation conflates two differences.** Table 3 compares VidTok (video tokenizer, FSQ) against a VQ image tokenizer, but the comparison varies both the tokenization type (video vs. image) and the quantization method (FSQ vs. VQ) simultaneously. It is unclear how much of the 62% FVD improvement comes from temporal modeling vs. the FSQ regularization.

**6. No inference speed or latency reported.** The model generates 4096 tokens sequentially (1024 per frame × 4 target frames). For a method motivated partly by its potential for causal/online world modeling, the absence of runtime measurements is a practical omission.

### Trivial
None.

## Nice-to-Haves
- An ablation replacing the camera autoencoder with a simpler conditioning (e.g., direct Plücker coordinate embeddings or sinusoidal camera pose encodings) to validate the autoencoder's contribution.
- Per-frame error accumulation metrics comparing ARSS against SEVA to directly address the causal vs. joint generation trade-off.
- Reporting GPU-hour comparisons between ARSS and the baselines for a fairer resource-based discussion.
- Inference latency measurements for the sequential AR decoding process.

## Removed Points
These points are flagged to be removed, treat them with caution:
- Abstract grammar issue ("achieves overall comparable"): removed per rule against grammar/style nitpicks.
- "perpetual loss" typo in line 149: removed per rule against typo nitpicks.
- Criticism about the third motivation not being specific to NVS (lines 75–78): the paper explicitly cites prior work and frames it as an extension; this is a correct characterization, not a weakness.
- Claim that Section 3.1's causal video tokenization is unclear: the description ("first frame independent and not compressed along temporal dimension") is substantively clear for the level of detail appropriate to the main paper; the masking mechanism is a reasonable implementation detail.
- Request for SEVA's resource comparison without numbers: the paper mentions this qualitatively; the criticism is valid but speculative in nature and belongs under Nice-to-Haves.

## Novel Insights
The reviews collectively surface a key observation: ARSS introduces a genuinely novel approach to NVS (decoder-only AR with camera-conditioned token sequences), but the evidence presentation creates a mismatch between the contribution's real value and the paper's claims. The strongest evidence for the approach — the hybrid permutation ablation and competitive PSNR/LPIPS results — coexists with the weakest evidence — the unablated camera autoencoder and the missing SEVA comparison in key analyses. The paper's genuine contribution is demonstrating that AR models can perform NVS at all at a competitive level, not that they outperform diffusion. This reframing would make the paper internally consistent and more fairly represent its scientific value.

## Suggestions
1. Calibrate claims throughout: replace "outperforms" with "achieves competitive results" or "is the first AR approach to NVS, achieving results comparable to diffusion-based methods."
2. Add an ablation study removing the camera autoencoder (or replacing it with a simpler conditioning) to validate its contribution.
3. Include SEVA in the error accumulation analysis, even as a separate figure or table, to directly address the causal vs. joint generation trade-off.
4. Clarify whether VidTok is frozen or fine-tuned during ARSS training.
5. Fix the notation issues in Eq. 5 (distinguish d and m, define o) and Eq. 7 (include the target argument in CE).
6. Either provide parallel decoding results or retract the claim about this capability.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>