Now let me compose the draft review and call `draft_review`, then do calibration.Based on my reading and calibration, let me finalize the review.

**Bracket:** Between 5.5 and 7.0. The paper is clearly above reject-tier (stronger than GtpubstM1D at 5.71 in scope, compute, and novel latent finding), but the diversity-repetition confound and limited RL comparison prevent it from reaching the 7.5-8.0 tier occupied by papers like "Synthetic continued pretraining" or "Training on the Test Task."

---

## Summary
This paper conducts what it claims to be the first systematic study of how reasoning data (varying in scale, diversity, and quality) affects LLM performance when injected at different stages of a three-phase training pipeline (pretraining → SFT → RL). Training an 8B hybrid Mamba-2/attention model from scratch at 1T tokens under four pretraining configurations and crossing each with multiple SFT recipes, the paper finds: (1) front-loading reasoning into pretraining yields durable advantages that SFT cannot recover; (2) diversity/scale matters most in pretraining while quality dominates SFT; (3) high-quality pretraining data has a "latent" effect only revealed after SFT; and (4) naively scaling SFT with noisy data is harmful.

## Strengths

- **Computationally ambitious, rare experimental scope.** Training four distinct pretraining configurations from scratch at 1T tokens (512 H100s each) is genuinely expensive and uncommon. Most prior work on reasoning data addresses only SFT or mid-training fine-tuning; this paper covers the full pretraining-to-RL continuum end-to-end, filling a real gap the community has had to speculate about due to compute cost.

- **The latent quality effect (Table 4) is specific and non-obvious.** M_LMQ ≈ M_LDQ immediately after pretraining (64.07 vs. 64.09 average in Table 1), yet post-SFT with the same recipe M_LMQ surpasses M_LDQ by +4.25% (50.95 vs. 46.70 in Table 4). This is a concrete, surprising finding that challenges the intuition that pretraining improvements should be directly visible from base-model evaluations, and points to a non-additive interaction between pretraining data quality and SFT alignment.

- **Honest catch-up falsification (Table 4).** Rather than simply asserting SFT cannot compensate, the paper tests 2× SFT epochs on M_base (34.01), which still falls below even the weakest reasoning-pretrained model M_SHQ + SFT_SHQ (37.33). This is a proper falsification attempt, not just a weak baseline.

- **RL analysis shows widening, not narrowing, gap (Table 3).** The gap between best and worst pretraining configuration grows substantially (+18.57%) after RL, providing important evidence that pretraining effects compound rather than wash out across subsequent training phases.

## Weaknesses

### Fatal
None.

### Major

- **Diversity vs. repetition confound in pretraining undermines the paper's central mechanistic claim.** The asymmetric principle "diversity matters more than quality in pretraining" is established by comparing M_SHQ (1.2M high-quality samples) vs. M_LDQ (268M diverse samples), both receiving 80B reasoning tokens. The paper explicitly states: "When a reasoning dataset is small, it is repeated" (Section 2.3). With D_SHQ at 1.2M samples, filling 80B reasoning tokens requires roughly 130× repetition (at ~500 tokens/sample). The lower performance of M_SHQ (avg 54.98 vs. 64.09 in Table 1) could entirely reflect overfitting/memorization from extreme repetition, not an absence of diversity per se. The current experimental design cannot distinguish "diversity is critical" from "heavy data repetition is harmful." An ablation sub-sampling D_LDQ to match D_SHQ's token count without repetition would isolate the actual causal variable at modest additional compute cost. Without it, the paper's specific mechanistic claim about diversity — which is the paper's most prominent result — is structurally under-evidenced.

- **RL comparison is limited to two extremes, making the "19% average gain" headline misleading.** Table 3 compares only M_LMQ + SFT_SHQ + RL vs. M_base + SFT_SHQ + RL — the best pretraining configuration against the worst. No RL results for M_LDQ or M_SHQ are shown, so whether the RL-stage gap monotonically tracks pretraining quality is unknown. The abstract's characterization of "19% average gain" creates a false impression of breadth when it is a single pairwise comparison of extremes.

### Minor

- **Budget-constraint framing (Eq. 2) is not experimentally implemented.** The paper frames its study as optimizing over a fixed budget B = |D_res^PT| + |D_res^SFT|, implying a genuine stage-level trade-off. But pretraining fixes reasoning tokens at 80B across all variants and SFT always uses 4.8M samples — these totals are never traded against each other across conditions. The paper answers "what type of data works best at each stage" rather than "how to allocate a fixed total reasoning budget," which is a different and somewhat more limited question than advertised.

- **Table 5 aggregates heterogeneous models (M_res), obscuring heterogeneity.** The comparison M_res + SFT_LDQ vs. M_res + SFT_SHQ averages across M_SHQ, M_LDQ, and M_LMQ pretrained models. Table 4's individual breakdowns are far more informative; the aggregation in Table 5 masks whether the quality benefit is uniform across pretraining conditions or driven by specific variants.

- **No variance/confidence intervals despite noise-sensitive benchmarks.** AIME results are averaged over 16 runs, which is appropriate, but no standard deviations appear in any table. For key findings like the +4.25% M_LMQ vs. M_LDQ post-SFT and the catch-up comparison (−4.09% vs. +3.32%), uncertainty bounds are relevant to assess whether these are distinguishable from noise.

### Trivial

- The 1.2B Transformer replication (Table 14) demonstrating architectural robustness is mentioned only in passing in the main text (Section 4) rather than receiving a brief dedicated discussion.

