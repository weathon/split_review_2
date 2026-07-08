Now I have sufficient calibration data. Let me synthesize the final review.

## Summary

This paper proposes AdaBoN, a two-stage adaptive allocation policy for Best-of-N sampling that estimates per-prompt reward distributions using a first-stage exploration budget, then greedily allocates remaining samples across prompts in a batch. The method requires no auxiliary training, works with any LM-RM pair, and is evaluated across 12 LM-RM pairs, 3 datasets, and 50 batches per setting.

## Strengths

- **Clean problem formulation and simple method.** Section 2.3 formalizes the inference allocation problem clearly, and AdaBoN (Algorithm 2) is straightforward to implement. The two-stage design is explicitly motivated by latency (only two sequential LM calls), a practical concern the paper correctly identifies. **[weight=8.42]**

- **Broad empirical coverage.** The evaluation spans 4 LMs (Mistral-7B, Gemma-7B, Qwen2.5-7B, Llama-3-8B), 3 RMs (RM-Mistral, FsfairX, ArmoRM), 3 datasets (AlpacaEval, HH-RLHF, PKU-SafeRLHF), and 50 random batches per setting. This is substantially more comprehensive than the closest related work (Damani et al., 2024). Tables 1–2 and the ablations over K and B in the appendix represent a real empirical investment. **[weight=8.99]**

- **Model-agnostic with no auxiliary training.** Unlike Damani et al. (2024), AdaBoN requires no learned predictor that must be retrained per domain or LM-RM pair. KDE with Scott's rule is fully automatic, leaving only one hyperparameter (exploration budget d). This is a genuine practical advantage. **[weight=8.78]**

- **EST metric provides a meaningful efficiency lens.** The Expected Survival Time metric (Eq. 5) quantifies how AdaBoN with budget B competes against uniform allocations with larger budgets, giving a concrete measure of computational savings (~25% in several settings). **[weight=8.85]**

## Weaknesses

### Fatal
None.

### Major
None. All identified issues are minor concerns about framing, comparison scope, and presentation — none threaten the paper's core claim that AdaBoN consistently outperforms uniform allocation.

### Minor

- **Framing of "small exploration budget" is misleading.** The paper calls d a "small exploration budget" (abstract, line 9; contribution list, line 28), but the default/recommended value is d = 0.75B (line 242). With B=120, this means 90 of 120 per-prompt samples are used for exploration — the dominant share, not a small one. The method works, but the framing exaggerates how much of the budget is adaptively allocated. **[weight=4.26]**

- **No direct comparison with the most closely related prior work (Damani et al., 2024).** The paper justifies this by citing lack of an existing implementation and computational cost (216,000 MLPs). However, the MLP count calculation appears to be off by roughly a factor of 10 (BK=600, 12 LM-RM pairs × 3 datasets × 600 = 21,600, not 216,000). A comparison on a single representative subset (e.g., one LM-RM pair, one dataset) would have been feasible and would strengthen the paper's claims relative to the only directly competing method. **[weight=2.34]**

- **Cross-prompt reward distribution variation is not quantified.** The paper claims reward distributions are "smooth and easy to learn" (line 27) and shows three histograms (Figure 1), but never quantifies how different the distributions are across prompts. Without measures such as variance of mean reward across prompts or variance in optimal per-prompt allocation, the reader cannot assess the inherent scope for adaptive reallocation. This makes the modest BWRs (0.54–0.62) harder to interpret — are they due to a genuinely useful method or limited opportunity? **[weight=3.96]**

- **No formal statistical significance testing against BWR=0.50.** The paper reports median [Q1, Q3] BWRs across 50 batches and % of batches with BWR>0.50 (Table 2b), which partially addresses variability. However, it does not report standard errors on the batch-level estimates (each estimated from 100 runs) or conduct a sign test against H0: BWR=0.50. For Gemma-Mistral (BWR=0.56 [0.51, 0.59], 76% batches >0.50), the evidence would benefit from stronger statistical grounding. **[weight=6.58]**

- **Disconnect between large-N motivation and experimental regime.** The paper motivates the problem by noting N can be as large as 10,000 (line 23) but experiments max out at B ≤ 160. The experimental regime does not connect to the claimed large-N motivation. **[weight=0.23]**

### Trivial
None.

## Nice-to-Haves

