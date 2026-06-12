## Summary
The paper proposes ConciseHint, a framework that intervenes *during* the reasoning generation of large reasoning models (LRMs) by continuously injecting learnable hints (manually designed or trained on concise data) to encourage more concise chain-of-thought outputs. The method adaptively controls injection intensity based on query complexity (via a linear interval function of current reasoning length) and dynamically selects injection positions to balance accuracy and computational cost. Experiments on DeepSeek-R1 and Qwen-3 series across GSM8K, AIME24, and GPQA-Diamond demonstrate 27–65% token reductions with well-maintained accuracy.

## Strengths
- **Novel and well-motivated paradigm**: The paper clearly identifies a gap in existing work—prior methods for efficient reasoning operate before reasoning (prompting, SFT, RL), while ConciseHint intervenes *during* generation. This "in-reasoning intervention" direction is genuinely orthogonal and underexplored, making the contribution conceptually valuable.
- **Comprehensive experimental evaluation**: The method is tested on four strong models (Qwen3-1.7B/4B/8B, DeepSeek-R1-14B) across three benchmarks of varying difficulty, with multiple baselines (BeConcise, Prompt, Deer, NoWait). The demonstration that ConciseHint consistently enhances all baseline methods when combined (Table 1) convincingly shows its flexibility and compatibility.
- **Thoughtful ablation studies**: Tables 3 and 4 provide clear evidence for the necessity of both the adaptive interval mechanism (fixed intervals harm complex tasks like AIME24) and the dynamic position strategy (tail injection causes severe accuracy degradation). The controllability via γ interpolation (Figure 3) is a nice practical property.

## Weaknesses
### Fatal
None.

### Major
- **Concerning accuracy drops on harder benchmarks**: On GPQA-Diamond with Qwen3-1.7B, ConciseHint-T at γ=1.0 drops accuracy from 39.39% to 35.05% (Table 2), a non-trivial degradation. On AIME24 with DeepSeek-R1-14B, ConciseHint alone drops accuracy from 63.00% to 61.00% (Table 1). The paper should more carefully characterize when the method hurts performance and provide clearer guidance on safe operating regimes, rather than framing results primarily through token reduction.
- **Missing recent competitive baselines**: The paper does not compare against several recent efficient reasoning methods such as token-budget-aware approaches (Han et al., 2024, which is cited but not compared), ThinkPrune, or other SFT/RL-based compression methods. The chosen baselines (prompting variants, early exit, transition-word suppression) are reasonable but somewhat weak, which may inflate the perceived advantage of ConciseHint.
- **ConciseHint-T results limited to smallest model only**: The trained hint embeddings are only evaluated on Qwen3-1.7B (Table 2). Given that the main results use 4B, 8B, and 14B models, the lack of ConciseHint-T results on larger models weakens the claim that training provides meaningful additional gains at scale.

### Minor
- **Ad hoc design choices**: The position formula (Equation 3) contains an unexplained constant 1024, and the 0.8 cap is not well-justified. While the paper states these work well empirically, a brief sensitivity analysis or theoretical motivation would strengthen the design.
- **No standard deviation reporting**: The paper mentions running experiments multiple times (5× for GSM8K, 10× for others) but only reports averages. Given the stochastic nature of LLM generation (temperature=0.6), variance information would help assess result reliability.
- **The "complexity" proxy is coarse**: Using current reasoning length as a complexity proxy (Equation 1) is a reasonable heuristic, but the paper acknowledges this is an approximation. A brief discussion of failure modes (e.g., verbose generation on easy queries being misinterpreted as complexity) would be valuable.

### Trivial
- Minor inconsistencies in notation (e.g., "Ori." vs "On" in Table 5).

## Nice-to-Haves
- A comparison of wall-clock inference time (not just token count) would make the efficiency claims more concrete, especially given the overhead of multiple generation calls and text manipulation.
- Analysis of how ConciseHint affects the *quality* of reasoning (not just length and accuracy)—does it eliminate genuinely redundant steps or also cut useful reasoning?
- Evaluation on code generation or other non-math reasoning domains to assess broader applicability.

## Novel Insights
The paper's most valuable insight is that in-reasoning intervention is a viable and complementary paradigm for improving reasoning efficiency, orthogonal to before-reasoning approaches. The empirical finding that hint injection at the tail of generated segments causes models to prematurely terminate or repeat text (rather than continue reasoning) is a useful observation about how LRMs respond to contextual signals during generation. The demonstration that learned hint embeddings can capture concise patterns from data and generalize out-of-domain (Table 2, AIME24 and GPQA-Diamond results) suggests that the "conciseness signal" has transferable structure.

## Suggestions
- Add ConciseHint-T experiments on at least one larger model (e.g., Qwen3-4B) to validate that training gains scale.
- Include standard deviations or confidence intervals in the main results table.
- Add a brief comparison against at least one recent strong baseline (e.g., token-budget-aware reasoning) to contextualize the contribution more fairly.
- Discuss failure cases more explicitly—under what conditions does ConciseHint degrade accuracy unacceptably?

## Score and Decision
The paper presents a genuinely novel paradigm (in-reasoning intervention) with solid experiments and good ablation studies. The method is simple, practical, and compatible with existing approaches. However, concerning accuracy drops on harder benchmarks, limited evaluation of the trained variant (ConciseHint-T) on larger models, and missing competitive baselines prevent a stronger recommendation. The contribution is above the median but not transformative.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept