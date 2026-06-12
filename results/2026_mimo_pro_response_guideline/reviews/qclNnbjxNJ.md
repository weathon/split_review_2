Now I have all the calibration data I need. Let me finalize the review.

## Summary

This paper identifies post-treatment selection — the selective inclusion of samples after interventions, such as quality control filtering in gene perturbation experiments — as a fundamental and previously unaddressed challenge for interventional causal discovery. It shows that post-treatment selection produces distributional patterns (variant marginal, invariant conditional) that are identical to those produced by true causal relations, rendering existing frameworks unable to distinguish them. The paper proposes: (1) a new causal formulation using augmented DAGs that explicitly model post-treatment selection; (2) a novel finer-grained equivalence class called FI-Markov equivalence; (3) a new graphical representation, F-PAG, with additional edge marks; and (4) a sound and complete algorithm, F-FCI, for recovering the FI-Markov equivalence class from observational and interventional data.

## Strengths

- **Identification of a genuine and practically important problem**: The paper clearly articulates post-treatment selection as a real and overlooked challenge in causal discovery, grounding it in concrete examples from gene perturbation studies (quality control filtering, line 13) and clinical trial per-protocol analysis (line 13). Figure 1 provides a precise graphical demonstration of why existing interventional causal discovery frameworks fail: structures (a) and (b) yield identical CI patterns despite one having a direct causal link and the other not. This is a substantive observational gap in the literature, building on and complementary to the predecessor CDIS work on pre-treatment selection.

- **Systematic characterization of distinguishing CI patterns across 8 canonical structures**: The table in Figure 4 (lines 106–112) provides an explicit enumeration of 6 distinct CI pattern signatures across 8 structural configurations involving causal links, latent confounders, and post-treatment selection. The key insight that hard interventions on a third variable ($X_3$) can disambiguate structures indistinguishable from endpoint-intervention CI patterns alone (line 132) is non-trivial and well-articulated.

- **Novel graphical representation (F-PAG) with principled motivation**: The paper provides a concrete argument (line 184, referencing Figure 5(b) vs (c)) that standard PAG cannot distinguish causal links from inducing-path-mediated dependencies under post-treatment selection, motivating novel edge marks (square $\square$, $\blacktriangleleft$, $\blacktriangleright$) and the concept of Type I/Type II inducing nodes (Definition 6). The F-PAG definition (Definition 5) extends PAG in a principled way.

- **Provably sound and complete algorithm**: Theorem 3 (soundness) and Theorem 4 (completeness) provide formal guarantees for the F-FCI algorithm under oracle CI tests. The algorithm design follows a principled decomposition: Step 1 recovers the skeleton from observational data, Step 2 leverages interventional CI patterns with four sub-steps including refinement via Type I inducing nodes, and Step 3 applies standard FCI rules to remaining edges. This is an improvement over the predecessor CDIS work, which was only sound.

- **Nonparametric and comprehensive experimental setup**: The simulation uses general SEMs with functions randomly drawn from {linear, square, sin, tanh} and non-Gaussian noise (line 275). Six baselines spanning different paradigms (GIES, IGSP, UT-IGSP, JCI-GSP, FCI-interven, CDIS) provide a genuinely informative comparison. Results in Figure 6 are averaged over 10 graphs with 95% confidence intervals across multiple sample sizes and graph dimensions under both hard and soft interventions.

## Weaknesses

### Fatal
None.

### Major
- **Narrow scope of soundness/completeness guarantees**: Theorem 3 states consistency "among intervened variables" and Theorem 4 applies "between a pair of intervened nodes." Step 3 of the algorithm applies standard FCI orientation rules to remaining edges (unintervened variables and cross-edges), but no separate guarantee is provided for these — the paper relies on inherited FCI properties. This should be explicitly stated rather than letting the theorems' titles ("Soundness of F-FCI" / "Completeness of F-FCI") imply coverage of the entire output graph. This matters because it limits the reader's understanding of what guarantees the full algorithm actually provides.

