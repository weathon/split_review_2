Now I have all the information needed. Let me produce the final consolidated review.

## Summary

This paper decouples class labels from target concepts in class-wise machine unlearning, introducing three new mismatch settings (target mismatch, model mismatch, data mismatch) beyond the conventional all-matched setting. It proposes TARF (TARget-aware Forgetting), a three-phase framework that uses annealed gradient ascent on forgetting data and gradient descent on identified retaining data to handle these mismatch scenarios. The empirical results on vision classification benchmarks (CIFAR-10, CIFAR-100, ImageNet) show TARF substantially outperforms existing unlearning methods on the mismatch settings, often by an order of magnitude on the Gap metric.

## Strengths

1. **Genuinely novel conceptual framework for class-wise unlearning.** The formalization of label-domain mismatch via the three label domains $\mathcal{L}_D, \mathcal{L}_M, \mathcal{L}_T$ (Section 3.1, Figure 1) and the four resulting scenarios is clean, well-motivated, and opens a research direction that prior work overlooked. This is not a minor extension — it reframes what "unlearning a class" could mean in practice.

2. **Dramatic empirical advantage on mismatch benchmarks.** On CIFAR-10/100 mismatch settings (Table 3), TARF's Gap score is often an order of magnitude better than the next-best baseline: e.g., Target mismatch on CIFAR-100: TARF Gap = 0.21 vs. next best (GA) = 8.86; Data mismatch on CIFAR-10: TARF Gap = 0.96 vs. next best (GA) = 5.89. These are not incremental improvements. The advantage holds on ImageNet-1k (Table 4), where TARF achieves the lowest Gap across all four settings.

3. **Method design follows logically from diagnosed failure modes.** The three-phase framework (target identification → target separation → retraining approximation) directly responds to the specific failure modes identified in Section 3.2: insufficient representation when $\mathcal{L}_D \prec \mathcal{L}_T$, and decomposition lacking when $\mathcal{L}_T \prec \mathcal{L}_M$. This internal coherence between analysis and solution is a genuine strength.

## Weaknesses

### Fatal
None.

### Major

1. **The LLM/TOFU experiments (Table 5) do not support the paper's claims and may contradict them.** The paper presents these as a "case study on real-world application," implying TARF is effective for LLM unlearning. However, the data in Table 5 tells a different story:

   - In the **All-matched** setting: TARF(GA) achieves QA Prob on F. (forgetting) = 0.0762 vs. CL(GA) = 0.0009 — TARF is *worse* at forgetting. TARF also achieves lower retaining probability (0.0824 vs. 0.1624).
   - In the **Target Mismatch** setting: TARF(GA) achieves QA Prob on R. = 0.0094 vs. CL(NPO) = 0.4481 — TARF destroys retaining utility while NPO preserves it.
   - In several settings (lines 318–325), TARF matches the baseline (GA) exactly, suggesting the TARF-specific mechanism adds no value in those cases.

   The table formatting is additionally difficult to interpret (repeated section headers, unclear column-to-setting mappings), but even accounting for this, the visible numbers do not demonstrate that TARF improves upon baselines for LLM unlearning. **This does not invalidate the core vision contribution, but the paper should either (a) present convincing LLM evidence, (b) honestly acknowledge that the method does not transfer to LLMs and frame the contribution as being about vision classifiers, or (c) remove this section.**

### Minor

2. **Theorem 3.2 is a standard Lipschitz bound, not a deep theoretical result.** The theorem states that after one gradient ascent step, the change in the loss gap is bounded by a term proportional to representation distance — essentially "gradients of similar examples are similar." This follows directly from the Lipschitz smoothness assumption (Assumption 3.1) and a Taylor expansion. The paper invokes it as foundational ("reveal crucial forgetting dynamics," "systematically analyze the new challenges"), which overstates its contribution. The real value in Section 3.2 comes from the *empirical* analysis (Figure 3, Figure 9) showing that representation entanglement correlates with poor unlearning. The paper would be stronger if it reframed Section 3.2 as an empirical investigation supported by a straightforward analytical bound.

