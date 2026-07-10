Now let me produce the final review.

## Summary

HighClass presents a metagenomic classification framework that replaces seed-and-extend alignment with hash-based token-to-taxon lookups, using variable-length QA-Token vocabularies, quality-aware scoring, and gradient-based sparsification. The core architectural insight — that taxonomic classification only needs to know *which* taxa contain discriminative subsequences, not *where* they align — is well-motivated. The paper includes a transparent ablation study and rigorous statistical reporting.

## Strengths

- **Transparent ablation study (Table 3).** The paper honestly shows that QA-Token + MetaTrinity alignment achieves 86.2% F1 (nearly matching MetaTrinity's 86.6%), and that replacing alignment with hash indexing costs about 1.1 pp of accuracy in exchange for speedup. This lets readers see exactly where the gains come from.

- **Rigorous statistical reporting.** The use of 95% bootstrap CIs over 10 independent runs, Wilcoxon signed-rank tests with Holm-Bonferroni correction, and Cohen's *d* effect sizes represents genuinely good practice often neglected in this area.

- **Informative computational cost breakdown (Table 5).** Per-read time decomposed by operation (containment search, seeding, chaining vs. token extraction, lookup, scoring) makes the source of the speedup concrete and verifiable.

- **Conceptually clean core idea (Sections 3.3, 5.5).** The paper correctly identifies that precise alignment positions are unnecessary for taxonomic classification, motivating a hash-based token mapping architecture.

## Weaknesses

### Major

- **Results reported for only 1 of 4 claimed benchmarks.** Section 5.3 states evaluation on CAMI II Marine, CAMI II Strain, HMP Mock communities, and Zymo Standards. All reported results (Tables 1–6) are for CAMI II Marine only. No results are presented for the other three datasets. Since CAMI II Strain involves near-identical genomes (≥95% ANI) where discriminative token patterns are much harder to learn, this omission critically weakens support for the paper's core claim that alignment can be replaced by token matching. The claim of "comprehensive evaluation" (Sections 1.3, 7) is contradicted by the evidence presented.

- **Internal numerical inconsistency in sparsification claims.** The abstract and Section 1.3 state sparsification "preserves 94% accuracy." Section 5.4.3 states it "preserves 99.5% relative accuracy." Table 1 shows 85.8% → 85.1% (−0.7 pp), which is 99.18% relative preservation. Three different numbers appear in the paper, none equalling 94%. This is not a minor copy-editing issue — it indicates a breakdown in the chain from data to reported numbers that undermines trust.

- **Undefined baseline in scalability experiment (Table 4).** Table 4 compares HighClass against "Metalign" — a method never introduced in Related Work, not listed among baselines in Section 5.3, and never defined or cited anywhere in the paper. The table is uninterpretable as presented.

### Minor

- **Theory-practice disconnect in the theoretical contribution.** The excess risk bound is claimed as ~0.021, but the stated rate O(√(V|Y|/n)) with V=32,000, |Y|=100, n=10^6 yields √(3.2) ≈ 1.79 — a large discrepancy suggesting a missing normalization factor not explained in the main text. The variance inflation factor of ~31.7 is described as "manageable" without discussing its practical implications (a 31.7× variance increase would substantially weaken concentration guarantees). More importantly, the theory does not inform any design decision in the paper; vocabulary size, quality sensitivity η=1.8, and sparsification ratio are all taken from prior work or heuristics, not derived from the theoretical framework.

- **Limited baseline comparison.** Only three baselines are included: Kraken2 (2019), Centrifuge (2016), and MetaTrinity (2023). Several widely used methods (e.g., Bracken, KrakenUniq, CLARK, Kaiju) are absent. The claim that HighClass is "within 1.5% of state-of-the-art" is only as strong as the assumption that MetaTrinity alone represents the full current SOTA.

- **Claim of additive component contributions without supporting evidence.** Section 5.4.3 states that "performance gains from different components are nearly additive" with "interaction effects less than 0.5 percentage points," but no interaction-term analysis, factorial ANOVA, or additive decomposition is presented to substantiate this. Given that the components operate sequentially (tokenization → weighting → sparsification → mapping), interactions are expected and should be demonstrated, not asserted.

- **Unexplained discrepancy between Table 1 and Table 3.** Table 1's "Full Index" shows 85.8% F1, while Table 3's "QA-Token + no sparsification" shows 84.7% F1. Both purport to describe the non-sparsified version but differ by 1.1 pp. The paper does not explain whether these use different indexing strategies (alignment-based vs. hash-based), making them non-comparable.

- **F1/hour metric is non-standard and potentially misleading as a headline claim.** F1/hour = F1 / runtime (hours) has no natural interpretation — F1 is not cumulative over time. Kraken2 (70.0% F1, 0.5h) achieves 140.0 F1/hour, while MetaTrinity (86.6% F1, 2.1h) achieves only 41.2. HighClass's lead on this metric is entirely driven by speed, not accuracy. Using it as a headline comparison (Tables 2, 6) without caveats about its interpretation is potentially misleading.

### Trivial

None.

## Nice-to-Haves

- Expand baseline comparison to include additional widely-used metagenomic classifiers beyond the three reported.
- Provide the missing normalization factor that connects the O(√(V|Y|/n)) rate to the claimed 0.021 excess risk bound.
- Replace the F1/hour metric with a standard accuracy-vs-runtime scatter plot for the Pareto frontier, or add a clear caveat about the metric's interpretation.

## Removed Points

These points are flagged to be removed; treat them with caution.
1. *"Theoretical contribution is unverifiable because proofs are in appendix"* — Removed per guidelines (appendix content stripped by parser should not be penalized). The retained version focuses on the theory-practice disconnect, which is a main-text issue.
2. *"Novelty is largely integration of existing components"* — Removed as a subjective contribution judgment; the paper is transparent about building on prior work.
3. *"Code should be available at submission time"* — Removed per guidelines about reproducibility nitpicks.
4. *"Inconsistent speedup claims (4.2×, 4.1×, 3.8×)"* — The paper explicitly explains these at line 300: 4.2× is pure speedup, 4.1× is the F1/hour ratio, 3.8× is a conservative version. This is adequately addressed.
5. *"Comparison against Bracken suggested"* — A nice-to-have, not a weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Resolve the numerical inconsistency in sparsification preservation claims (94% in abstract/Section 1.3 should be corrected to match the actual data in Table 1).
2. Report results on the other three claimed benchmarks (CAMI II Strain, HMP Mock, Zymo). The strain-level benchmark is the most informative for the paper's core thesis — if token matching works when genomes differ by only 5%, the claim that positional information is unnecessary is strongly supported; if it fails, the scope claim must be restricted.
3. Define and cite "Metalign" in Table 4, or replace it with the same baselines used in the main results.
4. Clarify the relationship between Table 1's "Full Index" and Table 3's "QA-Token + no sparsification" configurations.
5. Provide supporting evidence (e.g., interaction-term analysis) for the claimed additivity of component contributions.

## Score and Decision

The paper presents a well-motivated core idea with a transparent ablation study and rigorous statistical reporting. However, the evaluation is incomplete (results on only 1 of 4 claimed benchmarks), a numerical inconsistency in the headline sparsification claim (94% vs 99.5% vs 99.18%) undermines trust, and an undefined baseline appears in a key table. These issues prevent acceptance in the current form.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>