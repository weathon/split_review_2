## Summary
The paper introduces the Task-Method-Knowledge (TMK) framework—a cognitive science knowledge representation—as a prompting strategy to improve LLM performance on planning tasks. Evaluating on PlanBench’s Blocksworld domain (Classic, Mystery, Random variants) with several OpenAI models, the authors report that TMK-structured prompts improve accuracy, most dramatically for o1 on Random Blocksworld (31.5% → 97.3%). They argue that TMK acts as a symbolic steering mechanism, shifting models from linguistic approximation toward formal, code-like reasoning.

## Strengths
- **Addresses an important, well-motivated problem**: LLMs’ poor planning ability is a widely recognized limitation, and the paper targets this with a structured approach grounded in cognitive science.
- **Uses a rigorous evaluation framework**: PlanBench provides formal verification of full plans (not just final answers), and the benchmark includes obfuscated variants (Mystery, Random) that help isolate reasoning from semantic priors.
- **Demonstrates a substantial improvement in a challenging setting**: The gain from 31.5% to 97.3% on Random Blocksworld for the o1 model is impressive and goes well beyond typical incremental prompting gains.
- **Offers an interesting analysis of “performance inversion”**: The reversal of domain difficulty (Random becoming easier than Mystery under TMK for o1) is a nontrivial empirical finding that supports the claim of a different reasoning modality.

## Weaknesses
### Fatal
None.

### Major
- **Limited scope and missing comparisons**: The paper tests only Blocksworld (one domain) and only OpenAI models. More critically, it does **not compare TMK against other structured representations** such as a plain PDDL description, a simple JSON schema of actions without the TMK hierarchy, or even a well-organized textual description. Without such ablations, it is impossible to attribute the gains to TMK’s specific “teleological and causal” structure rather than to any well-structured format.
- **Unfair baseline comparison**: TMK is evaluated with one-shot prompts while the plain-text baseline uses the best of zero-shot and one-shot (and for older models, leaderboard zero-shot numbers). The authors argue this is inconsequential, but the paper does **not provide a direct zero-shot TMK baseline** or a careful one-shot plain-text run on the same set of instances. The claim that zero-shot outperforms one-shot in plain text does not guarantee that one-shot vs. zero-shot is irrelevant for TMK.
- **Lack of statistical rigor**: The paper reports only a single accuracy percentage for each condition, with **no confidence intervals, number of test instances, or indication of variance**. Given the known stochasticity of LLMs, it is unclear whether the improvements (especially the smaller ones) are statistically meaningful.
- **Mechanism claim is unsupported**: The central hypothesis—that TMK steers models toward “code-execution pathways”—is highly speculative. The paper provides **no internal analysis** (e.g., attention patterns, token probabilities, intermediate activations) to support this claim. The observation that o1 does better on Random under TMK is consistent with many alternative explanations (e.g., TMK simply provides better formatting for out-of-distribution tokens).
- **o1-mini regression unexplained**: The degradation on Mystery Blocksworld for o1-mini (19.1% → 16.83%) is dismissed with a capacity argument, but the paper does not investigate whether this is systematic or a random fluctuation. This weakens the claim of general improvement and raises questions about the robustness of TMK across model scales.

### Minor
- The paper does not report inference cost or prompt length; TMK prompts are substantially longer, and the added cost is not discussed.
- The related work section describes CoT and ReACT limitations but does not include a direct experimental comparison with these methods on the same setup.
- The phrase “performance inversion” is used prominently but is only clearly observed for the o1 model; for GPT-5 the effect is much smaller, and for other models there is no inversion.

### Trivial
- The paper mentions an OSF link for full results and prompts, but the link is anonymous and not verifiable in review.
- Some table formatting (e.g., Table 2) uses periods as thousand separators in percentages (e.g., 97.33%), which is fine but a minor style inconsistency.

## Nice-to-Haves
- A zero-shot TMK baseline would strengthen the attribution of gains to TMK structure.
- An ablation replacing TMK with a simple PDDL-like or JSON action specification would help isolate the contribution of TMK’s specific features.
- Testing on at least one other PlanBench domain (e.g., Logistics) would improve generalizability.
- Including error bars or per-problem breakdowns would increase confidence in the results.

## Novel Insights
None beyond the paper’s own contributions. The “performance inversion” observation is interesting but remains an empirical phenomenon without a theoretically grounded explanation or sufficient evidence to rule out simpler alternative accounts.

## Suggestions
- Compare TMK against an equally structured but non-TMK prompt (e.g., a PDDL description of the domain) with identical experimental settings (one-shot, same test instances).
- Run zero-shot TMK to directly match the leaderboard baseline and isolate the effect of the example.
- Report the number of test problems, run each condition multiple times (e.g., 3-5 seeds), and provide accuracy with confidence intervals or standard deviations.
- For the steering mechanism claim, consider analyzing the model’s internal representations (e.g., probing attention to token types, or examining the chain-of-thought tokens for evidence of code-like patterns).

## Score and Decision
**Score**: 4.5  
**Decision**: Reject  

The paper tackles a timely problem and presents an intriguing empirical result (the large gain on Random Blocksworld for o1). However, the evaluation is too narrow, the baselines are not sufficiently controlled, and the central claim about the steering mechanism lacks direct evidence. The contributions, while not invalid, are not yet convincing enough for acceptance at a top venue like ICLR. A more rigorous study with proper ablations and broader validation would strengthen the work considerably.

MY FINAL SCORE: 4.5  
MY FINAL DECISION: Reject