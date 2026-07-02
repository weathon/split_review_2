## Summary
# Final Review Report

## Summary

This paper investigates whether large language models (LLMs) exhibit a human-like inductive bias toward Information Bottleneck (IB)-efficient semantic categorization, using color naming as a testbed. The authors conduct two main studies: (1) an English color-naming evaluation across 39 LLMs, finding that larger instruction-tuned models achieve higher IB-efficiency and English-alignment, though no model matches human performance perfectly; and (2) an Iterated In-Context Language Learning (IICLL) paradigm that simulates cultural transmission of artificial color-naming systems, revealing that LLMs iteratively restructure random systems toward greater IB-efficiency. Only Gemini 2.0 recapitulates the full range of near-optimal IB tradeoffs observed across human languages, while other models converge to lower-complexity solutions. A preliminary Shepard circles experiment suggests potential generalization beyond color. The work is theory-driven, well-motivated, and makes creative use of the IB framework and iterated learning paradigms to probe LLM semantic representations. However, the paper's causal claims about LLMs being "guided by" the IB principle are not fully supported by the correlational evidence, key statistical reliability information is missing, and the theoretical mapping between IICLL dynamics and LLM inductive biases requires more careful qualification. Novelty and external comparison conclusions are deferred as external literature verification was unavailable in this run.

## Strengths
1. **Strong theoretical grounding.** The paper builds on a well-established IB framework for semantic systems (Zaslavsky et al., 2018) with broad empirical support across human languages. Using this framework to analyze LLM color naming provides a principled, information-theoretic lens that goes beyond simple accuracy comparisons. The connection between the IB principle and iterated learning is conceptually elegant and generates concrete, falsifiable predictions.

2. **Creative experimental paradigm (IICLL).** Extending I-ICL (Zhu & Griffiths, 2024) to iterated in-context *language* learning is a novel methodological contribution. The paradigm directly adapts human iterated language learning experiments to LLMs, enabling unusually direct comparison between human and machine cultural evolution dynamics. Using pseudo-words and hiding the color domain ("features" rather than colors) is a well-designed control against simple pattern matching.

3. **Comprehensive model coverage.** Testing 39 models across 6 families with varying sizes, training stages, and modalities is a substantial empirical contribution. The inclusion of both base and instruction-tuned variants, and analysis of Olmo training checkpoints, provides useful evidence about which model properties correlate with human-like color categorization.

4. **Rotation analysis for non-triviality check.** The rotation analysis (Section 4.2) addresses an important confound—whether IB-efficiency arises trivially from the color space geometry rather than from the model's inductive biases. Finding that Gemini's efficiency drops significantly under rotation strengthens the argument that its IICLL systems reflect genuine structure-seeking behavior.

5. **Transparent limitations.** The Discussion explicitly acknowledges several open questions (the need to integrate communicative pressure, the unclear origins of the efficiency bias, and the need for broader cross-linguistic analysis). This openness strengthens the paper's scientific credibility and provides a clear roadmap for follow-up work.

## Weaknesses
### Major Weaknesses

**W1. Causal overclaiming of IB-efficiency as a guiding principle (Page 9 - Discussion).** The paper states that LLMs are "guided by the same IB-efficiency principle that underlies human languages" and that IB-efficiency "may emerge to support intelligent behavior." These are strong causal and teleological claims. The evidence shows that IICLL trajectories *converge to* IB-efficient solutions, which is a descriptive finding. The paper does not provide mechanistic evidence that IB-efficiency is the causal driver of this convergence rather than a descriptive property of any structured categorization in this stimulus space given perceptual geometry. The rotation analysis partially addresses this but only for Gemini, and the results for other models are "less conclusive." The Discussion should replace causal framing ("guided by") with correlational framing ("consistent with," "align with"). **Fix: Replace causal language throughout and add a sentence clarifying the descriptive vs. prescriptive distinction.**

**W2. Missing statistical reliability evidence (Page 5 - Section 4.1).** All model comparisons in the English color naming study are reported as point estimates without variance, confidence intervals, or significance tests. The paper does not specify whether models were run multiple times with different seeds/prompts or whether results are deterministic. Given that alignment values in Figure 2c range continuously from ~0.1 to ~0.55, readers cannot assess whether a difference of 0.05 between models is meaningful or within measurement noise. This is especially critical for the claim that "larger instruction-tuned models achieve better alignment and IB-efficiency"—without variability estimates, this ordering could be unstable. **Fix: Report bootstrap confidence intervals for key models (Gemini, Gemma, Llama, Qwen) in both the English naming and IICLL experiments. At minimum, acknowledge the lack of repeated measurements as a limitation.**

