## Summary
# Final Review Report

## Summary

This paper makes a provocative theoretical claim: that decoder-only Transformer language models are almost-surely injective — distinct prompts map to distinct last-token hidden representations — under standard initialization and training. The authors prove this using real-analyticity of Transformer components, showing collisions can only occur on a measure-zero parameter set. They further introduce SIPIT, an algorithm that reconstructs the exact input prompt from per-position hidden states, with linear-time guarantees. Empirical collision searches across millions of prompt pairs and several model families (GPT-2, Gemma 3, Llama 3.1, Mistral 7B, Phi-4) report zero collisions, and SIPIT achieves 100% exact recovery.

The paper is clearly written, the theoretical question is well-motivated, and the main result — if fully validated — would be significant for interpretability, model auditing, and privacy discussions. However, several gaps limit the current contribution: (1) the theoretical proof relies on the real-analyticity assumption, which may not hold for some architectures and is not fully extended to floating-point implementations; (2) the proof sketch for training preservation (Theorem 2.3) glosses over the local-to-global gap in the Inverse Function Theorem argument; (3) SIPIT's practical applicability is constrained by requiring access to all per-position hidden states at an intermediate layer, a strong assumption rarely available in deployment; (4) the experimental comparisons are against baselines that solve a different problem, reducing their informativeness; (5) the novelty of the injectivity result relative to concurrent work (Sutter et al. 2025, who prove almost-sure injectivity at initialization) needs clearer differentiation. The paper would benefit from tightening these gaps before publication.

**Retrieval status**: External paper search was unavailable in this run (Retrieval-Disabled Mode). Novelty and comparison conclusions are marked for deferred manual verification.

## Strengths
1. **Well-motivated and clearly posed research question.** The paper addresses a fundamental question — whether Transformer hidden representations preserve input information losslessly — that has implications across interpretability, privacy, and model auditing. The framing of injectivity as a property of the discrete-to-continuous map rather than of individual components is conceptually clarifying.

2. **Rigorous theoretical framework.** The use of real-analyticity to establish almost-sure injectivity is elegant and mathematically principled. The dichotomy of real-analytic functions (identically zero vs. measure-zero zero set) provides a clean foundation for the main argument. The proof sketches are well-structured and clearly communicated, with detailed appendices supporting the main claims.

3. **Novelty of the training-preservation result.** While Sutter et al. (2025) previously showed almost-sure injectivity at initialization, this paper's extension to training trajectories — showing that gradient descent cannot destroy injectivity — appears to be a genuinely new contribution. The argument that GD preserves absolute continuity of the parameter distribution is technically interesting.

4. **Extensive empirical validation.** The collision search across 6+ model families (GPT-2, Gemma 3, Llama 3.1, Mistral 7B, Phi-4, TinyStories) with billions of pairwise comparisons is thorough. The inclusion of quantized models (FP4, INT8) and large models (14B, 70B) strengthens the empirical case. The observation that pairwise distances increase with depth and are not reduced by quantization is an interesting finding in its own right.

5. **Provably correct inversion algorithm.** SIPIT's guarantee of exact recovery with linear-time complexity is well-derived from the injectivity result. The gradient-guided policy that explores <0.22% of the vocabulary on average is practically efficient, and the robustness guarantee (Theorem 3.2) provides a clean noise tolerance bound.

6. **Excellent writing quality.** The paper is clearly organized, the narrative flows well from theory to algorithm to experiments, and the technical content is presented at an appropriate level of detail for the target audience. The use of theorem-sketch format with appendix pointers is reader-friendly.

## Weaknesses
### W1. Local-to-global gap in the training preservation proof (Major)

The proof sketch of Theorem 2.3 (injectivity preserved under training) relies on the Inverse Function Theorem to argue that gradient descent preserves absolute continuity of the parameter distribution. However, the Inverse Function Theorem guarantees only *local* invertibility — it ensures that φ is a local diffeomorphism where det Dφ ≠ 0. The global claim that "pushing forward an absolutely continuous distribution through φ yields another absolutely continuous distribution" requires φ to be a proper map or globally invertible on the support of the distribution, which is not argued. The composition of locally invertible maps across multiple GD steps is not guaranteed to be globally invertible, so the induction argument as sketched has a technical gap. 

