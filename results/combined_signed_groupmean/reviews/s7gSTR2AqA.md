Now I have all the calibration information I need. Let me compile the final review.

**Calibration Summary:**

All anchors retrieved:
1. **gwZ90hFSL2.md** (avg 1.0, round 1) — Unrelated rejection. Not comparable.
2. **5kMwiMnUip.md** (avg 1.4, round 1) — Jailbreaking paper. Not comparable.
3. **8QTpYC4smR.md** (avg 1.0, round 1) — Survey paper. Not comparable.
4. **Uj0h13lVrR.md** (avg 1.0, round 1) — GFlowNets. Not comparable.
5. **u1cQYxRI1H.md** (avg 10.0, round 1) — Diffusion illumination. Not comparable.
6. **P49gSPmrvN.md** (avg 1.0, round 1) — Scientific discourse. Not comparable.
7. **nyuaoVnVCa.md** (avg 2.33, round 1) — Emergent spatial language. Not directly comparable.
8. **z3DMFpaP6m.md** (avg 3.0, round 1) — Entropy metric. Not directly comparable.
9. **rTQNGQxm4K.md** (avg 3.0/6.0, round 1) — Phylogeny of LLMs. Not comparable.
10. **7ienVkNf83.md** (avg 3.0, round 1) — Emergent language in RL. Not comparable.
11. **f7aWmxgSN4.md** (avg 3.0, round 1) — LLM knowledge graph learning. Not comparable.
12. **SaOxhcDCM3.md** (avg 3.2/6.25, round 1) — Self-consuming training loop. Not comparable.
13. **FxNNiUgtfa.md** (avg 4.0/7.25, round 1) — Knowledge capacity scaling laws. Tangentially relevant.
14. **aN4Jf6Cx69.md** (avg 4.5, round 1) — ICL mechanistic basis. Tangentially relevant.
15. **TdgAtxP6G2.md** (avg 4.0, round 1) — Transformers learn VOMC in-context. Tangentially relevant.
16. **q5lJxCXjiY.md** (avg 5.4, round 1) — Compositionality signatures. Tangentially relevant.
17. **exfy4e7OJq.md** (avg 3.67, round 1) — Emergence via monosemantic neurons. Not comparable.
18. **IwxxnY98sf.md** (avg 5.4, round 1, itemized) — Unsupervised categorical structure. Tangentially relevant; strengths+9.85/9.83/9.70 but weaknesses re: scalability, relevance; lower-clearance paper.
19. **iVMcYxTiVM.md** (avg 7.0, round 1&2, itemized) — VLM shape-texture bias. **Most comparable anchor.** Extensive analysis (strengths +10, +9.99, +9.94, +9.83) with only minor weaknesses. *This paper is stronger than the current one methodologically but in a different domain.*
20. **62K7mALO2q.md** (avg 6.0, round 1&2, itemized) — ICL dynamics with binary sequences. Relevant methodology (ICL+cognitive science). Mixed reception; has major weaknesses about missing baselines and limited scope.
21. **kaGA40pfFY.md** (avg 6.5, round 1) — Rationality of thought. Tangentially relevant.
22. **tZCqSVncRf.md** (avg 6.0, round 1) — Inductive reasoning. Tangentially relevant.
23. **QQt0MwXA81.md** (avg 6.2, round 1&2, itemized) — LLMs' human-like response biases. Relevant topic (cognitive science + LLM evaluation). Mixed reception with weaknesses about methodology (-9.39) and generalization (-9.95). *This paper is comparable in ambition; current paper has stronger theoretical grounding.*
24. **Xbl6t6zxZs.md** (avg 6.0, round 1&2) — Cultural bias in VLMs. Tangentially relevant.
25. **fN8yLc3eA7.md** (avg 6.0, round 2, itemized) — **Most directly comparable anchor.** LLMs Telephone Game — iterated cultural transmission in LLMs. Scores of 3, 8, 8, 5 (mixed). Many severe weaknesses (-9.88, -9.98, -10.00, -9.70) but strengths about novelty. *The current paper has stronger strengths (+9.92 to +9.99) and fewer severe weaknesses.*
26. **Sy8upuD6Bw.md** (avg 6.33, round 2) — Emergent communication with repair. Tangentially relevant.
27. **XrsOu4KgDE.md** (avg 7.0, round 2) — Culture-conditioned generations. Tangentially relevant.
28. **HC0msxE3sf.md** (avg 6.0, round 2) — Signaling game as beta-VAE. Tangentially relevant.

