## Summary

This paper investigates the phenomenon of "benign relearning" in machine unlearning for LLMs — the recovery of supposedly-forgotten content through fine-tuning on benign data. It challenges the prevailing view that topical relevance drives benign relearning, arguing instead that surface-form/template overlap (which it calls "syntactic similarity") is the primary driver. The paper re-evaluates the BLUR benchmark to show its topicality-based conclusions are confounded by unequal training budgets and single-epoch evaluation. It then constructs controlled relearn sets on TOFU to isolate template overlap from topical relevance, finding that syntactically similar data consistently triggers more recovery. A mechanistic analysis reveals that unlearning disproportionately suppresses template tokens rather than keyword tokens, leaving keywords recoverable via structural restoration. The paper proposes syntactic diversification (paraphrasing forget queries into diverse surface forms before unlearning) as a mitigation.

## Strengths

1. **Careful confound analysis in the BLUR re-evaluation (Section 4, Figure 3).** The critique that BLUR's differing dataset sizes produce different numbers of gradient updates, and that reporting at one epoch conflates training budget with topical relevance, is well-founded. The standardized step-budget evaluation is a genuine methodological improvement. The finding that D_low (Lorem Ipsum) achieves recovery comparable to D_hi and D_mid in WHP is a striking result that motivates the rest of the paper.

2. **Mechanistic analysis connecting template overlap to parameter updates (Section 6).** The two-part analysis—(a) representation and gradient similarity (Figure 5) showing that syntactically similar sets align more closely with target sets than topically relevant sets across GA, NPO, and SCRUB; and (b) the template-vs-keyword loss ratio (Figure 6) showing unlearning suppresses template tokens more than keywords—provides a plausible mechanism for *why* surface-form overlap drives relearning, not just evidence *that* it does. The loss-ratio finding is the paper's most insightful contribution.

3. **The mitigation method (syntactic diversification) is simple, motivated, and follows directly from the analysis.** The method is grounded in the mechanistic story: if unlearning targets templates rather than keywords, breaking template homogeneity should force keyword-level forgetting. The measured drop in syntactic similarity from 0.4513 to 0.2241 (Section 7.1) confirms the intervention works as intended.

## Weaknesses

### Fatal

None.

### Major

1. **"Syntactic similarity" is operationalized via character-level Levenshtein distance, which measures surface-form/character-string overlap, not syntax in a linguistically meaningful sense.** Two sentences can share identical dependency structures but have low Levenshtein similarity, or share many characters but have very different syntax (e.g., different constituent structures or grammatical relations). The paper consistently uses the term "syntactic similarity" (abstract, introduction, Sections 5–7) for what is actually template/character-string overlap. The TOFU dataset's highly templatic structure is an artifact of synthetic data generation — real-world text rarely repeats exact question templates at this density. The paper acknowledges alternative measures (template-mining similarity, parse-tree similarity) only in a footnote referencing Appendix I (line 141), whose content cannot be assessed. This does not invalidate the empirical findings (the observed effect is real), but it means the paper's central explanatory variable is mischaracterized and claims more generality than its operationalization supports. (Lines 23, 103–109, fn. 1)

2. **The experimental scope is too narrow to support the broad claim that syntactic similarity is the "primary driver."** The core analysis (Section 5) and method evaluation (Section 7) are conducted on a single dataset (TOFU, forget05 scenario) with a single model (Llama-2-7b-chat). The main results for the mitigation (Figure 8, Table 2) are shown only under Gradient Ascent (GA). The BLUR re-analysis provides breadth across benchmarks and methods, but it only critiques BLUR's conclusions — it does not independently validate the syntactic similarity hypothesis on those benchmarks with controlled, parallel construction of relearn sets. Appendix results on Phi and LoRA are referenced but their content is not in the main body. The claim that syntactic similarity is "the primary driver" and that diversification "consistently suppresses benign relearning" are broad comparative claims resting on narrow evidence. (Sections 5–7; Figures 4, 8; Table 2)

3. **No variance or statistical significance reporting anywhere in the paper.** Every result is a single point estimate: no error bars, confidence intervals, standard deviations across runs, or statistical tests. Without variance estimates, the reader cannot assess whether observed differences (e.g., D_syntactic vs D_topic in Figure 4, or utility improvements in Table 2) are reliable or within natural noise. The claim that topical relevance is "not the primary driver" requires showing the relationship between syntactic similarity and recovery is significantly stronger — no such comparison is performed. (Confirmed: grep for "variance", "error bar", "standard dev", "confidence interval", "statistical", "seed" returns zero matches.)

4. **The syntactic diversification evaluation is incomplete.** (a) Figure 8 and Table 2 report results only for GA. Since the proposed mechanism (template suppression) should apply broadly, the paper should show whether diversification works under NPO or SCRUB. (b) Robustness is evaluated only against D_syntactic as the relearn set (line 287: "under relearning with D_relearn^syntactic") — we do not know whether diversification also protects against D_topic or other constructions. (c) The utility comparison (Table 2) compares D_forget vs D'_forget, but D'_forget contains multiple paraphrases per query and is thus larger in volume. The improvement could stem from increased data quantity/diversity rather than diversification per se. (Section 7; Figure 8; Table 2)

### Minor

1. **Confound in the TOFU experimental design.** The two relearn sets differ not only in syntactic similarity but also in the *type of information* queried: D_topic asks about birthplaces and occupations (non-name information), while D_syntactic asks about full names (the actual target information format). D_syntactic might drive stronger recovery simply because it's closer to the *format* of the target query, not because of syntax per se. (Lines 116–117, examples on lines 121–137)

