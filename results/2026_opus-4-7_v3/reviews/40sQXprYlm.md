Now let me re-read the key experimental tables and claims more carefully.Now I have a thorough understanding of the paper. Let me draft my review.Now let me run calibration Round 1 — bracketing across score bands.Let me read a few key anchor papers to calibrate the score.Now I have sufficient calibration data. Let me form my initial bracket and finalize the review.

**Round 1 bracket formation:**

Comparing the DNA paper against anchors:
- **ViMoE (3.0)**: DNA is clearly stronger — more ambitious framework, ImageNet+language, richer analysis
- **MOEfication (3.4)**: DNA is stronger — novel conceptual framework vs incremental sparsification
- **SMEAR (6.0)**: Similar level — both propose novel routing/architecture ideas with interesting analysis but experimental gaps
- **COMET (5.67)**: Similar level — both are ambitious architectural proposals tested across domains
- **Tight Clusters (7.0)**: DNA is weaker — that paper has theoretical backing + strong large-scale experiments
- **MoE++ (8.0)**: DNA is weaker — MoE++ demonstrates clear practical gains at scale

**Initial bracket: 4.5–6.0**

The DNA paper has a genuinely novel concept and rich interpretability analysis, but the missing MoE/MoD baselines, unclear parameter-matched comparisons, and small scale push it toward the lower end of this range.

Now let me write the final review.

## Summary
The paper introduces Distributed Neural Architectures (DNA), a framework where tokens traverse collections of computational modules (transformers, MLPs, attention) via learned routers, with connectivity emerging end-to-end during training. DNA generalizes MoE, MoD, parameter sharing, and early exit as special cases. The authors demonstrate feasibility on ImageNet (ViT-Small scale) and FineWeb-Edu (GPT-2 Medium scale), and provide extensive analysis of emergent path distributions (power-law), path specialization, compute allocation, and parameter sharing.

## Strengths
- **Unified conditional computation framework** (Sec 2.1, Eq. 1): The formulation elegantly subsumes MoE, MoD, weight sharing, and early exit under a single architecture via routers, identity modules, and flexible module composition. The construction is clean and well-motivated from Minsky's "society of mind" perspective.
- **Rich interpretability analysis**: Figure 3 shows convincing path specialization where low-rank (frequent) paths capture high-level features (edges, flat colors) while high-rank (rare) paths capture specific concepts (brass instruments, puzzle pieces). Figure 4's deep-dream reconstructions demonstrate meaningful hierarchical feature development through routing decisions. Figure 5 shows interpretable compute allocation where boundary-rich images receive more compute.
- **Power-law path distribution** (Fig. 1c-d): The finding that trained DNA paths follow power-law distributions with exponents −1 and −1.2 for vision and language is a novel empirical observation that connects neural architecture behavior to known distributional phenomena.
- **Emergent parameter sharing** (Sec 3.3): The observation that models learn to reuse modules without explicit incentive — with ~15–25% parameter reuse in vision — and that high-reuse images lack clear objects demonstrates genuine emergent structure.
- **Domain generality**: Testing the framework in both discriminative vision and generative language settings, showing qualitatively different but interpretable emergent behaviors in both (e.g., language routing groups parts of speech at early routers, Sec 4.2), strengthens the generality claim.

## Weaknesses

### Fatal
None

### Major
1. **No comparison with MoE, MoD, or other conditional computation methods** — The paper positions DNA as a generalization of MoE (Shazeer et al., 2017), MoD (Raposo et al., 2024), weight sharing, and early exit (Abstract, Sec 1, Sec 2.1), but the only baselines are dense ViT-Small and GPT-2 Medium. Without comparing against these established methods at matched parameter/compute budgets, the reader cannot assess whether the emergent routing structure provides any advantage over simpler hand-designed conditional computation. This is the paper's most critical experimental gap.

