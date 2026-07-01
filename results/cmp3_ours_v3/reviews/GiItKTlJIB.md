## Summary

This paper introduces a deletion-based probing framework to evaluate how much LLMs actually depend on their chain-of-thought (CoT) traces for physics problem solving. By intercepting CoT scratchpads, deleting tokens at varying rates using three strategies (end, random, physics-aware), and measuring downstream effects on answer accuracy, length, and information overlap, the authors find that: (1) accuracy remains stable under moderate deletion (40–60%) before collapsing; (2) models compensate by "cramming" reconstructed reasoning into the final answer; and (3) information overlap between deleted content and regenerated answers increases with deletion. The paper applies this methodology to three open-source models across three physics benchmarks.

## Strengths

1. **Novel deletion-based probing paradigm.** Prior CoT faithfulness work has focused on post-hoc analysis of generated traces or pre-generation prompt perturbation. Intercepting and deleting tokens from the scratchpad mid-generation is a distinct methodological contribution. The core question—whether models actually *depend* on their own CoT traces—is well-posed and practically important for AI-for-Science applications.

2. **The "cramming" observation is a non-trivial empirical finding.** Section 4.1 documents that when CoT tokens are removed, final answers grow longer, with the compensatory increase approximately inverse to reasoning length. This pattern holds across multiple models, datasets, and deletion strategies (end, random, physics-aware). Whether or not this reflects true reconstruction versus generic verbosity, the fact that accuracy can remain stable under 40–60% deletion while answer length rises is a striking and noteworthy pattern.

3. **Reasonable experimental breadth.** The study design crosses three deletion strategies × three models × three datasets, providing adequate coverage for a first investigation. The choice of open-source models (enabling scratchpad access) is appropriate given the research question.

## Weaknesses

### Fatal
None.

### Major

1. **Overlap metrics are mismatched to the faithfulness claims (Contribution 3).**  
   The paper claims "a rigorous faithfulness analysis leveraging the structured nature of physics and mathematics" (Section 1, Contribution 3) and that the domain's structure "enables precise quantification." However, the actual metrics used (Section 4.2) are Jaccard similarity and Manhattan distance over bag-of-words token representations—among the least structured possible text similarity metrics. Equations are flattened to word bags (e.g., "F = ma" and "a = F/m" would produce similar token overlap despite containing different physical information). The paper itself acknowledges these measure "surface-level similarity" (Section 4.2), which conflicts with the "precise quantification" claim. The overlap results in Figure 7 show surface-form token reuse, consistent with multiple explanations (lexical priming, canonical physics language, actual reconstruction). This is a major gap because Contribution 3 is one of the paper's three claimed contributions and the faithfulness framing is central to the narrative. The core deletion/cramming findings (Contributions 1 and 2) are not undermined, but the paper oversells what the overlap metrics can deliver.

2. **The deletion intervention implementation is underspecified.**  
   The paper states it "intercepts CoT mid-generation" and "removes tokens before decoding" (Abstract, Sections 1, 3.2) but never explains the technical mechanism. In standard autoregressive LLMs, deleting tokens from the middle of an already-generated prefix invalidates the KV cache, and it is unclear how generation continues from the modified point. Different implementation choices (re-running the forward pass with truncated input vs. true mid-generation state manipulation) would test different phenomena and lead to different interpretations. Without this detail—which affects every experimental result—reproducibility is compromised.

### Minor

1. **LLM-as-judge evaluation is not calibrated against ground-truth answers.**  
   Physics problems have definitive correct answers (numerical or symbolic), but the paper uses Claude-4 Sonnet as a judge on a 0–1 scale (Section 2.4) without reporting agreement with ground-truth correctness. No inter-rater reliability, confidence intervals, or comparison against direct answer extraction are provided. While the main trends (accuracy decline under deletion) are likely robust, the absence of calibration introduces uncertainty.

2. **Dataset descriptions are sparse.**  
   Beyond PhysReason (1,200 problems), the paper does not report the number of questions used from UG-Physics and PhyBench, the answer format (multiple choice, free-form, numerical), or sample question types. This makes it hard to assess evaluation adequacy.

3. **Calibration study is limited in scope.**  
   The convergence analysis (Section 3.1) uses 5 re-runs on 50 UG-Physics questions but does not verify whether this calibration holds for harder benchmarks (PhyBench, PhysReason) or for the deletion conditions specifically. Five samples per condition is modest for a study whose central claims are about trends across deletion levels.

4. **Physics-aware annotation is not validated.**  
   The paper uses Claude-4 Sonnet to identify physics-related tokens for deletion (Section 3.2) but reports no validation, agreement rates, or quality checks. Additionally, comparisons across deletion strategies at the same k% may be misleading if physics-structured elements constitute a smaller fraction of tokens with higher information density.

