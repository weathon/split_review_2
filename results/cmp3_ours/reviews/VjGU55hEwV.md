## Summary

RLIE is a framework that combines LLM-generated natural-language rules with probabilistic modeling (elastic-net regularized logistic regression) for rule learning. The pipeline has four stages: (1) LLM generates candidate rules from training samples, filtered by coverage; (2) logistic regression learns probabilistic weights for global selection and calibration; (3) error-driven iterative refinement using hard examples; (4) evaluation comparing direct linear-only inference (E1) against three LLM-injection strategies (E2–E4). The key finding is that the simple linear combiner (E1) consistently outperforms injecting rules back into the LLM (E2–E4), supporting a "division of labor" thesis where LLMs handle local semantic judgments and a probabilistic combiner handles global aggregation.

## Strengths

1. **Well-motivated framework design.** Combining LLM-generated natural-language rules with a probabilistic combiner (logistic regression with elastic net) directly addresses a genuine gap: existing LLM-based rule learning either refines a single rule (IO Refinement) or maintains independent rules without principled global aggregation (HypoGeniC). The four-stage pipeline is logically coherent and each stage serves a clear purpose.

2. **Thoughtful hierarchical evaluation strategy (E1–E4).** The layered comparison of Linear-only, LLM+Rules, LLM+Rules+Weights, and LLM+Rules+Weights+Linear Prediction cleanly isolates what information helps or hurts when rules are injected back into an LLM. The finding that E1 outperforms all LLM-injection strategies is a clean, honestly reported empirical result that supports the paper's "division of labor" thesis.

3. **Honest reporting of null/negative results.** The paper does not suppress the fact that LLM+weights strategies (E2–E4) underperform the simple linear combiner, nor does it claim the finding was expected. It acknowledges that IO Refinement sometimes outperforms RLIE and offers a plausible explanation (single-rule generalizability vs. multi-rule expressiveness).

## Weaknesses

### Fatal
None.

### Major

1. **Standard deviations promised but absent.** Section 4.3 states: *"Each experiment was repeated at least three times, and we report the mean and standard deviation of the results."* Neither Table 1 nor Table 2 reports any standard deviations or any variance measure whatsoever. The text then claims that RLIE "maintains stability" and that baselines "exhibit high variance and instability" (Section 5.1) — claims that are not just unsupported but contradicted by the paper's own stated reporting standard. Without variance estimates, the reader cannot assess whether reported differences between methods are meaningful or within experimental noise. This is an evidential gap that cuts across the entire experimental section.

2. **No proper component-level ablation despite claiming one.** Section 5 states: *"we conduct an ablation study on different inference strategies."* Comparing four ways to use the *final* rule set (E1–E4) is not an ablation of the framework's components. A proper ablation would isolate the contributions of: (a) iterative refinement vs. one-shot generation, (b) elastic-net logistic regression vs. simpler aggregation (e.g., majority voting or unweighted logical OR), (c) the coverage-based filtering threshold γ, and (d) the capacity limit H. Without these, we cannot determine which components of RLIE actually drive its performance.

### Minor

3. **No qualitative examples of generated rules in the main paper.** The paper claims interpretability, knowledge discovery, and "human-AI consensus" (Contributions, point 3) as key contributions. Yet the main paper body contains zero examples of rules, their learned weights, their coverage, or how rule sets evolve across iterations. While Appendix B is referenced for a case study, the absence of concrete examples in the main text weakens the substantiation of the interpretability and knowledge discovery claims.

4. **LoRA baseline uses a drastically smaller model.** LoRA Finetune uses Qwen3-8B while RLIE's main results use Qwen3-235B and DeepSeek-V3 (both orders of magnitude larger). The table caption notes *"LoRA achieves high scores on simple tasks but fails to generalize on complex reasoning tasks,"* but including this comparison in the main table without clearly separating model-scale effects from method effects is potentially misleading. On Reviews, LoRA achieves 94.1 vs. RLIE's 71.5 — a gap attributable to model size, not method quality.

5. **Inconsistent model naming between tables.** Table 1 lists the backbone as "DeepSeek-V3"; Table 2 lists "DeepSeek V3.2." If these refer to different models or different versions, the results are not directly comparable across tables. If they are the same model, the inconsistent naming is confusing. This needs clarification.

### Trivial

6. **Figure 1 "Update" arrow not explained in method text.** A red arrow labeled "Update" points from Evaluation back to Rule Generation in Figure 1. This is described in the figure caption as indicating *"an iterative cycle"* but is never explained in the Section 3.4 text. The iterative refinement described in Section 3.3 already covers the inner cycle of generation → regression → refinement → re-generation. If the arrow from Evaluation back to Generation represents an additional outer loop, this needs explicit description; otherwise it should be clarified or removed from the figure.

## Nice-to-Haves

- Sensitivity analysis on key hyperparameters (capacity H=10, coverage threshold γ=0.2, hard-example count k=20) would strengthen robustness claims.
- Computational cost disclosure: each test prediction requires running the LLM once per rule per sample to obtain the ternary judgment z_{i,j}, plus a logistic regression forward pass. With H=10 rules and ~300 test samples, this is ~3000 LLM judgment calls per evaluation.
- Extending the ablation to isolate iterative refinement vs. one-shot generation would directly strengthen the central claim about the framework's design.

