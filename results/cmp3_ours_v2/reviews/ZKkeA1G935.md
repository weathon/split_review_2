Now I have all the calibration information I need. Let me write the final review.

**Round 1 Bracket**: After examining the calibration anchors, I place this paper in the 4.0–6.0 range. It is stronger than papers scoring ~4.75 (which lack novel findings or have fundamental methodology issues) but weaker than papers scoring ~5.67 (which execute their methodology cleanly despite clarity concerns). The task ID leakage finding is novel and important, but the missing backbone specification and lack of ablation are significant gaps.

**Calibration Anchors** (all rounds):
- CLDyB (5.67, accepted) — Dynamic CL benchmark with pre-trained models; cleaner execution but similar benchmarking scope
- OCGL (5.00, rejected) — GCL benchmark paper; less novel findings than this paper
- PDGNNs-TEM (5.40, rejected) — GCL method with strong results but novelty concerns; similar to SimGCL's situation
- Dynamic MoE (4.75, rejected) — Graph incremental learning method; less comprehensive than this paper
- TiC-CLIP (6.25, accepted) — Large-scale CL benchmark with massive data; more ambitious than this paper
- "Is multitask all you need" (5.75, rejected) — CL analysis paper; similar in having a methodological critique

---

## Summary

This paper introduces LLM4GCL, a benchmark for evaluating LLMs on Graph Continual Learning (GCL). It makes three contributions: (1) identifying and demonstrating a task ID leakage flaw in the local-testing evaluation protocol used by prior GCL work, (2) benchmarking 9 LLM/GLM-based methods across 7 datasets under a corrected global-testing setup, and (3) proposing SimGCL, which combines ego-graph-derived textual prompts, first-session LoRA instruction tuning, and training-free prototype classification for subsequent sessions.

## Strengths

1. **Clear identification of task ID leakage in local-testing GCL (Section 3.1, Table 1).** This is the paper's strongest contribution. The demonstration that even mean pooling achieves the same near-perfect performance as TPP (95.2 AA, 0.0 AF on Cora) across all datasets is a genuine and important finding. It shows that the local-testing paradigm used by prior GCL benchmarks systematically underestimates task difficulty, degrading class-incremental learning into task-incremental learning. This analysis is clearly presented and independently valuable.

2. **Broad and systematic evaluation.** The benchmark covers 7 diverse datasets across multiple domains (citation, web link, e-commerce networks), 9+ methods spanning GNN-, LLM-, and GLM-based approaches, and two scenarios (NCIL and FSNCIL). The breadth is appropriate for a benchmark study and likely to serve as a useful reference for future work.

3. **SimGCL achieves strong results on most datasets under the corrected global-testing setup.** On Cora, Citeseer, Photo, and Products (NCIL), SimGCL outperforms all baselines by substantial margins (e.g., 84.6 vs 70.8 on Cora average accuracy; 82.1 vs 63.6 on Photo). Even accounting for the unspecified backbone issue, the magnitude of improvement on several datasets suggests the method has real value.

## Weaknesses

### Major

1. **The LLM backbone used for SimGCL in the main results is not specified.** Tables 2 and 3 report SimGCL results, but the paper never states which LLM backbone generates those numbers. The baselines include BERT, RoBERTa, LLaMA, and SimpleCIL (described as "RoBERTa integrated with SimpleCIL"). Figure 3 shows SimGCL with BERT variants and RoBERTa-large, but that figure is specifically about scaling behavior on Arxiv and does not state which backbone was used for the main tables. Since SimpleCIL uses a frozen RoBERTa while SimGCL uses LoRA-tuned LLM, if SimGCL's backbone is larger than RoBERTa-large, the comparison to SimpleCIL is not informative about the method's value. If it uses the same backbone, this should be stated explicitly. This omission makes the paper's central empirical claims unverifiable as presented.

2. **No ablation study isolating SimGCL's components.** SimGCL has three distinct components: (a) ego-graph-derived textual prompts, (b) LoRA instruction tuning on the first session, (c) training-free prototype classification. There is no ablation that isolates their contributions. The comparison to SimpleCIL (frozen RoBERTa + prototype) partially separates the combined effect of (a)+(b) from prototype-only, but does not separate the graph prompt from LoRA tuning. Without an ablation, readers cannot attribute the gains to specific design choices.

