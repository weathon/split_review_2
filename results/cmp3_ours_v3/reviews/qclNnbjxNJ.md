Now I have all the information needed to write the final consolidated review. Let me construct it.

## Summary

This paper identifies post-treatment selection bias in interventional causal discovery — the problem that samples are selectively retained after interventions, creating dependence patterns that mimic true causal relations. The authors introduce a formal framework (FI-Markov equivalence, F-PAG) that explicitly models this selection, characterize CI patterns that distinguish selection from causation via Type I inducing nodes, and propose F-FCI, a sound and complete constraint-based algorithm. Experiments on synthetic and real-world (Norman gene perturbation) data compare F-FCI against six baselines.

## Strengths

1. **Important and well-motivated problem.** The paper identifies a genuine gap: post-treatment selection in interventional data produces statistical signatures (variant marginal, invariant conditional) identical to true causation, so existing frameworks cannot distinguish them. The gene perturbation and clinical trial examples (Figure 1) are concrete and convincing. This problem framing is a contribution in itself.

2. **Clear non-identifiability demonstration.** Figure 1 shows concretely that structures with/without a direct causal link (a vs. b) and with/without direct selection (c vs. d) produce identical dependence patterns under existing formulations. Figure 4 systematizes CI patterns across 8 structures — this table is the paper's technical backbone and is well-organized.

3. **Soundness and completeness proofs.** Theorems 3 and 4 establish that F-FCI recovers the correct F-PAG under oracle CI tests with both directions proven. For a constraint-based method in a setting with latent confounders and selection, this is the appropriate theoretical standard and strengthens the contribution relative to prior work that proves only soundness.

4. **Novel graphical representation (F-PAG).** Extending PAG with square marks (□) and special edge types (→△, →▲) to capture the finer FI-Markov equivalence class is a natural extension motivated by a demonstrated limitation of PAG (it cannot represent FI-Markov equivalence). The edge types are grounded in identifiable CI patterns involving Type I inducing nodes.

## Weaknesses

### Fatal

None.

### Major

- **Real-world evaluation is too weak to support the claims.** The Norman dataset experiment uses Enrichr for validation — a gene-set enrichment tool that aggregates literature co-occurrence and curated pathway databases, not ground-truth causal graphs. No quantitative metric is provided (e.g., enrichment fold-change over a random baseline, held-out perturbation prediction, precision/recall against gold-standard regulatory interactions). Figure 13 and the appendix present identified links qualitatively, but such a presentation cannot distinguish the method from any alternative that also outputs a plausible-looking graph. This matters because the paper's core claim is about recovering causal relations under selection, and the real-world evidence for this claim is merely suggestive.

- **Practical scope of the distinguishing mechanism is unquantified.** The key disambiguation step (Step 2.3) depends on detecting Type I inducing nodes along inducing paths. The paper explicitly acknowledges this limitation ("The identification of direct causal links and selection structures depends critically on the presence of Type I inducing nodes," p. 9), but does not quantify how often Type I inducing nodes arise in its own synthetic experiments. Without knowing what fraction of edges between intervened nodes are disambiguable, the reader cannot assess whether the ~5% precision gain comes from the claimed mechanism or from incidental differences in how F-FCI uses interventional data. This is a gap between what the theory promises and what the evaluation measures.

### Minor

- **The synthetic evaluation conflates multiple sources of improvement.** The main results (Figure 6) report global DAG Precision and SHD on random graphs containing both causal relations and selection. Higher precision could stem from better management of latent confounders, better use of interventional data generally, or the claimed selection-handling mechanism. The direct disambiguation test is referenced as Table 1 in the appendix; the main body lacks a focused experiment isolating the paper's core claim that F-FCI can *distinguish* selection from causation.

- **Selection mechanism explored is narrow.** The synthetic data uses a specific selection rule (sum of transformed variables within a predefined interval, with functions drawn from linear/square/sin/tanh). Performance under more pathological selection (e.g., discontinuous functions, selection on a single variable — which the paper explicitly scopes out on p. 2) is not explored. This limits confidence in the method's generality.

- **95% confidence intervals with only 10 graph repetitions.** Figure 6 shows very tight CIs averaged over only 10 random graphs. The paper does not clarify whether CIs are bootstrap-based or computed differently, making the apparent tightness somewhat surprising given the small replication count.

- **FI-Markov equivalence sensitivity to the intervention set.** Definition 2 depends on "the same CI patterns between ψ and any intervened variable." Two graphs equivalent under one intervention set may not be equivalent under another. This sensitivity is not stated explicitly, which matters for interpreting experiments that vary graph size \(d\) and sample size \(n\) but not intervention set structure in a controlled way.

### Trivial

None.

## Nice-to-Haves

