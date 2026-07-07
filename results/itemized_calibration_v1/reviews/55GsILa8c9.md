Now let me write the final review.

## Summary

CausalNovo is a model-agnostic framework for de novo peptide sequencing that learns representations invariant to noise-peak perturbations while remaining predictive of the peptide sequence. Building on a Structural Causal Model with independence and sufficiency principles, it introduces a Causality Extraction Module with contrastive and cross-entropy objectives to disentangle causal (signal-related) from non-causal (noise) representations. Experiments on three datasets with three baseline models show consistent improvements at amino acid, peptide, and PTM levels, supported by cross-species validation and attention analysis.

## Strengths

1. **Well-motivated with concrete empirical grounding.** The vulnerability analysis (Figure 1) demonstrates concretely that existing models rely on spurious noise peaks, providing direct motivation for the proposed approach rather than relying on hypothetical reasoning.

2. **Clean, principled formulation.** The SCM (Figure 2A) with two derived principles (independence and sufficiency) gives the method intellectual coherence. The link from the SCM to the learning objectives (contrastive learning for independence, cross-entropy on z_c for sufficiency) is logically traced.

3. **Consistent, multi-dimensional improvements.** Results across three baselines (CasaNovo, AdaNovo, π-HelixNovo), three datasets (Nine-species, Seven-species, HC-PT), and multiple metrics (amino acid, peptide, PTM precision/recall) show broad improvements. The cross-species validation (Table 3) further demonstrates generalization across species.

4. **Attention analysis closing the loop.** Table 7 provides direct evidence that CausalNovo shifts attention toward causal peaks (from 19.26% to 32.87% of predictions fully attending to causal peaks), connecting the claimed mechanism to the observed outcome through an interpretable intermediate.

5. **Honest limitations.** The paper acknowledges the 2.3× training overhead and notes that the evaluation follows the older NovoBench protocol rather than the more realistic out-of-distribution protocol used by recent methods.

## Weaknesses

### Major

1. **Numerical inconsistency in reported results.** The text (line 227) reports improvements that do not match Table 1 in at least two cases:
   - **π-HelixNovo on Seven-species:** Claims +9.1% AA precision improvement, but Table 1 shows †π-HelixNovo at 0.465 and +CausalNovo at 0.536 — a difference of 7.1 pp (not 9.1%).
   - **CasaNovo on HC-PT:** Claims +9.0% improvement, but Table 1 shows †CasaNovo at 0.525 and +CausalNovo at 0.635 — a difference of 11.0 pp (not 9.0%).
   
   Since all other entries in the same paragraph use raw percentage-point differences (verified against the table), these discrepancies suggest either the table values or the text values are wrong. Such errors in flagship results undermine confidence in the reported numbers and must be corrected.

2. **Retrained baselines are materially weaker for some models, inflating reported gains.** The paper retrains all baselines "with the same configurations" (Section 4.1). For AdaNovo and π-HelixNovo, the retrained versions underperform the originally published results: AdaNovo Nine-species drops from 0.698→0.681 (−1.7 pp), π-HelixNovo Seven-species from 0.481→0.465 (−1.6 pp), and π-HelixNovo HC-PT from 0.588→0.532 (−5.6 pp). The paper claims "AdaNovo improves by +6.3% on Nine-species" (0.744 − 0.681), but against the original published AdaNovo (0.698) the gain is +4.6 pp — still positive but materially smaller. Using "same configurations" without per-baseline tuning puts the comparison on unequal footing. The paper should report improvements against both the original published results and the retrained results, and discuss why some retrained baselines underperform.

### Minor

3. **Causal framing is ambitious relative to what the method delivers.** "Causal factors" are operationalized as peaks matching the theoretical spectrum of the ground-truth peptide within a tolerance γ — these are *predictive* of the label but not shown to satisfy stronger causal criteria. The intervention replaces noise peaks as a data augmentation, not a Pearlian do-operation on the data-generating process. The paper is careful to call it a "simulated" intervention (Section 3.3), but the title and abstract imply a stronger causal claim than the method establishes. Reframing as "invariant and sufficient representation learning for robustness to noise" would be more accurate and prevent readers from criticizing the method on grounds it never intended to address.

4. **Gap between the theoretical independence objective and its practical implementation.** The theory (Section 3.3) uses I(z_c; z_c' | Y), but the implementation (Eq. 5) uses a batch-soft contrastive loss where the negative set is "the current training batch (excluding z_c')" without explicit conditioning on Y. This loosens the connection between the claimed theoretical grounding and actual optimization.

5. **Key hyperparameters α and γ not reported in the main text.** The replacement fraction α and m/z tolerance γ are central to the causal intervention (Section 3.4.1) but are not given concrete values. These may appear in the appendix (which was stripped by the parser), but they should be in the main text for reproducibility.

6. **"RI" in Table 6 is misleadingly labeled.** The caption says "RI means the relative improvement," but the values are absolute percentage-point differences (e.g., threshold=1: 0.605→0.689, RI=+8.4%, which is 8.4 pp not the relative improvement of 13.9%). This should be clarified.

7. **Abstract states "up to 10%" improvements, but the body reports improvements of 14.2% (AdaNovo HC-PT AA precision) and 15.1% (π-HelixNovo PTM Seven-species).** The abstract understates the results, which could cause confusion about whether these are relative or absolute improvements.

### Trivial

None.

## Nice-to-Haves

