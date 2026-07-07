Now I have all the data I need. Let me compile the final review.

---

## Summary

This paper proposes the Fast and Slow Effect (FSE) framework for evaluating whether LLM/VLM-generated concept annotations are "sufficient" for concept-based XAI. The framework progressively collects concepts across five annotation stages, then measures whether the same LLM can classify correctly using only those concepts (Class Representation Index, CRI). The paper reports that current annotation methods produce insufficient semantic coverage, with a 25%+ gap between vision-based (fast mode) and concept-based (slow mode) classification, and demonstrates that high downstream accuracy does not imply annotation quality (utility-as-proxy critique).

## Strengths

- **The utility-as-proxy critique (Table 4) is a genuine and well-demonstrated contribution.** The experiment shows that fused (fast+slow) mode achieves CRI near the fast mode (~90%) while the slow mode alone scores only ~50-60%. This cleanly demonstrates that high downstream accuracy does not imply annotation sufficiency, providing concrete evidence for a concern previously raised only theoretically. **Weight: +4.26**

- **The paper correctly identifies and articulates a real gap.** There is currently no established methodology for verifying whether automated concept annotations capture sufficient semantics, and the critique of both human evaluation challenges and the utility-as-proxy assumption (Section 3) is well-argued and grounded in prior work. **Weight: +3.29**

- **The motivating example (Figure 1) is compelling** and effectively communicates the core problem: an LLM correctly identifies a bird from images but, forced to use only its own textual concepts, chooses a different class. **Weight: +1.78**

## Weaknesses

### Major

1. **Self-consistency confound undermines the core claim.** The FSE framework uses the same LLM for both generating concepts and testing classification from those concepts. When the LLM fails at step 2, the paper attributes this to "insufficient concepts," but the failure could equally stem from the LLM's inability to reason from its own text, self-consistency failures, or the inherent difficulty of classifying from text alone. These confounds are never disentangled. The paper's central claim that "current annotation methods fail to provide sufficient semantic coverage" conflates annotation quality (a property of the concept set) with the LLM's text-based classification ability (a property of the LLM). Using a separate, fixed classifier (e.g., a text encoder + linear probe, or a different LLM) to evaluate concept sufficiency would substantially strengthen this claim. **Weight: -8.72** (this item merges the two most severe confounds)

2. **No reference standard for "insufficiency."** The paper defines annotation sufficiency (Definition 3.1) but provides no gold-standard baseline. Without knowing what CRI scores human-written concepts or expert annotations would achieve, it is unclear whether the observed 40-60% CRI on fine-grained datasets reflects annotation insufficiency or inherent task difficulty. The normative claim that annotations are "insufficient" is uncalibrated.

3. **The fast vs. slow mode comparison is confounded by modality asymmetry.** The paper frames the 25%+ CRI gap as evidence of annotation insufficiency, but the fast mode (t=0) uses the full pixel-level image while the slow mode (t>0) uses only text concepts. The information asymmetry makes the negative gap largely predictable. The "Slow Mode Superiority" hypothesis — that text-only concepts should outperform pixel-level vision — is motivated by dual-process theory from psychology (Kahneman, 2011) without any argument for why it transfers to LLMs. The absolute CRI scores (40-60% on fine-grained datasets) are independently informative and partially mitigate this concern, but the gap itself cannot be cleanly attributed to annotation quality.

### Minor

4. **CRI formula notational error.** Equation (2) defines CRI as (1/t) ∑_{i=1}^t 𝟙[y_i^t = y_i], but the test set has l instances (i=1,…,l), and t indexes annotation steps. The summation should run over i=1 to l with denominator 1/l. As written, the formula computes accuracy over only the first t instances. While the surrounding text clarifies the intent ("proportion of correctly predicted labels"), the notation as presented is mathematically incorrect.

5. **Claims about "current annotation methods" overstate what is evaluated.** The paper designs and evaluates its own 5-stage hierarchical annotation pipeline rather than directly running existing annotation pipelines (e.g., the specific prompts from Label-Free CBM or V2C-CBM). While Section 4.1 notes that the pipeline builds on prior 1/2/3-stage approaches, the 5-stage structure (Background, Superclass, Salient Features, Detailed Features, Auxiliary Features) is novel to this paper. Generalizing from this single pipeline to "current annotation methods" overextends the evidence.

6. **Missing sample sizes and statistical tests.** The paper does not report how many images were used in the main CRI experiments (only the 100-sample preliminary experiment is specified). No confidence intervals or significance tests are provided for the headline CRI-Gap differences in Table 2. The paper states standard deviations are "negligible" for Figure 3 but does not quantify this for the core fast-vs-slow comparison.