- A controlled disambiguation experiment using structures from Figure 1 (a vs. b, c vs. d) with varying Type I inducing node presence, reporting the fraction of edges correctly classified as causal vs. selection-induced vs. confounder-induced.
- An ablation that runs F-FCI without Step 2.3 to isolate how much of the precision gain comes from the Type I inducing node refinement versus the standard interventional FCI machinery.
- Quantitative real-world validation — e.g., whether the identified regulatory links are enriched in known databases beyond what a random graph would produce, or a leave-one-out perturbation prediction task using the inferred graph.
- An analysis of Type I inducing node prevalence in the synthetic setup, reported alongside the main results.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Garbled pseudocode (Step 2.2 and 2.3).** The harsh critic notes that Step 2.2 shows all branches with the same CI pattern `(⊥, ⊥, ⊥, ⊥)` and Step 2.3 contains notation that appears garbled. *Removed:* These are PDF parsing artifacts — the original submission does not have these formatting issues. The paper directs readers to Figure 4 for the orientation rules, which is the intended exposition.
- **ε nodes as graph vertices.** The reviewer notes that including noise as vertices is non-standard. *Removed:* The paper clarifies that these nodes are part of the structural causal model representation and that the MAG construction marginalizes them. This is a modeling choice, not a flaw.
- **Heckman-type corrections discussion.** The reviewer suggests the paper should discuss why standard Heckman-type selection corrections do not apply. *Removed:* This is scope creep — the paper is about causal *discovery* (structure learning), not causal *effect estimation*, which is Heckman's domain.
- **Missing runtime/complexity discussion.** The reviewer notes that Step 2.1 iterates over conditioning sets exponentially and that the main text lacks asymptotic complexity. *Removed:* The paper references Figure 11 (appendix) for scalability. While a brief complexity discussion in the main text would be helpful, this is a nice-to-have rather than a weakness, and the information exists in the full submission.
- **Selection function definition complaint.** The reviewer says the paper does not specify whether selection is deterministic or stochastic. *Removed:* Equation (1) and the surrounding text describe the factorization. The data generation procedure (Section 5.1) specifies the selection mechanism precisely.

## Novel Insights

The harsh critic's observation that the core disambiguation mechanism (Type I inducing nodes + hard interventions) has a practical scope that may be narrower than the framing suggests is insightful and not fully addressed by the paper's own limitation discussion. The critic correctly notes that the paper does not quantify this scope in its experiments, creating a gap between the theoretical claim and the empirical demonstration. This is a specific actionable gap that the reviewer identifies beyond what the paper itself acknowledges.

## Suggestions

1. **Quantify Type I inducing node prevalence.** In the synthetic setup, report the fraction of edges between intervened nodes that have a Type I inducing node along the path. This directly informs readers whether the ~5% precision gain is consistent with the mechanism working on its intended targets.
2. **Add a targeted disambiguation experiment.** Construct controlled structures from Figure 1 (a vs. b, c vs. d) and report disambiguation accuracy directly. This would be far more convincing than global SHD/Precision on random graphs.
3. **Strengthen real-world validation.** Add at least one quantitative metric — e.g., enrichment of identified links in known databases compared to random graphs, or a held-out perturbation prediction evaluation.
4. **Perform an ablation removing Step 2.3** to quantify the contribution of the Type I inducing node refinement separately from the rest of the interventional FCI machinery.
5. **Clarify the CI computation** for confidence intervals in Figure 6 (method, number of bootstrap replicates if used).

## Score and Decision

### Round 1 bracket

Bracket: **5.5 – 7.5**. Based on comparing the paper to three key anchors:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/xByvdb3DCm.md` (When Selection meets Intervention) | 8.00 | 1 | Directly comparable topic (selection bias in interventional discovery). Scored 8.0 despite presentation concerns and incomplete algorithm. My paper proves completeness (stronger theory) but has weaker real-world evaluation. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/G5KbDVAlI6.md` (GRN with Selection) | 4.00 | 1 | Similar topic (selection + latent confounders) but rejected due to scalability concerns and weak real-world experiments (5 genes). My paper has stronger theory and larger-scale synthetic experiments. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/u63OVngeSp.md` (Causal Order from Interventions) | 7.00 | 2 | Interventional causal discovery with mixed reviews (5,8,8,6,8), accepted. My paper has stronger theoretical guarantees (completeness) but weaker real-world validation. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Bp0HBaMNRl.md` (Differentiable Latent Hierarchical) | 6.75 | 1 | Accepted with experimental limitations. My paper is comparable in theoretical strength but has more evaluation gaps. |
| `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/SKulT2VX9p.md` (Interventional Fairness) | 6.67 | 2 | Accepted with comparable scope of evaluation. |

### Narrowing to final score

The paper sits below the 8.0 anchor (which had stronger and more comprehensive experiments) but above the 4.0 rejected paper (which was practically unscalable). It is most comparable to the ~7.0 range papers, which were accepted despite evaluation limitations that could be addressed in revision. The key discriminators are: (a) the real-world evaluation is genuinely too weak, relying only on Enrichr for qualitative validation; (b) the Type I inducing node prevalence is unquantified, creating a gap between theoretical scope and measured improvement. These are real but addressable weaknesses that do not undermine the theoretical contribution.

**Final score: 6.5** — borderline accept. The theoretical framework (FI-Markov equivalence, F-PAG, sound+complete F-FCI) is a genuine contribution to an important problem. However, the evaluation does not fully match the strength of the claims, particularly in the real-world experiment and in quantifying the practical scope of the distinguishing mechanism. With targeted improvements to the evaluation, the paper would make a strong case for acceptance.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>