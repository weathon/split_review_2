Now I have enough to write the draft review. Let me proceed.## Summary
OptMerge introduces (i) the first structured model merging benchmark for MLLMs with five capability categories (VQA, Geometry, Chart, OCR, Grounding), ≥100k samples each, covering both full fine-tuning (InternVL2.5) and LoRA (Qwen2-VL) regimes with publicly released checkpoints; (ii) a merging method combining SVD-based task vector denoising with robust data-free optimization; and (iii) modality merging experiments combining vision-, audio-, and video-language models toward an omni-model. The paper also derives a formal error bound (Theorem 3.1) explaining how fine-tuning intensity impacts merging quality.

---

## Strengths

- **Benchmark fills a genuine gap.** Prior MLLM merging work (AdaMMS, UQ-Merge) merges only two models at a time, requires test sets at merge time, or uses undifferentiated capability divisions. This paper provides the first taxonomy-driven benchmark with dual fine-tuning regimes and ≥100k samples per category, covering 10 merging baselines — the most comprehensive MLLM merging benchmark to date.

- **Modality merging is a genuinely novel framing.** Table 5 shows that static merging of vision-, audio-, and video-language models sharing a Vicuna-7B LLM backbone (67.00 avg) outperforms every individual modality model (best: 64.11) and competitive online composition methods NaiveMC (66.88) and DAMC (66.79), without extra parameters or training data.

- **Theorem 3.1 provides a formal account of fine-tuning intensity effects.** The three-term upper bound — convergence residual $\mathcal{O}(\gamma^T)$, cross-task interference $\mathcal{O}(\delta\eta T)$, curvature error $\mathcal{O}(\eta^2 T^2)$ — formally explains the empirical rise-then-fall merging performance pattern and motivates controlled parameter drift in benchmark construction.

- **Real-world Hugging Face validation (Table 6).** Merging four heterogeneous community-released models (math reasoning, Pokémon domain, PDF OCR, Vietnamese VQA) with OptMerge achieves 66.70 average, outperforming each individual model and the base Qwen2-VL-Instruct (62.23), demonstrating practical usability beyond controlled benchmarks.

---

## Weaknesses

### Fatal
None.

### Major

- **OptMerge underperforms its direct predecessor WUDI Merging in the primary LoRA setting (Table 3), contradicting the central method claim.** Table 3 shows WUDI Merging = 63.65 and OptMerge = 63.30 (−0.35 points). Section 5.2 nonetheless asserts "our approach achieves superior average results across various scenarios." OptMerge only leads in the full fine-tuning setting (Table 2: 57.44 vs 57.00, +0.44). Claiming consistent superiority when one of two primary experiments shows a regression is an overclaim that needs direct acknowledgment.

- **A 5-point numerical inconsistency between Table 3 and Table 4 undermines the ablation.** Table 4 uses 58.65 as the WUDI Merging baseline for Qwen2-VL, while Table 3 reports 63.65 for the same setting — a 5-point gap with no explanation. The paper's headline "2.48% average performance gain" (abstract, Section 1) is anchored to Table 4's ablation using the 58.65 baseline. If the correct baseline is 63.65 (as in Table 3), the 4.65% final improvement in Table 4 is illusory: OptMerge (63.30, Table 3) is actually below that baseline. The claimed headline figure is therefore not reproducible from the main evaluation tables and the inconsistency must be resolved.

- **The "data-free" characterization is overstated throughout.** Figure 1, the abstract, and the Introduction all label the method "data-free." However, Section 5.1 explicitly states: "we determine the optimal merging coefficient λ by searching within the range [0.1, 0.3, 0.5, 0.7, 1.0, 1.5]," which requires a validation set. All baselines are tuned identically, so cross-method comparisons remain fair, but the repeated "data-free" label misrepresents the method when it is compared against mixture training.

### Minor

- **Modality merging margins are small and significance is not assessed (Table 5).** The best static method (TSV, 67.34) leads OptMerge (67.00) by 0.34 points; OptMerge leads online composition (NaiveMC 66.88, DAMC 66.79) by <0.2 points. The claim of "outperforming online composition methods" is technically correct but the differences fall below any reported significance threshold.

- **Table 10 omits the InternVL2.5-1B-Instruct baseline, making general-task gains uninterpretable.** The dramatic ScienceQA gain (best individual model 76.54 → OptMerge 91.89) could reflect merging benefit or simply the instruct baseline already scoring near 91.89 on this benchmark; without that row the claim of "emergent integrated capabilities" cannot be verified.

### Trivial
None beyond resolved hard-rule removals below.

---

## Nice-to-Haves
- A jointly-trained omni-model baseline for Table 5 (analogous to mixture training in capability merging) would sharpen the core modality merging claim by showing whether joint training could achieve parity.
- Presenting a fixed-λ (e.g., λ=1.0) result alongside the searched-λ result would clarify method robustness without any validation-set search.
- Variance or standard deviation across tasks or runs for OptMerge vs. the two closest competitors, given differences are frequently <1 point.
- Adding the InternVL2.5-1B-Instruct row to Table 10 as a baseline.

