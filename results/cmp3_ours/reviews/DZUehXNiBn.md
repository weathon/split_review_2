Now I have sufficient calibration context. Let me write the final review.

**My round-1 bracket:** After comparing with anchors at scores 4.75 (Auto-Ensemble, rejected), 5.00 (DAG-TFRC, rejected), 5.25 (Exact Distributed, rejected), 5.50 (TICL, rejected), 5.60 (Extendable, accepted), and 5.80 (Quantized Local Independence, rejected), I place VISTA in the 4.5–6.0 range. The paper has a stronger evaluation than the 4.75–5.25 papers but has substantive issues (MB identification unspecified, real-data overclaims, theoretical independence concern) that distinguish it from the accepted 5.60 paper. I narrow to **5.0**.

Here is the final consolidated review:

---

## Summary

VISTA is a modular divide-and-conquer framework for causal structure learning. It decomposes the global DAG learning problem into Markov Blanket subgraphs, aggregates them via weighted voting with exponential decay, and enforces acyclicity via a Feedback Arc Set (FAS) heuristic. The framework is model-agnostic (can wrap any base learner), parallelizable, and the authors provide finite-sample error bounds and an asymptotic consistency proof.

## Strengths

- **Clean, modular design with formal coverage guarantee.** The three-phase pipeline (divide by MB → weighted voting merge → FAS acyclicity) is well-structured and genuinely model-agnostic. Proposition 3.1 — every true edge appears in at least two MB-induced subgraphs — is simple, correct, and provides the right foundation for the divide-and-conquer strategy.

- **Broad empirical evaluation.** Experiments span 6 base learners (NOTEARS, GOLEM, DAG-GNN, GraN-DAG, SCORE, CAM) across two synthetic graph families (ER, SF) with n up to 300, plus the Sachs real benchmark. This is more extensive than typical for a fusion-scheme paper.

- **The framework is genuinely lightweight and parallelizable.** The aggregation requires only O(|V|²) matrix operations with no solver or iterative training, and the divide phase is trivially parallel. This is a practical advantage over solver-based alternatives like DCILP.

## Weaknesses

### Major

1. **The MB identification algorithm used in experiments is not specified.** The pseudocode (Figure 2) treats `MB_solver` as an opaque parameter, and Section 4 names all base learners but never states what algorithm was used to identify Markov Blankets in the experiments. The only hint is a passing reference — "we also implemented the MB solver used in that work" (line 174, referring to DCILP) — which is insufficient. Since the coverage guarantee (Proposition 3.1) holds only if MBs are correctly identified, and since MB identification is itself a hard problem, the reader cannot assess whether the results depend on an oracle-quality estimator or a realistic one. The paper provides code, but the experimental protocol for MB identification must be stated in the paper itself.

2. **Real-data (Sachs) results contradict the paper's central claim that VISTA "typically increases precision without sacrificing recall."** The conclusion (line 287) makes this claim, but the Sachs data show systematic TPR degradation: GOLEM (0.26→0.18), SCORE (0.18→0.12), GraN-DAG (0.53→0.29). Only DAG-GNN improves TPR (0.12→0.18). While FDR improves substantially in all cases, the claim of "not sacrificing recall" is not supported on the real benchmark and should be qualified. This is not a method failure — GreedyFAS may correctly prune spurious edges that were true edges — but the paper's rhetoric needs to match the evidence.

3. **The theoretical guarantees rely on an independence assumption that is fundamentally violated, and the asymptotic regime does not match the actual setting.** Theorem 3.2 assumes A ~ Binomial(m, p) — votes from different subgraphs are independent. The paper acknowledges this is idealized (line 138), but the violation is severe: subgraphs are learned from the same dataset using the same base learner, with substantial overlap (since MBs overlap). Votes are almost certainly strongly dependent. Corollary 3.3, Theorem 3.4, and Theorem 3.5 are all built on this foundation. Furthermore, Theorem 3.5 requires m = C log n subgraphs per edge for asymptotic consistency, but in sparse graphs with bounded MB size, m is bounded above by a constant (roughly the max MB size) — it does not scale with n. The asymptotic result therefore relies on a regime that does not match the actual setting. The paper acknowledges these limitations in passing but the theorems are presented as operationally meaningful guarantees, which overstates their strength.

### Minor

4. **Improvement over the strongest baseline (NOTEARS) is marginal on synthetic data, while larger gains come from already-poor baselines.** On ER5 (n=100), NOTEARS standalone achieves F1=0.76, VISTA-WV achieves F1=0.79 — a 3-point gain. The larger gains (GOLEM: 0.35→0.60, DAG-GNN: 0.33→0.59) come from baselines that already perform poorly. This pattern suggests VISTA helps most when the base learner is weak, which is useful but tempers the claim that it "reliably enhances performance" of arbitrary algorithms.

