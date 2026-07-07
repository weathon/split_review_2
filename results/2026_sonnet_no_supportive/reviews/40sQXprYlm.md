Now let me draft the review based on my reading.## Summary
This paper introduces Distributed Neural Architectures (DNA), a unified framework in which tokens/patches are routed via learned paths through an arbitrary collection of computational modules. The construction subsumes MoE, MoD, weight sharing, and early exit as emergent special cases. The authors train DNA models at ViT-small and GPT-2-medium scale on ImageNet and FineWeb-Edu, then analyze the emergent routing structure — finding power-law path distributions, semantic specialization of paths in vision, and interpretable compute allocation.

## Strengths
- **Unifying framework with emergent structure**: Section 2 cleanly subsumes MoE, MoD, weight sharing, and early exit as special cases. Training recovers a mixture of all these behaviors rather than collapsing to any one, which is a substantive and verifiable finding (Fig. 2 bottom — the dense backbone splits into sparse distributed paths).
- **Semantic patch specialization (Fig. 3, Fig. 1e)**: Low-rank paths cluster patches by high-level visual features (edges, color regions) while high-rank paths cluster by narrow semantic concepts (brass instruments, puzzle pieces). The random-model baseline, which clusters by superficial pixel similarity, sharpens the contrast meaningfully.
- **Interpretable compute allocation (Fig. 5)**: The top-2 DNA assigns quantifiably higher compute to boundary-rich and texture-rich images, with a visually credible random draw across high/medium/low compute buckets and a mechanistic explanation (boundary-patch prioritization) that is specific and falsifiable.

## Weaknesses

### Fatal
None.

### Major

- **Vision performance–parameter tradeoff is not "competitive" without qualification**: Table 1 shows top-1 DNA (34M total parameters, 22M active) achieves 79.1% vs. ViT-small (22M total) at 79.8%; top-2 DNA (18M total, 25% skip) achieves 78.8%. The dense baseline wins on both accuracy and total parameter count. Training cost scales with total parameters, not active parameters. Since the paper never reports training FLOPs or wall-clock time, readers cannot assess whether the same training budget directed at a larger dense model would outperform the DNA. The "competitive" label in Section 3.1 and the abstract is defensible only if this asymmetry is stated clearly, which it is not.

- **Abstract overclaims parameter sharing**: The abstract states "compute efficiency/parameter sharing can be learnt from data." Section 4.3 explicitly concludes "module reuse is most likely random in the language case." Emergent parameter sharing holds in vision but is admitted to fail in language — a domain covering half the paper. The abstract presents this as an unqualified positive finding, misrepresenting the scope of the result.

- **Power-law path distribution is primarily structural, not learned**: The paper itself (Fig. 1c,d caption) notes that random (untrained) models exhibit power-law path distributions with exponent −1; trained models shift this to −1.2. The paper acknowledges this ("Somewhat surprisingly…") but does not resolve its implication: if the power-law form is determined by the combinatorial structure of routing decisions and training adjusts the exponent by only 0.2, the finding is substantially weaker as evidence of learned structure. The paper should either quantify whether this exponent difference meaningfully changes the token-distribution at each rank or qualify the finding accordingly.

### Minor

- **Language interpretability relies on qualitative, cherry-picked examples**: Section 4.2's claim that rank-8 tokens correspond to "relationships between actions and their targets or contexts" is a post-hoc label assigned to a small example set. The paper devotes roughly equal space to vision and language interpretability despite the vision analysis being demonstrably stronger. No systematic purity metric is applied to language token-path assignments.

- **Patch clustering semantic claim lacks quantitative validation**: Fig. 3 — the paper's strongest empirical finding — rests on visual inspection of a handful of randomly selected patches per path. A semantic purity score (e.g., ImageNet class-label purity per top-N path, or ARI against visual category labels) would convert this qualitative claim into a defensible quantitative result and would also answer the implicit question: does training actually change semantic content along the rank axis, or only the exponent?

- **Language skip model underperforms shallower dense baseline on most benchmarks**: Table 3 shows top-2 (30% skip) at loss 2.784 vs. GPT-2 (30% shallower) at 2.772, and substantially worse on LAMBADA (23.8 vs. 31.4), ARC-E (52.5 vs. 58.0), BoolQ (52.9 vs. 54.9), and Wikitext perplexity (52.6 vs. 38.0). The efficiency story in language is weaker than the framing in Section 4.3 suggests.

### Trivial
None.

## Nice-to-Haves
- Add a semantic purity quantification for patch-path clustering (e.g., class-label purity per path) to anchor the paper's strongest finding quantitatively.
- Report wall-clock training time and training FLOPs for DNA vs. dense baselines; without these, the efficiency framing is one-sided.
- Study load imbalance more explicitly: Fig. 2 (bottom) shows some modules are never activated; characterizing whether this reflects useful specialization or optimization failure would strengthen the architectural claims.
- For language, systematically label the 10 most-frequent paths by token syntactic/semantic categories rather than presenting illustrative examples, to dispel the impression of selective presentation.

## Removed Points
*These points are flagged to be removed, treat them with caution.*

