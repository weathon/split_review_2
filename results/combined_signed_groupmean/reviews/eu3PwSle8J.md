Now let me compile the final review. Here is my calibration analysis:

**Round-1 Bracket:** 6.5–7.5 (based on comparison with ISE paper at 6.00, Safety Layers at 6.00, and other LLM defense papers in the 6–7 range).

**Narrowing:** The ISE paper (6.00) had major weaknesses: novelty concerns (impact -9.99) and limited improvement on IH benchmark (-6.92). AIR's weaknesses are all minor (max -0.48 impact). AIR is clearly stronger than ISE — better motivation (diagnostic evidence), more thorough evaluation (3 models × 2 training methods × gradient-based attacks), and cleaner methodology. However, AIR is still an incremental extension within the same IH paradigm, and papers at 7.5+ (e.g., "Evaluating Zero-shot Robustness" at 7.50) tend to have broader scope or more original contributions. Therefore I narrow to 7.0.

**Calibration Anchors Used:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/sjWG7B8dvt.md` — ISE paper, avg 6.00, Round 1 & 2, itemized. AIR improves on this directly with stronger motivation and evaluation.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/8EtSBX41mt.md` — SEP paper, avg 6.67, Round 2, itemized. Different contribution type (benchmark paper).
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/l3bUmPn6u5.md` — PFT paper, avg 4.25, Round 2, itemized. Rejected paper with far more serious weaknesses.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/kUH1yPMAn7.md` — Safety Layers paper, avg 6.00, Round 3, itemized. Had major weaknesses like missing references and inappropriate metrics (-9.47 to -10.00 impact).