- **Missing ablation: performance without post-treatment selection**: The experiments show F-FCI outperforms baselines when post-treatment selection is present (since baselines are not designed for this setting), but there is no experiment where post-treatment selection is absent. Without this, the reader cannot determine whether F-FCI pays a cost for its generality — i.e., whether it introduces spurious edge marks when the simpler assumptions of existing methods hold. If F-FCI matches baselines under simpler conditions, the case for using it as a default method is much stronger. This is cheap to implement (remove selection from data generation) and would address a natural reader concern.

### Minor
- **Frequency of Type I inducing nodes not quantified**: The paper's own conclusion acknowledges that identification of direct causal links and selection structures "depends critically on the presence of Type I inducing nodes" (line 291). When inducing paths consist solely of Type II inducing nodes, the method falls back to standard PAG-level resolution. The paper does not quantify how often Type I inducing nodes appear in the synthetic experiments, making it difficult to assess how often the fine-grained identification actually activates and how much of the empirical improvement comes from the novel contribution versus inherited FCI behavior.

- **Underspecified experimental details**: (a) The number of intervention environments $K$ is not explicitly stated in Section 5.1; (b) how intervention targets are chosen (randomly? per variable?) is underspecified; (c) the sample size per environment is not stated (only total sample sizes $n=500, 1500, 2000$ are given); (d) the claim "average precision of over 5% in most configurations" (line 277) is ambiguous — whether this is absolute or relative improvement.

- **Real-world application section is very brief**: Section 5.2 consists of only three sentences (lines 283–285) plus a reference to an appendix figure. Given that the paper's motivation centers on real biological applications (gene perturbation, clinical trials), demonstrating that F-FCI identifies selection structures that baselines miss — and that these match known quality control effects — would strengthen the practical contribution considerably.

### Trivial
None.

## Nice-to-Haves
- Tabulate the frequency of Type I inducing nodes encountered during Step 2.3 alongside experimental results.
- Expand Section 5.2 with a concrete demonstration that F-FCI identifies selection artifacts missed by baselines in the Norman dataset.
- Explicitly note in the algorithm description that Step 2.3 requires hard interventions on inducing nodes — a practical constraint affecting applicability.

## Removed Points
These points are flagged to be removed, treat them with caution:
- Parser-related issues with Step 2.2 orientation conditions showing as $(⊥, ⊥, ⊥, ⊥)$ on all six rules (lines 216–226) — these are parser artifacts where the actual CI pattern specifications were lost during PDF extraction. The original paper presumably has correct and distinct conditions.
- "Eight types of edges" claim in Definition 5 potentially listing duplicates — likely a parser rendering issue where distinct mathematical symbols collapsed.
- Formatting/typo nitpicks — parser artifacts, not author errors.

## Novel Insights
The paper's core novel insight is that post-treatment selection creates a systematic blind spot in interventional causal discovery: the variant marginal / invariant conditional distribution pattern that existing frameworks use to identify causal relations is exactly replicated by post-treatment selection. The resolution — leveraging hard interventions on third-variable Type I inducing nodes to block selection effects on latent confounders, thereby disambiguating causal from selection-mediated dependencies — is a genuine technical contribution. This complements the predecessor CDIS work on pre-treatment selection and together they address two distinct temporal placements of selection bias in the causal pipeline.

## Suggestions
- Add an ablation experiment removing post-treatment selection to demonstrate F-FCI's robustness under simpler conditions.
- Table the frequency of Type I inducing nodes during Step 2.3 alongside experimental results, so readers understand when fine-grained identification activates.
- Clarify in the text (not just through theorem scope) that the soundness/completeness guarantees of Theorems 3–4 apply to intervened-variable pairs, with Step 3 relying on standard FCI properties for remaining edges.

## Calibration Report

