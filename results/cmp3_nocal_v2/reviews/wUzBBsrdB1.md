## Summary

This paper investigates the effect of the L₀ hyperparameter (average number of active latents per token) on Sparse Autoencoder (SAE) quality. Through toy model experiments where ground-truth features are known, the authors demonstrate that (a) low L₀ incentivizes SAEs to mix correlated features to improve reconstruction, producing polysemantic latents that score better on MSE than the ground-truth solution, and (b) sparsity-reconstruction tradeoff plots can therefore rank incorrect SAEs above correct ones. They propose a proxy metric, decoder pairwise cosine similarity (c_dec), that detects when L₀ is too low, and validate it on Gemma-2-2b and Llama-3.2-1b SAEs against sparse probing performance.

---

## Strengths

1. **Clean toy-model demonstration that low L₀ incentivizes incorrect features (Section 3.3).** The trained SAE at L₀=5 achieves MSE 2.73 while the ground-truth SAE (with correct, disentangled features) achieves 4.88. This is a crisp, falsifiable demonstration that sparsity-reconstruction tradeoff plots can be actively misleading — a result that holds regardless of what one thinks about the LLM experiments.

2. **Ground-truth initialization control (Section 3.1).** Initializing the low-L₀ SAE at the ground-truth solution and watching gradient pressure push it away from correctness is a strong experimental design. It cleanly separates "the solution is hard to find" from "the loss landscape actively penalizes the correct solution at this L₀."

3. **Important practical observation that *low* L₀ (not just high L₀) degrades SAE quality.** The argument that sparsity-reconstruction tradeoffs are unsound when L₀ is too low is well-supported by the toy model evidence and is a genuine contribution that changes how practitioners should think about hyperparameter selection.

---

## Weaknesses

### Fatal
None.

### Major
1. **c_dec's utility on real LLMs is more limited than the framing suggests.** The paper's own results show that for Gemma-2-2b Layer 5 (Figure 8, top-left), the c_dec curve drops sharply and then goes **completely flat** from L₀ ≈ 250 to L₀ ≈ 2000 — an 8× range where the metric cannot distinguish between settings. The paper's discussion acknowledges this ("the metric can sometimes remain nearly flat"), but the abstract and introduction frame c_dec primarily as a method for finding the correct L₀. In practice, c_dec reliably detects *obviously-too-low* L₀ (the sharp rise) but does not reliably identify a unique correct L₀. The toy model where c_dec cleanly bottoms out at the true L₀ is not representative of the LLM behavior. This is a real gap between the paper's framing and what the evidence supports.

2. **The claim that "most commonly used SAEs have an L₀ that is too low" is not well-supported by the presented experiments.** This claim appears in the abstract (line 9), introduction (line 37), and discussion (line 240), but the evidence consists of (a) SAEs trained at two layers of two small models (Gemma-2-2b and Llama-3.2-1b) at one width (32768), and (b) a "cursory search of open source SAEs on Neuronpedia" relegated to an appendix. Whether the finding transfers to larger models (e.g., Gemma-2-27b), deeper layers, wider SAEs, or different training distributions is not addressed. This claim should be substantially softened or explicitly qualified to the settings studied.

### Minor
3. **No formal statistical tests on LLM results.** Figures 8 and 9 show 3 seeds per L₀ value for sparse probing F1 scores, but no error bars or significance tests are reported. Given that the F1 differences between peak and high L₀ are modest (~0.82 vs ~0.78), it is unclear whether these differences are statistically meaningful.

4. **JumpReLU SAEs partially mitigate the problem.** The paper's own Figure 7 and Section 3.6 show that JumpReLU SAEs' L₀ "sticks" near the correct value across a wide range of sparsity coefficients. In LLM experiments (Figure 9), JumpReLU SAEs show much less c_dec rise at high L₀ and correspondingly better sparse probing performance. The paper is transparent about this (calling it "a testament to Anthropic's JumpReLU SAE training method"), but the headline claim about "most commonly used SAEs" does not distinguish between architectures. Many commonly used SAEs are JumpReLU, which significantly narrows the scope of the strongest warning.

### Trivial
5. The statement at line 99 — "if our L₀ is too low, every SAE latent will contain positive components of every positively correlated feature, and negative components of every negatively correlated feature" — is presented as a universal conclusion from a 5-feature toy model with a single correlation pattern. While the intuition is reasonable, the paper should specify the conditions under which this pattern holds.

---

## Nice-to-Haves

