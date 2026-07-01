Now I'll write the final consolidated review.

## Summary

This paper introduces INFO-SEDD, a method for estimating mutual information (MI) and KL divergences on high-dimensional discrete data using continuous-time Markov chains (CTMCs) and discrete diffusion models. The key innovation is that, by choosing an absorbing-state CTMC, marginal score ratios can be extracted from a single model trained on the joint distribution (Equation 6), avoiding the need for separate score models per marginal. The method is evaluated on synthetic benchmarks (where it significantly outperforms variational estimators in the high-MI regime), text summarization (consistency tests and model selection via alignment with human metrics), and genomics (motif discovery in promoter sequences).

## Strengths

1. **Novel and well-motivated approach to a genuine problem.** Existing neural MI estimators are designed for continuous spaces, and the common workaround of "embedding" discrete data into continuous space is acknowledged to be fragile and application-specific. INFO-SEDD operates directly in the native discrete space via CTMCs, targeting a real gap in the literature.

2. **Elegant computational design (Equation 6, Section 3).** The observation that an absorbing-state CTMC allows computing marginal score ratios from a single model trained on the joint distribution is theoretically clean and practically important. Without this, the method would require separate score models for the joint and each marginal, severely limiting scalability.

3. **Strong synthetic results (Table 1).** INFO-SEDD achieves mean estimates of 9.92 (MI=10) through 47.77 (MI=50) with low standard deviations (0.12–1.18), while the closest competitor (MINDE) at MI=50 gives 32.60 ± 3.93 — substantially biased with higher variance. The variational estimators show the known failure mode in the high-MI regime (McAllester & Stratos, 2020), and INFO-SEDD genuinely avoids it.

4. **Concrete scientific application (Section 4.3, Figure 5).** The TATA-BOX motif discovery experiment is compelling: the MI profile peaks within the biologically known region (-39 to -26 relative to TSS), and the method's ability to assess individual motif importance without interference from correlated motifs is methodologically non-trivial. This goes beyond benchmark scores into genuine scientific utility.

5. **Theoretical error bound (Equation 7).** The paper provides a decomposition of the estimation error into score approximation error and truncation bias, establishing consistency (up to exponentially decaying bias). This provides a formal grounding for the estimator's behavior.

## Weaknesses

### Fatal
None.

### Major

1. **Theoretical derivation of the core KL identity (Equation 2) is insufficiently justified and appears to conflict with standard properties of Markov chains as presented in the main text.** The paper asserts:

   KL[p₀ ‖ q₀] = E[log(p₀/q₀)(X_T)] = E[log(p_T/q_T)(X_T)]

   without explaining why these equalities hold. Under standard properties, the data processing inequality gives KL[p_T ‖ q_T] ≤ KL[p₀ ‖ q₀], and if both processes converge to the same stationary distribution π as T → ∞, then KL[p_T ‖ q_T] → 0 while KL[p₀ ‖ q₀] may be positive. Additionally, the claim that E[log(p₀/q₀)(X_T)] = KL[p₀ ‖ q₀] mixes the terminal distribution p_T in the expectation with initial densities p₀, q₀ in the log-ratio — this is not the standard definition of KL divergence and is not explained.

   The text after Equation (4) states "We omit the term E[log(p₀/q₀)(X₀)], as both p₀ and q₀ converge to π" — but E[log(p₀/q₀)(X₀)] with X₀ ~ p₀ is exactly KL[p₀ ‖ q₀], the quantity being estimated, and it does not vanish when both distributions converge to π under the forward process. The derivation as presented in the main text is therefore incomplete and potentially circular.

   **Why this is major, not fatal:** The strong empirical results (Table 1) suggest the estimator works in practice, and the full derivation may be in the appendix (which the parser has stripped). The paper mentions Dynkin's formula, which could provide a valid bridge. However, **as presented in the main text**, a reader cannot verify that Equation (2) is correct, and the reasoning about why the boundary term vanishes is not coherent. The authors must provide a clean, self-contained derivation in the main text.