**All anchors retrieved across rounds:**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| Financial Markets NN | 1.0 | R1 | Very different topic; reject for poor quality |
| KL Divergence GFlowNets | 1.0 | R1 | Very different topic; reject for poor quality |
| Scaling Illumination | 0.5 | R1 | Very different topic; irrelevant |
| Balancing Re-ID | 1.0 | R1 | Very different topic; reject for poor quality |
| DFITE treatment effect | 3.0 | R1 | Causal estimation; weaker methodology |
| Potential Outcomes Hidden Confounders | 3.25 | R1 | Causal estimation; narrower scope |
| Causal Bayesian Optimization | 3.4 | R1 | Causal optimization; incomplete theory |
| Best of Both Worlds | 3.0 | R1 | Causal prediction; weaker contribution |
| **GISL Gene Regulatory Network** | **4.0** | **R1** | **Very related topic; much weaker execution (5 nodes, scalability, presentation)** |
| Learning Latent SCM | 4.0 | R1 | Causal discovery; limited assumptions |
| Predicting perturbation targets | 4.25 | R1 | Related biological causal discovery |
| Mitigating Unobserved Confounding | 4.25 | R1 | Causal estimation with diffusion |
| CiVAE post-treatment variables | 6.25 | R1,R2 | Related topic; different approach, significant weaknesses |
| Domain Counterfactuals | 5.75 | R1 | Causal counterfactuals; narrower scope |
| ShadowCatcher collider bias | 6.75 | R1,R2 | Selection/collider bias; different framing |
| **Differentiable Causal Discovery Latent** | **6.75** | **R1** | **Causal discovery with latents; comparable contribution level** |
| TICL Test-Time Learning | 5.50 | R2 | Interventional causal discovery; different approach |
| Interventional Fairness | 6.67 | R2 | Interventional framework applied to fairness |
| **RLCD Versatile Causal Discovery** | **7.50** | **R2** | **Causal discovery with latents; well-written, strong theory** |
| Efficient Trustworthy Causal Discovery | 6.00 | R2 | Causal discovery with latents; adequate |
| **Deriving Causal Order** | **7.00** | **R2** | **Interventional causal discovery; similar contribution level** |
| IEM Exchangeable Mechanisms | 6.50 | R2 | Causal structure learning; different framing |
| **When Selection meets Intervention / CDIS** | **8.00** | **R1,R2** | **Same research group, predecessor paper on pre-treatment selection; very closely related** |

**Calibration reasoning:**

Round 1 bracket: **6.5–8.0**. The most relevant anchor is the CDIS predecessor paper (same group, pre-treatment selection, avg 8.0). The current paper addresses a complementary problem (post-treatment selection) with comparable rigor and additional theoretical contributions (completeness guarantee, F-PAG). However, the current paper has weaknesses CDIS lacked: the narrow scope of soundness/completeness guarantees and a missing no-selection ablation. Papers in the 6.5 range (RLCD at 7.5, Deriving Causal Order at 7.0) have similar contribution profiles — solid theory, good experiments, some gaps. The rejected GISL paper (4.0) addresses a similar topic but is far weaker; this confirms the current paper is well above the reject threshold.

Round 2 narrowed to **6.5–7.5**. The current paper is clearly above the 6.0–6.5 range (papers with narrower contributions or weaker theory) and below the 8.0 of CDIS (which had uniform reviewer enthusiasm despite its own weaknesses). The missing ablation and narrow guarantee scope are concrete gaps that separate this from the 8.0 range, but the core contribution — identifying post-treatment selection, developing F-PAG, and providing sound+complete algorithm — is strong.

Final score: **7.0**. The paper makes a genuine and well-executed contribution to causal discovery. The identification of post-treatment selection as a fundamental challenge is novel and well-motivated. The theoretical framework is systematic, the F-PAG representation is principled, and the experiments are comprehensive. The weaknesses (narrow guarantee scope, missing ablation, underspecified experiments) are real but bounded — they don't undermine the core contribution but prevent a higher score.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>