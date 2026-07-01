Now I have all the information I need. Let me compile the final review.

## Summary

This paper addresses output volatility in long-form LLM generation — the inconsistency in length and content across multiple generations of the same prompt. It offers three contributions: (1) VOLTBench, a multi-dimensional benchmark covering structured and unstructured tasks across languages and complexity levels, designed to quantify length volatility; (2) an attention trace analysis identifying "Attention Collapse" and "Attention Instability" as internal patterns correlated with volatile outputs; and (3) SELB (Structural Enforcement via Logits Boosting), a training-free decoding strategy that enforces structural constraints (section transitions, EOS suppression) to improve length adherence and stability.

## Strengths

- **VOLTBench fills a genuine gap in the evaluation landscape.** Existing long-form benchmarks (HelloBench, LIFEBench, LongGenBench) focus on single-generation quality and overlook output volatility — the inconsistency across multiple generations of the same prompt. The paper makes a clear case for why this matters (Section 1, lines 13–17). VOLTBench's multi-dimensional design (multiple task types, languages, complexity levels, structured *and* unstructured outputs, stability evaluation) is more comprehensive than any single prior benchmark, as documented in Table 1.

- **The chapter-based scalability mechanism is well-designed.** Scaling from 5 to 500 chapters provides a systematic way to stress-test models across output length scales up to ~100k words. The empirical finding that "when tasked with generating up to 50 sections, models failed in approximately half of the cases" and "for requests exceeding 50 sections, all models failed to complete the task as instructed" (line 161) is a striking and genuinely informative observation.

- **The attention trace methodology provides an interpretable diagnostic lens.** Probing constraint-attention scores over the course of generation (Section 5) and plotting $\bar{\alpha}^{(t)}$ gives a principled way to visualize *when* models lose track of instructions. The contrast between Attention Collapse (Qwen2.5-3B) and Attention Instability (Qwen2.5-7B) is a conceptually useful diagnostic distinction.

## Weaknesses

### Fatal
None.

### Major

- **The headline performance numbers in the abstract and contributions are framed in a misleading way.** The abstract (line 9) and contribution list (line 28) state that SELB "improves the mean output length of the base model by 148% and reduces the length volatility by 69%." Section 6.3 reveals that the 148% is SELB's 15,651 words vs. LongWriter-8B's 6,320 words, and the 69% reduction is SELB's LVC (14.02%) vs. LongWriter-8B's LVC (45.4%). SELB is applied to Qwen2.5-7B, whose base performance (Table 2: 445 words, LVC 17.0%) is very different from LongWriter-8B's (6,320 words, LVC 45.4%). A reader naturally interprets "base model" as the model SELB is applied to, which would yield a ~3,418% length increase and ~17.5% LVC reduction — very different from the advertised numbers. Comparing against LongWriter-8B without making this explicit is a significant framing distortion.

- **SELB is a set of hard constraints whose results are largely guaranteed by design, yet evaluated against baselines lacking similar structural enforcement.** SELB (Section 6.1–6.2) forces section transitions by applying a "large positive constant" $\beta$ to section-title logits (Eq. 2), suppresses EOS tokens until all sections are generated (Eq. 3), and bans conversational fillers. Any method that prevents EOS and forces transitions at pre-specified lengths will mechanically produce outputs of approximately the right length. The paper's baselines (Repetition Penalty, Entropy-Based Stopping, Length Constraint, Lookahead Decoding) do not use this class of structural constraints, making the comparison asymmetric. A proper evaluation requires comparing against other constrained-decoding approaches (e.g., grammar-constrained decoding, structured output schemas) or at minimum ablating whether the advantage comes from SELB's specific design versus the mere act of applying any structural constraint.

- **The claimed connection between the attention trace probing and SELB is narrative rather than substantive.** The paper states SELB "targets the identified internal patterns" (line 28) and was designed based on probing insights (line 24). But SELB does not interact with the attention mechanism — it targets behavioral symptoms (premature termination, section skipping) through hardcoded rules, not the identified attention-level patterns. There is no demonstration that SELB restores attention to constraint tokens, prevents attention collapse, or smooths attention instability. The probing and mitigation sections are essentially independent contributions linked only by framing. This weakens the paper's claim of a unified "benchmark → probe → mitigate" arc.

### Minor

- **The attention trace analysis is too limited in scope to support the claimed generality.** Section 5 presents attention traces for exactly two models (Qwen2.5-7B and Qwen2.5-3B) on a single task (diary generation with 40 required sections) — each shown in one figure (Figure 4). The paper claims to identify "several common internal patterns" (line 24) and that "output volatility is not random but closely linked to... failures in the model's internal attention dynamics" (line 188). From two models on one task, the generality of these patterns is unsubstantiated. Cross-model validation (e.g., Llama, Deepseek) and cross-task validation are needed.

- **VOLTBench uses N=5 generations per instruction for volatility estimation.** As the paper acknowledges (Section 3.2), the LSD metric is computed over N=5 samples. With only 5 samples, the standard deviation estimate has high variance (standard error ≈ σ/2.8). For a benchmark whose core purpose is measuring volatility, this limits the reliability of model-level rankings.

- **Claude-3.5-Sonnet is excluded from quality evaluation** "due to its low mean length (176 words), insufficient for long-text evaluation" (line 157). Yet Claude achieves the lowest LSD (3.30) and LVC (1.9%) in Table 2, making it the most stable model. Excluding it from the quality discussion selectively removes the model that most challenges the "all models exhibit severe volatility" narrative.

