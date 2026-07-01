## Summary

The paper proposes augmenting the AIDE fake-image detector with structural features derived from a hierarchical cuboidal partitioning algorithm. The image is recursively split by maximizing SSE reduction, and a cumulative gain vector is used as a structural fingerprint. When concatenated with AIDE's existing patchwise and semantic embeddings, the method achieves new SOTA mean accuracy (89.56%) on the GenImage benchmark and competitive second-best results on AIGCDetect and Chameleon. The work is presented as the first application of hierarchical structural analysis to AIGC detection.

## Strengths

- **Novel feature perspective for AIGC detection.** Applying cuboidal partitioning (an established structural analysis technique) to this task is a sensible and underexplored direction. The idea that generative models leave detectable traces in hierarchical image organization is well-motivated.
- **Clean and replicable integration.** The structural features are computed via a deterministic algorithm, compressed with a small trainable head, and concatenated to a frozen AIDE backbone. This plug-and-play design makes the method easy to reproduce and build upon.
- **Consistent improvement on GenImage.** The method beats the AIDE baseline on 7 out of 8 GenImage sub-benchmarks, with the largest gains on ADM (+3.0%), GLIDE (+3.4%), VQDM (+4.8%), and BigGAN (+6.8%). This demonstrates genuine complementarity for modern diffusion models.

## Weaknesses

### Major

1. **State-of-the-art claim is only partially supported.** The method is SOTA on GenImage but ranks second on AIGCDetect (91.85% vs AIDE's 93.02%) and second on Chameleon (both training scenarios). The paper's title and abstract emphasize "superior performance" and "state-of-the-art" without qualifying that the lead is limited to one benchmark. This overclaims weakens the core contribution.

2. **Performance degradation on many AIGCDetect subsets.** On 12 of the 18 AIGCDetect generators, the proposed method underperforms the AIDE baseline (sometimes by several points, e.g., BigGAN: −3.97%, Midjourney: −1.28%). The paper acknowledges this vaguely ("performance slightly decreased on certain subsets") but provides no analysis of when structural features help or hurt. The net gain on AIGCDetect is negative relative to AIDE, calling into question the universal value of these features.

3. **Lack of ablation studies.** The paper fixes N=1024, compresses to M=256, and freezes the AIDE encoders, but never justifies these choices. Without ablations on the number of partitions, the compression dimension, whether to jointly fine-tune AIDE, or how the structural features behave with different backbones, it is impossible to assess the robustness or optimality of the design.

### Minor

- **"Structural semantic" is a misnomer.** The features are computed from RGB pixel SSE—a low-level statistical measure, not semantic information. The title overstates what the features capture.
- **Claim of "first application of hierarchical structural analysis for AIGC detection" is too strong.** Prior work uses structural cues (e.g., facial landmarks, segmentation masks, perceptual hashing) for deepfake detection; the paper should position itself more carefully.
- **Qualitative results are cherry-picked.** Figure 3 shows 13 examples where AIDE fails and the proposed method succeeds. This is not informative about average behavior; a distribution of confidence shifts or error analysis would be more meaningful.
- **A key reference is a workshop paper (Haque et al. 2025).** While not disqualifying, it weakens the grounding of the structural method.

## Nice-to-Haves

- Experiment with training the AIDE encoders jointly instead of freezing them, to see if further gains are possible.
- Analyze the 1024 cumulative gain values: do they contain frequency or spatial patterns that correlate with generative model families?
- Apply the structural feature extractor to a different baseline (e.g., PatchCraft) to test transferability of the idea.

## Novel Insights

None beyond the paper's own contributions. The idea that recursive partitioning statistics can serve as a forensic feature is reasonably novel, but the insight remains shallow—the paper does not explain *why* generative models produce abnormal hierarchical structure or what specific artifacts the cumulative gain captures.

## Suggestions

- Tone down the "state-of-the-art" claim to reflect that the method is SOTA on GenImage but not universally across benchmarks.
- Add an ablation study varying N (e.g., 128, 256, 512, 1024) and M to validate hyperparameter choices.
- Include a per-dataset analysis of when structural features degrade performance (e.g., what do the generators where performance drops have in common?).
- Report average confidence shift and error bars for the qualitative comparison to make it less anecdotal.

## Score and Decision

The paper proposes a reasonable and novel feature perspective, and it achieves a clear improvement on one major benchmark. However, the core claim of "superior performance" is not consistently supported: the method underperforms its baseline on a second large benchmark and is second-best on the third. The lack of ablation studies and the absence of analysis for the performance degradation weaken the contribution. The improvement is incremental over an existing strong detector. At ICLR, the bar requires stronger evidence of robustness and deeper insight. Therefore, the paper is below the acceptance threshold.

MY FINAL SCORE: <score>4.0</score>  
MY FINAL DECISION: <decision>Reject</decision>