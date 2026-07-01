Now let me write the final review.

**Round 1 Bracket:** After comparing against calibration anchors, the initial plausible range is 4.5–5.5. This paper has a stronger empirical contribution than the 4.33-scored metagenomic binning paper (accepted) but weaker theory than typical 6+ papers. The DNABERT-S paper (5.67, rejected) had similar evaluation depth but different issues (limited novelty vs. theory problems here). The MeToken paper (5.80, accepted) is a stronger point of comparison for a systems paper with solid evaluation.

**Narrowing to final score:** The theory problems are significant enough to prevent a score above 6, but the empirical results (clean ablation, 15% relative F1 improvement over Kraken2 at same speed, thorough statistical validation) are real and distinguish this from 3–4 range papers. Within 4.5–5.5, the paper sits at the upper end because the core empirical contribution is well-supported. Final score: **5.0**.

## Summary

HighClass proposes a metagenomic classification framework combining variable-length tokens (from QA-Token) with hash-based inverted-index lookup, quality-aware scoring, and gradient-based sparsification. On CAMI II it achieves 85.1% F1 with 4.2× speedup over MetaTrinity and 68% memory reduction. The paper also presents theoretical results (generalization bounds, α-mixing concentration inequalities, consistency).

## Strengths

1. **Variable-length tokens + hash-based lookup is a sensible and well-evaluated combination.** The ablation study (Table 3) cleanly isolates contributions: variable-length tokens provide 6.8 pp over fixed 31-mers (78.3% → 85.1%), quality weighting adds 1.9 pp, and sparsification trades 0.7 pp for 68% memory reduction. This is the paper's core empirical contribution and is well supported by the data.

2. **The computational cost breakdown (Table 5) is detailed and informative.** It shows exactly which MetaTrinity operations are eliminated (containment search, seeding, chaining) and which replace them (token extraction, token lookup), with per-operation timing in ms/read. This gives readers a clear picture of where the speedup comes from.

3. **The sparsification analysis (Table 1) provides practical deployment guidance.** The 68% memory reduction to 6.8 GB with only 0.7 pp accuracy loss and a 78% reduction in cache misses is a concrete engineering contribution that enhances practical utility.

## Weaknesses

### Major

- **The theoretical framework is disconnected from the method, and its components lack a coherent relationship.** The paper presents three results (generalization bound reported as ~0.021 for n=10⁶, V=32,000, |Y|=100; α-mixing concentration with variance inflation factor 31.7; consistency) as a unified "first comprehensive theory of token-based genomic classification," but the main text never defines what the learning problem is, what constitutes a "training sample" (reads? tokens?), or how the three results interact. The rate O(√(V|Y|/n)) with the stated numbers (V=32,000, |Y|=100, n=10⁶) gives √3.2 ≈ 1.79, yet the paper reports 0.021 — a discrepancy that is not explained by any constant discussed in the main text. The α-mixing analysis reports a variance inflation factor of 31.7 for token dependencies, but the paper does not clarify whether this factor affects the generalization bound (dependencies within a read vs. across independent reads). The consistency result is a standard MLE property not specific to the method. Because the theory is foregrounded as the paper's first-listed contribution, this lack of clarity and internal coherence is a significant weakness.

### Minor

- **The framing overstates the algorithmic novelty.** The paper repeatedly characterizes its "key innovation" as replacing alignment operations with hash-based mapping (abstract, Sections 1.3, 3.5). However, Kraken2 (Wood et al., 2019), which the paper itself cites, already uses hash-based k-mer-to-taxon mapping with O(m) query time. The real novelty is the use of learned *variable-length tokens* (from QA-Token) within this hash-based paradigm, not the hash-based lookup structure itself. The reported results are meaningful, but the framing should reflect what is actually new.

- **An unexplained 5.5 pp gap between the reported QA-Token accuracy and the closest HighClass configuration using QA-Token tokens.** The paper states that QA-Token "achieves 0.917 taxonomic F1 on CAMI II" (line 100, citing Gollwitzer et al., 2025), but Table 3 shows "QA-Token + MetaTrinity alignment" achieving only 86.2% F1. If these numbers reflect different metrics, taxonomic levels, or benchmark subsets, the paper should state this explicitly.

