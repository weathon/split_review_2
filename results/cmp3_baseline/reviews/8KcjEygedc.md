## Summary

This paper develops a theoretical framework for data curation in high-dimensional binary classification, deriving exact scaling laws for test error under label-agnostic and label-aware pruning rules. The theory characterizes sharp phase transitions where “less is more” (aggressive pruning of hard examples) outperforms full-data training, conditioned on generator quality, oracle quality, and data abundance. The predictions are validated on synthetic data and ImageNet, and used to explain recent contradictory results in LLM mathematical reasoning (LIMO, s1).

## Strengths

- **Timely and well-motivated question.** The paper directly addresses a central empirical paradox in modern ML—when curated small datasets beat large ones—and provides a principled theoretical resolution.
- **Rigorous theoretical framework.** The analysis uses random matrix theory to obtain exact asymptotic test error under pruning. The results (Theorem 1–3) are clearly stated and the dependence on key parameters (ρ, ρ*, ρ_g) is interpretable.
- **Clear phase transition structure.** Theorem 2 provides analytically precise conditions under which “keep hard” vs. “keep easy” is optimal, tying the optimal strategy to generator quality and oracle quality.
- **Empirical validation on ImageNet with model collapse experiments.** The paper goes beyond synthetic data to show that the theoretical predictions hold in a realistic vision setting, and that strategic pruning can prevent degradation in iterative self-training loops.
- **Unifying lens for recent LLM results.** The explanation of why LIMO/s1 (less is more for average performance) and “more is more” for hard subsets is consistent with the theory—this is a novel synthesis.

## Weaknesses

### Fatal
None.

### Major
- **Empirical validation is limited in scope.** The ImageNet experiments use a single pre-trained model (presumably ViT from MMPreTrain) as both generator and pruner, controlling generator quality only by the amount of initial training data. This is a reasonable proxy, but the paper would benefit from testing across multiple architectures, different corruption types (e.g., noisy labels), and comparison with alternative curation baselines (e.g., uncertainty sampling, CLIP scores).
- **The LLM portion is purely post-hoc interpretation—no new experiments.** While the explanation is plausible, the paper does not directly test its predictions on LLMs (e.g., by varying generator strength in a controlled way). For a paper that claims to bridge theory and practice, this weakens the support.
- **Assumed model is very limited.** The theory assumes isotropic Gaussian features, binary classification, linear model with squared loss, and a specific high-dimensional asymptotic limit. Many real-world settings violate these assumptions (structured data, multi-class, non-linear predictors, multi-epoch training). The paper acknowledges this, but the gap between theory and practice remains substantial.

### Minor
- **Notation is dense and some quantities are defined only in the appendix.** For example, the functions m, \tilde{m}, r in Theorem 1 are not given explicit expressions in the main text, making it hard to assess the result without reading the appendix.
- **The definition of generator “strength” (ρ) conflates label shift with performance on a particular task slice.** In the LLM interpretation, the claim that the model is a strong generator for “average” problems but weak for “hard” problems relies on unverified assumptions about alignment with the ground truth for those slices.
- **The model collapse experiment (Figure 3) only shows one pruning strategy (keep hard) versus full data.** It would be informative to compare with random pruning or keep easy to see if the benefit is specific to the theory-predicted strategy.

### Trivial
None.

## Nice-to-Haves

- Including a simple baseline method (e.g., random pruning of the same size) more systematically in the ImageNet experiments to isolate the advantage of the direction-aware pruning.
- Providing closed-form expressions for the constants (p, γ, β, \tilde{β}) for the common “keep hard” and “keep easy” threshold rules, so that readers can directly plug in numbers.
- Discussing the computational overhead of obtaining oracle predictions for pruning.

## Novel Insights

The paper’s core insight—that data curation should be viewed as a function of generator quality (ρ) rather than a one-size-fits-all heuristic—is genuine and important. The phase transition where “less is more” emerges only at the intersection of a strong generator and abundant data is non-obvious and provides a clean explanation for why recent aggressive curation methods succeed in specific settings. The extension to label-aware curation and the demonstration that pruning can prevent model collapse (by filtering out low-quality synthetic labels) add significant depth beyond prior works like Sorscher et al.

## Suggestions

- Strengthen the empirical section by including at least one additional dataset (e.g., CIFAR-10/100 with a controlled label shift) and comparing against random and uncertainty-based pruning baselines.
- Provide a direct, small-scale LLM experiment (e.g., fine-tuning a small transformer on a reasoning task with a ground-truth verifier) to test the predicted transition from “keep easy” to “keep hard” as generator quality increases.
- Clarify in the main text how the Stieltjes transform m and related functions are computed for a given pruning rule, perhaps with a concrete example.

## Score and Decision

**Score: 8** — The paper presents a novel, rigorous theoretical framework for a timely problem, with careful mathematical analysis and encouraging empirical support. The limitations in scope and validation do not undermine the core contribution, which is both original and practically informative. The work is likely to influence future data-centric research and practice.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>