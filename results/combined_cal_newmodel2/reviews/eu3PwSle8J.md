Now let me compile the final review with all comparisons and the calibrated score.

## Summary

This paper proposes Augmented Intermediate Representations (AIR), a method for injecting instruction hierarchy (IH) signals into all decoder layers of a transformer LLM (via layer-specific trainable embedding tables), rather than only at the input layer as done in prior work (Delim, ISE). Evaluated across three model families (3B–8B), two training methods (SFT, DPO), and two datasets (AlpacaFarm, SEP), AIR consistently reduces attack success rate on gradient-based attacks (GCG, Astra) by 1.6× to 9.2× compared to prior IH injection mechanisms, with negligible parameter overhead (~0.4M for an 8B model) and minimal utility degradation.

## Strengths

- **Simple, low-overhead architectural modification.** The core idea — adding a trainable embedding table to each decoder layer, indexed by privilege level — adds only 0.4M parameters for an 8B model (0.005% increase), with negligible inference overhead. This makes the method practically appealing for deployment. [favorability=9.80]

- **Strong empirical results on gradient-based attacks.** Table 1 shows consistently large improvements on GCG and Astra attacks across all three model sizes. For example, on Llama-3.2-3B with SFT, AIR achieves 4.1% GCG ASR vs. 38% (Delim) and 48.1% (ISE). On Qwen-2.5-7B with DPO, AIR achieves 1.6% GCG ASR vs. 7.7% (ISE) and 32% (Delim). The robustness improvements on Astra are even more dramatic (e.g., 0.1% vs. 14.5% on Llama-3.2-3B SFT). [favorability=14.95]

- **Controlled experimental design.** The paper systematically varies the IH injection mechanism while holding the training procedure constant, allowing clean attribution of robustness differences to the injection mechanism rather than to confounding factors like different training data or hyperparameters. Evaluation spans three model families, two training methods (SFT, DPO), two datasets, and multiple attack types. [favorability=10.75]

## Weaknesses

### Major

- **The diagnostic in Figure 3 does not validly measure IH signal degradation for delimiter-based methods.** The paper computes cosine similarity between hidden representations of tokens assigned different privilege levels. For the Delim method, similarity is ~1.0 at all layers, which the paper interprets as the IH signal being lost (Section 3.2: "the representations may fail to adequately preserve the IH signals"). However, delimiter-based methods carry privilege information through special delimiter tokens at segment boundaries, not through modifications to regular token embeddings. Cosine similarity of non-delimiter token representations is not a meaningful diagnostic of whether the model can distinguish privilege levels via delimiter tokens. This weakens the paper's framing that *all* existing methods suffer from input-only signal degradation — the motivation holds cleanly for ISE but is overstated for Delim. This does not invalidate the empirical results, but it means the conceptual foundation of the paper's central critique is narrower than claimed. [favorability=-0.39]

- **Metric asymmetry between gradient-based and static attacks.** Gradient-based attack ASR is measured using model logits (likelihood of generating "hacked!"), while static attack ASR is measured using actual generated responses (checking if output contains "hacked!"). Logit-based and generation-based ASR can diverge. The paper's headline claims of 1.6× to 9.2× reduction in ASR are based on gradient-based attacks. While relative comparisons between methods use the same metric (so the ratios are valid), the absolute ASR numbers may differ under generation-based evaluation, and the paper does not acknowledge this transparency concern. [favorability=1.04]

### Minor

- **Asymmetric attack optimization steps not justified.** Gradient-based attacks use 200 steps for DPO models but only 50 for SFT models, without explanation or a plateau analysis. This does not affect within-group comparisons, but it makes cross-group claims (e.g., "adversarial training with DPO yields more robust models than SFT") harder to evaluate fairly. [favorability=6.22]

- **Missing ablation on shared vs. per-layer embeddings.** AIR uses a different trainable embedding table per layer, but there is no comparison against a shared embedding table. Such an ablation would distinguish whether the benefit comes from injecting the signal at all layers or from layer-specific customization. [favorability=3.11]

