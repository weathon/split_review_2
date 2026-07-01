Now I have enough calibration context. Let me write the final review.

## Summary

This paper proposes SteadyThought (ST), a three-stage framework (thought segmentation → thought completion → fine-grained preference optimization) to address "under-thinking" in Large Reasoning Models — the phenomenon where models abandon promising reasoning trajectories and switch excessively between thoughts. The core idea is to train models to recognize and commit to promising thoughts via thought-level preference optimization (STPO), rather than suppressing switching at inference time. Experiments across three model sizes (1.5B–14B) and four datasets (MATH-500, AIME 2024, GSM8K, LiveCode) show consistent accuracy improvements (up to 5.3%) with 17–39% token reductions, including out-of-distribution generalization to code.

## Strengths

1. **Well-motivated problem with concrete behavioral evidence.** Figures 1a/1b empirically ground the under-thinking concept by showing that correct thoughts appear early in the reasoning trace but are abandoned — this is a specific, observable failure mode distinct from generic "over-thinking." The paper doesn't just assert the problem exists; it demonstrates it with data.

2. **Novel formulation of under-thinking as a thought-level preference optimization problem.** The formalization in Section 2.1 (Commit Trajectory vs. Switch Trajectory with Bradley-Terry modeling over thought-level preferences) re-frames a phenomenon previously addressed via inference-time suppression into a principled training objective. This conceptual advance is the paper's strongest contribution.

3. **Thought-level preference construction is a genuine improvement over holistic preference optimization.** The observation that response-level DPO discards correct intermediate reasoning from otherwise-incorrect responses (Section 3.3) is well-taken, and conditioning preference pairs on (Q, Tᵢ) rather than the full question is a clean, justified design choice.

4. **Consistent accuracy improvements across model scales with meaningful efficiency gains.** Table 1 shows accuracy improvements on all three models (1.5B, 8B, 14B) across all four datasets, with token reductions of 17–25% (up to 39% on individual settings). The generalization to LiveCode — an out-of-distribution coding benchmark — is particularly strong evidence that the method learned a general reasoning discipline.

5. **Informative ablation of training objectives (Table 4).** Comparing SFT, DPO, and STPO under the same preference data clearly shows that the length-normalized, thought-level objective matters: SFT collapses to short inaccurate outputs, DPO struggles with length asymmetry, and STPO achieves the best trade-off.

## Weaknesses

### Fatal
None.

### Major

1. **Unaddressed tension around logit suppression.** The paper criticizes prior work (NOWAIT, etc.) for using logit suppression "globally, potentially limiting the model's flexibility to explore alternative reasoning thoughts" (lines 17–18). Yet Stage 2 (Thought Completion) uses precisely this technique — sharply decreasing logits for trigger words like "wait" and "alternatively" (line 99) — to generate the completions that become the "chosen" responses in the preference data. While there is a conceptual distinction (data generation vs. inference-time intervention), the paper never acknowledges or justifies this asymmetry. This leaves an open question: could the forced completions be biased or nonsensical in cases where a switch was genuinely necessary? The paper should explicitly address why logit suppression is acceptable in Stage 2 but not at inference time.

2. **No measures of variance despite reporting multiple runs.** The paper states it averages eight runs for AIME and two for LiveCode (line 143) but reports no standard deviations, confidence intervals, or any variance metric anywhere. For AIME with only 30 problems, a single problem shifts accuracy by ~3.3 pp. Without variance information, it is impossible to assess whether improvements like +1.9% (1.5B overall) or +3.12% (8B overall) are statistically reliable. This is the single most impactful addition the authors could make for credibility.

### Minor

3. **SEAL is competitive in several settings, but this is not discussed.** On Qwen3-8B, SEAL achieves higher accuracy than ST on LiveCode (83.4 vs. 77.1) and is close on the overall average (82.58 vs. 83.35). The paper presents ST as straightforwardly superior without discussing when and why SEAL's representation-level steering succeeds where ST's preference optimization does not. Discussing this comparative pattern would sharpen the contribution.

4. **Partial alignment of structural evaluation metrics with training objective.** The metrics most emphasized in Sections 4.4.1–4.4.2 (thought count, proportion of last thought, PCT) are partially measuring compliance with the training signal rather than providing fully independent evidence. The training directly prefers single-trajectory completions over multi-thought continuations; after training, finding fewer thoughts and higher last-thought proportion is expected. The accuracy improvements are the genuinely independent signal. The paper's narrative treats the structural metrics as co-equal evidence rather than as sanity checks that training worked as intended.

### Trivial

5. **Downward arrow for accuracy (Acc[%]↓).** In Table 1 (line 155), accuracy is marked with a down arrow, which is confusing since higher accuracy is better. This should use an up arrow or be explained clearly.

