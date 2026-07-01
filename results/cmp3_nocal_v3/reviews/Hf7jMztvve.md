## Summary

The paper presents two complementary investigations into LLM deception: (1) the Secret Agenda testbed, a social-deduction game that elicits incentive-driven lying across 38 models, and (2) an insider-trading compliance analysis using SAE activations. The central claim is that auto-labeled SAE features for deception fail to activate or steer during strategic dishonesty, while aggregate unlabeled activations show discriminative structure in a compliance domain. The authors present this as preliminary evidence motivating further study.

## Strengths

1. **The Secret Agenda testbed is a clean, reproducible experimental design.** Section 5.1 describes a synthetic transcript that places the LLM at a critical binary decision point (Round 6, already Fascist Leader, with a "no lying" law that has no enforcement mechanism), isolating the moment where incentive pressure favors dishonesty. The prompt variants (Snails vs Slugs, Truthers vs Liars, Day vs Night) test robustness to framing and deconfound the result from political associations in the role names. As a behavioral probe, this is a useful community resource.

2. **The research question is well-motivated and timely.** The paper asks whether auto-labeled SAE features—widely used in interpretability tooling—actually activate during strategic deception and whether they can causally control such behavior. This directly addresses open questions raised in the GemmaScope documentation about whether SAE features "really find the 'true' concepts in a model."

3. **The limitations are spelled out thoroughly.** Section 8 candidly discusses small sample sizes (n=2–30), resource constraints, the game-framing trade-off, the asymmetric analysis depth, and the preliminary nature of the findings. This candor sets appropriate expectations, even though it also means the paper's own claims are self-acknowledged as preliminary.

## Weaknesses

### Fatal

None.

### Major

1. **The methodology for classifying Secret Agenda responses as "truth" / "partial lie" / "lie" is not specified, yet the entire analysis depends on this classification.** The paper reports aggregate counts (e.g., Anthropic-Claude: 4 truth, 25 lie) in Figure 1 and mentions "manual analysis (~160 examples)" in Section 8.3 for the SAE activation check. But it never states: who classified the responses (human raters? an LLM judge? the authors?), how many annotators were involved, what annotation instructions were used, or what inter-rater agreement was achieved. For the remaining responses beyond the ~160 manually inspected ones, it is unclear how they were classified. This is a fundamental methodological gap because the behavioral ground truth is the linchpin of both the "38/38 models lied" finding and the SAE activation analysis.

2. **The Secret Agenda testbed does not cleanly separate role-play instruction-following from the kind of strategic deception relevant to AI safety.** The game prompt tells the model it is the Fascist Leader, describes a "no lying" law with no enforcement, and notes that lying is the optimal path to winning. The model is acting as a character in a game where deception is the correct play. The AI safety literature (Wei et al., 2023; Greenblatt et al., 2024; Scheurer et al., 2024) uses "strategic deception" to describe scenarios where models deceive *in pursuit of objectives they were trained to pursue*—not where they follow instructions to role-play a deceiving character. The paper's operational definition (Section 2) is behavioral and sidesteps intentionality, which is defensible, but the paper's narrative framing ("strategic deception," "scheming") invokes the safety literature's more loaded meaning. A control condition (e.g., the same scenario without the role-play framing) would be needed to distinguish genuine strategic deception from instructed role-play lying. The paper's own acknowledgment in Section 8.2 ("trades naturalism for reproducibility") does not resolve this gap.

3. **The activation analysis (Section 6.1) lacks systematic quantification, making the claim that "auto-labeled deception features fail activation tests" impossible to evaluate rigorously.** The paper reports manual inspection of ~160 examples and states that "most expected deception-related features did not activate. Only feature 5665 (secrecy in interactions) reliably activated." But no quantitative evidence is provided: no table of activation rates per feature per model, no threshold for what counts as "activated," no confusion matrix, no baseline comparison (e.g., activation levels on non-deceptive vs. deceptive text from the same models), and no systematic listing of which features were checked across which models. The four feature IDs named (14971, 1741, 6442, 10248) are introduced as examples ("such as"), but the text does not clarify whether these were the only features examined or a representative sample. For a venue like ICLR, such qualitative evidence is insufficient for a claim about feature non-activation across models.

4. **The steering experiments (Section 6.3) are described anecdotally without the experimental controls needed to support the "100+ features" claim.** The abstract states that "feature steering experiments across 100+ deception-related features failed to prevent lying," but the body provides no trial counts, no tabulation of which features were tested, no measurement of how "steered to -1" affected actual activation values, no blind evaluation of outputs, and no statistical analysis. The "bananas and banana-related concepts" comparison is offered as a single anecdotal contrast. The paper references supplementary materials (screenshots, parameter settings), but the main text should stand on its own for a quantitative claim of this weight. The lack of systematic experimental reporting means the reader cannot assess the reliability of the steering findings.

5. **The t-SNE analysis for Insider Trading (Figure 4) depends on visual inspection without any quantitative validation of cluster quality.** t-SNE is known to produce visually separable clusters even from random high-dimensional data (Wattenberg et al., 2016). The paper reports no silhouette scores, classification accuracy of a probe trained on the latent space, adjusted Rand index, or statistical test of separation. The claim that "aggregate unlabeled activations provide discriminative signal for compliance detection" therefore rests entirely on eye-balling 2D projections. While the heatmaps in Figure 5 provide complementary evidence, the lack of quantitative validation weakens what is presented as a key positive result.

### Minor

1. **Prompt variation results are incompletely reported.** Section 5.3 gives a specific quantitative result only for the Snails vs Slugs variant (6/6 models). The Truthers vs Liars, Day vs Night, Pink vs Turquoise, and Shortened variants are described qualitatively ("we continued to observe the strategic deception") with no reported counts. This limits the reader's ability to assess the robustness claims.

