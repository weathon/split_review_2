Here is the final consolidated review.

---

## Summary

This paper proposes **Steady Thought (ST)**, a three-stage framework (entropy-based thought segmentation → logit-suppressed thought completion → thought-level preference optimization) to mitigate the "under-thinking" problem in Large Reasoning Models, where models abandon promising reasoning trajectories prematurely. ST constructs preference pairs at the granularity of individual thoughts rather than whole responses and uses a SimPO-derived loss (STPO) to train models to commit to promising reasoning paths. Experiments across three model sizes (1.5B–14B) and four benchmarks show accuracy gains of up to 5.3% alongside token reductions of 19–39%.

---

## Strengths

- **Consistent results across model scales and datasets.** Table 1 shows accuracy improvements and token reductions for all three model sizes (1.5B, 8B, 14B) across all four benchmarks, including on LiveCode — an out-of-distribution coding benchmark from models trained only on math data (lines 148–149). This consistency suggests genuine learning of a more general reasoning pattern rather than dataset-specific overfitting.

- **Mechanistic evidence supports the claimed mechanism.** Table 2 shows that the proportion of correct intermediate thoughts (PCT) drops after ST training (e.g., from 54.9% to 40.4% for the 1.5B model on MATH-500, and from 14.5% to 7.9% on AIME 2024). This is direct evidence that the model abandons promising thoughts less often after ST training.

- **The method pipeline is coherent and well-structured.** The three-stage design (entropy-based segmentation → logit-controlled completion → thought-level preference optimization) forms a logical chain from data construction to training. The shift from holistic preference optimization to thought-level granularity (Section 3.3) is a reasoned response to the known limitation that holistic PO discards valuable correct intermediate reasoning.

- **Ablation study isolates the value of preference-level supervision.** Table 4 compares STPO against SFT and DPO using the same preference pairs. SFT on the chosen responses hurts accuracy (80.4% vs. 82.2% on MATH-500), while STPO preserves or improves accuracy while cutting tokens. This cleanly demonstrates that the benefit comes from the preference-style learning signal, not just exposure to shorter completions.

---

## Weaknesses

### Major

- **The NOWAIT baseline results are anomalous and indicate a broken implementation.** For Qwen3-8B on MATH-500, NOWAIT achieves 61.0% accuracy vs. Vanilla's 91.4% (a **−30.4 point drop**), and tokens increase to 13,274 from 4,724 (**+181%**). Since NOWAIT suppresses reflection keywords to *reduce* switching, a 181% token increase is inconsistent with a working implementation. Similar catastrophic degradations occur for Qwen3-8B on GSM8K (−22.3 pts) and for DeepSeek-R1-Distill-Qwen-14B on AIME 2024 (−26.6 pts). No suppression hyperparameters or configuration details are provided. This comparison cannot be interpreted as evidence — the claim that ST "outperforms existing suppression methods" is not supported by this baseline. (The comparisons against Vanilla and SEAL are unaffected.)

### Minor

- **No statistical variance is reported despite running multiple trials.** The paper states it averaged 8 runs for AIME 2024 (30 problems) and 2 runs for LiveCode (line 143), yet no standard deviations, confidence intervals, or significance tests are provided anywhere. For a 30-problem test set, a 3–4 point gain can correspond to roughly one additional correct answer — without variance, the reader cannot assess whether these gains are signal or noise.

- **The AIME 2024 1.5B results partially conflict with the "steady thinking" narrative.** For DeepSeek-R1-Distill-Qwen-1.5B on AIME 2024, the average number of thoughts increases from 12.87 to 18.21 (+41%) after ST training (Figure 2). The paper explains this as productive exploration on hard problems (line 219), but the mechanistic analysis in Table 2 reports only proportions (PCT), not absolute counts of correct intermediate thoughts. Since the denominator changes (more total thoughts), the PCT drop from 14.50% to 7.90% could partly reflect dilution rather than fewer abandoned correct thoughts. Reporting absolute counts alongside proportions would resolve this ambiguity.

### Trivial

- **Table 1 column headers use downward arrows (↓) for both Acc and Tokens.** Accuracy should use ↑ (higher is better) while tokens use ↓ (lower is better). This is a presentational inconsistency.

---

## Nice-to-Haves

- Provide absolute counts (not just proportions) for the correct intermediate thoughts analysis in Table 2.
- Include a controlled experiment comparing ST against a method that achieves similar token reduction through a different mechanism, to strengthen the claim that the benefit is specifically from "steadier thinking" rather than length reduction.
- Clarify the distinction between the paper's training-time logit suppression (Stage 2) and the inference-time suppression used by NOWAIT/SEAL. The paper criticizes global suppression while using it internally for data generation — the distinction is valid but could be articulated more precisely.

---

## Removed Points

These points were raised in the input reviews but are either factually incorrect, parser artifacts, scope creep, or noise:

