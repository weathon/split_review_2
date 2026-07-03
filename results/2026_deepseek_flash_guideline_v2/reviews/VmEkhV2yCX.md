Now I have enough understanding of the paper to write the final review. Let me compile it.

## Final Consolidated Review

---

## Summary

This paper conducts a systematic, large-scale empirical study of how reasoning data (varying in diversity, quality, and scale) should be allocated across pretraining and supervised fine-tuning (SFT) stages of LLM training. By pretraining four 8B models from scratch under controlled conditions (1T token budget, 80B reasoning tokens), cross-finetuning all four on three SFT datasets, and extending two to RL, the paper finds that: (1) front-loading reasoning into pretraining creates durable advantages that SFT alone cannot replicate; (2) an asymmetric principle where diversity matters more in pretraining while quality matters more in SFT; (3) high-quality pretraining data can have "latent effects" unlocked by SFT; and (4) naive SFT scaling with mixed-quality data can be actively harmful.

## Strengths

1. **Controlled, fully-crossed experimental design.** Four 8B models pretrained from scratch under the same 1T token budget and 80B reasoning token constraint, cross-finetuned on three SFT datasets (12 SFT models), with RL applied to the two extreme conditions. This enables causal attribution of downstream gains to the *phase* of reasoning data injection, which prior mid-training studies could not achieve because their interventions were confined to post-training without end-to-end pretraining control (Section 2.3).

2. **Direct empirical refutation of the "catch-up" hypothesis.** Table 4 shows that even doubling SFT epochs for M_base (→ 34.01 average) still underperforms the weakest reasoning-pretrained model, M_SHQ + SFT_SHQ (37.33). This provides concrete evidence that the gap from early reasoning injection is structural, not removable by simply scaling post-training.

3. **Asymmetric principle with phase-dependent optimal data strategy.** Diversity drives pretraining effectiveness (M_LDQ 64.09 vs M_SHQ 54.98, Table 1), while quality dominates SFT (M_res + SFT_SHQ 44.99 vs M_res + SFT_LDQ 31.54, Table 5). This inverted preference is a novel finding that goes beyond generic "data quality matters" advice because it shows that the optimal data property depends on the training phase.

4. **Identification of a "latent effect" from high-quality pretraining data.** M_LMQ (mixing SHQ into LDQ) shows minimal advantage over M_LDQ at pretraining (64.07 vs 64.09, Table 1) but pulls ahead after SFT by +4.25% (50.95 vs 46.70, Table 4). This counterintuitive finding about pretraining-SFT synergy is well-supported by the data.

5. **Quantifies harm from naive SFT scaling.** Table 8 shows that doubling mixed-quality LDQ data in SFT yields no average improvement (32.84 → 32.99) and actively degrades math reasoning by -4.92% (28.38 → 23.46), while a marginal (0.4%) addition of high-quality long-CoT data yields consistent gains. This provides a concrete, actionable negative result.

6. **RL compounding effect demonstrated.** Table 3 shows the pretraining advantage widens through RL (M_base + SFT + RL: 37.92 → M_LMQ + SFT + RL: 56.66, with a ~39 point gap on AIME24/25), providing evidence of compounding rather than merely additive returns from early reasoning injection.

## Weaknesses

### Major

1. **Repetition confound undermines the central "diversity > quality in pretraining" claim.** The paper keeps a constant 80B reasoning token budget. D_SHQ has 1.2M samples; D_LDQ has 268M samples. Because D_SHQ is far smaller, it is repeated many times to reach 80B tokens (the paper acknowledges this at line 93: "When a reasoning dataset is small, it is repeated"), while D_LDQ may be seen largely once. The headline comparison — M_LDQ (diverse, large) outperforms M_SHQ (narrow, small, high-quality) — is attributed to "diversity and scale mattering more than quality in pretraining" (lines 210–211). However, the gap could equally or partially reflect detrimental effects of extreme repetition (memorization, loss of gradient diversity, reduced coverage). Since repetition frequency and data properties are collinear in this design, the claim that "diversity drives pretraining effectiveness" (Conclusion) does not unambiguously follow from the evidence. A clean test would either subsample D_LDQ to match the unique-example count of D_SHQ (~1.2M) before repeating to 80B tokens, or test D_SHQ with fewer repetitions against a smaller total reasoning token budget.

### Minor

