## Summary
# Final Review Report

## Summary

This paper develops a theoretical framework for understanding when and why data curation (pruning) improves generalization in high-dimensional binary classification. The authors study two curation rules — label-agnostic (pruning based on feature magnitude/difficulty) and label-aware (pruning based on both label correctness and difficulty) — and derive exact asymptotic test error expressions using random matrix theory. The central result is a phase transition: when the data generator is strong ($\rho \to 1$) and data is abundant, "keep hard" pruning is optimal (the "less is more" regime); when the generator is weak ($\rho < 1$), "keep easy" is optimal. Empirical validation on synthetic Gaussian data confirms the predicted phase transitions, and experiments on ImageNet show a crossover consistent with the theory. The paper also interprets recent LLM reasoning results (LIMO, s1) through its theoretical lens.

**Strengths:** The paper tackles an important and timely question with rigorous asymptotic analysis. The phase transition characterization is clean and interpretable. The connection between generator quality and optimal pruning strategy provides a unifying principle.

**Weaknesses:** (1) The theory is restricted to isotropic Gaussian features with squared-loss binary classification — far from the LLM and ImageNet domains the paper claims to explain. (2) The LLM "validation" (Section 4.2) is entirely post-hoc reinterpretation of published tables without controlled experiments or direct measurement of theoretical quantities. (3) Theorem 1 is not self-contained in the main text, relying on undefined functions deferred to the appendix. (4) The ImageNet experiments conflate generator and pruner quality by using the same model for both roles. (5) The paper's strong claims about "resolving a central paradox" and "bending scaling laws" outpace the evidence provided.

**Novelty verdict:** Due to Retrieval-Disabled Mode (external paper search unavailable), novelty comparisons with prior work cannot be fully verified in this review. Key prior works (Sorscher et al., 2022; Feng et al., 2025; Firdoussi et al., 2024) already study data pruning in related settings. The paper's main theoretical innovation — incorporating difficulty-based pruning alongside label verification and deriving exact phase transitions — appears to extend these prior frameworks, but the extent of overlap requires manual literature verification. The novelty assessment is deferred.

## Strengths
**S1. Timely and important research question.** The paper addresses a central tension in modern ML: when does data curation outperform simply scaling up data? This question has significant practical implications for training efficiency, and the paper's framing around the "less is more" vs. "more is more" tension is well-motivated and current.

**S2. Clean theoretical formulation.** The paper sets up a tractable mathematical model (high-dimensional binary classification with Gaussian features, pruning oracles, squared-loss ridge regression) that admits exact asymptotic analysis via random matrix theory. The three quantities — $\rho$ (generator quality), $\rho_*$ (oracle quality), and $\rho_g$ (generator-oracle alignment) — provide a geometric and interpretable parameterization of the data curation problem.

**S3. Sharp phase transition characterization.** Theorem 2's characterization of the optimal pruning strategy as a function of generator quality ($\rho$) is a genuine theoretical insight: when the generator is excellent, keep-hard refines its capabilities; when it is poor, keep-easy builds foundational skills. This provides a principled explanation for why different curation strategies succeed in different regimes.

**S4. Bridge between theory and experiment on synthetic data.** The synthetic experiments in Section 4.1 (Figure 1) provide clean validation of the theoretical predictions, with a clear match between asymptotic theory curves and finite-sample simulations across four regimes. The bottom-left quadrant (large $n$, high $\rho$) convincingly demonstrates the "less is more" regime predicted by the theory.

**S5. Model collapse mitigation result.** The demonstration that strategic pruning (keep-hard on valid examples) can stabilize iterative pseudo-labeling and prevent performance degradation (Figure 3) is a practically relevant finding with implications for self-training and RLHF pipelines. This is a non-trivial extension of the theory to the iterative setting.

**S6. Honest limitations section.** Unlike many papers that bury assumptions, the conclusion explicitly acknowledges the Gaussian feature model, binary classification, and static oracle limitations. The future directions are concrete and actionable.

## Weaknesses
The weaknesses are ordered by severity and impact on the paper's validity and claims.

### W1. The gap between theoretical assumptions and claimed empirical validation is too wide (Critical)

The paper's theory assumes isotropic Gaussian features, binary labels generated by a linear classifier, squared L2 loss, ridge regression, and a single static pruning oracle. Yet the paper claims to "validate" this theory on ImageNet (multi-class natural images, deep neural networks, cross-entropy loss, SGD optimization) and LLM reasoning (autoregressive transformers, next-token prediction, RLHF training pipelines). The link is entirely qualitative: the theory predicts a crossover between keep-easy and keep-hard as generator quality improves, and the ImageNet experiments show a similar crossover. However:

