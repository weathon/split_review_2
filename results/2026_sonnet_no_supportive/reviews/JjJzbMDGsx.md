Based on calibration, the most similar papers (decoding-time lightweight LLM plug-ins with logit manipulation: ShieldHead avg 5.75, SASA avg 6.0) sit around 5.75–6.0. LCG has stronger mechanistic grounding (embedding norm decomposition), broader evaluation across 7 models, and a more principled training strategy than those analogues, but has the underspecified code-switching evaluation as a major gap. I'll place this at **6.5** — a borderline accept with a real but fixable evidentiary gap.

---

## Summary
This paper introduces the Language Confusion Gate (LCG), a lightweight two-layer MLP plug-in that reduces unintended language mixing in LLMs without modifying the base model. The core insight is that output token embedding norm imbalance systematically biases logits toward high-resource language tokens; a gate trained via norm-adjusted self-distillation on the model's own debiased predictions learns to predict permissible language families and masks disallowed tokens only when needed. Evaluated across 7 open-weight models spanning thinking and non-thinking modes, LCG reduces CJ and Latin confusion by an order of magnitude with negligible task performance degradation and 0.4% latency overhead.

## Strengths
- **Mechanistic insight (Section 3.2, Table 1, Figure 2):** The decomposition logitᵢ = ‖h‖ · ‖eᵢ‖ · cos_sim(h, eᵢ) identifies a specific, testable causal mechanism for high-resource language token bias. Table 1 shows CJ and Latin tokens occupy the top-5% norms at 4–11% vs. 0.07–2.4% for Low-Res, and Figure 2 demonstrates that norm-adjusting logits immediately removes CJ tokens from the top-10 at a Hebrew translation confusion point. This is a novel diagnostic contribution that would generalize beyond the language confusion problem.
- **Norm-adjusted self-distillation (Section 4.2):** Elegant data-free training strategy that uses the model's own debiased predictions as pseudo-labels, requiring no labeled corpus of language confusion examples.
- **Broad, consistent empirical results (Tables 3–4, Figure 3):** Across 7 diverse models covering different architectures, sizes, and thinking/no-think modes, reductions are consistent and large (e.g., Qwen3-30B CJ% 1.0→0.0%, Latin% 4.4→0.4%; Qwen3-8B CJ% 4.5→0.1%) with BLEU and accuracy essentially unchanged. The comparison with ICL, greedy decoding, and ORPO baselines (Figure 3) is informative.
- **Principled evaluation design (Section 5.2):** The FLORES-NO-LATIN/FLORES-WITH-LATIN split provides a rigorous way to measure confusion vs. legitimate code-switching, and the rationale for not using LCB is specific and defensible.
- **Practical efficiency (Section 6):** 0.4% latency overhead, 0.33–0.38% intervention rate, and compatibility with speculative decoding make the approach deployable.

## Weaknesses

### Fatal
None.

### Major
- **Underspecified code-switching preservation evidence (Section 5.3).** The 86.7% figure is the most direct evidence for LCG's central distinguishing advantage over rule-based blocking — that it can tell erroneous confusion from legitimate code-switching — yet neither the sample size nor inter-annotator agreement is reported for the human annotation study. Table 5 measures only a coarse "any Latin character present" signal that cannot distinguish appropriate from inappropriate code-switching; the paper explicitly notes the reference baselines are "not ground truth." The core differentiating claim is left incompletely supported.

### Minor
- **Residual confusion ceiling not decomposed (Section 5.3, Table 3).** Post-intervention Latin% remains 0.4–2.9%. The paper acknowledges in Section 6 that intra-script confusion (e.g., English into French) is structurally unreachable by the gate. For Llama3.1-8B at 2.9%, readers cannot tell whether this reflects an inherent ceiling or gate imprecision. Decomposing residual confusion into (a) intra-script and (b) gate error would clarify whether the remaining Latin% is improvable.
- **Training pseudo-label generation hyperparameters omitted (Section 4.2).** The specific k and p values used to construct pseudo-labels during training are not stated; only inference values (k=5/20, p=0.999/0.95) appear in Section 4.3. This affects reproducibility of the training procedure.
- **Intervention rule 3 cascade risk unanalyzed (Section 4.3).** The rule "always allow the language family of the immediately preceding non-symbol token" means a gate failure on the first confused token could permit subsequent confused tokens. Given that the confusion token is top-1 56.74% of the time (Section 3.1), this is a concrete interaction the paper leaves unaddressed.

### Trivial
- Table 4 caption reads "Effectiveness of LCG Intervention on 'No-Think' Models" but the table reports thinking-model results (Qwen3-8B/30B thinking, GPT-OSS).
- Claude-Sonnet-4 shows 0.00% CJ and 0.35% Latin confusion (Table 2), suggesting some SOTA models may largely solve this; the caveat that commercial interventions may already exist is buried in a table footnote in Section 3.4 rather than in the Introduction where the motivation is framed.

