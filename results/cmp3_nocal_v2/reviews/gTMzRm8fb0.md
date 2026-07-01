## Summary

This paper proposes GoalRank, a generator-only ranking framework for recommender systems. It provides a theoretical analysis (Theorem 1) showing that a single sufficiently large generator-only model can achieve strictly smaller approximation error to the optimal ranking policy than a k-mixture of generators with an evaluator. The paper then introduces group-relative optimization: a training method that constructs a reference policy from z-score normalized rewards within groups of candidate lists (assembled using auxiliary policies), then trains a generator to match this reference via cross-entropy minimization. Evaluation includes offline experiments on three datasets (ML-1M, Amazon-Book, Industry) with 17–25%+ improvements on some metrics, and large-scale online A/B tests on a platform with half a billion daily active users showing 0.1–1.2% gains on business metrics.

---

## Strengths

1. **Group-relative optimization is a practically motivated and concrete methodological contribution.** Constructing a reference policy via within-group z-scored rewards (Eq. 4) and training a generator to match it is a novel distillation approach. The idea of using auxiliary policies to construct groups with sufficient reward diversity is sensible. This is the paper's most original technical contribution.

2. **Extensive evaluation spanning offline benchmarks and production-scale online A/B tests.** The paper evaluates on three datasets (ML-1M, Amazon-Book, Industry), provides scaling experiments up to 0.1B parameters, and reports online A/B results from a platform with >500M DAU, 14-day duration, and tens of millions of users per bucket. Such breadth of validation is rare and valuable.

3. **Consistent empirical improvement across all settings.** GoalRank outperforms all baselines on all datasets and metrics in offline experiments. The online A/B results, while modest in absolute magnitude (0.1–1.2%), are consistently positive and statistically significant. The hybrid setting (GoalRank + MG-E) has been deployed to full production traffic — a strong practical endorsement.

4. **Reward bias ablation (Table 3) provides useful robustness analysis.** The controlled noise experiment ($\lambda \in \{0.0, 0.2, 0.5\}$) demonstrates the method degrades gracefully under biased reward signals, supporting the claim that the group-relative normalization mitigates reward bias.

---

## Weaknesses

### Fatal
None.

### Major

1. **Theorem 1 is an expressivity/existence result with no formal link to the training method.** Theorem 1 shows that a generator of width $\geq k\alpha + n$ has strictly smaller KL approximation error to $\pi^*$ than a $k$-mixture of width-$\alpha$ generators. This is a statement about **what policies exist** in the model class, not about what the proposed training procedure (group-relative optimization, Section 3.2–3.3) will find. The gap between "there exists such a policy" and "the group-relative cross-entropy objective will lead to it" is unaddressed. The paper would be stronger if it either (a) bounded $\text{KL}(\pi_\theta \| \pi^*)$ in terms of the training objective, or (b) explicitly framed the theory and the method as independent contributions rather than implying the training realizes the theoretical guarantee.

2. **Baseline comparison methodology is underspecified.** The paper states (line 236): "all baselines share exactly the same evaluator (reward model) as GoalRank." For different baseline families, this statement is ambiguous:
   - **G-E baselines (PIER, NAR4Rec):** These methods have their own learned evaluators designed for their architecture. If their evaluator was replaced with GoalRank's reward model, this may be suboptimal for them.
   - **G-only baselines (DNN, DLCM, PRM):** These methods do not use evaluators at inference. The paper does not clarify what "share the same evaluator" means for them — whether the reward model was used as an auxiliary training signal or otherwise.
   - **MG-E baselines:** The evaluator role (selecting among candidate lists) differs from the reward model's role in GoalRank (constructing training targets).

   Without clarification, it is difficult to assess whether the baselines were compared in their strongest form. This is the most significant experimental reporting gap in the paper.

### Minor

3. **Offline evaluation task differs from the training objective in a way that may asymmetrically favor GoalRank.** The offline evaluation (line 202) uses the last 6 chronological interactions as ground truth — a behavioral cloning task. GoalRank is trained on a reward model (trained on "long views" feedback), while baselines are (presumably) trained on typical ranking losses using the same interaction data. If baselines optimize directly for the evaluation signal and GoalRank optimizes for a reward proxy that happens to correlate well, the comparison conflates the training signal difference with the architectural difference. An ablation training all methods on the same objective would isolate the source of improvement.

4. **The offline-to-online performance gap is large and unexplained.** Offline improvements are 17–25%+ on H@6 and M@6 (Industry dataset), while online improvements are 0.1–1.2% on business metrics. While some attenuation is expected, this two-orders-of-magnitude gap warrants discussion. The paper does not address whether the offline metrics are a poor proxy for online engagement, or whether the offline evaluation confounds inflate the numbers.