5. **The weighting function conflates coverage frequency with directional confidence.** The term (1−e^(−λm)) down-weights edges that appear in few subgraphs regardless of whether all those subgraphs agree on direction. An edge with 2/2 agreement receives the same weight as one with 1/2 agreement when m=2. The paper does not discuss or justify this behavior.

6. **No comparison to other divide-and-conquer frameworks in the main text.** The paper mentions a DCILP comparison in Appendix F.2 (line 174) but no results appear in the main paper. Given that DCILP is the primary related-work baseline, a summary in the main text would substantially strengthen the evaluation.

7. **Sensitivity analysis of λ is limited.** Figure 4 shows only 3 (base learner, graph) combinations, and the paper uses λ=0.5, t=0.7 throughout without clarifying whether these were selected via validation, theory, or convention.

### Trivial

None.

## Nice-to-Haves

- An ablation comparing oracle-provided MBs vs. estimated MBs would cleanly separate the effect of MB estimation errors from the aggregation itself.
- A simple majority-vote baseline (not the deliberately-inclusive NV) would isolate the benefit of the exponential weighting scheme.
- An ablation comparing FAS-before-filtering vs. filtering-before-FAS would justify the claimed ordering advantage.

## Removed Points

- *Faithfulness assumption is too broad* (Section 1 note): This is a generic critique that applies to all constraint-based methods and does not specifically undermine VISTA.
- *NV comparison is misleading*: The paper is transparent about NV's role — it validates the coverage property (line 77–78) — and does not present NV as a competitive baseline. The catastrophic SHD values for NV are reported openly.
- *Runtime comparison is misleading*: The paper explicitly states the speedup comes from the divide-and-conquer design (line 237), not from any algorithmic innovation. This is transparent.
- *Large standard deviations in SHD*: Observation without a specific harm claim.
- *Model-agnostic claim is too broad*: VISTA is model-agnostic in the sense that it wraps any base learner; inheriting the base learner's assumptions is standard and not a flaw in the framework.
- *Conclusion should mention independence assumption*: The paper acknowledges this in the theory section itself (line 138).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Specify the MB identification algorithm** used in experiments in the main text (not just in code). Even a one-sentence statement ("we used the PC-based MB discovery algorithm from [ref]") would resolve this.
2. **Qualify the real-data claims** to honestly reflect the TPR degradation observed on Sachs. Replace "typically increasing precision without sacrificing recall" with a more measured statement.
3. **Reframe the theoretical guarantees** as qualitative guides informed by an idealized setting, and explicitly note that the asymptotic regime (m scaling with n) does not apply to sparse graphs with bounded MB size.
4. **Add a simple majority-vote baseline** and a brief summary of the DCILP comparison to the main text.
5. **Discuss the coverage-frequency issue** in the weighting function: justify why down-weighting by m regardless of directional agreement is appropriate, or propose a modification.

## Score and Decision

**Calibration anchors used (all rounds):**
- `Uj0h13lVrR` — avg 1.00, round 1: Strong reject, topic unrelated to CSL.
- `nSDOkm0SKo` — avg 1.00, round 1: Strong reject, topic unrelated.
- `JzFLBOFMZ2` — avg 3.20, round 1: LLM-supervised CSL; limited empirical evaluation, weaker than VISTA.
- `DUfwD5yiN4` — avg 5.25, round 1: Exact distributed BN learning; compared to only one baseline, similar evaluation breadth issue.
- `Lxst78Rrwj` — avg 5.00, round 2: Causal graph via distributional invariance; also a new framework with theoretical + empirical contributions.
- `UAkVjK00Wv` — avg 4.75, round 1: Auto-ensemble BN structure learning; limited novelty concern, weaker evaluation than VISTA.
- `mGmx41FTTy` — avg 6.33, round 1: Topological ordering for DAGs; stronger theoretical grounding, comparable real-data evaluation.
- `3n6DYH3cIP` — avg 5.60, round 1: Extendable BN structure learning; accepted, solid theory + experiments.
- `6O8lh1jIwI` — avg 5.00, round 1: DAG-TFRC for root causes; optimization not specified — similar specification gap to VISTA's MB issue.
- `9UGAUQjibp` — avg 5.80, round 1: Quantized local independence for RL; theory-implementation misalignment.

**Bracket:** Round 1 placed VISTA in 4.5–6.0. Round 2 narrowed to 5.0 based on comparison with papers at scores 4.75–5.80, where VISTA's evaluation breadth and clean design exceed the lower end but its combination of unspecified MB method, overclaimed real-data results, and theory on violated independence assumptions prevent it from reaching the upper end.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>