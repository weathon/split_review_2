Now I have all the calibration information I need. Let me write the final consolidated review.

## Summary

This paper proposes two new aggregation algorithms—Optimal Weight (OW) and Inverse Surprising Popularity (ISP)—for combining multiple LLM responses. OW is a Bayesian-optimal weighted voting scheme that uses agents' accuracies (first-order information) as weights. ISP is a counterfactual variant of surprising popularity that leverages only second-order information (answer correlations) and is proven to have higher expected advantage than majority voting. The paper validates both methods on synthetic data, UltraFeedback, MMLU, and a real-world healthcare dataset (ARMMAN), using 8 LLMs from 4 families, showing consistent improvements over majority voting.

## Strengths

1. **Principled derivation of the Bayesian-optimal aggregator (Section 3).** Given the model assumptions (conditional independence + random shuffle), OW's weight formula ω_i = log(x_i(K-1)/(1-x_i)) follows cleanly from the posterior. Theorem 1 proves this is Bayesian optimal among *all* aggregators (not just linear ones), and Corollary 2 shows MV is optimal under homogeneity. The connection to the Bradley-Terry model (Corollary 1) provides theoretical grounding for a widely-used preference model.

2. **The ISP algorithm is a genuinely novel variant of surprising popularity (Section 4.2).** Replacing SP's conditioning on each agent's actual answer with an average over all answers the agent did *not* give is a non-trivial modification with a clear motivation (SP underperforms MV in LLM settings because systematic biases are less pronounced than in human crowds). Theorem 2 provides explicit closed-form expressions for the expected advantage differences, and Theorem 3 gives a finite-sample convergence guarantee at rate O(1/√M).

3. **Comprehensive empirical scope.** The evaluation spans synthetic data (matching the model assumptions), standard NLP benchmarks (UltraFeedback with K=2, MMLU with K=4), and a real-world healthcare application (ARMMAN, K=2), using 8 LLMs from 4 families (GPT, Qwen, Llama, Phi). Per-question comparison (Table 4) and breakdown of disagreement subsets provide clear insight into where improvements come from. The t-statistics confirm statistical significance across all three datasets (12.53, 23.39, 3.22).

4. **Practical unsupervised variants.** OW-L and OW-I (Section 5.2) address the key limitation that true accuracies are usually unavailable, providing usable methods that still outperform MV across nearly all 16 ensembles (97.92% of cases for OW-L per line 313).

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **σ_K function discrepancy between abstract and main text.** The abstract (line 25) defines σ_K(x) = x²/(K-1+x²), while the main text (line 73) defines σ_K(x) = eˣ/(K-1+eˣ). These are different functions yielding different inverse weights. The main-text version (eˣ/(K-1+eˣ)) is the correct one for the Bayesian optimality claim—its inverse σ_K⁻¹(x)=log(x(K-1)/(1-x)) produces the claimed weight formula. The abstract's quadratic version does not yield the Bayesian optimal aggregator. This is a presentation error that must be corrected, as the abstract is the most-read part of the paper.

2. **Theorem 2 proves an ordering of expected *advantage*, not expected *accuracy*.** The theorem states E[Adv_ISP(s*)] ≥ E[Adv_MV(s*)] ≥ E[Adv_SP(s*)]. While the paper (line 205) notes that "effective aggregation requires the correct label s* to attain the largest advantage," the relationship between E[Adv(s*)] and P(Adv(s*) > max_{s≠s*} Adv(s))—i.e., accuracy—is not formally established. The experiments (especially the synthetic results in Table 2, which exactly match the model assumptions) empirically confirm the accuracy ordering, so this is not a fatal gap. But the theoretical claim is slightly overstated relative to what is proved: "outperforms" is clarified as being about advantage, yet the paper's overall framing is about accuracy. The authors should either provide a lemma connecting expected advantage to accuracy or be more precise about the scope of the theoretical claim.

3. **Evaluation lacks natural baselines beyond MV and SP.** The paper compares against MV and SP (plus Single Best as an oracle), but confidence-based aggregation methods (cited in related work: Chen et al. 2023a; Fu et al. 2025) are never implemented. A simple confidence-weighted vote using each LLM's output probabilities is feasible in the same unsupervised setting and would help calibrate how much value the theoretical machinery adds relative to simpler approaches. Similarly, performance-weighted voting using held-out validation accuracies directly parallels OW-L/OW-I and could have been included. Without these comparisons, the narrative that OW/ISP go "beyond" MV is less precisely quantified.

### Trivial

4. **OW-L and OW-I produce identical results across all three datasets (Table 3).** On UltraFeedback (73.66%), MMLU (90.37%), and ARMMAN (85.78%), OW-L and OW-I achieve exactly the same accuracy. ISP matches both on ARMMAN (85.78%). The paper does not remark on this coincidence. While likely explainable (e.g., the second-order information uniquely identifies the accuracy parameters under the model), the identity deserves a brief comment.

## Nice-to-Haves