3. **SimGCL underperforms SimpleCIL on Arxiv-23 by a large margin, undermining claims of consistent superiority.** In Table 2 (NCIL), SimpleCIL achieves 52.4 average accuracy on Arxiv-23 while SimGCL achieves 38.7 — SimpleCIL is better by nearly 14 points. The paper attributes this to Arxiv-23's sparse graph structure, but the explanation is incomplete: if sparse structure is the problem, why does SimpleCIL (which does not use graph structure at all) perform substantially better? This suggests SimGCL's LoRA tuning can sometimes hurt generalization. The paper's claims of "consistently overperform[ing]" (23 out of 28) should acknowledge this failure mode more directly.

4. **The "20% improvement" claim is imprecise and dataset-dependent.** The Abstract states SimGCL "surpasses the previous state-of-the-art GNN-based baseline by around 20% under the rehearsal-free constraint." The improvement varies substantially: ~29% relative on Cora (65.4→84.6), ~10.5% on WikiCS (66.5→73.5), ~7% on Arxiv-23 (36.1→38.7). The number appears to select a favorable case rather than representing the overall pattern. This should be calibrated to dataset-specific numbers.

### Minor

1. **No variance or statistical significance reported.** All results in Tables 2, 3, and 4 are single numbers with no standard deviations. LLM inference has stochasticity (temperature, dropout, sampling), and LoRA training has run-to-run variance. For a benchmark paper aiming to establish reference results, single-point estimates make it difficult to assess whether differences between methods are reliable.

### Trivial

None.

## Nice-to-Haves

- Add an ablation study comparing: (i) prototype classifier alone (equivalent to SimpleCIL), (ii) + ego-graph prompt, (iii) + LoRA tuning.
- Report mean and standard deviation over multiple runs for all main table entries.
- Provide an efficiency comparison (wall-clock time, parameter counts) with baselines.
- Include a sensitivity analysis for the scaling hyperparameter τ in Equation (2).
- Add a brief discussion of why sparse structure hurts SimGCL but not SimpleCIL on Arxiv-23.

## Removed Points

These points from the Harsh Critic input were removed with justifications:

1. **Claim that prior work may have already analyzed task ID leakage.** The critic speculated "some analysis of this issue presumably exists in the literature" based on CGLB being cited, without identifying any specific paper. Removed as unsubstantiated.

2. **Equation (1) notation issue.** The critic argued redundancy between |Y_b| and the indicator function. Re-reading the definition: |Y_b| is the total labeled nodes in session b, and the indicator filters for class i. The notation is mildly ambiguous but not incorrect. Removed as minor.

3. **LoRA motivation critique.** The critic said "prevent overfitting" is a non-standard LoRA motivation. LoRA can prevent overfitting by reducing the number of trainable parameters — the paper's usage is reasonable. Removed.

4. **"Flawless task ID prediction" phrasing.** The critic argued the text conflates task ID prediction with classification accuracy. Table 1 shows identical AA/AF to TPP, which was established to have 100% task ID accuracy. The claim is well-supported. Removed.

5. **Missing training details (LoRA rank, learning rate, etc.).** Per guidelines, nitpicks about undisclosed hyperparameters and trivial implementation details are removed — these are typically in the appendix (which was stripped during parsing).

6. **Observation numbering artifacts (skipping from ❹ to ❻).** Pure formatting/editing artifact. Removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Specify the backbone.** State explicitly which LLM backbone generates the SimGCL results in Tables 2 and 3. Ideally, include a row with the same backbone as SimpleCIL (RoBERTa-large) for a clean comparison.
2. **Add at least a minimal ablation** comparing: (i) prototype alone, (ii) + graph prompt, (iii) + LoRA tuning, all using the same backbone.
3. **Calibrate the claims.** Replace "20% improvement" with dataset-specific statements. Acknowledge the Arxiv-23 failure directly and discuss what it reveals about the method's limitations.
4. **Report variance.** Provide mean and standard deviation over at least 3 runs for all main table entries.

## Score and Decision

The paper makes one genuinely valuable contribution: it identifies and demonstrates that the local-testing evaluation protocol in prior GCL work permits task ID leakage, inflating reported results. The benchmark and evaluation of 9 methods under the corrected global-testing setup are useful. However, the paper's method claims are compromised by a critical omission: the LLM backbone for SimGCL's main results is never specified, making the central comparisons uninterpretable. The lack of ablation and variance reporting further weakens the empirical contribution. The task-ID-leakage critique is independently valuable, but the method portion requires substantial revision.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>