## Summary

This paper identifies three fundamental limitations of static supervised causal learning (SCL)—fragility under distribution shifts, failure in compositional generalization, and a synthetic-to-real performance gap—and proposes a paradigm shift to test-time training (TTT-SCL). The core idea is to dynamically generate, for each test instance, a customized training set via score-based graph search and then train an SCL model on that data. The instantiation, TACTIC, combines a likelihood-based Alignment of Distribution (AD) metric with sparsity constraints in a stochastic refinement procedure. Experiments on synthetic benchmarks, the real-world Sachs dataset, and the pseudo-real SynTREn dataset show that TACTIC substantially outperforms both traditional causal discovery methods and existing SCL approaches.

## Strengths

- **Problem diagnosis is clear and empirically grounded.** Section 3 systematically identifies three limitations of static SCL—distribution shift fragility, compositional generalization failure, and synthetic-to-real gap—with controlled experiments (Fig 2, Table 1). The finding that AVICI achieves 97.8 AUROC on in-distribution synthetic RFF_G but collapses to 62.3 on Sachs (while PC stays consistent) makes a compelling case for the problem. [favorability=14.22]

- **The core idea—test-time generation of customized training data for each SCL test instance—is genuinely novel in the SCL context.** Previous SCL work treats the training set as static; dynamically constructing it per test instance is a new direction that directly targets the identified OOD limitations. [favorability=12.30]

- **Table 4's three-stage analysis cleanly separates the contributions of the search phase and the SCL learning phase.** The progression from seed (82.0 on Linear_U) to highest-scoring graph (80.1) to final SCL output (86.3), and especially the Sachs jump from 66.6 to 78.9, provides direct evidence that the SCL training on generated data adds value beyond the score-based search alone. [favorability=13.14]

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **The experimental comparison with AVICI is asymmetric in computational budget**—AVICI (scm-v0) is a single pre-trained model evaluated zero-shot, while TACTIC trains a new SCL model from scratch per test instance using 200 dynamically generated datasets plus the search phase. The performance results are valid, but the paper does not acknowledge this resource disparity or discuss the computational trade-off. This limits the reader's ability to calibrate the comparison. [favorability=4.03]

- **Key implementation details are deferred to appendices that were stripped by the parser**, but even in the main text the regression function class used for Structure-Induced Mechanism (SIM) and the value/selection method for the sparsity penalty λ are not stated. These are central: the regression class determines what the AD metric measures, and λ controls the entire AD-sparsity trade-off. [favorability=0.60]

- **The compositional generalization evidence is interpreted more strongly than the data supports.** The "Component-mixed" vs. "i.i.d" drops in Fig 2 are 3–11 AUROC points. The paper interprets this as models that "merely memorize training configurations" and "fail to learn modular causal representations," but the drops could partly reflect that certain (graph, mechanism, noise) combinations produce harder learning problems, not a fundamental failure of modular causal learning. [favorability=6.05]

- **The acceptance rule for stochastic graph refinement needs clarification.** The main text says "accepted with probability proportional to its score"; the figure caption gives α = min[1, score(G_{k+1})/score(G_k)]. Since AD is a log-likelihood (typically negative) and the sparsity penalty is subtracted, scores can be negative, making this ratio non-standard as a Metropolis-Hastings criterion. The paper should clarify whether scores are exponentiated or otherwise transformed to define a valid acceptance probability. [favorability=8.24]

- **Sachs and Syntren results in Table 2 are reported without standard deviations or variance estimates**, unlike the synthetic datasets which include standard deviations. Given the stochastic nature of the search, multiple runs with reported variance are needed to assess reliability on these key datasets. [favorability=5.11]

- **The AD metric is presented as a contribution, but equation (3) is a standard average log-likelihood and equation (5) mirrors the canonical form of score-based causal discovery (BIC, GES).** The paper acknowledges this connection (line 248 distinguishes TACTIC from "classical score-based methods" by the two-stage process), but the abstract and introduction frame AD as a "proposed" formulation. A more precise characterization of what is and is not novel would help readers. [favorability=5.50]

### Trivial
None.

