Now I have a clear calibration picture. Let me write the final review.

**Round 1 bracket: Between 6.0 and 7.0.** The paper is clearly above the reject range (1-5.5 papers have fundamental issues LCG doesn't have) and below the strong accept range (8.0 papers like Knowledge Card and FlexPrefill have broader impact). Among comparable inference-time intervention papers: nudging (6.0, Reject), Tool Decoding (6.0, Accept), SADI (6.4, Accept), instruction-following steering (7.0, Accept). LCG sits in this band with its strong mechanistic analysis and code-switch overclaiming as the main differentiator.

**Round 2 narrowing:** After comparing with SASA self-detoxification (6.0, Accept), CoS context steering (6.67, Accept), context sensitivity knob (6.75, Accept), and editing overfitting (7.33, Accept), the paper sits between 6.0 and 7.0. Its mechanistic norm analysis and multi-model evaluation are stronger than most 6.0 papers, but the code-switch overclaiming keeps it below the 7.0 papers.

**Final score: 6.5.**

---

## Summary
This paper introduces the Language Confusion Gate (LCG), a lightweight plug-in two-layer MLP that reduces unintended language mixing in LLMs during decoding. Trained via norm-adjusted self-distillation on a frozen model's predictions, the gate learns to predict permissible language families at each generation step and masks logits of disallowed tokens. The method is evaluated across five models (Qwen3, Llama3.1, Gemma3, GPT-OSS) in both thinking and no-thinking modes, demonstrating substantial reductions in language confusion with negligible latency overhead.

## Strengths
- **Novel mechanistic insight grounded in quantitative analysis:** Section 3.2 decomposes logits as `||h|| · ||e_i|| · cos_sim(h, e_i)` and Table 1 shows concrete norm imbalance data across 5 models — CJ tokens dominate the top-5% norm group (e.g., 10.74% for Qwen3-8B) while Low-Res tokens are underrepresented (0.14%). Figure 2 demonstrates how norm-adjustment reshuffles the top-10 from entirely CJ tokens to correct-language tokens at a Hebrew confusion point. This analysis is genuinely novel and well-evidenced.
- **Norm-adjustment ablation directly validates the core contribution:** Table 3 shows LCG-adjusted consistently outperforms LCG-unadjusted across all four no-think models — e.g., Llama3.1-8B Latin confusion drops from 5.7% to 2.9%. This isolates norm adjustment as an active ingredient rather than just self-distillation.
- **Strong baseline comparisons demonstrating clear advantage:** Figure 3 shows ICL and greedy decoding provide only marginal improvement (CJ% from 4.5% to 4.2% for Qwen3-8B), while ORPO degrades INCLUDE accuracy (Qwen3-8B: 61.4→57.3, Llama3.1-8B: 46.1→43.2), demonstrating the advantage of a plug-in approach over training-based methods.
- **Comprehensive multi-model, multi-mode evaluation:** Five models across both thinking and no-thinking modes on FLORES+, INCLUDE, and Humaneval-XL benchmarks, substantially broader than typical prior work in this area.
- **Highly practical with negligible overhead:** 0.38% intervention rate (523/139,354 tokens) and only 0.4% latency increase (15.95ms → 15.99ms), plus compatibility with speculative decoding (Appendix F).

## Weaknesses

### Fatal
None

### Major
- **Over-claiming on code-switch preservation:** The paper's central claim is that LCG "preserves valid multilingual behaviors," but Table 5 shows that post-intervention code-switch rates on FLORES-WITH-LATIN fall *below* the ground-truth answer rate (38.36%) for all three models: Qwen3-8B drops to 25.90% (32% relative decrease), Llama3.1-8B to 31.60% (18% decrease), and Gemma3-12B to 25.57% (33% decrease). The paper characterizes Qwen3-8B's 25.90% as "not much lower than the ground-truth answer rate (38.36%)" — this framing is misleading given the magnitude of the gap. Meanwhile, the token-level metric (86.7% of human-validated confusion points allow English tokens) is presented alongside but never reconciled with the response-level metric. A per-response analysis (how many responses have all code-switch tokens allowed vs. at least one suppressed) would clarify whether the method systematically over-suppresses legitimate code-switching or only affects a minority of responses. This directly undermines a core claim of the paper.

### Minor
- **Gate vs. rule contribution insufficiently decomposed:** The intervention combines the learned LCG gate with three hand-crafted rules (Section 4.3): never mask Symbols/Low-Res, override gate when contradicted by high-confidence output, persist previous language family. The "No Rule" ablation in Figure 3 shows the combined effect, but individual rule ablations would clarify how much confusion reduction comes from the learned gate versus each heuristic. This matters for understanding the relative importance of the paper's learned contribution.
- **Abstract overclaims on reduction magnitude:** The abstract states LCG reduces confusion "often by an order of magnitude." While this holds for CJ confusion (e.g., Qwen3-30B: 1.0%→0.0%), it is less accurate for Latin confusion on some models (Llama3.1-8B: 8.4%→2.9%, ~3× reduction). The hedge "often" partially mitigates this but could be more precise.

### Trivial
- **Table 4 caption error:** The caption reads "Effectiveness of LCG Intervention on 'No-Think' Models measured on Humaneval-XL" but the surrounding text discusses "Experiments on Thinking Model Intervention" and the table includes "Length" (reasoning token length), a metric specific to thinking models. This is a copy-paste labeling error.

## Nice-to-Haves
- Reporting bootstrap confidence intervals for metrics with small differences (BLEU changes of 0.1-0.2) would strengthen "no degradation" claims.
- Analyzing what causes residual Latin confusion after intervention (e.g., Qwen3-8B still has 2.0% Latin confusion) — are these gate failures or rule override failures?
- Ablating training data diversity to understand if the 78K samples / 200+ languages are necessary.

## Removed Points
These points are flagged to be removed, treat them with caution.
- Harsh critic's claim about "no variance or confidence intervals reported" — moved to Nice-to-Haves as it's a reasonable but non-standard expectation for this type of benchmark evaluation.
- Any formatting nitpicks or parser artifacts — removed per hard rules.

## Novel Insights
The paper's most genuinely novel insight is the mechanistic observation that output token embedding norm imbalances systematically bias LLM sampling toward high-resource language tokens (Section 3.2, Table 1). While the logit decomposition `||h|| · ||e_i|| · cos_sim(h, e_i)` is standard linear algebra, its application to diagnose and address language confusion is original. The practical consequence — dividing logits by embedding norms during pseudo-label generation produces better training signal — is a clean and well-validated technical contribution (Table 3 ablation). Additionally, the observation that confusion tokens are top-1 56.74% of the time while correct-language tokens appear within top-3 99.29% of the time (Section 3.1) provides an elegant justification for logit-masking as an intervention strategy.

## Suggestions
- Add individual rule ablations to decompose gate vs. rule contributions in Figure 3.
- Reconcile the token-level (86.7%) vs. response-level (below ground-truth) code-switch metrics with a per-response breakdown.
- Fix Table 4 caption from "No-Think" to "Thinking."
- Calibrate the "order of magnitude" claim in the abstract, distinguishing CJ vs. Latin confusion reductions.

## Calibration Report

### Anchors Retrieved

**Round 1 (bracketing):**
- *gwZ90hFSL2* (Advancing Cross-Lingual Capabilities for Humanoid Robots), avg 1.0, Round 1 — irrelevant/weaker paper, LCG is clearly stronger.
- *8QTpYC4smR* (Systematic Review of LLMs), avg 1.0, Round 1 — survey paper with no technical contribution, LCG far stronger.
- *fSbPwHjdDG* (Llamas think in English), avg 3.0, Round 1 — interesting causal analysis but limited scope and weaker evaluation, LCG clearly above.
- *eznTVIM3bs* (Rise and Down of Babel Tower), avg 5.25, Round 1 — hypothesis-driven analysis paper, LCG has more concrete practical contribution.
- *HgAS03GU4J* (Inference-time Alignment/Nudging), avg 6.0, Reject, Round 1 — similar plug-and-play approach but less practical problem and weaker evaluation than LCG.
- *5bUy4F59mk* (Tool Decoding), avg 6.0, Accept, Round 1 — comparable plug-and-play approach, LCG has stronger mechanistic motivation and training methodology.
- *8WQ7VTfPTl* (SADI), avg 6.4, Accept, Round 1 — comparable inference-time intervention, LCG has cleaner method and broader evaluation.
- *WbWtOYIzIK* (Knowledge Card), avg 8.0, Accept, Round 1 — more broadly impactful modular framework, LCG is more narrowly focused.
- *xoXn62FzD0* (SMC for LLM control), avg 8.0, Accept, Round 1 — more principled statistical framework, LCG is more application-specific.

**Round 2 (narrowing):**
- *NCrFA7dq8T* (The Same but Different), avg 6.6, Accept, Round 2 — mechanistic interpretability paper, comparable depth of analysis to LCG.
- *jY5oml9fe9* (Self-Detoxification/SASA), avg 6.0, Accept, Round 2 — similar lightweight controlled decoding approach, LCG has broader evaluation and more practical impact.
- *xQCXInDq0m* (CoS Context Steering), avg 6.67, Accept, Round 2 — inference-time control, comparable quality.
- *wozhdnRCtw* (Instruction-Following Steering), avg 7.0, Accept, Round 2 — activation steering for instruction following, LCG is comparable but the code-switch weakness holds it slightly below.
- *Igm9bbkzHC* (Context Sensitivity Knob), avg 6.75, Accept, Round 2 — finding internal control mechanisms, comparable novelty.
- *t8qcGXaepr* (Editing Overfitting), avg 7.33, Accept, Round 2 — identifying and addressing a specific failure mode, LCG is slightly less novel.

### Bracket Progression
- **Round 1 bracket:** 6.0–7.0. LCG clearly outperforms sub-5.5 papers and is comparable to the 6.0–7.0 range of inference-time intervention papers.
- **Round 2 narrowing:** 6.0–7.0 confirmed. LCG is stronger than 6.0 papers (nudging, SASA) due to better evaluation and mechanistic grounding, but the code-switch overclaiming keeps it below 7.0 (instruction-following steering).
- **Final score: 6.5.** The paper is a solid accept: well-motivated, technically sound, comprehensively evaluated, with practical deployment value. The code-switch overclaiming is the main weakness preventing a higher score.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>