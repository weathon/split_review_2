Now let me produce the final consolidated review.

---

## Summary

This paper bridges classic Gray-Wyner information theory with learnable multi-task compression. It extends Wyner's and Gács-Körner common information to the lossy setting (Theorem 1), derives a Lagrangian objective from the Gray-Wyner formulation (Theorem 2, Eq. 12), and proposes a three-channel neural codec with a matching-based mechanism to separate common from task-private information. Experiments on synthetic data, colored MNIST, Cityscapes, and COCO validate that the method explores the transmit-receive rate tradeoff and outperforms independent coding baselines.

## Strengths

- **Strong theoretical contribution.** Theorems 1 and 2 extend Gray-Wyner theory to lossy, learnable compression, clearly articulating the transmit-receive tradeoff and the connection between Wyner's/Gács-Körner common information and operational rate bounds. The derivation from information-theoretic first principles is coherent and non-trivial.

- **Well-designed edge-case experiments.** The colored MNIST experiments (Dependent, Independent, and Mixture PMFs) directly test whether the method responds to the information structure of the data. The Dependent PMF yields the lowest transmit rate and the Independent PMF the lowest receive rate, providing genuine evidence that the method correctly adapts to the data's common information structure.

- **Clear, precise exposition of preliminaries.** Sections 2.1 and 3.1 present the Gray-Wyner region, Wyner's common information, and Gács-Körner common information with proper definitions and Markov conditions. The theory is communicated without hand-waving.

## Weaknesses

### Fatal
None.

### Major
- **Motivation-evaluation disconnect.** The paper motivates with a distributed inference scenario (lines 15–17: a camera transmits to one device for object detection, then later a different device needs semantic segmentation for the same input, requiring only the *additional* information to be transmitted). However, all experiments use co-located joint training with both decoders trained simultaneously. The receive rate is computed as a sum (2R₀+R₁+R₂) rather than tested in an actual distributed setting. No experiment freezes one decoder and trains the other from scratch using only its allocated channels, nor verifies that the common representation is usable by an independently trained downstream decoder. This creates a gap between the motivating scenario and the evidence provided. The paper's practical claims about distributed inference (Abstract, lines 15–17, line 277) are not directly supported by the experiments as designed.

- **Core architectural mechanism is not empirically validated.** The element-wise matching rule (Eq. 14), where common channel elements are kept only if Y₀⁽¹⁾ and Y₀⁽²⁾ exactly match after quantization, is the central mechanism for isolating common information, yet the paper provides no diagnostic evidence about it. Specifically absent: what fraction of Y₀ elements remain non-zero after training, what semantic information the common channel captures, whether the matched content is genuinely task-relevant common information versus low-level features easiest to align. The auxiliary L2 loss (Eq. 15) encourages the two branches to produce similar representations, but does not guarantee the matched content corresponds to task-relevant common information. The paper honestly notes that "it is often difficult to discard the information in the common channel from the private channels" (line 183), but provides no analysis of how much redundancy remains. The method works based on the rate-distortion results, but *how* the internal mechanism achieves separation is a black box.

### Minor
- **Headline quantitative claim not transparently supported.** The conclusion states "a BD-rate advantage of -81.58% in transmit rate, against single-task codecs" (line 275), but this number is not derivable from the main-text results alone. Section 4.3 describes two task-pair experiments (Cityscapes, COCO), yet the conclusion references "three computer vision experiments" — the third is not described in the main text. The calculation methodology for this aggregate figure is not shown, making the claim unverifiable from what the main text provides.

- **Single-source simplification.** All experiments use a single source (X₁ = X₂ = X, line 191), which simplifies the general Gray-Wyner setting where X₁ and X₂ are different sources. This removes the cross-source learning problem, which is the harder case of the general framework.

- **No variance or statistical significance reported.** Results are reported without variance across multiple training runs. Given the training complexity, this would strengthen the reliability of the reported numbers.

- **Scalability limitation constrains scope.** The number of channels scales exponentially (2^N - 1 for N tasks, acknowledged in line 279), which limits practical applicability beyond two tasks. While honestly acknowledged, this bounds the contribution's scope.

### Trivial
- The paper describes β as the "only" hyper-parameter (line 181), but λ₁ and λ₂ (rate-distortion tradeoff coefficients in Eq. 12) are also hyperparameters that are swept across operating points.

## Nice-to-Haves
- Provide empirical diagnostics of the common channel: matching rates between the two branches, semantic analysis of what Y₀ captures (e.g., train a classifier on Y₀ alone), and the extent of residual redundancy between common and private channels.
- Test the actual distributed scenario: freeze one decoder and train the other from scratch using only its allocated channels, measuring the performance penalty relative to joint training.
- Clarify the -81.58% BD-rate calculation by showing per-experiment breakdowns in the main text.
- Report variance across at least 3 training seeds for key results.

## Removed Points
These points from the input review were removed after verification against the paper:
- **"Method fails when common information is non-trivial"** (Mixture PMF): Removed — the paper states (line 235) that the method "still performs better, in terms of transmit rate, than the Independent approach." It underperforms relative to the edge-case PMFs but does not fail.
- **"Theoretical guarantees without Markov conditions"**: Removed — the paper's statement (line 167) that the architecture "removes the requirement for the conditions in 1" is a design observation about the architecture, not a claim about theoretical theorems. Correct as written.
- **"Why not a simpler architecture"**: Removed — the paper provides ablation studies (Separated, Combined, Joint, Independent) that directly address alternative designs, and Shared outperforms them.
- **"Auxiliary loss does the real work, not the architecture"**: Removed — this is speculation without evidence that the architecture is inert. The full method outperforms alternatives.
- **"Should compute interaction information for synthetic data"**: Removed — this is a nice-to-have, not a weakness.
- **"No discussion of computational cost"**: Removed — the encoder uses two parallel analysis transforms, which is standard for methods in this line of work; not a core weakness.

## Novel Insights
Beyond the paper's own contributions, the review process surfaces the following: the matching-based common channel mechanism (Eq. 14) is surprisingly brittle on paper yet appears to work in practice — this tension between architectural fragility and empirical success would benefit from diagnostic investigation. Additionally, the paper's theoretical framing (transmit vs. receive rate tradeoff) is genuinely novel for multi-task learned compression, but the experimental validation is strongest for rate-distortion behavior (what the theory predicts) and weakest for actual common-information separation (what the architecture claims to do). This asymmetry suggests that future work in this line should prioritize diagnostic experiments bridging theoretical guarantees and learned mechanism behavior.

## Suggestions
- Add empirical diagnostics of the common channel: matching rates, semantic content analysis, and tests of whether Y₀ alone suffices for each task.
- Test the distributed scenario: freeze one decoder post-training and verify the other can be trained from scratch using only its allocated channels.
- Provide per-experiment breakdown for the -81.58% BD-rate figure in the main text.
- Report variance across multiple training seeds.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>