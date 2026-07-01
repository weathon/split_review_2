Now I have enough calibration data. Let me write the final consolidated review.

## Summary

This paper proposes ARPO, an RL algorithm for training multi-turn LLM-based agents. It identifies that LLMs exhibit elevated token entropy after tool-call feedback (Section 2), and uses this signal to guide adaptive branching exploration at the step level rather than only at the trajectory level. The method combines global (trajectory-level) sampling with partial (step-level) branching at high-entropy tool-call points, along with an advantage attribution estimation. Evaluated on 13 benchmarks spanning math, knowledge-intensive reasoning, and deep search, ARPO consistently outperforms trajectory-level RL methods (GRPO, DAPO, REINFORCE++) across two model families (Llama, Qwen).

## Strengths

1. **Well-motivated empirical observation (Section 2, Figures 1-2).** The finding that LLM token entropy spikes sharply in the first 10–50 tokens after tool-call feedback — and that this effect is stronger for search tools than for Python interpreter feedback — is concrete, measurable, and non-obvious. This observation grounds the method in a real phenomenon rather than being a purely algorithmic invention. The connection between this observation and the proposed adaptive branching is direct and well-articulated.

2. **Consistent positive results across a broad evaluation (Tables 1-2).** The paper evaluates on 13 benchmarks spanning three task families (mathematical reasoning, knowledge-intensive reasoning, deep search) and two model families (Llama3.1-8B, Qwen2.5-7B, Qwen3-8B/14B). ARPO wins or ties on nearly every individual benchmark in Table 1 with an average gain of ~4%, and Table 2 shows consistent gains over GRPO on deep search tasks. This breadth is the paper's strongest empirical card.

3. **Tool-use efficiency is practically significant.** Even accounting for the overstatement discussed below, ARPO using fewer tool calls to achieve better results is meaningful because tool calls (external API calls) are the dominant cost in agentic RL training.

## Weaknesses

### Major

1. **Missing ablation: random/uniform branching at tool-call steps.** The paper's central claim is that *entropy-guided* adaptive branching is what drives improvement. But ARPO's rollout mechanism does two things simultaneously: (a) it branches at tool-call steps, and (b) it uses the entropy signal to decide *where* to branch (Equation 2: branch if P_t = α + β·ΔH_t > τ). Without a control that branches at tool-call steps with the same frequency but using a random or uniform signal instead of the entropy-based threshold, there is no evidence that the entropy signal itself is doing useful work. The improvement could come simply from exploring more diverse paths at tool-call steps — something any branching mechanism would achieve. This is not a minor missing experiment; it goes to whether the paper's stated motivation (entropy as an uncertainty signal worth exploiting) is actually responsible for the gains. The paper does not provide this ablation in the main text, and while Appendix A.2 is referenced for "more ablation and scaling analyses" (line 278), the appendix is not available in this submission.

2. **"Half the tool-call budget" claim is factually overstated.** The paper states ARPO uses "only half the tool-call budget" in the abstract (line 9), the introduction (line 45), the conclusion (line 300), and the caption of Figure 7a (line 278). However, Figure 7a shows GRPO using ~400–480 tool calls and ARPO using ~250–300 — a reduction of roughly 30–40%, not 50%. "Half" would require the ARPO curve to be around 200–240. The claim is overstated by 10–20 percentage points across three prominent locations in the paper. Furthermore, this comparison is shown for only one model (Qwen2.5-7B) and one baseline (GRPO), so generalization of the efficiency claim is unverified.

### Minor

3. **GPG Theorem (§3.3) is a notational variant, not a new theoretical result.** Equation 6 rewrites the standard policy gradient theorem (Sutton et al., 1999) with macro-actions (segments of tokens between tool calls) instead of single-token actions. Any grouping of tokens in an MDP with a Markov property satisfies this formulation; it is mathematically trivial. The paper claims this "encompasses the traditional Policy Gradient Theorem... as a specific instance of our broader GPG framework" (line 170) and calls ARPO "an advanced implementation of the GPG Theorem." This overclaims what is essentially a reparameterization. The paper's empirical results stand on their own and do not need this overclaimed theoretical framing.