5. **The main text does not clarify how $\pi_\theta = \text{softmax} \circ g_\theta$ is tractably computed over the combinatorial list space ($P(50,6) \approx 1.14\times 10^{10}$).** The paper states "the generator can be instantiated by any sequence generation model" (line 166), which implicitly assumes autoregressive factorization. This is a reasonable default for the target audience, but the text should state explicitly that the policy is factorized as $\pi_\theta(l) = \prod_{t=1}^L \pi_\theta(l_t \mid l_{<t})$, and discuss whether Theorem 1's guarantee (which considers the full softmax space) applies under this factorization. The appendix presumably contains architecture details (stripped by the parser), but a brief clarification in the main body would improve the paper.

6. **"Generator-only" framing overstates the distinction during training.** The paper contrasts GoalRank with MG-E methods and presents it as "generator-only one-stage." However, training requires: (a) a reward model trained on user feedback (effectively an evaluator), and (b) an auxiliary set of ranking policies $\mathcal{M}$ (multiple generators). The paper is honest about these components in Section 3.3, but the framing throughout (abstract, introduction, Figure 1) emphasizes "generator-only" as an architectural distinction, when it is actually an inference-time property. Clarifying this up front would avoid confusion.

### Trivial
- None beyond parser artifacts.

---

## Nice-to-Haves

- **Controlled ablation training GoalRank without the reward model** (i.e., using the same behavioral cloning objective as baselines) would isolate whether improvements come from the group-relative optimization, the generator-only architecture, or the additional reward signal.
- **Reporting training/inference compute cost** (latency, memory, FLOPs) relative to baselines would strengthen the practical contribution, especially given production deployment claims.
- **The scaling experiment (Figure 3) shows only 4 data points** across 100× model size. Additional sizes with error bars across multiple runs would make the "scaling law" claim more convincing.

---

## Removed Points

These points appeared in the input review but were removed per the filtering rules:

- **"Evidence upper bound" missing from the body** (Reviewer's Critical Issue #1). Removed because: the paper references Appendix A for proofs and technical details (line 118, line 321, line 329). The parser strips appendix content from all papers. Per the rules, criticisms about missing proofs that are deferred to the appendix must be removed, as the appendix exists in the original submission.
- **Claim that Theorem 1 "stacks the deck" by comparing a larger model to smaller models.** Removed because: Theorem 1 is fundamentally an expressivity analysis — it asks whether a larger generator's policy class can approximate $\pi^*$ better than an ensemble of smaller generators with an evaluator. Showing that a single wider model has richer expressivity is the intended result, not a flaw in the comparison. Parameter-matched expressivity analysis would be a different (also interesting) question, but its absence is not a weakness of the stated claim.
- **Speculative criticism about Theorem 1's guarantee not holding for autoregressive generators.** Removed because: the paper says "any sequence generation model" (line 166), which implies standard autoregressive factorization. Whether the theoretical guarantee transfers to factorized policies is a nuanced question that depends on the specific architecture (detailed in the stripped appendix); the reviewer's assertion that "the theorem's guarantee may not hold for it" is speculation, not a verified flaw.
- **Generic reproducibility concerns about undisclosed hyperparameters, implementational details.** Removed per rules about trivial reproducibility nitpicks and appendix-deferred content.

---

## Novel Insights

The most salient observation from triangulating the reviews is that the paper's theoretical contribution (Theorem 1) and practical contribution (group-relative optimization) are presented as a unified story but are not formally connected. Theorem 1 guarantees existence of a better-approximating policy in a wider model class; the training method is an ad-hoc heuristic (z-score normalization within groups, cross-entropy with an auxiliary-policy-assembled reference). The paper never shows that minimizing $\mathcal{L}(\pi_\theta)$ (Eq. 5) actually reduces $\text{KL}(\pi_\theta \| \pi^*)$ or bounds the gap. This disconnect means the theoretical framing adds rhetorical weight but not methodological guidance. Separately, the enormous offline-to-online gap (25% vs 0.2%) suggests the offline protocol (last-6-interactions behavioral cloning with MF retrieval) may not be a faithful proxy for the ranking task the method is designed for.

---

## Suggestions

1. Clarify whether baselines' evaluators were replaced with GoalRank's reward model, and if so, justify why this is fair to G-E methods that have their own purpose-built evaluators.
2. Add a brief statement in Section 3.2 (main text) about how $\pi_\theta$ is computed tractably — specifically, whether autoregressive factorization is used and whether $\text{softmax} \circ g_\theta$ is over items at each position or over the full list space.
3. Discuss the offline-to-online gap in the text: acknowledge the magnitude difference and explain which offline metrics best predict the online behavior.
4. Qualify the "scaling law" claim with the caveat that only 4 model sizes are shown; add error bars to the scaling figure.
5. Frame the "generator-only" distinction as an inference-time property rather than an architectural one throughout the paper.

---

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>