- A non-cumulative ablation (e.g., purification without independence) would more clearly isolate each component's contribution.
- Reporting variance or significance patterns across runs would strengthen confidence in small-margin gains (e.g., 0.4–0.6 pp in some ablations).
- The independence assumption between C and S in the SCM (Eq. 2: C ⟂ S) is asserted without discussion; a brief comment on what violations would mean would strengthen the framing.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Causality enhancement step mechanism is not entirely clear"** — The paper provides a reasonable explanation (adding theoretical peaks preserves causal relationships disrupted by replacement). The criticism is subjective, not a concrete error.
- **"Ablation should use non-cumulative design"** — The cumulative design is standard; this is a suggestion, not a flaw. Moved to Nice-to-Haves.
- **"Statistical significance / variance not reported"** — Single-run benchmark evaluation is the norm in this field. Moved to Nice-to-Haves.
- **General concern about C and S independence assumption** — Standard SCM assumption; the paper is not making strong causal discovery claims. Moved to Nice-to-Haves.
- **Garbled table formatting / parser artifacts** — These are parser issues, not author errors.
- **Questions about existence or availability of cited datasets/models** — Per hard rules, all cited entities are assumed to exist.
- **Missing related works** — Per hard rules, the reviewer cannot confirm the existence of unmentioned works.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the paper's framing and identify numerical and methodological issues but do not uncover fundamentally new dimensions of analysis.

## Suggestions

1. **Correct the two numerical inconsistencies**: π-HelixNovo Seven-species (+9.1% → +7.1 pp) and CasaNovo HC-PT (+9.0% → +11.0 pp), and carefully audit all text-table numbers for consistency.
2. **Report improvements against both originally published and retrained baselines**, and discuss why certain retrained baselines underperform. This is standard practice for fair comparison.
3. **Clarify throughout the paper** that the reported improvements are absolute percentage-point differences (not relative improvements), and fix the "RI" labeling in Table 6.
4. **Report concrete values for α and γ** in the main text.
5. **Consider moderating the causal framing** (e.g., "causality-inspired" or "invariant representation learning") to more accurately reflect what the method establishes — the substantive contribution does not depend on strong causal claims.

## Score and Decision

**Calibration Anchors:** I retrieved and analyzed the following anchor papers from the human-review corpus:

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/nSDOkm0SKo.md | 1.00 | R1-Bracket | No | Irrelevant (financial markets); score band verified as empty of relevant papers |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/gwZ90hFSL2.md | 1.00 | R1-Bracket | No | Irrelevant (humanoid robots) |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5lUdTogEL3.md | 1.00 | R1-Bracket | No | Irrelevant (person re-identification) |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/I2ZYngkRW6.md | 4.25 | R1-Bracket (3.5-5.5) | Yes | Distillation for de novo peptide sequencing; weaker novelty and smaller improvements (1-3%) than CausalNovo; CausalNovo is clearly stronger |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/MeCPwqrm19.md | 4.60 | R1-Bracket (3.5-5.5) | No | Peptide design (not sequencing); different task |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/uQnvYP7yX9.md | 6.50 | R1-Bracket (5.5-7.5) | Yes | **Closest anchor** — ReNovo: de novo peptide sequencing with retrieval; similar empirical rigor and scale; ReNovo has more novel architecture (RAG) while CausalNovo has stronger theoretical framing; both have data/comparison concerns |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/jqmptcSNVG.md | 6.20 | R1-Bracket (5.5-7.5) | No | Peptide design (not sequencing) |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/OzUNDnpQyd.md | 7.00 | R1-Bracket (5.5-7.5) | No | Protein conformation generation; different subfield |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/1iuaxjssVp.md | 7.25 | R1-Bracket (5.5-7.5) | No | Inverse folding for proteins |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/3cuJwmPxXj.md | 8.00 | R1-Bracket (7.5-8.5) | Yes | Causal representation learning theory paper; very different style (theory-heavy, limited experiments); not directly comparable |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/zMPHKOmQNb.md | 8.00 | R1-Bracket (7.5-8.5) | No | Protein generative modeling; different task |

**Round 1 Bracket:** 5.5–7.5 (based on topical similarity to ReNovo at 6.50 and comparison with weaker 4.25 distillation paper).

**Weighted-item comparison against closest anchor (ReNovo, 6.50):** ReNovo's strongest positive items (+4/+5 weights) are its originality (RAG for de novo) and substantial performance improvements. CausalNovo shares the "substantial performance improvement" strength but is weaker on originality since the individual components (contrastive learning, cross-entropy) are standard tools combined in a principled framework. ReNovo's strongest negative items (weight -4) are data leakage concerns and unfair comparison; CausalNovo's retrained-baseline issue is similar in severity but affects fewer models. CausalNovo's attention analysis and honest limitations add credibility that ReNovo's reviews did not highlight as strong points. Overall CausalNovo sits slightly below ReNovo due to lower architectural novelty and the numerical inconsistencies.

**Final calibration:** The paper makes a genuine, well-supported empirical contribution with a clean methodological framework. The two numerical inconsistencies and the retrained-baseline inflation are real issues that need correction, but the core finding — that learning representations invariant to noise-peak perturbations improves robustness and accuracy — is credible and the improvements remain positive even against original published baselines. The paper is clearly written, honestly discusses limitations, and provides mechanistic evidence (attention analysis) uncommon in this literature. This places it solidly at **6.0** — a borderline accept where the contribution is valid but presentation issues need resolution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>