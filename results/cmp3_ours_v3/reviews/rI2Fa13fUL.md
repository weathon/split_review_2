## Summary

This paper proposes **Generative Trajectory Policies (GTPs)**, a new policy class for offline RL that learns the entire solution map of a continuous-time generative ODE, rather than just its instantaneous form (diffusion) or endpoint (consistency). The paper first provides a unified ODE framework showing that diffusion, flow matching, consistency models, CTMs, shortcut models, and mean flows are all instances of learning the same solution map $\Phi(x_t, t, s)$ — a genuinely illuminating conceptual contribution. It then introduces two practical techniques: a closed-form score approximation that avoids costly ODE solver backpropagation during training (Theorem 1), and an advantage-weighted objective for value-driven policy improvement (Theorem 2). Experiments on D4RL show strong results, particularly in the AntMaze domain where GTP-BC dramatically outperforms prior generative BC methods.

## Strengths

1. **A genuinely useful unifying theoretical perspective (Section 3).** The paper casts diffusion models, flow matching, consistency models, CTMs, shortcut models, and mean flows as instances of learning the same ODE solution map $\Phi(x_t, t, s)$, distinguished only by which subset of the flow map they approximate and which loss (instantaneous flow vs. trajectory consistency) they emphasize. This is not a trivial rearrangement — it provides a clean design space that clarifies why different generative policies behave differently and what a "complete" policy (one that learns the full map) would look like. For a field that has been trading off expressiveness and efficiency empirically, this conceptual unification is a genuine contribution.

2. **The score approximation (Theorem 1, Remark 1) is clever and practically impactful.** Replacing the need to repeatedly solve an ODE (which would require backpropagating through a solver at every training step) with the closed-form surrogate $\tilde{f}(\mathbf{x}_t, t) = (\mathbf{x}_t - \mathbf{x})/t$ — so that intermediate points are obtained by direct one-step perturbation rather than numerical integration — addresses a real computational bottleneck. The ablation (Table 3) confirms the practical benefit: the ODE-solver variant takes 5.23h vs. 4.26h for GTP and achieves worse performance (99.7 vs. 112.2).

3. **Strong overall empirical results.** The BC results (Table 1) on AntMaze are genuinely striking: GTP-BC (66.3 average) versus C-BC (44.1) and D-BC (41.2). On antmaze-medium-diverse, GTP-BC reaches 85.0 vs. 31.6 for C-BC — these are not incremental gains. The full RL results (Table 2) also show the best average on both Gym (89.0) and AntMaze (80.6) domains.

4. **Clean ablation (Table 3).** The ablation cleanly isolates the contribution of each component: removing score approximation drops score from 112.2 to 99.7, and the linear Q-term alternatives either diverge or require delicate tuning. This strengthens the claim that both design choices matter.

## Weaknesses

### Major

1. **The "perfect scores on several notoriously hard AntMaze tasks" claim (abstract and Section 1) is overstated.** The abstract states "achieving perfect scores on several notoriously hard AntMaze tasks," and the introduction (line 27) repeats "perfect scores on several notoriously challenging AntMaze tasks." From Table 2, only antmaze-umaze achieves a perfect 100.0. The other AntMaze tasks do not reach 100.0 (antmaze-ud: 81.9, antmaze-mp: 83.3, antmaze-md: 94.2, antmaze-lp: 53.5, antmaze-ld: 71.0). This should be corrected throughout the paper.

2. **The paper's central framing — resolving the expressiveness–efficiency trade-off — is imprecise.** The paper opens by describing a trade-off between slow-but-expressive diffusion policies and fast-but-degraded consistency policies (lines 15–18), and frames GTP as bridging this gap. However, the evaluation uses *K = 5 sampling steps* for both diffusion policies and GTP, while consistency policies use *K = 2* (line 259). At inference time, GTP is therefore comparable to diffusion, not faster. The paper never provides an inference-time speed comparison. The efficiency gain is actually a *training-time* advantage (avoiding solver backpropagation via the score approximation), which the paper acknowledges in the conclusion ("reducing the substantial training time ... remains an important avenue for future research"). The framing should be clarified to honestly describe which efficiency is being improved.

### Minor

