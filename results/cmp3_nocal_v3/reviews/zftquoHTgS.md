Now I have all the information needed. Let me produce the final consolidated review.

---

## Summary

This paper identifies the "underthinking" phenomenon in LongCoT LLMs — where models prematurely switch between reasoning thoughts without sufficient exploration — and proposes SmartSwitch, an inference-time framework that detects thought switches via linguistic cues, evaluates the abandoned thought's potential using a process reward model (PRM), and intervenes (by rolling back and injecting a deepen prompt) when the abandoned thought was promising. Experiments on five math benchmarks (AIME24/25, AMC23, MATH-500, GaoKao2023en) across model scales from 1.5B to 32B show consistent accuracy improvements (e.g., +23.3 points on AIME25 for the 7B model) while also reducing response length and wall-clock time.

## Strengths

- **Well-identified problem with concrete evidence.** Section 3 substantiates the underthinking phenomenon qualitatively (Figure 1a, a striking example of 74 shallow thoughts) and quantitatively via the Underthinking Frequency metric (Figure 1b). Figure 2b shows that wrong answers exhibit substantially higher UF than correct answers, giving the problem face validity across multiple model families and scales.

- **Clean, motivated method design.** The SmartSwitch pipeline (Figure 3) is logically coherent: detect switches via linguistic cues → evaluate the abandoned thought with a PRM (Universal-PRM-7B) → intervene only if the thought scores above threshold. The two-module architecture (Perception + Intervention) maps directly onto the problem, and the fine-tuning-free framing is practically appealing.

- **Substantial empirical gains, especially on small models.** Table 1 shows large absolute improvements on smaller models: +16.7 points on AIME25 for the 1.5B model, +23.3 points for the 7B model. These are not marginal gains — they represent a meaningful shift in capability at those scales.

- **Counterintuitive efficiency finding.** Tables 2 and 3 show that SmartSwitch *reduces* both response length and wall-clock time despite explicitly encouraging deeper thinking. On average, SmartSwitch shortens inference time by 14–35% across model sizes and benchmarks. This suggests the method prunes wasteful token generation on unpromising threads, more than compensating for PRM overhead.

## Weaknesses

### Fatal

None.

### Major

1. **PRM training-data overlap with evaluation benchmarks is not disclosed, threatening the evaluation's validity.** The method's core decision — whether to intervene on a thought — depends entirely on scores from Universal-PRM-7B (Tan et al., 2025). The paper does not disclose this PRM's training data or verify whether it includes any of the evaluation benchmarks (AIME24/25, AMC23, MATH-500, GaoKao2023en). This is a critical omission because:
   - If Universal-PRM-7B was trained on solutions or reasoning traces from these competitions, the PRM's scores could reflect pattern-matching against known correct reasoning paths for those specific problems rather than general reasoning-quality assessment.
   - The ablation in Table 4 shows Universal-PRM-7B dramatically outperforming alternatives (36.7% vs 24.8% for the next best, Qwen2.5-Math-PRM-72B). The paper attributes this to long-context capability (32K vs 4K tokens), but differing training-data overlap across PRMs is a plausible confound that is not discussed.
   - The threshold ablation (Table 8) shows a very sharp peak at 0.70 across all tested models. While this does not prove leakage, it underscores the need for transparency about the PRM's training data to rule out benchmark contamination.

   **Required action:** Report Universal-PRM-7B's training data composition, explicitly check for overlap with the evaluation benchmarks, and ideally validate on a held-out dataset the PRM could not have seen during training.

### Minor

2. **The Underthinking Frequency metric is a length-based heuristic with known limitations.** Equation (1) defines a thought as "underthinking" if its token length falls below threshold *L*. This is an acknowledged heuristic (line 98), but it cannot distinguish a concise-but-correct step from a genuinely shallow, premature switch. The three key observations in Section 3 (prevalence, severity, contributing factors) all rest on this proxy. Additionally, the thought segmentation itself is performed by an external LLM (DeepSeek-V3, Appendix F.3), introducing a dependency whose segmentation quality is not evaluated. The paper should provide a validation study showing UF correlates with human judgments of reasoning quality, or adopt a complementary metric not based solely on length. (The thought-switching count in Figure 4b partially addresses this, but is itself a different type of proxy.)

3. **The TIP comparison is too narrow to support a claimed advantage.** Table 5 compares SmartSwitch against TIP (Wang et al., 2025) on a single model (DeepSeek-R1-Distill-Qwen-1.5B) and a single benchmark (AIME24). Testing across additional model scales and benchmarks is needed to substantiate the claim that SmartSwitch outperforms existing mitigation methods. The paper should also clarify whether TIP's hyperparameters were tuned for this setting.

4. **The "Always Intervene" baseline could be better controlled.** Table 4 shows that intervening at every thought switch (capped at 3) degrades performance to 18.9%, supporting the need for PRM-guided selection. However, this baseline conflates intervention frequency with selection quality. A *random-intervention* baseline (intervene on randomly selected switches with the same cap) would cleanly isolate the value of PRM-guided selection from the disruptive cost of the intervention mechanism itself.

