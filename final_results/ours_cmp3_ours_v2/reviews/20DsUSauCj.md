## Summary

This paper introduces "persona vectors" — linear directions in LLM activation space corresponding to personality traits — extracted via an automated pipeline from natural-language trait descriptions. The authors demonstrate four applications: monitoring prompt-induced and finetuning-induced trait shifts via projection, controlling trait expression via activation steering, a novel "preventative steering" method that adds the persona vector during finetuning to prevent trait drift while preserving capabilities, and pre-finetuning data screening using a projection-difference metric to flag problematic training data. Experiments use Qwen2.5-7B-Instruct and Llama-3.1-8B-Instruct across evil, sycophancy, and hallucination traits.

## Strengths

1. **Automated extraction pipeline (Section 2).** The pipeline that generates contrastive system prompts, evaluation questions, and rubrics from a single natural-language trait description is a clean systematization. Prior work (Wu et al., 2025; Turner et al., 2024) required hand-crafting contrastive pairs; this pipeline reduces that bottleneck considerably. This is a genuine methodological contribution.

2. **Preventative steering (Section 5).** The idea of steering *toward* an undesirable direction *during finetuning* to prevent drift is novel and counterintuitive. The fact that it preserves MMLU and new-fact accuracy better than inference-time steering (Figure 6) is a legitimate empirical finding. The comparison against CAFT (Casademunt et al., 2025) and regularization baselines shows differentiated behavior (effective for hallucination where CAFT is not), further supporting the method's value.

3. **Pre-finetuning data screening (Section 6).** The projection-difference metric — comparing training response projections against the model's own "natural" response projections — is a practical tool. The high correlations (r = 0.88–0.95 across settings in Figure 7) suggest genuine predictive value. The sample-level separability in Figure 8 is clean and intuitive, and the paper claims this method works on real-world datasets and can escape LLM-based filters (Appendices M, N).

4. **Honest about limitations.** The paper explicitly notes that monitoring correlations arise primarily from distinguishing between different prompt types (Section 3.3), that cross-trait correlations exist (footnote 6), that single-layer preventative steering does not always fully prevent trait acquisition, and that computing projection difference is expensive. This candor strengthens credibility.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Preventative vs. inference-time steering comparison is structurally asymmetric (Section 5).** The paper's abstract states that preventative steering "better preserves the model's general capabilities compared with standard inference-time steering." However, the comparison is between different regimes: inference-time steering must suppress behavior already baked into the weights by finetuning, while preventative steering prevents the weight shift from occurring in the first place. This asymmetry partly inflates the apparent advantage. Figure 6 partially addresses this by matching at baseline-level suppression for the hallucination case study, but the broader claim in Section 5 and the abstract still relies on the asymmetric framing. The paper would benefit from either (a) acknowledging this structural difference more prominently alongside the claim, or (b) adding a matched comparison where both methods achieve equivalent trait suppression levels.

2. **Heavy reliance on a single LLM judge with potential circularity (Sections 2–6).** GPT-4.1-mini is used to (a) filter responses for vector extraction, (b) select the best layer via steering effectiveness (Appendix D.4), and (c) evaluate all downstream trait expression. If the judge has systematic biases — e.g., confusing refusal with low trait expression — those biases propagate through the entire pipeline. The paper mentions validation against human evaluators and external benchmarks (Appendix D), which mitigates this concern, but reporting the human-agreement statistics in the main text would strengthen confidence. The layer selection methodology would benefit from an independent criterion (e.g., separability on a held-out set) to break the potential feedback loop.

3. **Mechanism of preventative steering is claimed but not demonstrated (Section 5.1).** The paper states that adding the persona vector during training "counteracts the finetuning objective's tendency to push the model along that direction," but provides no evidence for this mechanism. Alternative explanations are plausible (e.g., regularization, direction saturation, loss landscape changes). Without gradient analysis, weight-change analysis, or an ablation varying when steering is applied, the mechanism remains opaque. This does not invalidate the empirical finding, but it means practitioners lack guidance on when the method might fail.

4. **The finetuning-shift analysis is correlational, not causal (Section 4.2, "mediated by" language).** The paper asks "Are behavioral shifts during finetuning *mediated by* persona vectors?" and presents strong correlations (r = 0.76–0.97) as evidence. However, this is consistent with the persona vector being (a) a causal mediator, (b) a symptom of the change, or (c) one of many correlated directions that shift together. The paper's own acknowledgment of cross-trait correlations (footnote 6) suggests (c) is partially true. The "mediated by" language overstates what the evidence supports; "strongly correlated with" would be more precise.