- **The 100k-word scale claim is not demonstrated in the main paper.** The paper states VOLTBench supports up to ~100k words but presents experimental results only up to 100-section tasks (Table 2) with outputs in the hundreds-to-low-thousands range. No results at the claimed 100k scale appear in the main paper.

### Trivial
None.

## Nice-to-Haves

- The SELB-Hybrid free-form generation results (97% MLA on 20k-word novels, Section 6.4) are potentially the paper's most impressive finding and should be in the main paper rather than Appendix I.
- An ablation study separating the contribution of each SELB component (structural enforcement, EOS suppression, filler suppression) would help identify which design choices drive the improvements.
- Increasing N from 5 to 20–30 for volatility estimates would improve reliability of the benchmark.

## Removed Points

These points were identified in the input review but are removed with justification:

- **"SELB comparison is fundamentally unfair"** — Reframed rather than removed. The concern about asymmetric baselines is kept as a Major weakness, but the original phrasing overstated the issue. The paper does include a Length Constraint baseline (a form of constrained decoding), so "fundamentally unfair" is too strong; however, the comparison lacks baselines with the same *class* of structural constraints.
- **"Attention analysis is correlational not causal"** — Moved to Minor. The paper's wording ("closely linked to and preceded by") appropriately limits itself to correlation. The criticism is better scoped as insufficient evidence for generality.
- **Generic/superficial strengths from input** (e.g., "problem identification is well-motivated") — Kept but only in concrete, evidence-grounded form.
- **"Missing constrained decoding baselines"** — Incorporated into the second Major weakness.
- **"Strengthening the Paper on Its Own Terms" suggestions** — Incorporated into Nice-to-Haves and Suggestions.
- **"Missing related works"** — Removed per policy (cannot confirm existence of missing works from external knowledge).

## Novel Insights

None beyond the paper's own contributions. The most insightful external observation from the review is the structural disconnect between the attention probe analysis and the SELB mitigation design — the paper presents them as a unified narrative but the method does not mechanistically address the identified attention patterns. This observation could help the authors restructure the paper's framing.

## Suggestions

1. **Fix the headline numbers.** Make the comparison basis explicit in the abstract (e.g., "improves mean output length by 148% over LongWriter-8B"). Better yet, report improvement relative to the actual base model (Qwen2.5-7B) as the primary comparison.
2. **Restructure the SELB evaluation.** Either (a) add baselines with comparable structural constraints (e.g., grammar-constrained decoding, structured output parsers) and show SELB's advantage is not merely from having *any* constraint, or (b) reframe SELB transparently as a rule-based constrained decoding strategy and acknowledge that its advantage over unconstrained baselines is expected by design.
3. **Address the probe-to-mitigation disconnect.** Either demonstrate a mechanistic link (e.g., that SELB stabilizes attention to constraint tokens) or drop the narrative that SELB was derived from the probing analysis. Presenting the two as independent contributions would be more honest.
4. **Expand the attention trace analysis** to more models and tasks to substantiate the claim of "common internal patterns."
5. **Bring the SELB-Hybrid free-form results** into the main paper, as they are the strongest evidence for SELB's usefulness.

## Score and Decision

**Calibration anchors (retrieved from human review corpus):**

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| HelloBench (QM2WoPu1It) | 4.75 | R1 | Long-form generation benchmark paper; rejected due to limited novelty. The paper under review has a more specific angle (volatility) but similar scope. |
| Quantifying Variance (E2RyjrBMVZ) | 4.17 | R1, R2 | Evaluation variance focused; rejected for unclear value proposition. Less applied than the paper under review. |
| LongSafetyBench (dQzpP9ziaJ) | 3.50 | R2 | Safety benchmark for long-context; lower quality benchmark submission. |
| CASD (g3D27bfmrf) | 3.00 | R1 | Decoding strategy paper; rejected for insufficient novelty vs. prior work. SELB is simpler than CASD but the paper under review has a stronger benchmark component. |
| Inferring from Logits (t15cWqydys) | 3.00 | R1 | Decoding/logit paper; rejected for poor results. The paper under review has better empirical results. |
| LLMs Know More Than They Show (KRnsX5Em3W) | 6.50 | R1 | Internal representation analysis; accepted with rigorous cross-model experiments. The paper under review's attention analysis is less rigorous. |
| Syntactic/Semantic Control via SMC (xoXn62FzD0) | 8.00 | R1 | Principled constrained decoding with strong theory; much stronger than SELB. |

**Initial bracket (Round 1):** 3.0–5.5. The paper is substantially better than score-3 papers (which have fundamental flaws or trivial contributions), but the SELB evaluation issues prevent it from reaching the 5.5+ band where papers with rigorous analysis and sound evaluation sit.

**Narrowing (Round 2):** 3.5–5.0. Compared to HelloBench (4.75, rejected), the paper under review has a more specific contribution (volatility vs. general long-form evaluation) and additional analysis. However, the misleading framing of headline numbers and the weak link between probing and mitigation are significant problems that HelloBench did not have. Compared to Quantifying Variance (4.17), the paper has a more concrete applied contribution.

**Final score: 4.0.** This paper has a genuine contribution in VOLTBench and an interesting but preliminary attention analysis. However, the SELB mitigation method is straightforward (hard constraints that mechanically guarantee the measured outcomes), its evaluation is compared against inappropriate baselines, and the headline numbers in the abstract are framed in a misleading way (comparing against LongWriter-8B while saying "base model"). These issues are significant enough that the paper cannot be accepted in its current form. With substantial revision — particularly honest reframing of SELB, proper baselines, and fixing the misleading comparisons — the VOLTBench and attention analysis components could form the basis of a stronger submission.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>