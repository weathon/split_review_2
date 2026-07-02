## Summary

This paper proposes a theoretical framework for understanding how semantic associations emerge in attention-based transformers during training. Using a gradient leading-term expansion, the authors derive closed-form expressions for weight matrices (output, value, query-key, positional encodings) in terms of three interpretable corpus statistics: bigram mapping (B̄), interchangeability mapping (Σ_Ḃ), and context mapping (Φ̄). The theory is validated on a 3-layer attention-only transformer trained on TinyStories (achieving cosine similarities of 0.998–0.999 between theoretical and learned weights) and extended qualitatively to Pythia-1.4B through covariance comparisons.

## Strengths

- **Novel theoretical derivation producing closed-form weight expressions.** The gradient leading-term analysis yields explicit formulas for transformer weight matrices (Eqs. 5–8) as compositions of corpus statistics. This is a genuine theoretical contribution that goes beyond prior work by handling positional encodings, causal masking, and residual streams, and by working with natural language distributions rather than synthetic data. The theorem's ability to characterize all layers uniformly before they differentiate is an interesting finding.

- **Remarkably strong empirical fit for the 3-layer architecture it was designed for.** Table 1 reports minimum cosine similarities of 0.998–0.999 between the theoretical leading terms and learned weights, and Figure 4 shows these remain above 0.7 even after 100 epochs. These results are striking and demonstrate that the leading-term approximation captures real structure in the learned weights for this specific architecture and dataset.

- **Concrete, linguistically interpretable basis functions.** The decomposition into bigram mapping (B̄), interchangeability mapping (Σ_Ḃ = Ḃ^TḂ), and context mapping (Φ̄) translates abstract weight matrices into understandable linguistic quantities. Figure 5 provides illustrative examples (e.g., "red" correlating with "truck, ball, car, dress" under B̄; "fish" correlating with "pond, lake, water, sea" under Φ̄) that convincingly show the theory captures distributional-semantic structure.

## Weaknesses

### Fatal

None.

### Major

- **The theoretical guarantee covers ~5–6 gradient steps, but the paper draws conclusions about learning over the full training trajectory (100 epochs).** Computing the bound from Theorem 4.1 with the experimental parameters (η=0.005, T=200, L=3) gives s ≤ η⁻¹·min(5/(8√T), 1/(12L)) ≈ 5.6 steps. The Frobenius-norm error bounds are only formally guaranteed for this many steps. Yet experiments run for 100 epochs of SGD (many thousands of gradient steps), and the paper concludes that learned features "remain informative well beyond" the early stage (line 210). The paper acknowledges this gap but does not resolve it. Since the paper's stated goal is to explain "how semantic associations emerge during training" (line 52), the theorem can only formally speak to the first ~5 steps — a vanishingly small portion. The paper needs to either restrict its claims to the provable window or provide a separate argument (beyond the theorem) for the approximation's persistence over long training.

- **Theory assumes full-batch gradient descent; experiments use SGD with batch size 2048.** The theoretical analysis (line 84) is explicitly for full-batch GD, but the 3-layer experiments (line 210) use SGD with batch size 2048 "for computational tractability." Mini-batch noise changes gradient dynamics qualitatively and is not simply a scaled version of full-batch GD. The paper does not discuss whether or why the leading-term approximation should survive stochastic mini-batch sampling. This mismatch between theory and experiment weakens the claim that the theory is verified by the experiments, even for the 3-layer case.

- **The Pythia-1.4B validation uses an indirect methodology that cannot directly test the theory's predictions.** The theory provides expressions for weight matrices of a simplified architecture (shared QK, single head, no MLP). To bridge to Pythia (which has multi-head attention with separate Q/K/V, MLP layers, LayerNorm), the paper: (a) averages QK products across heads, (b) converts from embedding space to token space by sandwiching with E_(l,pre), and (c) compares **covariances** of the resulting matrices rather than the matrices themselves. The paper notes (line 236) that Pythia's architecture "makes it impossible to directly read off average token correlations from the weights." However, the resulting chain of transformations is so indirect that positive covariance similarity could arise from both matrices independently reflecting bigram statistics without supporting the theory's specific structural claims. The paper's conclusion that the theory "generalizes" (line 264) to practical LLMs is not well-supported by this evidence.

