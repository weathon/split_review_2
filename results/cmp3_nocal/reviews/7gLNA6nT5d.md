Now let me produce the final consolidated review.

## Summary

This paper proposes integrating n-gram induction heads (from Akyürek et al. 2024) into transformers for in-context reinforcement learning (ICRL), specifically building on Algorithm Distillation (AD). The motivation is well-grounded: transformers exhibit simplicity bias toward unigram patterns and in-context ability is transient, making AD training data-inefficient and hyperparameter-sensitive. By hardcoding n-gram attention patterns, the paper aims to reduce data requirements and improve training stability. Experiments on Dark Room, Key-to-Door, and Miniworld (discrete and pixel-based) show that the n-gram variant finds better hyperparameters faster and generalizes from fewer training goals than standard AD.

## Strengths

1. **Targeted architectural fix for a diagnosed problem.** The paper identifies two concrete failure modes of AD (simplicity bias and transient in-context ability, lines 61–71) and proposes n-gram heads as a direct remedy. This is not a generic "add a module" paper; the mechanism is explicitly tied to the underlying issue.

2. **Figure 1 shows genuine data-efficiency gains.** At 128 training goals, the n-gram model achieves a return of ~1.9, while the AD baseline at 128 goals achieves only ~1.0 and needs ~512 goals to approach the same performance. This improvement is clearly visible in the paper's own controlled experiments.

3. **The evaluation protocol (EMP from random hyperparameter search, fixed batch size, 10K gradient-step limit) avoids cherry-picking** and provides a fair basis for comparing hyperparameter sensitivity between methods. The ablation studies (Sections 4.4–4.5) asking whether n-gram layers expand the search space or hurt baseline performance are the right questions to ask.

4. **Demonstrated applicability to pixel-based observations.** Extending n-gram heads to visual domains via VQ, while straightforward, broadens the relevance of the method beyond discrete grid worlds.

## Weaknesses

### Major

1. **The marquee 27× data-efficiency claim is not empirically supported within the paper.** The claim (abstract line 45, Section 4.2 line 179) is that the n-gram method with 100 goals matches the performance reported for AD with 2048 goals from the original Laskin et al. paper [17]. But the paper never runs AD at 2048 goals (or any intermediate scale) in its own environment setup to verify that this performance level is actually achieved under its evaluation protocol. The AD baseline in Figure 4 is trained on the *same 100 goals* as the n-gram method and plateaus at a return of ~1.3 — well below the ~1.9 achieved by the n-gram model. The 27× ratio is therefore a cross-paper computation whose validity depends on assuming that Laskin et al.'s results transfer perfectly to this paper's implementation, data collection pipeline, and evaluation protocol. This is a significant gap in the evidence for the paper's central quantitative claim.

2. **Unexplained numerical discrepancy between Table 1 and Figures 5–6 for Miniworld-Dark.** Table 1(a–b) reports EMP values of 0.67–0.76 for various n-gram configurations in Miniworld-Dark (ablation on layer position and n-gram length). Yet Figure 5 (left, 30 goals, 50 histories) shows the n-gram method reaching ~0.96 EMP, and Figure 6 (left, 50 goals) shows ~0.95 EMP. The gap of ~0.2–0.3 EMP is very large. The paper does not state the experimental conditions (number of goals, learning histories, etc.) used for Table 1. If a different data regime was used, it must be stated explicitly; if the same regime was used, the results are contradictory. This omission undermines confidence in the reliability of the reported numbers.

### Minor

3. **Key quantitative results lack uncertainty estimates.** Figures 2, 4, and 5 report EMP from single random hyperparameter searches without any confidence intervals, standard errors, or min/max ranges. The paper makes precise numerical claims — e.g., "finding the optimal model requires just over 20 hyperparameter assignments, while the baseline model needs more than 400" (line 171) — but the reader cannot assess whether these numbers are stable across different random search orderings. Only Figure 6 includes confidence intervals. While EMP is a standard metric, the specific numerical comparisons in the text would be substantially more informative with variability estimates.

4. **No accounting for the computational cost of n-gram heads.** The n-gram layer adds learnable parameters (W₁, W₂, MLP) and the n-gram matching computation. The paper compares methods solely on data efficiency and hyperparameter search efficiency but never reports wall-clock time, FLOPs per step, or parameter counts for either method. If the n-gram layer adds non-trivial overhead per step, the comparison becomes less straightforward.

### Trivial

5. **N-gram attention equation notation is underspecified.** Equation (line 77) defines A(n)_{ij} by matching x_{i-k} against x_{j-k-1} but does not clearly explain why the indices are offset or how this implements a causal n-gram matching pattern. The surrounding text (line 83) gives a high-level intuition but the formal definition remains ambiguous.

## Nice-to-Haves

- Run AD at multiple data scales (e.g., 500, 1000, 2048 goals) in the same environments to directly demonstrate the data efficiency ratio rather than relying on a cross-paper comparison.
- Report the transformer architecture (number of layers, hidden dimension, heads, total parameters) in the main text.
- Provide VQ details: codebook size, training data, reconstruction accuracy.
- Analyze why the "[s, a, r]" matching variant underperforms the "states" variant in Key-to-Door — this could yield insights into what n-gram patterns are actually useful.

## Removed Points

These points were raised in the input review but removed with justification:

- **"Comparison limited to AD, ignoring data-centric ICRL approaches (noise curriculum, data augmentation, data filtering)."** — Removed as scope creep. The paper explicitly positions its contribution as model-centric and complementary to data-centric approaches (line 217). Demanding empirical comparison against fundamentally different intervention types is outside the paper's stated scope.
- **"Inconsistency between 'drop-in replacement' and 'additional layer' descriptions."** — Removed. Line 39 describes Akyürek et al.'s original use as a drop-in replacement; line 87 describes this paper's implementation following the NGL structure. The paper is clear enough.
- **"The 'permuted mask' experiment does not address redundancy when data is abundant."** — Removed. The experiment's stated scope (testing whether a broken n-gram mechanism harms performance) is exactly what it addresses; the experiment does not claim to test other failure modes.

## Novel Insights

None beyond the paper's own contributions. The connection between n-gram induction heads (previously shown to reduce perplexity in language modeling) and the data-efficiency problem in ICRL is the paper's core insight, and the reviews do not surface a distinct novel observation beyond this.

## Suggestions

- Replace or supplement the 27× cross-paper claim with a controlled scaling experiment (AD at 3–4 data scales) within the paper's own environment setup.
- Add confidence intervals or bootstrap ranges to the EMP curves in Figures 2, 4, and 5, especially for the specific numerical claims about hyperparameter assignment counts.
- State the experimental conditions (number of goals, learning histories, evaluation goals) used in Table 1 explicitly in the main text, and reconcile the ≈0.2–0.3 EMP gap with Figures 5–6.

## Score and Decision

The paper addresses a well-motivated problem with a sensible architectural modification and provides reasonable initial evidence. The core experimental results (Figures 1, 2, 4) show genuine improvements in data efficiency and hyperparameter robustness in simple environments. However, the paper's strongest quantitative claim (27× data reduction) relies on an uncontrolled cross-paper comparison rather than within-paper evidence, and an unexplained numerical discrepancy between Table 1 and Figures 5–6 undermines confidence in the Miniworld results. These issues are fixable but, as presented, the evidence is weaker than the claims.

**Score: 4**

**Decision: Reject**

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>