## Summary
This paper proposes the *Fast and Slow Effect* (FSE) framework for evaluating whether LLM/VLM-generated concept annotations are *sufficient* for concept-based XAI models. The framework progressively refines concept annotations through five coarse-to-fine stages and uses a novel *Class Representation Index* (CRI) to measure whether accumulated concepts can alone support correct classification against semantically similar distractors. Key empirical finding: on fine-grained datasets, the "slow mode" (concept-only classification) drops by 25%+ in CRI relative to "fast mode" (direct visual classification), and the common utility-as-proxy evaluation paradigm for annotation quality can be misleading.

## Strengths
- **Important and well-scoped research question**: The sufficiency of LLM-generated concept annotations for XAI is underexplored yet practically important. The paper clearly motivates why existing validation approaches (human evaluation, utility-as-proxy) are inadequate, providing a genuine gap in the literature.
- **Well-defined framework with clear formalism**: Definition 3.1 provides a precise, principled notion of "sufficient" annotation. The five-stage concept-chain gathering extends prior hierarchical extraction practices (1–3 stages in prior work) to a more granular continuum, and the CRI metric (Eq. 2) is straightforward to compute and interpret.
- **Revealing empirical finding on utility-as-proxy**: Table 4 demonstrates convincingly that the fused mode (visual + text) achieves ~90% CRI while the slow mode (text-only) achieves ~50%, directly showing that downstream task performance is an unreliable proxy for annotation quality. This is a practically valuable insight for the concept-based modeling community.
- **Comprehensive evaluation across models and datasets**: Six LLM variants from three model families (GPT, Llama, Qwen) are evaluated across five datasets including both fine-grained and general recognition benchmarks, providing reasonably broad coverage.

## Weaknesses
### Fatal
None.

### Major
- **Self-evaluation bias in CRI**: The same LLM generates concepts *and* evaluates whether those concepts are sufficient by attempting classification based on them. This conflates two failure modes: (1) the concepts genuinely lack discriminative information, and (2) the LLM is poor at reasoning over its own text-only concept representations. Without a human-concept baseline—showing that human-written concepts achieve high CRI in slow mode—the paper cannot disentangle these possibilities. The observed fast-slow gap could partially reflect inherent limitations of text-only LLM inference rather than concept insufficiency.
- **Distractor construction conflates visual and semantic similarity**: The Semantic Similarity Dictionary (SSD) is built from ResNet-18 prediction confusions (Section 5.3), which captures *visual* confusability according to a specific CNN, not true *semantic* similarity. This conflates perceptual difficulty with conceptual insufficiency. The paper should use established semantic similarity measures (e.g., WordNet distance, embedding-based semantic similarity) to construct distractors.
- **Nuanced results are under-discussed**: Table 3 shows that on general datasets (CIFAR-100, Caltech-101), slow mode *does* outperform fast mode, with CRI exceeding 90%. This contradicts the paper's headline claim about annotation insufficiency and suggests the limitation is dataset-dependent rather than fundamental to LLM annotators. The paper acknowledges this in passing but does not provide sufficient analysis of *why* the gap reverses—this analysis is critical for understanding the true scope and limits of the finding.

### Minor
- **CRI formula notation confusion**: In Equation 2, the summation runs from $i=1$ to $t$ with division by $t$, but $t$ is the annotation step throughout the paper while the test set size is $l$. If this is a parsing artifact, it should be noted; if intentional, the notation is internally inconsistent with the test case definition $\mathcal{D}_{\text{test}}$.
- **Small sample in preliminary experiment**: Table 1 uses only 100 images per dataset for the distractor strategy selection. While sufficient for a preliminary test, this limits confidence in the claim that semantically related selection is categorically superior.
- **Five-stage design justification is somewhat post-hoc**: The paper cites prior works using 1–3 stages and extends to 5, but provides no ablation over the number of stages or convergence analysis showing whether 5 stages is necessary/sufficient.

### Trivial
None.

## Nice-to-Haves
- An evaluation using human-generated concept annotations as a baseline for CRI, which would directly validate whether the framework measures concept quality vs. LLM text-reasoning ability.
- An analysis of what types of concepts the LLM fails to generate in slow mode (e.g., are fine-grained visual attributes systematically missing?).
- A sensitivity analysis over the number of distractors (currently fixed at 4) and the number of annotation stages.

## Novel Insights
The paper's most novel insight is that high downstream task utility can coexist with fundamentally insufficient concept annotations—the fused mode masking concept inadequacy. This directly challenges the increasingly common practice of using task performance as a proxy for annotation quality in concept-based XAI, and provides a concrete, automated diagnostic tool (FSE/CRI) to detect this failure mode. The observation that LLMs struggle to externalize their implicit visual expertise into explicit textual concepts (the fast-slow gap) is also a noteworthy contribution to understanding LLM knowledge representation.

## Suggestions
- Add a human-concept baseline: collect or use existing human-annotated concept sets and measure their CRI under the same protocol. This is the single most impactful experiment to validate the framework's ability to distinguish good from bad annotations.
- Refine distractor construction to use semantic (not visual-model-based) similarity, and report how results change under different distractor strategies.
- Provide a deeper analysis of the fine-grained vs. general dataset divergence, ideally identifying dataset characteristics (e.g., inter-class similarity, number of discriminative visual features) that predict when slow mode will underperform.

## Score and Decision
The paper addresses an important question with a novel framework and produces practically valuable findings about annotation sufficiency in XAI. However, the self-evaluation methodology and the lack of human baselines prevent definitive attribution of the observed fast-slow gap to concept insufficiency rather than LLM text-reasoning limitations. The nuanced dataset-dependent results further complicate the main narrative. The contribution is solid but requires stronger validation to be fully convincing.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: Reject