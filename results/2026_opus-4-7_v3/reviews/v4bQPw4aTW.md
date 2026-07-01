Now let me read the discussion/limitations section more carefully and check a few specific claims:Now I have thoroughly read the paper. Let me draft the review and then calibrate.Now let me calibrate with Round 1 — Bracketing:Let me read the most relevant anchors to calibrate:Now I have enough information to form my bracket and write the final review. Let me assess the anchors:

**Round 1 Bracket:**
- **Strong reject (< 1.5):** Papers like survey-only LLM reviews (1.0) — clearly much worse than AdaBoN. Not comparable.
- **Reject (1.5–3.5):** Papers like FiRST (3.0), Polybasic Speculative Decoding (3.0) — these have fundamental issues (weak baselines, unclear contributions). AdaBoN is better.
- **Borderline reject (3.5–5.5):** Adaptive Inference Theory (4.20), LASeR (5.25), Online Decision Deferral (4.25) — these are the closest range. AdaBoN shares characteristics with these: sound but limited contributions.
- **Borderline accept (5.5–7.5):** Damani et al. (6.50, Accepted), Inference Scaling Laws (5.75), GenARM (6.50) — Damani et al. is the most comparable. It's the same problem but with broader scope, downstream validation, and more ambitious results, though it requires auxiliary training.
- **Accept (7.5–8.5):** Papers here are significantly stronger contributions.

**Initial bracket: 4.5–6.0.** AdaBoN is better than the 3–4 papers (sound method, thorough experiments) but below Damani et al. (6.50) due to narrower scope, no downstream validation, and modest improvements. The key comparison is with Damani et al.: AdaBoN is model-agnostic (advantage) but has narrower scope, modest gains (0.54–0.62 BWR), and no downstream evaluation (disadvantages).

Now let me write the final review:

---

## Summary
This paper proposes AdaBoN, an adaptive two-stage Best-of-N sampling strategy that allocates inference budget across prompts based on estimated reward distributions. In stage 1, a fixed fraction (d = 0.75B) of the per-prompt budget explores each prompt uniformly and estimates reward distributions via Gaussian KDE; in stage 2, the remaining 25% is redistributed via a greedy algorithm proven optimal for concave marginal-gain vectors (Proposition 3.1). Evaluated across 12 LM-RM pairs, 3 datasets, and 50 batches, AdaBoN consistently achieves median BWRs of 0.54–0.62 and is competitive with uniform allocations using ~20% more budget.

## Strengths

- **Sound theoretical foundation with practical design.** Proposition 3.1 proves that the expected max-reward function is concave and monotonically increasing for any distribution with finite first moment, justifying the greedy allocation (Algorithm 1). The connection to Federgruen & Groenevelt (1986) is appropriate. This is a clean result with broad applicability — it holds regardless of reward distribution shape.

- **Genuinely model-agnostic and training-free.** Unlike Damani et al. (2024), which requires training a separate MLP for each LM-RM pair and budget level, AdaBoN operates entirely at test time with no pretrained auxiliary components. The paper demonstrates this concretely across 12 distinct LM-RM pairs (Section 4.1), showing the same algorithm works out-of-the-box for all. This is a real practical advantage.

- **Thorough experimental coverage within the target regime.** The evaluation spans 4 LMs × 3 RMs × 3 datasets × 50 batches. The 50-batch design (Section 4.1) ensures results are not artifacts of batch composition. Table 2b confirms BWR > 0.50 in 76–100% of batches across all 12 LM-RM pairs, and Figure 3 shows gains increasing with batch size K.

- **Well-justified evaluation metrics.** The BWR and EST metrics (Section 4.2) are well-motivated. The argument for using win rates over raw reward sums — that RM scores are only meaningful comparatively under Bradley-Terry — is sound and internally consistent with the paper's own optimization objective.

## Weaknesses

### Fatal
None

### Major
- **Adaptive headroom is mechanically limited by design.** With d = 0.75B, only 25% of the total budget is redistributable (e.g., 150 of 600 queries for K=5, B=120). The paper tests d ∈ {0.60B, 0.7B, 0.75B, 0.80B} (Appendix G.1) and finds d = 0.75B near-optimal, but provides no analysis of *why* — specifically, how the optimal d depends on distributional properties (variance, skewness, inter-prompt heterogeneity). This matters because it leaves unclear whether the method is approaching an inherent ceiling of two-stage allocation or whether better exploration strategies could unlock larger gains. The paper acknowledges the bandit-based alternative in Section 5 but does not analyze the fundamental tradeoff governing its own approach.

