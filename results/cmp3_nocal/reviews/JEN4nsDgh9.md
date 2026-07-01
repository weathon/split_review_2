## Summary

This paper introduces a benchmark for evaluating text-to-image (TTI) models on generating images for WordNet taxonomy concepts (synsets). The benchmark tests 12 models across three dataset splits (common-sense concepts, randomly-sampled WordNet nodes, and LLM-generated predictions), using 9 metrics including taxonomy-specific similarity measures, ELO rankings from human and GPT-4 pairwise evaluation, reward model scores, FID, and IS. The central finding is that model rankings on taxonomy-concept generation diverge from standard T2I benchmarks, with Playground-v2 and FLUX generally outperforming, and that TTI models produce more relevant images than a Wikimedia Commons retrieval baseline. The paper also releases a dataset of generated images covering WordNet-3.0.

## Strengths

- **The problem is genuinely underexplored and well-motivated.** The observation that ImageNet covers only ~6.5% of WordNet synsets (Section 1) establishes a clear gap. The paper correctly distinguishes between standard TTI evaluation (on detailed DiffusionDB-style prompts) and the qualitatively different task of generating images from sparse taxonomic labels (Figure 1, lines 17-46).

- **Broad experimental scope.** The evaluation spans 12 models, 3 dataset splits, 9 metrics, human evaluation (3370 pairwise comparisons, 4 annotators), GPT-4 evaluation, and a reward model. This represents substantial engineering effort. The inclusion of both ground-truth WordNet concepts and LLM-generated predictions (Section 2.3) addresses the practical use case of enriching taxonomies.

- **The headline finding is interesting and practically relevant.** The result that model rankings for taxonomy-concept generation differ from standard T2I rankings (Section 5, abstract) has practical implications for anyone building taxonomy-visualization tools. The explicit comparison to GenAI Arena rankings (lines 19-20, 73-74) makes this point clearly. The paper also reports meaningful correlations between the proposed similarity metrics and human judgment (ρ ≈ 0.91 for Hypernym CLIP-Score, ρ ≈ 0.87 for Cohyponym CLIP-Score, line 231).

## Weaknesses

### Fatal
None.

### Major

- **Gap between claimed theoretical framing and actual metric implementation.** The paper claims the similarity metrics are "derived from KL Divergence and Mutual Information" (contributions list, line 79; Section 4.2, line 209), with formal probabilistic definitions deferred to Appendix D. However, Equations 1–3 in the main text directly define the metrics as CLIP cosine similarity (for Lemma Similarity) and averages of CLIP cosine similarity over hypernyms/cohyponyms. The paper states "In practice, we approximate the probabilities using CLIP similarity" (line 211), but the gap between the KL/MI framing and what is actually computed is never bridged in the main text. This creates a mismatch between what the paper claims as a contribution and what is demonstrated. Either the formal connection should be presented in the main text, or the claims should be weakened to honestly describe the metrics as CLIP-similarity variants that exploit taxonomic structure through averaging. The resulting metrics (averaging similarity over taxonomic neighbors) are still sensible and novel — the problem is the overclaimed theoretical justification, not the metrics themselves.

### Minor

- **Overbroad claim about TTI models outperforming retrieval.** The paper states that "modern Text-to-Image models outperform traditional retrieval-based methods" (line 74) based solely on a retrieval baseline built from Wikimedia Commons (Table 1). As Figure 2 illustrates, Wikimedia Commons can return irrelevant images (e.g., a Buddha statue for "cigar lighter"), but this only demonstrates that Wikimedia Commons is an unreliable retrieval source for WordNet concepts. A stronger retrieval system (e.g., CLIP-based retrieval from LAION-5B or a web-scale search engine) would likely perform far better. The claim about TTI superiority over retrieval is broader than the evidence supports. The authors should either use a stronger retrieval baseline or explicitly caveat the conclusion to the specific retrieval source tested.

- **Metric disagreement is reported but not sufficiently analyzed.** Table 2 shows that different metrics select different top models: SDXL-turbo dominates the CLIP-based similarity metrics while ranking near-worst by ELO (Figure 4), and FID / IS prefer different models still. A benchmark whose metrics point in different directions needs to explain what each metric captures and why disagreement is informative (or problematic). The paper discusses possible reasons briefly (e.g., "CLIP-Score focusing solely on text-image alignment without accounting for image quality," line 265) but does not provide a systematic analysis of the relationship between metrics or guidance for practitioners on which metric to trust for which use case. This limits the usability of the benchmark.

- **GPT-4 position bias is acknowledged but its implications for the claimed contribution are not fully discussed.** The paper finds "no correlation between raw scores for individual battles" due to "a strong bias toward the first option" (line 257), yet lists "pairwise preference evaluation with GPT-4" as a contribution (line 80). While the paper correctly reports rank-level correlations (0.92 with definitions, 0.73 without) which are robust to uniform position bias, the raw-score contamination means the ELO magnitudes may not be meaningful. The paper should discuss this limitation more explicitly when positioning GPT-4 evaluation as a contribution, and ideally test whether counterbalancing presentation order changes results.

- **No per-concept-type analysis (abstract vs. concrete).** Given the taxonomic framing — WordNet includes both highly concrete synsets (e.g., "cat.n.01") and abstract ones (e.g., "chromatic_color.n.01") — the paper would be substantially strengthened by stratifying results by concreteness or abstraction level. Such analysis is the most natural way to demonstrate that the benchmark captures taxonomy-specific capability rather than just general TTI quality.

