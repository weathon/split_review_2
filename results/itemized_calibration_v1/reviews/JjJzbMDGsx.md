## Summary

This paper identifies a mechanistic cause of language confusion in LLMs—token embedding norm imbalance favoring high-resource languages—and proposes the Language Confusion Gate (LCG), a lightweight two-layer MLP that intervenes at decoding time to mask tokens from unintended language families. LCG is trained via norm-adjusted self-distillation from the frozen model's own top-k/p predictions and only activates when confusion is detected (~0.35% of tokens), adding 0.4% latency overhead. Evaluated on Qwen3, Llama3.1, Gemma3, and GPT-OSS across both standard and thinking variants, LCG reduces cross-script confusion (CJ and Latin characters in non-CJ/Latin text) by an order of magnitude while preserving code-switching ability and task performance.

## Strengths

1. **Norm imbalance as a mechanistic insight (Section 3.2, Table 1, Figure 2).** The decomposition of logits into norm × cosine similarity is elementary but its connection to language confusion has not been articulated before. Table 1 shows cross-model evidence that high-resource tokens dominate top embedding norms (e.g., CJ has 10.74% of top-norm tokens in Qwen3-8B vs. 0.14% for Low-Res). Figure 2 provides a concrete example where norm-adjustment causes CJ tokens to drop out of the top-10 at a confusion point. This is the paper's most distinctive contribution.

2. **Practical, sparse-intervention design (Section 4).** LCG intervenes only ~0.35% of the time with 0.4% latency overhead, and the architecture follows directly from the paper's observations (confusion is rare → sparse intervention; correct tokens are in top-k → gate has a feasible prediction task). This is a method designed for real deployment, not just a proof-of-concept.

3. **Code-switch preservation analysis (Section 5.3, Table 5).** The paper goes beyond minimizing confusion to measure impact on legitimate code-switching: 86.7% preservation of human-validated code-switch points, and FLORES-WITH-LATIN analysis showing post-LCG rates remain near the ground-truth answer rate. This practical consideration is rare in the "confusion mitigation" literature and increases confidence in real-world applicability.

4. **Broad model coverage.** Evaluation spans Qwen3 (8B and 30B), Llama3.1-8B, Gemma3-12B, and GPT-OSS-20B, across both standard and thinking variants, on multiple benchmarks (FLORES, INCLUDE, Humaneval-XL). This lends reasonable generality to the results.

## Weaknesses

### Major

- **Headline claims overstate the scope of what the method addresses.** LCG classifies tokens into four script-level families (CJ, Latin, Symbols, Low-Res). It can only detect and correct *cross-script* confusion—where a token from one script family appears in text whose ground-truth language belongs to a different script family. Confusion *within* a script family (Spanish vs. English, Hindi vs. Marathi, Arabic vs. Farsi) is invisible. The abstract claims LCG "decreases language confusion significantly, often by an order of magnitude" without qualifying this to cross-script confusion. The conclusion does acknowledge this limitation, but the abstract and introduction frame the contribution more broadly. The paper would be stronger if it scoped its claims to match the method's actual coverage.

