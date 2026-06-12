## Summary
This paper identifies and characterizes the "underthinking" problem in LongCoT LLMs, where models prematurely abandon promising reasoning paths through frequent shallow thought-switching. It proposes SmartSwitch, a plug-and-play inference framework that detects thought switches via linguistic cues, evaluates abandoned thoughts using a Process Reward Model (PRM), and prompts deeper exploration of promising but prematurely discarded reasoning paths. Experiments on five math benchmarks show consistent accuracy improvements (up to +23.3 percentage points) across model scales from 1.5B to 32B parameters, while simultaneously reducing response length and inference time.

## Strengths
- **Well-motivated problem with solid empirical characterization.** Section 3 provides both qualitative and quantitative evidence for the underthinking problem, introducing the Underthinking Frequency metric and demonstrating its prevalence across six models, its correlation with difficulty, and its association with incorrect answers (Figure 2). This is a genuine and well-documented phenomenon.
- **Impressive and consistent experimental gains.** SmartSwitch delivers substantial improvements across all five model sizes and all five benchmarks, with gains ranging from +0.6% to +23.3%. Notably, smaller models benefit enormously (DeepSeek-R1-Distill-1.5B +16.7 on AIME25; 7B +23.3 on AIME25), and the 14B model with SmartSwitch surpasses vanilla 32B inference, demonstrating effective cross-scale bridging.
- **Efficiency paradox resolved convincingly.** The paper shows SmartSwitch simultaneously improves accuracy while reducing token count (up to 14.2%) and wall-clock time (up to 35.3%), which is counterintuitive given that it encourages "deeper" exploration. The explanation—pruning wasteful shallow reasoning and redirecting compute to productive paths—is compelling and practically valuable.
- **Thorough ablation study design.** The ablations on PRM choice (Table 4, including the "Always Intervene" baseline showing naive intervention hurts performance), process division strategy (Table 6), score mapping (Table 7), and threshold sensitivity (Table 8) collectively demonstrate careful engineering and isolate the contribution of each component.
- **Direct comparison with alternative mitigation methods.** Table 5 comparing against standard prompting and TIP (Wang et al., 2025) provides useful context, showing that generic instructions are insufficient and that TIP's indiscriminate constraint is inferior to SmartSwitch's selective approach.

## Weaknesses
### Fatal
None.

### Major
- **Fragile threshold sensitivity.** Table 8 reveals sharp performance swings around the optimal threshold: for DeepSeek-R1-Distill-1.5B on AIME24, accuracy drops from 40.0% at threshold 0.70 to 30.0% at both 0.69 and 0.71. This sensitivity is consistent across models (e.g., 32B drops from 76.7% to 63.3%). This raises concerns about robustness in deployment without per-task or per-model tuning, and the paper does not provide practical guidance for threshold selection beyond picking the optimal value post-hoc.
- **Limited comparison baselines for test-time compute methods.** The paper compares against vanilla inference, standard prompting, and TIP, but does not compare against other test-time compute enhancement strategies such as best-of-N with a verifier/ORM, beam search, majority voting with re-ranking, or self-consistency. These are natural baselines for a method that uses an external PRM at inference time, and it is unclear whether SmartSwitch's gains are complementary to or subsumed by simpler PRM-based re-ranking approaches.
- **Mathematical reasoning only.** All five benchmarks are mathematics problems. The underthinking phenomenon likely manifests in other reasoning domains (coding, logical reasoning, scientific QA), and the paper provides no evidence that SmartSwitch generalizes beyond math. The paper's own future work section acknowledges this, but the current empirical scope is narrow.

### Minor
- **Crude thought-switch detection mechanism.** Detecting switches purely through fixed linguistic cues ("Alternatively", "Wait", etc.) is acknowledged as a limitation but is fundamental to the framework. The paper does not quantify what fraction of genuine premature abandonments are missed by this mechanism, making it difficult to assess the recall of the detection system.
- **UF metric oversimplification.** Defining underthinking solely by token length (a thought under 100 tokens = underthinking) is a rough proxy. A brief thought may be complete and correct, while a long one may still be shallow. The paper does not validate this metric against human judgments of reasoning quality.
- **The "Always Intervene" baseline performs below vanilla (18.9% vs 20.0% on AIME25 for 1.5B).** While this is presented as evidence for the importance of selective PRM-guided intervention, the magnitude of degradation is small and may not be statistically significant with 32 samples per problem. Statistical significance testing is absent throughout all results.

### Trivial
None.

## Nice-to-Haves
- A comparison showing SmartSwitch's gains are additive with best-of-N + PRM re-ranking (or showing it is superior), since both methods leverage PRMs at test time.
- Error analysis showing specific problem instances where SmartSwitch recovers correct answers versus where it fails, to understand the failure modes.
- Results on at least one non-mathematical reasoning benchmark (e.g., coding or logical reasoning).

## Novel Insights
The paper's central novel observation is that underthinking (premature thought-switching) is a widespread, difficulty-correlated failure mode in LongCoT models that is mechanistically distinct from overthinking, and that selective, PRM-guided intervention at detected switch points can simultaneously improve accuracy and efficiency. The finding that encouraging "deeper" thinking actually reduces total token count is particularly insightful—it suggests that much of the token expenditure in current LongCoT models is wasted on shallow, abandoned reasoning paths rather than productive exploration. This reframes the efficiency-accuracy trade-off in test-time compute.

## Suggestions
- Add statistical significance tests (e.g., bootstrap confidence intervals) for all reported accuracy differences, especially for the smaller gaps where significance is uncertain.
- Include at least one strong test-time compute baseline using the same PRM (e.g., best-of-32 with PRM re-ranking) to disentangle the value of the SmartSwitch intervention mechanism from simply having a PRM available.
- Provide a practical heuristic or automatic procedure for threshold selection rather than reporting only the optimal post-hoc value.
- Report the recall and precision of the linguistic-cue-based thought switch detector by manually annotating a sample of traces.

## Score and Decision
The paper presents a well-motivated, practically valuable framework with strong and consistent empirical results. The ablations are thorough and the efficiency findings are genuinely interesting. However, the fragile threshold sensitivity, narrow evaluation domain (math only), and absence of comparison with other PRM-based test-time methods represent meaningful limitations. The core contribution—detecting and intervening on premature thought switches—is sound and useful, but the evaluation does not yet fully establish the method's robustness or broader applicability.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>