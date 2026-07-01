Now I have all the calibration I need. Let me write the final review.

Calibration anchors (all from human-review corpus):
1. "Scaling and evaluating sparse autoencoders" (Avg: 8.20, Accept) — The influential TopK SAE paper with broad scaling laws; our paper is less impactful and narrower in scope.
2. "Sparse Autoencoders Do Not Find Canonical Units" (Avg: 7.00, Accept) — Novel stitching/meta-SAE methodology critiquing SAE assumptions; similar genre, but technically deeper.
3. "Towards Principled Evaluations of Sparse Autoencoders" (Avg: 7.00, Accept) — Systematic SAE evaluation framework; comparable quality but more thorough.
4. "Incidental Polysemanticity" (Avg: 5.67, Reject) — Theory + toy model critique, rejected for limited real-model applicability; our paper has stronger empirical validation.

Round 1 bracket: 5.5–7.5. After narrow comparison: our paper sits between "Incidental Polysemanticity" (5.67, less validated) and the 7.00 papers (deeper methodology or broader evaluation). Final score: 6.5 — a solid borderline accept.

---

## Summary

This paper studies how the L0 sparsity hyperparameter in Sparse Autoencoders (SAEs) affects feature quality. Using toy models with known ground-truth features, the authors demonstrate that if L0 is set too low, SAEs mix correlated features to improve reconstruction — creating a situation where standard sparsity-reconstruction tradeoff plots favor incorrect, hedging solutions over correct ones. They propose a decoder pairwise cosine similarity metric (c_dec) to detect when L0 is too low, and validate on Gemma-2-2b and Llama-3.2-1b SAEs using sparse probing.

## Strengths

1. **Clean toy model with ground-truth verification (Section 3).** The paper constructs a synthetic setup where features are orthogonal, firing patterns are controlled by a known correlation matrix, and the true L0 is known by construction. This enables direct measurement of whether the SAE recovers true features — which is impossible in real LLMs. The demonstration that a trained SAE beats the ground-truth SAE on MSE at low L0 (MSE 2.73 vs 4.88 at L0=5, Section 3.3) is a crisp causal proof that reconstruction alone is a misleading metric when L0 is misspecified.

2. **Important finding about sparsity-reconstruction tradeoff plots (Section 3.4, Figure 4).** The ground-truth SAE — which perfectly captures the underlying features — scores *worse* on variance explained than a trained SAE at any L0 below the true value. This is the paper's most important result: it shows that if practitioners rely on sparsity-reconstruction curves to compare SAE architectures, they would systematically reject correct solutions in favor of cheating ones. This is a non-obvious and practically consequential finding.

3. **Low-L0 vs high-L0 asymmetry (Section 3.2).** The observation that low L0 corrupts *every* latent while high L0 leaves many latents intact is a useful practical insight, well-supported by the toy model experiments.

## Weaknesses

### Major

1. **c_dec metric is not operationalized for practical use.** The paper acknowledges that c_dec "can sometimes remain nearly flat for a wide range of L0" (Section 6), and the Gemma-2-2b Layer 5 results (Figure 8) confirm this: the curve drops from ~0.030 to ~0.020 by L0=250 and then stays flat. The paper resorts to identifying an "elbow" by eye as the recommended L0, which is not a reproducible criterion. The sparse probing F1 curves are also quite flat (F1 varies from ~0.78 to ~0.82 across L0=0–2000), and no statistical testing is reported. Without an algorithmic procedure for choosing L0 from a flat c_dec curve, the metric's utility for practitioners is limited.

2. **Claims about "most SAEs" having too low L0 outpace the experimental evidence.** The paper states that "most SAEs used by researchers today have too low an L0" (abstract, Section 6), but the LLM experiments cover only two models (Gemma-2-2b, Llama-3.2-1b), at one or two layers each, with one dictionary size (h=32768). The broader claim is supported only by a "cursory search of open source SAEs on Neuronpedia" (Section 6). How the optimal L0 varies with model scale, layer depth, or dictionary width is unaddressed.

