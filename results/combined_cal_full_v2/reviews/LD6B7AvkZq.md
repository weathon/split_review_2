Now I have all the information needed. Let me produce the final review.

## Calibration Report

**Round 1 (Bracketing):** Retrieved anchors across all bands. The most topically similar anchors were:
- "How transformers learn structured data: insights from hierarchical filtering" (5.00, Reject) — studies transformer learning on PCFG data; comparable methodology and scope.
- "Depth Extrapolation of Decoders Trained on Nested Structures" (4.50, Reject) — studies decoder transformers on nested formal languages.
- "Training Neural Networks as Recognizers of Formal Languages" (6.25, Accept) — cleaner methodology, well-executed.
- "A Percolation Model of Emergence" (7.00, Accept) — more polished with a developed theoretical analogy.
- "Recovering Knowledge by Hardening Language Models" (3.00, Reject) — less novel, limited scope.

**Bracket:** [3.5, 5.5]. The paper clearly outranks the 1.0–3.0 anchors (pure surveys, flawed extraction methods) but has significant enough issues that it cannot reach the 6+ range of cleaner, better-executed work.

**Round 2 (Narrowing):** Itemized calibration on the closest 3 anchors within the bracket.

**Weighted-item comparison:** The paper's strengths carry strong positive weights (7.26–9.82). Its most damaging weakness — the garbled equation — carries weight -1.21, less severe than the most negative items in "How transformers learn structured data" (-4.73, -3.15). However, that anchor's negative items were about novelty/scope (more subjective), whereas this paper's garbled central equation is an objective mathematical error in the paper's "most important contribution." The remaining weaknesses (parallel learning underspecified, missing curriculum control, CKA over-interpretation) are real but not individually fatal.

**Final score:** 5.0. The paper sits just below the acceptance threshold. Its novel subgrammar framework and clean depth-vs-length experiment are genuine contributions, but the garbled mathematical exposition of the central theorem and the underspecified empirical claims prevent acceptance in the current form.

---

## Summary

This paper introduces a framework for studying how transformers learn context-free grammars through the lens of "subgrammar" structure. It defines inner and outer subgrammars, proves theoretical results showing that the KL divergence (equivalently, the language modeling loss) decomposes recursively over subgrammars, and presents empirical studies of subgrammar learning dynamics, curriculum learning via subgrammar pretraining, and generalization to deep recursion. The paper identifies a genuinely interesting question and makes a first pass at answering it, but suffers from serious mathematical presentation issues in its core theoretical derivation and underspecified empirical claims.

## Strengths

- **The core idea — studying CFG learning dynamics through subgrammar structure — is genuinely novel and well-motivated.** The observation (Section 1) that research on how neural networks learn function classes like polynomials has fruitfully studied substructure (monomials), and that CFG learning has lacked this lens, is perceptive. The connection to Gruska (1971) (grammatical levels) is appropriately acknowledged.

- **Section 6 (generalization to deep recursion) produces a clean and striking result.** Figure 3 cleanly separates two phenomena: models handle long contexts at fixed depth of recursion (error ~0.017) but fail on increasing depth (error ~0.173 at depth 200). The experimental design is simple, well-controlled, and directly targets the paper's motivating question about hierarchical syntax.

- **The CKA analysis in Section 5.2 is a genuine attempt to open the black box.** Computing representational similarity between pretrained and scratch-trained models and showing differences in how they cluster sequence types goes beyond loss curves and provides mechanistic evidence for the effect of subgrammar pretraining.

## Weaknesses

### Fatal
None.

### Major

- **The central theoretical derivation from Equation (1) to Equation (4) (lines 124–130) contains a garbled equation that does not parse as valid mathematics.** Equation (4) shows fractions of logarithms (log P / log Q) where the KL divergence requires terms of the form P·log(P/Q). This is not a parser artifact — the typesetting as `\frac{\log P}{\log Q}` is mathematically incorrect. While the surrounding text explains the conceptual idea (KL decomposes into a sum of conditioned KL-divergences), and a correct proof may exist in the appendix, the main-text exposition of what the paper calls its "most important contribution" (line 26) is unreliable as presented. A paper whose central theoretical claim cannot be verified from the main text alone has a serious communication failure.