1. **"The scatter plots are difficult to interpret"** — formatting nitpick; removed.
2. **"Entropy-based segmentation is not novel"** — the paper's contribution is the full pipeline (segmentation + completion + thought-level PO), not just entropy-based segmentation; removed as scope creep.
3. **"Computational cost of Stage 2 deserves more discussion"** — the paper references Appendix E for this (line 103), which is stripped by the parser; the original submission likely addresses it. Removed.
4. **"Missing training data size and cost"** — same parser artifact issue (appendix content stripped).
5. **"Confounding effect of length reduction"** — the PCT analysis in Table 2 already addresses this concern by measuring intermediate thought correctness directly. Removed.
6. **Strengths about the problem being "important" or the paper being "well-written"** — generic; removed per filtering rules.
7. **Criticism about "ST uses logit suppression it criticizes" elevated to structural** — the paper's distinction (training-time data generation vs. inference-time method) is real and legitimate; demoted to Nice-to-Haves.
8. **"No statistical significance" labeled as evidential/structural** — the paper does run multiple trials, making this a reporting gap rather than a methodology flaw; downgraded to Minor.

---

## Novel Insights

None beyond the paper's own contributions. The key insight — that thought-level rather than holistic preference pairs can teach models to commit to promising reasoning paths — is the paper's own contribution, and neither reviewer offered a novel reframing of it.

---

## Suggestions

1. **Fix or honestly characterize the NOWAIT comparison.** Either tune the suppression strength to produce reasonable results (and document the tuning process) or, if NOWAIT's code does not support these models, remove it and compare primarily against Vanilla and SEAL, which are clean.
2. **Add standard deviations** to all reported results, especially for AIME 2024 where the test set has only 30 problems.
3. **Report absolute counts of correct intermediate thoughts** alongside the proportion metric in Table 2, to clarify whether the PCT decrease genuinely reflects fewer abandoned correct thoughts.
4. **Reconcile the AIME 2024 anomaly (1.5B model, +41% thoughts)** with the paper's mechanistic claims, or hedge the scope of the "steady thinking" narrative for this specific setting.

---

## Score and Decision

### Calibration

**Round 1 bracket:** I retrieved anchor papers from six score bands (0–1.5, 1.5–3.5, 3.5–5.5, 5.5–7.5, 7.5–8.5, 8.5+). The most topically similar anchors fell in the 5.5–7.5 band:

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| TPO (preference opt. for reasoning) | O0sQ9CPzai.md | 6.33 | 1,2 | Yes | Similar contribution type; TPO had noisy data (-9.76) and heuristic reward (-9.96) as decisive weaknesses, with strong motivation (+9.93) and code release (+10.00) as strengths. Comparable to this paper's one decisive weakness (-10.00 for NOWAIT) and two decisive strengths (+10.00, +9.99). |
| Overthinking the Truth | Tigr1kMDZy.md | 7.33 | 1 | Yes | Higher-scored analysis paper; its weaknesses were about scope limitations (-6.54) rather than methodology problems. Not directly comparable in contribution type. |
| Mind Your Step (CoT harms) | rpbzBXdo4x.md | 5.00 | 1 | Yes | Rejected; multiple decisive weaknesses (-10.00, -9.99, -9.99) and framing issues. This paper's core evidence is stronger. |
| TypedThinker (typed reasoning) | VIUisLx8lQ.md | 6.00 | 2 | Yes | Accepted; had lack of novelty (-10.00), marginal gains (-9.95), and complex pipeline (-9.81) as decisive weaknesses. Received one 8 and three 5/6 scores. |
| RouteLLM (learning to route) | 8sSqNntaMr.md | 6.33 | 2 | Yes | Accepted; had missing baselines (-9.97, -9.99) as decisive weaknesses but strong cost savings evidence (+9.90, +9.67). |
| General Preference Modeling | xS4XOS4NQ5.md | 5.00 | 1 | No | Rejected; less topically similar. |
| Supervised Chain of Thought | pXIbcRPxWR.md | 2.50 | 1 | No | Rejected; not topically similar. |

**Round 1 bracket:** 5.5–6.5.

**Round 2 narrowing:** Comparing itemized impact scores, this paper's profile (one decisive weakness at -10.00, but two decisive strengths at +10.00 and +9.99, plus a strong +8.63) places it closer to the TPO (6.33) and RouteLLM (6.33) anchors than to Mind Your Step (5.00, rejected) or TypedThinker (which had three decisive weaknesses). Unlike TypedThinker's three decisive weaknesses and marginal gains critique, this paper's single decisive weakness (NOWAIT baseline) is fixable and does not affect the core Vanilla and SEAL comparisons. The paper's strongest positive evidence (consistent multiscale results at +10.00, mechanistic evidence at +9.99) is comparable to RouteLLM's cost-saving evidence (+9.90, +9.67) and TPO's code release (+10.00).

**Final score: 6.0** — borderline accept. The NOWAIT issue needs to be addressed, but the core contribution (thought-level preference optimization for under-thinking) is well-motivated, methodologically sound, and supported by evidence that goes beyond what the broken baseline affects.

### Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>