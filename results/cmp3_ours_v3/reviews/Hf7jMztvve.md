Now I have strong calibration anchors. Let me finalize the review with the calibration context.

**Bracket determination (Round 1):** Based on the anchors, this paper sits between "Tall Tales at Different Scales" (3.67, Reject) and "pSAE-chiatry" (2.50, Reject). It is significantly less rigorous than "How to Catch an AI Liar" (6.75, Accept), "BeHonest" (5.00, Reject), and "Towards Principled Evaluations of SAEs" (7.00, Accept). The paper has a creative testbed and tests 38 models, giving it an edge over pSAE-chiatry (2.50), but its central claims (Contributions 3 and 4) lack systematic quantitative evidence, putting it below the benchmark papers at 3.67–5.00 level. **Narrowest bracket: 3.0–4.0.**

**Narrowing pass:** Comparing specifically to "Tall Tales" (3.67): that paper had more systematic experiments (scaling trends, fine-tuning) but also suffered from qualitative reporting and missing details. Our paper has a cleaner testbed but weaker evidence for the mechanistic claims. I anchor at **3.0 (Reject)** — the evidence gap for the core contribution is too large for borderline-reject territory.

Here is my final review:

---

## Summary

This paper investigates whether current auto-labeled Sparse Autoencoder (SAE) features capture the neural mechanisms underlying strategic deception in LLMs. It introduces two testbeds: (1) "Secret Agenda," a social-deduction game synthetic transcript that tests whether 38 models lie when incentivized, and (2) Insider Trading compliance scenarios analyzed through Goodfire 8B (labeled) and 70B (unlabeled) SAE architectures. The headline findings are that all 38 models lied at least once under incentive, that auto-labeled deception features rarely activated during deception and could not prevent lying through steering, and that unlabeled aggregate activations showed discriminative structure for compliance detection in the Insider Trading domain.

## Strengths

- **The Secret Agenda testbed is a clean, reproducible design for eliciting incentive-driven deception.** The paper constructs a binary choice (admit Fascist identity and lose, or lie and potentially win) at a fixed decision point in Round 6 using synthetic game history (Section 5.1). This isolates the moment of strategic dishonesty better than open-ended conversation, and the synthetic transcript enables exact replication.

- **Testing across 38 models provides meaningful breadth.** The behavioral result that every tested model lied at least once under these incentives is a clear existence proof that spans model families (Claude, Gemini, Grok, Llama, OpenAI, Perplexity, Qwen).

- **The limitations section (Section 8) is unusually transparent.** The paper explicitly acknowledges small sample sizes (n=2–30 per model), asymmetric analysis depth across testbeds, the need for LLM-as-a-Judge budget they lacked, and that results are preliminary.

## Weaknesses

### Major

- **The central claim that "100+ deception-related features failed to prevent lying" is not supported by systematic quantitative evidence.** The abstract and Contribution 3 assert this as a headline finding, but Section 6.3 provides only one concrete example (the "tactical deception and misdirection methods" feature) and a qualitative statement that "none of the features... resulted in non-lies." There is no table of feature IDs, auto-labels, steering strengths, trial counts, or proportions of deceptive outputs before vs. after steering. The "Bananas" sanity check is a single anecdote. The reader cannot independently assess whether this was a systematic test of 100+ features or a handful of cherry-picked examples. For a claim presented as a central contribution, this level of reporting is insufficient. (Section 6.3, abstract, Contribution 3)

- **The t-SNE cluster separation claims (Contribution 4) lack any quantitative validation.** The paper asserts that unlabeled SAE activations "provide discriminative signal for compliance detection" based on visual inspection of t-SNE plots (Figure 4). t-SNE is a nonlinear stochastic method that can create apparent clusters from random noise; no quantitative cluster quality metric (silhouette score, adjusted Rand index) or classifier-based evaluation (e.g., AUROC on held-out activations) is reported. The heatmaps (Figure 5) are also visual-only. Since the contrast between "labeled features fail" and "unlabeled activations work" is the paper's primary narrative arc, the lack of any quantitative validation for the latter claim critically weakens the argument. The paper does rank features by mean-difference (a quantitative step in Section 7.1) but never measures whether the resulting clusters are actually separable. (Section 7.2, Figures 4–5)

### Minor

- **Behavioral result framing overstates what the data show.** The abstract says Secret Agenda "reliably induced lying" and Section 5.2 calls it "systematic deceptive behavior." What the data establish is: 38/38 models lied *at least once* — an existence proof. Sample sizes range from n=2 to n=30 per model, and the paper's own limitations (Section 8.1) state they are "insufficient for robust frequency estimates." At the individual-model level, e.g., Meta-Llama shows 7 lies from 11 trials — this does not establish "reliable" or "systematic" deception per model. The existence claim is valuable; the framing should match the caution of Section 8.1.

- **Secret Agenda response classification methodology is unspecified.** The paper reports counts of "truth," "partial or partial lie," and "lie" per model family (Table 1/Figure 1) but does not state who performed this classification, under what rubric, or whether inter-rater reliability was measured. Section 8.3 mentions "manual analysis (~160 examples)" but this detail belongs in the methods section, not buried in limitations. The classification labels are central to the behavioral results.

