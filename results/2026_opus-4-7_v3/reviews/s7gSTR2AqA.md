Let me read the paper in chunks to verify the reviewer's claims.Now let me read the IICLL details more carefully and the discussion section:Now I have a thorough understanding of the paper. Let me draft the review before calibration.Now let me run calibration Round 1 — bracketing across score bands:Let me read a few key anchors to calibrate my scoring:Now let me read one more mid-range anchor that's very relevant - the Neural Language of Thought paper:Now I have sufficient calibration data. Let me produce the final review.

**Round 1 Bracket Analysis:**

- **Score 1.0 anchors**: Clearly very weak/pseudo-papers. The paper under review is far superior.
- **Score 3.0-3.4 anchors**: Rejected with significant problems. This paper is substantially better.
- **Score 4.25-5.25 anchors**: The "Theory of LLM sampling" (4.25) had vague methodology and overclaimed conclusions with weak evidence. The current paper is more rigorous.
- **Score 5.75-6.50 anchors**: "Building Abstract Representations" (6.50) and "Neural Language of Thought Models" (6.50) are cognitive-science-meets-AI papers accepted with concerns. The current paper is comparable in quality.
- **Score 8.0 anchors**: TopoLM (8.00) has a cleaner novel contribution and more direct experimental validation. The current paper's overclaiming gap prevents it from reaching this level.
- **Score 8.5+**: No results found.

**Initial bracket: 5.5–7.0**

Given this bracket and my analysis, here is my final consolidated review:

---

## Summary
This paper investigates whether LLMs exhibit human-like inductive biases toward Information Bottleneck (IB)-efficient semantic categorization, using color naming as its primary testbed. It contributes two studies: (1) an English color naming experiment across 39 models from 6 families, revealing wide variation in IB-efficiency and alignment, and (2) a novel Iterated In-Context Language Learning (IICLL) paradigm simulating cultural evolution of pseudo color-naming systems. The key finding is that LLMs converge toward IB-efficient categorization over IICLL generations, though only Gemini 2.0 recapitulates the full range of near-optimal tradeoffs observed across human languages.

## Strengths

- **Principled theoretical framework enabling direct human-LLM comparison.** The use of the IB framework (Zaslavsky et al., 2018) and replication of two specific human experiments (Lindsey & Brown, 2014; Xu et al., 2013) provides quantitative, non-ad-hoc evaluation measures (efficiency loss, NID-based alignment, IB-alignment) defined in Section 3. This enables genuine comparison rather than loose analogies.

- **Unusually thorough model survey with informative negative results.** Testing 39 models across 6 families varying size, instruction-tuning, and modality (Section 3, Figure 2c) is substantially more comprehensive than typical studies. The finding that many state-of-the-art models *fail* to recapitulate even English color naming (Figure 2a,b) is a genuinely interesting negative result. The observation that some models (Olmo 2 32B inst., Qwen 2.5 VL 7B inst.) produce systems resembling low-resource WCS languages (Section 4.1, Appendix E) rather than English adds an unexpected and informative dimension.

- **Creative IICLL methodology.** Adapting Zhu & Griffiths (2024)'s I-ICL framework to full iterated *language* learning with pseudo-labels and abstract feature representations (Section 2.3, Figure 1c) is a well-motivated methodological contribution. Presenting colors as "features" with pseudo terms constitutes a genuine attempt to control for training-data associations.

- **Thoughtful controls.** The rotation analysis (Section 4.2, Appendix H), the feature-based clustering baseline (Appendix M), and the Olmo training trajectory analysis (Appendix F)—showing instruction-tuning as the primary driver of English-alignment rather than pre-training—strengthen the empirical claims and provide mechanistic insight.

## Weaknesses

### Fatal
None

### Major
- **The sRGB training-data confound is insufficiently controlled, undermining the central "inductive bias" claim.** The paper's core argument (abstract, Sections 1, 4.2, 5) is that LLMs exhibit a genuine inductive bias toward IB-efficiency rather than "merely mimicking patterns in their training data." The IICLL paradigm uses pseudo-labels and abstract "features" framing, which is a reasonable first step. However, the stimuli remain sRGB coordinates—a representation ubiquitous in web data, design tutorials, and code. The paper's *own* finding in Section 4.1 that all models fail with CIELAB coordinates directly demonstrates that LLM color knowledge is tied to specific training-data representations, not abstract perceptual understanding. If models cannot generalize across equivalent color representations, their IB-efficient behavior with sRGB inputs is more parsimoniously explained by leveraging learned sRGB→category associations than by a domain-general compression bias. The paper acknowledges the question is open in Section 5 ("the precise origins of the bias we observe in LLMs toward efficiency are unclear"), but the abstract and introduction frame the findings as demonstrative rather than suggestive.