- **Computational cost discussion.** ISP requires estimating N² conditional probability tables from M questions, and OW-L solves an optimization over N parameters. A note on overhead compared to MV (O(N) per question) would improve practical usability.
- **Discussion of ARMMAN results.** The 0.54% absolute improvement over MV is the weakest result across all experiments, and all three methods converge to the same accuracy. A more candid discussion (ceiling effect? limited headroom for aggregation in this setting?) would strengthen the paper.
- **Per-question variance and failure modes.** While the t-statistics and per-question counts (Table 4) are informative, a brief discussion of cases where ISP or OW performs *worse* than MV would help characterize boundary conditions.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Formal discrepancy in the definition of σ_K between abstract and main text" called "Evidential."** This is kept as Minor weakness #1 above—it is a real error, but it is a presentation error in the abstract, not an evidential flaw. The main-text theory is self-consistent. Downgraded from "Critical/Evidential" to Minor.
- **"Inequality chain on line 164 conflates model property with empirical observation."** The paper states P(A_i=s₂|A_j=s₁) ≤ P(A_i=s₂|A_j=s₂) under the model assumptions and then notes this "suggests that humans tend to assign higher predictions to answers that match their own." This is a reasonable analogy/motivation drawn from the SP literature, not a conflation. Removed as misunderstanding.
- **"Missing discussion of when random shuffle is lossless."** The paper explicitly defers this to Appendix B.1 (line 49). The appendix exists in the original submission. Removed per hard rule about appendix content.
- **"The random shuffle and conditional independence impose a specific covariance structure."** While technically true of any model with assumptions, this criticism is generic (all models impose structure) and not a specific identified problem with the paper's claims. Removed.
- **"Strongest Single Best is not a fair baseline."** The paper already notes this explicitly (line 287: "Single Best functions as a clairvoyant oracle rather than a fair baseline"). Removed as already addressed.
- **"MV never achieves best performance — could be misleading."** The paper clarifies with exact percentages and notes ties are counted. This is sufficiently clear. Removed.
- **"No discussion of computational cost."** Moved to Nice-to-Haves.
- **"ARMMAN results only 0.54% improvement."** Moved to Nice-to-Haves with softened framing.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's observations about the advantage-versus-accuracy gap and the missing baselines are useful but do not constitute novel insights about the paper's topic.

## Suggestions

1. **Fix the σ_K formula in the abstract** to match the main text (eˣ/(K-1+eˣ) instead of x²/(K-1+x²)).
2. **Bridge the advantage-to-accuracy gap.** Add a brief lemma or simulation-based argument showing that the expected advantage ordering implies accuracy ordering under the model's symmetric setting (the synthetic experiments in Table 2 already confirm this empirically).
3. **Add at least one simple alternative baseline.** A confidence-weighted vote using softmax probabilities from each LLM is straightforward to implement and would anchor the practical value of the theoretical contributions.
4. **Explain the OW-L = OW-I identity** with a brief comment in Section 5.2 or the results discussion.

**Bracket reasoning:** After Round 1 calibration, I identified the plausible range as 5.5–7.0. The strong-reject anchors (avg ~1.0) and reject-range anchors (avg 3.0–3.3) are clearly below this paper's quality. The borderline/accept-range anchors include "Truthful Aggregation of LLMs" (5.25, Reject—less thorough experiments, incremental contribution), "Model aggregation: minimizing empirical variance" (6.00, Accept—similar topic but no theoretical guarantees), and "Balancing Act: Diversity and Consistency in LLM Ensembles" (6.25, Accept—SOTA empirical results but weaker theory and disconnected experiments). Our paper has stronger theory (Bayesian optimality proof) and more thorough experiments (8 models, 4 families, 3 datasets + synthetic) than any of these. The weaknesses (σ_K formula error, advantage-vs-accuracy gap, missing baselines) are all minor and addressable. The paper sits cleanly within the accept range, slightly above the 6.00–6.25 anchors but below the 8.00 strong-accept level.

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| 8QTpYC4smR (survey) | 1.00 | R1 | Far weaker; unserious submission |
| nSDOkm0SKo (NN finance) | 1.00 | R1 | Unrelated and weak |
| 5kMwiMnUip (jailbreaking) | 1.40 | R1 | Unrelated and weak |
| cSnbM9SIJJ (multi-agent sim) | 3.00 | R1 | Less rigorous, fewer contributions |
| xFezgECSLa (LLM algo design) | 3.00 | R1 | Different scope, weaker |
| yCEf1cJDGh (LLM aggregation/advertising) | 5.25 | R1 | Less thorough experiments, incremental |
| EW62GvCzP9 (peer prediction eval) | 4.67 | R1 | Related methodology but weaker experiments |
| grM2Yv49cI (model aggregation) | 6.00 | R1 | Very relevant; no theoretical guarantees, unclear hyperparameters |
| Dl6nkKKvlX (LLM ensembles DMoA) | 6.25 | R1 | Very relevant; SOTA empirical but weaker theory, disconnected experiments |
| yaOe2xBcLC (NoVo norm voting) | 6.00 | R1 | Related (LLM aggregation) but different approach |
| ohJxgRLlLt (unsupervised in-context learners) | 5.75 | R1 | Different topic (ICL adaptation) |
| ouRX6A8RQJ (CoT info theory) | 6.40 | R1 | Different topic (CoT interpretability) |

**Initial bracket:** 5.5–7.0. The paper is clearly above the 3.0–5.25 range (rejected papers) and comparable to or slightly stronger than the 6.00–6.25 anchors (accepted papers). It does not reach the 8.0 level of strong accepts.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>