2. **Comparison fairness is not adequately established, and the paper lacks basic computational cost reporting.** The paper claims "We use the same backbone for all methods" (Section 4.1), but this is not a sufficient control across method classes. INFO-SEDD uses a score network trained via the DWDSE loss for discrete diffusion — a fundamentally different training objective than the critic networks used by variational estimators (MINE, NWJ, SMILE) or the generator/discriminator networks used by F-DIME estimators. For the text summarization experiment, INFO-SEDD uses **MDLM-SMALL**, a pretrained discrete diffusion language model, as its backbone. The variational competitors use the same architecture but learn an embedding look-up table from scratch — they do not benefit from pretraining. This asymmetry advantages INFO-SEDD in a way that the comparison does not control for.

   More importantly, the paper reports **no wall-clock training times, no parameter counts, and no FLOPs** for any method in the main text. The abstract claims INFO-SEDD is "lightweight and scalable," but this claim is unsupported. Given that INFO-SEDD requires training or fine-tuning a full generative diffusion model, while variational estimators use comparatively lightweight critics, this omission is significant. The authors should report compute costs and either control for pretraining or explicitly acknowledge the asymmetry.

### Minor

1. **Consistency test reference lines in text summarization (Section 4.2) are heuristic upper bounds, not ground truth.** The paper constructs reference values of 256–303 nats by multiplying character-level entropy rates (≈1 bit/character) by the average summary length. This estimates the **total entropy** of the summary text, not the MI between summary and source. MI = H(summary) − H(summary | source) ≤ H(summary), so these reference lines are upper bounds. The paper implicitly treats them as ground-truth MI values when it claims INFO-SEDD "closely matches" them. The linear assumption (MI = ρ · H(summary)) additionally assumes conditional entropy is zero at ρ=1, which is false for summarization. The paper does partially acknowledge this ("we cannot establish exact ground truth") and calls it an "order-of-magnitude estimate," but the presentation in Figure 1 and the text overstates the evidential value.

2. **The "Empirical MI estimate" shown in Figure 1 (grey line) is never defined in the main text.** It appears only in the figure caption and legend. Without knowing how it is computed, the reader cannot interpret whether it is a valid reference.

3. **Darrin et al. (2024) correlation values are not reported.** The paper claims INFO-SEDD-C "achieves a comparable correlation" with consistency, but the actual Darrin et al. numbers are absent. The reader cannot verify this comparison.

4. **No baselines are compared on the TATA-BOX motif discovery task (Section 4.3).** The paper demonstrates that INFO-SEDD can localize the TATA-BOX motif, but does not compare against existing motif discovery tools (e.g., MEME, or the original Umarov & Solovyev method) in terms of localization accuracy or precision/recall. The experiment demonstrates feasibility, not superiority.

5. **Genomics classifier-based reference (Section 4.3) assumes the CADUCEUS classifier is near-optimal.** The reference MI is constructed by approximating H(Y|X) as H_b(Acc.), which assumes the classifier's accuracy equals the Bayes error rate. If the classifier has room for improvement, MI is overestimated. The absolute MI values are small (0–0.7 nats), so the error is likely bounded, but this limitation should be explicitly acknowledged.

6. **The error bound (Equation 7) contains constants (C₁*, C₂, D|χ|) whose magnitudes are not discussed.** For high-dimensional data (large D|χ|), which is precisely the setting INFO-SEDD targets, the bound could be very loose. A discussion of the bound's tightness or an empirical evaluation would strengthen the theoretical contribution.

7. **Overclaiming in the abstract.** The abstract claims INFO-SEDD "outperforms alternatives" — this is too broad, as the comparisons are against a specific set of variational estimators, not the full space of possible approaches. The claim of being "lightweight" is unsupported (see Major Issue 2).

### Trivial
None.

## Nice-to-Haves