- **The full range of human-like IB-tradeoffs rests on a single model (Gemini 2.0).** Only Gemini recapitulates the wide range of near-optimal IB tradeoffs observed across human languages (Figure 3). The other three models (Gemma 3 27B, Llama 3.3 70B, Qwen 2.5 32B) converge to low-complexity solutions. This convergence is ambiguous: it could reflect (a) an IB-bias expressible only at low complexity, or (b) limited in-context learning capacity causing category-distinction collapse (which trivially lands near the IB bound at low complexity). The paper acknowledges the in-context learning explanation (Section 4.2) but treats it as secondary. The rotation analysis—the paper's most important control—produces "less conclusive" results for non-Gemini models, weakening generality. The title and abstract claim "LLMs" rather than reflecting this model-specificity.

### Minor
- **The iterated learning analogy has an unaddressed theoretical gap.** In human IL (Griffiths & Kalish, 2007), convergence-to-the-prior depends on *different* learners at each generation. IICLL iterates the *same* model. The paper cites the Griffiths & Kalish (2007) convergence result (Section 2.3) without discussing whether it applies when the learner population is size one. This follows established I-ICL methodology from Zhu & Griffiths (2024), so it is not a novel flaw, but the theoretical interpretation—that IICLL "reveals implicit inductive biases" analogously to human IL—deserves explicit qualification.

- **The "perceptually grounded" language in Section 5 overclaims.** The conclusion states LLMs are "capable of evolving perceptually grounded, human-like semantic systems" (line 167), yet Section 4.1 shows that CIELAB coordinates fail for all models and that image inputs do not consistently improve performance for larger multimodal models (Appendix E). These results suggest the opposite of perceptual grounding.

- **The Shepard circles experiment (Section 4.3) is too preliminary for its claimed role.** It uses only Gemini, k=4, 4 chains, with no IB-efficiency analysis and no human comparison data. The paper itself calls this "preliminary investigation" and "initial evidence," yet the Discussion draws on it for domain-generalization claims.

- **Absence of formal statistical testing.** Figure 4 shows 95% confidence intervals but no tests of whether final-generation metrics significantly differ from random initialization, or whether Gemini significantly outperforms other models. The rotation analysis reports "less conclusive" results for non-Gemini models without quantification (e.g., effect sizes, p-values).

### Trivial
- Methodological asymmetry between Gemini (API-based controlled generation) and open-weight models (log-probability scoring) is not discussed as a potential confound. These different decoding methods could systematically affect category structure.

## Nice-to-Haves
- Run IICLL with stimuli from a continuous space that cannot be recognized as any familiar domain (e.g., arbitrary 3D feature vectors with a Gaussian similarity kernel). If convergence to IB-efficiency persists, the inductive-bias claim would be substantially strengthened.
- Formally address how single-model IICLL dynamics differ from multi-agent IL (e.g., varying temperature or random seeds per generation to simulate population variability).
- Expand on the intriguing finding that Gemini *exceeds* human IL trajectories in efficiency and alignment (Section 4.2)—what does this imply about the nature and origin of the bias?
- Add statistical significance tests to key comparisons and the rotation analysis.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Reproducibility concern about Gemini being closed-source with unknown training details**: While contextually relevant, this amounts to questioning the availability/verifiability of a cited model, which violates the hard rule. The relevant substance (possible training-data exposure to IB/WCS material) is subsumed by the sRGB confound weakness above.
- **Demand for more IICLL setup details in main text** (number of chains, generations, sampling procedure): The paper's reproducibility statement points to appendices with these details, and demanding appendix content in the main text is a formatting preference.
- **Concern about missing related work**: Cannot verify specific omissions.

## Novel Insights
The paper's most genuinely novel observations are: (1) the finding that some LLMs produce color naming systems resembling low-resource WCS languages rather than English, despite being trained predominantly on English—suggesting a generic color-categorization capacity that is only refined to English-like systems through instruction-tuning (supported by the Olmo training trajectory in Appendix F); (2) the IICLL methodology itself is a useful, reusable contribution for the CogSci/AI community; and (3) the observation that many IICLL trajectories initially *climb* in complexity toward the IB bound before evolving downward (Section 4.2), which is a specific and informative characterization of the dynamics.