5. **Alternative explanations for cramming are not explored.**  
   Section 4.1 interprets increased answer length under deletion as "cramming" or reconstruction, but does not consider generic hedging behavior (longer answers with more disclaimers, repetition, or restarts) that would also inflate length. Without content analysis of whether the elongated answers actually recover the correct deleted content, the "cramming" label implies directed reconstruction that is not fully demonstrated.

### Trivial
None.

## Nice-to-Haves

- A no-modification control where semantically empty tokens (e.g., filler text) are deleted at the same rates would help disambiguate whether effects are specific to removing reasoning content or are generic responses to any input perturbation.
- The overlap analysis could be strengthened with equation-level semantic matching (e.g., symbolic comparison of LaTeX expressions) or targeted n-gram overlap on equation tokens, which would directly exploit the structured nature of physics that the paper emphasizes.

## Removed Points

The following points from the critic input were removed per the filtering rules:
- **Magistral/Magistrall typo and related-work gaps**: Per hard rules, typos and missing related-work citations are removed.
- **Criticism about missing appendix content**: Per hard rules, the appendix was stripped by the parser and cannot be assumed missing.
- **Claim about missing engagement with prompt perturbation literature**: Per hard rules, missing related works are not mentioned as a weakness.
- **Speculative "fatal" framing of the metric issue**: The critic framed the metric mismatch as "structural" and fatal, but the paper's core contributions (deletion curves, cramming) survive even if the faithfulness analysis is reframed. Downgraded to Major.

## Novel Insights

The critic's most valuable insight is the mismatch between Contribution 3's "rigorous faithfulness analysis" promise and the bag-of-words metrics used. This is a genuine gap that the paper could address by either (a) recalibrating the contribution claims to match what the metrics actually measure, or (b) replacing/supplementing the metrics with semantically aware ones that exploit physics structure. The implementation underspecification concern is also insightful: without knowing whether the intervention is re-prompting or true mid-generation interception, the interpretation of results is ambiguous. These two insights together suggest the paper's core novelty (the deletion paradigm and cramming observation) survives, but the faithfulness analysis overreaches and needs restructuring.

## Suggestions

1. Recalibrate or remove the "rigorous faithfulness analysis" claim (Contribution 3) to match the actual surface-form overlap measurements, or replace the bag-of-words metrics with semantically aware alternatives that exploit physics structure (equation matching, numerical value comparison).
2. Clarify the deletion intervention implementation—specifically how KV cache state is handled and whether the approach is re-prompting or true mid-generation interception.
3. Calibrate the LLM judge against ground-truth answer extraction on a held-out subset, or where possible replace it with direct final-answer comparison (physics problems have definitive answers).
4. Validate the physics-aware annotations (e.g., against human judgments) and report inter-annotator agreement.
5. Report dataset sizes, answer formats, and total experimental runs across all conditions.

## Score and Decision

**Calibration anchors considered:**

| Paper | Avg Score | Decision | Round | Comparison to this paper |
|-------|-----------|----------|-------|--------------------------|
| "On the Hardness of Faithful CoT" | 5.00 | Reject | R1 | Directly about CoT faithfulness; tested existing methods with limited success. Similar score range. Our paper has more methodological novelty but clearer evaluation issues. |
| "To CoT or not to CoT?" | 6.67 | Accept | R1 | Large-scale meta-analysis + 20 datasets × 14 models. More comprehensive and rigorous than our paper. |
| "Is Factuality Enhancement a Free Lunch" | 6.67 | Accept | R1 | Well-executed study with systematic analysis. Stronger evaluation rigor. |
| "Mind Your Step (by Step)" | 5.00 | Reject | R2 | Interesting idea with framing/control concerns. Comparable quality and score to our paper. |
| "FLARE: Faithful Logic-Aided Reasoning" | 5.75 | Reject | R2 | Neuro-symbolic approach. Mixed scores (3,6,6,8). |
| "BALCONI" | 5.25 | Reject | R1 | Context-faithfulness benchmark. Similar score range. |
| "Distributional Reasoning in LLMs" | 5.00 | Reject | R2 | Interpretability analysis of reasoning. Comparable quality. |

**Round 1 bracket**: 4.0–6.0 (above the 3-4 reject range due to genuine novelty, but below the 6-7 accept range due to overclaimed faithfulness analysis and evaluation gaps).

**Reasoning for final score**: The paper has a genuinely novel core idea (deletion-based probing) and a non-trivial empirical finding (cramming) that together represent a real contribution. However, Contribution 3 is overclaimed given the bag-of-words metrics, the deletion implementation is underspecified, and the evaluation lacks calibration against ground-truth answers. These are fixable issues—with substantial revisions the paper could be a solid contribution—but in its current form the evidence does not fully support the scope of the claims. The score of 5.0 reflects a borderline paper where the core idea is promising but the execution has gaps that prevent acceptance at a top venue.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>