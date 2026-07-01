## Summary

This paper identifies a critical safety vulnerability in Masked Diffusion Language Models (MDLMs) termed the *priming vulnerability*: if an affirmative token for a harmful query appears at an intermediate denoising step, subsequent generation can be steered toward a harmful response even in aligned models. The authors systematically characterize this vulnerability, show it can be exploited without explicit intervention (via a novel First-Step GCG attack grounded in a theoretical lower bound), and propose *Recovery Alignment* (RA), a training method that teaches models to generate safe responses from adversarially contaminated intermediate states. Experiments across three MDLMs and multiple benchmarks demonstrate RA significantly mitigates the vulnerability and improves robustness against conventional jailbreak attacks with minimal degradation in general capability.

## Strengths

- **Novel and timely problem identification.** The paper reveals a previously unexplored vulnerability specific to the MDLM inference mechanism, which is important as these models gain adoption. The distinction between priming (intermediate-state contamination) and prefilling attacks on ARMs is clearly drawn.
- **Rigorous characterization.** The anchoring attack provides a clean, controlled way to quantify the vulnerability, and the results show even a single affirmative token at the first step significantly increases ASR. Figure 2 vividly demonstrates the severity.
- **Theoretical contribution with practical impact.** Theorem 4.1 provides a tractable lower bound on the attack objective, enabling First-Step GCG. This is both theoretically sound (with empirical validation of the monotonicity assumption in Appendix C.2) and practically effective, achieving ~20× speedup and up to 4× higher ASR over Monte Carlo GCG.
- **Effective and principled mitigation.** Recovery Alignment directly addresses the root cause—training-inference mismatch on intermediate states—rather than applying ARM-based defenses post-hoc. The linear curriculum on intervention steps is a sensible training strategy. Empirical results in Tables 2 and 3 show RA consistently outperforms SFT, DPO, and MOSA across all three models and multiple attack types.
- **Comprehensive evaluation.** The paper evaluates robustness against two threat models (intervention-based and optimization-based attacks), conversational jailbreak attacks (PAIR, ReNeLLM, Crescendo), and general capability on 11 benchmarks. Ablations on the max intervention step and scheduling strategy (Figure 3) provide useful insights.
- **Clear exposition.** The paper is well-structured, with a clear problem statement, method description, and experimental setup. Figures effectively illustrate the vulnerability and the proposed solution.

## Weaknesses

### Fatal
None.

### Major
- **Dependence on reward model quality.** RA uses DeBERTaV3 as a reward model. The performance of RA is inherently tied to the accuracy and fairness of this reward model. Biases in the reward model (e.g., over-refusal, over-optimization) could lead to unintended degradation in helpfulness or reduced robustness. The paper does not analyze sensitivity to the choice of reward model or its failure modes.
- **Monotonicity assumption remains partially unverified.** While Appendix C.2 provides empirical evidence that the assumption holds across models, the assumption itself is not proven theoretically and could be model-dependent. A failure mode where the assumption is violated could affect the validity of First-Step GCG as a surrogate objective, though the empirical results are strong.

### Minor
- **Generalizability beyond the studied models.** Only three MDLMs are evaluated (two LLaDA variants and MMaDA), all at similar scales (approx 2B-7B). It is unclear how the priming vulnerability manifests in larger MDLMs or those with different architectures/training recipes. The paper acknowledges this limitation only implicitly.
- **Comparison with concurrent defenses.** The paper compares against MOSA, which is a DLM-specific alignment method, but other concurrent defenses (e.g., those by Zhang et al. 2025, Wen et al. 2025) are mentioned only as attacks. Including a defense baseline from those works would strengthen the evaluation, though this may be infeasible due to timing.

### Trivial
None.

## Nice-to-Haves

- Exploring a DPO-style supervised variant of RA would be valuable, as the paper notes this could reduce training cost. The authors acknowledge this as a limitation, but a preliminary experiment (even on a subset) would strengthen the paper.
- Analysis of RA's behavior under distributional shift in harmful queries (e.g., queries not in the BeaverTails distribution) would test generalization of the learned recovery capability.
- Discussion of potential negative societal impacts of RA (e.g., increased censorship or over-refusal) beyond general capability metrics would be a useful addition.

## Novel Insights

Beyond the paper's own contributions, a broader insight emerges: the safety failure in MDLMs originates from a *training-inference mismatch*—the model is trained only on fully-masked initial states but during inference encounters intermediate states containing affirmative tokens. This mismatch is a fundamental property of the iterative denoising process, not an artifact of a particular architecture. Recovery Alignment's curriculum approach—progressively exposing the model to more contaminated states—suggests a general principle for robustifying iterative generative models: explicitly train on the distribution of states that will be encountered during attack scenarios. This principle may extend beyond MDLMs to other iterative refinement models (e.g., diffusion-based image editors, iterative LLM refinement).

## Suggestions

- **Reproducibility and sensitivity.** Provide full training hyperparameters, reward model details, and random seeds in the final version. Consider releasing the code and trained models.
- **Failure mode analysis.** Include a qualitative analysis of cases where RA still fails (e.g., ASR > 0 at large intervention steps). Understanding these failures could guide future improvements.
- **Clarify linear schedule specifics.** In Algorithm 1, `t_min` and `t_max` should be explicitly defined (likely time steps, not fractions). The current text says "range [t_min, t_max]" but uses values like 2, 4, 8 in Figure 3a—these appear to be time steps (out of T=128). Clarify.

## Score and Decision

The paper makes a significant contribution by identifying a novel and severe vulnerability in an emerging class of language models, providing a principled mitigation, and supporting claims with thorough experiments. The weaknesses are primarily about scope and assumptions, none of which invalidate the core contributions. The work is original, timely, and practically relevant.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>