**W3. Unaddressed gap between IL theory and IICLL interpretation (Page 3-4 - Section 2.3).** The paper invokes the theoretical result of Griffiths & Kalish (2007) that IL converges to the learner's prior $p(L)$ under Bayesian assumptions, then applies IICLL to LLMs without addressing whether LLMs satisfy these Bayesian conditions. LLMs are transformer-based next-token prediction models, not Bayesian agents with shared priors and likelihoods. The empirical IICLL results are valuable independently, but the paper's interpretive framing—that IICLL "reveals LLMs' implicit inductive biases"—relies on a theoretical guarantee that does not apply to LLMs. **Fix: Add an explicit caveat that the Griffiths & Kalish convergence theorem assumes Bayesian agents and does not automatically extend to IICLL with LLMs; clarify that IICLL provides behavioral evidence consistent with an inductive bias rather than a formal characterization of priors.**

**W4. Underdetermined explanation for Gemini's advantage (Page 7 - Section 4.2).** The paper attributes Gemini's superior IICLL performance to its "strongest in-context capabilities" without independent verification on this specific task. Alternative explanations are not discussed: training data composition (Gemini may have seen more diverse color-language associations), instruction-tuning methodology (different alignment procedures), API infrastructure differences (controlled generation vs. log-probability scoring), or architectural differences. **Fix: Acknowledge these alternative explanations explicitly and temper the claim that ICL capacity is the differentiating factor.**

**W5. Quantitative magnitudes missing for input representation analysis (Page 6 - Section 4.1).** The finding that CIELAB coordinates hurt performance is described only qualitatively ("all models struggled"). The comparison of image vs. text inputs lacks reported effect sizes. These are potentially important results about LLMs' lack of perceptual grounding, but without numbers (e.g., "English-alignment dropped from X to Y"), the reader cannot assess the severity of the effect. **Fix: Add a compact table in the main text reporting alignment and complexity scores for key models under each input condition.**

### Minor Weaknesses

**W6. Overclaim of "novel theoretical framework" (Page 1 - Introduction).** The paper describes its approach as "a novel theoretical and cognitively-motivated framework for studying semantic systems in LLMs." In fact, the theoretical framework is the IB model from Zaslavsky et al. (2018) applied to LLMs—the novelty lies in the experimental paradigm (IICLL) and behavioral replication, not in the theoretical apparatus. Rephrase to: "a theory-driven approach, grounded in the IB framework, combined with a novel experimental paradigm."

**W7. Uniqueness claim about color data needs qualification (Page 2 - Section 2.1).** The claim that the WCS + IL data combination is "unique to the domain of color" is strong. Other semantic domains (kinship, spatial language, odor categories) also have substantial cross-linguistic datasets. Soften to: "Among semantic domains, color is exceptionally well-resourced with both types of data."

**W8. Efficiency loss formula missing definition of B (Page 4 - Section 3).** The normalization term B in the efficiency loss $\varepsilon$ formula is not explicitly defined. This makes the absolute magnitude of $\varepsilon$ values (0 to ~1.5 in Figure 4a) difficult to interpret. Add: "where B is [the number of $\beta$ values sampled / a normalization constant], and $\varepsilon=0$ indicates an optimal system."

**W9. Shepard circles experiment overclaims domain generality (Page 8 - Section 4.3).** The conclusion that LLMs have a "domain-general bias" is based on one model, one category count (k=4), one synthetic domain, and no IB-efficiency analysis. Replace "domain-general" with "a bias that may extend beyond color, pending further evidence."

**W10. Abstract lacks explicit prior-gap sentence (Page 1 - Abstract).** The abstract jumps from the research question directly into the study design without a sentence stating what is missing in prior work. Add a sentence: "However, it remains unknown whether LLMs, which learn language from text alone without communicative grounding, can develop categories that follow the same efficiency principles."

**W11. Novelty and external comparison not verifiable in this run.** External literature search was unavailable (Retrieval-Disabled Mode). All claims about the paper's novelty relative to prior work (e.g., the extent to which IICLL advances beyond I-ICL, NIL, and Carlsson et al. 2024) require manual literature verification. The authors should independently confirm that no directly comparable LLM iterated-learning study exists for color categorization.

## Score
**Final Score: 6.5/10**

**Rationale:** The paper makes a creative and theoretically grounded contribution by bridging the IB framework with LLM evaluation via an innovative IICLL paradigm. The empirical scope (39 models) and the cognitive-science-inspired methodology are clear strengths. However, the score is constrained by several factors: (1) the core causal claim that LLMs are "guided by" IB-efficiency is not adequately supported by the correlational evidence; (2) key statistical reliability information (variance, confidence intervals) is absent, weakening confidence in model rankings; (3) the theoretical mapping between IICLL and LLM inductive biases is not fully justified; and (4) novelty and external comparison claims cannot be verified without literature retrieval. The paper is above the acceptance threshold in its current form for a venue focused on interdisciplinary cognitive science + AI, but requires revisions to the causal framing, statistical reporting, and interpretive caveats before it meets the highest standards of rigor.