- **TaxoLLaMA predictions are used without correctness validation.** The LLM-generated concepts (Section 2.3) are described as testing TTI models on "AI-generated content," but there is no evaluation of whether TaxoLLaMA's predictions themselves are correct. If the predictions are wrong, evaluating TTI on them tests the models' ability to depict incorrect concepts, which is not informative for the claimed use case of taxonomy enrichment.

- **No empirical comparison to existing ISP/SCS metrics.** The paper cites Baryshnikov & Ryabinin (2023) and notes that the Specificity metric "generalizes the In-Subtree Probability" (line 243). However, no empirical comparison is made between the new metrics and ISP/SCS, which would help establish whether the proposed metrics add value over existing approaches.

### Trivial

- **The sampling probability description in Section 2.2 is confusing.** The paper gives two different probability sets: 0.1/0.1/0.8 for sampling relations during dataset construction, and 1×10⁻⁵/0.05/0.1 for test set occurrence probabilities (lines 105-106). The relationship between these two distributions and how they produce the reported test set counts (828/170/204) is unclear from the prose and would hinder reproducibility.

- **FID calculation is unusual.** The paper computes FID relative to retrieved images (line 247: "we calculate FID based on retrieved images, meaning that in this specific setting, FID reflects the 'realness' or closeness to retrieval rather than the semantic correctness of an image"). This is an unconventional choice that makes FID scores difficult to interpret and incomparable to standard T2I FID values. The paper should either use a standard reference set or more clearly justify why this choice is appropriate for the benchmark.

## Nice-to-Haves

- An analysis of whether hypernym/cohyponym similarity captures information beyond lemma similarity (e.g., computing Δ = Hypernym Similarity − Lemma Similarity per model to identify cases where the image resembles the parent concept more than the target concept).
- A human evaluation of whether generated images are actually useful for the downstream task of taxonomy illustration (e.g., asking annotators whether an image adequately represents its intended synset).
- Testing whether counterbalancing presentation order in the GPT-4 pairwise comparisons changes the ELO rankings.
- A discussion of whether the CLIP-based metrics are confounded with models that were explicitly trained with CLIP-based objectives (SDXL-turbo being a distilled variant that dominates these metrics is consistent with this concern).

## Removed Points

These points were flagged in the harsh critic input but are removed for the following reasons:

- **"First to evaluate" claim is unqualified** — removed. The paper claims to be "the first to evaluate the performance of the 12 publicly available Text-to-Image models to generate images for WordNet concepts **on the developed benchmark**" (line 82). The qualifier "on the developed benchmark" makes this claim accurate, as the benchmark itself is the novel contribution. Prior work (Baryshnikov & Ryabinin, 2023) evaluated hypernymy understanding with different metrics, not this benchmark.

- **Human evaluation is too small (3370 comparisons, 4 annotators)** — removed. The inter-annotator Spearman correlation of ρ=0.8 (p≤0.05, line 199) and significant rank correlations between human and automatic metrics demonstrate that the human evaluation is sufficient for its purpose. The size is comparable to or larger than human evaluations in many accepted NLP/CV benchmark papers.

- **Model Family column in Table 1 is sparse** — removed. This is a parser artifact from PDF extraction; the original submission likely contained this information.

- **Openjourney's small parameter count (123M) not discussed** — removed. This is a standard model inclusion decision; benchmark papers routinely include models of varying sizes without controlling for parameter count.

## Novel Insights

Beyond the paper's own contributions, the reviews surface one observation worth noting: the conflict between CLIP-based similarity metrics (where SDXL-turbo dominates) and preference-based metrics (where FLUX and Playground dominate) may itself be diagnostic. This pattern suggests that distillation for speed preserves CLIP alignment but degrades human-perceived quality — turning what the paper treats as a "disagreement problem" into a potentially informative signal about the tradeoff between CLIP alignment and human preferences in distilled models. This connection is implicit in the paper's discussion (line 265) but not developed as an insight.

## Suggestions

1. **Reframe the metric claims.** Remove or substantiate the "KL Divergence and Mutual Information" framing. Present the taxonomy similarity metrics honestly as CLIP score variants that exploit taxonomic structure through averaging over hypernyms and cohyponyms — this is sufficient novelty for the benchmark paper.
2. **Strengthen or caveat the retrieval comparison.** Either add a stronger retrieval baseline (e.g., CLIP-based search over LAION-5B or a web image corpus) or explicitly narrow the conclusion to Wikimedia Commons.
3. **Add per-concept-type analysis.** The most compelling evidence for the benchmark's value would be showing which models handle abstract vs. concrete synsets well. This is a straightforward stratification that would directly demonstrate taxonomy-specific insight.
4. **Provide practitioner guidance on metric selection.** Given the disagreement across metrics (Table 2), include a paragraph explaining which metric to prioritize for different downstream goals (e.g., preference for human-facing applications, CLIP-based metrics for alignment-focused evaluation).
5. **Address the GPT-4 position bias.** If possible, report ELO scores with counterbalanced presentation order. At minimum, add an explicit caveat that individual GPT-4 battle judgments are contaminated by position bias and only rank-level aggregates are reliable.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>