## Nice-to-Haves
- Report wall-clock time per test instance to help the community assess practical applicability.
- Include an ablation that removes AD entirely (e.g., random graphs or sparsity-only optimization) to more fully characterize each component's contribution.
- Test robustness to noise distribution mismatch (the training data uses standard Gaussian noise by default).

## Removed Points
- **AD as score-based discovery / novelty overclaiming (original Critical Issue 1):** The paper explicitly states that AD is likelihood-based (line 148: "in the main text we use the implementation based on likelihood") and distinguishes TACTIC from score-based methods by the two-stage process. The claim that the paper "obscures" this relationship is overstated. The remaining concern (imprecise novelty framing) is kept as a minor weakness.
- **"State-of-the-art" overclaiming on specific datasets:** The claim "TACTIC achieves state-of-the-art performance on all other datasets" is technically correct per Table 2 (TACTIC achieves the highest AUROC on Linear_U, Chebyshev_G, Sachs, and Syntren). Modest margins on some datasets do not invalidate the claim.
- **Computational cost as a limiting factor:** The paper references Appendix F for complexity analysis, which is standard practice. The main text adequately points the reader to the appendix.
- **The "three fundamental limitations" overclaiming:** The paper shows these issues across multiple synthetic settings and one real-world dataset, which provides sufficient empirical support for the claim.
- **Missing related works:** Removed per instructions—the reviewer cannot verify what is missing.
- **Formatting/typo nitpicks:** Removed per instructions—these are parser artifacts.

## Novel Insights
None beyond the paper's own contributions. The reviews engage with the paper's claims on their own terms rather than adding new analytical perspectives.

## Suggestions
- Clarify the acceptance rule: specify whether scores are exponentiated or transformed to ensure valid probabilities.
- Report λ values (or selection method) and the regression function class for SIM in the main text.
- Add standard deviations for Sachs and Syntren results.
- Include a brief discussion of computational cost (wall-clock time per test instance) to help readers assess practical applicability.
- Temper the interpretation of the compositional generalization results to acknowledge alternative explanations.

## Score and Decision

**Round 1 — Bracketing:** I retrieved calibration anchors spanning the full score range. Strong reject anchors (scores 0.5–1.4, sim 0.54–0.60) and low-band anchors (scores 3.0–3.4, sim 0.69–0.72) are clearly below this paper's quality. Middle-band anchors (scores 4.0–5.0, sim 0.70–0.74) include "Demystifying amortized causal discovery with transformers" (5.00, Reject)—a purely analytical SCL paper with no new method and only bivariate synthetic results. The reviewed paper is substantially stronger: it proposes a novel method, handles multivariate settings, and validates on real-world data. Upper-middle-band anchors (scores 5.67–6.75, sim 0.71–0.77) include "Zero-Shot Learning of Causal Models" (6.25, Reject), "A Meta-Learning Approach to Bayesian Causal Discovery" (6.00, Accept), and "Out-of-Variable Generalisation" (6.75, Accept). **Round 1 bracket: [5.5, 7.5].**

**Round 2 — Narrowing:** I performed itemized calibration on the three most relevant upper-middle anchors. The 5.00 anchor's weaknesses include "only bivariate cases," "only synthetic data," and "limited scope"—none of which apply to the reviewed paper. The 6.00 anchor (BCNP) has strengths with favorability up to 11.49 but also weaknesses as low as −4.73 (incremental contribution concerns, lack of novelty). The reviewed paper's strengths have higher favorability (12.30–14.22) and its weaknesses are milder (all ≥ 0.60). The 6.25 anchor (Zero-Shot) has strengths up to 15.99 but suffers from strong assumptions and lacks real-world validation—the reviewed paper's real-world Sachs/SynTREn results are a significant advantage. The 6.75 anchor (Out-of-Variable) is a theory paper with proof-of-concept synthetic experiments only. **Final placement:** above the 5.00–6.25 anchors (stronger empirical contribution and real-world validation), comparable to but slightly above the 6.00 anchor (clearer novelty and broader evaluation), and slightly below the 6.75 anchor (which has deeper theoretical contributions). The reviewed paper's weaknesses are uniformly minor and addressable; none threaten the core contribution.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>