- **The shared query-key matrix (W^(l)) is a significant architectural departure from practical LLMs.** The architecture in Definition 3.1 uses the same matrix for both query and key projections, while GPT-style models use separate Q and K matrices. This choice is stated but not prominently discussed as a limitation. Since the theoretical characterizations depend on this shared structure, it is unclear how they would extend to standard transformer architectures with separate projections.

### Minor

- **The "first explicit characterization" claim (line 33) is stated without qualification.** Given substantial prior work on training dynamics of transformers under realistic conditions (Nichani et al., 2024; Huang et al., 2025; Bietti et al., 2023), the claim depends on how "explicit characterization" is defined. The paper legitimately differs from prior work in its setup, but the unqualified "first" framing should be softened to acknowledge connections and distinctions more carefully.

- **No variance or statistical reliability reported for the 3-layer experiments.** Table 1 reports a single "Min. Cosine" value per weight type, and Figure 4 shows a single trajectory. Given that SGD involves stochasticity, reporting results across multiple random seeds would strengthen confidence.

- **The bound's dependence on sequence length T (Eq. 7: 13s⁵η⁵T) raises a concern deferred to the appendix.** The informal theorem statement (line 106) defers the formal version to Appendix D, leaving the reader unable to assess whether hidden dependencies on |V| or other quantities affect the bound's tightness or whether the T factor makes it vacuous for longer contexts.

### Trivial

None.

## Nice-to-Haves

- A comparison against simpler baselines (e.g., raw bigram or co-occurrence matrices without the gradient leading-term derivation) would clarify whether the gradient analysis provides additional insight over standard distributional statistics.
- A dedicated limitations paragraph discussing the theory-experiment gaps (early-stage guarantee vs. full training, full-batch vs. SGD, shared QK vs. separate Q/K) would strengthen the paper's credibility.
- Full-batch GD experiments (or very large batch experiments) for the 3-layer model, even for a limited number of steps, would provide a cleaner verification of the theorem.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"No discussion of limitations"** — removed as a style/preference issue. The paper implicitly discusses limitations (e.g., line 210 on going beyond theory, line 236 on Pythia differences), and a dedicated section is not required.
- **"No comparison with alternative theories"** — removed because the paper is not framed as a comparative evaluation; the suggestion is valid but belongs in Nice-to-Haves.
- **"MLP ablation claim is presented as a finding"** — removed because the paper explicitly says "one possible hypothesis" (line 265), framing this as speculation, not a concluded finding.
- **"Three basis functions are re-descriptions of corpus statistics, not a theory of learning"** — partially removed. The core criticism mischaracterizes the contribution: the paper derives these statistics from gradient dynamics, which is a mechanistic account. The correlational-vs-causal distinction is reasonable but already implicit in the paper's framing; the retained weaknesses about the scope gap between theorem and claims capture the same concern more precisely.

## Novel Insights

The reviews surface two insights that sharpen the evaluation beyond what the paper itself provides. First, the quantitative gap between the theorem's formal guarantee (~5 steps) and the empirical validation (100 epochs) is not merely a presentation issue — it creates a structural tension between the paper's ambitious framing ("how semantic associations emerge during training") and what the mathematics can actually secure. Second, the Pythia validation methodology, while creative and necessary given architectural mismatches, is too indirect to support the claimed generality: averaging across heads, converting embedding spaces, and comparing covariances rather than matrices compounds unverified assumptions at each step. Together, these observations reframe the paper's strongest contribution as the closed-form derivation and its validation on the exact architecture it was designed for, rather than any general claim about real-world LLMs.

## Suggestions

- Compute the number of gradient steps covered by the bound for the experimental setup and explicitly report it. If the approximation holds far beyond this window empirically, discuss why this might be (e.g., higher-order terms remaining small due to specific data or architectural properties).
- Run the 3-layer experiments with full-batch GD (or a very large batch) for at least the provable window to provide a cleaner theory-experiment alignment. If this is infeasible, discuss why mini-batch dynamics are not expected to change the leading-term structure.
- For the Pythia analysis, either (a) provide a direct comparison by projecting the theoretical matrices from token space into Pythia's embedding space using the same transformation, or (b) explicitly state what each transformation step assumes and why a positive covariance result supports the theory despite these assumptions. The current text conflates "generalizing" with "producing correlated covariances."
- Add a limitations paragraph acknowledging the architectural simplifications (shared QK, single head, no MLP, full-batch assumption) and the gap between theoretical guarantee and empirical scope.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Reject</decision>