**Round 1 bracket:** Based on similar interdisciplinary cognitive-science-meets-LLM papers, I bracketed this paper between 5.5 and 7.5, anchored by the telephone game paper (6.0) on the low end and the VLM bias paper (7.0) on the upper end.

**Narrowing:** Comparing to the telephone game paper (6.0): that paper had more severe weaknesses and weaker strengths. The current paper has stronger strengths (+9.92 to +9.99 vs max +8.89) and fewer severe weaknesses. Comparing to the VLM bias paper (7.0): that paper had equally strong strengths but its weaknesses were significantly less severe (max -8.19 vs -10.00). The current paper's inference confound and overclaiming are more substantive issues.

The most impactful items that differentiate this paper from the 7.0 anchor are the inference confound (-9.57) and the mechanistic overclaim (-10.00). These pull the paper below 7.0. Compared to the 6.0 anchor, the paper's stronger strengths and cleaner experimental design push it above 6.0. The resulting placement is 6.5.

**Final score: 6.5** — borderline accept. Solid paper with real contribution held back by a methodological confound and overclaiming.

Now let me write the final review text.

Wait, I need to reconsider - the decision should be Accept (since 6.5 is "borderline accept" in the ICLR scale). Let me finalize.

Actually, I realize I need to do one more careful check. Let me re-read the inference confound issue more carefully in the paper to make sure I'm not overstating it.

The paper says (line 81): "In both of our studies, we provided instructions in the prompts to choose only from a fixed set of terms. The Gemini API supports controlled generation which makes this constrained classification task straightforward; for all open-weight models, we used log probability based scoring of the allowed terms as a continuation of the prompt."

So for the English naming task: The set of allowed terms is English color words. Gemini uses controlled generation (the API forces the output to be one of the allowed color terms). Open-weight models compute log-probabilities for each allowed term as a continuation of the prompt and pick the highest.

For the IICLL task: The set of allowed terms at each generation is the set of pseudo-words from the previous generation. Same two methods apply.

The critic's concern: Log-prob scoring systematically favors shorter strings because each additional token multiplies probabilities. This is partially true but oversimplified. Log-prob scoring normalizes by token count in some implementations, but not all. The paper doesn't specify whether length normalization is used.

However, even without length normalization, the effect would depend on the tokenization of the specific terms. Many basic color terms are single tokens (red, blue, green, yellow, etc.). Some are multi-token (turquoise might be 2 tokens, maroon might be 1-2 tokens). The magnitude of the bias is unclear.

For IICLL, the pseudo-words could vary in token length depending on the specific pseudo-words used. But the number of categories k is fixed per condition, so all k labels must be used. The log-prob scoring would prefer shorter labels but the model still needs to assign colors to all k labels.

I think the confound is real but its impact is likely modest. The paper's surviving claim—that ALL models converge to IB-efficient systems via IICLL—doesn't depend on this confound. Only the claim about Gemini being special depends on it.

So 6.5 seems right. Let me write the review.Now I'll write the final consolidated review.

## Summary

This paper investigates whether LLMs exhibit a human-like inductive bias toward Information Bottleneck (IB) efficient semantic categorization, using color naming as a testbed. It conducts two studies across 39 models: (1) an English color naming study showing that larger instruction-tuned models achieve better alignment and IB-efficiency, and (2) an Iterated In-Context Language Learning (IICLL) study showing that LLMs iteratively restructure initially random category systems toward greater IB-efficiency, with only Gemini 2.0 recapitulating the full human range of near-optimal IB tradeoffs.

