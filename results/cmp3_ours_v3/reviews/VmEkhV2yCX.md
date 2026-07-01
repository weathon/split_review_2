I have all the evidence I need. Here is the final consolidated review.

---

## Summary

This paper presents a systematic empirical study of how reasoning data — varying in scale, diversity, and quality — affects LLM performance when introduced at different training stages (pretraining vs. SFT). The authors pretrain four 8B models from scratch for 1T tokens with different reasoning data mixtures, cross them with multiple SFT recipes, and include an RL phase. The central findings are: (1) front-loading reasoning data into pretraining creates a durable advantage that SFT cannot fully recover; (2) pretraining benefits from diverse data while SFT benefits from high-quality data (asymmetric principle); (3) high-quality pretraining data shows latent effects unlocked by SFT; (4) naive scaling of mixed-quality SFT data can be ineffective.

## Strengths

- **Ambitious and genuinely informative experimental design.** Pretraining four 8B models from scratch under controlled reasoning-data conditions, then crossing them with multiple SFT recipes and an RL phase, provides far richer evidence than the typical "pretrain once, fine-tune many" design. This is the paper's genuine differentiator.

- **Robust core finding.** The result that reasoning data injected during pretraining produces durable gains that SFT cannot fully recover is well-supported. The "catch-up" experiment (Table 4: M_base with 2× SFT epochs still cannot match M_SHQ + SFT_SHQ) directly tests and refutes a plausible counterargument.

- **The asymmetric principle is clearly demonstrated as an empirical pattern.** The contrast between M_LDQ vs. M_SHQ in pretraining (Table 1: 64.09 vs. 54.98) and SFT_SHQ vs. SFT_LDQ in SFT (Table 5: 44.99 vs. 31.54) is striking and internally consistent. Even with attribution caveats, the phase-dependent pattern itself is a valuable empirical observation.

- **The RL phase provides a sustainability check.** Showing that the gap widens rather than closes after RL (Table 3: 37.92 vs. 56.66) is essential evidence that the pretraining advantage is compounding, not superficial.

## Weaknesses

### Major

- **"Diversity" and "quality" attributions are confounded with multiple uncontrolled variables.** The paper attributes M_LDQ's pretraining advantage over M_SHQ to "diversity," and SFT_SHQ's SFT advantage over SFT_LDQ to "quality." However, D_LDQ (268M samples, 56% math/17% code/27% science, heterogeneous Q&A) and D_SHQ (1.2M samples, 71% math/21% code/8% science, long CoT from teacher models) differ on size (224× factor), domain distribution, data format, and — because D_SHQ is heavily repeated to reach 80B tokens during pretraining — repetition rate (line 93: "When a reasoning dataset is small, it is repeated"). Any of these could drive the observed gap. The paper's causal language (e.g., line 278: "diversity drives pretraining effectiveness, while quality governs SFT") overstates what the experimental design can cleanly attribute. The empirical pattern is valuable, but the mechanistic label is undersupported.

- **The "latent effect" claim has a straightforward alternative explanation from data overlap.** The paper claims that M_LMQ shows a +4.25% advantage over M_LDQ after SFT on D_SHQ (Table 4, line 215), arguing that high-quality pretraining data creates "latent potential" activated only by SFT. However, M_LMQ sees D_SHQ data during pretraining (as D_LMQ = D_LDQ + D_SHQ, line 86), while M_LDQ does not. Both are then SFT'd on D_SHQ. The +4.25% could simply reflect prior exposure to D_SHQ's format and content, making SFT more efficient through familiarity — a mundane explanation the paper never addresses. (Line 215: "M_LMQ achieves an additional +4.25% gain over M_LDQ post-SFT. This reveals a critical finding that high-quality but less diverse data may act as a complementary amplifier.")

### Minor

- **Numerical claims in the abstract are inconsistent with the tables.** The abstract claims an "11% average gain" from diversity in pretraining, but the body (line 211) reports "an absolute +9.09% average gain" for the diversity comparison (M_LDQ vs. M_SHQ). The abstract claims a "15% average gain" from quality in SFT; the relevant comparison in Table 5 shows a 13.45 percentage-point gap (M_res+SFT_SHQ at 44.99 vs. M_res+SFT_LDQ at 31.54). These discrepancies are small but undermine precision in the headline claims.

- **No variance or significance reporting for main results.** The paper reports multiple evaluation runs (16 runs for AIME, 4 runs for most other benchmarks, line 148) but never provides standard deviations, confidence intervals, or any uncertainty quantification for Tables 1–8. For fine-grained comparisons (e.g., the +4.25% latent effect, the 0.15-point change from doubling SFT data), it is impossible to assess whether differences are meaningful or within evaluation noise. (While multi-seed pretraining is cost-prohibitive, evaluation variance is reportable.)

- **The "naive scaling is harmful" claim is overstated relative to the evidence.** The abstract states that naively scaling SFT data "actively harmed mathematical reasoning by -5% on average." Table 8 shows that doubling D_LDQ changes the overall average from 32.84 to 32.99 (essentially flat), with a 4.92-point drop in MATH_SFT AVG specifically but science, code, and instruction-following flat or slightly positive. Characterizing this as broadly "harmful" is misleading when the overall effect is neutral. The data supports "unhelpful" or "math-specific degradation," not "actively harmful" as a general claim.

