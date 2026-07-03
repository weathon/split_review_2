Now I have all the information I need. Let me finalize the review.

## Summary

This paper identifies and formalizes the problem of post-treatment selection in interventional causal discovery — where samples are selectively retained after intervention (e.g., quality-controlled cells in perturbation experiments). It shows that existing frameworks cannot distinguish post-treatment selection from genuine causation because both produce the same cross-intervention pattern (variant marginal, invariant conditional). The authors introduce $\mathcal{FI}$-Markov equivalence and $\mathcal{F}$-PAG (a graphical representation with novel edge marks), and propose $\mathcal{F}$-FCI, a provably sound and complete algorithm that exploits interventions on Type I inducing nodes to disambiguate selection from causation. Experimental results on synthetic data and the Norman gene perturbation dataset are reported.

## Strengths

1. **Problem identification and formalization**: The paper identifies a genuine, practically-motivated problem (post-treatment selection) that existing interventional causal discovery frameworks cannot handle, and demonstrates formally in Section 2.2 that structures with and without direct causation are placed in the same equivalence class under current formulations because both yield the same pattern of variant marginal and invariant conditional distributions.

2. **Finer-grained equivalence class**: The $\mathcal{FI}$-Markov equivalence (Definition 2) and $\mathcal{F}$-PAG representation (Definition 5) extend beyond standard interventional Markov equivalence by incorporating CI patterns between intervention indicators and variables, enabling distinctions that were previously impossible. The CI pattern table in Figure 4 concretely illustrates how structures (a)/(b) and (e)/(f) — indistinguishable under existing formulations — can be separated using additional interventions on Type I inducing nodes.

3. **Provably sound and complete algorithm**: $\mathcal{F}$-FCI is presented with soundness (Theorem 3) and completeness (Theorem 4) guarantees for recovering the $\mathcal{FI}$-Markov equivalence class under oracle CI tests.

4. **Consistent empirical advantage on synthetic data**: Figure 6 shows $\mathcal{F}$-FCI outperforming six baselines (GIES, IGSP, UT-IGSP, JCI-GSP, FCI-interven, CDIS) in Precision and SHD across graph sizes 10–25, sample sizes 500–2000, and both hard/soft interventions, with 95% confidence intervals over 10 random graphs. The gap widens as problem size increases.

5. **Honest limitation discussion**: Section 6 explicitly states that identification depends critically on Type I inducing nodes and flags identification along Type II-only inducing paths as an open problem, without over-claiming the scope.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **No evaluation on data without post-treatment selection**: All experiments are conducted with post-treatment selection present. Without a control condition without selection, it is impossible to verify that $\mathcal{F}$-FCI's explicit selection modeling does not degrade performance in standard settings where selection is absent. This is important for establishing that the method is safe to apply broadly.

2. **No ablation isolating the core innovation**: The paper does not ablate Step 2.3 (the Type-I-inducing-node disambiguation) to isolate its contribution from other algorithmic components. Since the claimed 5% precision improvement is modest, an ablation is needed to attribute this gain to the paper's core theoretical innovation rather than to other algorithmic differences (e.g., different skeleton discovery, different orientation rule ordering).

3. **Completeness theorem stated informally**: Theorem 4 states that substructures "can be identified by different types of CI patterns," which is a descriptive statement rather than a formal completeness guarantee. The paper does not explicitly claim (or prove) that $\mathcal{F}$-PAG is *maximally informative* for $\mathcal{FI}$-Markov equivalence — i.e., that no finer resolution is possible given the data. This contrasts with the standard PAG literature where maximal informativeness is a key property.

4. **Real-world evaluation is qualitative**: The Norman dataset analysis is evaluated via Enrichr prior knowledge but without quantitative summary statistics (e.g., what fraction of predicted edges are supported by prior knowledge, how this compares to baseline methods on the same data). The main text claims are not backed by quantitative evidence on real data.

5. **Type II limitation acknowledged but not analyzed**: The method's reliance on Type I inducing nodes is honestly stated, but the paper does not characterize how common Type II-only scenarios are or discuss whether the Norman dataset involves Type I or Type II paths. This makes it difficult for practitioners to assess when the method will be effective.

### Trivial

- "DAG Precision" is used as a metric label in Figure 6 but is not explicitly defined in the main text (precision of directed edges? of adjacencies? of entire structures?).

## Nice-to-Haves

- An evaluation on data without post-treatment selection to verify that $\mathcal{F}$-FCI remains competitive with baselines in standard settings.
- An ablation study removing Step 2.3 to quantify the benefit of Type I inducing node detection.
- Quantitative real-data evaluation (precision/recall against Enrichr annotations, comparison against baselines).
- Discussion of the prevalence of Type I vs. Type II inducing paths in biological perturbation data.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

1. **Rendering artifact in Algorithm 1 Step 2.2**: The harsh critic noted that all six conditional branches in Step 2.2 check the same CI pattern tuple `(⟂, ⟂, ⟂, ⟂)`. This is a PDF-to-text extraction artifact — the original submission has distinct CI-pattern tuples in each branch. The mapping is available in Figure 4's table. Removed per the rule that formatting/rendering artifacts are parser errors, not author errors.

2. **Claim that the experimental comparison is unfair/staged**: The harsh critic argued that comparing F-FCI against methods not designed for post-treatment selection is "staged." This misses the paper's purpose: the experiment demonstrates that existing methods confuse selection for causation, which is exactly the problem the paper identifies. Evaluating methods on their own terms (without adapting them) is standard and appropriate. Removed as factually incorrect reasoning about the experiment's purpose.

3. **Claim that the paper should include missing related works**: Removed per rule — the reviewer cannot verify existence of unmentioned work.

4. **Request that the F-PAG be proven maximally informative**: The paper does not claim maximal informativeness for $\mathcal{F}$-PAG, nor is this a standard requirement. The completeness theorem states what is identifiable. Removed as a scope-expansion request that goes beyond the paper's stated claims.

5. **Critique about intervention targets not being explicit in Algorithm 1 input**: The algorithm's input specification on line 202 already states "interventional targets $\mathcal{I}$" as input. Removed as factually incorrect.

6. **Strength Finder generic praise**: Generic statements about the problem being "important" were dropped per the rule that drops generic or superficial strengths. The remaining strengths are concrete and grounded.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add an experimental condition without post-treatment selection to rule out performance degradation in standard settings and demonstrate that the selection-modeling machinery does not harm performance when selection is absent.
2. Include an ablation removing Step 2.3 to isolate the contribution of Type I inducing node detection from the rest of the algorithm.
3. Provide quantitative metrics for the real-world evaluation (e.g., precision/recall against Enrichr annotations) and ideally a baseline comparison on the same data.
4. Strengthen Theorem 4's formulation to clarify whether $\mathcal{F}$-PAG is maximally informative for $\mathcal{FI}$-Markov equivalence, or at minimum state the formal sense in which the algorithm is "complete."
5. Add a brief discussion or analysis of when Type I vs. Type II inducing paths arise in practice to help practitioners understand the method's coverage.

**Calibration**: The calibration dataset was inaccessible, so I could not retrieve anchor papers with known human scores. In the absence of calibration anchors, the score is based on my assessment of the paper's content against ICLR's scoring scale.

The paper makes a genuine contribution by identifying an overlooked problem (post-treatment selection) and providing a principled formal framework and algorithm. The theoretical development is sound, and the synthetic experiments show consistent improvement. However, the experimental validation has gaps — no control without selection, no ablation, qualitative real-world evaluation — that prevent the evidence from fully matching the strength of the claims. These are all addressable in revision and are not fatal flaws.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>