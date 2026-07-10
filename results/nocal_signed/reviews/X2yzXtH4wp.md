Now let me produce the final consolidated review.

## Summary

This paper introduces Ambig-SWE, an underspecified variant of SWE-Bench Verified, and evaluates how six LLM-based agents handle underspecified instructions in software engineering tasks. The paper's core contribution is an analytical decomposition of the problem into three capacities — detecting underspecificity, asking targeted clarification questions, and leveraging interaction to improve outcomes — with distinct experiments for each. The empirical findings include several striking results: Qwen 3 Coder's complete refusal to interact despite strong SWE-Bench performance, Claude models' efficient exploration-first questioning strategy, and quantitative evidence that interaction meaningfully recovers performance lost to underspecification.

## Strengths

- **Well-motivated problem and clean analytical decomposition.** The paper separates handling underspecified instructions into three testable capacities (detection, questioning, integration) and designs distinct experiments for each (§4, §5, §3). This enables diagnostic evaluation rather than opaque aggregate comparisons.
- **Several genuinely interesting and non-obvious findings.** (a) Qwen 3 Coder's 100% FNR across all prompt conditions (Table 2) despite being among the strongest models on standard SWE-Bench is a striking result. (b) Claude Sonnet models achieve comparable information gain to Qwen with ~50% fewer questions by exploring the codebase first (§5.3). (c) Qwen's resolve rate *worsens* when navigational information is provided (Table 1), suggesting rigid protocol-following that cannot adaptively incorporate user input.
- **Clean three-setting experimental design.** The Full / Hidden / Interaction comparison (Figure 3) cleanly isolates the effect of interaction on resolve rates, using the human-validated SWE-Bench Verified as a foundation.
- **Methodological awareness in dataset construction.** The distributional analysis comparing GPT-4o-generated underspecified variants to naturally occurring underspecified issues (§2.1), and the explicit rationale for not using naturally underspecified examples (lack of paired ground truth), show thoughtful design.

## Weaknesses

### Fatal
None.

### Major

- **Claude Sonnet 4's Hidden baseline evaluated on only 100/500 instances, making the key comparison non-comparable.** Footnote 4 states Claude Sonnet 4 is evaluated on a subset of 100/500 instances in the Hidden setting, while Interaction and Full settings use all 500. The headline comparison for the paper's best-performing model — Hidden 40% → Interaction 61.4% (53.5% relative improvement) — is not apples-to-apples. If the 100-instance subset differs systematically from the full set (cost-driven selection could correlate with instance difficulty), the comparison is invalid. The paper asserts findings remain "statistically significant (Table 4)," but even a significant difference on a biased sample can misrepresent the *magnitude* of the effect. This is the most significant evidential gap in the paper.

### Minor

- **No confidence intervals or variance measures for any resolve rate** (Figure 3, Table 1). All values are point estimates. With 500 instances per condition (only 100 for Sonnet 4 Hidden), binomial confidence intervals are straightforward. For example, Llama 3.1's Hidden rate of 3.2% (16/500) and Interaction rate of 4.8% (24/500) produce substantially overlapping intervals, yet the paper makes strong comparative claims. The paper reports Wilcoxon tests (appendix), but the reader cannot assess the reliability of individual differences without variance information.

- **Numerical imprecision in the headline "74%" claim.** The abstract and introduction (§1) state interaction yields improvements "up to 74% over the non-interactive settings." The maximum relative improvement (Interaction−Hidden)/Hidden in the reported data is 100% (Claude Haiku 3.5). The closest plausible computation is Claude Sonnet 4's gap recovery of 76.4%, which is close but not 74%. The specific number does not match any straightforward computation from Figure 3. This should be corrected or clarified.

- **GPT-4o serves triple duty as dataset generator, user proxy, and LLM-as-judge,** introducing circularity for the question quality metric (§5.1). Specifically: GPT-4o generates the user proxy's answers and then GPT-4o scores those same answers on "specificity and novelty of information" (Figure 6). The question quality scores therefore partly reflect how well GPT-4o's self-generated answers match its own criteria, not necessarily how useful those answers are to the agent. The cosine distance metric (text-embedding-3-small) is independent and mitigates concern for that sub-result, but the LLM-as-judge scores should be interpreted with caution.