**Impact**: The core claim that injectivity holds with probability one after training is not fully proved in the main text. While the conclusion may still be correct (and the appendix may address this more carefully), the sketch as presented does not convincingly close the argument.

**Recommended fix**: Either (a) prove that GD iterates with step sizes in (0,1) form a proper map on the sublevel set of the loss, or (b) use a simpler argument: the set of parameters leading to collisions is measure-zero by Theorem 2.2, and GD is a deterministic function; since the initial parameter distribution is absolutely continuous and the collision set has measure zero, the pre-image of the collision set under the GD trajectory also has measure zero, so the probability of landing in it remains zero. This avoids the pushforward argument entirely.

### W2. SIPIT access assumptions severely limit practical applicability (Major)

SIPIT requires access to "all per-position states at a given layer ℓ" — essentially white-box access to every intermediate hidden state in the sequence. This is a strong assumption that is not available in standard API-based deployments of LLMs. The paper acknowledges this, stating that "designing an efficient algorithm for [recovery from only the final embedding] is nontrivial and left to future work," but this admission appears late (in Section 3) and is not reflected in the title or abstract, which claim broadly that "language models are invertible." 

**Impact**: Readers may infer a broader privacy vulnerability than actually demonstrated. The practical relevance of SIPIT is limited to niche scenarios (leaked KV-cache, shared-inference pipelines, research settings with full model access).

**Recommended fix**: (a) Add a prominent caveat in the abstract and introduction specifying the access assumption. (b) Discuss what fraction of real-world deployments expose per-position hidden states. (c) Include a roadmap or preliminary results toward the logit-only setting.

### W3. Real-analyticity assumption boundary not clearly delineated (Major)

The entire theoretical framework depends on the assumption that all Transformer components are real-analytic functions of their parameters. While the paper claims that GELU, SwiGLU, tanh, sigmoid, etc. are real-analytic (which is correct — they are compositions of analytic functions), the paper does not clearly state which models satisfy this at every layer. Models using piecewise-linear activations (ReLU, hard sigmoid, hard Swish) at any layer would violate the real-analyticity assumption. The "Failure cases" subsection mentions that non-analytic choices can break injectivity, but it does not enumerate which popular architectures are covered and which are not.

**Impact**: Practitioners may incorrectly assume the theoretical guarantee applies to all transformer LMs, when it technically excludes models with non-analytic components. This also affects the empirical results — if the tested models happen to satisfy the analyticity assumption, the theory is consistent, but the empirical method could be applied to non-analytic models where the theory does not guarantee injectivity.

**Recommended fix**: Add a table in Section 2 or the appendix enumerating activation functions and their real-analyticity status, and listing which commonly used models are fully covered. For models with non-analytic components, explicitly state that the theoretical guarantee does not apply and empirical verification is needed.

### W4. Inversion experiment baselines are not comparable (Moderate)

Table 5 compares SIPIT against HARDPROMPTS and a BRUTEFORCE ablation. HARDPROMPTS is a prompt optimization method (designed to find prompts for a target output), not a hidden-state inversion method. The paper acknowledges that prior inversion methods (Morris et al. 2023a,b, Nazir et al. 2025) use different access assumptions, but this does not justify the comparison against a method solving a different task. Showing that SIPIT achieves 100% accuracy while HARDPROMPTS achieves 0% is a straw-man comparison.

**Impact**: The headline results in Table 5 may mislead readers about SIPIT's relative performance. The claimed efficiency advantage (28s vs 6132s for HARDPROMPTS) is meaningless if the methods address different problems.

