Now I have all the calibration data I need. Let me synthesize my findings and write the final review.

**Calibration Summary:**

| Anchor Paper | Avg Score | Round | Itemized? | Comparison to VISTA |
|---|---|---|---|---|
| nSDOkm0SKo (Financial Markets Neural Net) | 1.00 | R1 | No | Unrelated topic, very weak paper — no comparison |
| 5kMwiMnUip (NEMESIS Jailbreaking) | 1.40 | R1 | No | Unrelated topic |
| JzFLBOFMZ2 (LLM Supervised CSL) | 3.20 | R1 | No | Less structured approach, limited evaluation |
| fSxiromxAq (Sparse Causal Model) | 3.00 | R1 | No | Different methodological focus, less thorough |
| Lxst78Rrwj (Distr. Invariance Causal Graph) | 5.00 | R1 | Yes | Different approach but comparable scope; VISTA has clearer modular design |
| DUfwD5yiN4 (Exact Distributed BN) | 5.25 | R1 | Yes | Most directly comparable; VISTA has broader evaluation and clearer contribution |
| UAkVjK00Wv (Auto-Ensemble D&D BN) | 4.75 | R1 | Yes | Similar D&D approach; VISTA has more thorough evaluation and clearer framework |
| mGmx41FTTy (Two Time-Slices Topology) | 6.33 | R1 | Yes | Strong empirical results; VISTA's framework is more model-agnostic |
| BZYIEw4mcY (Efficient Trustworthy Causal) | 6.00 | R2 | Yes | Solid work with theory; VISTA has broader experiments but weaker theory |
| u63OVngeSp (Deriving Causal Order) | 7.00 | R2 | No | Strong theory + experiments; VISTA's theory is less rigorous |
| ZXs3pkmrRG (TICL Test-Time) | 5.50 | R2 | No | Different paradigm; VISTA has more comprehensive evaluation |
| 9UGAUQjibp (Quantized Local Independence) | 5.80 | R2 | No | RL-focused; less directly comparable |

**Round 1 bracket**: 5.5–6.5. VISTA is stronger than the 4.75–5.25 D&D papers (broader evaluation, clearer contribution, convincing runtime data) but weaker than the 7.0 paper (theory gap, missing experiment details).

**Final score**: 6.0. VISTA's core modular framework is a genuine contribution with broad empirical support. The three major weaknesses (MB solver unspecified, theory independence gap, overclaimed FDR) are significant but fixable, and the strengths (modular design, broad evaluation across 6 baselines, large runtime gains) are decisive enough to place it at borderline accept.

Let me now write the final review.

The score is 6.0 — borderline accept. Decision is Accept.

Wait, let me reconsider. Looking at the anchor papers more carefully:

- The "Exact Distributed" (5.25) had fundamental clarity issues that prevented reviewers from evaluating correctness. VISTA does NOT have this issue — it's clearly presented.
- The "Auto-Ensemble" (4.75) had limited novelty as a refinement. VISTA has a fundamentally new framework.
- The "Efficient and Trustworthy" (6.0) had severe presentation issues but all reviewers gave it 6.

Given VISTA's strengths in empirical breadth and clarity, and the fixable nature of its weaknesses, 6.0 seems right.

Wait, one more thought. The MB solver issue is a genuine concern. If the MB solver used is actually doing most of the work, then VISTA's contribution is diminished. The paper acknowledges this is a modular framework where any MB solver can be plugged in, but NOT specifying what was used in experiments is a real gap.

However, Figure 1 shows MB identification maintaining high F1 while baseline methods degrade — suggesting the MB solver is standard and works well. The paper mentions "we also implemented the MB solver used in that work" for DCILP comparison (line 174), suggesting they used a published MB solver.

I'll keep the score at 6.0.## Summary

VISTA proposes a modular, model-agnostic framework for causal structure learning that decomposes the global problem into Markov Blanket subgraphs, applies any base learner to each subgraph independently, then aggregates via a weighted voting mechanism with acyclicity enforcement. The framework is designed to be fully parallelizable and compatible with arbitrary base learners and MB estimators.

## Strengths

- **Clean, modular design that is genuinely model-agnostic.** VISTA accepts any base learner and any MB estimator, with a transparent pipeline (Figures 2-3) and lightweight edge-level aggregation that avoids solver-based optimization (unlike DCILP). This is a real practical advantage over prior divide-and-conquer approaches.

- **Broad empirical evaluation across 6 base learners** (NOTEARS, GOLEM, DAG-GNN, GraN-DAG, SCORE, CAM), 2 graph families (ER, SF), and multiple graph sizes (30–300). This is substantially more thorough than most divide-and-conquer papers, which typically test with only 1–2 base learners.

- **Significant runtime improvements** demonstrated in Table 3 — e.g., NOTEARS from ~12,500s to ~2,100s at n=300; DAG-GNN from ~17,700s to ~1,960s — driven by the divide-and-conquer design that reduces per-subgraph problem size and enables parallel execution.

- **Theoretical analysis** providing finite-sample error bounds (Theorems 3.2, 3.4) and asymptotic consistency (Theorem 3.5), which is a step beyond prior heuristic-based merging methods that offer no formal guarantees.

## Weaknesses

### Major

1. **Markov Blanket identification solver is never specified.** The paper does not name which MB identification algorithm was used, report its runtime, or provide an ablation of its effect on downstream results. Figure 1 shows MB F1~0.9 at n=300 but gives no indication of how this is achieved. Since the entire pipeline depends on MB quality for both correctness and scalability, and results could vary dramatically with the MB solver chosen, this omission prevents proper evaluation of the claimed scalability. The paper's statement about providing "a flexible interface" (line 59) addresses the framework's modularity but does not excuse the absence of the experimental specification.