- **Metalign appears as a comparator in Table 4 (scalability) but is never defined, cited, or introduced in the main text.** Section 5.3 lists only MetaTrinity, Kraken2, and Centrifuge as baselines. The scalability comparison against Metalign is therefore uninterpretable.

- **The conclusion claims the theory "transforms sequence classification from heuristic methods to principled approaches with provable guarantees."** This overstates what has been demonstrated. The method remains substantially heuristic (vocabulary learned via PPO/Gumbel-Softmax on another task, sparsification gradient-based, η learned from data), and the theoretical guarantees are not shown to cover the full system in a unified way.

### Trivial

None.

## Nice-to-Haves

- A sensitivity analysis of the quality-weighting parameter η (e.g., F1 vs η from 0.5 to 3.0) would strengthen confidence that η=1.8 is near-optimal.
- Per-read latency (rather than only total runtime) would aid cross-dataset comparison.
- Comparison against Kraken2 with a tuned k-mer size or confidence threshold would strengthen the claim that variable-length tokens are inherently superior to fixed k-mers.

## Removed Points

These points from the input review were removed with justification:

- **"The bound becomes 10.1 when combining generalization bound with α-mixing factor."** The calculation assumes the mixing factor applies to the generalization bound's effective sample size, but the α-mixing analysis addresses token dependencies (within reads) while the generalization bound likely assumes independent reads. The real weakness is unclear presentation, not a proven numerical contradiction. Removed to avoid propagating a potentially incorrect interpretation.
- **"Missing baselines (Bracken, CLARK, Kallisto)."** Removed per policy: do not raise missing related works/references.
- **"F1/hour metric conflates accuracy and speed."** This is a standard efficiency metric widely used in systems evaluation; not a flaw specific to this paper.
- **"Table 1 caption unclear about Full Index."** The caption ("Impact of genome sparsification. ... Full Index") is sufficiently clear from context.
- Section-by-section notes that were generic or not anchored to specific content in the paper.

## Novel Insights

The review process surfaces a structural observation not fully articulated in the paper: HighClass has two separable contributions — (a) an empirical demonstration that variable-length tokenization + hash-based lookup outperforms fixed k-mer + hash-based lookup (Kraken2), and (b) a theoretical framework for token-based classification. These are presented as a unified whole, but the theory does not demonstrably underwrite the empirical system. The paper would be stronger if it either (i) made the theory self-contained and clearly connected to the method, or (ii) presented the empirical result on its own terms and offered the theory as a separate, exploratory contribution.

## Suggestions

1. **Clarify or restructure the theoretical contribution.** Either explain precisely what learning problem is being solved, how the three theoretical results relate to each other and to the classification pipeline, and what n refers to; or present the theory as a separate exploratory contribution rather than a claimed guarantee for the full system.

2. **Reframe the novelty.** State the contribution as "variable-length token-based classification within a hash-based lookup paradigm" rather than "replacing alignment with hashing," which Kraken2 already accomplished in 2019.

3. **Explain the 0.917 vs 86.2% QA-Token discrepancy.** This is a simple fix that would remove a credibility concern.

4. **Introduce or remove Metalign from Table 4.**

## Score and Decision

**Calibration anchors consulted:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| vBw8JGBJWj.md (UnitigBin) | 4.33 | R1 | Weaker empirical setup, accepted. Our paper has stronger validation. |
| 9klRFLY2TT.md (DNABERT-S) | 5.67 | R1 | Similar domain, rejected for limited novelty. Our paper has similar evaluation depth but different weakness profile (theory problems vs. novelty concerns). |
| noUF58SMra.md (MeToken) | 5.80 | R1 | Strong systems paper with solid evaluation, accepted. Our paper has comparable empirical rigor but weaker theory. |
| IEZjjDX0iC.md (pLM comparison) | 3.00 | R1 | Largely comparative without new method. Our paper is much stronger. |

**Round 1 bracket:** 4.5–5.5. The empirical contribution (clean ablation, 15% relative F1 improvement over Kraken2 at same speed, thorough statistical validation) distinguishes this from score-3 papers. The theory problems prevent scores above 6. Within the bracket, the paper sits at the upper end because the core empirical claim is well-supported and practically valuable.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Accept</decision>