**Recommended fix**: (a) Remove HARDPROMPTS from the main comparison or clearly label it as solving a different task. (b) Add a learned-inversion baseline (e.g., MLP classifier trained on hidden states matching SIPIT's access) to provide a meaningful comparison. (c) Alternatively, compare against a simple nearest-neighbor baseline using hidden-state distances.

### W5. "First algorithm" claim for exact recovery needs qualification (Moderate)

The abstract and introduction state that SIPIT is "the first algorithm that provably and efficiently reconstructs the exact input text from hidden activations." This may be accurate under the specific setting (per-position hidden states, provable linear time), but the paper should include the access qualifier in this claim. Without it, readers may compare against Thomas et al. (2025) who also recover prompts from hidden states (though without exactness guarantees). The "first" claim is defensible when qualified to "first with provable exactness guarantees," but the current wording overreaches.

**Recommended fix**: Add the qualifier "under the assumption of access to per-position hidden states" and clarify that the novelty lies in provable exact recovery, not inversion per se.

### W6. Empirical coverage of prompt space is extremely limited (Minor)

The collision search uses 100k prompts, which is an infinitesimal fraction of the possible prompt space (|V|^{≤K}). While the authors acknowledge this implicitly, the presentation could be read as more comprehensive than it is. The prompts are sampled uniformly from only four data sources (Wikipedia, C4, The Pile, Python GitHub code), which may not be representative of the diverse prompts encountered in practice.

**Recommended fix**: Add an explicit statement acknowledging that the prompt space coverage is vanishingly small, and characterize the sampling as a necessary limitation. Consider adding adversarial prompts designed to maximize collision probability as a stress test.

### W7. "Probability one" in algorithm guarantee is misleading (Minor)

Theorem 3.1 states that SIPIT recovers the true sequence "with probability one." This phrasing inherits from the parameter-randomness context of Theorems 2.2 and 2.3, but as applied to the algorithm, the guarantee is deterministic (given injectivity holds, the unique matching token will be found). The "probability one" qualifier is unnecessary and potentially confusing.

**Recommended fix**: Replace "with probability one" in Theorem 3.1 with "deterministically" and clarify that the probabilistic guarantee refers to the underlying parameter distribution, not the algorithm itself.

### W8. Missing discussion of floating-point arithmetic effects (Minor)

The paper proves injectivity for real-analytic functions over real numbers, but all practical implementations use floating-point arithmetic (float32, bfloat16, float16). Floating-point representations are discrete and finite, so the continuous mathematics of measure-zero sets does not directly apply. While the empirical results suggest injectivity holds in practice, the theoretical-to-practical gap is not discussed.

**Recommended fix**: Add a brief discussion of the floating-point issue in Section 2 or the Discussion, noting that the theoretical guarantee applies to the idealized real-analytic model and that empirical validation bridges the gap to practice.

## Score
**Final Score: 6/10**

This score reflects the paper's strengths (a well-motivated theoretical question, rigorous use of real-analyticity, extensive empirical validation) weighed against significant limitations: the training-preservation proof has a local-to-global gap in the main text sketch, the practical applicability of SIPIT is constrained by strong access assumptions not reflected in the title/abstract, the real-analyticity assumption boundary is not fully delineated, and the experimental comparisons are against inappropriate baselines. The paper makes a genuine contribution to understanding Transformer representations, but these issues reduce confidence in the claims as currently presented.

---

### ASCII Diagram — Paper Structure & Evidence Map

```text
Paper: Language Models are Injective and Hence Invertible
├── Claim C1: Decoder-only Transformers are almost-surely injective
│   ├── Evidence: Theorem 2.1 (real-analyticity) + Theorem 2.2 (init) + Theorem 2.3 (training)
│   ├── Gap: Real-analyticity assumption not verified for all model architectures
│   ├── Gap: Local-to-global step in training preservation proof sketch
│   └── Gap: Floating-point vs real-number gap not discussed
├── Claim C2: No collisions observed empirically
│   ├── Evidence: ~5B pairwise comparisons across 6+ model families
│   ├── Gap: 100k prompts is vanishing fraction of prompt space
│   └── Gap: Limited to 4 data source domains
└── Claim C3: SIPIT achieves exact prompt recovery
    ├── Evidence: 100% accuracy on 100 prompts, 20 tokens each
    ├── Gap: Requires per-position hidden states (strong access assumption)
    ├── Gap: Compared against inappropriate baselines (HARDPROMPTS)
    └── Gap: "First algorithm" claim needs access-scope qualifier
```

---

### ASCII Diagram — Revision Strategy Roadmap

```text
Priority 0 (Must fix before publication):
┌─────────────────────────────────────────────────────┐
│  W1: Close local-to-global gap in Theorem 2.3 proof │
│  → Use pre-image argument instead of pushforward    │
│  → Or add properness condition                      │
│  → Impact: Core theoretical claim                   │
└──────────────────────┬──────────────────────────────┘
                       │
Priority 1 (Must fix):
┌──────────────────────────────────────────────────┐
│ W2: Calibrate SIPIT access assumptions prominently│
│ → Add caveat to title/abstract/intro              │
│ → Impact: Prevents misinterpretation              │
├──────────────────────────────────────────────────┤
│ W3: Clarify real-analyticity boundary             │
│ → Add activation function coverage table          │
│ → Impact: Theoretical rigor                       │
├──────────────────────────────────────────────────┤
│ W4: Fix baselines or repurpose comparison         │
│ → Remove/add appropriate baselines for inversion  │
│ → Impact: Experimental credibility                │
└──────────────────────┬────────────────────────────┘
                       │
Priority 2 (Important improvements):
┌─────────────────────────────────────────────────────┐
│ W5: Add access-scope qualifier to "first" claim    │
│ W6: Acknowledge prompt space coverage limitations  │
│ W7: Fix "probability one" wording in Theorem 3.1   │
│ W8: Add floating-point arithmetic discussion       │
└─────────────────────────────────────────────────────┘
```

---

### ASCII Diagram — Related-Work Taxonomy Tree

```text
Transformer Representations: Injectivity & Inversion (Root)
├── Branch 1: Analytical Properties of Transformers
│   ├── Leaf 1.1: Non-injectivity of components
│   │   └── LayerNorm (Ba et al. 2016), attention rank decay (Dong et al. 2021)
│   ├── Leaf 1.2: Injectivity/Surjectivity results
│   │   ├── Surjectivity of modern architectures (Jiang & Haghtalab 2025)
│   │   └── Almost-sure injectivity at initialization (Sutter et al. 2025)
│   │       └── Our paper: extends to training, last-token, parameter view
│   └── Leaf 1.3: Universal approximation & completeness
│       └── Softmax bottleneck (Yang et al. 2018)
│
├── Branch 2: Inverse Problems in Language Modeling
│   ├── Leaf 2.1: Output-to-prompt inversion (approximate)
│   │   ├── Logit-based trained inverters (Morris et al. 2023a,b)
│   │   ├── Logprobs sequence inversion (Nazir et al. 2025)
│   │   └── Generative continuation matching (Zhang et al. 2024)
│   ├── Leaf 2.2: Hidden-state inversion (exact)
│   │   ├── LLM-based policy ranking (Thomas et al. 2025) — no exactness
│   │   └── Our paper: SIPIT — provably exact, linear time
│   └── Leaf 2.3: Prompt optimization (related but distinct)
│       ├── AutoPrompt (Shin et al. 2020)
│       ├── Hard Prompts Made Easy (Wen et al. 2023)
│       └── Gradient-based discrete optimization (Guo et al. 2025)
│
└── Branch 3: Privacy & Regulatory Implications
    └── Hidden states as personal data (Miranda et al. 2025, HmbBfDI 2024)
        └── Our paper: injectivity strengthens privacy arguments
```

**Note**: This taxonomy is constructed from the paper's own citations and general domain knowledge. External paper search was unavailable in this run (Retrieval-Disabled Mode); novelty verdicts and comparison completeness require manual verification against the full literature.

---

### Contribution-level Novelty Conclusion (Deferred)

Due to Retrieval-Disabled Mode in this run, novelty and comparison conclusions are marked for deferred manual verification. The three main contribution claims — C1 (almost-sure injectivity theory), C2 (empirical collision evidence), C3 (SIPIT exact recovery algorithm) — appear to have partial overlap with concurrent work by Sutter et al. (2025) on initialization-only injectivity, but the training-preservation result and the SIPIT algorithm appear to be novel. A full literature search is needed to confirm the scope of novelty, particularly for the claim of being "first" to achieve provable exact recovery from hidden states.