- The ImageNet experiments use a pre-trained ViT as **both** the generator ($w_g$) and the pruner ($w_o$), violating the theoretical assumption that these are distinct vectors with independent quality parameters ($\rho$ and $\rho_*$). When both roles are filled by the same model, $\rho_g = 1$ (perfect alignment) and $\rho_*$ is maximally coupled to $\rho$, so the theory's independent variation of these parameters is not tested.
- The LLM "validation" (Section 4.2) contains no experiments by this paper. It reproduces two tables from other papers and assigns post-hoc labels ("strong generator" vs. "weak generator") to match the observed patterns. The key theoretical quantity $\rho$ is never measured or estimated. This is not scientific validation.

**Required fix:** Either (a) run controlled experiments where $\rho$, $\rho_*$, and $\rho_g$ are directly manipulated and measured in settings closer to the theoretical assumptions, or (b) substantially downgrade the claim from "validation" to "qualitative interpretation" throughout the paper, including the abstract.

### W2. Theorem 1 is not self-contained in the main text (Major)

Theorem 1's test error formula depends on functions $m$, $\tilde{m}$, and $r$, which are described only as "explicitly determined by the constants in Eqn (8)" and "$m$ is the Stieltjes transform of a Marchenko-Pastur law, 'deformed' by pruning." These functions are never given in closed form in the main text. Additionally, the constant $\gamma$ defined in Eq. (8) does not appear in the subsequent expressions for $m_0$ and $\nu_0$ — its role is unclear. A reader cannot verify, apply, or build upon Theorem 1 without consulting the appendix (which is not provided in the reviewable manuscript).

**Required fix:** Provide explicit closed-form expressions for $m$, $\tilde{m}$, $r$ in the main text (or in a concise appendix summary within the main paper). Clarify the role of $\gamma$. Consider providing the simplified data-rich limit ($\phi \to 0$, $\lambda \to 0$) as a corollary — this would give readers immediate intuition.

### W3. Synthetic experiment details are critically underspecified (Major)

The synthetic validation (Section 4.1, Figure 1) is described at a high level without sufficient detail for reproducibility:
- No values are given for $\rho$ in the "poor generator" regime (only $\rho < 1$)
- The random pruning baseline uses $\rho_* = \rho_g = 0$, meaning the pruner is orthogonal to both ground truth and generator — an extreme and unmotivated choice
- It is unclear whether the theoretical curves are computed from Theorem 1, Theorem 2, or a different formula
- The empirical "dashed lines" come from finite-$d$ simulations, but the values of $d$, $\phi$, number of trials, and error bar computation method are not stated

**Required fix:** Add a dedicated experimental setup subsection with a table of all simulation parameters: $d$, $n$, $\phi$, $\lambda$, $\rho$, $\rho_*$, $\rho_g$, $\alpha$ (threshold), number of trials, and procedure for computing theoretical vs. empirical curves.

### W4. Squared loss for binary classification is non-standard and unanalyzed (Minor)

The paper uses squared L2 loss $\ell(z; y) = (z-y)^2/2$ for binary classification with $y \in \{-1, 1\}$. The minimizer of this loss under Gaussian features has known properties (it recovers the Bayes classifier up to scaling under certain conditions), but this connection is not discussed. Logistic loss or hinge loss are standard for classification. The paper does not address whether the theoretical results are expected to transfer to other loss functions, or whether the phase transition boundaries depend on the choice of loss.

**Required fix:** Either justify the squared loss choice (cite relevant Gaussian equivalence results) or discuss the expected sensitivity of results to the loss function.

### W5. Post-hoc LLM interpretation is presented as a "principled explanation" (Major)

Section 4.2 presents a narrative where the base LLM is a "strong generator" for average AIME problems and a "weak generator" for hard AIME problems. The theory then "correctly predicts" the observed patterns. However, this is a circular argument: the classification into strong/weak is made after seeing the data to match the desired prediction. The theory is not tested — it is used as a labeling scheme. The section title says "Reconciling Recent Findings," which is an appropriate framing, but the abstract and introduction claim "principled explanation" and "validation," which overstates the evidence.

**Required fix:** Reframe this section as "Qualitative Interpretation" or "Connections to Existing Results." Add a caveat that the theoretical quantities are not directly measured. Remove claims of "predictive validation" in favor of "consistent with."

### W6. Related work is organized as a literature list rather than by comparison axes (Minor)

The Related Work section (Section 5) reads as a chronological narrative rather than a structured comparison. The paper does not clearly differentiate its contributions from the most closely related theoretical works (Feng et al., 2025; Firdoussi et al., 2024), which already analyze label-verification oracles in high-dimensional linear models. The section would be more effective if organized around axes such as: (i) theoretical frameworks for data pruning, (ii) label verification vs. difficulty-based selection, (iii) model collapse mitigation strategies.

