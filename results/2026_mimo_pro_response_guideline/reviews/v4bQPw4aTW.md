Now let me finalize my calibration analysis and score.

**Calibration anchors retrieved across all rounds:**

| Path | Avg Score | Round | Comparison to AdaBoN |
|------|-----------|-------|---------------------|
| Uj0h13lVrR (GFlowNets) | 1.00 | 1 | Completely unrelated topic |
| bEgDEyy2Yk (minimax path) | 1.00 | 1 | Completely unrelated topic |
| 5lUdTogEL3 (person re-ID) | 1.00 | 1 | Completely unrelated topic |
| BjZP3fTlVg (LLM deployment risk) | 3.00 | 1 | Less rigorous methodology, weaker claims |
| n7iwmPacDt (speculative decoding) | 3.00 | 1 | Different approach to inference efficiency |
| y2ch7iQSJu (budget active learning) | 2.00 | 1 | Budget-constrained learning, different domain |
| 2DD4AXOAZ8 (MixAttention) | 2.00 | 1 | KV cache optimization, orthogonal |
| hJDTuVQcQp (adaptive inference theory) | 4.20 | 1 | Theoretical framework for adaptive inference |
| 0xUEBQV54B (Large Language Monkeys) | 5.00 | 1 | Repeated sampling scaling; rejected; AdaBoN has more novelty |
| 8HQS1X2AK4 (Test-Time Alignment) | 5.33 | 1 | Test-time alignment via ensembles; rejected; AdaBoN has broader eval |
| of25Zg4AdM (Online Decision Deferral) | 4.25 | 1 | Bandit-based deferral, less directly related |
| 6qUUgw9bAZ (Damani et al., 2024) | 6.50 | 1 | **Closest anchor**: Same problem, AdaBoN is simpler but has weaker baselines |
| 77gQUdQhE7 (Inference-Aware Fine-Tuning) | 5.67 | 1 | Best-of-N fine-tuning; accepted with limited experiments |
| CUABD2qIB4 (OCCAM) | 6.50 | 1 | Adaptive inference allocation; similar methodology rigor |
| VNckp7JEHn (Inference Scaling Laws) | 5.75 | 1 | Inference compute scaling analysis |
| A3YUPeJTNR (Hidden Cost of Waiting) | 8.00 | 1 | Stronger theoretical contribution |
| rfdblE10qm (Rethinking Reward Modeling) | 8.00 | 1 | More novel theoretical insight |
| OfjIlbelrT (FlexPrefill) | 8.00 | 1 | More impactful system contribution |

**Round 1 bracket: 5.5 – 7.0**

- AdaBoN is clearly stronger than rejected papers at 4.2–5.33 (more novelty, broader evaluation, cleaner methodology).
- AdaBoN is comparable to accepted papers at 5.67–6.50, particularly Damani et al. (6.50) which addresses the identical problem. AdaBoN is simpler and more practical but has weaker baseline comparisons and more modest gains.
- AdaBoN is weaker than 8.00 papers which tend to have more novel theoretical contributions or much stronger results.

Given that Damani et al. was accepted at 6.50 and AdaBoN offers a simpler alternative with broader evaluation but a key baseline gap, I place AdaBoN at **6.0** — a solid but not exceptional paper that warrants acceptance.

**Final score: 6.0 (Accept)**

The paper is a well-executed practical contribution: clean method, sound theory (Proposition 3.1), broad evaluation (12 LM-RM pairs, 3 datasets, 50 batches), and a genuine practical advantage over the closest prior work (no auxiliary training). The main weakness — the absence of adaptive baselines beyond uniform — is a real evidential gap but is comparable to the baseline criticism leveled at Damani et al. (which was accepted at 6.50). The modest effect sizes (BWR 0.54–0.62) and the 75% exploration fraction are minor concerns that don't undermine the core contribution.

---

## Summary
AdaBoN proposes a two-stage adaptive allocation strategy for Best-of-N inference-time alignment. Given a batch of prompts with a fixed total inference budget, the method first explores each prompt's reward distribution using kernel density estimation on a fraction of the budget, then greedily allocates the remaining budget to prompts where the expected marginal gain is highest. The method is model-agnostic, requires no auxiliary training, and needs only two parallelized LM calls. Evaluation uses two new metrics—Batch Win Rate (BWR) and Expected Survival Time (EST)—across 12 LM-RM pairs, 3 datasets, and 50 batches per configuration.

