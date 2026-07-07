## Summary

This paper introduces IterRef, a test-time scaling method for discrete diffusion models that performs reward-guided iterative refinement via Multiple-Try Metropolis (MTM). The key technical contribution is tailoring both the MTM transition kernel (as a noising-denoising process) and the balancing function so that importance weights become uniform and the acceptance ratio reduces to a simple reward comparison — eliminating backward proposals and enabling pool reuse. The method is evaluated on two language backbones (MDLM, LLaDA-8B) and one image backbone (MaskGIT) across four language reward functions and CLIPScore for images, consistently outperforming FK Steering, SVDD, SoP, and Best-of-N.

## Strengths

- **Principled and non-trivial method design.** The transition kernel (Eq. 2: summing over noised-then-denoised states) combined with the choice of balancing function λ such that weights become uniform and acceptance reduces to a reward comparison (Eq. 3) is genuinely elegant. The practical payoff — eliminating backward proposals, enabling pool reuse, selective application via effective timesteps — is significant and well-motivated.

- **Consistently positive empirical results across diverse settings.** IterRef outperforms all baselines on 2 language backbones × 4 reward functions, plus an image backbone with CLIPScore, under controlled compute budgets. The gains are often substantial: on MDLM, IterRef at 4T NFEs matches FK at 32T NFEs on Toxicity, and the pattern holds across most tasks and NFE levels as shown in Figure 2.

- **Informative diagnostic analysis (Tables 2, 3, Figure 4).** The finding that later denoising stages matter more for discrete diffusion (Table 2, unlike continuous diffusion) and that increasing iterations k matters more than increasing particles N (Table 3) directly supports the paper's thesis that iterative refinement is the key mechanism.

## Weaknesses

### Major

- **Proposition 1's convergence guarantee depends on an unverified assumption.** The proposition assumes that *q* and *p_θ* form a reversible Markov kernel. The paper provides no argument or evidence that this holds — *p_θ* is a learned approximation of the reverse process, not the true reversal of *q*, and the absorbing-state forward process has no exact reverse in the same parametric family. The paper lists this as Contribution 3 ("explanation of its effectiveness under certain assumptions") but never discusses whether the assumption is reasonable or what happens when it is violated. A theoretical guarantee resting on an unchecked assumption about the model does not strengthen the paper's contribution; it should be honestly reframed.

- **Evaluation is conducted entirely on the same proxy metrics used for guidance, without independent quality assessment.** For the language experiments, Toxicity, Sentiment, CoLA, and Perplexity *are* the reward functions being optimized — measuring IterRef on these conflates "better reward optimization" with "better generation quality." While ImageReward is mentioned (Appendix C.1) for images, no independent quality metric (human evaluation, LLM-as-judge, or held-out metric) is provided for the text experiments. Since the paper defines reward-guided generation as aiming to "preserve the naturalness of the samples while maximizing the given reward" (Section 2), the evaluation only addresses the reward maximization side.

- **Missing baseline: PG-DLM (Dang et al., 2025).** The paper acknowledges PG-DLM in Related Work (§5) as applying "Particle Gibbs sampling, repeatedly resampling the entire trajectory multiple times" — the same conceptual family as IterRef (MCMC-based iterative refinement of discrete diffusion trajectories). It is not included in any experiment and no justification for its exclusion is given. A direct comparison would either strengthen the paper's claim or clarify meaningful differences between the approaches.

### Minor

- **Figure 5 safety experiment introduces undefined baselines.** The figure description lists "SLP, SR, SVTOD" as baselines, none of which are defined in the paper text. Additionally, the figure confusingly lists both "IterRef" and "Ours" as separate entries when they should be the same method. The reader cannot determine what the safety comparison is actually against.

- **Safety evaluation is on a small scale.** The detoxification study uses 300 generations from 15 prompts, which is relatively small for safety-critical conclusions where standard practice uses substantially larger prompt sets.