## Strengths

- **Principled use of cognitive theory.** The IB framework (Zaslavsky et al., 2018) and iterated learning framework (Griffiths & Kalish, 2007; Kirby et al., 2008) are applied thoughtfully, generating quantitative predictions (the IB bound in Figure 3) compared against real human data from the WCS and Xu et al. (2013). The paper correctly identifies that training on human text is distinct from being trained on the IB objective. (Sections 2.2, 2.3)

- **Large and systematic model sweep.** Testing 39 models across 6 families with variation in size, instruction-tuning, and modality is a genuine strength. The finding that many state-of-the-art LLMs fail to capture English color naming, that instruction tuning plays a key role, and that some models produce systems resembling low-resource WCS languages rather than English are concrete empirical contributions. (Section 3, Figure 2, Appendix D)

- **Complementary two-experiment design.** The English naming study establishes what LLMs know about color categories; the IICLL study tests whether this reflects underlying bias or just memorization. The rotation analysis provides a control showing the evolved systems are non-random and non-trivial. (Sections 4.1, 4.2)

- **The IICLL paradigm is a useful methodological contribution.** Adapting I-ICL (Zhu & Griffiths, 2024) to the language-learning setting closely mirrors human ILL experiments and could be valuable for future work probing inductive biases in other semantic domains.

## Weaknesses

### Major

- **Inference method confound between Gemini and all other models.** The paper states (Section 3, line 81): *"The Gemini API supports controlled generation which makes this constrained classification task straightforward; for all open-weight models, we used log probability based scoring of the allowed terms as a continuation of the prompt."* This methodological difference directly affects the headline finding that only Gemini recapitulates the human range of IB tradeoffs. Log-prob scoring can systematically favor shorter continuations (each additional token multiplies probabilities), which could bias open-weight models toward simpler category systems for purely methodological reasons. This confound applies to both the English naming and IICLL studies, weakening the central between-model comparison that drives the paper's most prominent narrative. The basic finding that *all* models converge to IB-efficient systems via IICLL is robust (since open-weight models all use the same method), but the claim that Gemini is uniquely capable of matching the human range requires addressing this confound.

- **The mechanistic claim goes beyond the evidence.** The abstract concludes that human-aligned semantic categories emerge *"via the same fundamental principle that underlies semantic efficiency in humans"* and the discussion states LLMs are *"guided by the same IB-efficiency principle that underlies human languages."* The paper's evidence is descriptive: LLM systems are often near the IB bound and converge toward it under IICLL. This is consistent with the IB principle as a *descriptive* framework, but the paper does not show that LLMs optimize an IB objective, experience a complexity-accuracy tradeoff as a pressure on their representations, or arrive at IB-efficient systems through the same mechanism as humans. The Discussion appropriately notes that *"the precise origins of the bias we observe in LLMs toward efficiency are unclear,"* which partially mitigates this concern, but the abstract and title remain overclaimed relative to the evidence.

- **The IICLL results do not uniquely distinguish an IB-efficiency bias from ICL capacity constraints.** The paper's own observation (Section 4.2, line 143) that *"the IICLL task requires very strong in-context learning"* and that weaker ICL models converge to low-complexity solutions is equally consistent with the alternative hypothesis that what is being measured is ICL capability rather than an inductive bias toward IB-efficiency per se. The rotation analysis shows the systems are non-random but does not specifically support IB-efficiency bias over general regularity-seeking tendencies. The paper acknowledges this possibility in passing but does not run control experiments (e.g., providing more in-context examples to weaker models) that could distinguish the alternatives.

### Minor

- **The Shepard circles experiment (Section 4.3) is too preliminary to support even the hedged generalization claims.** It tests only Gemini with k=4 labels, uses images (numerical inputs failed), and does not include IB analysis. The paper appropriately uses hedging language ("preliminary investigation," "potentially"), but the section still contributes little evidentiary weight to the paper's core claims.

