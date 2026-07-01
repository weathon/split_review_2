Now let me write the final review.

**Calibration Bracket (Round 1):** Based on the retrieved anchors, the most comparable paper is "Mimetic Initialization Helps State Space Models Learn to Recall" (avg 4.50, Reject) which similarly studies whether SSM recall deficits are due to training difficulties vs capacity. The current paper is substantially stronger: it covers more architectures (Mamba, Hyena, Mamba2, DeltaNet), has a cleaner central finding (LR sensitivity as confound), and provides more thorough ablations. "On Limitation of Transformer for Learning HMMs" (avg 5.25, Reject) is also comparable as a synthetic-benchmark study of architectural limitations, but the current paper has more practical implications. "Small-scale proxies for large-scale Transformer training instabilities" (avg 8.00, Accept) is methodologically similar (LR sensitivity experiments) but more polished and complete. The current paper sits between these — stronger than 4.5–5.25 papers but less polished than the 8.0 papers. Narrowest plausible bracket: **5.5–6.5**.

## Summary

This paper systematically compares SSM and Transformer learning dynamics on multi-query associative recall (MQAR) and copying tasks, documenting that SSMs (Mamba, Hyena) have much narrower learning rate windows (~1 order of magnitude) than Transformers (~2 orders), and that this can confound comparative evaluations. It also reveals contrasting scaling behaviors (SSMs benefit from width, Transformers from depth) and identifies the 1D convolution as the key architectural component enabling single-layer SSM recall. The study encompasses over 3,000 runs and approximately 20,000 GPU hours.

## Strengths

1. **The central LR-sensitivity finding (Figures 1 and 5) is clean, well-documented, and practically impactful.** It shows that on MQAR, Attention maintains high accuracy across roughly 2 orders of magnitude of learning rates, while Mamba and Hyena attain high accuracy only within a narrow window (~1 order or less). The dashed vertical lines marking the learning rates used by Arora et al. (2023) make the confounding argument concrete and visual: prior work's grid simply missed the narrow SSM-compatible range. This finding recontextualizes a meaningful body of comparative work on SSMs vs. Transformers and is a direct, actionable insight for practitioners.

2. **The width-vs-depth scaling analysis (Figures 3, 4; Table 1) is well-executed and informative.** The paper shows that 1-layer SSMs can solve MQAR with sufficient width, while 1-layer Transformers cannot regardless of width (Figure 3). Figure 4 clarifies that the relevant variable is *how* parameters are allocated (width vs. depth), not total parameter count. Table 1 on the copy task reinforces this practically: a 12-layer, 1408-width Mamba achieves 100%, while a 24-layer, 1024-width Mamba with the same total parameters achieves only 16%.

3. **The ablation connecting convolution to single-layer performance (Table 2) is crisp and mechanistic.** Removing the 1D convolution from 1-layer Mamba drops accuracy from 99% to 2%. Adding a 1D convolution to the 1-layer Transformer raises its accuracy from 2% to 99%. This clean symmetry identifies convolution as the critical architectural component enabling single-layer recall.

4. **The DeltaNet result (Figure 7) adds forward-looking value.** DeltaNet maintains high accuracy across a wide LR range where Mamba and Mamba2 show sharp peaks. The paper offers a plausible mechanistic hypothesis (Householder-based updates avoid vanishing-gradient problems from A-matrix decay), grounding the discussion in a concrete architectural improvement.

## Weaknesses

### Major

None.

### Minor

1. **The central thesis on line 39 overreaches relative to the paper's own evidence.** The paper states: *"Transformers differ from SSMs not in terms of expressive power but mainly because of their optimization dynamics"* (line 39). However, the paper's own 1-layer results (Figure 3, Section 4) show that 1-layer Transformers cannot solve MQAR regardless of width (accuracy at chance level ~1/N_keys), while 1-layer SSMs can with sufficient width and proper tuning. This is an expressivity difference, not merely an optimization one — no amount of LR tuning enables the 1-layer Transformer. The paper acknowledges this indirectly (lines 144–145: "Attention exhibit a surprisingly different behavior: when constrained to a single layer, they fail to solve the task") and the abstract uses more nuanced language ("a crucial differentiator lies not just in their expressivity but in their fundamental learnability properties"). But the strong claim on line 39 remains internally inconsistent with the 1-layer evidence. The paper's actual evidence supports a more nuanced story: in the 2-layer setting, optimization is the primary differentiator; in the 1-layer setting, a genuine expressivity gap exists. This framing issue is fixable and does not undermine the paper's empirical contributions.

2. **The induction head interpretation (Section 6) is speculative and lacks mechanistic evidence.** The paper claims the loss bump in 1-layer Attention "resembles the formation of an induction head circuit" (line 188). The paper's own background (lines 71–73) correctly notes induction heads require a *two-layer* circuit. The paper uses hedged language ("resembles," "hypothesize," "attempts"), which is appropriate, but the claim remains thin. No attention pattern analysis, probing, or mechanistic evidence is provided to substantiate it. A loss bump alone could indicate generic optimization dynamics (e.g., escaping a saddle point, navigating a loss plateau). The conclusion (line 235) also presents this as "training dynamics resembling the induction head phenomenon" despite the thin evidence. Softening this to "a phase transition of unknown origin" or providing actual mechanistic evidence would strengthen the paper.