- **The paper notes that IterRef underperforms BoN on CoLA with LLaDA** and offers an explanation ("LLaDA already generates linguistically well-formed text") but does not analyze this failure mode further — e.g., by examining whether similar patterns appear on other tasks with strong base-model performance.

### Trivial

- The figure description for Figure 5(a) lists both "IterRef" and "Ours" as separate methods, creating confusion; they should be the same method.

## Nice-to-Haves

- Add at least one independent quality evaluation for language generations (e.g., LLM-as-judge or human ratings on fluency/alignment) to substantiate the claim that IterRef improves generation quality rather than merely optimizing the reward proxy more efficiently.
- Compare against PG-DLM experimentally to directly situate IterRef among MCMC-based refinement methods for discrete diffusion.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **"The 8× faster claim is a point comparison"** — REMOVED. The paper provides full curves across compute budgets (Figure 2) and the claim is explicitly contextualized to the specific task. This is a legitimate characterization of the data at that operating point.
- **"Paper does not discuss the failure case on CoLA with LLaDA"** — REMOVED. The paper explicitly discusses this at line 202: "on CoLA, Best-of-N (BoN) achieves larger gains, which can be attributed to the fact that LLaDA already generates a linguistically well-formed text."
- **"Per-timestep computational cost not directly compared"** — REMOVED. The paper acknowledges NFE limitations and provides wall-clock time analysis in Appendix C.4.
- Various section-by-section observations that are commentary rather than weaknesses.

## Novel Insights

The paper's own contributions provide the primary insights: the tailored MTM framework for discrete diffusion is genuinely novel. The reviewer's key observation is that Proposition 1's unverified reversibility assumption, coupled with the evaluation gap (proxy metrics only), forms a pattern where the paper makes stronger claims — on both the theoretical and empirical fronts — than the evidence fully supports. This is a calibration issue, not a methodological one; the method itself is sound and empirically effective.

## Suggestions

1. Reframe Proposition 1 honestly — either justify the reversibility assumption or state it as a heuristic motivation rather than a formal guarantee. The paper is empirically strong enough to stand without an overstated theoretical claim.
2. Add at least one independent quality metric (human evaluation or LLM-as-judge) for the language experiments.
3. Define SLP, SR, SVTOD, or remove them from Figure 5 if they are not part of the paper's core comparison.
4. Consider including PG-DLM as a baseline if feasible.

## Calibration Anchors

The following calibration anchors were retrieved to calibrate the score:

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| Ombm8S40zN.md — Steering Masked Discrete Diffusion Models via DDPP | 6.25 | R1 | Yes | Most similar topic (steering discrete diffusion models). Similar novel method framing, diverse experiments; shares weaknesses of missing baselines and theory concerns. Our paper has stronger empirical results (always beats baselines) but weaker evaluation (no independent quality metrics). |
| G328D1xt4W.md — Fine-Tuning Discrete Diffusion Models via Reward Optimization | 6.00 | R1 | Yes | Addresses discrete diffusion + rewards but via fine-tuning rather than inference-time guidance. Has theory concerns similar to our paper (questionable theorem). |
| 2fgzf8u5fP.md — Derivative-Free Guidance with Soft Value-Based Decoding | 3.80 | R1 | Yes | Similar topic but with fatal flaws (α=0 contradicts stated goals, unfair comparisons). Our paper is significantly stronger. |
| peNgxpbdxB.md — Scalable Discrete Diffusion Samplers | 6.00 | R1 | No | Different focus (training discrete diffusion samplers for combinatorial optimization). |
| iIGNrDwDuP.md — Scaling Laws for Diffusion Transformers | 5.25 | R1 | No | Different focus (scaling laws for DiT training). |

**Round 1 bracket:** 5.5–7.5. After itemized comparison against the closest anchor (Ombm8S40zN, 6.25), our paper sits slightly below due to the combination of an unverified theoretical assumption and evaluation only on proxy metrics. The core method is strong and empirically well-supported, warranting acceptance with revisions. Final score: **6.0**.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>