2. **Theoretical guarantees rely on an independence assumption that is knowingly violated and inadequately addressed.** Theorem 3.2 assumes votes from different local subgraphs are independent Binomial draws. In reality, subgraphs overlap systematically (every edge appears in at least 2 subgraphs, potentially many more), and all are learned from the same observational data, inducing correlated errors. The paper acknowledges this at line 138 ("subgraphs learned from the same dataset can induce correlations among votes") but dismisses it as a minor caveat, stating the bound should be interpreted as a "qualitative guide." The quantitative bounds in Corollary 3.3 and the asymptotic consistency in Theorem 3.5 inherit this structural flaw, and the paper does not attempt to characterize how correlation affects the bounds.

3. **Claimed "50~80% FDR reduction" is factually inaccurate for several baselines in Table 1 (n=100, h=5).** The paper states (line 178) that "WV reduces FDR by 50~80% relative to the original baselines." Checking Table 1: SCORE's FDR drops from 0.92 to 0.80 (13% reduction), DAG-GNN's from 0.66 to 0.36 (45% reduction), and GraN-DAG's from 0.92 to 0.43 (53% reduction under ER5). While the claim holds for NOTEARS and GOLEM (both ~62%), it does not hold universally as stated. This overclaiming erodes trust in the paper's quantitative narrative.

### Minor

- **Sample size for synthetic experiments is not reported.** The paper specifies graph families, sizes, and out-degrees but omits how many observational samples were generated per dataset — a fundamental experimental parameter needed for reproducibility and interpretation.

- **Large standard deviations in many baseline results** (e.g., NOTEARS TPR 0.74±0.26, SHD 208.80±190.71) make it difficult to assess whether VISTA improvements are statistically significant. The paper reports means and standard deviations but does not perform significance testing.

- **Runtime breakdown is not provided.** Table 3 shows impressive total runtime reductions, but without decomposing time spent on MB identification, subgraph learning, and aggregation, the reader cannot determine where the speedup originates.

### Trivial

None.

## Nice-to-Haves

- Ablation of the GreedyFAS ordering (the paper claims the ordering over threshold-based filtering matters but provides no empirical evidence).
- Precision-recall curves for all baselines, not just the three in Figure 4.

## Removed Points

- *Naive Voting baseline produces catastrophic FDR*: Removed. The paper explicitly uses NV only to demonstrate the coverage property (Proposition 3.1) and as a comparison point; VISTA's primary contribution is WV, not NV.
- *Sachs results are modest*: Removed. The improvements on Sachs (Table 4) are positive and consistent, even if not dramatic (e.g., GraN-DAG FDR from 0.82 to 0.00).
- *DCILP comparison relegated to appendix*: Removed. The paper explicitly states this comparison is in Appendix F.2, and the parser strips appendices.
- *GreedyFAS ordering ablation requested*: Moved to Nice-to-Haves. This is a tertiary detail.
- *Formatting/presentation nitpicks, missing related work, reproducibility concerns about unreleased tools*: Removed per hard rules.

## Novel Insights

None beyond the paper's own contributions. The review confirms the paper's framing: a clean modular framework with broad empirical support but with significant gaps in both experimental reporting (MB solver, sample size) and theoretical rigor (independence assumption).

## Suggestions

1. **Specify the MB solver** used in all experiments (algorithm name, parameters), report its runtime separately, and provide an ablation showing how MB accuracy degrades with graph size and sample size.
2. **Either derive a concentration bound that accounts for overlapping subgraph dependencies, or explicitly downgrade the theoretical claims** from quantitative guarantees to heuristic analysis, removing the implication that the Binomial bounds hold quantitatively.
3. **Correct the overclaimed FDR reduction** statement to accurately reflect per-baseline results.
4. **Report the sample size** for synthetic data in the main text.
5. **Include statistical significance tests** for the main comparisons, given the large standard deviations.

## Score and Decision

| Anchor | Score | Round | Comparison |
|--------|-------|-------|------------|
| DUfwD5yiN4 (Exact Distributed BN) | 5.25 | R1 | Most directly comparable; VISTA has broader evaluation and clearer contribution |
| UAkVjK00Wv (Auto-Ensemble D&D BN) | 4.75 | R1 | Similar D&D paradigm; VISTA has more thorough evaluation and cleaner framework |
| BZYIEw4mcY (Efficient Trustworthy Causal) | 6.00 | R2 | Comparable impact; VISTA broader empirically but weaker theory |
| mGmx41FTTy (Two Time-Slices) | 6.33 | R1 | Strong empirical results; VISTA's framework is more model-agnostic |
| Lxst78Rrwj (Distr. Invariance Causal Graph) | 5.00 | R1 | Different approach, comparable evaluation scope |

**Round 1 bracket**: 5.5–6.5. VISTA is stronger than the D&D papers scoring 4.75–5.25 (broader evaluation across 6 base learners, clearer modular contribution, convincing runtime data) but weaker than the 7.0-level papers (theory gap, missing experimental details).

**Narrowing**: Compared to the 6.0 anchor (BZYIEw4mcY), which had severe presentation weaknesses [-9.99, -9.87, -9.94] and limited experiments [-10.00] but strong theory, VISTA reverses the profile — strong experiments [+9.95, +10.00] and clear presentation but weaker theory [-10.00, -10.00]. Both the MB solver omission [-10.00] and the independence-assumption theory gap [-10.00] are the paper's decisive negative items; these are comparable in impact to the missing experiments [-10.00] and presentation failures [-9.99] of the 6.0 anchor, but VISTA's decisive positive items (broad evaluation [+10.00], runtime gains [+9.95], modular design [+9.85]) are at least as strong as that anchor's top items.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>