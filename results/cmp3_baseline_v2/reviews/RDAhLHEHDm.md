## Summary

This paper challenges the prevailing sequence-centric paradigm in Scientific Large Language Models (Sci-LLMs) by proposing a "context-driven" approach that replaces raw biomolecular sequences with high-level structured annotations from established bioinformatics tools (e.g., InterProScan, BLASTp). Through systematic experiments on protein QA tasks, the authors demonstrate that providing only textual context consistently outperforms both sequence-as-language and sequence-as-modality approaches, and that adding raw sequences to context actually degrades performance. The paper argues that current Sci-LLMs should be reframed as reasoning engines over expert knowledge rather than sequence decoders.

## Strengths

- **Clear and well-motivated research question**: The paper identifies a genuine and important tension in Sci-LLM design—the tokenization dilemma—and formulates a clean hypothesis about whether raw sequences add value beyond structured context.
- **Comprehensive experimental design**: The paper evaluates multiple input configurations (sequence-only, context-only, combined) across diverse models (specialized Sci-LLMs and general-purpose LLMs) and multiple tasks (function, pathway, subcellular localization), providing a thorough empirical comparison.
- **Novel and insightful findings**: The consistent result that adding raw sequences degrades performance is counterintuitive and potentially impactful for the field. The temporal analysis showing differential degradation patterns across paradigms is particularly revealing.
- **Practical validation**: The wet-lab validation on truly novel sequences (unpublished proteins) and the cost-efficiency analysis add real-world credibility to the claims.

## Weaknesses

### Fatal
None.

### Major

- **The context-driven approach conflates tool-based inference with LLM reasoning**: The method uses BLASTp and InterProScan—tools that directly perform the task (e.g., BLASTp retrieves GO annotations from homologs). The LLM is essentially reading pre-computed answers rather than reasoning. This makes the comparison fundamentally unfair: the context-driven approach is not a "reasoning" paradigm but a retrieval-augmented one where the retrieval tools already solve the task. The paper's framing as "reasoning over expert knowledge" obscures that the expert tools are doing the heavy lifting.

- **Information leakage concerns are not fully addressed**: The paper claims to avoid label leakage by using homology-based inference rather than direct annotation matching. However, for many proteins in standard databases, the homologs' annotations are highly correlated with the query's true labels. The "intrinsic analysis" via InterProScan also relies on curated domain databases that are built from the same knowledge sources as the ground truth. The 100% accuracy on novel Rhodopsin sequences is suspicious—if these are truly novel and unpublished, how does BLASTp find informative homologs? This suggests either the sequences are not truly novel or the evaluation is circular.

- **The benchmark tasks are too narrow and simplistic**: The three tasks (molecular function, pathway, subcellular localization) are all directly answerable by the bioinformatics tools used. A more convincing test would involve tasks requiring genuine reasoning: predicting effects of mutations, inferring interaction partners, or explaining mechanisms. The current setup essentially tests whether the LLM can read and summarize tool outputs, not whether it can reason about biology.

- **The "degradation" claim is overstated**: The performance drop from context-only to sequence+context is small (e.g., 86.15 to 84.03 for Intern-S1) and within reasonable variance. The paper presents this as evidence that sequences are "informational noise," but an alternative explanation is that the models are simply confused by redundant or conflicting information. The claim that sequences "consistently and substantially" degrade performance is not supported by the magnitude of the drops.

### Minor

- **The embedding analysis (Section 5.2) compares apples to oranges**: The context-driven approach uses a text embedding model (Qwen-embedding) on textual context, while the other models use their own internal representations of sequences. The near-perfect ARI of 0.958 for the context approach is expected because the context already contains functional labels (GO terms, domain names). This is not a fair comparison of representation quality.

- **The temporal analysis (Section 5.4) has a confound**: The context-driven approach's performance decline over time is attributed to "diminishing availability of rich, homologous information," but this is exactly the same reason Evolla's performance declines. The paper claims superiority for the context approach, but both methods degrade for the same reason—newer proteins have less characterized homologs. The difference in slope magnitude could simply reflect that the context approach has more information to lose.

- **The cost analysis (Table 2) is misleading**: The batch processing time for Evolla (20s) vs. the context method (0.13s) is compared per-sequence, but the context method requires running BLASTp and InterProScan first, which have their own computational costs not fully accounted for in the "batch" scenario.

### Trivial
- The paper uses "Sci-LLMs" as an acronym but the field typically uses "LLMs" or "scientific LLMs."
- Figure 7's "trade-off landscape" is conceptually interesting but the axes are not quantitatively defined for semantic alignment.

## Nice-to-Haves

- Test on tasks that require genuine reasoning beyond what the bioinformatics tools can directly answer (e.g., "What would happen if residue X is mutated to Y?" or "How does this protein interact with protein Z?").
- Include a baseline where the LLM receives raw sequence plus a simple instruction to "use your pre-trained knowledge" without any context, to separate the effect of tool-based retrieval from LLM reasoning.
- Conduct an ablation study where the context is systematically degraded (e.g., removing domain information, removing GO terms) to understand which parts of the context are most valuable.

## Novel Insights

The paper's most genuinely novel observation is that adding raw sequence information to an already informative context consistently degrades performance across multiple models and tasks. This is not obvious a priori—one might expect that more information (sequence + context) would be better than less (context only). The finding suggests a fundamental incompatibility between how current tokenization schemes represent biological sequences and how LLMs process textual information, even when the models are specifically designed for biological sequences. This points to a deeper issue: the "language of biology" may not be amenable to the same tokenization strategies that work for natural language, and forcing this analogy may introduce noise rather than signal. The paper's demonstration that this degradation is consistent across both sequence-as-language and sequence-as-modality paradigms strengthens this insight.

## Suggestions

- Reframe the paper's contribution more honestly: instead of claiming a new "reasoning paradigm," present it as a systematic empirical study showing that current Sci-LLMs do not benefit from raw sequence input when structured context is available. This is a valuable negative result that the community should know about.
- Add a control experiment where the LLM receives the raw sequence plus a random or scrambled context, to verify that the degradation is specific to the sequence-context combination and not just a general effect of longer inputs.
- Include a "context-only" baseline where the context is generated by a simple rule-based system (e.g., just the top BLAST hit) to separate the effect of context quality from the effect of tool-based retrieval.

## Score and Decision

The paper addresses an important question and provides clean, reproducible experiments with a surprising result. However, the core weakness is that the "context-driven approach" is not a novel method but a straightforward application of existing bioinformatics tools, and the comparison is fundamentally unfair because the tools directly solve the benchmark tasks. The paper's framing overclaims the contribution. The empirical finding that sequences degrade performance is valuable, but the paper would be stronger if it acknowledged the limitations of its comparison more explicitly and focused on the negative result rather than proposing a new paradigm.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>