## Nice-to-Haves
- An ablation decoupling repetition from diversity: sub-sample D_LDQ to match D_SHQ's token budget without repetition and compare against M_SHQ. This is the single highest-impact experiment and would cost a fraction of the existing runs.
- Complete the RL comparison by running RL on M_LDQ + SFT_SHQ and M_SHQ + SFT_SHQ to test whether compounding is monotone with pretraining quality.
- Report token counts (not just sample counts) for SFT datasets; D_SHQ's long CoT traces likely represent far more tokens per sample than D_LDQ, and this asymmetry may confound the SFT quality comparison.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Front-loading" label is misleading within pretraining** (reviewer concern that reasoning appears only in the last 400B of 1T pretraining tokens). The paper explicitly describes this schedule; "front-loading relative to SFT" is accurate per the paper's framing. The term choice is not a factual error.
- **D_ALF length proxy not validated** (section-level note). Valid but too minor/speculative to constitute a standalone weakness — demoted out of the list.
- **Architecture non-standardness as a weakness.** The paper trains a single consistent architecture throughout; citing its hybrid Mamba-2 nature as a weakness is scope creep — the 1.2B Transformer replication addresses cross-architecture generalizability.
- **No confidence intervals as Major.** Moved to Minor; AIME is reported with 16-run averaging and single-run reporting is standard practice in large-scale LLM pretraining papers.
- **Table 8 generalizability limited to M_LDQ base.** Framed as an ablation; the narrowness is acknowledged and stated as a limitation.

## Novel Insights
The paper's most genuinely novel mechanistic observation is the "latent quality effect": high-quality pretraining data (in D_SHQ) produces minimal measurable gain at the base-model evaluation stage yet unlocks substantial gains (+4.25%) after SFT alignment. This suggests a non-additive interaction where pretraining data quality installs latent representational structure that only becomes visible — and useful — once the model is fine-tuned. This finding has implications beyond this paper: it implies base-model evaluations may systematically underestimate the value of pretraining data quality, and that pretraining data choices should be judged by their post-SFT performance ceiling rather than their immediate base-model scores.

## Suggestions
- Run the sub-sampled D_LDQ ablation (matching D_SHQ token volume, no repetition) to isolate diversity from repetition — the single most impactful addition.
- Correct the budget-constraint framing: either implement Eq. 2 as a true trade-off experiment, or reframe the objective as "phase-specific data strategy" without the fixed-budget constraint language.
- Add RL results for intermediate pretraining variants (M_LDQ, M_SHQ) to test monotonicity of compounding.
- Include a brief discussion of Table 14 (1.2B Transformer replication) in the main text.

## Score and Decision

**Anchor Papers Retrieved:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| 8QTpYC4smR.md | 1.00 | R1 | Generic LLM survey; nothing like this paper |
| 5kMwiMnUip.md | 1.40 | R1 | Jailbreaking paper; unrelated |
| SaOxhcDCM3.md | 3.20 | R1 | Self-consuming training loop study; related topic but narrower scope |
| EOPLy80bBm.md | 3.00 | R1 | Data pruning for fine-tuning; related but no pretraining scope |
| 28gMnEAgl9.md | 5.33 | R1 | LLMs on abstract reasoning benchmark; purely evaluation, no training study |
| 8uXkyWFVum.md | 4.20 | R1 | Pre-training/fine-tuning relationship study; similar spirit but shallower experiments, smaller scale |
| cijO0f8u35.md | 5.25 | R1 | Scaling math reasoning with SFT; similar topic, narrower scope (no from-scratch pretraining or RL) |
| th63j8qHa6.md | 4.25 | R1 | Math for AI generalization; related but no systematic from-scratch pretraining experiments |
| GtpubstM1D.md | 5.71 | R1 | Most similar: math reasoning at pretraining/SFT stages; reviewed paper is broader (8B, from scratch, RL included, multi-domain) and finds novel latent effect |
| w6nlcS8Kkn.md | 6.67 | R1 | CoT meta-analysis; well-executed systematic empirical study; reviewed paper comparable in rigor |
| S6cBH99BhB.md | 6.50 | R1 | Multilingual reasoning data proportions study; narrower scope |
| C25SgeXWjE.md | 6.25 | R1 | FOL reasoning benchmark paper; different contribution type |
| PdaPky8MUn.md | 8.00 | R1 | Fair comparison requiring data-driven priors; stronger methodological contribution, cleaner causal claims |
| 07yvxWDSla.md | 8.00 | R1 | Synthetic continued pretraining (EntiGraph); novel method + strong theory; cleaner contribution |
| mMPMHWOdOy.md | 8.00 | R1 | WizardMath; strong SOTA results with clear methodology |
| jOmk0uS1hl.md | 8.00 | R1 | Training on the Test Task; crisp conceptual contribution with broad empirical sweep |

**Round 1 Bracket:** 5.5–7.0

The reviewed paper sits clearly above the 3.5–5.5 tier (it is more ambitious, more expensive, and more novel than papers like 8uXkyWFVum or cijO0f8u35). It is comparable to GtpubstM1D (5.71) but stronger in scope, scale, and novel findings (RL phase, latent quality effect). It is below the 8.0 tier (PdaPky8MUn, EntiGraph) which all have cleaner methodological claims and novel algorithmic/theoretical contributions. The closest analog is the 6.5–6.7 range of systematic empirical studies (w6nlcS8Kkn, S6cBH99BhB).

The diversity-repetition confound is a real Major weakness that prevents a confident accept — it undermines the paper's most specific headline claim. However, the primary finding (front-loading reasoning creates durable, compounding advantages) is robustly supported by Tables 1–4, and the latent quality effect is a genuine novel observation. The paper is stronger on "what" than "why," but the "what" evidence is credible and the computational investment is real.

**Final Score: 6.0 — Borderline Accept**

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>