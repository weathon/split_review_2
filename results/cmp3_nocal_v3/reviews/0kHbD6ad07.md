## Summary

This paper proves that causal decoder-only Transformer language models are almost-surely injective: distinct prompts produce distinct last-token hidden states. The proof uses real-analyticity of transformer components and the dichotomy that real-analytic functions are either identically zero or have measure-zero zero sets. Injectivity is established at initialization and the paper argues it is preserved under gradient-based training. Building on this property, the paper introduces SIFT (SIPIT), an algorithm that recovers the exact input prompt from hidden states with linear-time worst-case guarantees. Empirical validation includes billions of collision tests across six models (GPT-2 family, Gemma-3, Llama-3.1-8B, Mistral-7B, Phi-4-mini, TinyStories-33M) finding no collisions, plus inversion experiments demonstrating exact recovery.

## Strengths

1. **Elegant proof strategy via real-analyticity (§2).** Applying the zero-set dichotomy of real-analytic functions to the squared distance function \(h(\theta) = \|\mathbf{r}(s;\theta) - \mathbf{r}(s';\theta)\|_2^2\) is a clean way to reframe the injectivity question. This avoids messy case analysis over architectural components and correctly exploits the discrete-to-continuous framing (prompts → last-token states) that makes the result work.

2. **Thorough empirical collision search (§4.1).** Testing approximately 5 billion pairwise comparisons across GPT-2 (S/M/L), Gemma-3 (1B/4B/12B), Llama-3.1-8B, Mistral-7B, Phi-4-mini, and TinyStories-33M, and finding no collisions with minimum distances well above \(10^{-6}\), is compelling supporting evidence. The additional experiments with FP4/INT8 quantization (Tables 2–3) and the sequence-length analysis (Figure 5) are well-designed and strengthen the empirical case considerably.

3. **The central claim is genuinely counterintuitive and well-motivated (§1).** The paper correctly identifies the widespread intuition that nonlinearities, normalization, and many-to-one attention cause information loss, and challenges it directly. The discrete-to-continuous reframing (prompts → last-token states rather than a map within \(\mathbb{R}^d\)) is the right framing to make the result work.

## Weaknesses

### Major

1. **Training-preservation proof sketch has an unsubstantiated claim in the main text (§2, Theorem 2.3).**  
The argument that gradient descent preserves injectivity relies on the claim that the Jacobian determinant \(\det D\phi(\theta)\) of the GD update map is "not identically zero (one can check this by evaluating at a simple parameter setting)." The paper does **not** provide this evaluation or even sketch what such a setting would look like. For the argument to be complete, one must exhibit at least one \(\theta_0\) where \(I - \eta H_{\mathcal{L}}(\theta_0)\) is invertible. The paper simply asserts this can be done. Since the full proof is relegated to the appendix (Theorems C.1 and C.5, stripped during parsing), the main text is incomplete on its own. This matters because the paper's stated advance over Sutter et al. (2025) — which already proved injectivity at initialization — is precisely the extension *under training* (§5: "crucially, we show that injectivity is not an initialization artifact but persists under training"). **Why it matters:** The paper's main theoretical claim over prior work rests on this step. However, the empirical evidence (billions of collision tests on trained models showing no collisions) independently supports the conclusion, so this is a gap in the proof presentation rather than a refutation of the claim.

2. **The empirical comparison is not calibrated to the task (§4.2, Table 5).**  
HARDPROMPTS (Wen et al., 2023) is a method for *prompt optimization* (finding prompts that maximize a downstream score), not for exact prompt *reconstruction* from hidden states. Reporting that it achieves 0% accuracy at this task is not a meaningful comparison — the method was never designed for this. Meanwhile, the paper mentions Thomas et al. (2025) in Related Work as "most closely related to ours" — a method that also recovers prompts from hidden states — but does not include it as an empirical baseline. The BRUTEFORCE ablation is reasonable, but the evaluation would be far more informative if it compared against the most related prior inversion method. **Why it matters:** Without a comparison against a method designed for the same task, the empirical case for SIFT's practical advantage over existing inversion approaches is not fully made.

3. **Small sample sizes for inversion experiments (§4.2).**  
The main inversion experiment uses only 100 prompts, and the robustness experiment uses only 50. While 100% accuracy is reported, the sample is small enough that the variance is not captured. Testing on substantially more prompts (e.g., 1000+) would be straightforward and would significantly strengthen the statistical basis of the claims. **Why it matters:** The claim that SIFT achieves exact recovery in practice would benefit from larger-scale validation.

### Minor

1. **The SIFT algorithm is largely a direct corollary of injectivity plus causal structure (§3).**  
Given injectivity and the causal masking property, the algorithm reduces to iterating over the vocabulary at each position and checking for a match. The \(O(T|\mathcal{V}|)\) worst-case bound is the brute-force bound, and the algorithm's correctness follows directly from the injectivity guarantee. The gradient-guided heuristic reduces average-case cost, but it is not theoretically analyzed and the mechanism is not explained in the main text (it references only Algorithms 2 and 3 in the stripped appendix). The paper's framing as "the first algorithm that provably reconstructs the **exact** input text" is accurate but the algorithmic contribution is modest relative to the theoretical one.

2. **The threat model and practical significance of the inversion are not fully delineated (§3, §6).**  
The paper requires both (a) full model parameter access and (b) hidden states at some layer. The privacy discussion in §6 argues that hidden states "are effectively handling the user's verbatim text" but does not adequately acknowledge that SIFT requires model weights — a non-trivial access assumption. The paper states it "does not define a full adversarial model" (§3), which is reasonable for a theory paper, but the subsequent privacy implications are discussed without scoping the access requirements. The result is less a practical privacy threat and more a theoretical demonstration of information preservation.

3. **The claim that quantization "more than doubles the minimum distance" is reported without explanation (§4.1).**  
Tables 2–3 show that FP4/INT8 quantized models have larger minimum distances than FP32 models. This is an interesting observation but the paper offers no hypothesis or analysis for why quantization would *increase* separation. It is unclear whether this is a general phenomenon or an artifact of the specific models and quantization schemes tested.

### Nice-to-Haves

- **Empirical comparison against Thomas et al. (2025)** would make the inversion evaluation more complete, since Thomas et al. works in the same setting (hidden states + model access) and is the closest prior work.
- **Explanation of the gradient-guided search mechanism in the main text** (rather than only in the appendix) would improve readability and help readers understand why the algorithm explores only ~0.2% of the vocabulary.
- **The paper could strengthen credibility by downgrading the training-preservation claim from an unconditional theorem to a result conditional on the full appendix proof** or by noting that the empirical evidence independently supports the conclusion. As written, the main text claims a theorem with an incomplete sketch.

### Trivial

- The algorithm is called "SIFT" in the abstract and "SIPIT" in §3 — a minor naming inconsistency the authors should harmonize.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"The SIFT algorithm is essentially brute-force search, not a meaningful inversion method"** — Overstated. While the worst-case is brute force, the gradient-guided heuristic achieves practical efficiency (~0.2% vocabulary explored). The algorithm is not a major algorithmic innovation, but it is a correct and useful operationalization of the theoretical result.
- **Criticism about missing reproducibility details (dataset splits, seed information, floating-point precision, tolerance \(\varepsilon\))** — These are standard nitpicks that the rule set instructs to remove. The paper describes the dataset mixture and experimental setup at a reasonable level for a conference submission.
- **"Algorithm 2 and 3 are referenced but the appendix is not available"** — The parser strips appendix content. The full algorithm descriptions exist in the original submission.
- **Criticism that the training-preservation argument is "fatal" / "structural gap"** — The full proof is in the appendix (which cannot be accessed due to parsing). The empirical evidence independently supports the claim. The gap in the main-text sketch is a real concern but does not invalidate the paper's broader contribution. Downgraded from fatal to major.

## Novel Insights

The most insightful observation from the review process is that the paper's proof strategy via real-analyticity cleanly sidesteps the usual difficulties of analyzing transformer information flow. By treating the model as a parameter-to-representation map and exploiting the analytic dichotomy, the paper converts a question about discrete input separation into a tractable continuous analysis. This framing — that what matters is not whether individual components are injective but whether the *difference function* can be identically zero across parameters — is a genuinely useful perspective that could be applied to other architectural analyses. The review also surfaces the fact that the main tension in the paper is between its ambitious theoretical claim (training preservation via GD) and the more modest evidence it provides for that specific sub-claim in the main text, versus the very strong empirical evidence that the property holds in practice regardless.

## Suggestions

1. **Complete the training-preservation proof in the main text** by either (a) providing the explicit parameter construction that shows \(\det D\phi \not\equiv 0\), or (b) relaxing the claim — e.g., proving injectivity only at initialization (building on Sutter et al. 2025) and treating training preservation as an empirical finding supported by the collision search, which already covers trained models.
2. **Replace or supplement the HARDPROMPTS baseline** with a comparison against Thomas et al. (2025) or another method designed for prompt reconstruction from hidden states.
3. **Increase the sample size** for inversion experiments (from 100/50 to at least 1000 prompts) to improve statistical confidence.
4. **Provide a brief sketch of the gradient-guided search mechanism** in the main text (even 2–3 sentences) so readers can understand why the algorithm is efficient without consulting the appendix.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>