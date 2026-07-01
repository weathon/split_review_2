## Summary

This paper identifies a failure mode in LLM unlearning — the "squeezing effect," where suppressing a target response causes probability mass to redistribute to semantically related high-likelihood alternatives, yielding only surface-level forgetting. The paper proposes a bootstrapping framework (BS-T at the token level, BS-S at the sequence level) that penalizes both the target and the model's own high-confidence predictions, and provides theoretical analysis connecting the method to learning dynamics. Experiments on TOFU and WMDP benchmarks show modest improvements over existing baselines.

## Strengths

1. **Well-identified and empirically demonstrated failure mode (Section 3, Figure 2).** The paper convincingly illustrates that NPO-based unlearning produces outputs that are semantically similar to the original while standard metrics suggest success. The diagnostic analysis in §3.2 — grouping generations by likelihood bands and showing that high-likelihood outputs maintain the highest semantic similarity to targets — is clean and informative. This problem diagnosis is a genuine contribution independent of the method.

2. **Method follows directly from the diagnosis.** The insight that probability mass shifts to high-likelihood neighborhoods corresponding to the model's own confident predictions leads naturally to methods that suppress those predictions. BS-T (interpolating a soft target with the top-k distribution) and BS-S (augmenting the forget set with sampled high-confidence sequences) are intuitive instantiations of this idea. The coherence between problem analysis and solution design is a strength.

3. **Theoretical grounding (Section 5).** Connecting the method to the AKG learning dynamics framework to show how BS-T reshapes the residual term compared to GA goes beyond what most unlearning papers provide. This analysis explains *why* suppressing the top-k neighborhood changes gradient dynamics.

## Weaknesses

### Fatal

None.

### Major

1. **LaaJ evaluation is too sparse to resolve the metric tension; paper overclaims its LaaJ results.**  
   The paper convincingly argues (§3.1) that standard metrics (ROUGE, Probability, Truth Ratio) can *misreport* actual success — yet the main TOFU results (Table 1) use Memorization scores that include Paraphrased Probability and Truth Ratio, metrics whose reliability the paper itself questions. The LLM-as-a-Judge (LaaJ) evaluation is presented as a more reliable alternative, but it is shown for only one setting (TOFU 10%, one model). Furthermore, the reported LaaJ numbers (Figure 4c) do **not** support the paper's claim that "BS-T and BS-S obtain higher Naturalness and Similarity than baselines" (line 343). Checking the table directly: GradDiff achieves higher Similarity (4.8) than BS-S (4.3) and BS-T (4.1); SimNPO achieves higher Naturalness (4.5) than BS-S (3.9) and BS-T (3.7). BS methods achieve a better *trade-off* across both dimensions, but the paper asserts a stronger result that is not borne out by its own numbers. Combining the metric tension with the sparse and partially overclaimed LaaJ evidence, the experimental support for the central claim (that BS methods achieve "more thorough forgetting") is weaker than needed.

2. **No variance or statistical quantification of results.**  
   The improvements in Table 1 are often small (0.01–0.04 on aggregate scores over the best baseline). No standard deviations, confidence intervals, or significance tests are reported. Given that these differences are within typical run-to-run variance for LLM fine-tuning, the robustness of the claimed improvements is unclear.

3. **Theory scope gap relative to the main empirical comparison.**  
   Theorem 5.2 formalizes the advantage of BS-T over GA by comparing their residual structures. However, the paper's primary empirical baseline is NPO, not GA. NPO's residual structure differs from GA's in ways the theory does not address (NPO is an instance-weighted variant with a sigmoid-style weighting). The paper does not show that the theoretical advantage of BS-T over GA extends to BS-T over NPO — which is the practically relevant comparison. The theory also relies on the lazy eNTK assumption and first-order expansion, which are strong and unvalidated in this context.

### Minor

1. **BS-S assumption about sampled continuations not directly verified.**  
   BS-S assumes that any high-confidence continuation of a forget prompt constitutes a "belief" that should be erased. The paper provides indirect evidence (Figure 2a shows high-likelihood generations are semantically related to targets) but does not directly analyze what BS-S actually samples (e.g., are they semantically related rephrasings, or could they include generic template completions or refusal patterns?). Unlearning unrelated continuations could degrade utility without improving forgetting.

2. **No analysis of LaaJ judge reliability.**  
   Gemini 2.5 Flash is used as the LLM judge (line 343), but the paper provides no analysis of the judge's calibration, agreement with human raters, or potential biases. Since LaaJ is presented as a key diagnostic tool that addresses the limitations of standard metrics, its reliability is important to establish.

3. **Small absolute improvements on WMDP.**  
   On WMDP (Table 2), BS-S achieves 0.26/0.27 (Bio/Cyber) vs. NPO's 0.27/0.30 and RMU's 0.29/0.27. Differences of 0.01–0.02 on QA accuracy are marginal, and without variance reporting it is unclear whether these are meaningful.

### Trivial

None.

## Nice-to-Haves

- Expand the LaaJ evaluation to cover all experimental settings (all benchmarks, model sizes, forget ratios) and use it as a primary rather than supplementary metric.
- Report results from multiple random seeds with variance.
- Provide examples of the high-confidence continuations BS-S samples and unlearns, to verify they are semantically related to the target knowledge.
- Extend the theoretical analysis to compare BS-T with NPO residuals, or acknowledge the gap and provide empirical evidence that NPO's squeezing dynamics are similar enough to GA's for the same analysis to apply.
- Include hyperparameter sensitivity (λ_BST, λ_BSS) in the main paper.

## Removed Points

These points were flagged by the reviewer but are removed for the indicated reasons:

- **MUSE results deferred to appendix.** The reviewer notes that MUSE results are in Appendix F.3, not the main paper. However, the appendix exists in the original submission and was stripped by the parser. Deferring results to an appendix is standard practice for space-constrained submissions. The paper clearly references the appendix location. REMOVED per parser-stripping rule.
- **Section 3 only shows results on TOFU 10%.** The reviewer notes that the claim "spurious unlearning is not a corner case but a systematic outcome of NPO" is only supported by one setting. This section is a diagnostic analysis — it identifies and characterizes a phenomenon rather than providing comprehensive evaluation. The diagnostic evidence is sufficient for its purpose. REMOVED as scope-creep.
- **"Modest improvements" as standalone criticism.** Merged into the "no variance" weakness rather than listed separately.
- **Table formatting/style concerns.** REMOVED as formatting nitpicks.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Correct the factual overstatement about LaaJ results (line 343). The numbers show BS methods achieve the best *trade-off* across Naturalness and Similarity, not the highest score on each dimension individually.
- Add a clear justification for why using the same class of metrics critiqued in §3 is appropriate for the main experimental comparison. For example, note that benchmark-standard aggregate metrics (Memorization) differ from the individual metrics shown to be misleading, and that comparisons between methods on the same metrics are valid even if absolute metric values can be gamed.
- Run experiments with at least 3 random seeds and report means and standard deviations, especially given the small margins of improvement.

## Score and Decision

<score>5.0</score>
<decision>Reject</decision>