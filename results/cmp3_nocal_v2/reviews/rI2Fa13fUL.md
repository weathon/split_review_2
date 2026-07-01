## Summary

This paper introduces Generative Trajectory Policies (GTPs), a new policy class for offline RL that learns the full ODE solution map of a continuous-time generative process. The authors (1) present a unified ODE framework connecting diffusion, flow-matching, consistency, and trajectory models, (2) adapt this framework to offline RL with a score-approximation technique (Theorem 1) that replaces expensive ODE solvers with a closed-form surrogate during training, and (3) integrate advantage-weighted guidance for policy improvement. Empirically, GTP achieves state-of-the-art performance on D4RL, particularly on the challenging AntMaze tasks where it substantially outperforms prior generative policies.

## Strengths

- **Score approximation (Theorem 1) is a genuine theoretical contribution.** The result that replacing the true score with the closed-form surrogate \(\tilde{f}(\mathbf{x}_t,t) = (\mathbf{x}_t - \mathbf{x})/t\) changes the training objective by only \(O(h^p)\) provides formal justification for a technique that simultaneously reduces computational cost and removes a source of training instability. This is non-trivial and connects a practical design choice to a provable guarantee.

- **AntMaze results are genuinely strong.** In the BC setting (Table 1), GTP-BC achieves 66.3 average on AntMaze vs 44.1 for C-BC and 41.2 for D-BC—a gap exceeding 20 points. In the full RL setting (Table 2), GTP reaches 80.6 vs QGPO at 78.3 and D-QL at 69.6, with a perfect 100.0 on antmaze-umaze and 94.2 on antmaze-medium-diverse. These are the hardest D4RL domains and the improvements are practically meaningful.

- **Clean exposition of the design space.** Sections 3.1–3.4 provide a well-structured synthesis showing how diffusion models, consistency models, CTMs, shortcut models, and mean flows instantiate different aspects of the same ODE flow-map formulation. While the relationships are known in the generative modeling literature, applying this lens to frame the RL policy design space is useful and clearly motivates the GTP architecture.

## Weaknesses

### Fatal
None.

### Major

1. **The abstract factually misrepresents the results.** The abstract (line 9) and contribution list (line 27) both claim that GTP achieves "perfect scores on *several* notoriously hard AntMaze tasks." Examining Table 2, only **one** task—antmaze-umaze—achieves a perfect 100.0. The remaining AntMaze results (umaze-diverse 81.9, medium-play 83.3, medium-diverse 94.2, large-play 53.5, large-diverse 71.0) are strong but not perfect. "Several" unambiguously implies more than one. This is a factual inaccuracy about what the method accomplished. The underlying results are strong enough without embellishment; the claim should be corrected to reflect the single perfect score and the state-of-the-art performance on the harder variants.

2. **The central framing about resolving the expressiveness-efficiency trade-off is misaligned with what is actually delivered.** The paper's motivating question (line 17) asks whether we can achieve *both* policy expressiveness *and* computational efficiency, contrasting "slow, iterative" diffusion policies with "fast, single-step" consistency policies. However, GTP uses \(K=5\) sampling steps at inference—**the same number** as the diffusion policies (D-QL, D-BC) it compares against (line 259). Consistency policies use \(K=2\). GTP is therefore not faster than diffusion policies at inference; it matches them. The efficiency improvement from score approximation (~19% training-time speedup per Table 3) is real but applies to *training*, not the inference bottleneck that the motivation section emphasizes. The paper should either reframe its contribution around *training* efficiency and policy quality (setting aside inference speed claims) or provide wall-clock inference times demonstrating that GTP's 5 steps are somehow faster than prior 5-step diffusion methods. As written, the framing overpromises relative to what is demonstrated.

### Minor

3. **C-BC baseline numbers appear anomalously low on several Gym tasks, raising questions about fair comparison.** In Table 1, C-BC obtains 31.0 on halfcheetah-medium vs BC's 42.6, and 32.7 on halfcheetah-medium-expert vs BC's 55.2. A 10–20 point drop from a simple Gaussian BC to a more expressive consistency model is surprising and not obviously consistent with standard D4RL results. The paper does not specify whether these numbers are reproduced in-house or cited from Ding & Jin (2024), nor does it describe the C-BC setup. Since GTP-BC outperforms these baselines by a large margin, this does not threaten the paper's main conclusions, but the discrepancy should be explained or corrected for scientific rigor.

4. **The ablation study (Table 3) is conducted on a single task (hopper-medium-expert).** While the score approximation shows a clear benefit (+12.5 points) and the advantage-weighting comparison is informative, ablating on only one environment makes it difficult to assess whether the benefits generalize. Including at least one AntMaze task in the ablation would substantially strengthen the evidence, particularly since AntMaze is where GTP's main gains are observed.

5. **Theorem 2 is a standard result in KL-regularized RL.** The advantage-weighted objective \(\pi^*(a|s) \propto \pi_{\text{BC}}(a|s) \exp(\eta A(s,a))\) appears in MPO, ABM, AWAC, and many prior works. It is correctly stated and applied, but presenting it as a theorem implies a level of novelty that is not warranted. Stating this as "following the standard derivation" would be more appropriate.

### Trivial
None.

## Nice-to-Haves

- The score approximation derivation (Theorem 1) uses a complex multi-step solver apparatus, but in practice (Eq. 11) the method uses direct perturbation \(\mathbf{x}_u = \mathbf{x} + u \cdot \mathbf{z}\), corresponding to the \(h \to 0\) limit of an Euler solver with the surrogate. The practical implication is simpler than the theorem's formalism suggests and could be stated more directly.
- The parameterization in Eq. (3) introduces the \(\frac{t}{t-s}\) scaling factor without explaining the intuition behind it; a brief explanation would improve accessibility.

## Removed Points (caution advised)

- **"The unified ODE framework is not a novel contribution"** — The paper explicitly cites Kim et al. (2024) and does not claim the framework itself as a novel discovery; it is presented as a pedagogical lens to motivate the RL-specific contributions in Section 4. The criticism attacks a claim the paper does not actually make.
- **"The conclusion undercuts the paper's framing"** — The final sentence acknowledges that reducing training time remains future work. This is an honest statement of limitation, not a contradiction of any core claim.
- **Various presentation nitpicks** (Eq. 3 derivation clarity, Theorem 1 apparatus complexity) — These are matters of taste and do not constitute substantive weaknesses.

## Novel Insights

None beyond the paper's own contributions. The reviews identify two real issues (abstract overclaim, inference-efficiency framing mismatch) but do not surface any novel theoretical or empirical insight about the method that the paper missed.

## Suggestions

1. **Correct the factual inaccuracy in the abstract and contribution list.** Replace "perfect scores on several notoriously hard AntMaze tasks" with accurate language: "achieves a perfect score on the umaze task and state-of-the-art results on the harder AntMaze variants." This makes the paper *more* credible.
2. **Reframe the efficiency contribution around training time.** The score approximation provides a real ~19% training speedup and stability benefit. The paper should state this clearly and drop any implication that GTP improves inference efficiency over diffusion policies, or else provide inference wall-clock comparisons showing that 5-step GTP is faster than 5-step D-QL/D-BC (e.g., due to architectural differences).
3. **Add a baseline verification note** explaining the source and configuration of the C-BC numbers in Table 1.
4. **Extend the ablation to at least one AntMaze task** to demonstrate the generality of the score approximation benefit.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>