1. Report the **allocation vectors** AdaBoN produces for representative batches (how much variance is there across prompts in allocated samples?). This would directly address whether the adaptivity is meaningfully non-uniform or mostly uniform.
2. Report **raw expected cumulative rewards** (Eq. 1) alongside BWR, so readers can assess effect sizes, not just win rates.
3. Include a **comparison with Damani et al. (2024)** on a single representative LM-RM pair and dataset, even if approximate.
4. Report **wall-clock runtime** of AdaBoN's Monte Carlo estimation step relative to LM inference calls.
5. Test **smaller d values** (e.g., d=0.25B, d=0.5B) to understand how the method performs when the exploration budget is genuinely small.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **"AdaBoN gets 90 free samples for estimation that don't contribute to the final max-reward"** — REMOVED. This is factually incorrect. Equation 2 explicitly includes exploration samples R_{i,1:d} in the max: V_{i,j} = E[max{R_{i,1},...,R_{i,d}, Z_1,...,Z_j}]. The exploration samples DO contribute to the final per-prompt reward. Both AdaBoN and uniform use the same total budget BK. The reviewer partially acknowledges this later but the critique should not stand.

2. **"EST comparison disadvantages uniform since larger N yields diminishing returns"** — REMOVED. This is inherent to the EST metric's design. Diminishing returns for larger N is precisely why EST>B is informative.

3. **"Exploration budget should be treated as a genuine cost; report what happens if exploration samples are excluded"** — REMOVED. The method is designed so exploration samples are never wasted; they always contribute to the final selected response.

4. **Various generic criticisms about missing runtime cost, ablation at smaller d, simpler heuristic baselines** — MOVED to Nice-to-Haves. These are scope extensions, not core flaws.

5. **Critique about missing standard errors on individual batch-level BWR estimates** — The paper averages BWR over 100 runs per batch and reports the cross-batch distribution via [Q1, Q3]. This is standard practice and sufficient; elevated to Nice-to-Have.

## Novel Insights

None beyond the paper's own contributions. The reviewer correctly identifies a framing issue (calling 75% of the budget "small") and notes the MLP count calculation appears inflated, but these are presentation critiques, not novel insights about the method or area.

## Suggestions

1. Fix the MLP count calculation (21,600 vs 216,000) in the Damani et al. justification.
2. Add a sign test or confidence interval on BWR against H0=0.50 for each LM-RM pair.
3. Report allocation vectors to show AdaBoN's allocations are meaningfully non-uniform.
4. Rephrase "small exploration budget" to reflect that d=0.75B is the recommended value.

## Score and Decision

**Round 1 bracket:** 4.0 – 6.5 (between "Inference time LLM alignment" at 4.25 and Damani et al. "Learning How Hard to Think" at 6.50)

**Anchor comparison and narrowing:**

| Anchor | Path | Score | Round | Itemized? | Comparison |
|---|---|---|---|---|---|
| Damani et al., "Learning How Hard to Think" | 6qUUgw9bAZ | 6.50 | 1 | Yes | Most directly comparable paper. AdaBoN has broader evaluation and no training requirement, but Damani's approach is more general (routing + BoN) and their paper is better positioned relative to baselines. AdaBoN's key gap (no comparison with Damani) and framing issues pull it slightly below. |
| "Inference-Aware Fine-Tuning for BoN" | 77gQUdQhE7 | 5.67 | 1 | Yes | Addresses BoN efficiency from a different angle (fine-tuning vs. allocation). Both have similar-level contributions. AdaBoN has broader evaluation but smaller effect sizes. |
| "Large Language Monkeys" | 0xUEBQV54B | 5.00 | 1 | Yes | About scaling laws for repeated sampling, not allocation. Rejected despite interesting findings; its novelty concerns were heavier than AdaBoN's. |
| "Test-Time Alignment via Hypothesis Reweighting" | 8HQS1X2AK4 | 5.33 | 2 | Yes | Different approach to test-time alignment. Similar score range — both have real but limited contributions. |
| "Inference time LLM alignment" | 1Uem0nAWK0 | 4.25 | 2 | Yes | More limited in scope and validation. AdaBoN is stronger empirically. |
| "Adaptive Inference: Theoretical Limits" | hJDTuVQcQp | 4.20 | 2 | No | Theoretical framework, different approach. AdaBoN is stronger empirically. |

**Weighted-item comparison:** My draft's high-weight strengths (8.42–8.99) are comparable to Damani et al.'s (8.71–8.90), confirming the paper has genuinely strong empirical contributions. My draft's highest-weight weakness (6.58 for statistical significance) is notable but not fatal since the paper already provides IQR and % > 0.50 statistics. The framing and missing-comparison weaknesses have lower weights (4.26, 2.34, 3.96) and don't undermine the core claims.

The paper sits above the 4–5 range papers (which have more fundamental flaws) but below Damani et al. (6.50) due to: (i) the paper does not compare against the most directly related method, (ii) the framing inflates reader expectations about effect sizes, and (iii) the modest BWRs (0.55–0.62) make the contribution incremental rather than substantial.

**Final score: 5.5** — The contributions are real but modest; the method is clean and the evaluation is broad, but the framing overstates results and the missing comparison limits the paper's conclusiveness.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>