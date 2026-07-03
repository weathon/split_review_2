Since the calibration search tool is unavailable due to an infrastructure issue, I'll proceed with my expert judgment calibrated against the ICLR scale. Let me compile the final review.

Now let me write the final consolidated review.

## Summary
HighClass proposes a metagenomic classification framework that replaces alignment operations with hash-based token mapping using variable-length learned tokens (from QA-Token), quality-aware scoring, and gradient-based sparsification. On CAMI II, it achieves 85.1% species F1 (within 1.5 pp of MetaTrinity's 86.6%) with 4.2× speedup and 68% memory reduction. The paper also presents theoretical analysis using Rademacher complexity and α-mixing.

## Strengths
1. **Clean ablation study isolating each component's contribution (Table 3).** Variable-length tokens contribute +6.8 pp over fixed k-mers, quality weighting adds +1.9 pp, and sparsification preserves 99.5% relative accuracy. The paper verifies that interaction effects between components are less than 0.5 pp, a valuable empirical finding. The ablation row "QA-Token + MetaTrinity alignment" (86.2% F1) cleanly isolates the cost of replacing alignment with hash lookups (~1.1 pp).

2. **Detailed computational cost breakdown with standard errors (Table 5).** MetaTrinity's three-step pipeline (containment search: 3.2±0.2 ms, seeding: 2.8±0.1 ms, chaining: 1.9±0.1 ms) is contrasted with HighClass's two-step pipeline (token extraction: 0.8±0.05 ms, token lookup: 0.7±0.03 ms). The 8.8±0.3 ms/read vs 1.9±0.1 ms/read directly substantiates the speedup with quantified uncertainty.

3. **Clear contrast with deep-learning tokenization paradigms (Section 2.4, final paragraph).** The paper explicitly distinguishes using tokens as *mapping primitives* (matched against compressed inverted indices at inference) from the prevalent use of tokens as *features* for neural encoders. This correctly situates the contribution within taxonomic classification, not representation learning.

4. **Statistical rigor.** Experiments use 10 independent runs, 95% bootstrap confidence intervals, Wilcoxon signed-rank tests with Holm-Bonferroni correction, and Cohen's d effect sizes — above the standard for computational biology papers.

## Weaknesses

### Major
1. **Overstated novelty framing obscures genuine contribution.** The paper claims to "fundamentally transform the computational paradigm" (Abstract) by "replacing alignment with hash-based token mapping" (Section 1.3), but Kraken2 (Wood et al., 2019), which the paper itself cites, already performs alignment-free classification via hash-based k-mer lookups with O(m) query time. The paper's real contribution is more specific and valuable: using *variable-length learned tokens* (from QA-Token) rather than fixed k-mers within a hash-based index, combined with quality-aware scoring and sparsification. The current framing invites unnecessary skepticism about a contribution that stands well enough on its own terms.

2. **Narrow baseline comparison cannot support the Pareto-optimality claim.** The paper compares against only three methods: Kraken2 (2019), Centrifuge (2016), and MetaTrinity (2023, same research group). Several widely used modern alignment-free classifiers — Bracken, CLARK, Kaiju — are absent. The claim of "establishing a new operational point on the Pareto frontier" (Section 7) cannot be properly evaluated without broader comparison. With two of three baselines being at least 6 years old, the trade-off space is undersampled.

3. **Unsupported numerical claims in the theoretical analysis.** The generalization bound claims an excess risk of ~0.021 for V=32,000, |Y|=100, n=10^6 (Section 4.3). But √(V|Y|/n) = √(32,000 × 100 / 10^6) = √3.2 ≈ 1.79, and the paper does not derive how the implicit constant yields 0.021. Standard Rademacher bounds for multiclass settings typically involve constants that would render this bound far larger, potentially vacuous. The mixing parameters C≈2.3 and γ≈0.15 are described as "empirically validated" (Section 4.1) but the estimation procedure is entirely in the appendix, with no evidence in the main text that the exponential-mixing assumption holds for genomic token sequences. The theory does not guide any design choice or yield a non-trivial prediction verified in the experiments; it reads as standard tools applied generically.

4. **Unexplained QA-Token F1 discrepancy.** The paper states QA-Token "achieves 0.917 taxonomic F1 on CAMI II" (Section 2.1). HighClass, using QA-Token's pre-trained vocabulary, achieves 85.1% species F1. If both are at the same taxonomic level, this ~6.6 pp gap is large and unexplained. If the QA-Token figure is at a different level (e.g., genus-level F1 is typically higher), the paper must clarify. The ablation row "QA-Token + MetaTrinity alignment" reaches only 86.2% — still far below 91.7% — suggesting the gap is not primarily due to the alignment-to-hash replacement. This discrepancy undermines the claim that HighClass optimally leverages QA-Token's representations.

### Minor
5. **"Within 1.5% of state-of-the-art" is ambiguous** — the numbers show a 1.5 *percentage point* difference (86.6% vs 85.1%), not a 1.5% relative difference. This should be clarified.

6. **Metalign in Table 4 is not introduced.** The reader is given no context about what Metalign is, how it relates to other baselines, or why it is included only in the scalability table.

7. **Choice of k=31 for the fixed k-mer baseline (Table 3) is not justified.** Kraken2's default is k=31 (not 35 as the reviewer claimed — Kraken2 default is actually k=31), so the choice is reasonable, but the paper does not explain this or show sensitivity to k.

8. **Scoring function notation ψ(a,b) (line 142) is not defined in the main text** — it is referenced to Appendix D, which is standard for detailed derivations but leaves the main text incomplete on a key formula.

9. **Minor index size discrepancy:** Table 1 reports the sparsified index as 6.8 GB, while Table 2 shows HighClass's index column as 6.2 GB (total memory 6.8 GB). The difference is small but unexplained.

### Trivial
None beyond what is listed as Minor.

## Nice-to-Haves
- Discussion of failure modes and sensitivity to quality score calibration would strengthen the paper.
- The theoretical section would benefit from at least one non-trivial prediction that is verified experimentally (e.g., how the bound changes with vocabulary size or mixing parameters).
- A sensitivity analysis over k for the fixed k-mer baseline would strengthen the claim that variable-length tokens are inherently superior (as opposed to better-tuned for a specific k).

## Removed Points
These points were raised by the reviewers but are excluded from the main weaknesses for the reasons stated:

1. **"The theoretical analysis is generic textbook material" (Harsh Critic)** → Kept in weakened form (Major #3) focusing on the unsupported numerical claims rather than the generic nature of the tools. The criticism that the theory is "decorative" is partly valid but overstates — many ML papers apply standard frameworks to their setting.

2. **"Related works dominated by own prior work" (Harsh Critic)** → Removed. The paper does cite Kraken2, Centrifuge, and general methods. Citing one's own prior work that directly builds on is standard practice. The call for missing related works (Bracken, CLARK, Kaiju) is reframed as a baseline comparison issue (Major #2) rather than a related-work deficiency.

3. **"Missing discussion of limitations" (Harsh Critic)** → Moved to Nice-to-Haves. A genuine gap but not central to evaluating the paper's contributions.

4. **"O(√(V|Y|/n)) bound is vacuous with mixing inflation" (Harsh Critic)** → Merged into Major #3. The specific concern about mixing inflating the bound is valid but the critic's precise numerical counter-claim (constant at least 2 → bound near 3.6) depends on assumptions about the implicit constant that could vary based on the specific normalization in the full proof (in the inaccessible appendix). The core issue (unsupported numbers) is retained.

5. **Strength Finder Point 3 ("Explicit numeric constants in theoretical guarantees")** → Downgraded. The presence of explicit constants is noted as methodologically positive, but the validity of those constants is contested in Major #3, so this strength cannot stand without caveat.

6. **"No discussion of scenarios where alignment might still be necessary" (Harsh Critic)** → Moved to Nice-to-Haves. This is scope-adjacent — the paper explicitly scopes to taxonomic classification, not variant detection.

## Novel Insights
The reviews surface a useful observation that none of the individual reviewers fully articulated: the near-additive decomposition of accuracy gains (vocabulary → +6.8 pp, quality → +1.9 pp, sparsification → ~0 pp loss) is an unusually clean result for a multi-component ML system. This suggests the design decisions operate on relatively independent signal dimensions and merits more explicit discussion. Additionally, the ablation column "QA-Token + MetaTrinity alignment" (86.2%) cleanly quantifies the specific accuracy cost of replacing alignment with hash lookups (~1.1 pp) — this is arguably the paper's most informative single data point and could be front-loaded.

## Suggestions
1. **Reframe the contribution.** Remove "paradigm transformation" and "fundamentally transforms" language. The paper's actual contribution — variable-length learned token indexing with quality-aware scoring for metagenomic classification — is strong enough to stand without inflated framing.

2. **Broaden the baseline set.** Add Bracken, CLARK, and Kaiju to substantiate the Pareto-optimality claim. With three baselines (two old, one from the same group), the current empirical evaluation is not commensurate with the strength of the claims.

3. **Clarify the QA-Token discrepancy.** State explicitly at what taxonomic level QA-Token's 0.917 F1 is reported, and explain the gap between that figure and HighClass's 85.1% (and even the 86.2% with alignment).

4. **Either derive method-specific bounds or scale back the theoretical claims.** The theory section would be stronger if it either (a) produced a non-trivial prediction verified in the experiments, or (b) was honestly presented as standard tools applied to this setting, with the numerical 0.021 claim either properly derived or removed.

5. **Introduce Metalign in the text** and explain the 6.2 GB vs 6.8 GB index size discrepancy.

## Score and Decision

Given the constraints, I am unable to use the calibration_search tool for anchoring. I proceed with my expert assessment.

The paper has a genuine empirical contribution: combining variable-length learned tokens (from QA-Token) with hash-based indexing, quality-aware scoring, and sparsification yields a practical classifier with a favorable accuracy-efficiency profile. The ablation study is clean and informative. The computational cost breakdown is precise.

However, the paper has four significant issues that prevent acceptance in its current form: (1) overclaimed novelty that misrepresents the contribution relative to prior alignment-free methods; (2) a baseline set too narrow to support the Pareto-optimality claim; (3) unsupported numerical claims in the theoretical analysis that the main text does not properly derive; and (4) an unexplained discrepancy between QA-Token's reported F1 and HighClass's.

These are all fixable with revision (reframing, broader baselines, clarifying the theory and the QA-Token numbers). The core methodology is not flawed. On the ICLR scale, a score of **5.0** (borderline reject) reflects a paper with genuine contributions that has significant gaps between its claims and the evidence presented as currently written. A revised version that addresses the four major issues could be acceptable.

**Score: 5.0 — Borderline Reject**
**Decision: Reject** (with clear path to acceptance after major revision)