2. **Parameter accounting undermines the "competitive" claim** — Per Table 1, top-1 DNA has 34M total parameters vs. ViT-Small's 22M (54% more), yet underperforms by 0.7% (79.1% vs. 79.8%). Per Table 2, top-1 DNA has 583M total parameters vs. GPT-2's 406M (44% more), yet has higher loss (2.754 vs. 2.720). The top-2 DNA (language) uses 603M total parameters and 433M active parameters vs. GPT-2's 406M to achieve only marginally better loss (2.674 vs. 2.720). The non-shared active parameters are even lower (242M and 266M respectively). The claim of being "competitive with dense baselines" (Abstract) needs qualification given these parameter asymmetries.

### Minor
1. **Compute efficiency mechanism degrades downstream performance substantially** — Table 3 shows the 30% skip DNA model degrades significantly on downstream tasks vs. the full top-2 DNA (LAMBADA: 23.8 vs. 34.0; WikiText perplexity: 52.6 vs. 31.5; ARC-E: 52.5 vs. 59.2). While the shallower GPT-2 also degrades, the DNA skip model degrades *more* on most benchmarks despite similar loss (2.784 vs. 2.772). This weakens the claim that "compute efficiency can be learnt from data" (Abstract).

2. **Power-law in random networks reduces the finding's significance** — The paper itself notes (Fig. 1 caption) that random DNA models also exhibit power-law path distributions with exponent −1. Training shifts this only modestly (to −1 or −1.2). This suggests the power-law is partly an architectural property rather than a learned one, diminishing its interpretive significance.

3. **Language parameter sharing is admittedly random** — Section 4.3 explicitly concludes "module reuse is most likely random in the language case" with no correlation between different DNA models. This undercuts the generality of the "emergent parameter sharing" narrative presented in the abstract and vision sections.

4. **No FLOP or wall-clock comparisons** — The paper discusses compute efficiency in terms of module skip rates but never reports FLOPs per forward pass or wall-clock training/inference times. Router overhead (linear classifiers at each step) could partly negate savings from identity modules, and this is never quantified.

### Trivial
None

## Nice-to-Haves
- FLOP-matched comparisons with dense baselines would make the "competitive" claim rigorous
- Scaling experiments (even one intermediate scale point) to assess whether DNA benefits grow with scale — the paper explicitly defers this (Sec 5) but it would substantially strengthen the story
- Ablation on backbone size ($N_b$) and its effect on training stability, given the empirical finding that "first few modules not routed" is critical (Sec 2.2)
- The "Strengthening the Paper on Its Own Terms" direction of discouraging language parameter sharing (suggested by the authors themselves in Sec 4.3) could improve language DNA results

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **No input review weaknesses to remove** — The input harsh critic review was effectively empty/truncated (contained no actual weakness claims), so there are no reviewer claims to verify or filter. All weaknesses above are derived from direct reading of the paper.

## Novel Insights
The paper's most genuinely novel observation is that emergent routing in a flexible architecture produces power-law distributed paths that exhibit semantic specialization: frequent paths handle generic features while rare paths handle domain-specific concepts. The connection between path rank and semantic specificity — demonstrated through both visual patch analysis (Fig. 3: low-rank = edges/colors, high-rank = brass instruments/puzzle pieces) and linguistic token analysis (Fig. 8: low-rank = linking verbs/punctuation, high-rank = context-specific roles) — provides a new empirical lens for understanding how neural networks self-organize computation. The finding that different patches within a single image follow different paths, with boundary patches separated from object and background patches (Fig. 1e, Fig. 13), connects to prior work on critical patch identification (Riquelme et al., 2021) in a more general framework.

## Suggestions
- Add MoE and MoD baselines with matched active parameters and total parameters — this is the single highest-impact improvement
- Report FLOPs per forward pass for all models (dense and DNA variants) to make efficiency claims concrete
- Consider a ViT-Small DNA variant with exactly 22M total parameters (not just active parameters) to enable a clean apples-to-apples comparison
- Investigate whether discouraging module reuse in language (as the authors suggest in Sec 4.3) closes the gap with GPT-2 for top-1 DNA
- Present the power-law finding more carefully, emphasizing what changes between random and trained networks (the exponent shift and, more importantly, the semantic content of paths) rather than the power-law itself