### Trivial

None.

## Nice-to-Haves

- Disentangle the diversity/quality confound with targeted ablations (e.g., filtering D_LDQ to only long-answer examples to match D_SHQ's quality profile, then comparing in pretraining).
- Address the latent-effect confound by testing with SFT data that M_LMQ has not seen during pretraining, or by explicitly acknowledging the data-overlap alternative.
- Add behavioral analysis (accuracy vs. reasoning length, error type breakdowns) to deepen understanding of where the gains come from.
- Report standard deviations for evaluation runs.
- Clarify throughout whether gains are reported as absolute percentage points or relative percentages.

## Removed Points

These points were flagged by the reviewer but are removed for the stated reasons:

- *"The optimization formalism (Equations 1–2) is never actually used"* — The framing is conceptual, not a literal optimization to solve. Standard for empirical framing.
- *"Section 2.2 doesn't disclose tokenization lengths or whether D_LDQ contains CoT"* — Minor data detail questions; not substantive weaknesses that affect the paper's claims.
- *"Section 4 main text aggregates across SFT recipes"* — Full breakdown is in Appendix Table 13. Standard practice.
- *"Table 3's RL only uses two models"* — The paper deliberately compares extremes (M_base vs. M_LMQ), which is a reasonable and common design choice.
- *"Section 5 instruction-following trade-off not properly qualified"* — The paper does acknowledge this trade-off (lines 251–252): "may modestly reduce alignment-sensitive metrics. The optimal balance may therefore depend on the target deployment domain."
- *"Missing behavioral analysis"* — Moved to Nice-to-Haves; not a weakness.
- *"The 1.2B transformer experiment is mentioned in passing"* — It is reported in the appendix (Table 14) as a cross-architecture validation; not a core part of the main argument.
- *Section-by-section presentation notes* — Not substantive enough.

## Novel Insights

The most valuable critical insight from the review process is identifying the data-overlap confound for the "latent effect" claim: M_LMQ's +4.25% SFT advantage over M_LDQ can be explained by simple prior exposure to D_SHQ during pretraining, not a mysterious "latent potential." This is a cleaner and more parsimonious explanation than the paper offers, and it directly undermines one of the four headline claims. A second insight is that while the asymmetric pattern (diverse in pretraining, high-quality in SFT) is empirically real and useful, the paper's causal attribution to "diversity" vs. "quality" as distinct mechanisms is not supported by the experimental design, which varies multiple factors simultaneously. Beyond these, the broader frame of "data allocation across training stages as a strategic design problem" is well-executed and the paper's core empirical contribution is solid.

## Suggestions

1. Reframe the diversity/quality attribution as observational rather than causal — the pattern is real and useful, but the underlying mechanism requires additional isolation.
2. Explicitly acknowledge the data-overlap alternative explanation for the latent-effect claim and, if possible, provide a control experiment with unseen SFT data.
3. Harmonize numerical claims across the abstract and main text, and clearly distinguish percentage-point differences from relative improvements.
4. Add standard deviations to the main result tables for evaluation metrics where multiple runs were conducted.

## Score and Decision

### Calibration Details

**Anchors retrieved (all rounds):**

| Path | Avg Human Score | Round | Comparison |
|------|----------------|-------|------------|
| `KIPJKST4gw.md` (At Which Stage Does Code Data Help LLMs Reasoning) | 7.25 | 1 | Very similar topic; that paper had a confound (uncontrolled total tokens) but was accepted. This paper has a more ambitious design but more central confounds. |
| `5BjQOUXq7i.md` (RegMix) | 7.20 | 1 | Methods paper for data mixture optimization; different contribution type. |
| `1hQKHHUsMx.md` (What Kind of Pretraining Data Do LLMs Rely On) | 6.75 | 2 | Empirical study about pretraining data for reasoning; similar contribution type. Comparable quality. |
| `GtpubstM1D.md` (Advancing Mathematical Reasoning) | 5.71 | 2 | Similar empirical study of CPT vs. SFT with confound issues. This paper is stronger in experimental design and control. |
| `EDoD3DgivF.md` (On Linear Representations) | 6.00 | 2 | Accepted with all 6s; different topic but comparable score anchor. |
| `8QTpYC4smR.md` (Systematic Review of LLMs) | 1.00 | 1 | Strong reject anchor; not comparable (survey paper). |

**Round 1 bracket:** 5.5–7.5. The paper is stronger than GtpubstM1D (5.71) in experimental design and control, but weaker than KIPJKST4gw (7.25) because its confounds are more central to the headline claims and harder to address with simple rebuttal fixes.

**Narrowing:** After inspecting full reviews of KIPJKST4gw and GtpubstM1D, the paper's combination of genuine empirical contribution + significant attribution confounds + numerical inconsistencies places it below KIPJKST4gw (7.25) and slightly below 1hQKHHUsMx (6.75). It aligns most closely with the strength of an accepted 6.0 paper.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>