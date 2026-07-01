Now let me read the remaining sections for completeness:Now I have a thorough understanding of the paper. Let me draft the review before calibration.Now let me perform calibration. Round 1 — Bracketing:Let me read a few anchor papers for calibration:Let me also look at a few more anchors in the 6-7 range:Now let me narrow my bracket with a Round 2 calibration search:Let me read the most closely comparable anchors:Now I have sufficient calibration data. Let me synthesize the final review.

**Round 1 Bracket: 5.5 to 7.0**

Based on anchors:
- Score 3.0 papers have fundamental methodological issues or presentation problems — LCG is clearly above this.
- Score 5.25-5.67 papers (Babel Tower, Crosslingual Capabilities) have similar scope limitations but less practical impact.
- Score 6.0 papers (SASA, Tool Decoding, OPAD, Nudging) are very closely comparable — lightweight decoding-time interventions with practical value but limited novelty or scope.
- Score 6.6+ papers (Same but Different) have more thorough analysis despite limited scope.
- Score 8.0 papers (DEPT) represent fundamentally more ambitious framework contributions.

**Round 2 Narrowing: 6.0 to 6.5**

The LCG paper is most directly comparable to the cluster of "lightweight decoding intervention" papers scoring 6.0 (SASA for detoxification, Tool Decoding for tool use, OPAD for preference alignment). LCG has a stronger mechanistic motivation (norm bias analysis) than most of these, but its evaluation circularity and scope limitations are comparable to the weaknesses in those papers. The novel mechanistic insight and 4-model-family consistency push it to the top of this cluster but not clearly above it.

---

## Summary
This paper introduces the Language Confusion Gate (LCG), a lightweight plug-in mechanism that reduces cross-script language confusion during LLM decoding without modifying base model weights. The method is motivated by a mechanistic analysis showing that output token embedding norm imbalance biases sampling toward high-resource languages. A small MLP is trained via norm-adjusted self-distillation to predict permissible language families (CJ, Latin, Symbols, Low-Res) and dynamically mask disallowed tokens, achieving substantial confusion reduction across four model families with 0.4% latency overhead.

## Strengths
- **Novel mechanistic insight on embedding norm bias (Section 3.2, Table 1, Figure 2).** The decomposition of logits into norm and cosine-similarity components, showing that CJ tokens occupy 10.74% of top-5% norms for Qwen3-8B vs. 0.14% for Low-Res, provides a concrete, well-evidenced explanation for cross-script confusion that both motivates the method and stands as an independent analytical contribution.

- **Strong practical deployment properties.** 0.4% latency overhead (15.95ms → 15.99ms per step), 0.33–0.38% intervention rate, no modification of base model weights, and compatibility with speculative decoding (Appendix F). These properties are quantified precisely and make the method immediately deployable, distinguishing it from retraining-based approaches.

- **Consistent cross-architecture results (Tables 3, 4).** CJ confusion on FLORES-NO-LATIN drops from 4.5% to 0.1% for Qwen3-8B, 1.0% to 0.0% for Qwen3-30B, and 3.0% to 0.4% for Llama3.1-8B. Effectiveness across Qwen3, Llama3.1, Gemma3, and GPT-OSS in both thinking and no-think modes demonstrates architectural generality without per-model retraining.

- **Meaningful distinction between confusion and code-switching (Section 5.3, Table 5).** The 86.7% token-level preservation rate for legitimate code-switching at confusion points demonstrates the gate has learned a nuanced distinction rather than blanket suppression. This addresses a key limitation of simpler rule-based approaches.

- **Informative ORPO comparison (Figure 3).** ORPO degrades general capability (INCLUDE accuracy drops from 61.4 to 57.3 for Qwen3-8B), while LCG maintains or slightly improves it. This practical finding is genuinely useful for practitioners choosing between approaches, and the comparison is fair — any asymmetry favors the baseline.

## Weaknesses

### Fatal
None

### Major
1. **Evaluation metric is aligned with optimization target** — The confusion metric (Section 5.2: "the percentage of responses containing at least one character from an unintended language script") directly measures what the gate optimizes: script-level masking. While BLEU and accuracy scores confirm no degradation, there is no independent measure of whether reducing script confusion actually improves output quality or user experience. This creates a circularity: the paper demonstrates the gate masks what it's designed to mask, but does not close the loop on whether this masking helps downstream. A human evaluation or task-specific quality measure would strengthen the evidence.

2. **Code-switching is meaningfully suppressed despite positive framing** — Table 5 shows Qwen3-8B code-switch rate drops from 46.34% to 25.90%, which is 32% below the ground-truth answer rate (38.36%). The paper characterizes this as "not much lower than the ground-truth answer rate," which is misleading. While the 86.7% token-level preservation is encouraging, the response-level data shows LCG substantially reduces legitimate multilingual behavior. The comparison to Claude Sonnet 4 (23.29%) as a floor is offered but Claude's lower rate may itself represent a deficiency. This trade-off deserves more honest discussion.

