## Summary

This paper introduces Distributed Neural Architectures (DNA), where tokens follow learned arbitrary paths through a collection of modules (MLP, attention, transformer blocks, identity). The key idea is that depth and width become emergent properties of routing decisions rather than fixed architectural choices. DNA is described as a generalization of conditional computation methods (MoE, MoD, weight sharing, early exit). The authors demonstrate DNA in vision (ImageNet classification, ViT-small scale) and language (FineWeb-Edu language modeling, GPT-2 Medium scale), and provide an extensive interpretability analysis of the emergent routing patterns, path specialization, and compute allocation.

---

## Strengths

- **The core idea is genuinely novel and well-motivated.** DNA reframes "depth" and "width" as emergent rather than architecturally fixed. The idea of tokens following arbitrary learned paths through a collection of modules is conceptually clean and opens a new design space. (Section 2.1, Figure 1)

- **Two-domain demonstration strengthens plausibility.** Training DNA models in both vision (ImageNet classification) and language (FineWeb-Edu language modeling) shows that the architecture is trainable across different data modalities, loss functions, and model scales. This is non-trivial for a first-introduction paper. (Sections 3.1, 4.1)

- **The interpretability analysis is creative and yields genuinely interesting observations.** The patch-level path visualization (Figure 3), deep-dream routing reconstruction (Figure 4), and compute allocation analysis (Figure 5) go well beyond standard attention maps. The findings — boundary patches consuming more compute, paths specializing in concepts like "brass instruments" or "puzzle pieces," and early routers grouping semantically similar tokens in language — are concrete, non-obvious, and well-supported by the visualizations. (Section 3.2, Section 4.2)

- **The paper is explicit about its scope.** Footnote 3 states the work is "not focused on beating SOTA models in any domain, but on showing that distributed models are *feasible* and on analyzing their emergent structure." This framing is appropriate for a first-exploration paper and should be respected in evaluation.

---

## Weaknesses

### Fatal

None.

### Major

- **Efficiency analysis relies on module-count proxies without measuring actual compute.** The paper motivates DNA by the need to "save inference compute" (Introduction) and claims "compute efficiency/parameter sharing can be learnt from data" (Abstract). However, the only quantitative efficiency metrics are the "effective number of compute nodes" (a module count) and "normalized compute" (module-count averaged and normalized). Different module types (full transformer block, attention-only, MLP-only, identity) have different computational costs, so counting them equally does not yield a meaningful measure of actual compute savings. A model that uses 30% fewer modules could easily use the same or higher FLOPs if the remaining modules are more expensive ones. Given that efficiency is a stated motivation (though not the paper's primary contribution), the gap between the motivation and the evidence weakens this part of the paper's claims. Adding even approximate FLOP counts (profiling each module type) would substantially strengthen the efficiency analysis without changing the paper's scope.

### Minor

- **No statistical significance or variance reporting.** All results are from single "best runs" after hyperparameter search. The vision gap between ViT-small (79.8%) and top-1 DNA (79.1%) is 0.7 percentage points — within potential training variance. Language results are likewise reported as point estimates. Without multiple seeds or confidence intervals, the reader cannot assess whether reported differences are meaningful. This is a common limitation in resource-constrained settings but should be acknowledged.

- **Inconsistent comparison configurations make interpretation less straightforward.** In vision (Table 1): ViT-small has 22M params, top-1 DNA has 34M total/22M active, and top-2 DNA has 18M total/15M active. In language (Table 2): top-2 DNA has 603M total/433M active vs GPT-2's 406M. Varying total parameter counts, embedding dimensions, and head counts across the compared models conflates architectural differences with scale differences, making it harder to isolate the effect of the DNA design itself.

- **No comparison to MoE or MoD baselines despite claiming generalization over these methods.** The paper states DNA "includes feed-forward, MoE, MoD, weight sharing, early exit as particular cases" (Section 1) and is "a natural generalization of the sparse methods such as Mixture-of-Experts, Mixture-of-Depths" (Abstract). However, the only baselines are dense transformers (ViT-Small, GPT-2 Medium). A comparison to compute-matched MoE or MoD models would help answer whether the additional flexibility of DNA provides any practical benefit over simpler existing conditional computation methods. Given the paper's scope as a feasibility study this is not a fatal omission, but it limits the evidence for one of the paper's framing claims.

### Trivial

None.

---

## Nice-to-Haves

- A discussion of load imbalance as a practical limitation. The paper explicitly chooses not to use load-balancing (line 102) for analysis purposes, which is fine, but the routing patterns show clear imbalance (Figure 2, bottom), and this limits deployability.
- The power-law finding in path distributions (Figure 1) is reported alongside the observation that random models also produce power-law distributions with exponent -1. The paper is transparent about this, but a fuller discussion of what the trained model's exponent (-1.2 in language) reveals beyond the random baseline would strengthen the analysis.

---

## Removed Points

The following points from the input review were removed per filtering criteria:
- **"No Related Work section"**: Removed per hard rule — the paper discusses related work (conditional computing, MoE, MoD, layer pruning) in the introduction, and the reviewer cannot verify the existence of external related works.
- **"Load balancing not discussed as limitation"**: Removed — the paper explicitly states why load balancing is not used ("our objective is to let models develop the structures they need"), making this a deliberate design choice rather than an oversight.
- **"Power-law finding undercut by random model baseline"**: Removed — the paper itself acknowledges this finding ("the distribution of paths through the random model also follows power-law with exponent -1"), so this is transparent reporting, not a weakness.
- **"Parameter sharing is a null result in language"**: Removed — this is an honest negative finding, not a weakness. The paper reports both positive (vision) and negative (language) results transparently.
- **"Section-by-section presentation notes"**: Various minor editorial observations (e.g., about the framing of compute efficiency in the abstract relative to evidence) were either already addressed by the paper's scope statement (footnote 3) or are matters of presentation preference, not substantive weaknesses.

---

## Novel Insights

The most valuable cross-cutting insight from reviewing this paper is the tension between novel architecture exploration and quantitative rigor. The paper does something genuinely rare — it introduces a new architecture family with creative analysis of its emergent properties — but the efficiency claims, while plausibly true, are not backed by the level of measurement that the paper's own motivation would warrant. This is a paper where the core contribution (the architecture + qualitative analysis) is stronger than the quantitative evidence for some of its framing claims. The interpretability findings (path specialization, compute allocation correlating with visual boundaries) are the most novel and well-supported parts, and they stand on their own as contributions regardless of the efficiency measurement gap.

---

## Suggestions

1. **Add FLOP or throughput measurements.** Even approximate per-module-type FLOP counts would transform the efficiency analysis from qualitative ("some paths are shorter") to quantitative ("DNA saves X% FLOPs with Y% accuracy trade-off"). This directly addresses the largest gap in the evidence without requiring any change to the paper's scope.
2. **Add at least one conditional-computation baseline** (e.g., a MoD-style model or standard MoE with comparable active parameters) for one domain. This would help calibrate whether DNA's flexibility provides any practical benefit over existing methods.
3. **Report results over multiple seeds** (even 2-3) for the top hyperparameter configuration, or at minimum acknowledge the single-run limitation in the paper.
4. **Explicitly discuss the module-count proxy limitation** in the efficiency section, and clarify that the efficiency claims are about *learned skipping behavior* rather than measured FLOP savings.

---

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>