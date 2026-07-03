Now I have all the information I need. Let me produce the final consolidated review.

## Summary

This paper investigates how the L0 hyperparameter (average number of active latents per token) in sparse autoencoders (SAEs) affects whether the SAE learns correct, monosemantic features. Using controlled toy models with known ground-truth features, the authors demonstrate that L0 values below the true L0 cause the SAE to mix correlated features together ("feature hedging"), and crucially, that the standard sparsity-reconstruction tradeoff plot is actively misleading — a ground-truth correct SAE scores *worse* on reconstruction than a trained SAE that cheats by mixing features (MSE 4.88 vs 2.73 at low L0). The paper proposes a diagnostic metric (decoder pairwise cosine similarity, c_dec) and validates it in LLMs against sparse probing performance across two models (Gemma-2-2b, Llama-3.2-1b).

## Strengths

- **Toy-model demonstration that the sparsity-reconstruction tradeoff is unsound (Section 3.4, Figure 4):** The paper constructs a ground-truth SAE with the correct dictionary and shows it scores *worse* on reconstruction than a trained SAE at every L0 below the true L0. This directly falsifies the foundational assumption — used by several prior SAE papers (Cunningham et al., 2024; Gao et al., 2024; Rajamanoharan et al., 2024) — that better reconstruction at a given sparsity implies a better SAE. This is the paper's strongest and cleanest contribution.

- **Clean causal isolation of L0's effect on feature mixing (Section 3.1, Figures 2-3):** The paper initializes a low-L0 SAE to the ground-truth solution before training, ruling out the possibility that the observed feature mixing is merely a local-minimum artifact. The decoder cosine-similarity heatmaps directly visualize how the SAE systematically mixes correlated (and anti-correlated) feature components. The paper tests both positively and negatively correlated features, which matters because the authors argue negative correlations are prevalent in language.

- **Empirical alignment between c_dec and downstream task performance in LLMs (Section 4, Figure 8):** For both Gemma-2-2b (layer 5) and Llama-3.2-1b (layer 7), the "elbow" in the c_dec curve — the point just before the sharp rise at low L0 — coincides with peak k=16 sparse probing F1 scores across 100+ tasks. This provides cross-model validation that the toy-model phenomenon manifests in real SAEs and that c_dec can guide practitioners toward a reasonable L0. Results are shown with 3 seeds per L0.

- **JumpReLU SAE "sticking" phenomenon (Section 3.6, Figure 7):** The observation that JumpReLU SAEs' L0 does not vary linearly with λ_s but instead "sticks" near the true L0 over a wide range of λ_s values is a novel empirical finding. It offers a plausible explanation for why JumpReLU SAEs trained with Anthropic's procedure (Conerly et al., 2025) may be more robust to misspecified sparsity coefficients.

## Weaknesses

### Major

- **LLM validation is correlational (c_dec vs sparse probing), not a direct test of feature correctness:** In the toy model, c_dec is validated because ground-truth features are known. In the LLM experiments, validation is against k-sparse probing F1 scores — a measure of whether SAE features are useful for linear classification on 100+ probing tasks. A high sparse-probing score is consistent with correct features, but also with features that happen to be useful for those specific classification tasks while still being corrupted in other ways. The paper does not provide a more direct test (e.g., case studies of individual latents showing the predicted mixing pattern in LLMs). This gap means the paper is strong as a cautionary study (the toy model shows a real problem exists) but weaker as a prescriptive method (the LLM evidence for c_dec is correlational).

- **"Correct L0" is ambiguously defined in real LLMs, limiting the metric's practical precision:** In the toy model, "correct L0" is the average number of ground-truth features firing. In real LLMs, there is no analogous ground truth. The paper acknowledges c_dec "is not a perfect guide" and that it can remain "nearly flat for a wide range of L0" (Gemma-2-2b layer 5, Figure 8 — flat from roughly L0=200 to L0=2000). The paper uses the "elbow" before the sharp rise at low L0 rather than the global minimum, which is a reasonable heuristic but not derived from theory. The practical guidance is therefore effective at detecting "too low" L0 but less informative for distinguishing among moderate-to-high L0 values.

- **Claim that "most SAEs used by researchers today have too low an L0" is weakly supported:** This claim appears in the abstract (line 37) and discussion (line 240), but is supported only by "a cursory search of open source SAEs on Neuronpedia" relegated to Appendix A.13. This is a strong claim about widespread practice; it deserves either a systematic survey or a softened framing.

### Minor