3. **No validation on language modeling tasks.** The paper acknowledges this limitation in the conclusion, but the gap between the paper's architectural claims and its evidence is notable. The findings are presented with implications for "state-of-the-art industry-size applications such as language modeling" yet come entirely from two synthetic token-prediction tasks (MQAR and copying). The paper claims these benchmarks are "highly correlated with language modeling performance" (abstract) without providing specific evidence for this correlation beyond citing prior work. At least a small-scale language modeling perplexity experiment (e.g., on WikiText-103 or OpenWebText) would increase confidence that the LR-sensitivity and scaling findings generalize beyond synthetic tasks.

### Trivial

4. **DeltaNet "Transformer-level robustness" claim slightly overstated.** At dim=64 in Figure 7, DeltaNet's accuracy drops from ~0.9 to ~0.5 at the highest learning rate, while Transformers maintain near-perfect accuracy across their full range in Figure 1.

## Nice-to-Haves

- A small-scale language modeling experiment (e.g., on WikiText-103) comparing Mamba and a Transformer at their respective optimal LRs would directly address the scope limitation.
- Testing intermediate width/depth allocations (not just extreme wide-shallow vs. narrow-deep) would make the scaling analysis more complete.
- Testing at least one additional optimizer (e.g., AdamW) would strengthen the claim that optimization sensitivity is architecture-specific rather than optimizer-specific.
- Replacing the induction-head speculation with actual attention-pattern analysis or removing it entirely.

## Removed Points

These points from the input review were removed with justification:
- **"Learning rate scheduling not reported"**: The paper's experimental details are in Appendix A.2, which was stripped by the parser. Per review policy, penalizing missing appendix content is not allowed.
- **"Training compute cost not reported"**: The paper does report "approximately 20,000 GPU hours" (line 23).
- **"Table 4 (positional encodings) in stripped appendix"**: Per review policy, penalizing appendix content stripped by the parser is not allowed.
- **"Only Mamba tested on the copy task"**: Moved to Minor weakness 3 (synthetic-only benchmarks), as this is a specific instance of the broader scope limitation.
- **Generic/vague criticisms** from the section-by-section notes that lacked specific anchoring to paper content.

## Novel Insights

The most interesting observation from the review is that the paper's own evidence contains a more nuanced story than its central thesis admits — and the paper actually presents that evidence transparently. The single-layer expressivity gap (1-layer Transformers cannot solve MQAR; 1-layer SSMs can with width and tuning) is clearly documented in Figure 3 and Section 4, yet the line-39 thesis claims the difference is "mainly" about optimization, not expressivity. The paper would be stronger if it leaned into this duality: the 2-layer setting is about optimization, the 1-layer setting reveals a genuine expressivity tradeoff. Additionally, the convolution ablation (Table 2) is under-discussed relative to its significance — it provides the sharpest mechanistic insight of the paper by showing that removing the 1D convolution from Mamba collapses it to Transformer-level performance, and adding it to the Transformer raises it to SSM-level performance.

## Suggestions

1. **Reframe the central thesis** (line 39) to explicitly separate the 2-layer case (where optimization is the primary differentiator) from the 1-layer case (where an expressivity gap exists). The existing evidence already supports this distinction.
2. **Either provide mechanistic evidence** for the induction head claim (attention pattern analysis, logit lens probing) or substantially soften the claim to "a phase transition of unknown origin."
3. **Add a small-scale language modeling experiment** (even a brief perplexity comparison at optimal LRs) to increase confidence that the findings generalize beyond synthetic tasks.

## Score and Decision

**Bracket (Round 1):** 5.5–6.5.

**Calibration Anchors Considered:**
- `iVy7aRMb0K.md` — "Mimetic Initialization Helps State Space Models Learn to Recall" (avg 4.50, Reject): Very similar topic, but this paper has broader scope (more architectures, cleaner central finding, more ablations). Current paper is clearly stronger.
- `b5lXUwZiD3.md` — "On Limitation of Transformer for Learning HMMs" (avg 5.25, Reject): Synthetic-benchmark study of architectural limitations; comparable approach but the current paper has more practical implications and a cleaner central finding.
- `QFgbJOYJSE.md` — "State Space Models are Provably Comparable to Transformers" (avg 5.75, Accept): Theoretical+empirical paper with similar scope; accepted at this score.
- `pymXpl4qvi.md` — "Understanding Bottlenecks of SSMs through Recency and Over-smoothing" (avg 6.00, Accept): Similar topical area with both theoretical and empirical contributions.
- `d8w0pmvXbZ.md` — "Small-scale proxies for large-scale Transformer training instabilities" (avg 8.00, Accept): Methodologically similar in studying LR sensitivity, but more polished and complete. Current paper is not at this level.
- `PdaPky8MUn.md` — "Never Train from Scratch" (avg 8.00, Accept): Similarly about benchmarking confounds between architectures, but cleaner central claim and more complete. Current paper is not at this level.

**Final Score:** 6.0. The paper makes genuine empirical contributions (the LR-sensitivity confound, the scaling analysis, the convolution ablation) that are well-documented and practically useful. The weaknesses (overreaching thesis, speculative induction head claim, lack of language modeling validation) are real but fixable and do not undermine the core findings.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>