3. **Missing baseline entries in Table 2 weaken comparative claims.** BDM has missing entries for antmaze-lp and antmaze-ld. C-AC has missing entries for antmaze-md, antmaze-lp, and antmaze-ld. The average comparison across all six AntMaze tasks (GTP: 80.6) is computed over tasks where these baselines have no reported results — this is not clearly indicated. Additionally, on individual tasks the picture is more mixed than the "state-of-the-art" average claim suggests: C-AC substantially outperforms GTP on halfcheetah-medium (69.1 vs. 53.9) and halfcheetah-medium-replay (58.7 vs. 50.8), and QGPO outperforms GTP on antmaze-large-play (66.6 vs. 53.5).

4. **Theorem 1's theoretical analysis does not fully align with the practical implementation.** Theorem 1 bounds $|\mathcal{L}_{\text{prac}} - \mathcal{L}_{\text{ideal}}| = O(h^p)$ where $h$ is the maximum solver step size, and assumes a $p$-th order multi-step solver. However, Remark 1 states that the practical method bypasses the solver entirely, using a single direct perturbation $\mathbf{x}_u = \mathbf{x} + u \cdot \mathbf{z}$. This is equivalent to one Euler step ($p=1$, $K=1$), yielding a bound of $O(h)$ where $h = t-u$ could be large. The paper does not discuss how the approximation quality degrades as $|t-u|$ grows. The theorem provides some theoretical grounding but the gap between its assumptions and the practice should be acknowledged.

5. **Theorem 2 (advantage-weighted objective, Eq. 12) is a standard result from KL-regularized RL.** The formulation $\pi^*(a|s) \propto \pi_{\text{BC}}(a|s) \exp(\eta A(s, a))$ underlies AWR (Peng et al., 2019), AWAC (Nair et al., 2020), IQL (Kostrikov et al., 2021), and many others. The legitimate contribution is applying this weighting to *generative trajectory losses* (Eqs. 17–18), which is a valid design choice. Presenting it as a new "Theorem" (line 189) overstates novelty.

6. **Inference efficiency is not evaluated despite being central to the paper's framing.** The paper claims to address an expressiveness-efficiency trade-off but provides no wall-clock inference time comparison. Given that GTP uses the same K=5 steps as diffusion, an explicit comparison would clarify what efficiency gain is actually being achieved.

### Trivial

7. **Table 1 is labeled as "behavior cloning" but includes methods that use value functions (AWAC, TD3+BC, DT).** The text clarifies these are included for context, and the key comparison (GTP-BC vs. D-BC vs. C-BC) is fair. The label is mildly imprecise but not misleading once the text is read.

## Nice-to-Haves

- Ablate the number of sampling steps $K$ for GTP. If GTP with $K=2$ outperforms C-BC with $K=2$, that would directly substantiate the claim that learning the full trajectory map is better than learning only the endpoint. If GTP with $K=1$ or $K=2$ is competitive with GTP with $K=5$, that would be a strong result supporting the efficiency claim.
- Provide inference wall-clock time comparison across methods (D-BC with K=5, C-BC with K=2, GTP with K=5).
- Report statistical significance or confidence intervals for AntMaze results where standard deviations are large (e.g., 8.1 on antmaze-mp).
- Provide sensitivity analysis for the advantage temperature $\eta$.

## Removed Points

These points were raised in the input reviews but are removed with justification:

- **"Table 1 mixes pure imitation with RL methods — misleading comparison"**: The paper explicitly states that AWAC, TD3+BC, and DT are "offline RL methods" and the key comparison is GTP-BC vs. D-BC vs. C-BC. The table includes the RL methods for broader context, which is standard practice. The heading is mildly imprecise but the text is clear.

- **"Theorem 2 is a known result — not a contribution"**: Partially retained (Minor weakness 5). The result itself is standard, but applying it to generative trajectory losses is a valid contribution. The original critique overstated the severity.

- **"Theorem 1 justification doesn't match practice"**: Retained but demoted to Minor (weakness 4). The reviewer's analysis of the multi-step vs. single-step gap is technically correct, but the core idea (surrogate field is a valid approximation) is still supported. The bound being O(h) is acknowledged but the empirical results (Table 3) validate the approach.