**Other anchors (not itemized) from calibration_search:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5kMwiMnUip.md` — avg 1.40, strong reject (not comparable)
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/3MDmM0rMPQ.md` — avg 3.00, reject (weaker defense paper)
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/2VmB01D9Ef.md` — avg 4.25, reject (attack paper)
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/0VZP2Dr9KX.md` — avg 5.25, reject (baseline defense paper)
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/rnJxelIZrq.md` — avg 6.50, accept (different defense method)
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/sULAwlAWc1.md` — avg 7.00, accept (attack paper)
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/g9diuvxN6D.md` — avg 7.50, accept (analysis paper, broader scope)

---

## Summary

This paper identifies a limitation in existing Instruction Hierarchy (IH)-based defenses against indirect prompt injection: injecting IH signals only at the input layer allows the signal to degrade as representations propagate through decoder layers. The authors propose Augmented Intermediate Representations (AIR), which injects a small trainable embedding (0.4M parameters for 8B models) at every decoder layer to maintain privilege-level separation. Across 3 models, 2 training methods (SFT, DPO), and multiple attack types, AIR consistently outperforms prior IH injection mechanisms (Delim, ISE), achieving 1.6× to 9.2× lower ASR on gradient-based attacks without significantly degrading utility.

## Strengths

- **Well-motivated diagnostic finding (Figure 3).** The paper does not simply assert that input-level IH signals degrade — it measures it. Using 100 prompts from AlpacaEval with two privilege levels, it shows that cosine similarity between representations of differently-privileged tokens increases through layers (ISE: 0.55→0.92). AIR maintains lower similarity (0.55→0.88), directly justifying the method before any robustness results. [impact=+9.64]

- **Clean and lightweight method.** AIR adds one small trainable embedding table per decoder layer — 0.4M parameters for Llama-3.1-8B (0.005% increase). The design is as simple as possible while addressing the identified problem, and overhead is clearly quantified. [impact=+8.90]

- **Thorough evaluation grid.** The paper evaluates 3 model sizes (3B, 7B, 8B) × 2 training methods (SFT, DPO) × 3 IH injection mechanisms (Delim, ISE, AIR) against 4 static attacks + 2 gradient-based attacks. All mechanisms undergo the same controlled two-stage training procedure. [impact=+8.37]

- **Compelling results against gradient-based attacks.** In Table 1, AIR consistently achieves lower ASR than both Delim and ISE across all model/attack/training combinations, often with large margins. For example, Llama-3.2-3B against Astra drops from 14.5% (SFT-Delim) or 25.8% (SFT-ISE) to 0.1% (SFT-AIR); Qwen-2.5-7B against Astra drops from 39.2% (SFT-ISE) to 2.4% (SFT-AIR). [impact=+9.98]

- **Utility is preserved.** Figure 6 shows AIR's win rates on AlpacaEval are comparable to or slightly better than the non-adversarial baseline, with <2% degradation in one case honestly reported. [impact=+9.89]

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Gradient-based ASR is measured from log-probabilities, not decoded output.** The paper states (Section 5.4) that gradient-based attack ASR is "measured using the likelihood (from model's logits) of generating the target phrase," while static-attack ASR uses text-based detection. These are different quantities — log-probability ASR is a proxy, not observed success. The paper does not discuss this choice or report empirical (decoded) ASR. Within-gradient comparisons are fair (same metric for all methods), and Figure 7's loss curves provide complementary evidence, but the headline ratios (1.6× to 9.2×) rest on this logit-based proxy. [impact=-0.48]

- **SEP improvements over ISE are modest.** The average AIR improvement over ISE on SEP is ~0.5 points across 6 configurations (with two ties). SEP is the most diagnostic benchmark for instruction-data separation, which AIR's mechanism directly targets. The improvement is real but small, somewhat undercutting the strength of the mechanistic claim. [impact=-0.08]

- **Gradient-based attacks use only 50 (SFT) or 200 (DPO) optimization steps.** Standard GCG literature often uses 500–1000+ steps. The paper does not justify these counts. Figure 7 shows loss curves still decreasing at the final step for some configurations. It is unclear whether AIR's advantage persists at convergence. [impact=-0.00]

- **No confidence intervals or variance estimates for Table 1 ASR results.** For gradient-based attacks with random initialization, multiple runs with different seeds would strengthen statistical reliability. [impact=-0.04]

- **ISE sometimes underperforms Delim** (e.g., Llama-3.2-3B GCG SFT: Delim=38 vs ISE=48.1; Llama-3.2-3B Astra DPO: Delim=34.5 vs ISE=57.3). If an input-level injection method can be worse than simple delimiters, this merits discussion and suggests that adding layer-wise embeddings might not monotonically improve robustness. [impact=-0.00]

- **The 145× claim for Astra** (line 242: 14.5/0.1) is unstable because the denominator is near zero. A single instance flip could change the ratio dramatically. The paper should note this limitation. [impact=-0.00]

- **Diagnostic experiment (Figure 3) only tests Llama-3.2-3B.** Showing similar degradation on Qwen-2.5-7B and Llama-3.1-8B would strengthen the claim that input-level IH signal degradation is a general phenomenon. [impact=-0.01]

- **SFT uses full fine-tuning while DPO uses LoRA** (lines 163–164), introducing a confound between training objective and parameter efficiency. This is acknowledged as corroborating SecAlign but means SFT vs DPO comparisons conflate two factors. [impact=-0.02]

- **No dedicated limitations section.** A defense paper should discuss failure cases, e.g., AIR requires architectural modification (not applicable to API-only access), an adaptive attacker could target the IH embedding tables, and evaluation is against specific attacks with specific parameters. [impact=-0.20]

### Trivial
None.

## Nice-to-Haves
- Report empirical (decoded-text) ASR for gradient-based attacks alongside the logit-based proxy.
- Run gradient-based attacks for more steps (e.g., 500–1000) to confirm AIR's advantage persists at convergence.
- Add confidence intervals or variance estimates for Table 1.
- Show the diagnostic experiment (Figure 3) on Qwen-2.5-7B and Llama-3.1-8B.
- Discuss why ISE sometimes underperforms Delim and what this implies about injection mechanisms.

## Removed Points
These points are flagged to be removed, treat them with caution:
- **Abstract/Introduction framing concern about "1.6× to 9.2×" reduction**: The paper's abstract (line 9) and introduction (line 35) both explicitly state "on gradient-based prompt injection attacks." The criticism that the framing could mislead is inaccurate — the scope is already clearly specified. REMOVED (factually incorrect criticism).
- **RoPE analogy imprecision**: The paper acknowledges RoPE modifies self-attention while AIR modifies residual stream. The analogy is about the principle of distributing critical information across layers, not a mechanistic equivalence. REMOVED (presentation nitpick).
- **Figure 8 description being vague**: A presentational preference, not an evidence problem. REMOVED.
- **Table formatting complaints**: The garbled table is a parser artifact, not a paper flaw. REMOVED per hard rules.
- **Training datasets not in main text**: The paper refers to Appendix B.1, which is standard practice. REMOVED per soft rules.

## Novel Insights
None beyond the paper's own contributions. The harsh critic's main novel observation is the logit-based ASR measurement issue — this is a genuine methodological note that distinguishes how different attack types' ASR is computed, but the paper's loss curves (Figure 7) provide complementary evidence that mitigates the concern.

## Suggestions
- Add a limitations/discussion section covering: (a) AIR requires architectural modification (not applicable to API-only access), (b) adaptive attackers could target the IH embedding tables, (c) evaluation is against specific attacks with specific parameters.
- Report decoded-text ASR for gradient-based attacks to complement the logit-based measure.
- Extend gradient-based attacks to more optimization steps to demonstrate AIR's advantage at convergence.
- Add confidence intervals or error bars to Table 1.
- Discuss the ISE < Delim cases and what they reveal about injection mechanisms.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>