**Required fix:** Restructure Related Work around 2-3 comparison axes. In each paragraph, explicitly state: what prior work does, what limitation it leaves open, and how this paper addresses it.

### W7. Pruning ratio $p$ is defined but its relationship to the threshold $\alpha$ is not discussed (Minor)

The pruning ratio $p = \mathbb{E}[q(G)]$ depends on the threshold $\alpha$ (for keep-hard: $q(t) = 1[|t| \leq \alpha]$). The relationship $p = \mathbb{P}(|G| \leq \alpha) = 2\Phi(\alpha) - 1$ for Gaussian $G \sim \mathcal{N}(0,1)$ is straightforward but not stated. Theorem 2 fixes $p$ and optimizes over $q$, but in practice one chooses $\alpha$ (the difficulty threshold) — translating between $p$ and $\alpha$ would help practitioners apply the theory.

**Required fix:** Add a brief note connecting $p$ to $\alpha$ for the keep-hard and keep-easy strategies (e.g., for isotropic Gaussian: $p = \mathbb{P}(|G| \leq \alpha) = 2\Phi(\alpha) - 1$).

### W8. Model collapse experiment lacks proper controls (Minor)

The model collapse experiment (Figure 3) compares "training on all data" vs. "training on hard valid examples." The "hard valid" condition selects only hard examples with correct labels. This combines three interventions: (a) reduced dataset size, (b) difficulty-based selection, and (c) label-verification filtering. A control condition using random subsets of the same size with label verification would isolate the effect of "hard" selection from the effect of data quantity and correctness filtering.

**Required fix:** Add a random-subsample baseline of the matched size (with label verification) to the model collapse experiment, enabling attribution of the stabilization effect to the difficulty-based selection rather than simply to reduced data volume or correctness filtering.

## Score
**Final Score: 5.5/10**

**Scoring rationale:**

- **Research value (6/10):** The paper addresses an important and timely question. The phase transition characterization (Theorem 2) provides a clean theoretical insight that can guide intuition about data curation. However, the restrictive assumptions (isotropic Gaussian, squared loss, binary classification, static oracle) limit the practical scope of the findings. The claimed connections to LLM and ImageNet domains are qualitatively suggestive but not rigorously validated, reducing the effective research contribution.

- **Novelty (5/10 — deferred, tentative):** External literature verification is unavailable in this run, so novelty cannot be conclusively assessed. Based on manuscript-grounded reasoning, the paper extends prior theoretical frameworks (Sorscher et al., 2022; Feng et al., 2025; Firdoussi et al., 2024) by incorporating difficulty-based pruning alongside label verification and deriving exact phase transition boundaries. This appears to be a meaningful but incremental extension rather than a breakthrough. The theoretical machinery (random matrix theory, Marchenko-Pastur law) follows established techniques. *Final novelty determination requires manual literature comparison.*

- **Validity/Soundness (5/10):** The mathematical derivations appear sound within their stated assumptions (isotropic Gaussian, squared loss, proportional asymptotics). However, Theorem 1 is not self-contained in the main text, and the synthetic experiment details are critically underspecified. The empirical "validations" on ImageNet and LLM reasoning do not meet the scientific standard of testing theoretical predictions — the ImageNet experiments conflate generator and pruner roles, and the LLM section is purely post-hoc interpretation.

- **Reproducibility (4/10):** The theory cannot be reproduced from the main text alone (critical functions $m$, $\tilde{m}$, $r$ are deferred). The synthetic experiments lack sufficient parameter details. The ImageNet experiments use unspecified training configurations (architecture, optimizer, hyperparameters, data splits).

- **Presentation (7/10):** The paper is generally well-written and the narrative is clear. The main weakness in presentation is the gap between the strength of claims (especially in the abstract) and the evidence provided. The related work section could be more structured.

**Summary:** The paper develops a clean theoretical framework with a genuine insight (phase transition in optimal pruning strategy as a function of generator quality). The synthetic validation is promising. However, the paper substantially overclaims the empirical support, with the LLM "validation" being particularly weak (post-hoc interpretation without controlled experiments). The ImageNet experiments have confounds. The main text defers critical theoretical details to the appendix. The score reflects the gap between the theoretical ambition and the empirical delivery. A revised version that honestly bounds its claims and adds controlled experiments could merit a higher score.

**Post-Revision Target:** [6.5, 7.5]/10 — contingent on: (a) reframing of empirical claims throughout, (b) adding controlled experiments that directly test theoretical predictions, (c) making Theorem 1 self-contained, (d) adding proper controls to the model collapse experiment, (e) restructuring the LLM section as qualitative interpretation rather than validation.