- **Missing ablation: rules-only without the learned gate.** The "No Rule" condition in Figure 3 removes all intervention rules at once, showing that LCG alone (without rules) still reduces confusion. But the reverse condition—the heuristic rules (Rules 2 and 3) applied *without* the learned gate—is absent. Rules 2 (refrain if high-confidence model output contradicts the gate) and Rule 3 (persistence of previous token's language) are strong heuristics that could plausibly account for a significant portion of the improvement. Without this control, the paper cannot demonstrate how much value the learned MLP adds beyond sensible heuristics. The "No Rule" condition provides a partial answer (LCG alone works), but the rules-only condition is the other half of the puzzle.

### Minor

- **No variance or statistical significance reported.** Confusion rates, BLEU scores, and accuracies throughout Tables 2–5 and Figure 3 are point estimates with no confidence intervals or standard deviations. For the thinking-model evaluation, prompts are repeated 10 times, but no variance is reported across runs. When differences are small (e.g., CJ% of 0.11 vs. 0.07 on INCLUDE), the reader cannot assess reliability.

- **ORPO baseline is underspecified.** The paper states ORPO was applied by "prepar[ing] a multilingual dataset, and synthesiz[ing] samples with language confusion as rejected samples similar as Lee et al. (2025)." No details on dataset size, composition, training hyperparameters, or checkpoint selection are provided. ORPO shows a substantial accuracy drop on INCLUDE (61.4→57.3 on Qwen3-8B), which is atypical for preference optimization. Without knowing whether the method was properly tuned or the training data was appropriate for this task, the comparison is hard to evaluate.

- **Pseudo-target quality is not directly validated.** The gate is trained via self-distillation from norm-adjusted top-k/p predictions. The paper does not report precision/recall of these pseudo-targets against an oracle (e.g., ground-truth language family). While the downstream results suggest the signal is adequate, direct validation would strengthen the self-distillation claim and address the circularity concern about training on potentially unreliable model outputs.

- **Thinking-model evaluation is narrow.** Reasoning-capable models are evaluated only on Humaneval-XL (code generation), which is inherently Latin-heavy and has low baseline confusion rates (0.12–1.50%). A multilingual reasoning benchmark (e.g., multilingual MATH or MMLU) would provide a stronger test of LCG's effect on thinking models.

### Trivial

- Table 4 caption states "Effectiveness of LCG Intervention on 'No-Think' Models" but the table reports thinking-model results; the caption appears to be a copy-paste error.

## Nice-to-Haves

- Report confidence intervals or standard deviations for the main results.
- Validate pseudo-target quality on a small human-annotated sample (e.g., 200–500 confusion points).
- Add individual ablations of Rule 2 and Rule 3 (beyond the all-or-nothing "No Rule" condition).
- Supplement the thinking-model evaluation with a multilingual reasoning task.

## Removed Points

- **"Large Reasoning Models seem to reintroduce the problem" claim not backed by own experiments.** This claim in the introduction is supported by citations to prior work (Guo et al. 2025, Wang et al. 2025), not asserted as the paper's own finding. It serves as motivation, not a claimed contribution. Not a weakness of the paper.
- **"No analysis of the gate's own accuracy / confusion matrix."** The paper evaluates downstream effects (confusion reduction), which is the primary metric of interest. A confusion matrix of gate predictions would be informative but is not required to validate the method's effectiveness.
- **Missing training hyperparameters for the gate.** The paper states the gate was trained on 78k samples but does not specify learning rate or number of steps. This is a reproducibility concern, but the gate is a standard two-layer MLP with BCE loss, and the paper provides enough detail to reproduce (training data composition, self-distillation procedure, architecture). Moved to nice-to-have.
- **FLORES-NO-LATIN may overestimate confusion due to legitimate English proper nouns.** The paper's own code-switch analysis (FLORES-WITH-LATIN, 86.7% preservation) partially addresses this concern. The limitation is acknowledged by the evaluation design itself.
- **Section-by-section notes about presentation and framing.** Most are either addressed in the retained weaknesses or are minor presentation observations that do not affect the paper's technical validity.

## Novel Insights

The harsh critic's observation that the rules-only (no learned gate) ablation is missing is the most insightful point. It identifies a concrete experiment that would cleanly separate the contribution of the learned MLP from the heuristics, which the existing "No Rule" condition does only halfway. The critic also correctly notes that the paper's strongest claim in the abstract ("decreases language confusion") lacks the qualifier "cross-script" that the method's actual capability requires, and that the thinking-model evaluation on code generation is a weak test of a language-confusion intervention. None of these insights contradict the paper's core contributions—they identify precise places where the evidence or framing could be tightened.

## Suggestions

1. Add the missing "rules-only" ablation condition (Rules 2 and 3 applied without the learned gate) to Figure 3. This is the single highest-leverage experiment to clarify the method's contribution.
2. Qualify the abstract and introduction claims to specify that LCG addresses *cross-script* language confusion, and mention the script-level granularity limitation up front.
3. Report standard deviations or confidence intervals for the main confusion rate results, especially in Table 3 where small absolute differences appear.
4. Provide training details for the ORPO baseline to make the comparison interpretable.

## Score and Decision

**Calibration anchors retrieved (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| 8QTpYC4smR (survey paper) | 1.00 | R1 | No | Much weaker; no novel contribution |
| gwZ90hFSL2 (pseudoscience) | 1.00 | R1 | No | Much weaker; not a valid paper |
| 5kMwiMnUip (jailbreaking) | 1.40 | R1 | No | Much weaker; no rigorous evaluation |
| P49gSPmrvN (discourse analysis) | 1.00 | R1 | No | Much weaker; different domain |
| fSbPwHjdDG (Llamas think in English) | 3.00 | R1 | No | Weaker; limited intervention analysis |
| IqGVIU4rvM (visual tokenizer) | 2.50 | R1 | No | Weaker; unclear contribution |
| 5dDYhvt6dY (efficient transformer) | 3.00 | R1 | No | Weaker; marginal improvement |
| UFwefiypla (speech tokenization) | 3.00 | R1 | No | Weaker; narrow evaluation |
| dDLGZTKZYZ (MLPs for NLP) | 3.75 | R1 | No | Weaker; shows MLPs inferior to transformers |
| UHg1xTRzZK (translation distillation) | 5.00 | R1 | Yes | Weaker; method not practically useful, similar weaknesses but more severe |
| VfYShlQbj7 (GNN distillation) | 5.00 | R1 | No | Weaker; analysis paper, no new method |
| rpR9fDZw3D (sequence knowledge distillation) | 4.00 | R1 | No | Similar tier but narrower contribution |
| CP6CAqxAGJ (vocabulary unification) | 5.67 | R1 | No | Comparable; similar practical contribution but less novel insight |
| HMa8mIiBT8 (cross-lingual consistency) | 6.00 | R1 | Yes | Comparable; had wrong assumption (-4), no error bars (-4), but detailed analysis (+2). My paper has a more novel insight and no equivalent methodological error. |
| BCyAlMoyx5 (crosslingual knowledge barriers) | 5.67 | R1 | Yes | Weaker; selected non-multilingual models (-5), data leakage (-3). My paper avoids such methodological missteps. |
| zGej22CBnS (byte-level probabilities) | 6.25 | R1 | Yes | Comparable; strong theoretical contribution (+4,+4) but very similar to prior work (-3) and minor improvements (-2). My paper has more novel empirical insight and the weaknesses are more addressable. |
| tyEyYT267x (diffusion LMs) | 8.00 | R1 | No | Stronger; sets new SOTA on multiple benchmarks |
| f4gF6AIHRy (dimensional collapse) | 8.00 | R1 | No | Stronger; solves a clear problem with rigorous evaluation |
| 1oijHJBRsT (instruction backtranslation) | 8.00 | R1 | No | Stronger; highly impactful self-alignment method |
| vf5aUZT0Fz (decoupled embeddings) | 8.00 | R1 | No | Stronger; significant pre-training efficiency gains |

**Round-1 bracket: 6.0–7.0.**

**Narrowing to final score:** The paper sits above anchors in the 3.0–5.0 range (which have fundamental flaws like wrong assumptions, non-multilingual models, or methods that don't actually work). It is comparable to the 5.67–6.25 anchors but with a more novel mechanistic insight (norm imbalance) than vocabulary unification (5.67) or cross-lingual consistency studies (5.67–6.00). Unlike the cross-lingual consistency paper that had a wrong assumption about language relatedness (-4) and the byte-level paper that was very similar to prior work (-3), this paper's weaknesses are about missing ablations and scope overclaiming—all addressable without invalidating the core contribution. However, the paper does not reach the 7.5+ level because the missing rules-only ablation prevents full confidence in the gate's contribution, the scope overclaiming is a framing issue that should be fixed, and the thinking-model evaluation is notably weaker than the no-think evaluation. The most relevant heavy-weight comparison item is the missing error bars (a -4 in the 6.00 anchor; here mitigated because the paper's confusion reduction is large in absolute terms, not marginal). The final score is **6.5**.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>