- **Bias hyperparameters r and u sensitivity**: The harsh critic flagged that Eq. 3 introduces r and u without sensitivity analysis in the main body. The paper states values are in the appendix (Appendix A), and requesting main-body sensitivity analysis is a scope/presentation nitpick not central to the claims. Removed.

- **No load-balancing as a weakness**: The paper explicitly eschews load-balancing as a deliberate design choice to "let models develop the structures they need" (Section 2.2). This is a coherent scientific choice aligned with the paper's goals. Not a weakness.

- **Deep dream misclassification as a critical flaw**: The bell pepper being classified as "spotlight" (p=0.48) is reported honestly in the paper (Fig. 4 caption), which attributes it to hierarchical uncertainty — and correctly notes that the top-5 guesses for hummingbird and spaniel are all birds and dogs, respectively. The paper discloses this limitation transparently. Removed as a criticism.

- **Harsh critic's framing of 30% skip as a "positive result"**: The critic stated the skip model achieves "essentially no cost relative to a shallower dense model." Table 3 shows this is incorrect — the skip model is worse on most benchmarks (see Minor weakness above). Removed as stated, replaced with accurate characterization.

## Novel Insights
The most genuinely novel observation is the rank-stratified semantic specialization along the power-law path distribution: frequent (low-rank) paths generalize over high-level visual features while rare (high-rank) paths specialize in narrow semantic concepts. The structural power-law baseline (random models also exhibit it) complicates but does not eliminate this finding — the trained model's different exponent and demonstrably different semantic content at each rank constitute a real phenomenon. If future work can quantify this semantic shift with a purity metric, it would constitute a strong argument that routing learns to encode semantic abstraction in path frequency.

## Suggestions
- Rewrite the abstract to qualify: "compute efficiency can be learned from data in both domains; parameter sharing emerges in vision but is random in language."
- Add a quantitative semantic purity evaluation for patch-path clustering.
- Add a training-compute comparison (FLOPs or wall-clock time) between DNA and dense baselines to enable honest efficiency assessment.
- Foreground the language skip model's underperformance relative to the shallower dense baseline rather than leaving it implicit in Table 3.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| /…/762u1p9dgg.md (MOEfication by Experts as Masks) | 3.40 | R1 | Narrower: post-hoc MoE sparsification without novel architecture framework |
| /…/KaYXsoCxV7.md (ViMoE) | 3.00 | R1 | Narrower: empirical study of MoE in ViT with modest contribution |
| /…/04RLVxDvig.md (NanoMoE) | 3.00 | R1 | Narrower: parameter-efficient MoE blocks without interpretability analysis |
| /…/tI3eqOV6Yt.md (Adaptivity and Modularity) | 5.00 | R1 | Similar scope (dynamic/modular routing for transformers) but narrower domain and weaker analysis |
| /…/jIAKjjEmWi.md (Attention Is All You Need For MoD Routing) | 4.00 | R1 | Similar topic (MoD routing improvement) but more limited; no unifying framework |
| /…/rWui9vLhOc.md (MoLEx) | 6.33 | R1 | Comparable: MoE layer-level adaptation with clear contribution and eval |
| /…/Pu3c0209cx.md (Tight Clusters Make Specialized Experts) | 7.00 | R1 | Comparable: MoE routing improvement with systematic eval; stronger empirical story |
| /…/IDJUscOjM3.md (Self-MoE) | 6.00 | R1 | Comparable: compositional LLM with self-specialized experts; narrower than DNA |
| /…/6mLjDwYte5.md (MoE + Instruction Tuning) | 6.75 | R1 | Comparable: systematic study of MoE in fine-tuning; more concrete gains |
| /…/EzrZX9bd4G.md (BEEM Early Exit) | 6.25 | R2 | Similar: early exit framework with competitive baseline comparison |
| /…/q44uq3tc2D.md (γ-MoD) | 6.67 | R2 | Similar: MoD adaptation with concrete gains; better performance story than DNA |
| /…/bcHty5VvkQ.md (SkipDecode) | 5.50 | R2 | Similar: skip/early-exit efficiency but narrower scope and weaker framing |
| /…/1xG3MN1RRW.md (SparseVLM) | 5.20 | R2 | Similar: efficient token pruning; narrower scope |

**Round 1 bracket: 5–7.** The paper is clearly above the 3–4 range (those papers have narrower scope, no unifying framework, no interpretability analysis). The performance story does not support the 7–8 range (where papers have strong empirical gains or truly clean contributions). The paper sits between MoLEx/Self-MoE (6.0–6.33) and Tight Clusters (7.0).

**Round 2 narrowing:** DNA's unifying framework is more ambitious than most 6-range papers, which tend to be applications of existing MoE ideas. The semantic patch specialization finding (Fig. 3) is concrete and specific. However, three real weaknesses pull the score down: (1) vision DNA underperforms the dense baseline despite more total parameters; (2) the abstract overclaims parameter sharing; (3) the power-law's structural origin undermines one of the headline findings. These are not fatal but are material. The paper lands closer to 6.0 than 7.0 — it is a genuine contribution worthy of acceptance, but the framing mismatch and unresolved evidential gaps hold it back from a clear accept.

**Final score: 6.0**

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>