- Frame c_dec primarily as a diagnostic for detecting *obviously-too-low* L₀ (a useful lower bound) rather than as a method for pinpointing a unique optimal L₀. The paper's own discussion already leans in this direction; the abstract and introduction should follow suit.
- Provide a practical rule-of-thumb for L₀ relative to dictionary size (e.g., L₀ as a fraction of h or of input dimension d), if the data support it.
- Report whether the 100k samples used for the MSE comparison (Section 3.3) versus 15M for other toy experiments represents a meaningful difference. (On inspection, the 100k samples are for *evaluation* of already-trained SAEs, not training, so this is likely fine — but an explicit note would help.)

---

## Removed Points

These points from the harsh critic were removed or demoted to the Nice-to-Haves section after cross-checking against the paper:
- **"The c_dec metric's utility is substantially weaker than the framing suggests (methodological gap)"** — partially kept as Major #1 above. The portion claiming the metric "cannot distinguish between L₀=250 and L₀=2000" and that the paper "underplays this" was retained; the portion claiming the paper's practical value is marginal was removed because the paper's Discussion (lines 244-248) already honestly acknowledges this limitation.
- **"The 'true L₀' concept does not cleanly transfer to LLMs"** — removed because the paper does not claim to find a "true L₀" in LLMs. It validates c_dec against sparse probing performance, an operational criterion. The paper explicitly notes that real features may not be perfectly linear (citing Engels et al., 2025).
- **"No comparison against alternative SAE quality metrics"** — removed. The paper validates against sparse probing, which is a downstream task metric. A comprehensive comparison against interpretability scores, dead latent fractions, etc., would be a separate contribution. The paper's scope is the c_dec metric and its relationship to sparse probing.
- **"JumpReLU 'sticking' result undermines the paper's own framing"** — demoted to Minor #4. The paper openly discusses this as a positive finding about JumpReLU training. It does not "undermine" the paper's core claim (that L₀ matters); it supports it by showing that some architectures handle it better.
- **"100k vs 15M sample inconsistency"** — removed. The 100k samples in Section 3.3 are for *evaluation* of already-constructed/frozen SAEs, not for training. This is sufficient for computing MSE.
- **"Missing appendix content (A.13, A.9)"** — removed. Appendices are stripped by the PDF parser; they exist in the original submission.
- **"No error bars"** — kept as Minor #3 but softened. The paper does show shading for 5 seeds in Figure 6 and notes 3 seeds in Figure 8; the criticism is that formal significance testing is absent.

---

## Novel Insights

Beyond the paper's own contributions, the review surfaces one genuinely novel observation: the c_dec metric has a fundamentally different *shape* in toy models (clean V-shape with a unique minimum) versus real LLMs (sharp drop then flat plateau). This suggests that LLM features have a correlational structure that is qualitatively different from the simple orthogonal-feature toy model — specifically, that there may be a wide range of "acceptable" L₀ values where feature mixing does not worsen, rather than a single correct value. This observation is not made explicitly in the paper and could motivate future work on whether LLM features have a hierarchical or multi-scale structure that makes the L₀ selection problem genuinely different from what the toy model captures.

---

## Suggestions

1. Soften the "most commonly used SAEs have too-low L₀" claim to match the evidence presented, and qualify it to the specific architectures (BatchTopK) and settings (32768-width SAEs on Gemma-2-2b/Llama-3.2-1b) studied.
2. Reframe c_dec in the abstract and introduction as a diagnostic that reliably detects *obviously-too-low* L₀, rather than a method for finding the unique correct L₀.
3. Add error bars or confidence intervals to the LLM sparse probing results, or at minimum report the variance across seeds for the key comparisons.
4. Acknowledge more prominently that JumpReLU SAEs appear less vulnerable to the L₀ problem, and that the paper's strongest warnings apply primarily to TopK/BatchTopK architectures.

---

## Score and Decision

The paper makes a genuine and well-demonstrated contribution: it shows through clean toy-model experiments that low L₀ causes feature mixing, that sparsity-reconstruction tradeoff plots can therefore be misleading, and that c_dec can detect problematic L₀ values. These results are important for the SAE community. However, the paper overclaims in two ways: the c_dec metric's utility on real LLMs is more modest than the abstract suggests, and the claim about "most commonly used SAEs" goes beyond what the experimental evidence supports. The paper should be accepted if these claims are calibrated to match the evidence; as written, the gap between the strongest claims and the evidence is notable but does not undermine the core contribution.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>