5. **Gap between monitoring motivation and demonstrated capability (Section 3.3).** The introduction motivates monitoring with examples of *unexpected* persona shifts (Bing chatbot, Grok), but the demonstrated monitoring detects *explicit, prompt-induced* shifts. The paper honestly notes that correlations are "more modest when controlling for prompt type" and that vectors "may be less reliable for more subtle behavioral changes." However, it does not address the more fundamental issue: detecting unexpected shifts requires knowing *which* persona vector to monitor a priori. This gap between the motivating examples and the demonstrated capability should be discussed.

### Trivial
None.

## Nice-to-Haves

- **Effect sizes beyond correlations.** The paper extensively reports correlation coefficients but not absolute prediction error (e.g., RMSE for the projection-difference metric). While scatter plots show absolute values, explicit error metrics would strengthen the quantitative claims.
- **Efficiency discussion for projection difference.** Computing projection difference requires generating base-model responses for all training samples, which is expensive at scale. The paper mentions approximation strategies in Appendix K; a brief discussion of computational cost in the main text would set expectations for practitioners.
- **Broader model scaling.** Only 7–8B instruction-tuned models are used. Including a model at a different scale (e.g., 1–3B or 70B+) or a base model would strengthen generalizability claims.

## Removed Points

These points were removed from the input reviews after verification against the paper. They are kept for transparency.

1. **"Preventative steering mechanism needs gradient/weight-change analysis"** — Removed from Major to Minor status. The mechanism claim is a plausible explanation for an empirical finding; the paper's main contribution is that the method *works*, not the precise mechanism. Preserved in softened form as Minor weakness #3 above.

2. **"The paper should run the actual filtering experiment"** — Removed. The paper explicitly states it does this in Appendix M and Appendix N. Since the appendix is stripped by the parser, the paper's claim stands.

3. **"N=2 models insufficient"** — Removed. Two models from different families at a popular scale is standard practice.

4. **"API model versions can change"** — Removed. Generic concern applying to virtually all LLM research.

5. **"Score range 0–100 is uncalibrated"** — Removed. The paper validates against human evaluators, which addresses this.

6. **"Missing appendix content"** — Removed. The appendix is stripped by the parser for all papers.

## Novel Insights

None beyond the paper's own contributions. The key novel synthesis — that a single extracted direction can serve monitoring, steering, preventative steering, and data screening — is well articulated by the paper itself. The insight that preventative steering (adding the vector *toward* the undesirable trait during training) outperforms post-hoc mitigation is genuinely novel and well demonstrated.

## Suggestions

1. **Add a matched comparison in Section 5** where both preventative and inference-time steering achieve equivalent trait suppression and capability preservation is compared, to directly address the structural asymmetry concern.

2. **Report human-validation agreement statistics from Appendix D in the main text** alongside the LLM-judge results, to give readers direct confidence in the evaluation pipeline.

3. **Soften the "mediated by" framing in Section 4.2** to reflect that the evidence is correlational rather than causal.

4. **Discuss the gap between unexpected-shift motivation and pre-identified-direction monitoring** more explicitly in Section 3.3.

5. **Consider an independent criterion for layer selection** (e.g., separability on a held-out set) to break the potential LLM-judge feedback loop.

## Score and Decision

**Calibration anchors (retrieved):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `8QTpYC4smR.md` | 1.00 | R1 low | Survey paper; far weaker |
| `DXaUC7lBq1.md` | 3.00 | R1 mid-low | Personality origins via SAEs; less rigorous, weaker claims |
| `2XBPdPIcFK.md` | 5.00 | R1 mid | ActAdd steering; less comprehensive, outdated models |
| `TqwTzLjzGS.md` | 5.25 | R1 mid | BIG5-CHAT personality dataset; training-based, different scope |
| `0DZEs8NpUH.md` | 6.00 | R1 mid-high | Personality alignment via activation intervention; comparable breadth |
| `LYHEY783Np.md` | 6.67 | R1/R2 mid-high | Neuron-based personality induction; similar topic, comparable quality |
| `8WQ7VTfPTl.md` | 6.40 | R2 mid-high | Dynamic steering vectors; comparable |
| `wozhdnRCtw.md` | 7.00 | R1 high | Instruction-following via steering; cleaner scope and evaluation |
| `Oi47wc10sm.md` | 7.33 | R1/R2 high | Conditional activation steering; cleaner evaluation design |
| `tTPHgb0EtV.md` | 8.00 | R1 high | Booster harmful fine-tuning defense; tighter, cleaner contribution |

**Round 1 bracket:** 6.0–7.5. **Round 2 narrow:** 6.0–7.0.

The paper is stronger than the 5.0-range ActAdd paper (more contributions, more honest caveats, more thorough evaluation) and comparable to the 6.0–6.67 personality/steering papers. It does not reach the 7.0+ range because of the comparison asymmetry (weakness #1), LLM-judge circularity risk (weakness #2), and unsubstantiated causal framing (weakness #4). These are addressable but keep the paper from being top-tier. The paper makes several genuine contributions, is well-written and honestly caveated, and its core findings are reproduced across two model families.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>