- **The "too high L0" failure mode is architecture-dependent, which the title/abstract framing does not fully reflect:** The paper's title ("Sparse But Wrong") and abstract treat low and high L0 as roughly symmetric failure modes. Yet the paper's own evidence (Section 4.1, Figure 9) shows JumpReLU SAEs have only modest c_dec increases at high L0 and maintain strong sparse probing performance, while BatchTopK SAEs degrade significantly. The paper explicitly attributes this to JumpReLU's per-latent thresholds and the "sticking" phenomenon. The data is clear; the disconnect is in the framing. The "too high L0" failure mode is verified for BatchTopK but not shown to be a universal property of SAEs.

- **"Every latent is affected" claim at low L0 is supported only qualitatively:** The paper claims (Section 3.2, line 107) that at low L0, "every latent in the SAE is affected." This is based on visual inspection of scatter plots (Figure 1) rather than a quantitative per-latent degradation measure. While the qualitative evidence is visually compelling, a quantitative measure would strengthen the claim.

- **No dedicated Limitations section:** The paper integrates some caveats into the Discussion (Section 6), but a focused Limitations section would help readers calibrate the strength of the LLM evidence. Specific issues worth discussing include: the correlational nature of LLM validation, the challenge of identifying the "correct" L0 in practice beyond the "too low" regime, and the limited number of layers and models tested (2 models, ~2-3 layers analyzed with c_dec).

### Trivial

None.

## Nice-to-Haves

- Case studies showing the specific feature-mixing pattern (latents containing components of correlated features) in LLM SAEs with low L0 would concretely bridge the toy model and LLM regimes.
- A quantitative per-latent degradation measure to support the claim that "every latent is affected."
- A brief discussion in the main text about whether c_dec could be adapted for single SAEs (not requiring a sweep) — currently deferred to Appendix A.11.

## Removed Points

These points were flagged by reviewers but set aside with justification:

- *"c_dec theoretical justification deferred to appendix"*: Standard practice in papers with space constraints; the main text provides the intuition.
- *"5-feature toy model is too simple"*: The paper explicitly scales to 50 features in Section 3.2, so this concern is addressed.
- *"The distinction between this work and Chanin et al. on feature hedging could be sharper"*: The paper clearly distinguishes width-based hedging (Chanin et al.) from L0-based hedging (this work) in Section 5.
- *"Too high L0 problem is less severe than framing suggests"* (harsh critic wording): This is accurate as a framing observation but the paper's own evidence establishes the asymmetry. Moved to Minor as a framing issue rather than a separate weakness.
- *Formatting/style nitpicks*: Parser artifacts, not author errors.
- *Strength Finder strengths about "important problem" or generic praise*: Removed as not specific to this paper's content.

## Novel Insights

The reviews surface one insight not fully emphasized in the paper: the asymmetry between "too low" and "too high" L0. The low-L0 failure is universal across architectures (BatchTopK and JumpReLU both degrade severely), while the high-L0 failure is architecture-dependent (JumpReLU is largely robust due to per-latent thresholds). This distinction — that low L0 is always harmful while high L0 is harmful only under certain architectural choices — is a more precise framing than the paper's symmetrical treatment and deserves sharper articulation.

## Suggestions

1. **Add a dedicated Limitations section** discussing the correlational nature of LLM validation, the ambiguity in identifying the "correct" L0 from c_dec in practice, and the limited model/layer coverage.
2. **Either systematically survey existing SAEs' L0 values or soften the claim** that "most SAEs used by researchers today have too low an L0." The current phrasing overstates what the evidence supports.
3. **Reframe the "too high L0" finding** to acknowledge its architecture-dependence more explicitly in the abstract and title (or at least avoid suggesting the two failure modes are symmetric).
4. **Consider adding case studies** of individual latents from low-L0 LLM SAEs to directly demonstrate the predicted feature-mixing pattern (e.g., a latent that activates on two negatively correlated concepts simultaneously).
5. **Provide a quantitative per-latent degradation measure** in the larger toy model to complement the qualitative scatter-plot evidence.

## Score and Decision

Based on my reading, this is a solid empirical paper with a genuine and well-demonstrated core contribution (the sparsity-reconstruction tradeoff is actively misleading). The toy-model evidence is clean and compelling. The LLM evidence is correlational but still informative. The main weaknesses are framing issues (overstating symmetry, weakly supporting the "most SAEs" claim) and the gap between the strong toy-model results and the weaker LLM validation. None of the weaknesses are fatal — they do not invalidate the core claim, which is well-supported by the toy model alone. The paper makes a timely, actionable contribution to the SAE community.

I calibrate this paper in the **borderline accept to accept** range. The core finding matters and is solidly demonstrated; the limitations are real but do not undermine the central contribution. I assign a score of **6.5**.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>