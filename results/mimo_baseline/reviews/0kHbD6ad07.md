## Summary

This paper proves that decoder-only Transformer language models are almost-surely injective as maps from discrete input sequences to continuous last-token representations—despite their non-injective components (LayerNorm, softmax, activations). The proof relies on showing Transformers are real-analytic in their parameters, that collision sets have measure zero, and that gradient-based training preserves absolute continuity of the parameter distribution. The paper further introduces SIPIT, a constructive algorithm that recovers exact input text from hidden activations with provable linear-time guarantees, and validates both injectivity and invertibility through billions of empirical collision tests across multiple state-of-the-art models.

## Strengths

- **Novel and counterintuitive theoretical result with clean proofs.** The paper elegantly leverages real-analyticity to resolve a fundamental question about Transformer representations. The three-step argument (analytic architecture → measure-zero collision sets at initialization → preservation under GD) is logically tight and each step is well-motivated. The proof sketches provided are convincing and the key technical lemmas (real-analyticity of all components including LayerNorm with ε>0, the fundamental dichotomy for real-analytic functions, absolute continuity preservation under GD maps with non-degenerate Jacobians) are all standard and correctly applied.

- **Extremely thorough empirical validation.** The collision search spans billions of pairwise comparisons across six model families (GPT-2 S/M/L, Gemma-3 1B/4B/12B, Llama-3.1-8B, Mistral-7B, Phi-4-mini, Phi-4-14B, Llama-3.1-70B, TinyStories-33M), multiple quantization schemes (FP4, INT8, FP32), and varying sequence lengths. The consistent finding that minimum pairwise distances are orders of magnitude above any collision threshold (typically ~0.001 vs. threshold at 10⁻⁶) provides strong empirical support.

- **Practical demonstration via SIPIT.** The transition from theory to constructive algorithm is well-executed: SIPIT achieves 100% exact token-level recovery across all tested settings, explores less than 0.22% of the vocabulary on average, and dramatically outperforms both HARDPROMPTS (0% accuracy) and brute-force (prohibitively slow). The gradient-guided policy is a sensible design choice that explains the efficiency.

- **Broad significance.** The implications span interpretability (hidden states faithfully encode inputs, so probe failures are not due to missing information), privacy (hidden states are lossless encodings of user text, with direct GDPR implications), and the SIPIT algorithm itself opens avenues for auditing and transparency.

## Weaknesses

### Fatal

None.

### Major

- **The SIPIT threat model is restrictive and limits practical impact.** The algorithm assumes access to all per-position hidden states at a fixed layer (equivalent to a leaked KV-cache or exposed intermediate representations). The paper acknowledges this but does not address the arguably more common and interesting setting of reconstructing prompts from only the final last-token representation, which the injectivity theorem directly guarantees is information-theoretically sufficient. While deferring this to future work is reasonable, it means the operational claim (SIPIT as a practical tool) is somewhat premature—the current demonstration is more of an injectivity sanity check than a realistic inversion tool.

- **The "linear-time" claim deserves qualification.** SIPIT is O(T·|V|) in the worst case, which is linear in sequence length T but linear in vocabulary size |V|—and |V| can be 128K+ for modern models. The empirical results show only ~0.2% of vocabulary is explored on average, but the worst-case guarantee is still O(T·|V|) forward passes. The paper should more carefully distinguish between the linear-in-T claim and the |V| dependence, especially since the gradient-guided policy is heuristic and has no formal sub-linear-in-|V| guarantee.

### Minor

- **The paper occasionally conflates "SIFT" and "SIPIT."** The abstract and early sections use "SIFT" while Section 3 introduces "SIPIT" as the full name. This is a minor naming inconsistency that could confuse readers.

- **The quantization experiments (Tables 2–3) actually show that quantization *increases* minimum distances.** This is briefly noted but deserves more discussion. If quantization is a form of deliberate non-analyticity (as the failure-cases discussion suggests), why does it strengthen rather than weaken injectivity? This seems like an interesting phenomenon worth explaining rather than just reporting.

- **The comparison with prior inversion methods (Morris et al., Nazir et al.) is somewhat dismissive.** The paper correctly notes these operate in different settings (black-box, approximate), but a brief discussion of when SIPIT's white-box exact setting is actually more useful would strengthen the positioning.

### Trivial

None.

## Nice-to-Haves

- A brief discussion of what happens with ReLU-based models (non-analytic at the origin) would help readers assess the boundary of the result. The paper focuses on models using analytic activations (GELU, SiLU), but explicitly addressing ReLU as a deliberate non-analytic choice that could break the guarantee would clarify the theory's scope.
- An explicit connection to the softmax bottleneck literature (Yang et al., 2018) explaining why the bottleneck doesn't contradict injectivity (it constrains the output distribution space, not the hidden-state space) would preempt a common reader question.

## Novel Insights

The key novel insight is that the discrete-to-continuous nature of the Transformer's input map fundamentally changes the injectivity analysis. While individual components (LayerNorm, softmax) are non-injective on continuous inputs, the fact that prompts live in a finite discrete set means that collisions between distinct prompts require the real-analytic difference function to vanish exactly—which happens only on measure-zero parameter sets. This reframes the "lossy Transformer" intuition as a confusion between component-level non-injectivity and global sequence-level injectivity. The preservation under training is a non-trivial extension beyond prior initialization-only results (Sutter et al., 2025), and the connection to absolute continuity preservation via the Inverse Function Theorem on GD maps is elegant.

## Suggestions

- Resolve the SIFT/SIPIT naming inconsistency throughout the paper.
- Add a dedicated subsection (or expand the failure-cases discussion) on ReLU and other non-analytic activations, explicitly stating whether the result holds or breaks for the most common architectures.
- Clarify the SIPIT complexity claim to distinguish the linear-in-T guarantee from the |V| dependence, and discuss whether the gradient-guided policy has any formal sub-linear-in-|V| properties.
- Provide a brief discussion of the quantization paradox (increased distances) to show deeper understanding of when and why non-analytic perturbations can *help* rather than *hurt* injectivity.

## Score and Decision

This paper presents a genuinely surprising and well-executed theoretical result—that Transformer language models are almost-surely injective—supported by clean mathematical proofs and extremely thorough empirical validation across billions of tests. The SIPIT algorithm operationalizes the theory effectively, and the implications for interpretability, privacy, and regulation are significant. The major weakness (restrictive SIPIT threat model) limits the immediate practical impact but does not diminish the core theoretical contribution. This is a strong method paper that establishes a fundamental structural property of Transformers.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>