3. **The target identification procedure assumes knowledge of the target concept's composition.** Section 2 states: "we assume that the number of classes in $\mathcal{D}_{un}$ belonging to the target concept is known in target mismatch forgetting." This assumption is used to set the threshold $\beta$ for identifying false retaining data. In practice, a user reporting "boy" and "girl" images to unlearn "people" may not know how many other classes (man, woman, baby, etc.) fall under the target concept. The paper does not explore how performance degrades when this composition is misspecified or unknown, which narrows the practical applicability more than the paper acknowledges.

4. **Key hyperparameters lack concrete guidance in the main text.** The parameters $k$, $t_0$, $t_1$, and $\beta$ are critical to performance. Their selection is deferred to the appendix with only vague guidance (e.g., "$\beta$ can be estimated by the information about the specific unlearning request and the rank of loss/accuracy change"). A concrete recommendation or sensitivity analysis in the main text would improve reproducibility.

### Trivial

5. **No error bars in main tables.** The standard deviations are relegated to Appendix F.7. While single-run evaluation is common for large-scale vision benchmarks, the main tables would benefit from at least a note on variance.

6. **Limited discussion of computational cost.** The paper mentions Appendix E.2 for cost analysis, but the overhead of Phase I (running gradient ascent and evaluating accuracy across all remaining classes) is a practical concern that warrants at least a paragraph in the main text.

## Nice-to-Haves

- The ablation on gradient cleaning vs. gradient ascent for the selected forgetting data (Figure 7, right panel) suggests that setting gradients to zero may outperform gradient ascent on retaining accuracy. This is a useful practical insight that the paper does not fully discuss or consider incorporating.
- A dedicated limitations section in the main text would help contextualize the assumptions made in the target identification procedure.
- A sensitivity analysis for the target composition assumption (varying the number of classes assumed to belong to the target concept) would strengthen the practical applicability claims.

## Removed Points

These points were raised in the input review but are removed under the filtering rules:

- **"The claim that 'previous studies showed class-wise unlearning is effective' could be more precise"** — Minor phrasing issue; the paper's context makes the intended meaning clear.
- **"Text describing Figure 2 is somewhat repetitive"** — Style nitpick; does not affect the technical contribution.
- **"Representation gravity adds rhetorical flair but no technical content"** — The quantity $I_{\text{con}}$ is defined operationally (change in loss after $t$ gradient steps) and is used directly in the algorithm. Calling it "gravity" is metaphorical but the underlying computation is concrete and necessary.
- **"Gap metric is somewhat opaque"** — This is an observation about presentation, not a weakness. The paper breaks down Gap into its constituent metrics (UA, RA, TA, MIA), so readers can examine individual components.
- **"No discussion of limitations"** — The conclusion does discuss an open challenge (lines 355–360). While not a full limitations section, the paper acknowledges inherent difficulty in ambiguous regimes. This is reasonable.

## Novel Insights

None beyond the paper's own contributions. The reviews surface that the LLM/TOFU results are problematic and that the theoretical analysis is overstated, but these are corrections to the paper's framing rather than novel insights about the method itself.

## Suggestions

1. **Address the LLM/TOFU section honestly.** Either present results that convincingly demonstrate TARF's effectiveness in LLM settings, or remove the claim of LLM applicability and frame the contribution as being about vision classifiers. Presenting data that contradicts the narrative without acknowledging the contradiction weakens the paper.

2. **Recalibrate the rhetorical weight on Theorem 3.2.** Reframe Section 3.2 as an empirical investigation of forgetting dynamics supported by a simple analytical bound, rather than claiming the theorem as a foundational theoretical result.

3. **Add a sensitivity analysis** exploring how TARF's performance degrades when the target concept composition is misspecified (e.g., incorrect assumption about which classes fall under the target concept). Alternatively, state this as a clear limitation.

## Score and Decision

The paper makes a genuinely novel conceptual contribution and provides compelling experimental evidence on vision classification benchmarks. The TOFU issue is significant but fixable and does not invalidate the core contribution. I recommend acceptance.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>