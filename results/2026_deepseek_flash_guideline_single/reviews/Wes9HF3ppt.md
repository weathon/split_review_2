Now I have a solid calibration. Let me finalize the review.

**Calibration Summary:**

Anchors used (topical matches):
1. **FiLM** (4.25, reject) — fill-in LM, similar training/inference concern, weaker empirical results
2. **COrAL** (5.75, reject) — order-agnostic modeling, limited task generalization
3. **SequenceMatch** (6.00, accept) — novel IL formulation for sequence modeling
4. **Energy-Based Diffusion LM** (6.75, accept) — alternative text generation paradigm
5. **Beyond Autoregression: Discrete Diffusion for Planning** (6.25, accept) — discrete diffusion for planning/reasoning, closest topical match on the planning side. Strong planning results, accepted despite limited task scope.
6. **SAD3-LM** (8.00, accept) — comprehensive with theoretical grounding

**Bracket:** Round 1 suggested 5.0–6.0. Round 2 narrowed: the ILM paper has planning results at least as compelling as the 6.25 MDM planning paper, but suffers from an unanalyzed biased objective that the MDM paper doesn't have. The text results are weaker than the 6.75 EDLM paper. This places ILM at 5.5—between the accepted planning-diffusion paper (6.25) and the rejected FiLM paper (4.25).

Here is the final review:

## Summary

This paper introduces Insertion Language Models (ILMs), a novel approach to sequence generation that learns to insert tokens at arbitrary positions via a denoising objective. Unlike autoregressive models (ARMs) that generate left-to-right and masked diffusion models (MDMs) that unmask fixed positions simultaneously, ILMs remove tokens during training and learn to reinsert them one-at-a-time. The paper evaluates ILMs on planning tasks (star graphs, zebra puzzles) and text generation/infilling, showing strong results on structured tasks where ILMs outperform both ARMs and MDMs.

## Strengths

1. **Star graph experiments (Table 1) convincingly demonstrate a genuine capability gap.** ILM achieves 100% on Star_easy and Star_medium and 99.1% on Star_hard, while the best alternative (ARMO) is not applicable on medium/hard tasks, and MDM drops to 36.5% and 21.0%. The three difficulty levels cleanly isolate the effects of variable-length arms (MDMs' weakness) and out-of-order generation needs (ARMs' weakness). This is the paper's most compelling result — a regime where existing methods systematically fail and ILM does not.

2. **The core idea is well-motivated and clearly framed.** The paper correctly identifies two real limitations of MDMs — simultaneous unmasking violating sequential dependencies and fixed mask positions preventing arbitrary-length infilling — and proposes an insertion-based paradigm that directly addresses both. Figure 1 provides an illuminating contrast between ARMs, MDMs, and ILMs.

3. **Zebra puzzle results provide consistent supporting evidence.** ILM's 90% accuracy beats ARM (81.2%) and MDM (82.6%) and approaches the oracle-decomposed ARM (91.2%) on a distinctly different type of constraint-satisfaction task.

## Weaknesses

### Fatal
None.

### Major

1. **The biased training objective is acknowledged but not analyzed, and its relationship to the sequential inference procedure is unclear.** The training target (Equation 2) is an aggregate count distribution over *all* missing tokens in each gap — predicting the normalized frequency of each vocabulary item appearing in the original sequence between two visible tokens. During inference, however, the model inserts tokens *one at a time*, recomputing after each insertion. The paper states that an unbiased Monte Carlo estimate "can have extremely high variance" (line 18) and that the proposed objective is "biased" (line 79), but it never characterizes: (a) what quantity is being approximated and what the bias is relative to, (b) under what conditions the bias is large vs. small, or (c) why optimizing the aggregate-count objective should yield a model capable of correct sequential insertion at inference. While the empirical results suggest the bias is not fatal in practice (especially on the planning tasks), the complete lack of analysis of this central methodological choice is a significant gap.

2. **Text generation claims are overstated relative to the evidence, and the evaluation is confounded by length differences.** The abstract states ILMs "perform on par with ARMs" on unconditional text generation. Table 2 tells a different story: on LM1B the gap is large (4.67 vs. 3.94 NLL), and even on Stories where it is closer (2.14 vs. 2.11), ILM is still strictly worse. Critically, ILM generates sequences shorter than the training average on both datasets (Stories: 119 vs. 205; LM1B: 21 vs. 28), while the comparison models produce sequences at or above the average. Since NLL under a reference LLM is length-sensitive, this confound makes the raw NLL comparison unreliable for assessing generation quality. The entropy metric confirms ILM's text is less diverse (LM1B: 2.80 vs. ARM's 3.12 and training data's 3.08). The paper's own introduction uses the more measured language "competitive with ARMs" — the abstract overreaches.

### Minor

1. **No uncertainty estimates (standard errors/confidence intervals) are reported in any table.** Table 1 reports exact match accuracy without variance across seeds, data splits, or generation trials. Given the small size of some datasets (e.g., zebra puzzles), this makes it difficult to assess whether reported differences between methods are reliable.

2. **The stopping loss and its effect on generated length are underexplored.** ILM generates sequences significantly shorter than the training average on both text datasets. The stopping classifier is trained on random patterns of dropped tokens but used on the sequential states visited during inference — a mismatch that parallels the core training-inference gap. An analysis of stopping behavior (precision-recall or length distribution) would clarify whether this is a correctable calibration issue or a deeper limitation.

3. **Inconsistent naming:** The text switches between "Star_small" (line 147) and "Star_easy" (Table 1) for the same task configuration.

### Trivial
None.

## Nice-to-Haves
- **Add a fill-in-the-middle (FIM) ARM baseline for infilling, or a clearer justification for its exclusion.** The paper argues ARMs "are not capable of performing infilling without specialized training" (line 245), but work on FIM training (Bavarian et al., 2022, cited) provides a natural baseline, even if limited to single-segment infilling. Including this would strengthen the claim of practical advantage for infilling.
- **Analyze the biased objective empirically**, e.g., by comparing to an unbiased Monte Carlo estimator at small scale on the star graph tasks.
- **Add length-controlled evaluation for text generation**, e.g., by reporting NLL on sequences within a matched length range, or using standard held-out perplexity.
- **Sweep ILM's inference hyperparameters** (position top-k, token nucleus p) and report their effect on quality, similar to the MDM step-count sweep in Figure 6.

## Removed Points
- **"MDM baselines appear unusually weak"** — Speculative. The paper provides implementation details (based on Sahoo et al. 2024, log-linear noise schedule). The inflated MDM lengths are noted by the paper as an observed behavior, not necessarily a tuning artifact.
- **"Missing FIM baseline as a critical omission"** — Demoted to Nice-to-Have. The paper scopes its infilling claims to arbitrary-length and multi-segment infilling, where FIM-trained ARMs face their own limitations (discussed in Related Work).
- **Section-by-section presentation notes** about introduction framing and MDM description details — These are observations that don't rise to the level of verifiable weaknesses.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Recalibrate the abstract's text generation claim from "on par with ARMs" to "competitive with ARMs" (consistent with the introduction's own language).
2. Add an analysis (even brief) of the biased training objective — this is the most concerning gap.
3. Report confidence intervals or standard errors for all main results.
4. Analyze the stopping classifier's behavior and its effect on generated length distributions.
5. Fix the "Star_small"/"Star_easy" naming inconsistency.

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>