## Nice-to-Haves

- Analyze whether the model's switching rate depends on the *quality* of the current thought (e.g., intermediate correctness) to demonstrate that it learned discriminative commitment rather than a uniform bias toward sticking with the current thought.
- Show concrete cases where the model *correctly switches* to a better thought, demonstrating that flexibility is preserved (as claimed).
- Report training hyperparameters (learning rate, batch size, β, γ) and training set size to facilitate reproducibility and comparison.

## Removed Points

These points were flagged by the harsh critic but are removed with justification:

1. **Missing training details / hyperparameters (original Critical #3).** The paper specifies the training source (omni-math) and the STPO objective (Eq. 7). The appendix (stripped by the parser) likely contains the hyperparameter values referenced. Per the rules, parser-stripped appendix content and reproducibility nitpicks about undisclosed hyperparameters are removed.

2. **Thought segmentation quality not validated (from Section-by-Section).** While a human evaluation of segmentation quality would strengthen the paper, the entropy-based approach is a standard technique (referenced to Wang et al. 2025b), and the hyperparameter analysis in Table 3 provides indirect validation. Demanding a human evaluation for an algorithmic contribution is scope creep by the reviewer.

3. **"Correct intermediate thoughts = Invalid Switches" assumption (Section 4.4.2).** The reviewer argued this conflates distinct phenomena. However, the paper's definition is explicit: an invalid switch is *any* abandonment of a correct intermediate thought. While imperfect, this is a clear operational definition, and the paper's interpretation is transparent about what it measures.

4. **STPO is "just SimPO applied at thought level."** The paper's contribution is explicitly the *framework* (data construction + thought-level framing), not a new loss function. The paper is transparent about this — line 119 says "inspired by the reference-free and length-normalized objective of SimPO." This is not a weakness; it is an appropriate building-block approach.

5. **Underspecified data generation pipeline (from Section-by-Section).** The paper describes the pipeline at a reasonable level of detail for the main text. Specific yield rates and per-problem sampling counts are likely in the appendix.

## Novel Insights

None beyond the paper's own contributions. The key insight — that under-thinking can be addressed via thought-level preference optimization — is the paper's own, and the reviews do not surface a deeper or conflicting perspective.

## Suggestions

1. Add standard deviations or confidence intervals for all reported accuracy numbers. With 8 runs on AIME, this is straightforward and would substantially strengthen the paper.
2. Add a paragraph in Section 3.2 explicitly justifying why logit suppression is acceptable during data generation but not at inference time, and acknowledge the limitation.
3. Discuss the SEAL comparison more honestly — particularly why SEAL outperforms ST on Qwen3-8B LiveCode — and what this reveals about the relative merits of representation-level steering vs. preference optimization.
4. Reframe the structural metrics (thought count, PCT) as sanity checks that the training worked as intended rather than as co-eval evidence of the method's value.

## Score and Decision

**Round 1 bracket:** 5.5 – 7.5 (after comparing to similar papers on preference optimization for reasoning).

**Calibration anchors:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| TPO (O0sQ9CPzai.md) | 6.33 | R1 | Preference optimization for reasoning with trees. SteadyThought has broader evaluation (3 models vs 1) but similar methodological contribution. Slightly stronger than ST. |
| TypedThinker (VIUisLx8lQ.md) | 6.00 | R1 | Multiple reasoning types framework. ST has clearer problem motivation and more consistent gains. Comparable in overall quality. |
| SuperCorrect (PyjZO7oSw2.md) | 6.50 | R1 | Teacher-student DPO for reasoning. Similar contribution level, both accepted. ST has more model/dataset variety. |
| Step-Controlled DPO (ZRDa2IT1sQ.md) | 6.00 | R2 | Data curation for DPO with reasoning errors. Rejected due to limited novelty. ST has stronger novelty and broader scope. |
| 3D-Properties (9Hxdixed7p.md) | 6.25 | R1 | Analysis of DPO properties. Different paper type (analysis vs method). Comparable quality tier. |
| Critic-CoT (JEehcb48Vp.md) | 5.75 | R2 | Self-critic framework for reasoning. Rejected. ST has stronger empirical results and clearer contribution. |

SteadyThought is most comparable to TPO (6.33, Accept) and SuperCorrect (6.50, Accept) in terms of contribution depth and evaluation breadth. It is notably stronger than Step-Controlled DPO (6.00, Reject, limited novelty) and Critic-CoT (5.75, Reject). The paper's weaknesses (missing variance, unaddressed logit-suppression tension, SEAL discussion) are real but fixable and do not undermine the core contribution.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>