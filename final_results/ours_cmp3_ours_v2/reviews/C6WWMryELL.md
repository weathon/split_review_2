## Summary

This paper studies output length volatility in long-form LLM generation — the fact that the same prompt can produce wildly different output lengths across multiple generations. It makes three contributions: (1) **VOLTBench**, a multi-dimensional benchmark covering unstructured and structured tasks across languages, instruction complexities, and length scales up to 100k words, with volatility as a core metric; (2) an **attention trace analysis** identifying "Attention Collapse" and "Attention Instability" as internal patterns correlated with output failures; and (3) **SELB** (Structural Enforcement via Logits Boosting), a training-free decoding strategy that enforces section structure and suppresses failure-prone tokens.

## Strengths

1. **VOLTBench is a well-designed, multi-dimensional benchmark for a genuinely underexplored problem.** Output volatility in long-form generation — unpredictable token consumption, unreliable length adherence — is a practically relevant issue that prior benchmarks largely ignore by evaluating single generations in isolation. The benchmark systematically varies language (EN/ZH), instruction complexity (simple/complex/fine-grained), output format (unstructured/structured), and length scale (up to 100k tokens via chapter scaling). The inclusion of both objective quality metrics (execution-based verification for structured tasks) and fine-grained constraint-following evaluation — combined with multiple-sampling volatility measurement — is a clear step beyond prior benchmarks (as shown in Table 1's comparison).

2. **Attention trace analysis provides a plausible mechanistic story.** The identification of "Attention Collapse" (attention to constraints dropping to near-zero, followed by task abandonment) and "Attention Instability" (abnormally large attention spike preceding erratic output) is intuitive and visually supported by the traces in Figure 4. Connecting generation failures to measurable internal attention dynamics moves beyond purely behavioral observation and is a worthwhile direction for the field.

3. **SELB is lightweight and training-free.** Operating at decoding time with no additional training or model modifications is a practical virtue for adoption. The method is clearly described (Equations 1–3) and easy to understand.

4. **The fine-grained constraint collapse finding is robust and insightful.** The observation that constraint adherence collapses after 100 sections, with no model delivering more than 40 correct constrained sections at 500 (Section 4.3.1), is a clean, quantitative demonstration of a real limitation in current models.

## Weaknesses

### Fatal
None.

### Major

1. **The headline claims (148%, 69%) are framed against LongWriter-8B, not the actual base model, creating a misleading narrative.** The abstract, contributions list, and conclusion repeatedly state that SELB "improves the mean output length of the base model by 148% and reduces the length volatility by 69%." However, the results section (6.3) reveals that the 148% figure compares SELB+Qwen2.5-7B (15,651 words) against *LongWriter-8B* (6,320 words) — not against Qwen2.5-7B (445 words, which would be a 3,418% increase). Similarly, the 69% volatility reduction compares SELB's LVC of 14.02% against LongWriter-8B's 45.4% — the actual base model Qwen2.5-7B has LVC 17.0%, making the genuine reduction ~18%. Comparing against LongWriter-8B is a legitimate secondary reference (it shows a training-free method on a 7B model beating a specialized fine-tuned 8B model), but the abstract should not call LongWriter-8B the "base model." This framing needs to be corrected throughout the paper.

2. **SELB is not compared against equivalently-informed decoding baselines on the same base model in the main results section.** Section 6.3 compares SELB+Qwen2.5-7B only against LongWriter-8B (a different model). The training-free decoding baselines (Repetition Penalty, Entropy-Based Stopping, Length Constraint, Lookahead Decoding) are introduced in Table 2 but never revisited in the SELB evaluation. This omission is significant: Lookahead Decoding applied to the *same* base model (Qwen2.5-7B) achieves LVC of 9.3% on the same 100-section task — lower than SELB's 14.02%. While Lookahead produces much shorter output (2,883 vs 15,651 words, making a direct LVC comparison nuanced because volatility tends to be lower for shorter outputs), the paper should still acknowledge and discuss this. The lack of a direct comparison table weakens the claim that SELB is the best training-free method for reducing volatility.

3. **No ablation studies for SELB's two components.** SELB combines structural enforcement (M_struct: section-title boosting, EOS suppression) and failure prevention (M_fail: filler-phrase banning). Without ablations, it is impossible to tell whether the structural enforcement alone — which directly forces section completion — accounts for most of the benefit, or whether the failure-prevention component adds meaningful independent value. A simple ablation (SELB without M_fail, SELB without M_struct) would resolve this.

### Minor

4. **N=5 generations per instruction is low for volatility estimation, and no confidence intervals are reported.** The paper's core metrics (LSD, LVC) are variance estimates. With only 5 samples per condition, the confidence intervals around these estimates will be wide. No bootstrap estimates, confidence intervals, or significance tests are reported, making it hard to assess whether reported differences (e.g., LVC 1.9% for Claude vs 33.9% for GPT-4o-mini) are reliable.

5. **Claude-3.5-Sonnet's exclusion from quality evaluation is insufficiently justified.** Claude generated 176 words (~1.76 words/section) on a 100-section task — essentially a task failure. The paper excludes it from quality comparisons "due to its low mean length" without investigating whether this was a prompt misunderstanding, refusal, or genuine inability. Excluding a capable model without explanation could bias the comparative conclusions.

6. **The attention trace evidence is based on a narrow sample (2 models, 1 task) and is correlational.** The analysis uses Qwen2.5-7B and Qwen2.5-3B on a single diary-generation task with 40 sections. The paper appropriately uses correlational language ("closely linked," "preceded by"), but broadening the analysis across more models and tasks would substantially strengthen the mechanistic claims.

### Trivial
None.

## Nice-to-Haves
- Add a comparison table showing SELB against the decoding baselines (Repetition Penalty, Lookahead, etc.) on the same base model.
- Include bootstrap confidence intervals for LSD/LVC metrics.
- Provide a qualitative example of SELB's output to demonstrate content quality beyond structural metrics (SCA).

## Removed Points
- **"SELB's evaluation confounds the method with benchmark-specific structural priors"** — Removed because SELB is explicitly designed to use structural information (section count, section titles); this is the method's design, not a confound. The paper's claim is that a decoding-time method leveraging structural priors reduces volatility, which is a legitimate claim. The useful part of this critique — that baselines should be given equivalent structural information — is already covered by Major Weakness #2 (missing comparison against informed baselines) and #3 (missing ablation).
- **"No comparison against training-based methods"** — Removed because the paper explicitly scopes itself as training-free; demanding training-based comparisons is scope creep.
- **"Free-form generation results are too briefly described"** — The parser strips appendices; the paper references Appendix I for details.
- **"Attention trace supports correlation, not causation"** — The paper uses correlational language appropriately ("closely linked"), not causal claims. Downgraded to Minor Weakness #6.
- **Generic formatting, citation, and reproducibility nitpicks** — Removed per hard rules.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Reframe the headline percentages.** State explicitly in the abstract that the 148%/69% figures compare SELB+Qwen2.5-7B against LongWriter-8B (a specialized long-generation model), not against the base model. Report the honest comparison against Qwen2.5-7B (3,418% length increase, ~18% LVC reduction) alongside this.
2. **Add a direct comparison against decoding baselines.** In Section 6.3, include a table showing SELB against Repetition Penalty, Lookahead Decoding, etc., all applied to the same base model (Qwen2.5-7B) on the same 100-section task.
3. **Add ablation experiments:** SELB without M_fail, SELB without M_struct, and sensitivity analysis on β and τ_max.
4. **Increase N** to at least 10 per condition, or report bootstrap confidence intervals for LSD/LVC.
5. **Clarify why Claude-3.5-Sonnet failed** and discuss whether exclusion affects the comparative conclusions.

---

## Calibration

**Anchors used (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| LongWriter (kQ5s9Yh0WI) | 6.00 | R1/Bracket | Same topic (long-form generation). LongWriter has a cleaner method evaluation with ablations and thorough baselines, but less comprehensive benchmarking. This paper has a stronger benchmark but weaker method evaluation. |
| Beyond In-Context Learning (Dj9wssUmLn) | 5.80 | R2 | Long-form generation enhancement. This paper has more thorough ablations but less comprehensive benchmarking. Comparable level of contributions. |
| PolyPythias (bmrYu2Ekdz) | 6.50 | R1 | Training stability analysis. Higher score due to releasing valuable data and thorough analysis. |
| Length Representations (dNBE4ciYJF) | 4.00 | R2 | Length control in LLMs. Shares presentation/evaluation weaknesses but this paper has stronger benchmarking. |
| MAP's not dead yet (vXf8KYTJmm) | 5.25 | R2 | Decoding degeneracy analysis. Similar level — neat idea with some methodological gaps. |
| Unlocking Anticipatory Text Generation (774elYc5tw) | 4.25 | R2 | Constrained decoding. Weaker contributions than this paper. |
| GOOD: Decoding-Time Alignment (cayKVPCrOP) | 4.50 | R2 | Training-free decoding method. Similar evaluation concerns. |

**Round 1 bracket:** 4.0 – 6.0. The paper's benchmark contribution is strong (near 6.0 territory, similar to LongWriter), but the method evaluation issues (misleading framing, no ablations, missing baselines against decoding strategies on the same base model) pull it down toward the 4.0–5.5 range.

**Round 2 narrowing:** Comparing against LongWriter (6.00) — that paper has cleaner method evaluation (ablations, proper baselines), suggesting this paper's method evaluation is weaker. Comparing against Beyond In-Context Learning (5.80, *Reject*) — that paper has thorough ablations but weaker benchmarks. This paper has a stronger benchmark but weaker method evaluation. The two roughly balance, placing this paper in the 5.0–5.5 range.

**Final score:** 5.0. The VOLTBench benchmark and attention analysis are genuine contributions. However, the misleading framing of SELB's headline results, the missing comparison against decoding baselines on the same base model, and the absence of ablation studies prevent the paper from being a clear accept. These issues are fixable, but in the current form the evaluation does not support the strength of the claims made about SELB.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>