---

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Claim that "data-free" comparison with test-time adaptation is unfair**: Partially retained as major weakness #3 (overstated characterization), but the cross-method fairness aspect is removed since all baselines are tuned identically under the same protocol.
- **Theorem 3.1 connection to OptMerge's SVD design is loose**: The reviewer's note that the theorem motivates benchmark construction but not directly the SVD method is valid but minor; removed as a standalone weakness since the paper does not conflate them in a way that invalidates the theorem.
- **Table 5 comparison with TSV not being the best**: TSV Merging (67.34) edges OptMerge (67.00) in modality merging; retained in minor weakness rather than as a separate point.
- **Speculation about ablation using a "different configuration"**: Retained only as the factual inconsistency (Table 3/4 discrepancy), not as speculation about why it exists.
- **Request for confidence intervals across all tables**: Moved to nice-to-haves.

---

## Novel Insights
The modality merging framing — treating audio-language, video-language, and vision-language models as mergeable experts given a shared LLM backbone — is a conceptually clean and practically impactful contribution that prior model merging work has not systematically explored. The finding that static merging of single-modality models can match or exceed online composition methods (which require 3× the parameter storage) suggests model merging as a viable path to omni-model construction, independent of the contested OptMerge vs. WUDI comparison. Theorem 3.1's decomposition of the merged loss into three interpretable terms (convergence residual, interference, curvature) also provides a reusable analytical lens for future benchmark design in model merging.

---

## Suggestions
1. **Resolve the Table 3 / Table 4 baseline discrepancy (58.65 vs 63.65) explicitly.** If the ablation was run on a subset of benchmarks or under different hyperparameters, say so and provide a separate ablation row for the full Table 3 protocol.
2. **Revise the headline "2.48% improvement" claim** to accurately reflect the win/loss record: OptMerge leads WUDI in full fine-tuning (+0.44%, Table 2) and on Hugging Face models (+1.9%, Table 6), but trails in LoRA (−0.35%, Table 3) and roughly ties in modality merging.
3. **Replace "data-free" with "validation-guided" or "training-data-free"** throughout, and add a sentence in Section 5.1 clarifying that λ search uses a small validation set.
4. **Add InternVL2.5-1B-Instruct as a row in Table 10** to establish whether merged-model gains exceed the instruction-tuned baseline.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| lNtio1tdbL (ATM: Alternating Tuning and Merging) | 3.00 | R1 | Merging method + theory, weaker benchmark; cleaner theoretical motivation but no MLLM focus |
| Bq3fEAGXUL (Realistic Eval of Model Merging) | 5.33 | R1 | Benchmark + multi-setting evaluation; comparable scope to OptMerge's benchmark half, no novel method |
| fvUVe2gJh0 (What Matters for Model Merging at Scale?) | 5.33 | R1/R2 | Systematic benchmark-style evaluation without a new merging method |
| plflYGf23L (CABS) | 4.75 | R1/R2 | Method + experiments, similar field; modestly outperforms baselines |
| lIdc5DUplq (SUPERMERGE) | 4.33 | R2 | Gradient-based merging method; weaker experimental scope |
| 1v7SRWsYve (MAP) | 6.33 | R2 | Principled method with Pareto fronts; cleaner theoretical + empirical support |
| irPcM6X5FV (Leveraging Submodule Linearity) | 6.00 | R2 | Task arithmetic method with clean closed-form results; consistent improvement over baselines |
| McqeEcMSzy (Task Vectors are Cross-Modal) | 3.67 | R1 | VLM task vector analysis; interesting but weaker empirical support |
| 4wuvmJRAU4 (Interfering with Interference) | 5.00 | R2 | SVD/random-projection merging, no benchmark contribution |

**Round 1 bracket: 4.5 – 5.5.**

The benchmark contribution (structured MLLM taxonomy, dual fine-tuning regimes, modality merging framing, released checkpoints) is at the level of the 5.33 benchmark papers (Bq3fEAGXUL, fvUVe2gJh0). However, the method claims (OptMerge) are significantly weakened by the Table 3/Table 4 inconsistency and the regression vs. WUDI in the primary LoRA setting. Papers that consistently demonstrate method improvement land around 6.0 (irPcM6X5FV, MAP); OptMerge does not clear that bar. The two major credibility issues push this below the 5.33 pure-benchmark anchors, as they undermine the method half of the dual contribution. On the other hand, the benchmark is more comprehensive than those pure-benchmark papers, preventing a drop to 4.33.

**Final score: 5.0** — the benchmark portion justifies borderline consideration, but the inconsistencies and the overclaimed method headline prevent acceptance as written.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>