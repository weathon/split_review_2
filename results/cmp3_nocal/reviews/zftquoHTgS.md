## Summary

This paper identifies and formalizes the "underthinking" problem in LongCoT-reasoning LLMs—where models prematurely abandon promising reasoning paths with shallow exploration. The authors propose SmartSwitch, a training-free, plug-and-play inference framework that detects thought-switches via linguistic cues, evaluates the abandoned thought's potential using a Process Reward Model (PRM), and intervenes by backtracking and injecting a deepen prompt when a high-potential thought is judged prematurely discarded. Experiments on five math benchmarks across five model sizes (1.5B–32B) show substantial accuracy gains (e.g., +16.7 points on AIME25 for the 1.5B model) while also reducing response length and wall-clock time.

---

## Strengths

1. **Well-motivated and empirically grounded problem definition.** The underthinking phenomenon is supported by both a qualitative trace (Figure 1a: a 74-thought DeepSeek-R1 response with median 150 tokens) and a quantitative UF metric showing correlation with problem difficulty and incorrect answers (Figure 2). This makes a clear case that the problem is real and consequential.

2. **Clean, practical, and plug-and-play method.** SmartSwitch is conceptually simple—detect switches, score with an off-the-shelf PRM, intervene when promising—and requires no fine-tuning. It can be applied to any existing LongCoT model, which is a genuine practical advantage.

3. **Consistent, large empirical gains across model sizes.** Table 1 shows accuracy improvements on every model and every benchmark (e.g., DeepSeek-R1-Distill-Qwen-7B: +23.3 points on AIME25; QwQ-32B: +7.2 points on AIME24, reaching 100% on AMC23). The consistency across five models is the paper's strongest evidence.

4. **Efficiency improvement despite deeper exploration.** Tables 2 and 3 show that SmartSwitch _reduces_ both response length (e.g., −14.2% for the 32B model) and wall-clock time (e.g., −33.7% for the 1.5B model on AIME24) while improving accuracy. The method prunes wasteful shallow thoughts rather than simply adding tokens.

5. **Thorough ablation studies.** The "Always Intervene" baseline (Table 4, 18.9% vs. vanilla 20.0%) cleanly shows that selective PRM-guided intervention is essential. The ablations of process division strategies (v1–v4, Table 6) and score mapping strategies (Table 7) provide practical, actionable guidance.

---

## Weaknesses

### Major

1. **Extreme threshold sensitivity raises robustness concerns.** Table 8 shows a consistent pattern across all five models: accuracy spikes sharply at a threshold of 0.70 and collapses at neighboring values (0.69, 0.71). For example, R1-Distill-Qwen-7B goes from vanilla 55.5% → 66.7% at 0.70 → 43.3% at 0.71 (worse than vanilla). For R1-Distill-Qwen-32B, 0.69 and 0.71 both give 63.3% vs. vanilla 72.6%. While the fact that 0.70 works across all tested models is positive, the operating region that beats vanilla is narrow (±0.01), and the paper provides no mechanistic explanation for why this single value is universal. In deployment, PRM calibration drift could easily shift the optimal threshold.

2. **The PRM's scoring ability vs. the intervention mechanism's value are not disentangled.** SmartSwitch delegates the central judgment ("is this abandoned thought promising?") entirely to Universal-PRM-7B. Table 4 shows that swapping the PRM changes results dramatically (Universal-PRM-7B: 36.7% vs. Qwen2.5-Math-PRM-72B at 10× the size: 24.8%). The paper does not compare SmartSwitch to a simpler PRM-as-verifier baseline (e.g., generate N samples, score with the same PRM, pick top-1). Such a comparison would isolate whether the real-time backtracking-and-deepening mechanism adds value beyond what the PRM could achieve as a solution ranker, which is central to the paper's claimed contribution.

### Minor

3. **Thought-switch detector recall is unquantified.** The method can only intervene when the model uses explicit markers (e.g., "Alternatively..."). The paper acknowledges this limitation but does not measure (a) what fraction of actual thought switches are captured by the cue list, or (b) how many are missed. This is measurable (e.g., manually annotate a sample of traces) and the answer determines whether this bottleneck is minor or severe.

4. **Comparison to the only prior underthinking mitigation method (TIP) is limited to one model and one benchmark.** Table 5 compares TIP only on R1-Distill-Qwen-1.5B and AIME24. Extending this to additional models and benchmarks would strengthen the empirical positioning.

5. **No analysis of intervention frequency or success rate.** The paper does not report how many interventions fire per problem on average, or how often a deepened exploration leads to a correct answer vs. persisting on a wrong path. This would directly validate whether the mechanism works as intended.

6. **No statistical uncertainty quantification.** Results are reported as point estimates over 32 responses without confidence intervals or significance tests. Given the sharp threshold sensitivity, uncertainty intervals would help assess whether the gains at 0.70 are statistically robust.

### Trivial

- The process-to-thought "last process score" strategy (Table 7) is attributed to being "most representative," but a more precise explanation is that PRM scores tend to increase as reasoning unfolds and the path becomes clearer. This nuance would improve the discussion.

---

## Nice-to-Haves

- **A PRM-as-verifier baseline** (generate N samples → rank by PRM score → pick top-1) would cleanly separate the contribution of the PRM's scoring ability from the contribution of the real-time intervention mechanism.
- **Quantifying detector recall** on a manually annotated sample (50–100 traces) would establish how serious the linguistic-cue bottleneck actually is.
- **An analysis of why gains are much smaller on MATH-500** (0.6–2.0 points) than on AIME24/AIME25 would clarify when SmartSwitch is most beneficial.
- **A breakdown of wall-clock time** separating PRM overhead from saved generation time would clarify the net efficiency story, especially for the 1.5B model where the 7B PRM is larger than the base model.

---

## Removed Points

These points from the input review are excluded with justification:

- *"The PRM is doing the intellectually hard part" (as a fatal framing)* — The paper never claims the PRM is not doing important work; the claim is about the *framework* combining detection + evaluation + intervention. The concern is preserved as **Major weakness #2** (the missing baseline), not as a standalone fatal flaw.
- *"UF metric conflates shallow reasoning with short thoughts"* — The metric is explicitly heuristic and used only for motivation (Section 3.2), not as an evaluation metric. Reasonable for its purpose.
- *"200-token segmentation threshold not ablated"* — This is a practical design choice for PRM context management; requesting an ablation is reasonable but a relatively minor point that would inflate the weakness list.
- *"Non-math domain evaluation"* — The paper scopes to mathematical reasoning; extending beyond scope is a nice-to-have, not a weakness.
- *"The last process score explanation"* — The paper's explanation is defensible; the reviewer's alternative reading is not clearly more correct.

---

## Novel Insights

The input reviews do not surface any insight about the paper that goes beyond what the paper itself claims. The observation that the paper achieves efficiency gains *despite* encouraging deeper thinking is well-documented by the authors (Tables 2–3). The reviews' main novel observation is the severity of the threshold sensitivity pattern across all five models, which the paper reports but does not deeply analyze.

---

## Suggestions

1. Add a **PRM-as-verifier baseline** (best-of-N with the same PRM) to disentangle the PRM's scoring contribution from the intervention mechanism's contribution.
2. **Analyze the threshold spike**: examine the distribution of PRM scores for "should intervene" vs. "should not intervene" cases to understand why 0.70 is universally optimal and why neighboring values fail.
3. **Quantify detector recall** by manually annotating 50–100 reasoning traces and reporting the fraction of switches caught by the cue-based detector.
4. Report **confidence intervals** (e.g., via bootstrapping of the 32 responses) for the main results.

---

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>