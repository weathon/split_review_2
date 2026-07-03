Now let me produce the final consolidated review.

## Summary

The paper studies preference optimization for Large Reasoning Models (LRMs), where computing the marginal objective over reasoning traces is intractable and the common single-trace surrogate induces high gradient variance. The proposed method, BVPO, mixes a standard trace-based gradient with an "empty-trace" gradient (obtained by suppressing reasoning trace generation) via a convex combination \(g_c = \alpha g_t + (1-\alpha)g_e\). The paper provides theoretical analysis showing variance reduction, an MSE-optimal mixing coefficient, and links to SGD convergence bounds. Empirically, BVPO improves alignment on Arena-Hard and AlpacaEval 2 by 5–8 points over DPO/SimPO across three DeepSeek-R1 distill models, and also improves math reasoning despite training only on conversational data.

## Strengths

1. **Formalization of trace-induced gradient variance as a distinct challenge for LRM alignment.** The paper clearly articulates a genuine, underexplored problem. Section 3.2 contrasts the intractable marginal objective \(\mathcal{L}_m\) with the tractable but noisy trace-based proxy \(\mathcal{L}_t\), giving this problem clean mathematical footing. Prior work on LRM alignment is indeed limited to brief remarks in technical reports, making this a meaningful contribution.

2. **Consistent and sizable empirical gains across multiple models and benchmarks.** Table 1 shows BVPO improves over the best baseline by up to **7.8 points on AlpacaEval 2** and **6.8 points on Arena-Hard**. Gains hold across three model sizes (1.5B, 7B, 8B), both Thinking and NoThinking inference modes, and two alignment benchmarks. The pattern of improvement is consistent and not cherry-picked.

3. **Unexpected improvement in math reasoning after conversational-only alignment.** Despite training exclusively on general conversational data (UltraFeedback), BVPO raises the base model's average across six math reasoning benchmarks by **up to 4.0 points** (Table 2). This is a non-obvious finding that supports the claim that variance reduction has downstream benefits beyond alignment.

4. **Clean, intuitive method that is simple to adopt.** The BVPO loss (Equation 2) is a straightforward convex combination of two DPO-style losses. The practical implementation — appending `