- **Prompt variation results are incompletely reported.** Five variants are listed in Section 5.3 (primary, Snails vs Slugs, Truthers vs Liars, Day vs Night, Pink vs Turquoise, plus Shortened). Only two have numerical results (primary: 38/38; Snails vs Slugs: 6/6). The remaining four are described only qualitatively ("continued to observe... strategic deception"). Per-variant counts should be reported or the exploratory nature stated.

- **Abstract generalizes beyond the evidence.** The claim that "aggregate unlabeled activations provide population-level structure for risk assessment" (abstract) is only demonstrated in the Insider Trading compliance domain, not in the deception domain. The paper's own Section 8.3 explains why the latter was infeasible, but the abstract presents the finding as a general result. The conclusion (Section 10) is more measured ("in the insider-trading setting... may support risk assessment"); the abstract should match.

### Trivial

- The "100+ deception-related features" count appears only in the abstract with no corresponding enumeration in the body.

## Nice-to-Haves

- A systematic table of steering experiments: feature ID, auto-label, steering strength, trials, proportion of deceptive outputs pre/post steering.
- A quantitative cluster validation metric (silhouette score or AUROC) for the t-SNE results.
- Specification of the Secret Agenda response classification methodology (who classified, rubric, inter-rater reliability).
- Numerical results for all prompt variants tested, or explicit statements about which were exploratory.

## Removed Points

- **Issue 3 (domains differ undermining contrast):** Removed. The paper's Section 8.3 explicitly acknowledges this asymmetry and frames the testbeds as complementary, not a controlled comparison. The abstract's generalization is addressed under Minor weaknesses above (framing tension), but this is not a structural flaw.

- **Table 1 undermines the paper's framing:** Removed. The paper's claim is about auto-labeled *deception* features failing in the *deception domain*. Table 1 shows discriminative features for insider trading compliance, a different phenomenon. Section 7.3 correctly attributes the insider trading success to aggregate activations distinguishing compliance behaviors.

- **Role-play confound:** Removed. The paper's Section 2 explicitly adopts a behavioral definition of deception that "remains agnostic to assumed beliefs." The role-play interpretation is a non-issue under the paper's own operational definition.

- **References to non-academic sources:** Removed per rules. The paper may cite any sources it considers relevant.

- **Missing related work:** Removed per rules (cannot confirm existence of works not cited).

- **Reproducibility concerns about screenshots:** Demoted from the reviewer's original framing. The paper also provides Colab notebooks, API references, and version identifiers; screenshots are supplementary documentation.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a table of all features tested in steering experiments with quantitative pre/post behavior change metrics.
2. Add a quantitative cluster validation metric (silhouette score or classifier AUROC) for the t-SNE results.
3. Report the Secret Agenda response classification methodology (who classified, rubric, inter-rater reliability).
4. Tone down the abstract to match the cautious framing of Section 8.
5. Report numerical results for all tested prompt variants.

## Score and Decision

**Calibration anchors (all retrieved papers):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| YRXDl6I3j5 (Tall Tales at Different Scales) | 3.67 | 2 | Similar topic (LLM deception), more systematic experiments but similar qualitative reporting issues. Our paper has cleaner testbed but weaker mechanistic evidence. |
| ijFdq8uqki (BeHonest) | 5.00 | 2 | Benchmark for LLM honesty with more rigorous evaluation. Our paper is less systematic. |
| LQdaXixB0g (pSAE-chiatry) | 2.50 | 1 | Similar qualitative SAE analysis approach, rejected. Our paper tests more models and has a more creative testbed. |
| 567BjxgaTp (How to Catch an AI Liar) | 6.75 | 1 | Much more rigorous lie detection paper with proper statistical evaluation, generalization tests, ablations. Our paper is far from this level. |
| 9ca9eHNrdH (SAEs Do Not Find Canonical Units) | 7.00 | 1 | High-quality negative result about SAEs with clever experimental design. Our paper lacks comparable rigor. |
| 1Njl73JKjB (Towards Principled Eval of SAEs) | 7.00 | 1 | Rigorous SAE evaluation framework. Our paper is significantly less rigorous. |
| ZtvRqm6oBu (Applying SAEs to Unlearn Knowledge) | 5.25 | 1 | SAE application paper rejected despite more systematic evaluation. Our paper is less rigorous. |

**Round 1 bracket:** [3.0, 4.0]

The paper has a creative and well-motivated testbed (Secret Agenda) and tests across 38 models, which are genuine positives. However, the core claimed contributions — that auto-labeled SAE features systematically fail to capture deception, and that unlabeled activations provide discriminative signal — are not supported by adequate evidence. The steering experiments are reported qualitatively with no systematic results table, the t-SNE analysis lacks any quantitative validation, and the abstract generalizes beyond what the evidence supports. The paper reads as a well-motivated pilot study that does not yet deliver on its ambitions.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>