The calibration corpus path is inaccessible. I'll proceed with my judgment based on the paper content and review analysis.

Let me now compile the final review.

---

## Summary

This paper proves that decoder-only Transformer language models are almost surely injective — different prompts map to distinct last-token hidden states — both at initialization and after training with gradient descent/SGD. The proof relies on real-analyticity of Transformer components and measure-theoretic arguments. Building on this, the paper introduces SIFT, an algorithm for exact input reconstruction from hidden states with provable linear-time guarantees. Experiments on six models (~5B pairwise comparisons) find zero collisions, and inversion tests achieve 100% token accuracy while exploring <0.22% of the vocabulary.

## Strengths

1. **Theoretical proof that injectivity persists through training, not just at initialization.** Theorem 2.3 and its corollaries go beyond Sutter et al. (2025), which only proved injectivity at initialization and for the full hidden-state matrix. The use of real-analyticity and the Inverse Function Theorem to show that GD/SGD updates preserve absolute continuity of the parameter distribution is a clean and nontrivial argument.

2. **SIFT algorithm with provable linear-time exact reconstruction.** Theorem 3.1 guarantees correctness in at most \(T|\mathcal{V}|\) steps. Empirical results (Table 5) show 100% token-level accuracy at ~28s mean runtime vs. ~3889s for brute force. This is the first algorithm to offer provable exact recovery from hidden states in decoder-only LMs.

3. **Large-scale collision search across diverse model families.** ~5 billion pairwise comparisons across 6 models (GPT-2, Gemma-3, Llama-3.1, Mistral-7B, Phi-4, TinyStories) find zero collisions, with minimum L2 distances orders of magnitude above machine epsilon in all layers (Tables 1–3, Figure 3). This provides strong empirical support.

4. **Quantization robustness.** FP4 and INT8 quantization does not introduce collisions and often increases minimum pairwise distances (Table 2: Llama-3.1-8B min distance increases from 1.274 to 6.597 with INT8). This non-obvious finding extends practical relevance to compressed deployment scenarios.

5. **Gradient-guided search efficiency.** Table 4 shows SIFT achieves 100% accuracy while exploring <0.22% of the vocabulary, empirically confirming the linear-time complexity bound with a tiny constant factor.

## Weaknesses

### Fatal
None.

### Major

1. **Optimizer coverage gap between theory and practice.** The training-preservation result (Theorem 2.3, Corollary 2.3.1) is proved only for gradient descent and SGD/mini-batch GD. The paper never mentions Adam — the de facto optimizer for all modern LMs tested (GPT-2, Gemma, Llama, Mistral, Phi). While the theorems explicitly state "gradient descent" and "SGD," the abstract, introduction, and discussion use broader language: "common training procedures (gradient descent with standard step sizes)" (line 31) and "under standard initialization and training" (line 345). This framing does not acknowledge the gap between the optimizer for which the theory holds (GD/SGD) and the optimizer used for the tested models (Adam). The empirical results do confirm injectivity in practice, but a clear statement of this limitation is expected. **This is fixable in revision** — the paper should add a sentence acknowledging the gap and discussing whether the result plausibly extends to adaptive optimizers.

### Minor

2. **HARDPROMPTS comparison is uninformative.** Table 5 reports HARDPROMPTS at 0.00 accuracy on exact input reconstruction. The paper itself notes (line 291) that HARDPROMPTS is designed for "approximate prompt discovery" — it is a prompt optimization method, not an exact reconstruction method. Presenting a 0.00 accuracy on a task the method was never designed for does not provide a meaningful baseline and inflates SIFT's apparent advantage. The HARDPROMPTS row should either be removed or accompanied by a clear caveat that the task mismatch explains the 0.00 result.

3. **Small inversion experiment sample sizes.** The main inversion experiment (Table 5) uses 100 prompts (20 tokens each = 2000 token predictions) for GPT-2 Small, and the quantization robustness test (Table 4) uses 50 prompts. While the theoretical guarantee makes statistical power less critical for correctness, larger samples with confidence intervals would strengthen the empirical claims.

4. **Legal claim overreach.** Lines 348–350 state: "hidden states are not abstractions but the prompt in disguise: any system that stores or transmits them is effectively handling user text itself." This conflates the theoretical existence of an invertible map with the practical feasibility of inversion. SIFT requires (a) per-position hidden states at a specific layer, (b) white-box access to run many forward passes, and (c) the model to be computationally accessible. The practical threat is narrower than the unqualified claim suggests.

