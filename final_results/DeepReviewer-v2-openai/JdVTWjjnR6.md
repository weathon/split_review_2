## Summary
# Final Review Report

## Summary

This paper proposes HiTNet, a hippocampal-thalamic inspired dual-stream network for multimodal sentiment analysis under random frame-level missingness. The core idea is to model two brain mechanisms computationally: (1) hippocampal memory retrieval via a key-value semantic memory module with sparse activation for intra-modal feature completion, and (2) thalamic perceptual regulation via a confidence-perception module and cross-modal completion for inter-modal integration with redundancy suppression.

The paper targets a practically relevant problem (missing data in multimodal sentiment analysis), presents a well-motivated architecture with neuroscience inspiration, and reports experimental results on three benchmarks (MOSI, MOSEI, SIMS) with average accuracy improvements of 1.5–2.0% over baselines. Ablation studies confirm the contribution of each stream and loss component. The method maintains reasonable performance even at 90% missing rate.

However, several concerns limit the current contribution: (1) A critical table error (TETFN results appear incorrectly duplicated between MOSI and MOSEI) undermines the claimed SOTA results until corrected. (2) No statistical significance or variance reporting is provided for the relatively small performance gains. (3) The confidence-perception module conflates "completeness" (missing ratio) with "reliability," which weakens the thalamic inspiration claim. (4) The semantic memory module populates its store from corrupted inputs, raising questions about retrieval quality. (5) Loss naming is inconsistent across text, equations, and tables. (6) Because external literature retrieval was unavailable, novelty claims require manual verification.

Overall, the paper presents a thoughtful architectural contribution with promising empirical results, but the above issues must be addressed before the findings can be fully relied upon.

## Strengths
**S1. Well-motivated neuroscience-inspired architecture.** The dual-stream design (hippocampal intra-modal completion + thalamic inter-modal regulation) is grounded in specific neuroscientific mechanisms: pattern completion via associative memory and multisensory integration with gating. This is more than a loose analogy; the authors connect each biological function to a concrete computational module (key-value memory with cosine retrieval for hippocampus; confidence estimation with weighted fusion for thalamus).

**S2. Addresses a practically important but underexplored problem.** Random frame-level missingness across all modalities is a realistic deployment scenario that has received less attention than modality-level missingness. The paper correctly identifies that existing cross-modal consistency methods neglect residual intra-modal cues and lack reliability assessment.

**S3. Comprehensive evaluation across three benchmarks.** Experiments cover MOSI (English, ~2k), MOSEI (English, ~23k), and SIMS (Chinese, ~2k), providing multi-language and multi-scale validation. The missing-rate sweep (0% to 90%) systematically tests robustness under varying data degradation levels.

**S4. Strong performance under extreme missingness.** Maintaining 72.20% accuracy at 90% missing rate on MOSEI is a practically meaningful result, suggesting the dual-stream completion mechanism provides genuine resilience beyond what simple imputation would achieve.

**S5. Thorough ablation analysis.** The study ablates both architectural components (SMM, CPM, Intra stream, Inter stream) and loss terms (L_ubl, L_cp, L_rec), showing that each contributes non-trivially. The completion visualization (Figure 4) and confusion matrices (Figure 5) provide complementary qualitative evidence.

**S6. Code and reproducibility commitment.** The anonymous repository and detailed implementation parameters (architecture dimensions, learning rate, batch size, seed count) support reproducibility.

## Weaknesses
**W1. [CRITICAL] Table 1 data error — TETFN MOSEI results appear duplicated from MOSI.** In Table 1, the TETFN row for MOSEI shows Acc-7=30.30, Acc-2=69.76/67.68, F1=65.69/63.29, MAE=1.087, Corr=0.508. These values are virtually identical to the MOSI column for the same method (Acc-7=30.30, Acc-2=69.76/67.68, F1=65.69/63.29, MAE=1.087, Corr=0.507). Since MOSEI is ~10x larger than MOSI, identical performance is highly implausible. This strongly suggests a copy-paste or table layout error. If TETFN results for MOSEI are incorrect, the claimed SOTA improvements (Section 4.4) must be recomputed. *Severity: Critical. Fixability: High (correct the table and re-run comparisons).*

**W2. [MAJOR] No statistical significance or variance reporting.** The paper reports average results over 3 seeds but never reports standard deviations, confidence intervals, or significance tests. Many improvements are small (Acc-2 gain: 1.31%, F1 gain: 1.41%). Without variance, readers cannot assess whether the observed gains are statistically reliable or could arise from seed variation. The claim of "substantial 2.56% gain in Acc-7 on MOSEI" is also ambiguous (absolute vs relative). *Severity: Major. Fixability: High (add std to tables, report p-values for key comparisons).*

**W3. [MAJOR] Confidence-perception module conflates completeness with reliability.** The CPM is trained to predict $s_m$ against $1 - r_m$ (missing ratio inverted), meaning it learns to estimate *data availability* rather than *signal reliability*. A modality with low missing ratio may still be uninformative (e.g., static visual frame), while a high-missing-ratio modality may carry strong sentiment (e.g., a single critical word). Using $s_m$ as the confidence weight in Equations 9-10 may therefore not achieve the claimed "filtering of high-quality cues." The module name and narrative overstate what the supervision signal supports. *Severity: Major. Fixability: Medium (rename module to "completeness estimation" or re-target supervision on actual reliability).*