## Suggestions
- Reframe the abstract and title to accurately reflect the model-specificity of the full-range IICLL result, e.g., "Among tested models, only the model with strongest in-context capabilities recapitulates the full range…" — this is already stated in the abstract's body but contradicted by the framing.
- Conduct IICLL with non-sRGB stimuli in an abstract feature space to provide a cleaner test of the inductive-bias hypothesis.
- Add formal statistical tests (effect sizes, permutation tests) to the rotation analysis and generation-over-generation comparisons.
- Explicitly discuss the single-model-across-generations issue and qualify the theoretical analogy to human iterated learning.
- Soften "perceptually grounded" language in Section 5 to be consistent with the CIELAB and image-input findings.

## Score and Decision

### Calibration Anchors (Round 1)

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| Chinese NLP Humanoid Robots | gwZ90hFSL2 | 1.00 | R1 | Far weaker—pseudoscientific, no real contribution |
| Systematic Review of LLMs | 8QTpYC4smR | 1.00 | R1 | Far weaker—survey with no novel contribution |
| UMAP Scientific Discourse | P49gSPmrvN | 1.00 | R1 | Far weaker—basic visualization, no rigor |
| NEMESIS Jailbreaking | 5kMwiMnUip | 1.40 | R1 | Far weaker—limited contribution |
| LLM Concept Banks | KLUDshUx2V | 3.40 | R1 | Weaker—less rigorous framework, narrower experiments |
| Entropy/Semantics from Tokens | z3DMFpaP6m | 3.00 | R1 | Weaker—novel metric but limited validation |
| Knowledge Graph Universality | f7aWmxgSN4 | 3.00 | R1 | Weaker—interesting claims but insufficient evidence |
| VQ-VAE/Diffusion Tokenizers | IqGVIU4rvM | 2.50 | R1 | Weaker—narrow contribution, methodological issues |
| Concepts' IB Models | 2xRTdzmQ6C | 4.40 | R1 | Somewhat weaker—IB-related but less thorough experiments |
| Narrowing IB for Multimodal | INqLJwqUmc | 5.25 | R1 | Slightly weaker—similar IB theme but less comprehensive |
| Theory of LLM Sampling | ejvf3JrZuC | 4.25 | R1 | Weaker—vaguer methodology, overclaimed with less evidence; read in full |
| LLMs as Entropy Models | ulIW7Frjpn | 4.75 | R1 | Somewhat weaker—narrower scope |
| Concept Bottleneck LLMs | RC5FPYVQaH | 5.75 | R1 | Comparable—accepted with concerns, but different focus |
| Abstract Representations | xIUUnzrUtD | 6.50 | R1 | Comparable quality—cognitive science + AI, accepted with limitations; read in full |
| Neural Language of Thought | HYyRwm367m | 6.50 | R1 | Comparable—cognitive science bridge paper with novel method; read in full |
| Enhancing LMM Cognition | lHbLpwbEyt | 6.00 | R1 | Comparable—accepted with all-6 scores |
| Modality Gap/Object Bias VLMs | uAFHCZRmXk | 8.00 | R1 | Stronger—cleaner experimental design, broader validation |
| Submodular File Selection | f4gF6AIHRy | 8.00 | R1 | Stronger—novel algorithm with clear experimental support |
| TopoLM | aWXnKanInf | 8.00 | R1 | Stronger—novel model with cleaner contribution and brain alignment evidence; read in full |
| Visual Data-Type Understanding | WyEdX2R4er | 8.00 | R1 | Stronger—thorough empirical study with clearer conclusions |

**Round 1 bracket: 5.5–7.0**

**Narrowing rationale:** The paper is clearly above the 3-5 range (those papers have fundamental methodological issues or vague contributions). It is comparable to the 6.0-6.5 accepted papers: like "Building Abstract Representations" (6.5) and "Neural Language of Thought" (6.5), it bridges cognitive science and AI with a well-designed study and genuine methodology contribution, but has limitations that prevent clean support of its stronger claims. It falls short of the 8.0 papers, which have cleaner contributions and stronger evidence-to-claim ratios.

The two major weaknesses (sRGB confound undermining the central causal claim, and single-model dependence for the full result) are significant but not fatal—the experimental design is sound, the methodology is valuable, and the findings are interesting under conservative interpretation. The overclaiming in the abstract/introduction relative to the evidence is the paper's key deficit: if framed more modestly as suggestive rather than demonstrative evidence for an inductive bias, these findings would be a solid contribution.

**Final score: 6.0** — Borderline accept. The paper asks a genuinely interesting question, uses well-chosen theoretical frameworks, contributes a reusable methodology (IICLL), and provides a thorough empirical survey. However, the central causal claim (inductive bias toward IB-efficiency rather than training-data patterns) is not cleanly separated from the sRGB confound, and the strongest results depend on a single model. The work brings value to the community but needs more careful framing of what the evidence actually supports.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>