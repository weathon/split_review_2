## Summary

CausalNovo proposes a model-agnostic framework for de novo peptide sequencing that uses a Causality Extraction Module (CEM) with contrastive learning objectives to make models attend to signal fragment ions (b/y/a) rather than noise peaks. The method is evaluated on three baseline models (CasaNovo, AdaNovo, π-HelixNovo) across three benchmark datasets, showing consistent improvements of up to 10–14% at amino acid, peptide, and PTM levels. Extensive analysis (attention matrices, NSR generalization, ablation studies) provides mechanistic evidence for why the approach works.

## Strengths

- **Clear and empirically grounded problem framing (Section 1, Figure 1).** The vulnerability analysis demonstrates that existing models' performance degrades systematically when noise peaks are perturbed, and this degradation worsens as the m/z tolerance threshold tightens. This characterization of an important failure mode is a genuine contribution in its own right.

- **Consistent and substantial empirical gains across diverse settings (Tables 1–3, Figures 3–4).** Improvements of up to ~10% on Seven-species and HC-PT are non-trivial in this domain. Gains hold across all three baseline models, all three datasets, and all three evaluation levels (amino acid, peptide, PTM). Cross-species validation (Table 3) shows gains in all 8 individual species, indicating the effect is systematic rather than dataset-specific.

- **Model-agnostic design with demonstrated generality.** The CEM attaches to an existing encoder without changing the core architecture. Demonstration on three distinct recent architectures (CasaNovo, AdaNovo, π-HelixNovo) is more convincing than proposing yet another monolithic model.

- **Rich mechanistic analysis beyond headline numbers.** The attention analysis (Table 7) shows CausalNovo increases attention to all 3 causal peaks from 19.26% to 32.87%, providing direct evidence of *why* the method works. NSR generalization (Figure 4) and peak-distinguish-strategy analysis (Table 6) further validate robustness.

- **Honest self-assessment of limitations (Section 5).** The paper acknowledges the 2.3× training time increase and notes that evaluation follows the NovoBench protocol rather than the more realistic protocol used by recent methods, which is commendable.

## Weaknesses

### Major

