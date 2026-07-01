## Summary

RADAR augments neural VRP solvers to handle asymmetric distance matrices via two contributions: (1) SVD-based node embeddings that encode static asymmetry by concatenating left and right singular vectors scaled by singular values, and (2) replacing softmax with Sinkhorn normalization in encoder attention to produce doubly-stochastic attention matrices that capture dynamic asymmetry. The method is evaluated on 17 synthetic VRP variants and 3 real-world tasks, consistently outperforming prior neural methods and generalizing zero-shot from size-100 training to sizes 200/500/1000.

## Strengths

- **Principled problem decomposition into static and dynamic asymmetry.** The distinction between asymmetry present in the input matrix and asymmetry that emerges during learned interactions is conceptually clean and yields two well-motivated architectural components rather than a single monolithic fix.

- **Mathematically grounded SVD initialization.** Definition 1 formalizes what it means for embeddings to encode directional asymmetry, and the construction \(X = [U\sqrt{\Sigma} \mid V\sqrt{\Sigma}]\) with the explicit reconstruction \(XW_1(XW_2)^\top = U\Sigma V^\top \approx D\) (Eq 3–5) provides a provable foundation lacking in prior informed-initialization strategies (ICAM's k-nearest, RRNCO's distance-based sampling).

- **Extensive and fair evaluation.** 17 synthetic VRP variants (ATSP + 16 asymmetric RouteFinder variants) plus 3 real-world benchmarks, comparing against traditional solvers (LKH3, HGS, PyVRP, OR-Tools), constructive neural solvers (MatNet, ICAM, ELG, ReLD, UniCO, RRNCO), and improvement solvers (GLOP, UDC). Baselines are retrained under unified settings where fair, and the paper is transparent about disabled features (mixed-size training for ICAM/UDC).

- **Clean ablation isolating both components.** Table 6 shows SVD-only and Sinkhorn-only improvements independently, with the full model best at all sizes. The Sinkhorn-only gain (gap 2.08% → 1.82%) confirms the attention change has standalone value beyond better initialization.

- **Strong zero-shot generalization.** Training on size 100 and testing on sizes 200/500/1000 without finetuning yields competitive gaps (ATSP100: 0.72%, ATSP200: 1.01%, ATSP500: 2.13%), demonstrating that the SVD embeddings do not overfit to a specific n.

## Weaknesses

### Major

- **No variance or statistical significance reporting.** Results are reported as point estimates over 1,000 instances with no standard deviations, no confidence intervals, and no information on the number of training seeds used. In comparisons where gaps are small (e.g., RADAR 0.72% vs. ReLD 1.64% on ATSP100; RADAR 1.64% vs. ReLD 1.96% on ACVRP100), the reader cannot assess whether differences are statistically reliable. Table 5 (asymmetry levels study, 50/100 nodes, trained for 1200 epochs) similarly lacks any variance indication. While the large test sets make the observed differences likely genuine, this is a material gap in experimental rigor for a paper that makes comparative performance claims.

### Minor

- **Training algorithm not stated in the main text.** The Method section describes the architecture and decoding procedure but never specifies the loss function or training algorithm (REINFORCE with rollout baseline? POMO's multi-start shared baseline?). POMO is mentioned only as related work and as an augmentation reference in Section 5.4. This detail is likely deferred to the (parser-stripped) appendix, but for a first read it is a surprising and significant omission from the experimental setup.

- **Sinkhorn motivation is rhetorically overstated.** The paper claims (lines 101–107) that softmax attention "only makes \(A_{i,j}\) aware of distance information in the neighborhood of node \(i\)" and that Sinkhorn makes it "aware of the complete neighborhood structure of node \(j\)." In reality, the similarity function \(\text{Sim}(\cdot)\) in Eq. 6 already incorporates \(D_{j,i}\) directly, and the SVD embeddings of node \(j\) encode its neighborhood structure. Sinkhorn's actual contribution is enforcing balanced bidirectional attention flow (double stochasticity), which is a meaningful improvement but is not equivalent to directly injecting \(D_{j,:}\) into the attention score. The paper would be stronger by describing what Sinkhorn *does* (balance incoming/outgoing attention) rather than claiming new "awareness" of distance relations.

- **Connection between SVD theory and attention mechanics is not fully bridged.** Definition 1 shows that \(XW_1(XW_2)^\top \approx D\) with specific projections \(W_1=[I|0]^\top, W_2=[0|I]^\top\). The actual attention mechanism computes \(XW_Q W_K^\top X^\top\), which requires the learned projections to factor as \(W_Q W_K^\top = W_1 W_2^\top\) for the reconstruction to hold. The model can learn this approximately, but the paper does not acknowledge the gap between the neat theoretical guarantee and the implemented computation.

### Trivial

None.

## Nice-to-Haves

- Provide a runtime breakdown showing the SVD step's cost separately from the decoder for n=1000 (Table 6 shows total time 11.57m for the full model at 1000, but isolating the SVD overhead would be informative).
- Show the reconstruction loss \(\|Attention(Q,K) - D\|_F\) before and after training to empirically verify that the SVD structure is exploited by the learned attention weights.

## Removed Points

These points were flagged in the input review but removed with justification:

- "ATSP1000 entry missing from Table 1 but present in Table 6": REMOVED — no method in the ATSP section of Table 1 has ATSP1000 data; the table simply does not include that size for any method. No inconsistency exists.
- "HGS infeasibility rates deferred to Appendix G": REMOVED — the paper already notes this in the main table footnote and defers detailed rates to the appendix, which is standard practice and the content likely exists in the (parser-stripped) appendix.
- "Typo 'real-worlrd' in conclusion": REMOVED per formatting/typo rule.
- "Sinkhorn differentiability and gradient stability not discussed": REMOVED — Sinkhorn's differentiability is standard knowledge; not a meaningful omission.
- Several generic strengths from the input review (e.g., "important problem," "timely topic," "addresses a gap") were removed for lacking concrete grounding in the paper's specific contributions.

## Novel Insights

Beyond the paper's own contributions, the most interesting observation from synthesizing the review is that the SVD-based initialization appears to be the more impactful component — comparing the Table 6 ablation: adding SVD alone drops the gap from 2.08% to 1.19% (0.89pp improvement), while adding Sinkhorn alone drops it from 2.08% to 1.82% (0.26pp improvement). This suggests that for asymmetric VRPs, the initial embedding quality may matter considerably more than the attention normalization choice — a finding that could guide future work on which component to prioritize under a limited computational budget. The coordinate analysis (Section 5.4) showing that RADAR without coordinates outperforms RRNCO with coordinate augmentation is also noteworthy: distance-based embeddings can fully substitute for spatial coordinates in asymmetric settings, and the main value of coordinates is enabling data augmentation diversity rather than encoding structure.

## Suggestions

1. Report standard deviations over at least 3 training seeds and over the 1,000 test instances to address the variance gap.
2. Explicitly state the training objective and algorithm (loss function, baseline method) in Section 5.1.
3. Re-frame the Sinkhorn motivation in Section 4.2 to emphasize balanced bidirectional attention flow rather than "awareness of \(D_{j,:}\)."
4. Add a brief discussion (1–2 sentences) acknowledging that the attention mechanism learns projections that *approximately* enforce the reconstruction guarantee, rather than directly implementing it.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>