## Nice-to-Haves
- Report sample size and inter-annotator agreement for the 86.7% human annotation study; alternatively, annotate a random post-intervention sample from FLORES-WITH-LATIN and classify each Latin-containing response as appropriate or erroneous — this would directly support the central claim.
- Decompose residual post-intervention confusion into intra-script vs. gate-error categories per model/benchmark.
- Clarify whether the 99.29% correct-language-in-top-3 finding generalizes beyond Qwen3-8B (Section 3.1), since the entire method rationale depends on this observation.
- Evaluate Low-Res confusion scenarios: rule 1 never masks Low-Res tokens, so LCG's behavior when the confused language is Low-Res is unexplored.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **ORPO implementation fidelity concern (Harsh Critic, Section 5.3):** REMOVED per the hard rule — the performance asymmetry favors the ORPO baseline, not the authors' method; criticizing the comparison would work against the stronger claim being made.
- **Missing appendix content (Appendix G, H, I):** REMOVED — the parser strips appendices from all papers; they exist in the original submission.
- **"Language confusion far from solved" motivation caveat:** Partially retained as a Trivial issue; the underlying complaint that SOTA models may have partly solved this is noted, but not as a fatal motivation gap.

## Novel Insights
The logit decomposition logitᵢ = ‖h‖ · ‖eᵢ‖ · cos_sim(h, eᵢ) as a mechanistic explanation for high-resource language token bias is a genuinely novel diagnostic contribution that extends beyond this paper. It provides a clean, quantitative, and model-agnostic explanation for why greedy decoding fails to fix language confusion (the confusion token is top-1 56.74% of the time), and why norm-adjusted pseudo-labels are a principled — not merely heuristic — training signal. This geometric perspective on logit bias could be applied to other settings where vocabulary-level embedding norm imbalance skews generation, such as domain or register control in generation.

## Suggestions
1. Report sample size and inter-annotator agreement (or single-annotator methodology) for the 86.7% code-switch human annotation, or conduct structured annotation of post-intervention FLORES-WITH-LATIN classifying each Latin-containing response.
2. Add a residual confusion decomposition (intra-script vs. gate error) for the models with highest post-LCG Latin% (Llama3.1-8B 2.9%, Qwen3-8B 2.0%).
3. State the k and p hyperparameter values used for pseudo-label generation in Section 4.2.
4. Fix Table 4 caption to say "Thinking Models."
5. Move the commercial model caveat from the Section 3.4 footnote to the Introduction so the motivation is accurate at the point it is made.

---

## Score and Decision

**Anchor papers and comparisons (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| gwZ90hFSL2.md | 1.00 | R1 | Robotics/Chinese NLP — not comparable; far below LCG quality |
| 8QTpYC4smR.md | 1.00 | R1 | LLM survey — not comparable |
| fSbPwHjdDG.md | 3.00 | R1 | Causal intervention on latent language — topically closer but narrower and weaker empirically |
| eznTVIM3bs.md | 5.25 | R1 | Multilingual code LLM evolution study — similar analysis depth, LCG has stronger method |
| r3GxWNGpSj.md | 4.75 | R1 | XTransplant multilingual — LCG stronger mechanistic grounding and broader evaluation |
| NHCkILEmWn.md | 5.75 | R1 | ShieldHead (classification head on hidden states for safety) — most structurally similar; LCG has stronger mechanistic story |
| jY5oml9fe9.md | 6.00 | R1 | SASA (lightweight controlled decoding for toxicity) — similar spirit; LCG has clearer norm-bias theory and broader model coverage |
| TOveLu4O51.md | 5.75 | R1 | DetoxiGen (contrastive decoding for detox) — analogous genre; LCG stronger |
| CEvGuwMum0.md | 5.75 | R1 | JudgeRail (logit rectification for safety) — LCG has more principled training |
| Bo62NeU6VF.md | 8.00 | R1 | Backtracking for safety — significantly more technically developed than LCG |
| xoXn62FzD0.md | 8.00 | R1 | SMC for controlled LLM generation — more theoretically rigorous; LCG less novel |

**Round 1 bracket:** 6.0–7.0. LCG sits above ShieldHead/SASA/DetoxiGen (5.75–6.0) due to the mechanistic insight, broader 7-model evaluation, and principled training strategy. It sits below the score-8 papers (Backtracking, SMC) which are more technically ambitious and fully rigorous. The unverified code-switching claim is a real gap but the methodology is otherwise sound and the empirical scope is impressive.

**Final score:** 6.5 — borderline accept, reflecting a real and well-executed contribution with one major but fixable evidential gap.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>