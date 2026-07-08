Now let me write the final review.

## Summary

This paper proves that decoder-only Transformer language models are almost-surely injective (distinct prompts yield distinct hidden states) using real-analytic function theory, shows this property is preserved under gradient-based training, and introduces SIFT, an algorithm for exact prompt recovery from hidden activations. The theoretical contribution — establishing injectivity as a measure-zero property in parameter space that training cannot disrupt — is genuinely novel and the paper provides large-scale collision search experiments (~5 billion comparisons across six model families) confirming no collisions in practice.

## Strengths

- **Novel theoretical framing (weight 11.26).** The paper is the first to apply real-analytic function theory to prove injectivity of the full prompt-to-hidden-state map in Transformer LMs. The insight that collisions are measure-zero events in parameter space rather than architectural inevitabilities is well-articulated and represents a meaningful conceptual contribution (Section 2, Theorems 2.1–2.2).

- **Training-preservation argument (weight 9.93).** Theorem 2.3 (injectivity preserved under training) goes substantially beyond prior work such as Sutter et al. (2025), which only established injectivity at initialization. Showing that gradient descent preserves absolute continuity of the parameter distribution is the paper's strongest theoretical contribution.

- **Large-scale collision search (weight 9.06).** ~5 billion pairwise comparisons across multiple model families (GPT-2, Gemma3, Llama-3.1, Mistral, Phi-4) with consistent null results provide a genuine sanity check that the theory does not break in practice. Minimum distances far exceed finite-precision thresholds (always > 0.001 at first layer, > 0.1 at mid/deep layers), which is informative beyond the existence proof of injectivity (Section 4.1, Figure 3).

## Weaknesses

### Fatal
None.

### Major
- **No comparison against the closest prior work for the inversion setting (weight -0.64).** The paper cites Thomas et al. (2025) as the most related hidden-state inversion method (line 339) but does not implement it as a baseline. Instead, it compares against HARDPROMPTS (Wen et al., 2023), a prompt-optimization method for a different task — a comparison the paper itself acknowledges as not directly comparable (lines 293–311). This weakens the empirical positioning of SIFT.

- **Inversion experiments are small relative to the strength of the claims (weight 0.19).** The main inversion experiment uses 100 prompts of 20 tokens each (line 291), and the robustness experiment uses 50 prompts of 10 tokens each (line 323). For a paper claiming "the first algorithm that provably and efficiently reconstructs the exact input text," a sample of 100 prompts is modest — a single failure case would drop accuracy from 100% to 99%. No confidence intervals on the accuracy metric or analysis of failure modes are provided.

### Minor
- **Unanalyzed runtime variance and gradient heuristic.** The runtime of 28.01 ± 35.87 seconds (Table 5) has a standard deviation exceeding the mean, indicating a highly skewed distribution that is not discussed. The gradient-guided policy that achieves the empirical speedup is described in the appendix (stripped by the parser), but the main text provides no analysis of when the gradient heuristic correctly ranks candidates or how its performance degrades across models or data distributions.

- **Quantization experiments are not grounded in the paper's own theory.** The theory explicitly identifies quantization as a failure mode for injectivity (line 125: "non-analytic choices such as quantization"), yet experiments on quantized models (Tables 2, 3, 4) are presented without reconciling this. The fact that injectivity empirically survives quantization does not follow from the theoretical framework and should be discussed as an empirical finding, not as predicted by the theory.

- **Theorem 3.2's robustness guarantee is conditional on an unverifiable quantity.** The bound depends on Δ_{π,t} (minimum separation between hidden states for different tokens given a prefix), which itself would require exhaustive search over all token pairs to compute. This makes the guarantee useful in principle but difficult to apply without additional bounds on Δ.

- **Naming inconsistency.** The algorithm is referred to as SIFT (abstract, line 9), SIPIT (Section 3 heading, line 139), SIpT (experiments, line 234), SiPT (Tables 4 and 5, lines 309/319), and SiPIT (conclusion, line 345). While individually minor, this is distracting.

### Trivial
None.

## Nice-to-Haves
- Provide a lower bound on Δ_{π,t} (minimum token separation) or clearly separate the theoretical guarantee (injectivity) from the empirical heuristic (gradient-guided search).
- Scale inversion experiments to thousands of prompts of varying lengths; report failure cases and statistical analysis of when/why the gradient heuristic explores more vocabulary.
- Add a baseline comparison against Thomas et al. (2025) for hidden-state inversion.
- Resolve the naming inconsistency.

## Removed Points
These points from the input review were not carried forward because they either misread the paper, violated hard rules, or were found to be unsubstantiated upon verification:
- **"Linear-time guarantees are misleading / O(T|V|) not O(T)"**: The paper states the O(T|V|) bound explicitly in Theorem 3.1. Calling O(T|V|) "linear" is standard when V is a fixed constant — the phrasing is precise enough for a theory paper.
- **"Injectivity of intermediate layers asserted without proof"**: The reviewer acknowledged the reasoning (lines 143–145) is logically valid. This is not a weakness.
- **"Algorithm description too high-level / POLICY is a black box"**: Algorithms 2 and 3 describing the policy are in the appendix (stripped by the parser). Deferring algorithmic details to the appendix is standard practice.
- **"Suggests rushed preparation"**: Subjective editorializing removed.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add a baseline comparison against Thomas et al. (2025) to properly position the inversion algorithm.
2. Scale up the inversion experiments and report confidence intervals on accuracy.
3. Add an analysis of when the gradient-guided policy fails (e.g., does it ever explore >1% of vocabulary?).
4. Discuss quantization results explicitly as an empirical phenomenon that extends beyond the theory's scope.
5. Resolve the naming inconsistency.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>