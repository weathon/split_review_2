## Summary

This paper presents the first large-scale systematic study (400k+ GPU-hours) of scaling reinforcement learning for LLMs, introducing a sigmoidal compute-performance scaling law that enables predictive extrapolation. Through extensive ablations, the authors characterize design choices (off-policy setup, loss type, precision, aggregation, normalization, filtering, curriculum) by their asymptotic performance \(A\) and compute efficiency \(B\). They consolidate the best choices into a recipe, SCALERL, and validate its predictable scaling on a 100,000 GPU-hour run across multiple axes (model size, batch size, generation length, multi-task training), while also demonstrating that SCALERL outperforms existing recipes like DeepSeek GRPO, DAPO, Magistral, and MiniMax.

## Strengths

- **Novel predictive framework for RL scaling**: The sigmoidal law (Equation 1) is a clean, practical tool that enables extrapolation from smaller runs to much larger compute budgets. This fills a critical gap in the RL-for-LLMs literature, which has lacked scaling methodology comparable to pre-training.
- **Massive and methodical empirical study**: With over 400k GPU-hours, the paper is among the most extensive ablations of RL design choices in the LLM setting. The leave-one-out experiments at 16k GPU-hours per run provide strong causal evidence for each component’s contribution.
- **Practical, well-validated recipe**: SCALERL is not only shown to scale predictably to 100k GPU-hours but also achieves higher asymptotic performance and compute efficiency than several widely used recipes. The cross-recipe comparison (Figure 2) is particularly informative.
- **Breadth of scaling axes**: The paper demonstrates predictable scaling along model size, batch size, generation length, and multi-task training, which strengthens the claim that the framework generalizes.
- **Clarity and structure**: The paper is well-motivated, the scaling curves are consistently interpreted through parameters \(A\) and \(B\), and the “bitter lesson” observation (methods that look good at small scale may be worse at large scale) is an important takeaway for practitioners.

## Weaknesses

### Fatal
None.

### Major

- **Lack of full reproducibility details**: The base 8B dense model used in the main experiments is not explicitly named in the main text (e.g., architecture, pre-training data, availability). While the appendix may provide details, a responsible scaling study should clearly identify the model. Similarly, the “Polaris-53k” dataset is only referenced without description in the main text, making it difficult for readers to assess the training distribution.
- **Limited theoretical justification for the sigmoidal law**: The paper relies on empirical stability of the sigmoidal fit over power-law alternatives, but provides no theoretical grounding (e.g., connection to bounded performance, learning dynamics, or capacity). A brief theoretical argument or citation to related saturating-effect models would strengthen the claim that the form is more than a convenient fit.

### Minor

- **Overreliance on in-distribution validation pass rate**: While this is standard in scaling studies, the paper’s primary conclusions about asymptotic performance and efficiency are drawn from held-out training-set prompts. The generalization to truly out-of-distribution tasks (e.g., AIME-24 in Figure 1) is reported but not systematically integrated into the scaling framework. A more thorough study of how the scaling parameters transfer between validation and downstream tasks would be valuable.
- **Leave-one-out differences are modest**: The LOO experiments show SCALERL has slightly higher efficiency (\(B\)) than variants, but the differences are small (e.g., B=2.01 vs. 1.62–1.97). The paper acknowledges this by re-fitting with fixed \(A\), but the practical significance of these efficiency gains at large compute scales is not quantified.
- **Comparison set could be broader**: While the paper compares with four prominent recipes, there are many more variants (e.g., PPO with KL, Reinforce-based methods, different clipping strategies). The scope is pragmatic given compute, but the “state-of-the-art” claim is qualified.

### Trivial

- The paper uses “pass rate (log scale)” in figures, but the y-axis is labelled “R (pass-rate, log scale)” – this is consistent but could be clearer if the metric (mean@16) were annotated directly.
- The SCALERL loss equation uses the stop-gradient function (sg) but does not explicitly state that \(\epsilon\) is a hyperparameter (likely from truncation); a brief note in the main text would help.

## Nice-to-Haves

- Provide explicit training compute (in FLOPs or token count) alongside GPU hours to make the framework hardware-agnostic. GPU hours are useful but not portable across accelerators.
- Include uncertainty estimates (e.g., confidence intervals) for fitted parameters \(A, B, C_{\text{mid}}\) to quantify the reliability of extrapolations.
- Release the full training logs and configuration files for SCALERL to enable exact reproduction.

## Novel Insights

Beyond the paper’s own contributions, a genuinely novel insight is that **asymptotic performance (\(A\)) in RL scaling is not universal** – it can be shifted by choices that are often considered secondary (e.g., loss type, logit precision). This contrasts with pre-training where architectural choices affect the exponent but not the “data-limited” ceiling. The observation that many interventions adjust only efficiency (\(B\)) while leaving \(A\) unchanged suggests a hierarchy of design decisions: a few choices determine the eventual ceiling, while the rest affect how quickly you approach it. This could guide future researchers to focus their compute on identifying ceiling-raising interventions.

## Suggestions

- Explicitly name the base 8B dense model and provide a link to its weights in the camera-ready version. Similarly, include a brief description of the Polaris-53k dataset in the main text.
- Consider adding a figure that shows how the extrapolation error (predicted vs. observed at 100k GPU hours) behaves as a function of the fitting horizon (i.e., how much early compute is needed for reliable extrapolation). This would strengthen the practical utility of the framework.
- Add a brief discussion on the conditions under which the sigmoidal fit may break (e.g., if training becomes unstable, or if the validation distribution shifts). Acknowledging limitations would improve scientific rigor.

## Score and Decision

**Score**: 8 (accept)

**Decision**: Accept

This is a strong paper that makes a significant, timely contribution to the RL-for-LLMs community. The predictive scaling framework is novel and practically useful, the empirical scale is impressive, and the resulting recipe performs well. The weaknesses (limited reproducibility details and theoretical grounding) are minor relative to the contribution’s value and can be addressed in the camera-ready version.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>