### Trivial

None.

### Nice-to-Haves
- Report generation-based ASR for gradient attacks alongside logit-based numbers.
- Discuss any failure cases or scenarios where AIR underperforms.
- Tighten the motivation in Section 3.2 to correctly distinguish signal degradation claims for ISE vs. Delim.

## Removed Points

These points were flagged in the input review but removed per filtering rules. They are listed here for awareness but should not weigh in the evaluation.

- **Strength about diagnostic evidence (Figure 3):** Removed because it conflicts with the verified weakness that the diagnostic is not valid for Delim methods.
- **Criticism about training dataset details in appendix:** Removed per rule that appendix-stripped content exists in the original submission and is not assessable.
- **Failure mode analysis request:** Removed as a generic/nice-to-have request, not an actual paper flaw.
- **"Connection to prior work" re-implementation note:** Removed as a minor clarification, not a substantive weakness.
- **Section-by-section editorial observations:** Removed as non-actionable comments.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions
- Report generation-based ASR for gradient attacks to resolve the metric asymmetry concern.
- Add an ablation comparing shared vs. per-layer embedding tables to isolate the source of AIR's improvement.
- Justify the asymmetric attack step counts (50 for SFT, 200 for DPO) with a saturation analysis.
- Revise Section 3.2's critique of prior work to correctly distinguish between ISE and delimiter-based methods.

## Calibration Anchors

| Anchor | Path | Avg Human Score | Round | Itemized? | Comparison to Reviewed Paper |
|--------|------|----------------|-------|-----------|------------------------------|
| PFT (prompt injection defense) | l3bUmPn6u5.md | 4.25 | 1,2 | Yes | Weaker paper: evaluated only against weak/static attacks, missing strong-attack evaluation, had questionable problem framing |
| ISE (instructional segment embedding) | sjWG7B8dvt.md | 6.00 | 2 | Yes | Most directly comparable — same topic, same type of contribution. AIR has stronger empirical results (gradient attacks) but a framing overreach (Delim diagnostic). Comparable overall quality. |
| SEP (instruction-data separation) | 8EtSBX41mt.md | 6.67 | 2 | Yes | Less directly comparable (benchmark/dataset contribution). Stronger paper with rigorous formalism; AIR is more applied. |
| Baseline Defenses | 0VZP2Dr9KX.md | 5.25 | 1 | Yes | Different type (survey-style evaluation). AIR has a clearer novel contribution. |
| ReFAT (refusal feature adv. training) | s5orchdb33.md | 5.75 | 1 | Yes | Mechanistically deeper but less directly comparable. AIR has stronger direct ASR improvements. |
| Jailbreaking (adaptive attacks) | hXA8wqRdyV.md | 6.14 | 1 | Yes | Attack paper, not defense. Different framing but comparable evaluation rigor. |
| RA-LLM | V01FPV3SNY.md | 5.33 | 1 | No | Similar defense scope but weaker empirical evaluation. |
| DPP (defensive prompt patch) | wetJo6xXb1.md | 4.50 | 1 | No | Weaker: prompt-based defense, not architectural. |
| AutoHijacker | 2VmB01D9Ef.md | 4.25 | 2 | No | Attack paper, different category. |

**Score calibration rationale:** The closest anchor is ISE (6.00, unanimous accept). Comparing itemized favorability: AIR's strongest strength (14.95 for empirical results on gradient attacks) exceeds ISE's best (12.85), and AIR's worst weakness (-0.39 for the Delim diagnostic) is milder than ISE's worst (-4.71 for novelty concerns). The ISE paper was unanimously accepted at 6. AIR delivers stronger empirical results against more challenging attacks, with better-controlled experiments. However, the framing overreach regarding the Delim diagnostic is a real flaw not present in ISE. Overall, the papers are of comparable quality — solid borderline accept contributions with clear practical value but some methodological imperfections. **Score: 6.0 (borderline accept).**

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>