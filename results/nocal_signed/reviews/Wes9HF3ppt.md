Now I'll write the final consolidated review.

## Summary

This paper introduces Insertion Language Models (ILMs), which generate sequences by inserting tokens one at a time at arbitrary positions — jointly selecting both *where* and *what* to insert. ILMs replace the fixed-length mask tokens of Masked Diffusion Models (MDMs) with a learned insertion mechanism, enabling variable-length generation and flexible infilling. The authors propose a denoising training objective (acknowledged as a biased approximation), a transformer-based parameterization with a learned stopping classifier, and evaluate on planning tasks (star graphs, zebra puzzles) and language modeling (LM1B, TinyStories).

## Strengths

- **Well-motivated and clearly articulated problem.** The paper concretely identifies a real gap in MDMs: fixed-length masks causing simultaneous-unmasking violations of token dependencies, and rigid infilling constraints. The examples ("chef added sugar", Section 1) are specific and testable, not hand-waving.

- **Strong planning-task results that cleanly demonstrate the benefit of insertion-based generation.** On star graphs (Table 1), ILM achieves 99.1% on the hard setting vs. MDM's 21.0% and ARM's 23.0%. The ablation against Insertion Transformer (17.5% on hard) confirms the dedicated stopping classifier matters. The zebra puzzle result (90.0% vs. 82.6% for MDM and 81.2% for ARM) further supports the method's value for constraint-satisfaction tasks where out-of-order generation helps.

- **The paper is honest about the limitations of its approach.** It openly states the training objective is "biased" (Section 3), acknowledges ILM performs worse than ARM on LM1B (Section 6), and notes the lack of KV caching as a practical limitation.

## Weaknesses

### Fatal
None.

### Major

1. **Missing comparison against improved MDM inference techniques.** The paper only compares against vanilla MDM with tau-leaping sampling, yet Section 4 itself cites improved inference methods — greedy sequential unmasking (Gong et al., 2024), top-k unmasking (Zheng et al., 2024), and flow-based corrections (Campbell et al., 2024) — that were designed to address exactly the "simultaneous unmasking" problem the paper highlights. Since these techniques exist specifically to mitigate the limitation ILMs are positioned against, the claim that ILMs "overcome the limitations of MDMs" is only substantiated against the weakest form of MDM inference. This is the single most impactful comparison gap.

2. **The training objective bias is acknowledged but unanalyzed.** The training loss (Equation 2) predicts normalized token counts across all dropped tokens in one pass, while inference inserts tokens sequentially with re-evaluation after each insertion. This is a genuinely different task. The paper describes the objective as "biased," references Appendix D for high-variance issues, but provides no analysis of what the bias is, when it breaks down, or why the biased objective still yields a correct generative distribution. The method's mixed language results (competitive on Stories, 18.5% worse on LM1B) could plausibly stem from this mismatch, and without analysis the reader cannot assess whether the gap is fundamental or fixable.

3. **The abstract overclaims language modeling performance.** The abstract states ILMs "perform on par with ARMs and better than MDMs in unconditional text generation." Table 2 shows this is accurate on Stories (2.14 vs. 2.11 NLL, within 1.4%) but not on LM1B (4.67 vs. 3.94 NLL, an 18.5% gap). The claim should explicitly acknowledge the LM1B gap rather than generalize "on par."

### Minor

4. **Prometheus evaluation lacks statistical rigor.** The Prometheus judge scores (Figure 5) are reported without confidence intervals, sample sizes, or significance tests. The entropy metric is also acknowledged by the authors to be confounded by sequence length differences between models, but no length-normalized alternative is provided.

5. **No ablation of the stopping classifier on text tasks.** The main difference between ILM and the prior Insertion Transformer (Stern et al., 2019) is the dedicated stopping classifier, but this is only ablated on star graphs. An ablation on text would clarify whether the stopping mechanism is critical for language quality or only for the length-matching demands of planning tasks.

### Trivial

6. **Potential indexing ambiguity in Equation 2.** The sum runs over $k \in [L-n]$ gaps between visible tokens, but with $L-n$ visible tokens there are $L-n+1$ total gaps (including before the first and after the last visible token). The special `<stp>` token at position 0 may account for the first gap, but the last gap's handling should be clarified.

## Nice-to-Haves

- Compare against MDMs with greedy/top-k sequential unmasking, especially on the star graph task where the comparison would be most informative.
- Analyze the training objective bias on a small-scale task, comparing the proposed objective against a Monte Carlo estimate of the true marginalization.
- Report total FLOPs or wall-clock time including KV caching comparisons for practical inference cost assessment.
- Provide length-normalized entropy to isolate token diversity from sequence-length effects.

## Removed Points

These are flagged to be removed; treat them with caution.

1. *"Section 1 claim about ARMs struggling with sophisticated constraints is not backed by a citation"* — REMOVED (factually incorrect: the paper cites Sun et al., 2023 on line 13).
2. *"Star graph ARM accuracy is counterintuitive (32.3% easy vs. 75.0% medium)"* — REMOVED (the paper explains this via degree differences between the two task variants).
3. *"The 'reverse' generation claim is inconsistent"* — REMOVED (the paper's phrasing on line 18 refers to the denoising direction, not the generation order; the meaning is clear in context).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add MDMs with greedy/top-k sequential unmasking as baselines to substantiate the claim of "overcoming MDM limitations."
2. Analyze or ablate the training objective bias, even on a small synthetic task, to clarify whether the approximation is harmless or limiting.
3. Qualify the abstract's language modeling claim to acknowledge the LM1B gap explicitly.
4. Report confidence intervals for Prometheus scores and provide length-normalized entropy.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>