## Strengths
- **Well-grounded theoretical foundation**: Proposition 3.1 (Section 3, line 108) proves that the expected maximum of i.i.d. samples is concave and monotonically increasing, guaranteeing the greedy allocation algorithm is optimal via Federgruen and Groenevelt (1986). This is a clean, general result that provides rigorous justification for the entire two-stage pipeline.
- **Comprehensive empirical evaluation**: Table 1 shows consistent improvement across all 12 LM-RM pairs (median BWRs 0.54–0.62), Table 2b shows 76–100% of batches outperform uniform, and Table 2a shows median ESTs of 148–153 (competitive with ~25% larger uniform budgets). Evaluation spans 3 datasets and 50 distinct batches per configuration.
- **Model-agnostic and practical**: Unlike Damani et al. (2024) which requires training a separate MLP for each LM-RM pair and each budget value (potentially 216,000 MLPs for the experimental setup, line 188), AdaBoN uses only Gaussian KDE with Scott's rule at test time, making it plug-and-play for any LM-RM combination.
- **Novel, well-motivated evaluation metrics**: BWR (Equation 3) and EST (Equation 5) are justified by the observation that RM scalar outputs are only meaningful comparatively under the Bradley-Terry model, not in absolute terms (Section 4.2, line 172). EST provides an intuitive "budget equivalence" interpretation.
- **Scalability with batch size**: Figure 3 and Table 14 (Appendix K.2) show that average BWR increases with K from 3 to 20 across all LM-RM pairs, with Mistral achieving BWR > 0.50 for 100% of batches at K=20.
- **Transparent failure analysis**: The Qwen-Armo pair's weaker performance (median BWR 0.54, lowest in Table 1) is diagnosed as caused by left-skewed reward distributions, with explanation in Appendix G.1 (line 217).

## Weaknesses

### Fatal
None

### Major
- **Absence of adaptive baselines**: The paper's central claim is that AdaBoN outperforms uniform allocation. While Figure 3 (line 232) includes "Best-of-N" and "Random" as additional methods, the body text never discusses or defines what these baselines do. More critically, there are no adaptive baselines that use the *same exploration data* but apply simpler allocation rules (e.g., allocating remaining budget proportional to exploration sample variance, or inversely proportional to the current exploration maximum). Without at least one such baseline, it is impossible to determine whether AdaBoN's specific greedy marginal-gain strategy drives the improvement, or whether *any* non-uniform allocation informed by exploration samples would achieve comparable gains. The evidence demonstrates that some adaptivity beats no adaptivity, but not that AdaBoN's particular approach is what matters.

### Minor
- **Narrow exploration fraction ablation**: The paper tests d ∈ {0.60B, 0.70B, 0.75B, 0.80B} (line 242). With d = 0.75B and B = 120, K = 5, exploration consumes 450 of 600 total queries, leaving only 150 for adaptive allocation. The ablation excludes lower exploration fractions (e.g., 0.25B, 0.50B) where the adaptive component would have substantially more budget, limiting understanding of the exploration-exploitation tradeoff.
- **Modest practical effect sizes**: Median BWRs of 0.54–0.62 (Table 1) are consistently above 0.50 but represent small absolute gains. For Qwen-Armo, 22% of batches perform worse than uniform (Table 2b, 78%). The paper does not discuss the practical magnitude of savings (e.g., dollar cost or wall-clock time in a realistic deployment scenario).
- **Decoding strategy not controlled**: Using "the default decoding strategy for all LMs" from Hugging Face (line 215) means temperature and other generation hyperparameters are not controlled across models. The paper should acknowledge that different decoding strategies could affect sample diversity and thus the shape of reward distributions.

### Trivial
None

## Nice-to-Haves
- Add simple adaptive baselines using the same exploration data to isolate AdaBoN's specific contribution from the general value of adaptivity.
- Broaden the d ablation to include lower exploration fractions (0.10B–0.50B).
- Briefly discuss practical deployment savings (cost, latency).
- Report confidence intervals on per-batch BWR estimates (currently only median and quartiles across batches).

## Removed Points
These points are flagged to be removed, treat them with caution.
- **EST "arg max" notation concern**: The harsh critic claimed Equation 5 (line 184) uses "arg max" where "max" should be used. However, "arg max" is correct—it returns the largest N for which AdaBoN ties or beats uniform(N), and the expectation gives the expected survival time. Not an author error.
- **Missing related works**: Cannot verify existence of external works not in the paper.
- **Formatting/style issues**: Parser artifacts, not author errors.
- **Missing appendix content**: Appendices are stripped by the parser; claims about missing proofs or details cannot be verified.

## Novel Insights
The paper introduces two useful evaluation metrics for adaptive allocation methods: Batch Win Rate (BWR) measures the probability of beating uniform allocation on the same budget, while Expected Survival Time (EST) quantifies how large a uniform budget would need to be to match the adaptive method. EST in particular offers an intuitive "budget equivalence" interpretation that practitioners can directly use. The paper also provides a clean demonstration that reward distributions across diverse LM-RM pairs are smooth and well-approximated by Gaussian KDE (Section 3.1), which is a useful empirical observation.

## Suggestions
- Add at least one adaptive baseline (e.g., variance-proportional or random non-uniform allocation using the same exploration data) to isolate AdaBoN's specific contribution.
- Expand the d ablation range to lower values (0.25B, 0.50B).
- Briefly discuss practical deployment implications (cost savings, latency).
- Consider reporting confidence intervals on per-batch BWR estimates.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>