**W4. [MAJOR] Semantic memory module is populated from corrupted inputs.** The memory keys and values are derived from $x_m$ (mean-pooled and projected from the incomplete input). This means the memory store encodes corrupted patterns. When a query (also corrupted) retrieves a memory that was stored from similarly corrupted data, the "completion" may reinforce missing patterns rather than reconstructing clean content. The residual gating mechanism (Eq. 3) may not fully compensate because the gate is learned from the same corrupted representation. *Severity: Major. Fixability: Medium (use original complete features $u_m$ for memory population while keeping $x_m$ as query).*

**W5. [MAJOR] Loss naming inconsistency across text, equations, and tables.** The utilization balance loss is introduced as $\mathcal{L}_{\text{ubl}}$ in Eq. (6). In the ablation text (line 119) it appears as $\mathcal{L}_{ubi}$. In Table 3, the row is labeled "w/o \<math\>L_{abs}\</math\>" (unclear rendering). Additionally, Table 3 contains a row "w/o $L_{enc}$" that is never defined in the optimization objective (Eq. 15), likely referring to $\mathcal{L}_{rec}$. These inconsistencies create confusion about which ablation condition corresponds to which loss. *Severity: Major. Fixability: High (unify naming across all locations).*

**W6. [MODERATE] Novelty claims require external verification.** Due to the unavailability of external paper search in this run, novelty claims (brain-inspired dual-stream for missing data, semantic memory with residual gating, confidence-guided cross-modal completion) cannot be verified against the existing literature. The paper's positioning relative to the closest related work (key-value memory networks, brain-inspired multimodal methods, incomplete multimodal learning) should be manually verified by the authors with explicit head-to-head comparisons. *Severity: Moderate (conditional). Fixability: High (provide literature comparison).*

**W7. [MODERATE] TETFN results on {V} and {A} modality-level missing are identical.** Table 4 shows TETFN achieving exactly 55.25% Acc-2 for both {V} alone and {A} alone. While the value itself is plausible, identical results across modalities that have different dimensionalities and information content is suspicious and may indicate a default fallback behavior. *Severity: Moderate. Fixability: Medium (verify TETFN implementation for single-modality input).*

**W8. [MINOR] Introduction lacks citation support for the claim that frame-level missingness is harder than modality-level missingness.** The statement (Page 1 line 8) that frame-level missingness "is more complex, causing fragmented emotional cues and discrepancies in data quality, making sentiment analysis more challenging" is presented without supporting evidence or references. *Severity: Minor. Fixability: High (cite prior empirical comparison or remove the comparative claim).*

**W9. [MINOR] Conclusion introduces an unsupported future direction (classification imbalance).** The future work paragraph mentions "addressing classification imbalance" without any prior analysis of class imbalance in the paper. This appears disconnected from the paper's content. *Severity: Minor. Fixability: High (replace with a grounded future direction or add imbalance analysis).*

**W10. [MINOR] Related work sections read as paper lists rather than structured comparisons.** The MSA related work paragraph follows a paper-by-paper chronological listing. This reduces the persuasive power of the novelty positioning. The brain-inspired paragraph (2 sentences) is too brief to establish the gap. *Severity: Minor. Fixability: High (restructure by comparison axes, expand brain-inspired coverage).*

**W11. [MINOR] Completeness visualization analyzed at only one missing rate (90%).** The completion distance analysis (Section 4.6) would be more convincing with multi-rate analysis showing monotonic improvement as missing rate decreases. *Severity: Minor. Fixability: High (add 10%/50% rates).*

## Score
**Final Score: 5.5/10**

**Rationale:** The paper addresses a practically important problem (frame-level missingness in multimodal sentiment analysis) with a thoughtfully designed neuroscience-inspired architecture. The dual-stream concept is compelling, and the experimental scope (three benchmarks, comprehensive missing-rate sweep) is commendable. However, several issues prevent a higher score in the current version:

1. **Critical data integrity concern (W1):** The apparent duplication of TETFN results between MOSI and MOSEI in Table 1 undermines confidence in the reported comparisons. Until corrected and verified, the claimed SOTA improvements cannot be fully trusted. This alone precludes a score above 6.

2. **Statistical reliability gap (W2):** The absence of variance reporting and significance tests for small-margin improvements (1.3–1.4% in key metrics) makes it impossible to assess whether the observed gains are robust.

3. **Design-evidence mismatch (W3, W4):** Two core design choices (confidence target conflating completeness with reliability; memory populated from corrupted features) weaken the claimed mechanisms. These are fixable but indicate that the current empirical support overstates what the architecture actually achieves.

4. **Novelty unverifiable (W6):** External literature verification was unavailable in this run; novelty claims require manual author verification.

**Post-Revision Target: [6.5, 7.5]/10**

The paper has clear potential to reach a higher score if the following are addressed: (a) correct Table 1 and re-verify all baseline comparisons; (b) add variance/std and significance tests; (c) clarify the confidence module's actual supervision target and adjust claims accordingly; (d) fix the memory population strategy; (e) unify loss naming; (f) provide external literature positioning.

**Scoring breakdown (current):**
- Research value / problem importance: 7/10
- Novelty / conceptual contribution: 6/10 (deferred literature verification)
- Methodological soundness: 5/10 (critical table error, design mismatches)
- Empirical support / evidence strength: 4/10 (no variance, single-rate completion analysis)
- Reproducibility / clarity: 6/10 (good implementation details but naming inconsistencies)
- Writing / presentation: 6/10 (clear motivation but related work structure weak)