### Minor

3. **Toy model assumptions not stress-tested.** Features are perfectly orthogonal (line 65), whereas the LRH posits features are only "nearly orthogonal" (line 13, 59). The SAE dictionary size equals the number of true features (g=h), whereas real SAEs are overcomplete. No sensitivity analysis is provided to show how the c_dec diagnostic degrades as these assumptions are relaxed. Additionally, line 99 states "every SAE latent will contain positive components of every positively correlated feature... in the model," which extrapolates beyond the hub-and-spoke correlation structure actually demonstrated in the toy model's experiments.

4. **Tension between "single correct L0" framing and per-latent evidence.** The paper is framed around finding "the correct L0," but Section 4.2 shows that at L0=750 on Gemma-2-2b, some latents become more monosemantic while others mix features, and the paper states "there is likely a range of L0s where some latents are firing more than they ideally should while other latents are firing less than they ideally should." This tension between global-L0 framing and per-latent sparsity needs is acknowledged but not resolved.

5. **Different architectures give different c_dec minima.** For Gemma-2-2b Layer 12 (Figure 9), BatchTopK SAEs have a c_dec minimum around L0=200 while JumpReLU SAEs have a minimum around L0=250–300. This introduces ambiguity about which L0 is "correct" if the metric is architecture-dependent.

### Trivial

None.

## Nice-to-Haves

- Operationalize the c_dec metric with a threshold or algorithm (e.g., "choose the smallest L0 such that c_dec is within X% of its minimum").
- Add sensitivity experiments varying feature orthogonality and dictionary overcompleteness in the toy model.
- Investigate whether JumpReLU's per-latent threshold adaptation (shown in toy models to "stick" near the correct L0) mitigates the global-L0 problem at scale.

## Removed Points

- **JumpReLU "self-correction" limits scope (Reviewer Critical Issue 1, part 2).** The reviewer argues that JumpReLU's L0 "sticking" means the paper's alarm applies mainly to BatchTopK. However, even with JumpReLU, practitioners must choose λ_s, and Figure 9 shows JumpReLU exhibits the same c_dec spike at low L0. The paper's core point — that L0 matters — applies to all architectures.
- **Related work distinction from Chanin et al. (Section 5 criticism).** The paper explicitly states "We consider our work a version of feature hedging due to low L0." This is a clear, honest positioning, not a gap.
- **"No discussion of computational cost."** This asks for content beyond the paper's stated scope and is not a core weakness.
- **"No ablation with random initialization of the L0=1.8 SAE."** The paper intentionally initialized to the ground-truth solution to isolate gradient pressure — this is a deliberate experimental design choice, not an omission.
- **Criticisms about missing appendix content (A.6, A.13, A.16).** These are parser artifacts; the appendix exists in the original submission.
- **Section 3.4 framing criticism ("correct means orthogonal decoder vectors").** This is the entire point of the toy model as a controlled experiment with known ground truth.
- **"Missing related works."** Not included per policy — I cannot verify the existence of works not cited in the paper.

## Novel Insights

The core insight — that sparsity-reconstruction tradeoff plots can systematically favor incorrect SAEs that hedge correlated features over correct SAEs — is novel and well-demonstrated. The paper provides a causal proof (Section 3.3) that MSE loss actively incentivizes feature mixing at low L0, which goes beyond the correlational evidence in prior work on feature hedging (Chanin et al., 2025). The asymmetry between low and high L0 (low L0 corrupts all latents; high L0 corrupts only some) is also a useful and non-obvious distinction for practitioners.

## Suggestions

1. Reframe the contribution to acknowledge that per-latent sparsity needs likely vary, and that c_dec is a useful heuristic for avoiding severely low L0 rather than a method for locating a single "correct" L0.
2. Provide an algorithmic procedure for picking L0 from a c_dec curve (e.g., "the smallest L0 where the derivative of c_dec with respect to L0 falls below a threshold").
3. Either broaden the LLM experiments (more models, layers, dictionary widths) or temper the claim about "most SAEs" to what the data actually supports.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>