7. **Distractor selection via ResNet-18 introduces model-specific bias.** Using a pretrained ResNet-18 to define semantic similarity for distractor selection means the evaluation difficulty depends on a specific vision model's similarity judgments. This choice affects reproducibility and may not align with concept-level similarity. Different models could yield different distractor sets and thus different CRI values.

### Trivial

None.

## Nice-to-Haves

- Using a separate, fixed classifier (e.g., a small text encoder + linear probe, or a different LLM) to evaluate concept sufficiency would disentangle annotation quality from the generating LLM's reasoning ability.
- A small-scale human baseline study (even 50 examples per dataset) would establish an interpretable reference point for CRI scores.
- Directly testing the specific prompts from existing methods (Label-Free CBM, V2C-CBM) alongside the custom pipeline would better support claims about "current annotation methods."

## Removed Points

- "DeepSeek-R1 claim unsubstantiated" — REMOVED. The paper references Appendix D for these results, which was stripped by the parser; the original submission likely contains them. Per hard rules, appendix content is assumed present in the original submission.
- "5-stage pipeline underspecified / prompt details in appendix" — REMOVED. Same reason: prompt formulations were deferred to Appendix B, which was stripped by the parser.

## Novel Insights

None beyond the paper's own contributions. The most novel finding is the utility-as-proxy critique (Table 4), which provides clean empirical evidence that downstream accuracy gains from concept integration do not imply annotation quality — a finding with direct practical implications for the CBM and XAI communities.

## Suggestions

1. Fix the CRI formula notation (Eq. 2) to use l instead of t in summation bounds and denominator.
2. Report sample sizes and confidence intervals for all main experiments.
3. Supplement the same-LLM evaluation with a separate-classifier evaluation to disentangle annotation quality from LLM reasoning ability.
4. Add a human baseline to calibrate what CRI scores constitute "sufficient."
5. Tone down claims about "current annotation methods" to reflect that the evaluation uses a custom 5-stage pipeline inspired by prior work.

## Score and Decision

**Round 1 bracket:** 3.0–4.0.

**Anchors retrieved and compared:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| `/home/.../kTjEPEy96Q.md` | 3.00 | 1 | Yes | Similar area (CBM evaluation framework), but had a more severe conceptual fallacy (-11.99) than our paper's strongest negative (-8.72). Our paper has stronger positives. |
| `/home/.../KLUDshUx2V.md` | 3.40 | 1,2 | Yes | Same area (LLM concept bank evaluation), but had severe novelty concerns (-9.23) that our paper does not share. Our paper has methodological confounds instead. |
| `/home/.../a8wjeqTZ9C.md` | 3.75 | 2 | Yes | Related area (CBM label noise). Negatives max at -7.99 (merely experimental), comparable to our -8.72. |
| `/home/.../0qrTH5AZVt.md` | 4.67 | 1 | Yes | Concept-based explanations. Much weaker negatives (max -3.36). Our paper has stronger methodological concerns. |
| `/home/.../pNgY6ODeMp.md` | 4.25 | Narrow | Yes | Visual concept decomposition in CBMs. Negatives max at -8.55 (poor writing). Our paper's negatives are methodological rather than presentational. |
| `/home/.../5Aem9XFZ0t.md` | 4.83 | 2 | Yes | Zero-shot CBMs. Had strong novelty concerns (-9.80, -9.48) and strong positives (+5.42, +5.16). |
| `/home/.../RC5FPYVQaH.md` | 5.75 | 1,2 | No | CB-LLM paper. Higher-quality contribution at a different level. |

**Weighted-item comparison final placement:** The paper sits between the 3.00-3.40 anchors and the 3.75-4.25 anchors. Like the 3.00 anchor (kTjEPEy96Q), it has a fundamental evaluation-design concern (self-consistency confound vs. conceptual fallacy), but the severity is lower (-8.72 vs. -11.99). Like the 3.75 anchor (a8wjeqTZ9C), it has a solid empirical contribution in one area (utility-as-proxy critique) alongside methodological concerns. The paper lacks the severe novelty concerns of the 3.40 anchor (KLUDshUx2V, -9.23), but its methodological issues are more central than the presentation issues of the 4.25 anchor. Placing it at 3.5 reflects that the utility-as-proxy critique is valuable but the core evaluation methodology has confounds that prevent the paper's central claims from being fully supported as written.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>