## Removed Points

- **Criticism about missing appendix content (case study in Appendix B):** The parser strips appendices; the paper references Appendix B for case studies. This concern cannot be fairly evaluated from the main text alone. Removed per hard rule.
- **Criticism that different LLMs are used (gpt-4o-mini for judgment vs. Qwen3/DeepSeek for backbones):** The paper's framework is designed to work with any LLM for judgment calls; this is a design choice, not a flaw. Removed as misunderstanding.
- **"Evaluation numbers should be interpreted with small dataset size in mind":** Generic concern applicable to many papers, not a specific identified weakness.
- **"Temperature set to 1×10⁻⁵ not truly deterministic":** Generic nitpick about LLM API behavior, not a meaningful weakness in this context.
- **"E3/E4 include LLM's own rule judgments creating circularity":** This is the deliberate design of the experiment, testing whether providing more information to the LLM helps. Not a flaw.
- **Criticism about HypoGeniC framing in introduction:** The paper correctly distinguishes its contribution (adding probabilistic weighting to multi-hypothesis sets); the distinction from prior work is accurate. Removed as not a genuine weakness.
- **"The central finding (E1 outperforms E2–E4) is not surprising":** Subjective opinion rather than a verifiable weakness.
- **"Could random sampling of hard examples work as well?":** Valid ablation question but framed as a demand rather than a suggestion. Moved to Nice-to-Haves.

## Novel Insights

The reviews surface a useful observation not explicitly discussed in the paper: the E3 and E4 evaluation strategies effectively ask the LLM to reason about its own previous outputs (since the rules being injected were generated by the same LLM). This potential self-referential bias is not discussed as a limitation, though it does not invalidate the E1 finding (the linear combiner avoids this issue entirely). Beyond this, the reviews do not contribute new analytical perspectives beyond what the paper already states about the division of labor between LLMs and probabilistic combiners.

## Suggestions

1. Add standard deviations (or confidence intervals) to Tables 1 and 2. If the three runs produced near-identical results, state this explicitly.
2. Add a proper component-level ablation: compare the full RLIE against (i) one-shot rule generation without iterative refinement, (ii) majority-vote or unweighted aggregation instead of elastic-net logistic regression, (iii) varied coverage thresholds γ and capacity limits H.
3. Include 2–3 concrete examples of generated rules with their learned weights and coverage statistics in the main paper to substantiate the interpretability claims.
4. Clarify whether "DeepSeek-V3" (Table 1) and "DeepSeek V3.2" (Table 2) are the same or different models.
5. Explain the "Update" arrow from Evaluation back to Rule Generation in the method text, or remove it from the figure.

## Score and Decision

**Calibration Anchors (All Rounds):**

| Path | Avg Score | Round | Comparison to RLIE |
|------|-----------|-------|-------------------|
| `.../tAmfM1sORP.md` (HtT) | 4.75 | R1+R2 | Simpler method, synthetic-only datasets. RLIE clearly stronger (real data, clearer method, better eval design). |
| `.../Ns6fnLFsCZ.md` (SPECTRUM) | 5.25 | R2 | Probabilistic rule learning with theory guarantees but missing related work. RLIE comparable, different weakness profiles. |
| `.../BpIbnXWfhL.md` (RuAG) | 6.33 | R1+R2 | Rule-augmented generation with MCTS, broader task diversity but clarity issues. RLIE slightly weaker (missing SD more damaging). |
| `.../hTphfqtafO.md` (LSP) | 6.33 | R1+R2 | Neuro-symbolic with proper ablations and clear evaluation. RLIE weaker on experimental rigor. |
| `.../zDjHOsSQxd.md` (End-to-End Rule Induction) | 6.25 | R2 | Clear methodology with proper evaluation. RLIE weaker. |
| `.../SpTzsQjgxF.md` (Rule-Based Rating) | 5.75 | R1 | Rule-based data selection, missing baselines. RLIE comparable quality with different weaknesses. |

**Round 1 bracket:** [4.5, 6.5] — RLIE is clearly above HtT (4.75) but below RuAG/LSP (6.33).

**Round 2 narrowing:** [4.75, 5.5] — SPECTRUM (5.25) provides the closest anchor; RLIE has a clearer method but the missing SD and lack of proper ablation are more damaging than SPECTRUM's missing baselines. Below RuAG/LSP (6.33) and the Rule-Based Rating paper (5.75).

The paper has a well-motivated core idea and a thoughtfully designed evaluation strategy. However, the two major weaknesses — (1) standard deviations promised but entirely absent, and (2) the misleadingly labeled "ablation study" that compares inference strategies rather than framework components — mean the experimental evidence does not fully support the claims about robustness and component effectiveness. With these fixed, the paper could reach acceptance level. In its current form, the paper is below the acceptance threshold but not fatally flawed.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>