### ASCII Diagram — Paper Structure & Evidence Map
```text
[Research Question: Do LLMs exhibit IB-efficiency bias in categorization?]
    |
    +--> [C1: Evaluate English color naming in 39 LLMs]
    |       |
    |       +--> Evidence: IB tradeoff plots (Fig 2a), mode maps (Fig 2b)
    |       +--> Gap: No variance/CI, single-run per model
    |       +--> Verdict: Partially supported — pattern holds but statistical reliability unknown
    |
    +--> [C2: IICLL reveals convergence to IB-efficient systems]
    |       |
    |       +--> Evidence: IICLL trajectories (Fig 3), efficiency loss curves (Fig 4)
    |       +--> Gap: Bayesian IL theory does not apply to LLMs; alternative explanations for Gemini's advantage not tested
    |       +--> Verdict: Partially supported — convergence observed, but causal mechanism unclear
    |
    +--> [C3: Gemini's IB-efficiency reflects genuine inductive bias]
            |
            +--> Evidence: Rotation analysis, WCS-alignment over generations
            +--> Gap: Only one model (Gemini) shows full effect; results "less conclusive" for others
            +--> Verdict: Partially supported for Gemini; unclear for other models
```

### ASCII Diagram — Revision Strategy Roadmap
```text
Priority | Problem                              | Fix                                       | Expected Gain
---------|--------------------------------------|-------------------------------------------|--------------
P0       | Causal overclaim ("guided by")        | Replace with "consistent with" wording    | Strengthens scientific credibility
P1       | Missing statistical reliability       | Add bootstrap CI for key models           | Enables interpretation of model rankings
P2       | IL theory-IICLL gap                   | Add caveat about Bayesian assumptions     | Clarifies interpretive scope
P3       | Underdetermined Gemini explanation    | Acknowledge alternative factors           | Prevents over-attribution to ICL capacity
P4       | Missing quantitative magnitudes       | Add summary table for input conditions    | Enables reader verification
```

### ASCII Diagram — Related-Work Taxonomy Tree (Layered)
```text
LLM Color Naming & Semantic Efficiency (Root)
├── Branch 1: IB Framework for Semantic Systems
│   ├── Leaf 1.1: Human color naming [Zaslavsky et al., 2018; Lindsey & Brown, 2014]
│   ├── Leaf 1.2: Cross-linguistic support [Zaslavsky et al., 2019, 2021, 2022; Mollica et al., 2021]
│   └── Leaf 1.3: Emergent communication [Chaabouni et al., 2022; Tucker et al., 2022; Gualdoni et al., 2024]
├── Branch 2: Color Representations in LLMs
│   ├── Leaf 2.1: Embedding-based recovery [Abdou et al., 2021; Patel & Pavlick, 2022]
│   └── Leaf 2.2: Prompt-based naming [Marjieh et al., 2024] ← Closest to this paper's Study 1
├── Branch 3: Iterated Learning & Cultural Evolution
│   ├── Leaf 3.1: Human iterated learning [Griffiths & Kalish, 2007; Kirby et al., 2008; Xu et al., 2013]
│   ├── Leaf 3.2: Neural iterated learning [Ren et al., 2020; Carlsson et al., 2024]
│   └── Leaf 3.3: LLM iterated in-context learning [Zhu & Griffiths, 2024; Ren et al., 2024; Kumar et al., 2024]
│       └── THIS PAPER: IICLL (Leaf 3.3 extension to language learning)
└── Branch 4: Shepard Circles / Non-Color Categorization
    └── Leaf 4.1: Human categorization [Shepard, 1964; Carr et al., 2020]
        └── THIS PAPER: Preliminary IICLL extension (Section 4.3)

NOTE: Novelty verification is deferred — external literature search was unavailable in this run.
All taxonomy placements and relative novelty assessments require manual literature verification.
```

### Contribution-Level Novelty Conclusion (deferred)
Due to Retrieval-Disabled Mode, external literature could not be searched. The following provisional tags are based on manuscript evidence only and require manual verification:
- **C1 (Large-scale English color naming evaluation):** `unclear` — prior work by Marjieh et al. (2024) tested similar prompt-based naming with fewer models. The main increment (39 models, IB analysis) appears significant but overlap boundaries need verification.
- **C2 (IICLL paradigm):** `unclear` — IICLL extends I-ICL (Zhu & Griffiths, 2024) to language learning. The degree of novelty versus prior I-ICL work and versus NIL-based work (Carlsson et al., 2024) requires literature verification.
- **C3 (Human-like IB-efficiency bias):** `unclear` — while the paper presents compelling behavioral evidence, whether prior work already demonstrated similar biases in LLMs or other neural models needs external verification.