### Minor
1. **Four-family granularity limits scope without quantification** — The gate cannot address intra-script confusion (e.g., Spanish vs. English, Chinese vs. Japanese). Section 6 acknowledges this limitation in one sentence, but the paper never quantifies what fraction of real-world confusion is cross-script vs. intra-script. Without this, the reader cannot calibrate the method's practical coverage, and the abstract's claim of reducing confusion "often by an order of magnitude" may overstate impact if substantial real-world confusion is intra-family.

2. **Theory-practice disconnect for CJ↔Latin confusion** — Section 3.2 explicitly states the norm explanation "can't explain language confusion between English and Chinese since they both have high norm," yet Table 3 shows LCG-adjusted consistently outperforms LCG-unadjusted on Latin confusion (e.g., Qwen3-8B: 6.2% → 2.0%). Why norm adjustment helps in cases the theory doesn't cover is left unexplained. This gap between the mechanistic narrative and empirical results weakens the coherence of the paper's story.

3. **Confusion point analysis verified on only one model** — The key motivating finding that "language consistent tokens appear within top-3 99.29% of the time" (Section 3.1) is established only for Qwen3-8B on FLORES-NO-LATIN. Since this observation justifies the entire logit-masking approach, verifying it across the other three evaluated model families would strengthen the foundation.

4. **Intervention rule thresholds unjustified** — Rule 2 (Section 4.3) uses two threshold pairs ((5, 0.999) and (20, 0.95)) without justification or sensitivity analysis. The "No Rule" ablation (Figure 3) shows these rules materially affect performance, making their selection an important unexplored hyperparameter.

5. **Gate intrinsic accuracy not reported** — The gate is a trained classifier, but its precision/recall per language family is never evaluated directly. Reporting this would help diagnose whether remaining confusion stems from gate errors or from the coarseness of the four-family taxonomy.

### Trivial
None

## Nice-to-Haves
- Variance reporting or confidence intervals across multiple runs, especially for small confusion rates (<1%) where noise could be substantial. HumanEval-XL uses 10 repeats per prompt (Section 5.2), but other experiments appear single-run. While single-run evaluation is common in the LLM benchmark setting, the specific confusion rates being compared are often small enough that run-to-run variance matters.
- Characterizing the distribution of real-world confusion types (cross-script vs. intra-script) to quantify LCG's practical coverage.
- Sensitivity analysis for intervention rule thresholds.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **ORPO comparison "potentially unfair"**: The reviewer noted ORPO modifies weights while LCG is decoding-time. However, any asymmetry favors the baseline (ORPO gets to modify the model), not LCG. This makes the comparison a stronger test for LCG, not a weaker one. Removed.

- **Avoiding the LCB benchmark**: The paper provides clear, reasonable rationale (Section 5.2) — LCB queries sometimes require natural code-switching and its language detector produces false positives. Using established benchmarks with targeted filtering is a defensible choice, even if it complicates cross-paper comparison.

- **"Order of magnitude" claim overstated**: The paper uses the qualifier "often." CJ reductions are frequently 10×+ (4.5% → 0.1%, 1.0% → 0.0%). Latin reductions are smaller (3–6×). The qualifier adequately hedges the claim.

- **Low-Res tokens never masked (Rule 1, Section 4.3)**: This means confusion *into* low-resource languages is unaddressed, but the paper explicitly explains the rationale: "It's very rare for high-resource language to mix low-resource languages." This is a deliberate scope decision, not an oversight.

- **No statistical significance reported**: Demoted to nice-to-have. Single-run evaluation is standard practice in LLM benchmarking. While the small confusion rates make variance a legitimate concern, demanding multi-run significance testing is a field-norm stretch for this type of evaluation.

## Novel Insights
The decomposition of logits into norm and cosine-similarity components, revealing that high-resource language tokens systematically dominate the high-norm group in the output embedding matrix, provides a mechanistic explanation for cross-script language confusion that is both novel and actionable. The key insight — that "language switching errors are not due to a complete absence of correct-language candidates in the model's output distribution, but rather to the model assigning insufficient probability mass to them" (Section 3.1), with correct-language tokens appearing in top-3 99.29% of the time — motivates a minimally-invasive masking intervention rather than expensive weight modification, and the norm-adjusted self-distillation training procedure elegantly converts this insight into a practical training signal.

## Suggestions
- **Quantify the distribution of real-world confusion types** (cross-script vs. intra-script) to give readers a concrete sense of LCG's practical coverage and transform the one-sentence limitation into a quantified scope statement.
- **Report gate precision/recall per language family** to separate gate accuracy from taxonomy limitations and enable targeted improvement.
- **Discuss why norm adjustment helps for CJ↔Latin confusion** when the theory predicts it shouldn't — this gap between mechanism and result is the paper's weakest narrative point.
- **Present code-switching impact more transparently** — the 25.90% vs. 38.36% gap deserves honest discussion alongside the 86.7% token-level figure, rather than being framed as negligible.
- **Verify the top-3 99.29% finding across other model families** to strengthen the claim's generality.