- **Significant gap between information-theoretic objectives and their practical implementation (Section 3.3–3.4).** Two specific problems:
  - *Independence objective.* The paper claims to maximize I(z_c; z_c' | Y) (Eq. 5), but the implementation is a standard contrastive loss where positive pairs share the same original spectrum (hence same Y) and negatives are other batch samples. There is no explicit conditioning on Y in the loss — it is a data-augmentation consistency loss, not a conditional mutual information estimator. The paper does not discuss why this approximation is valid or compare against a proper conditional variant.
  - *Purification objective.* The paper trains z_s (the "non-causal" representation) to also predict Y by maximizing I(z_s; Y), claiming this "indirectly leads to purification of z_c." The mechanism is not convincingly justified — training the non-causal pathway to predict the label seems to undermine the separation the framework is designed to achieve. The explanation (lines 97) references prior work without clarifying the local mechanism, and the ablation (Table 4) conflates purification with other components.

- **The causal framing overreaches relative to what the method actually does (Sections 1, 3.1–3.2).** The paper presents an SCM with causal factors C and non-causal factors S, and uses language of causal interventions (do-operator). In practice, the identification of "causal" vs. "non-causal" peaks requires the ground-truth label Y: peaks are labeled as causal if they match b/y/a ions from the theoretical spectrum computed from Y (Eq. 4). This is not causal discovery or causal representation learning — it is applying well-established fragmentation chemistry to supervise attention, which the paper itself acknowledges (lines 109). The SCM provides a useful organizing metaphor, but the method is more accurately described as "domain-knowledge-guided attention weighting with contrastive consistency training." The paper would be equally compelling under that honest framing.

### Minor

- **No statistical significance or variance reporting.** None of the tables report standard deviations or confidence intervals over multiple runs. Given that several improvements are modest (e.g., +0.4% in the ablation, +2.2% on Nine-species amino acid precision), the reader cannot assess whether these differences are reliable or within run-to-run variance. This is a notable omission for an empirical paper.

- **Retrained baseline discrepancies are not discussed.** Retrained CasaNovo (0.741) is 6.3% *higher* than the published value (0.697) on Nine-species, while AdaNovo retrained (0.681) is 2.4% lower than published (0.698). The paper states baselines are retrained "with the same configurations" but does not discuss whether these configurations might advantage or disadvantage any method. The large gains on Seven-species (e.g., +12.0% over †CasaNovo) occur on a dataset where even the retrained baseline (0.357 AA precision) far underperforms SearchNovo (0.488), suggesting the baseline may operate in a regime where large gains are relatively easy.

- **Evaluation protocol limitation.** The paper acknowledges (Section 5) that evaluation follows the NovoBench protocol, whereas recent methods (ContraNovo, RankNovo) adopt a more realistic protocol training on large-scale corpora and evaluating on out-of-distribution test sets. This means the reported gains may not directly transfer to the evaluation setup the community is moving toward.

### Trivial

- None.

## Nice-to-Haves

- Test on at least one non-Transformer architecture (e.g., DeepNovo's CNN) if claiming model-agnosticism, or qualify the claim to Transformer-based models.
- Provide a clearer justification for why the contrastive loss approximates conditional mutual information, or rename it to what it is — a data-augmentation consistency loss.
- A direct comparison of "with purification" vs. "without purification" broken out more clearly in the ablation (the current design conflates purification with other components).

## Removed Points

These points were identified by reviewers but are removed per the filtering rules:

1. **Figure 2 caption inconsistency ("charge state" vs "causal factors").** This is a parser artifact from embedded image alt-text — the paper's text consistently defines C as causal factors. Not a paper error.
2. **Table 4/5 rendering issues (all checkmarks).** Parser artifact; the text description clarifies the ablation structure.
3. **"Statistical nature" criticism is strawmannish.** Opinion-based characterization, not a substantive weakness.
4. **Criticism about missing appendix content or references.** Parser strips these from all papers; they exist in the original submission.

## Novel Insights

The attention analysis (Table 7) provides genuinely insightful evidence that transcends the usual "our method is better" reporting: CausalNovo increases the proportion of predictions attending to all 3 causal peaks from 19.26% to 32.87%, while reducing completely non-causal attention from 12.73% to 10.76%. The correction-case analysis (Appendix Table 14) showing that the baseline fails to attend to causal peaks in 14.18% of incorrect predictions, while CausalNovo reduces this to 5.44%, concretely demonstrates the mechanism by which the method improves accuracy. The vulnerability analysis (Figure 1) establishing that existing models systematically degrade under noise peak perturbation is also a valuable empirical contribution.

## Suggestions

1. **Tone down the causal framing.** The SCM can remain as motivation, but describe the method as "using domain knowledge (fragmentation chemistry) to generate a supervised attention mask, with contrastive consistency training between original and noise-replaced spectra." Drop or qualify the causal discovery / causal representation learning language.
2. **Report standard deviations** over 3–5 runs with different seeds for all main tables.
3. **Clarify the independence objective.** Either justify why the contrastive loss approximates I(z_c; z_c' | Y), or rename it and frame it as a data-augmentation consistency loss on its own terms.
4. **Clarify or remove the purification objective.** Provide a clearer argument for how training z_s to predict Y purifies z_c, or remove the component if the ablation shows negligible impact.
5. **Discuss retrained baseline discrepancies** explicitly. Show that each baseline's own optimal hyperparameters produce similar results, or acknowledge the limitation.
6. **Run at least one small-scale comparison** under the ContraNovo/RankNovo evaluation protocol, or discuss more thoroughly why gains are expected to transfer.

## Calibration Report

**Anchors retrieved:**

| Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| uQnvYP7yX9.md (ReNovo) | 6.50 | R1 | Yes | Stronger positive weights (+5.5 vs +4.7) and accepted; CausalNovo's negatives (-5.5, -4.6) are less severe than ReNovo's missing related work (-8.3) and missing comparison (-6.4) |
| 87B3zDRMjv.md (RankNovo) | 5.50 | R1 | Yes | RankNovo had modest improvements (3.7% pep recall) vs CausalNovo's much larger gains (up to 14%); both share computational cost concerns. RankNovo rejected. |
| I2ZYngkRW6.md (Distilling NAT) | 4.25 | R1 | Yes | Engineering-heavy with limited novelty; CausalNovo has stronger method contribution |
| OGtnhKQJms.md (Multi-view CRL) | 7.00 | R1 | Yes | Purely theoretical causal representation learning paper with strong theory; not directly comparable |
| cbFqqtJGtA.md (Causal CDN) | 4.25 | R2 | Yes | Rejected for causal overclaiming (-4.38) and marginal contribution (-8.96); CausalNovo's causal overclaim is less severe and its method contribution is stronger |
| 7Fh57rIpXT.md (Causal AS) | 3.67 | R2 | Yes | Rejected for limited novelty (-9.66) and poor presentation; CausalNovo is substantially stronger |
| lQYi2zeDyh.md (Amortized CD) | 5.00 | R2 | Yes | Rejected for limited scope; CausalNovo has broader empirical validation |
| jqmptcSNVG.md (PepHAR) | 6.20 | R1 | No | Peptide design paper; different task |
| 78tc3EiUrN.md (MADGEN) | 6.00 | R1 | No | Molecular generation; different task |
| G1r2rBkUdu.md (Synergy CRL) | 6.00 | R2 | No | Theoretical CRL; not comparable |
| MeCPwqrm19.md (SurfFlow) | 4.60 | R1 | No | Peptide design; different task |
| kz5igjl04W.md (CDEV) | 5.50 | R2 | No | Causal inference in animal communication; not comparable |

**Round-1 bracket:** Plausible score range is 4.5–6.5. The paper is clearly stronger than the Causal CDN (4.25) and Distilling NAT (4.25) anchors — its method contribution is more substantial and its empirical validation is more thorough. It is weaker than ReNovo (6.50) whose positive weights (+5.5) substantially exceeded CausalNovo's (+4.7). The closest comparison is RankNovo (5.50, rejected) — CausalNovo has larger improvements but struggles with a causal overclaiming issue that RankNovo didn't have.

**Final calibration:** My draft's heaviest positive items (+4.69 for empirical gains, +4.54 for mechanistic analysis, +4.43 for model-agnostic design) are comparable to RankNovo's strongest positive (+4.54) but well below ReNovo's (+5.66). My heaviest negative items (-5.46 for info-theoretic gap, -4.64 for variance reporting) are significant but not fatal — the method itself is valid and the results are strong. The causal framing overclaim weakness (-1.43) reduces credibility but is less severe than the Causal CDN paper's analogous criticism (-4.38). On balance, the paper sits between the RankNovo (5.50, reject) and ReNovo (6.50, accept) anchors, closer to RankNovo due to the framing and rigor concerns.

**Final score: 5.5** — borderline reject. The paper has genuine contributions (the method is sound and empirically well-supported) but the causal framing overreaches, the gap between theoretical objectives and practical implementation is not acknowledged, and the lack of variance reporting weakens confidence in the modest effect sizes. With substantial revisions addressing these issues, the paper could be a borderline accept.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>