5. **No variance or statistical significance reported.** The paper reports pass@1 accuracy averaged over 32 responses per problem but provides no standard deviations, standard errors, or confidence intervals. Given that AIME24 and AIME25 have only 30 problems each, individual response-level variance matters. While most reported gains are large enough to be clearly meaningful, smaller gains (e.g., +0.6 points for 7B on MATH-500, +0.9 points for 32B on MATH-500) cannot be assessed for reliability without variance information.

6. **Switch detection recall is not evaluated.** The detection mechanism relies on a fixed set of linguistic cues (Appendix D.2). The paper does not report what fraction of genuine thought switches are captured by these cues. Missed switches mean missed intervention opportunities, and without recall numbers the reader cannot assess how much headroom remains. A manual annotation study on a sample of responses would address this.

7. **The "plug-and-play" claim is overstated for API-gated models.** The abstract describes SmartSwitch as "easily integrated into any large language model as a plug-and-play solution." In practice, the method requires (a) access to the model's token-level output stream, (b) ability to interrupt generation mid-stream and roll back the context, and (c) running a separate 7B PRM concurrently. This is feasible for open-weight models but not for API-gated models (GPT-4, Claude, Gemini) where users lack token-level access. The claim should be qualified.

### Trivial

None.

## Nice-to-Haves

- A cost analysis reporting FLOPs or GPU-hours beyond wall-clock time would help practitioners assess adoption trade-offs.
- Extending evaluation beyond math benchmarks (which the paper acknowledges as future work) would strengthen claims about generality.

## Removed Points

These points from the input review were removed or demoted with justification:

- **Threshold uniformity being "suspicious" (Table 8, 0.70 optimal across all models):** REMOVED. A well-calibrated PRM producing absolute-quality scores would naturally yield a similar optimal threshold across model scales. The sharp peak can be partially explained by AIME24's small size (30 problems), where a single problem changing correctness can swing accuracy by ~3 points. This is not evidence of leakage.
- **"TIP was designed for larger models":** REMOVED. This claim about TIP's intended scale is external information not verifiable from the paper. The core criticism (narrow comparison) is retained.
- **Table 2 (14B model "All" length increasing +0.4%):** REMOVED as a standalone weakness. This is a single datapoint; the overall trend across all models is reduced length. The observation is intriguing but does not undermine the efficiency claim.
- **Strengths dropped:** None of the four listed strengths were removed — all are concrete, specific, and evidence-grounded.

## Novel Insights

The reviews converge on a clear vulnerability: the method's empirical results hinge entirely on PRM score quality, yet the paper provides no transparency about the PRM's training-data composition relative to its evaluation benchmarks. This is the single highest-priority concern. A secondary cross-cutting insight is that the UF metric — while useful for characterizing the phenomenon — is fragile (length-only heuristic + external segmentation), and the paper's evidence that SmartSwitch mitigates underthinking would benefit from a non-length-based validation. The narrow TIP comparison and missing variance reporting are standard evidential gaps that weaken but do not invalidate the contribution. The counterintuitive efficiency finding (reduced tokens despite deeper thinking) is genuinely interesting and appears robust across model sizes.

## Suggestions

1. **Disclose Universal-PRM-7B's training data and verify benchmark overlap.** This single step determines whether the evaluation is trustworthy. If the PRM has seen these benchmarks, repeat experiments on a held-out set.

2. **Add a random-intervention baseline** to Table 4 to isolate PRM selection value from intervention disruption.

3. **Report standard deviations or confidence intervals** for all accuracy numbers, especially on the 30-problem AIME benchmarks where variance is higher.

4. **Expand the TIP comparison** to at least one additional model (e.g., QwQ-32B) and one additional benchmark (e.g., AIME25).

5. **Qualify the "plug-and-play" claim** to reflect that the method requires token-level access to the generation loop.

## Score and Decision

This paper identifies a genuine and well-motivated problem, proposes a clean and logically coherent method, and reports substantial empirical gains that are (on the surface) impressive. The efficiency improvement is a non-obvious and interesting finding. However, the evaluation has a significant unaddressed confound: the PRM whose scores drive all intervention decisions is used without any disclosure of its training data or verification of benchmark overlap. Given the enormous gap between Universal-PRM-7B and other PRMs in the ablation, and the extreme threshold sensitivity, this is not a minor detail — it is the central vulnerability of the evaluation. The remaining issues (narrow TIP comparison, no variance, missing controls) are addressable.

If the PRM overlap concern is resolved favorably (the PRM was not trained on these benchmarks), the paper's contribution is solid and acceptance with minor revisions is warranted. If it is not resolved, the headline results may be substantially inflated. I recommend acceptance conditioned on clarifying this issue.

**Score:** 6  
**Decision:** Accept

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>