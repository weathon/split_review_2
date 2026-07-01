## Summary

HighClass presents a metagenomic classification framework that replaces the alignment step (seed-and-extend) with hash-based token mapping using pre-trained QA-Token vocabularies and gradient-based sparsification, achieving a 4.2× speedup and 68% memory reduction over MetaTrinity at the cost of ~1.5 pp F1 (85.1% vs 86.6% on CAMI II). The core engineering insight — that taxonomic classification does not require precise alignment positions and can be reframed as a position-invariant token matching problem — is legitimate and well-illustrated through a clean ablation study.

## Strengths

- **Well-structured ablation study (Table 3).** The paper cleanly decomposes the contribution of each component: QA-Token vocabulary (+6.8 pp F1 over fixed k-mers), quality weighting (+1.9 pp), and sparsification. The inclusion of the "QA-Token + MetaTrinity alignment" row (86.2% F1) honestly shows that the QA-Token benefit is partly contingent on the downstream hash-based pipeline, not a universal improvement.

- **Clear computational cost breakdown (Table 5).** Per-operation timing (containment search, seeding, chaining in MetaTrinity vs. token extraction, lookup, scoring in HighClass) makes the 4.2× speedup concrete and verifiable. This level of detail is valuable for reproducibility and for understanding where the gains come from.

- **Legitimate conceptual insight (Section 5.5).** The framing that "alignment-based methods ask *where* and *how well* a read matches a reference, whereas token-based classification asks *which taxa contain the discriminative subsequences*" articulates the accuracy–runtime trade-off in principled terms. This insight is the paper's most distinctive intellectual contribution.

## Weaknesses

### Fatal
None.

### Major

- **Theoretical contributions are substantially oversold relative to what is actually provided.** The paper claims "the first comprehensive theory of token-based genomic classification" (abstract, Sections 1.3, 6.1, 7) with "rigorous theoretical foundations," but the results presented in the main text are standard off-the-shelf bounds from statistical learning theory applied without method-specific analysis. The Rademacher complexity bound $O(\sqrt{V|\mathcal{Y}|/n})$ is the generic rate for any multiclass hypothesis class with $V|\mathcal{Y}|$ parameters — there is nothing in the bound that reflects the token-based architecture, hash-based mapping, quality weighting, or sparsification. The α-mixing concentration analysis is a standard application lacking justification for how parameters $\gamma\approx0.15$ and $C\approx2.3$ are derived or validated from genomic data. The consistency result (Theorem 8) restates standard maximum-likelihood consistency. The theory is not wrong, but it is not meaningfully *about* HighClass; it does not analyze why hash-based token mapping preserves accuracy, how sparsification affects the hypothesis class, or how quality weighting alters the risk. A reader familiar with learning theory will recognize these as textbook bounds relabeled as novel foundations. This gap between the strength of the claim ("first comprehensive theory") and the content of the theory would mislead readers.

- **Internal numerical inconsistency in reported accuracy preservation.** The abstract and Section 1.3 state that gradient-based sparsification "preserves 94% accuracy." Section 5.4.3 states it "preserves 99.5% relative accuracy." Table 1 shows the sparsified index achieves 85.1% F1 vs. the full index's 85.8% F1 — a ratio of 85.1/85.8 ≈ 99.2%. These three figures (94%, 99.5%, 99.2%) are mutually inconsistent and the paper provides no explanation for the 94% figure. This is particularly concerning because the 94% claim appears in the abstract and contributions — the parts readers see first — and does not match the data in the paper's own tables.

- **Limited and non-contemporary baseline set.** The primary comparator is MetaTrinity (Gollwitzer et al., 2023), from the same group, and the other two baselines — Kraken2 (2019) and Centrifuge (2016) — are several years old. The paper's claims of "state-of-the-art" performance would be substantially strengthened by comparison against more recent and widely used methods. Additionally, Metalign appears in the scalability table (Table 4) with no introduction, no description in the experimental setup or related work, and no citation or configuration details — this makes the scalability comparison unverifiable and is a significant methodological gap.

### Minor

- **The F1/hour metric conflates accuracy and efficiency in a way that systematically favors high-speed methods.** HighClass's F1/hour of 170.2 vs. MetaTrinity's 41.2 is driven primarily by the 4.2× speedup, not by accuracy. The paper already reports F1 and runtime separately (Table 2); the composite metric should be presented alongside a clear discussion of the trade-off rather than as a primary result.

- **Related work section is dominated by the authors' own prior work.** Sections 2.1 devotes ~60% of the related work to describing QA-Token and MetaTrinity, both from the same group. External methods receive only a brief paragraph (Section 2.2). This imbalance underrepresents the broader landscape of metagenomic classification tools.

- **Training cost of pre-trained components is not reported.** HighClass adopts pre-trained QA-Token vocabularies and gradient-based sparsification masks, but their one-time training cost is never mentioned. A reader evaluating the overall efficiency of the approach needs this context to understand the total resource investment.

- **Positioning as a "third paradigm" (neither alignment-based nor alignment-free) is overstated.** Token-based classification with inverted indices is a specific form of alignment-free method by standard definitions. The paper would be better served by positioning itself within the alignment-free family while emphasizing its distinctive design choices, rather than claiming a separate paradigm.

### Trivial

None beyond those absorbed into minor weaknesses above.

## Nice-to-Haves

- Provide a confidence interval or bootstrap estimate for the speedup ratio (not just for F1 and runtime separately).
- Discuss index maintenance cost when the reference database is updated (the current evaluation assumes a static database).
- The ablation observation that QA-Token within MetaTrinity's native alignment pipeline achieves 86.2% vs. MetaTrinity's 86.6% (essentially a tie) is worth explicit discussion: the benefit of QA-Token tokenization appears to depend on the downstream aggregation method.
- Report pairwise significance tests between ablation configurations (Table 3) to clarify which differences are statistically meaningful.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **"Kraken2 at 70% F1 on CAMI II is suspiciously low; typical CAMI II evaluations show Kraken2 achieving substantially higher species-level F1."** — This speculation about what Kraken2's performance "should" be cannot be verified from the paper alone; removed as unsupported.

2. **"The paper should compare against KrakenUniq, Bracken, Path-aware, SHOGUN, Ganon."** — Per policy, specific un-cited tools are not included as explicit demands; the general criticism about limited/outdated baselines is retained above.

## Novel Insights

None beyond the paper's own contributions. The reviewer's observation about the QA-Token × downstream method confound is a useful analytical point but is directly derivable from the data the paper already presents (Table 3).

## Suggestions

1. **Resolve the 94% vs 99.2% vs 99.5% inconsistency.** Ensure all numeric claims in the abstract and contributions are consistent with the data in the tables. If "94%" refers to a different accuracy metric than F1, define it explicitly.

2. **Tone down the theoretical claims.** Frame the Rademacher complexity, α-mixing, and consistency results as standard applications of known tools that justify the approach, not as "the first comprehensive theory." Replace the abstract's claim of a "comprehensive theory" with a more measured description of what the bounds actually contribute.

3. **Expand the baseline set** to include at least one or two widely used contemporary metagenomic classifiers beyond the authors' own prior work. Provide a proper introduction for Metalign if it appears in the evaluation.

4. **Separate F1 and runtime reporting from the composite F1/hour metric**, and discuss the accuracy–speed trade-off explicitly rather than collapsing it.

## Score and Decision

<score>4</score>
<decision>Reject</decision>