- **Win rates without margins obscure practical significance.** The paper reports only BWR (win/loss rates) but never the *magnitude* of improvement when AdaBoN wins. A median BWR of 0.58 (Table 1) could reflect negligible or substantial reward margins. Since the paper's own argument (Section 4.2) is that RM scores are only meaningful comparatively, the natural extension is to report *how much* better the adaptive allocation is when it wins — e.g., mean or median reward advantage conditional on winning. Without this, it is impossible to assess whether the gains matter in practice.

### Minor
- **Gap between theoretical guarantee and practical algorithm is unexamined.** Proposition 3.1 guarantees optimality of greedy allocation for the *true* V vectors, but the method uses estimated V̂ from KDE-estimated distributions and Monte Carlo sampling. The paper acknowledges this (line 121: "the greedy procedure may not be optimal when run on the estimated vectors") but provides no analysis of sensitivity to estimation error. Table 2b shows Gemma-Mistral achieves BWR > 0.50 in only 76% of batches, suggesting non-trivial degradation in ~24% of cases — yet no investigation of what causes these failures or how to mitigate them.

- **Minimax optimality claim is unsubstantiated.** Section 2.3 states: "without knowledge of the true distributions, the uniform allocation is the minimax optimal non-adaptive allocation." This is asserted without proof, citation, or qualification about the distribution class considered. While intuitively reasonable under symmetry, it should be formally justified or qualified.

- **Evaluation is purely RM-score-based.** No downstream validation (human evaluation, LLM-as-judge, or cross-RM validation) is provided to confirm that RM-score improvements translate to quality improvements. While this is partially standard for Best-of-N methodology papers, the paper's own citation of reward hacking concerns (Gao et al., 2023) makes this omission notable. This weakens practical significance claims but does not invalidate the algorithmic contribution, which is about efficient allocation within the RM-score framework.

### Trivial
None

## Nice-to-Haves
- Analysis of whether gains concentrate on batches with heterogeneous prompt difficulty (high variance in reward distribution parameters) vs. homogeneous batches — this would directly connect to the motivating intuition and help practitioners predict when AdaBoN helps.
- Reporting wall-clock timing to quantitatively substantiate the latency motivation for two-stage over more adaptive approaches.
- A limited comparison with Damani et al. (2024) on a small subset of settings to empirically validate the claim that their method does not work well in the small-K, large-B regime.
- Testing with different decoding strategies (temperature, top-p) since these affect reward distribution shape and may change the KDE estimation quality.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"The Bernoulli example overpromises gains"** — The Bernoulli example (Section 2.3) is explicitly pedagogical, using extreme parameters (p₁=0.95, p₂=0.05) to illustrate the *principle* of adaptivity. The paper does not claim real distributions exhibit such extreme gaps, and the experimental results are presented honestly. This is a framing preference, not a weakness.

- **"No comparison with Damani et al. invalidates the contribution"** — The paper provides three substantial justifications for this omission (Section 4.2): no available implementation, 216,000 MLPs needed, and different operating regime (small K vs. large K). While a partial comparison would strengthen the paper, the absence does not invalidate it. The paper clearly articulates the three-way distinction in approach (Section 1.1). Moved to nice-to-have.

- **"Missing downstream validation is fatal"** — This is a legitimate concern but does not rise to fatal because the paper's contribution is algorithmic (efficient allocation within the RM-score framework), not about alignment quality per se. Evaluating on RM scores is standard for Best-of-N papers (Gao et al., 2023; Beirami et al., 2024). Retained as minor weakness rather than fatal/major.

- **"KDE with Scott's rule may fail on skewed distributions"** — The paper itself identifies and discusses this issue (Appendix G.1, explaining the Qwen-Armo drop), and also tests alternative estimators (Gaussian and Skew-Normal MLE, Table 16 in Appendix K.3). The paper engages with this concern rather than ignoring it.

## Novel Insights
The paper's central empirical finding — that reward distributions for LM-RM pairs are smooth enough that simple Gaussian KDE from a modest exploration budget suffices for effective adaptive allocation — is practically useful. This makes the resource allocation problem substantially easier than a general bandit/online optimization problem and enables a simple, training-free solution. The finding that a single hyperparameter setting (d = 0.75B) works across all 12 LM-RM pairs suggests a degree of universality in reward distribution smoothness that could inform future work on inference-time compute allocation.