## Score and Decision

### Calibration Anchors (all rounds)

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| KL Divergence GFlowNets | Uj0h13lVrR | 1.0 | 1 | Far weaker — fundamentally flawed methodology |
| Illumination Harmonization | u1cQYxRI1H | 10.0 | 1 | Far stronger — exceptional results with rigorous evaluation |
| Financial Markets NN | nSDOkm0SKo | 1.0 | 1 | Far weaker — toy hypothetical scenario |
| Clothing-Irrelevant ReID | 5lUdTogEL3 | 1.0 | 1 | Far weaker — poorly conceived approach |
| Collective Model Intelligence | XVHXVdoV11 | 3.4 | 1 | Weaker — DNA has more ambitious framework and richer analysis |
| ViMoE | KaYXsoCxV7 | 3.0 | 1 | Weaker — limited to CIFAR, marginal novelty; DNA is more ambitious |
| MOEfication by Experts as Masks | 762u1p9dgg | 3.4 | 1 | Weaker — incremental approach; DNA offers a more general framework |
| dFCExpert | sTI75sFQkn | 3.25 | 1 | Weaker — domain-specific, less general contribution |
| Mixture of LoRA Experts | uWvKBCYh4S | 5.0 | 1 | Similar tier — both have interesting ideas but experimental gaps |
| PERFT | PPjpGTPG5K | 5.33 | 1 | Similar — both propose frameworks with mixed experimental evidence |
| Glider Router | 0gVatTOgEv | 4.0 | 1 | DNA is somewhat stronger — richer analysis and two-domain evaluation |
| VQMoE | RVPZJpmyGU | 4.6 | 1 | Similar — both propose novel routing mechanisms with modest results |
| SMEAR | QHzzAU7Qf9 | 6.0 | 1 | Similar level — both have novel ideas and good writing but experimental limitations |
| Mutual-Inform SMoE | V7EiYG5DwZ | 5.75 | 1 | Similar — both propose novel routing; DNA has richer analysis but weaker results |
| COMET | 1qq1QJKM5q | 5.67 | 1 | Close match — both ambitious multi-domain architectural proposals |
| Tight Clusters | Pu3c0209cx | 7.0 | 1 | DNA is weaker — lacks theoretical grounding and strong large-scale results |
| MoE++ | t7P5BUKcYv | 8.0 | 1 | DNA is weaker — MoE++ has clear practical gains at scale |
| Probabilistic L2D | zl0HLZOJC9 | 8.0 | 1 | DNA is weaker — that paper has rigorous theoretical + experimental contributions |
| FlexPrefill | OfjIlbelrT | 8.0 | 1 | DNA is weaker — FlexPrefill demonstrates clear practical efficiency gains |
| MOS | Y6aHdDNQYD | 8.0 | 1 | DNA is weaker — MOS has complete, well-validated contribution |

**Round 1 bracket: 4.5–6.0**

The DNA paper is clearly above the 3.0–3.5 rejected papers (those have limited experiments, narrow scope, or marginal contributions). It sits in the range of papers like SMEAR (6.0), COMET (5.67), and VQMoE (4.6) — interesting architectural ideas with experimental limitations. The missing MoE/MoD baselines and parameter-mismatched comparisons are significant gaps that differentiate it from accepted papers in the 7.0+ range.

**Final calibrated reasoning:** The paper presents a genuinely novel and thought-provoking framework with rich analysis, but the experimental validation has two significant gaps: (1) no comparison against the very methods (MoE, MoD) it claims to generalize, and (2) parameter-unmatched comparisons that make the "competitive" claim hard to evaluate. The interpretability analysis is the paper's strongest contribution, but the performance story is incomplete. This places it below the borderline-accept threshold but above clear rejects.

**Final Score: 5.0**

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>