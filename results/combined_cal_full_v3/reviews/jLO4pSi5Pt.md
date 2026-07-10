Now I have all the calibration data I need. Let me produce the final consolidated review.

## Summary

This paper identifies and formulates the problem of long-tailed test-time adaptation (TTA) for Vision-Language Models (VLMs). It proposes L-TTA, containing three co-designed components: Synergistic Prototypes (SyPs) combining deterministic and exclusionary prototypes to enrich tail-class representations, Rebalancing Shortcuts (RSs) for learnable adaptation with a class re-allocation loss, and Balanced Entropy Minimization (BEM) to counteract head-class bias in standard entropy minimization. The method is evaluated across 15 datasets, 4 backbone architectures, 3 imbalance ratios, and against 11 baselines, demonstrating consistent improvements in accuracy and macro-F1.

## Strengths

1. **Novel problem identification with VLM-specific analysis.** The paper is the first to explicitly formulate and target the long-tailed TTA problem for VLMs, identifying two specific failure modes — Text-induced Tail Erosion and Modality-bias Amplification (Section 1, Figure 1) — that are grounded in VLM architectural properties (text-prior bias and modality mismatch). This goes beyond applying generic long-tailed techniques to TTA.

2. **Comprehensive and well-controlled evaluation.** Across 15 datasets (OOD, Cross-Domain, Corruption benchmarks), three imbalance ratios (10, 20, 50), four backbone architectures (ViT-B/16, ViT-L/14, ViT-H/14, SigLIP-L/16, MetaCLIP-BigG), and 11 baselines with 5 runs per experiment, L-TTA consistently outperforms prior methods on both accuracy and macro-F1 (Tables 1–3, 5). This is more thorough than typical for the TTA literature.

3. **Genuinely strong efficiency.** Table 4 shows L-TTA achieves the highest harmonic mean of accuracy and macro-F1 while being faster (1.45h) than many competing methods (RLCF: 18.3h, WATT: 27.7h) and memory-competitive (1.89GB). This is a practical advantage, not the usual "strong but expensive" trade-off.

4. **Component-level ablation confirms each design choice.** Table 6 demonstrates that each component (DPs, EPs, RSs, BEM) individually contributes, and the full combination is best. The ablation covers both ResNet-50 and ViT-B/16 backbones, and the sensitivity analyses (Figure 4) for hyperparameters λ₁, λ₂, η, K, β provide useful guidance.

## Weaknesses

### Major

1. **Evaluation is entirely on simulated long-tailed data, not real long-tailed distributions.** The paper creates long-tailed test sets by "random sampling to manipulate the cardinality distribution into an exponentially decayed curve" from originally balanced datasets (Section 4). Real long-tailed data (e.g., iNaturalist, Places-LT) has different properties: tail classes may be visually similar to head classes, have higher intra-class variance, or exhibit semantic hierarchies that interact with cardinality in ways that random subsampling does not replicate. When tail classes are created by simply removing 90% of samples from a balanced set, the remaining 10% are still as canonical as the head-class samples — just fewer. The paper frames the problem in terms of "real-world test sets" (Abstract, Introduction) but provides no experiment on a naturally long-tailed benchmark. This weakens the paper's central ecological validity claim. **Severity: major** — the empirical conclusions may hold, but the evidence for real-world applicability is indirect.

2. **Propositions 1 and 2 are stated with insufficient specificity to be evaluable in the main text.** Both propositions say classes are split into head/tail "with certain measurements" without specifying what measurement or threshold is used. Proposition 1's claimed gradient sign inequality depends entirely on this unspecified criterion. The proofs are in the appendix, but the main-text formulation is too vague for readers to assess what is actually being claimed. Proposition 2 inherits the same issue and adds the BEM formulation with the undefined ℙ̃ (next point). These read as post-hoc justifications rather than theoretically grounded design choices. The paper would be stronger if it acknowledged the heuristic nature of BEM and relied on the clear empirical evidence rather than claiming theoretical guarantees that cannot be evaluated from the main text.

### Minor