## Suggestions
- Report the mean/median reward margin conditional on AdaBoN winning to quantify practical significance of BWR improvements.
- Provide theoretical or empirical analysis of how the optimal d depends on batch heterogeneity and reward distribution shape (e.g., bound suboptimality as a function of KDE error).
- Investigate the ~24% failure cases (Gemma-Mistral) to characterize when the method degrades and provide practical guidance.
- Include a small-scale downstream validation (e.g., LLM-as-judge on a subset) to confirm RM-score gains are meaningful.

## Score and Decision

**Anchor papers retrieved:**

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| LLM Survey | 8QTpYC4smR | 1.00 | R1 | Far worse — not even a research contribution. |
| NEMESIS Jailbreaking | 5kMwiMnUip | 1.40 | R1 | Far worse — weak methodology. |
| KL Divergence GFlowNets | Uj0h13lVrR | 1.00 | R1 | Far worse — fundamentally flawed. |
| IC-Light | u1cQYxRI1H | 10.00 | R1 | Far better — strong novel contribution. |
| Efficient LLM Deployment | BjZP3fTlVg | 3.00 | R1 | Weaker — limited evaluation, but comparable scope ambition. |
| Polybasic Speculative Decoding | n7iwmPacDt | 3.00 | R1 | Weaker — lacks theoretical grounding AdaBoN has. |
| FiRST Router-Selective | ulGwcj1egv | 3.00 | R1 | Weaker — AdaBoN has cleaner experiments. |
| ALLoRA | 7X65yoKl3Y | 3.33 | R1 | Weaker — more fundamental issues identified. |
| Adaptive Inference Theory | hJDTuVQcQp | 4.20 | R1 | Comparable — theory without actionable prescriptions; AdaBoN is more practical but also limited in depth. |
| LASeR | fDcn3S8oAt | 5.25 | R1 | Comparable — similar scope, also rejected for limited contributions; AdaBoN is cleaner but narrower. |
| Test-Time Hypothesis Reweighting | 8HQS1X2AK4 | 5.33 | R1 | Comparable — similar borderline quality. |
| Online Decision Deferral | of25Zg4AdM | 4.25 | R1 | Comparable — bandit-based allocation, also limited validation. |
| **Damani et al. (most related)** | 6qUUgw9bAZ | **6.50** | R1 | **Key anchor.** Same problem, broader scope, downstream validation, larger gains (up to 50% compute reduction). AdaBoN is model-agnostic (advantage) but narrower, more modest gains, no downstream eval. |
| Inference Scaling Laws | VNckp7JEHn | 5.75 | R1 | Somewhat related — broader compute-optimal inference study, accepted with similar mixed reviews. |
| SAIL Online Alignment | 02kZwCo0C3 | 5.75 | R1 | Somewhat related — online alignment, rejected despite some strengths. |
| GenARM | J0qTpmbSbh | 6.50 | R1 | Less related — test-time alignment with autoregressive RM, stronger novelty. |

**Round 1 bracket: 4.5–6.0**

**Narrowing reasoning:** The most informative comparison is with Damani et al. (6.50, Accepted). AdaBoN tackles the same problem but is strictly narrower in scope, provides no downstream validation, and achieves more modest improvements. The model-agnostic advantage is real but does not compensate for these gaps. Damani et al. was borderline-accepted with scores of 6/8/6/6 — it was criticized for weak baselines and generalizability, but it had downstream metrics (pass rates, GPT-4 judge) and demonstrated up to 50% compute savings. AdaBoN's consistent-but-modest gains (BWR 0.54–0.62, ~20% budget equivalence) and lack of depth on the explore-exploit tradeoff place it below Damani et al. However, the method is sound, the experiments are thorough, and the contribution (training-free adaptive BoN) is real. This puts AdaBoN clearly below the borderline accept line (6) but above the reject threshold (3–4) where fundamentally flawed papers sit.

**Final score: 5.0** — The paper delivers a clean, practical method with thorough experiments, but the contribution is incremental: modest gains limited by design, no downstream validation, and insufficient theoretical depth on the core tradeoff. It falls between the borderline-reject (4) and borderline-accept (6) anchor points.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>