2. **Catch-up experiment scope too narrow for the strength of some claims.** The catch-up test (Table 4) uses only one remedial strategy: 2× SFT epochs on the *same* SFT dataset (D_SHQ). The experimental section is appropriately measured ("cannot be fully replicated by *simply scaling* the SFT phase," line 213), but the abstract and introduction make broader claims: "proving that SFT cannot compensate for a weak foundation" and "cannot be fully replicated by later-stage SFT, even with more data" (abstract). The test does not explore other potentially stronger catch-up strategies (more diverse SFT data, multi-stage SFT, curriculum-based SFT, etc.). A finding that one specific catch-up attempt fails is informative but does not warrant universal claims about SFT's inability to compensate.

3. **Ambiguous percentage reporting.** The abstract reports "19% average gain," "11% average gain," and "15% average gain" without specifying whether these are absolute percentage point gains or relative gains. The "19% gain" is actually 18.74 absolute percentage points (Table 3: 56.66 − 37.92), which corresponds to a ~49% *relative* improvement. Similarly confusing for the other figures. This could mislead readers. The paper should consistently disambiguate absolute vs. relative gains.

4. **Formalism-practice mismatch.** Equation 2 sets up a constrained optimization over a fixed total budget B = |D_res^PT| + |D_res^SFT|, but the experiments never enforce this trade-off — pretraining tokens are held fixed while SFT varies freely. This minor mismatch between the mathematical framing and actual experimental design could confuse readers.

5. **Only 2 of 12 SFT models carried to RL phase.** The RL experiment (Table 3) compares only M_LMQ + SFT_SHQ vs M_base + SFT_SHQ. This limits understanding of whether the RL-stage advantage generalizes across SFT datasets or whether the choice of SFT_SHQ is crucial for realizing RL gains. While cost constraints are understandable, the paper does not acknowledge this as a limitation.

### Trivial

6. **No statistical uncertainty reported.** No standard deviations, confidence intervals, or significance tests accompany any result. This is broadly consistent with norms for single-run large-scale pretraining experiments, but the paper should explicitly acknowledge this limitation rather than presenting numbers as if deterministic.

7. **No dedicated limitations section.** The paper lacks a paragraph discussing its limitations (single model size/architecture, single run per condition, proprietary data, repetition confound, limited RL scope).

## Nice-to-Haves

- Extend the catch-up experiment with more diverse SFT data or multi-stage SFT to strengthen the "catch-up is impossible" claim.
- Release the composition of D_LMQ and the exact mixing ratios for reproducibility.
- Add an explicit limitations paragraph.

## Removed Points

The following points from reviewers were removed with justification:

- *"First systematic study" claim overstated* — Removed as a minor novelty dispute; the paper can reasonably frame its contribution as "first systematic study of reasoning data *across both pretraining and SFT with a crossed design*," which is defensible.
- *Proprietary data limits reproducibility* — Removed per policy: criticisms questioning the existence/availability of cited datasets are disallowed.
- *SFT evaluation benchmarks are harder than base model evaluations* — Removed because the paper explicitly acknowledges this design choice in Section 3.2 ("unlike in base model evaluations, where mostly focus on the generalizability of the LLM").
- *Missing appendix content* — Removed per policy: the parser strips these sections; they exist in the original submission.
- *Generic formatting/presentation nitpicks* — Removed as parser artifacts.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Deconfound repetition from data diversity.** This is the single most impactful improvement. Compare M_LDQ against a version of D_LDQ subsampled to the same unique-example count as D_SHQ (~1.2M samples), then repeated to 80B tokens. If subsampled D_LDQ still outperforms D_SHQ, the diversity claim is supported; if not, the gap is driven by repetition artifacts.
- **Clarify percentage claims.** Consistently specify whether reported gains are absolute (percentage point) or relative throughout the abstract and introduction.
- **Qualify the "catch-up" claim.** Acknowledge that only one remediation strategy was tested and that other SFT strategies might narrow the gap further.
- **Add a limitations paragraph.** Discuss single run per condition, repetition confound, limited RL scope, and single architecture/scale.
- **Acknowledge the RL-phase limitation** that only 2 of 12 SFT conditions were carried forward.

## Score and Decision

The paper provides valuable large-scale empirical evidence on a timely question and several of its findings (front-loading helps, asymmetric principle via SFT, latent effects, harmful SFT scaling) are well-supported. However, the central claim that "diversity drives pretraining effectiveness" is confounded with repetition frequency in the critical M_LDQ vs M_SHQ comparison, and the catch-up claims are somewhat overextended relative to the evidence. The contributions are real and practically relevant, but the core interpretability problem needs resolution before the paper's main thesis is fully convincing.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>