3. **Balanced Entropy Minimization has an undefined term.** Equation 9 defines ℒ_BEM = ℍ'(ℙ̃) = -σ(z')log(σ(z')), z' = z - (1 - ℙ̃)^β log(π/Σπ_i). The variable ℙ̃ is used in the formulation but never explicitly defined — it can be inferred as the original softmax prediction σ(z), but the paper does not state this. Since ℙ̃ appears both as the argument to the entropy function ℍ' and inside the penalty factor (1 - ℙ̃)^β, this ambiguity makes the formulation unreproducible as written. Fixable with one clarifying sentence.

4. **No limitations section.** The paper ends with a brief conclusion and does not discuss its limitations. Given that the evaluation is entirely on simulated long-tailed data, the method introduces several hyperparameters (λ₁, λ₂, β, η, K) whose sensitivity is only partially explored (Figure 4), and the method assumes the class list is known in advance (text embeddings are pre-computed for all classes), a limitations paragraph is warranted for completeness.

5. **Hyperparameter K description is ambiguous.** The method (Section 3.2) describes K as the "number of hyper-class vectors," but the implementation (Section 4) sets K = 0.3, and the ablation (Figure 4c) sweeps K from 0.1 to 1.0. These fractional values suggest K is a fraction of something (number of classes? embedding dimension?), but this is never specified. The mismatch between "number of vectors" (an integer concept) and the fractional values used is confusing and should be clarified.

### Trivial

None.

## Nice-to-Haves

- **Add one naturally long-tailed benchmark** (e.g., iNaturalist, Places-LT) to directly support claims about real-world applicability and close the gap between the "real-world test sets" framing and the entirely simulated experiments.
- **Replace the underspecified Propositions 1/2** with an empirical gradient analysis comparing EM vs. BEM head/tail gradients across the actual datasets used in the paper. This would be more informative and more honest about what is known.
- **Include a direct measurement of the two identified failure modes** — show that standard TTA methods cause text embeddings of tail classes to drift away from their visual features (Text-induced Tail Erosion) or that unimodal adaptation widens the modality gap (Modality-bias Amplification). An analysis experiment visualizing these phenomena would tighten the link between motivation and design.

## Removed Points

These points were raised in the input review but removed after cross-checking against the paper:

- **EP mechanism conceptual confusion** (critic claimed EP motivation does not match implementation): The critic argued that storing the current image's feature into every class prototype weighted by unlikelihood is not "storing improbable features." But this description is equivalent to what the paper claims — for class c, features weighted by how unlikely they are to belong to class c are accumulated in the EP for class c. The mechanism is coherent with its stated goal. Removed because the criticism misreads the paper's mechanism.
- **Table 7 misalignment** (four accuracy values for three epsilon columns): Likely a parser artifact from PDF extraction. Removed per formatting-artifact rule.
- **"First attempt" claim overstatement**: The paper explicitly frames its contribution as being about VLMs and cross-modal challenges (Section 2.1), distinguishing itself from prior non-i.i.d. TTA work which addresses class bias in unimodal settings. The claim is reasonable within this scoped framing.
- **Corruption benchmark only uses gaussian noise in main results**: The paper explicitly states that results on 16 other corruption types are in Appendix J (Section 4). This is a presentation choice, not a weakness.
- **RS optimization details**: The paper specifies the overall optimizer (AdamW) and the combined loss (Eq. 11). The critic's demand for per-component optimization specifics exceeds what is standard for TTA papers.

## Novel Insights

Beyond the paper's own contributions, the most novel observation emerging from a combined reading of the paper and the reviews is that the three-component design (SyPs, RSs, BEM) directly maps to the two identified VLM-specific failure modes — this is stronger than the paper itself argues. The paper identifies Text-induced Tail Erosion and Modality-bias Amplification as failure modes, but never directly measures them in experiments. Confirming these failure modes empirically (e.g., tracking text embedding drift for tail classes, or measuring modality gap widening under standard EM) would not only validate the problem framing but also provide diagnostic tools for future long-tailed TTA work. The paper's contribution would be strengthened by verifying the causal chain: failure mode → design → measured mitigation.

## Suggestions

1. Add at least one naturally long-tailed benchmark (e.g., iNaturalist) to experiments.
2. Clarify the definition of ℙ̃ in Equation 9.
3. Specify what quantity K is a fraction of, or rename it to avoid confusion.
4. Replace or supplement Propositions 1/2 with an empirical gradient analysis.
5. Add a limitations section discussing the simulated-data limitation, the known-class-list assumption, and hyperparameter sensitivity.

## Score and Decision

**Calibration analysis:**

All rounds retrieved the following anchors for this topic area:

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| Concept Drift | b20VK2GnSs | 7.00 | R1, R2 | Yes | Similar scope (long-tailed VLMs); its weakness (-1.93 favorability) was more severe than our paper's worst (-0.15); strengths comparable. |
| DOTA | yD2JMeKumt | 6.00 | R1, R2 | Yes | CLIP TTA paper; our strengths (7.96–10.80 favorability) exceed DOTA's (7.79–9.44); our weakness (-0.15) much less severe than DOTA's worst (-2.33, 1.80). |
| L2C Frozen CLIP | TD3SGJfBC7 | 6.25 | R2 | Yes | Few-shot TTA for CLIP; our strengths higher on average; our weakness (-0.15) less severe than L2C's novelty weakness (-2.83). |
| Reliability Bias | TPZRq4FALB | 8.00 | R1 | Yes | Multi-modal TTA paper with top strengths (10.27–13.27 favorability); clearly a level above our paper in analytical depth and benchmark contribution. |
| Reject anchors | 5lUdTogEL3, gwZ90hFSL2 | 1.00 | R1 | No | Not remotely comparable — irrelevant topics. |

**Round 1 bracket:** 5.5–7.5 (based on concept-drift paper at 7.00 and DOTA at 6.00 as the closest topical anchors).

**Round 2 narrowing:** Comparing rated items: Our paper shares with the 7.00 Concept Drift anchor the property of having well-above-zero favorability for all strengths and a single meaningful weakness. However, our weakness (-0.15) is substantially milder than the concept drift paper's setup flaw (-1.93). Our efficiency strength (10.80 favorability) is notably high. Compared to the 6.00 DOTA paper, our strengths are uniformly higher and our weakness less severe. The gap to the 8.00 Reliability Bias paper is clear — that paper had strengths at 10.27, 13.27 favorability with deeper analytical contributions.

**Final placement:** The paper sits above 6.00 (DOTA range) and slightly below 7.00 (Concept Drift), at approximately **6.5**. This reflects a genuinely novel problem framing and strong empirical execution, tempered by the simulated-data limitation and minor presentation issues that prevent it from reaching the 7+ range.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>