- Provide a clean, self-contained derivation of Equation (2) in the main text that either (a) proves the equalities under explicit conditions, or (b) acknowledges them as approximations with a characterization of the error.
- Report parameter counts, wall-clock training time, and total training cost for INFO-SEDD and each competitor across all experiments. If competitors use smaller models, frame the comparison accordingly.
- Report Darrin et al. (2024) correlation numbers to substantiate the "comparable" claim.
- Define the "Empirical MI estimate" reference in the main text.
- Compare against a standard motif discovery tool on the TATA-BOX task.
- Add a brief discussion of the magnitude of constants C₁*, C₂ in the error bound for typical settings.

## Removed Points

- **"Theoretical derivation of Equation (2) would imply KL = 0" (reviewer's specific framing).** The reviewer argued that if both p_T and q_T → π then E[log(p_T/q_T)(X_T)] → 0, and since Equation (2) equates this with KL[p₀ ‖ q₀], it would imply KL = 0. While this highlights the issue, the derivation may involve the specific absorbing CTMC construction and the finite-time horizon (T not necessarily large enough for convergence), which the appendix may clarify. I have reframed this as a clarity/justification issue rather than asserting an actual contradiction.

- **"The 'same backbone' claim is not meaningful across method classes" (reviewer's broad framing).** The reviewer claimed that sharing architectural building blocks is "unusual" and that variational MI estimators "typically use much smaller MLP critics." While the concern about architecture-method fit is valid, using the same backbone for all methods is a standard and reasonable practice for controlling architecture effects. I have reframed this to focus on the specific, verifiable issues: (a) pretrained MDLM-SMALL advantages INFO-SEDD specifically, and (b) the lack of compute/parameter reporting.

- **"INFO-SEDD using a large transformer score network while competitors are forced into a similar architecture that is poorly suited" (reviewer's speculation).** The paper explicitly states minimal architectural changes (just initial/final layers). This is standard methodology. The reviewer's claim that the architecture is "poorly suited" is speculative and unsupported by the paper text. Removed.

- **"Abstract claims are too broad about outperforming alternatives"** — I have kept a milder version of this under Minor weaknesses rather than the reviewer's stronger framing.

- **"The error bound is loose for high-dimensional data"** — The reviewer's stronger claim that the bound "could be very loose" is speculative. I kept this as a minor point about missing discussion.

## Novel Insights

The most valuable cross-perspective synthesis from the reviews is the observation that the theoretical derivation and the empirical comparison methodology are in tension: the paper positions INFO-SEDD as a principled, theory-grounded alternative to heuristic embedding-based methods, but the core theoretical step (Equation 2) is not clearly justified in the main text, while the empirical comparisons do not provide the compute/parameter transparency needed to evaluate the method's practical advantages cleanly. Resolving either issue independently would strengthen the paper; resolving both would significantly raise its impact. The reviewers also collectively highlight that the TATA-BOX experiment (Figure 5) is the strongest real-world demonstration, but the lack of baselines on this task limits its probative value — this is an under-exploited opportunity for the authors to make a stronger case.

## Suggestions

1. **Rewrite the derivation in Section 2.2** so that the relationship between KL divergence and the CTMC expectation is either (a) rigorously proven with explicit conditions stated in the main text, or (b) clearly labeled as approximate with the error source characterized. The current presentation asserts exact equalities (Equation 2) that appear inconsistent with standard Markov chain theory, then switches to an approximation (Equation 4) without explaining how the gap is bridged. A single worked example showing the identity for a simple (e.g., two-state) CTMC would help.

2. **Provide a table of parameter counts and training costs** (wall-clock time, GPU-hours, or training steps until convergence) for INFO-SEDD and each competitor across all experiment settings. This is table-stakes for any comparison across method classes with different model sizes.

3. **Clarify the status of the "Empirical MI estimate"** in Figure 1 — specify how it is computed in the main text.

4. **Report Darrin et al. (2024) correlation values** when claiming "comparable correlation" with consistency.

5. **Add a baseline to the TATA-BOX motif discovery experiment** (e.g., the original Umarov & Solovyev method, or a standard tool like MEME) to demonstrate superiority over the status quo.

## Score and Decision

<score>6</score>
<decision>Borderline Accept</decision>