### Minor

- **Definition 3.3 (Inner Subgrammar) has a formal closure issue.** It states that 𝒫' is "the set of all rules with non-terminals in 𝒩'." It is ambiguous whether this includes rules whose RHS contains non-terminals outside 𝒩' — if so, the subgrammar would not be self-contained; if not, the definition requires tightening. A similar ambiguity exists in Definition 3.5 (Outer Subgrammar). This matters because Theorems 4.1 and 4.3 depend on these definitions being well-behaved, though the issue is fixable with clarification.

- **The claim that models "learn all subgrammars in parallel" (lines 208–209) is underspecified.** The evidence (Figures 1, 2) shows all KL curves decreasing simultaneously, but this is largely a consequence of Theorem 4.3: if total KL = sum of subgrammar KLs and total KL is decreasing, the sum of subgrammar KLs is trivially decreasing. The paper provides no formal definition of what "sequential" learning would look like, no contrast condition, and no statistical test. Corollary 4.7 is essentially a tautology (if updates on subgrammar A_i don't hurt A_j, then all are learned in parallel) and is acknowledged as informal.

- **The curriculum learning comparison (Section 5) lacks an important control.** Pretraining on a subgrammar then finetuning on the full grammar may simply benefit from more total training steps compared to training from scratch on the full grammar. The paper acknowledges this trade-off in passing (lines 252–253) but does not provide the control experiment of training on the full grammar for an equivalent number of total steps.

- **The CKA results (Table 1) are over-interpreted relative to the evidence.** No variance is reported despite stating that 30 random seeds were used. The interpretation that pretrained models are "better at internally segregating sequences with and without subgrammar subsequences" (line 250) goes well beyond what CKA similarity alone can establish — higher CKA between layers of the same model does not directly demonstrate functional segregation of string types. Targeted probing would be needed.

- **The loss curves in Figures 1 and 2 show single trajectories without error bands or multiple runs.** Given that training involves random initialization and sampling, variance information is needed to assess reliability.

### Trivial

- **The "prediction error" metric in Section 6 (Figure 3) is never formally defined.** The text says the model's output logits are compared against the ground-truth next-token distribution (lines 274–275), but the specific distance metric (cross-entropy? total variation? KL?) is not stated.

## Nice-to-Haves

- A sketch of the KL decomposition proof's key steps in the main text rather than full deferral to the appendix.
- Explicit operational definition of "parallel learning" with a concrete criterion or null model.
- Control experiment for curriculum training: train on the full grammar for the same total number of steps as pretrain+finetune.
- Variance/error bars for all reported experimental results.

## Removed Points

These points were flagged for removal and should be treated with caution:

- **Theorem 4.6 not empirically validated:** The paper references "Appendix 4" for a visual representation. Per policy, criticisms about missing appendix content are removed since the parser strips appendices from all papers.
- **Grammar definitions relegated to appendix:** Same reason — appendix content was stripped by the parser. The grammar definitions exist in the original submission.
- **Natural language not fully captured by CFGs:** This concerns a single sentence in the abstract's framing. The paper studies toy CFGs and is upfront about this scope; it is not a substantive weakness about the paper's technical contribution.
- **Speculative fatal flaw from definitional closure:** The closure issue in Definition 3.3 is real but fixable with tightening; it does not make the paper's theory unsalvageable as the harsh critic suggested.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Fix Equation (4) to show correct KL decomposition terms (P·log(P/Q) not log P / log Q). Include a sketch of the proof's key steps in the main text rather than deferring entirely to the appendix.
2. Clarify Definitions 3.3 and 3.5 to ensure closure: explicitly state whether rules with RHS non-terminals outside 𝒩' are included or excluded.
3. Define "parallel learning" operationally with a concrete criterion or null model to test against.
4. Add a control to the curriculum experiments: train on the full grammar for the same total number of steps as pretrain+finetune.
5. Report variance/error bars for all experimental results (CKA, loss curves).
6. Define the "prediction error" metric used in Figure 3 explicitly.
7. Add error bands to loss curves in Figures 1 and 2 to show variance across random seeds.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>