5. **Corollary 2.3.1 proof sketch is incomplete.** The argument that the batch Jacobian determinant is nonzero "by linearity of differentiation" does not fully justify why the determinant of the averaged Hessian would be nonzero given only that each individual sample's update map has nonzero determinant at the same θ*. The full proof in the appendix likely addresses this, but the main text sketch is insufficient.

### Trivial

6. **Inconsistent naming of the algorithm.** The algorithm is called SIFT (abstract, line 17), SIPIT (line 45, Section 3 heading), SIpIT (Algorithm 1 heading, line 167), SIpT (line 234), and SiPT (Tables 4, 5). These inconsistencies suggest incomplete proofreading.

## Nice-to-Haves

- A discussion of whether the training-preservation proof might extend to Adam or other adaptive optimizers, or why the measure-theoretic argument is optimizer-agnostic in principle but the technical details differ.
- Larger inversion experiments (500–1000+ prompts) with per-token confidence intervals.
- An explicit description of the gradient-guided candidate policy in the main text (Algorithms 2 and 3 are referenced but not summarized in prose).

## Removed Points

These points were flagged by the reviewers but removed from the main weakness list either because they are factually incorrect, misread the paper, or are generic/non-substantive:

- **"Significance oversold / straw man" (Harsh Critic Point 3):** The paper clearly distinguishes its setting (discrete-to-continuous map from prompts to hidden states) from component-level injectivity (attention rank collapse, LayerNorm). Section 5 explicitly states: "Our focus is different." The community view being challenged is real — believing hidden states are lossy encodings — and formalizing its refutation is a genuine contribution. **Removed: misreading of the paper.**

- **"Local diffeomorphism can collapse positive-volume sets to measure zero" (Harsh Critic, Theorem 2.3 discussion):** This concern is mathematically incorrect. A map with nonzero Jacobian determinant almost everywhere is a local diffeomorphism a.e. and cannot map a set of positive Lebesgue measure to a set of measure zero (the change-of-variables formula gives a density). The measure theory invoked is standard. **Removed: factually incorrect criticism.**

- **"Per-position hidden state access is a strong assumption limiting practical relevance":** The paper states this assumption clearly in the threat model (line 141) and explicitly says extending to the last-token-only setting is future work. Transparency about scope is not a weakness. **Removed: mischaracterization of a stated assumption.**

- **"Experiments cannot confirm injectivity in any statistical sense":** The paper presents the theory as the primary evidence and the experiments as supporting consistency checks. The tone ("confirming local injectivity as predicted by our theory," line 285) is appropriate — the experiments are verifying the theory's predictions, not serving as independent proof. **Removed: overly strict reading.**

- **"Table numbering confusing":** This is a PDF-parser artifact, not an error in the original submission. **Removed: parser artifact.**

- **Generic strengths from Strength Finder** (e.g., "this paper addressed an important problem"): Dropped as superficial. Only concrete, evidence-backed strengths are retained.

## Novel Insights

The clash between the paper's framing (injectivity as a "surprising" property) and the reviewer skepticism (that it is intuitively obvious) reveals a useful tension. The genuinely non-trivial contributions are: (1) formalizing injectivity via real-analyticity into a rigorous finite-width, finite-depth guarantee, (2) proving the property survives GD/SGD training (this is the non-obvious part — training could, in principle, move parameters into the measure-zero collision set), and (3) showing that injectivity can be operationally exploited for efficient exact reconstruction. The paper would be more persuasive if it recalibrated its framing from "surprising discovery" to "rigorous formalization and training-proof extension of a property that was plausibly true but unproven."

## Suggestions

1. Add a sentence in the Discussion acknowledging that the training-preservation proof covers GD/SGD, and that extending it to adaptive optimizers like Adam is an open question (even though the empirical results suggest it holds in practice).
2. Remove the HARDPROMPTS row from Table 5, or add an explicit caveat that it is designed for a different task (prompt optimization, not exact reconstruction) and serves only as a negative baseline.
3. Standardize the algorithm name throughout (the most common variant in the paper is SIFT/SIPIT).
4. Expand the inversion experiments to 500–1000 prompts and report per-token confidence intervals.
5. Tone down the legal claim in lines 348–350 to reflect the actual threat model (per-position hidden-state access + white-box model access required).

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>