2. **The loss ratio analysis (Figure 6) does not specify which unlearning method produced the curves.** The figure labels show "Unlearn (blue)" and "Relearn (green)" but do not indicate whether this is GA, NPO, or SCRUB. This makes it unclear whether the template-suppression mechanism generalizes across methods or is method-specific. (Figure 6, lines 217–231)

3. **Syntactic similarity differences in Table 1 are small and not statistically tested.** On WMDP, the scores are 0.2244, 0.2059, and 0.1771 across D_hi, D_mid, D_low. On WHP, D_low (0.1818) is actually *higher* than D_mid (0.1767). The paper asserts these explain BLUR's ordering (line 177: "can be largely attributed to their syntactic similarity") but does not compute a correlation or regression to test whether syntactic similarity predicts recovery better than topicality. (Table 1, line 177)

4. **The paper relies on GPT-4o for paraphrasing** (Section 7.1), which raises reproducibility and cost concerns. No comparison with simpler paraphrasing methods (e.g., rule-based or smaller open models) is provided to assess whether the benefit comes from diversification itself or from GPT-4o's particular paraphrasing quality.

### Trivial

None.

## Nice-to-Haves

- Running the diversification experiment on at least one more unlearning method (NPO or SCRUB) and demonstrating effectiveness beyond D_syntactic as the relearn set.
- Adding variance estimates (3 random seeds with error bars) would transform the credibility of every figure and table.
- A direct quantitative comparison (regression or correlation) between syntactic similarity and recovery strength, controlling for topical relevance, would sharpen the "primary driver" claim.
- Controlling for the confound between query format (name vs. non-name) and syntactic similarity in the TOFU experimental design.

## Removed Points

- "The 1.00 values for all self-similarities in Figure 5 are suspiciously clean" — **REMOVED**: self-similarity of the target set with itself is definitionally 1.00; this is expected, not suspicious.
- "Broader implications (Section 8) are speculative" — **REMOVED**: discussion sections are appropriately speculative by nature; this is not a weakness.
- "The paper should compare against alternative mitigation baselines (data augmentation, regularization)" — **REMOVED**: the contribution is a mechanistic analysis plus a motivated mitigation; requiring exhaustive comparison against orthogonal approaches is scope creep.
- "Missing related works" — **REMOVED**: cannot verify existence of missing references as external sources are not available.
- Various formatting nitpicks — **REMOVED** per filtering rules (parser artifacts).

## Novel Insights

The review's most useful observation is that the paper's central finding is both real and mislabeled. The empirical phenomenon — that surface-form template overlap drives relearning more than topical relevance in a templatic synthetic dataset — is convincingly demonstrated and mechanistically explained (template vs. keyword token suppression). But the paper consistently overclaims by framing this as "syntactic similarity." The loss-ratio analysis is the paper's most original contribution and does not depend on the "syntax" framing to be valuable. If reframed as "surface-form template overlap drives relearning in synthetic unlearning benchmarks," the paper's contributions would be more defensible and its claims more honest.

## Suggestions

1. **Reframe the central concept.** Replace "syntactic similarity" with a more precise term such as "surface-form similarity" or "template overlap" throughout. The current Levenshtein-based measure captures character-string overlap, not syntax in any linguistic sense. If the authors wish to retain the "syntactic" framing, they should replace the metric with a proper syntactic measure (e.g., tree-edit distance on dependency parses).

2. **Broaden the evidence base.** The core analysis would benefit from at least one additional dataset and one additional model family in the main paper (not just the appendix). The diversification evaluation should be shown for at least NPO or SCRUB.

3. **Add variance reporting.** Run experiments with 3 random seeds and report error bars or confidence intervals on all quantitative results. This is standard practice for comparative claims.

4. **Acknowledge the TOFU confound.** Discuss whether the different query types (name vs. non-name questions) could affect the results, and consider controlling for this by using name-format questions for both D_topic and D_syntactic (varying entities while keeping format constant).

5. **Quantify the comparison.** Add a correlation or regression analysis to directly compare how syntactic similarity vs. topical relevance predicts recovery strength across the BLUR datasets, rather than relying on qualitative interpretation of Table 1.

## Score and Decision

**Round 1 Bracket:** 5.0–6.5 (based on comparison with anchors).

**Anchors retrieved:**
- "Jogging the Memory of Unlearned LLMs Through Targeted Relearning Attacks" (6.75, Accept) — Very similar relearning topic, broader evaluation but less specific mechanism claim. Current paper is slightly weaker.
- "A Closer Look at Machine Unlearning for Large Language Models" (6.00, Accept) — Comprehensive evaluation, proposes methods and metrics. Current paper has more novel specific finding but weaker evidence.
- "Evaluating Deep Unlearning in Large Language Models" (5.33, Reject) — Interesting finding about logical deduction vulnerability, but rejected for narrow scope on synthetic dataset. Closest parallel to current paper.
- "UnSTAR: Unlearning with Self-Taught Anti-Sample Reasoning" (5.50, Reject) — Novel method rejected for practicality concerns.
- "Tool Unlearning for Tool Augmented LLMs" (5.17, Reject) — Novel task rejected.
- "Meta-Unlearning on Diffusion Models" (4.00, Reject) — Vision-domain relearning, scope concerns.

**Narrowing:** The paper has genuine contributions (BLUR re-evaluation, template-vs-keyword mechanism, diversification method) but the "syntax" framing is imprecise, the experimental scope is narrow (one dataset, one model, one method for the mitigation), and there is no variance reporting. These weaknesses are structural enough that acceptance would require substantial additional work. Comparable to "Evaluating Deep Unlearning" (5.33, Reject) in both contribution style and limitation profile.

**MY FINAL SCORE: <score>5.5</score>**
**MY FINAL DECISION: <decision>Reject</decision>**