4. **Advantage Attribution Estimation (§3.2) is largely a relabeling of standard GRPO.** The paper lists "Advantage Attribution Estimation" as a separate contribution (lines 33, 48). However, Section 3.2 explicitly states: "While we retain the original GRPO loss formulation, our novel partial rollout design explicitly distinguishes the update strategies between shared and individual tokens" (line 142). The "soft" variant (the paper's default) is simply applying the standard GRPO loss to the branched trajectories — the shared vs. individual token distinction arises automatically from importance sampling ratios in GRPO. The "hard" variant is a small modification that performs worse (Figure 5). Listing this as a separate contribution inflates the contribution narrative.

5. **No statistical significance or variance reported.** None of the results in Tables 1-2 include confidence intervals, standard deviations, or significance tests. For small benchmarks (e.g., AIME2024 has 30 problems; a 23.3→30.0 improvement corresponds to 2 more correct answers out of 30), knowing whether reported gains are statistically significant is important for assessing reliability.

6. **Hyperparameter values not stated in main text.** The paper introduces α, β, τ, k, Z, M, N as key parameters (Equations 1-2, Section 3.1) but does not give their values or describe how they were chosen in the main text. A sensitivity analysis for the most critical parameters (α, β, τ) would strengthen the method's credibility.

7. **Computational complexity claim is uninformative (line 116).** The paper states ARPO reduces complexity "from the trajectory-level RL's O(n²) to between O(n log n) and O(n²)." A range spanning from O(n log n) to O(n²) that includes the original bound as its upper endpoint is not a meaningful reduction guarantee. Moreover, the "O(n²)" attribution to trajectory-level RL is not explained — what quadratic operation is being referred to? Standard GRPO's rollout complexity is O(G·n) where G is group size, not O(n²) as a function of trajectory length alone.

8. **LLM-as-Judge bias not acknowledged.** The paper uses Qwen2.5-72B-instruct as the judge for several benchmarks (line 178) while the backbone models are from the Qwen family. Using the same model family as the evaluator is a known potential bias that should be acknowledged.

### Trivial

9. **Rollout diversity analysis is weakly supported (Figure 7b).** The clustering analysis reports 54 vs. 48 clusters without quantitative metrics (silhouette score, Davies-Bouldin index, gap statistic), making the claim of "greater intra-cluster compactness and larger inter-cluster separation" unsupported.

## Nice-to-Haves

- Show tool-call efficiency for at least one additional model-baseline pair.
- Clarify what constitutes the "1k RL samples" from the open-source web search dataset (line 216).
- Report training FLOPs or GPU hours to contextualize the computational trade-off.
- Discuss potential LLM-as-Judge bias when using Qwen2.5-72B to evaluate Qwen-family models.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"Only one baseline for efficiency comparison" framed as a separate weakness** — absorbed into weakness #2 (the overstatement claim already notes the comparison scope).
- **"Unclear reproducibility of pilot study"** — The critic noted details of the pilot study (which model, dataset, sample count) were not stated in the main text, but the paper references Appendix F.1 for agentic RL preliminaries. Since details may be in the stripped appendix, this is not verifiable from the available text. Removed as potentially addressed in supplementary materials.
- **Generic "missing related works" concerns** — Not verifiable without external knowledge.

## Novel Insights

None beyond the paper's own contributions. The entropy pattern observation (Section 2) is the paper's most novel intellectual contribution, and the reviews do not surface additional insights beyond what the paper claims.

## Suggestions

1. **Add a random/uniform branching ablation**: Keep the same rollout structure and total branching budget, but replace the entropy threshold with a random decision or fixed probability at every tool-call step. If ARPO beats this control, the entropy signal is doing useful work. If not, the core claim is unsupported and the contribution reduces to "branching at tool-call steps helps" — a much weaker result.

2. **Correct the efficiency claim**: State the actual measured reduction (e.g., "30–40% fewer tool calls" instead of "half") and show the comparison for at least one additional model and baseline.

3. **Tone down the GPG Theorem**: Remove the claim of theoretical novelty. A brief note that the method is consistent with the standard policy gradient theorem suffices.

4. **Report variance/confidence intervals** for key results, especially on small benchmarks like AIME2024 (30 problems).

5. **State hyperparameter values** (α, β, τ, k, Z, M, N) in the main text and include a sensitivity analysis for the most critical ones.

## Score and Decision

### Calibration Process

**Round 1 (bracketing)**: Retrieved papers across 6 score bands using queries on "reinforcement learning for language model agents with tool use."

**Anchor papers consulted:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `5kMwiMnUip.md` (NEMESIS jailbreaking) | 1.40 | R1 | Far weaker — not a real research contribution. ARPO is clearly above. |
| `8QTpYC4smR.md` (Systematic review) | 1.00 | R1 | Similarly far weaker. |
| `7ienVkNf83.md` (EReLELA) | 3.00 | R1 | Narrower evaluation, less practical significance. ARPO is stronger. |
| `cb4etlGvOY.md` (Towards Autonomous Agents) | 2.50 | R1 | Limited results. ARPO much stronger empirically. |
| `YCu7H0kFS3.md` (EAST — entropic activation steering) | 4.75 | R2 | Most directly comparable (entropy + LLM agents). EAST had simple scenarios and missing ablation. ARPO has broader evaluation but shares the missing ablation issue. |
| `6AUzsrsNUx.md` (MetaTool) | 5.00 | R1 | Tool learning with consistent results but several weaknesses. Comparable quality to ARPO. |
| `F0q880yOgY.md` (Can Language Agents Approach RL) | 4.40 | R1 | Interesting question but limited scope. ARPO is stronger empirically. |
| `HHmnfVQagN.md` (Flow of Reasoning) | 5.75 | R2 | Diversity-seeking LLM training; had overclaiming issues. ARPO is similar in quality. |
| `Dpqw0namg3.md` (LAM Simulator) | 6.00 | R1 | All 6s but rejected. Had clarity issues. ARPO is slightly weaker due to the missing ablation. |
| `aVfDrl7xDV.md` (BOPRO) | 6.25 | R2 | Bayesian optimization for LLMs. Honest about limitations, thorough analysis. ARPO has broader evaluation but less honest about limitations. |
| `hILVmJ4Uvu.md` (TWOSOME) | 6.00 | R1 | LLM+RL for embodied. Clean submission with all 6s. ARPO has comparable empirical breadth but the missing ablation is a more serious gap. |
| `apErWGzCAA.md` (Intelligent Go-Explore) | 7.00 | R2 | FM-guided exploration. Strong paper with some overclaiming but accepted. ARPO is clearly below this quality level. |

**Round 1 bracket**: Narrowest plausible range: **4.5 – 5.5**

**Final score determination**: ARPO sits between EAST (4.75, rejected — similar "missing ablation" weakness) and MetaTool (5.00, rejected — consistent results but weaknesses) / Flow of Reasoning (5.75, rejected despite one 8). The paper has genuine strengths: a well-motivated empirical observation, broad and consistent evaluation, and practical efficiency significance. However, the missing random-branching ablation undermines the core mechanistic claim, and the "half the tool-call budget" overstatement is a clear presentation issue appearing in the abstract, introduction, and conclusion. These weaknesses are significant enough to prevent acceptance at ICLR standards while not warranting a strong reject.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>