2. **The threshold for "reliably activated" (feature 5665) is not defined.** Section 6.1 states feature 5665 "reliably activated" without specifying what activation magnitude or frequency constitutes reliability, or whether this was measured against a baseline of non-deceptive text from the same model.

3. **The 4-bit quantization of the Llama 70B model used in the Insider Trading analysis is noted but its potential effects on SAE analysis are not discussed.** Section 7.1 specifies the use of "Unsloth's quantized 70B Llama (bnb-4bit)." Quantization at this level can alter model behavior and internal representations, and the SAE was presumably trained on full-precision activations. This is a potential confound that goes unaddressed.

4. **The paper's two analyses are not symmetric, which limits the interpretability of the central contrast.** The Secret Agenda analysis tests auto-labeled features manually on ~160 examples; the Insider Trading analysis uses aggregate (labeled and unlabeled) activations on 149 regex-classifiable responses with PCA+t-SNE. The paper acknowledges this asymmetry in Section 8.3, but the contrast between "auto-labeled features fail" and "unlabeled activations work" remains confounded by domain (adversarial game vs. structured compliance), analysis method (manual inspection vs. automated dimensionality reduction), and feature type (pre-selected labeled vs. aggregate unlabeled). The paper does test auto-labeled features on insider trading examples in a limited way (Section 6.1: "select examples of insider trading from Scheurer et al. (2024) were also dormant"), but this is not a systematic symmetric analysis.

### Trivial

None.

## Nice-to-Haves

- **Systematic activation quantification for Secret Agenda:** Report mean activation rates with standard deviations for deception-related SAE features across all models/trials, with baseline comparisons to non-deceptive text from the same models. Include a confusion-matrix-style table.
- **Controlled steering experiments with blind evaluation:** Report, e.g., 10 trials per feature per steering direction, with outputs evaluated by a blind rater, and report the proportion of lies vs. truths.
- **Quantitative validation of t-SNE clusters:** Report silhouette scores or linear-probe classification accuracy with confidence intervals for the Insider Trading analysis.
- **Symmetric auto-labeled feature analysis on Insider Trading:** Systematically test whether deception-related auto-labeled features activate on insider trading engagement vs. refusal responses, matching the Secret Agenda methodology.

## Removed Points

These points from the input review were removed with justification:

- *"The discriminative features themselves have labels that make domain sense, which actually suggests the labeled features are doing reasonable work in this domain. The paper never cleanly tests whether unlabeled features outperform labeled ones for the discrimination task."* — Removed because the paper analyzes both labeled (8B) and unlabeled (70B) features for Insider Trading (Section 7.1) and presents visualizations for both. The claim "unlabeled activations provide discriminative signal" does not assert that unlabeled features outperform labeled ones — it is a separate claim. This criticism attacks a claim the paper never makes.

- *"Prior work already shows lying can be prompted (Chern et al., 2024; Hagendorff, 2024; Ward et al., 2023). The contribution of the behavioral benchmark should be the testbed design, not the discovery that lying can be elicited."* — Partially removed because the paper itself states in Section 1.1 that its contribution is methodological ("a complementary behavioral benchmark with different tradeoffs"), not the discovery of deceptive capability. The criticism about thin sample sizes (n=2 for some models) is retained as part of Major Weakness 1 (classification methodology), but the "already known" framing is dropped since the paper does not claim first discovery.

- *"Only one variant (Snails vs Slugs) gets a quantitative result... This makes it impossible to assess whether the robustness claims are actually supported."* — Retained but demoted to Minor Weakness 1, since the incomplete reporting is a real gap but does not threaten the core claim.

- *"The insider trading analysis would benefit from a quantitative validation of the t-SNE clusters"* and *"strengthening the paper"* suggestions — Moved to Nice-to-Haves.

- *"The paper reads like a preliminary report or workshop paper"* — This is an overall assessment, not a specific weakness. The specific evidential gaps are captured in the weaknesses above.

- *"100+ features claim not matched by evidence"* — Retained in Major Weakness 4 with proper context: the supplementary materials are referenced (Section 9, DeLeeuw, 2024) but the main text lacks supporting tabular evidence.

- *"The paper does not report which models are which sizes"* — The paper reports family-level totals in Figure 1 and notes sample sizes n=2–30 in the caption. Per-model breakdown would be better but is not a critical omission. This is subsumed under the broader point about limited quantification.

## Novel Insights

None beyond the paper's own contributions. The input review raises a genuinely insightful framing point (Weakness 2) about the gap between the paper's behavioral definition of "strategic deception" and the stronger notion used in the AI safety literature, but this is a critique of framing/scope rather than a novel positive insight about the paper's subject matter.

## Suggestions

1. **Clarify the response classification methodology.** Specify who classified Secret Agenda responses, how many annotators, what instructions were given, and what inter-rater agreement was achieved. If possible, release the annotated dataset.

2. **Add a control condition** to the Secret Agenda testbed that maintains the same incentive structure but removes the explicit role-play framing (e.g., a scenario where the model's training objective is to be helpful and honest, and deception would violate that objective without being instructed).

3. **Quantify the activation analysis.** Report activation rates with thresholds, confusion matrices, and per-model-per-feature statistics for the GemmaScope analysis. If manual annotation is the only option, report kappa scores and error bars.

4. **Document steering experiments systematically.** Provide a table enumerating the 100+ features tested, the number of trials per feature, the steering settings used, and the outcomes (lie vs. truth per trial).

5. **Quantify t-SNE cluster separation** with silhouette scores, a trained linear probe with held-out accuracy, or a permutation test against random labels.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>