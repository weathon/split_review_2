Based on my direct analysis of the paper and the filtered reviewer inputs, I'll now produce the final review.

Here is my reasoning for the score:

**Positive aspects:** The paper introduces a novel conceptual framework (subgrammar structure for CFGs) and has one genuinely well-designed experiment (depth vs. length generalization in Section 6). The CKA analysis is a reasonable attempt at mechanistic evidence.

**Critical issues:** (1) The main-text derivation of the central theoretical claim (Eq. 1–5) is mathematically unsound — Equation (4) contains terms like log P / log Q that do not correspond to any valid KL-divergence manipulation. For a paper that bills this as its "most important contribution," this is a major flaw. (2) The context-insensitivity assumption (Corollary 4.5) on which the simplified decomposition depends is acknowledged as strong but only supported by visual inspection, not quantitative testing. (3) No variance reporting despite 30 seeds in Table 1. (4) The paper overclaims ("prove a suite of fundamental results," "show definitively") relative to what is actually established.

The paper's core contribution — the theoretical decomposition — is not convincingly established in the main text, and the empirical support is less rigorous than the claims require. At ICLR, this level of execution is insufficient for acceptance.

Score 4, decision Reject.

---

## Summary
This paper studies how transformer language models learn context-free grammars (CFGs) through the lens of "subgrammar" structure. It defines inner and outer subgrammars, attempts to prove that the KL-divergence decomposes recursively over subgrammars, and provides empirical results on small transformers including observations about parallel learning, subgrammar pretraining with CKA analysis, and a depth-vs-length generalization experiment.

## Strengths
- **Clean depth-vs-length experiment (Section 6, Figure 3):** The paper compares two test conditions on a nested-parentheses PCFG — contexts of the form $(a)^i$ (same depth, growing length) where error stays at 0.017, versus contexts of the form $(^i$ (growing depth) where error rises to 0.173. Since the ground-truth next-token distribution is identical in both cases, this cleanly isolates recursive depth as the limiting factor, a distinction many prior studies conflate.
- **CKA-based mechanistic evidence (Section 5.2, Table 1):** The paper goes beyond loss curves by using Centered Kernel Alignment to examine internal representations, showing that models pretrained on a subgrammar exhibit higher attention-layer alignment (+8.9% to +21.7%) than scratch-trained models, across 30 random seeds.
- **Novel conceptual framing:** Introducing subgrammar structure as a lens for studying language model learning dynamics is a worthwhile research direction that opens new questions about how neural networks interact with compositional grammar structure.

## Weaknesses

### Major
1. **Main-text derivation of the core theoretical result is mathematically unsound as presented (Equations 1–5).** The paper's "most important contribution" (Section 4.2) is a claimed decomposition of KL-divergence over subgrammar structure. However, the derivation from Equation (1) to Equation (4) contains algebraic errors: Equation (4) presents terms of the form log P / log Q (fractions of log-probabilities), which do not correspond to any valid manipulation of KL-divergence (Σ P log(P/Q)). The notation is ambiguous throughout — `P_G(a)` appears without clear definition, sums are not properly scoped, and the "abuse of notation" disclaimer does not resolve the errors. Since the full proof is deferred to the appendix (not available for verification), a reader cannot assess whether the central theoretical claim is actually correct.

2. **Context-insensitivity assumption is acknowledged as strong but only supported by visual, not quantitative, evidence (Corollary 4.5).** The corollary simplifies the KL decomposition based on the assumption that the model's conditional distribution over a subgrammar is identical across all contexts. The paper calls this "a strong assumption" but provides only informal visual evidence ("varying prefixes did not result in qualitatively different results"). No quantitative measure of variation across contexts, no bound on approximation error, and no comparison of the simplified formula vs. actual KL are provided. This weakens confidence in the practical applicability of Theorems 4.3 and 4.6.

3. **No variance reporting despite using 30 random seeds (Table 1).** The CKA analysis reports average similarity values across 30 seeds but provides no standard deviations, confidence intervals, or any measure of variance. The reported differences are small in absolute terms (e.g., 0.258 vs. 0.281 on a 0–1 scale), and without variance estimates it is impossible to assess whether these differences are meaningful or within noise. The percentage changes (+8.9%, +21.7%) amplify small absolute differences without indicating reliability.

### Minor
4. **Corollary 4.7 is close to definitional and contributes little insight.** It states: if gradient updates on one subgrammar do not hurt performance on other subgrammars, then the model learns all subgrammars in parallel. This is essentially the condition restated as a conclusion. The paper acknowledges the condition may not hold and calls testing it future work. Including this as a formal contribution inflates the paper's apparent theoretical depth.

5. **"Parallel learning" claim is supported only by visual inspection with no quantitative metric.** The paper states models "learn all subgrammars in parallel" based on visual inspection of Figures 1–2. No quantitative metric (e.g., correlation of loss reductions, comparison to a sequential baseline, statistical test) is provided. The observation may be correct, but the evidence does not constitute a demonstrated finding.

6. **Abstract overclaims relative to what is established.** Phrases like "prove a suite of fundamental results" and "show definitively" are not supported given the derivation issues (weakness 1) and missing variance estimates (weakness 3). The comparison to child language acquisition ("unlike children") is a framing device the paper does not substantively engage with.

### Trivial
7. The GPT-5.1 anecdote (Section 6) is explicitly called "purely anecdotal" by the paper itself and adds no evidential weight. It can be removed without loss.

## Nice-to-Haves
- Reporting standard deviations or confidence intervals for Table 1 and other quantitative comparisons.
- Testing the context-insensitivity assumption quantitatively: measuring how much conditional distributions vary across contexts, with a bound on the resulting error.
- Defining the specific CFGs used in experiments in at least sketch form in the main text.

## Removed Points
*These points were flagged for removal; treat them with caution.*

- *Criticism that the paper doesn't clearly differentiate from Cagnetta & Wyart (2024):* The paper explicitly frames its contribution as being about learning *dynamics* and subgrammar structure, while prior work studied static representations or converged models. This differentiation is stated.
- *Criticism about architectural details being absent from the main text:* Many papers in this community defer implementation details to the appendix. This is standard practice.
- *Criticism that Equation (4) might be a pure rendering artifact:* Even allowing for extraction artifacts, the text describes the result as a sum over "conditioned KL-divergences" but the mathematical expression given does not produce a valid KL decomposition. This is a substantive issue, not a formatting nitpick.
- *Strength Finder's claim about Theorem 4.3 being "genuinely novel":* While the paper claims this, the novelty cannot be assessed independently of whether the derivation is correct. Given the mathematical issues, this strength is conditional at best.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Fix the main-text derivation.** Rewrite Equations (1)–(5) with correct algebra, showing how the autoregressive decomposition of log-probabilities properly separates into subgrammar contributions. The current Equation (4) is not mathematically valid and must be corrected for the theoretical contribution to be assessable.
2. **Test the context-insensitivity assumption quantitatively.** Provide a measure of how much the model's conditional distribution over a subgrammar varies across contexts, with a bound or error analysis on the simplified formula.
3. **Report variance for all quantitative claims** — standard deviations or confidence intervals for the CKA values (Table 1) and for loss/KL values across seeds.
4. **Remove or substantially revise Corollary 4.7** unless a non-trivial sufficient condition for parallel learning can be identified.
5. **Tone down overclaims.** Replace "definitively" and "fundamental" with language commensurate with the evidence, or strengthen the evidence to support these terms.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>