- **Several generic "missing" or "could be improved" points from the Strengthening section**: These are moved to Nice-to-Haves.

## Novel Insights

The input review's harsh critic identifies a genuinely novel observation about the framing mismatch: the paper claims to resolve the expressiveness-efficiency trade-off but the efficiency gain is in training, not inference — while the paper's narrative implies an inference-time breakthrough. This observation is specific, verifiable from the paper (K=5 for both diffusion and GTP), and points to a real flaw in how the contribution is presented. The critic also correctly identifies that Theorem 1's theory-practice gap (multi-step solver analysis vs. single-step perturbation implementation) is not discussed, which is a subtle but valid technical point that escaped the surface-level presentation.

## Suggestions

1. **Correct the "perfect scores" overstatement** throughout the paper. Replace with "a perfect score on antmaze-umaze and strong results on other AntMaze tasks."
2. **Clarify the framing** of the expressiveness-efficiency trade-off. Acknowledge that GTP uses the same number of inference steps as diffusion (K=5), and position the efficiency contribution as a *training-time* improvement (via the score approximation avoiding ODE solver backpropagation). Provide inference wall-clock comparisons to be transparent.
3. **Fill in missing baseline entries** in Table 2 for BDM and C-AC, or add a footnote explaining why they are missing and how averages are computed.
4. **Add a discussion** of the gap between Theorem 1's assumptions (multi-step solver, p-th order) and the practice (single Euler step). Acknowledge that the bound is O(h) where h may be large, and note that strong empirical results compensate.
5. **Reframe Theorem 2** as a design choice derived from standard KL-regularized RL, rather than a new theoretical result. Cite AWR/AWAC/IQL.
6. **Ablate K** (number of sampling steps) to substantiate the claim that GTP "can achieve high performance even with a few sampling steps."

## Score and Decision

### Calibration Report

**Round 1 — Bracketing**: Searched for similar papers across all score bands with query "offline reinforcement learning generative diffusion policy ODE framework". Retrieved the following anchors (all rounds combined):

| Path | Avg Score | Comparison to this paper |
|------|-----------|--------------------------|
| BDQL (gEdg9JvO8X.md) | 3.67 | Weaker on both novelty and results |
| Offline-to-Online RL (cXxfVkRCHJ.md) | 3.00 | Less relevant topic, weaker results |
| ADEPT (1zuJZ1jGvT.md) | 5.00 | Comparable scope but less novel framework |
| Revisiting Generative Policies (duCs92vmMc.md) | 5.75 | Similar unified-perspective goal but weaker empirical results and less novel core contribution |
| Value Function Estimation (TeeyHEi25C.md) | 6.25 | Interesting idea but weaker baseline set |
| Energy-Weighted Flow Matching (HA0oLUvuGI.md) | 6.25 | Similar contribution level; current paper has stronger empirical validation |
| What Makes a Good Diffusion Planner (7BQkXXM8Fy.md) | 7.50 | More exhaustive empirical study but less novel conceptual contribution |

**Round 1 Bracket**: 5.5–7.5. The paper is clearly stronger than the 3–5 range papers and has a more novel core contribution than the 5.75–6.25 papers. It is not as empirically comprehensive as the 7.50 paper but has a more novel conceptual framework.

**Narrowing**: Comparing to Revisiting Generative Policies (5.75) — the current paper has a genuinely more novel framework (unified ODE lens vs. KL classification) and stronger empirical gains. Comparing to Energy-Weighted Flow Matching (6.25) — both have novel theoretical contributions and fixable overclaiming issues; the current paper's empirical validation is stronger and more thorough, placing it slightly above. The gap to What Makes a Good Diffusion Planner (7.50) is due to the current paper's framing issues and lack of inference-time analysis.

**Final score: 6.5** — The paper makes a genuine contribution (the unified ODE framework is conceptually valuable, the score approximation is practically effective, and the empirical results are strong), but the presentation overstates results ("perfect scores on several tasks"), the framing around expressiveness-efficiency is imprecise, and several minor issues (missing baselines, theory-practice gap in Theorem 1) need addressing. With revisions, this would be a solid paper.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>