## Score and Decision

### Anchor Comparison Table

| Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| Humanoid Robots Chinese NLP | gwZ90hFSL2 | 1.00 | R1 | Not a real contribution; LCG is far stronger |
| Systematic Review of LLMs | 8QTpYC4smR | 1.00 | R1 | Survey paper, no method; incomparable |
| NEMESIS Jailbreaking | 5kMwiMnUip | 1.40 | R1 | Weak methodology; LCG far above |
| Time-dependent Development | P49gSPmrvN | 1.00 | R1 | Irrelevant topic; not comparable |
| Llamas Think in English | fSbPwHjdDG | 3.00 | R1 | Single-task, poor presentation, non-replicable findings; LCG clearly stronger |
| Synergistic Cross-lingual IR | zkNCWtw2fd | 3.00 | R1 | Limited novelty, uniform scores of 3; LCG stronger |
| Correlation Analysis MT | MyotJECv0D | 2.50 | R1 | Limited contribution; LCG far above |
| Latent Space Theory LLMs | 4y3GDTFv70 | 3.25 | R1 | Mixed reviews, theoretical gaps; LCG more practical |
| Babel Tower Multilingual Code | eznTVIM3bs | 5.25 | R1 | Similar scope issues; LCG more practical but less theoretical depth |
| Scaling Laws Multilingual | T2h2V7Rx7q | 5.25 | R1 | Broader theoretical contribution but rejected; comparable tier |
| Language Fusion FLARE | eLBKQSpsVd | 4.25 | R1 | Mixed reviews, limited impact; LCG stronger |
| Mexa Cross-lingual Alignment | hsMkpzr9Oy | 5.40 | R1 | Evaluation-focused, limited novelty; similar tier |
| Crosslingual Capabilities | BCyAlMoyx5 | 5.67 | R1 | Wrong model choices undermined contribution; LCG has better experimental design |
| TransLLM Non-English | US2UCMvzvP | 6.25 | R1 | Engineering-focused, limited novelty; comparable to LCG |
| Knowledge Cross-lingual | HMa8mIiBT8 | 6.00 | R1 | Analysis paper with limited mitigation; similar tier |
| Same but Different | NCrFA7dq8T | 6.60 | R1 | More thorough mechanistic analysis; LCG slightly below |
| DEPT Decoupled Embeddings | vf5aUZT0Fz | 8.00 | R1 | Major framework contribution; LCG clearly below |
| Interpolating AR Diffusion | tyEyYT267x | 8.00 | R1 | Fundamental method advance; LCG clearly below |
| Transfusion | SI2hI0frk6 | 7.60 | R1 | Major multi-modal contribution; LCG clearly below |
| Context-Parametric Inversion | SPS6HzVzyt | 8.00 | R1 | Novel finding with broad implications; LCG below |
| Nudging (Inference-time Alignment) | HgAS03GU4J | 6.00 | R2 | Very similar spirit — plug-in decoding intervention; comparable |
| SASA Self-Detoxification | jY5oml9fe9 | 6.00 | R2 | Closest analog — lightweight decoding with internal representations; LCG has stronger mechanistic motivation |
| Tool Decoding | 5bUy4F59mk | 6.00 | R2 | Similar plug-and-play approach; LCG has more novelty through norm analysis |
| OPAD Principle-Guided Decoding | cfn2O1qvxp | 6.00 | R2 | Inference-time alignment; comparable scope and contribution |
| Unified Representation Space | FrFQpAgnGE | 7.00 | R2 | Broader analysis contribution; LCG slightly below |
| Discrete Auto-regressive Biasing | Duuerhutvq | 5.75 | R2 | Controlled decoding; comparable but LCG has stronger practical validation |
| Byte-Level Probabilities | zGej22CBnS | 6.25 | R2 | Tokenization bias analysis; comparable tier |
| LM Arithmetic | SLw9fp4yI6 | 7.00 | R2 | More general framework with broader applicability; LCG slightly below |

**Round 1 bracket:** 5.5–7.0
**Round 2 narrowing:** 6.0–6.5

The paper sits squarely in the 6.0 cluster of lightweight decoding-time interventions (SASA, Tool Decoding, Nudging, OPAD). It has a slightly stronger mechanistic contribution than most of these (the norm bias analysis) and broader experimental validation (4 model families), but its evaluation circularity (metric aligned with optimization target) and the code-switching suppression concern are genuine major weaknesses that prevent it from reaching the 6.5+ tier. The scope limitation to cross-script confusion is clearly acknowledged and reasonable but bounds the contribution.

**Final score: 6.0** — The paper makes a useful, well-motivated applied contribution with a genuine mechanistic insight. The method is practical, lightweight, and consistently effective across architectures. The major weaknesses (evaluation circularity, understated code-switching impact) are addressable but currently limit confidence. This is a borderline accept: the contribution is real and deployable, but the evaluation doesn't fully demonstrate that the intervention improves user-facing quality beyond the script-presence metric it directly optimizes.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>