- **The paper invokes the Griffiths & Kalish (2007) convergence theorem** to justify interpreting IICLL outputs as revealing inductive biases (Section 2.3, line 67), explicitly noting its conditions (Bayesian agents with shared priors and likelihoods), but does not discuss whether autoregressive transformer LLMs satisfy these conditions. This gap should be acknowledged explicitly.

- **The rotation analysis** (Section 4.2, line 145) reports a "significant decrease" for Gemini but "less conclusive" results for others without reporting effect sizes, test statistics, or confidence intervals for the rotation effect.

### Trivial

None.

## Nice-to-Haves

1. Run at least one open-weight model with controlled generation (or Gemini with log-prob scoring) to verify that the inference method does not drive the Gemini-vs-others difference.
2. Run IICLL with more in-context examples for weaker models to test whether the limitation is ICL capacity or absence of bias.
3. Add quantitative similarity measures between LLM and human IICLL trajectories (e.g., comparing distributions of final-generation systems in IB space).
4. Report statistical details for the rotation analysis.

## Removed Points

These points from the harsh critic review were removed per filtering rules:

- **"Number of IICLL chains not stated"** — Removed because experimental design details (chain counts, initializations) would be in the appendix, which the parser strips from all papers. The paper refers to Appendix G and L for these details.
- **"CIELAB performance not discussed"** — Removed as factually incorrect. The paper explicitly discusses this (line 119): *"we find that all models… struggled to align with English naming when colors are presented in CIELAB. This reveals a key difference."*
- **"Omission of GPT-family models"** — Removed. The paper's model selection (open-weight models accessible for log-prob scoring plus Gemini) is a legitimate scope decision; the paper cites Marjieh et al. (2024)'s GPT results and does not claim exhaustive coverage.
- **"Human IL trajectory data not overlaid"** — The paper shows human IL data in Figure 3 (plus signs) and provides quantitative baselines in Figure 4. Too minor to retain.
- **Criticisms framed as speculation** (e.g., "if log-prob scoring disadvantages longer pseudo-words…") — Where insufficiently anchored to specific evidence in the paper, these were merged into the retained weaknesses rather than kept as separate items.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. In a rebuttal, address the inference confound experimentally: run at least one open-weight model using controlled generation (if available) or run Gemini with log-prob scoring and demonstrate equivalent results.
2. Hedge the mechanistic claims: replace "same fundamental principle" language with phrasing like "consistent with the IB principle" or "achieve comparable levels of IB-efficiency."
3. Provide quantitative trajectory-similarity measures between LLM and human IICLL data.
4. Report effect sizes and confidence intervals for the rotation analysis.

## Score and Decision

**Round 1 bracket:** 5.5–7.5, anchored on the low side by the telephone game paper (fN8yLc3eA7, avg 6.0—mixed reception, many severe weaknesses, weaker strengths) and on the high side by the VLM bias paper (iVMcYxTiVM, avg 7.0—clean methodology, only minor weaknesses).

**Narrowing:** Compared to the telephone game anchor (6.0), this paper has stronger strengths (three at +9.9+ vs max +8.89) and fewer severe weaknesses. Compared to the VLM bias anchor (7.0), this paper has comparable strengths but its weaknesses are more substantive (an inference confound and an overclaimed mechanistic claim vs only minor significance concerns). The inference confound (-9.57 impact) and mechanistic overclaim (-10.00 impact) are the decisive items pulling this paper below 7.0; the very strong strengths (+9.92 to +9.99) push it above 6.0.

**Final score: 6.5** — borderline accept. The paper makes a genuine contribution by bringing a sophisticated cognitive-science framework to LLM evaluation, conducting a large-scale model sweep, and introducing the IICLL paradigm. However, the central between-model comparison is confounded by different inference methods, and the paper overclaims on mechanism. Both issues are addressable.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>