- **RQ2 detection experiment conflates detection ability with the decision to interact** (§4). The experiment measures underspecificity detection by whether the model *chooses to interact*. This conflates two distinct capacities: detecting missing information and deciding to ask about it. A model might detect underspecificity correctly but not ask (e.g., using exploration-first strategies like Claude Sonnet 4), or ask without genuine detection (e.g., following a template). The paper does not discuss this conflation as a limitation in §7.

- **The cosine distance metric for information gain** (§5.1–5.2) operationalizes "information gain" as embedding change before vs. after interaction using text-embedding-3-small. This could reflect topic drift, confusion, or irrelevant elaboration rather than genuine task-relevant information acquisition. The LLM-as-judge metric partially addresses this, but both share this limitation.

### Trivial
None.

## Nice-to-Haves

- Provide a quantitative analysis connecting the three sub-capacities (e.g., does detection accuracy predict the interaction benefit? does question quality correlate with resolve rate after controlling for base coding ability?) to substantiate the claim that these are the "right" three capacities to study.
- Re-evaluate Claude Sonnet 4's Hidden condition on the full 500-instance set, or provide a sensitivity analysis demonstrating representativeness.
- Use a different model (e.g., Claude or Llama) as the LLM-as-judge to break the GPT-4o circularity for question quality scoring.
- Add a post-hoc analysis for RQ2 distinguishing detection failures from strategic non-interaction.

## Removed Points

These points were flagged for removal; treat them with caution:

- **Critic's claim that the "80% recovery" statement is an overstatement.** The paper computes Interaction/Full ratio, yielding Haiku 79.3% and Sonnet 3.5 80.2% — both approximately 80%. The critic erroneously computed gap recovery instead. **Removed** — the paper's claim checks out.
- **Critic's §2.1 concern about generalizability of GPT-4o-generated vs. natural underspecification.** The paper already provides distributional analysis (§2.1) and explicit justification. The critic's concern is addressed in the paper. **Removed.**
- **Critic's §4 comment that Deepseek's behavior is "under-discussed."** Subjective opinion about depth of discussion, not a weakness. **Removed.**
- **Critic's claim about "interdependence of gaps" being asserted rather than demonstrated.** Speculative and not central to the paper's contribution. **Removed.**
- **Critic's point about text-embedding-3-small creating "single-vendor dependency."** Using a specific embedding model is standard practice; this is not a meaningful weakness. **Removed.**
- **Critic's §3.2 "80% gap recovery" inconsistency in takeaway box** — the main text correctly uses Interaction/Full ratio (~80%), and the takeaway's phrasing "performance gap" is a minor wording inconsistency that does not affect the paper's claims. **Removed.**
- **Weaknesses from Strength Finder that were generic or not backed by evidence:** removed per filtering discipline (generic statements about "addressing an important problem" that lack specific evidence).

## Novel Insights

None beyond the paper's own contributions. The reviews surface that the RQ2 detection experiment has a cleaner interpretation issue than the paper fully acknowledges (it measures willingness-to-interact, not detection ability *per se*), but this is already implicitly present in the experimental design and does not constitute an unclaimed flaw.

## Suggestions

1. **Correct the "up to 74%" claim** in the abstract and introduction to accurately reflect the data, and specify which computation is being used (relative improvement, gap recovery, or another metric).
2. **Re-evaluate Claude Sonnet 4's Hidden setting** on the full 500-instance set, or provide a detailed sensitivity analysis showing the 100-instance subset is representative.
3. **Add 95% binomial confidence intervals** to all resolve rate figures and tables.
4. **Use a different model as LLM-as-judge** for the question quality metric to break the GPT-4o circularity.
5. **Add a discussion of the detection-vs.-decision conflation** in the limitations section (§7).

## Score and Decision

The paper makes a clear contribution — a structured diagnostic framework for evaluating how LLM agents handle underspecification, a useful dataset variant, and several genuinely surprising empirical findings. The weaknesses are real but addressable: the Claude Sonnet 4 subset issue is the most significant and requires attention, but the overall pattern (interaction helps across models) is robust even setting that comparison aside. The paper is well above the acceptance threshold in terms of contribution and insight.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>