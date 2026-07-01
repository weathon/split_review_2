## Summary

This paper articulates a "tokenization dilemma" faced by Scientific LLMs when processing biomolecular sequences — either sequences are tokenized too granularly (destroying functional motifs) or treated as a separate modality (creating alignment challenges). The authors propose a "context-driven" paradigm that bypasses raw sequences entirely by providing LLMs with structured textual annotations from bioinformatics tools (BLASTp, InterProScan). Through systematic experiments across 7 models and 3 input configurations, they find that context-only dramatically outperforms sequence-only, and that for specialized Sci-LLMs, adding raw sequence to context slightly degrades performance. While the paper identifies an important research question and produces extensive comparative data, its central claims are significantly overstated, and the experimental design conflates pipeline-level information retrieval with LLM reasoning capability.

## Strengths

- **Clear articulation of the tokenization dilemma.** Sections 1 and 3 present the two horns of the dilemma formally (Eqs. 2–4 and Eqs. 5–6), providing a clean theoretical framework that lets readers understand exactly what is being compared. This framing is a genuinely useful conceptual contribution for the community.

- **Broad and systematic model coverage in the main experiment.** Table 1 evaluates 7 models (3 specialized Sci-LLMs + 4 general-purpose LLMs) across 3 distinct input configurations (sequence-only, context-only, sequence+context) on 3 task types. This provides a substantial body of comparative data.

- **Multiple independent analyses supporting the main comparison.** Beyond the core QA benchmark, the paper includes embedding-space analysis (Section 5.2), layer-wise representational analysis (Section 5.3), temporal robustness analysis (Section 5.4), cost analysis (Section 5.5), and wet-lab validation (Section 5.6). This breadth of analysis, even if individual pieces have issues, demonstrates thoroughness.

## Weaknesses

### Major

1. **Core comparison conflates pipeline-level design with LLM reasoning claims, and the claims in the abstract overreach what the experiment supports.** The context-driven pipeline provides the LLM with GO terms and domain annotations retrieved from close homologs via BLASTp (lines 103, 119–123). For questions about molecular function, metabolic pathway, and subcellular localization, this context effectively contains answer-relevant information. The paper acknowledges this concern (lines 136–142) and correctly notes it uses *homolog* annotations rather than the query's own record as a guard against label leakage. However, the paper's headline claim — "the primary strength of existing Sci-LLMs lies not in their nascent ability to interpret biomolecular syntax from scratch, but in their profound capacity for reasoning over structured, human-readable knowledge" (abstract, line 9) — frames this as a discovery about LLM *capabilities*, when what is actually compared are two different *pipelines* with asymmetrical information access. One pipeline has access to database annotations; the other does not. The finding that providing answer-relevant information improves answer accuracy is not a surprising discovery about LLM reasoning, and the paper should more honestly characterize the comparison as between two end-to-end systems (tool-assisted retrieval + LLM vs. sequence-only LLM) rather than as a probe of LLM reasoning capacity.

2. **The claim that raw sequences "consistently" degrade performance is contradicted by the paper's own data.** The abstract (line 9) and Section 5.1 (line 178) state that sequences "consistently act as informational noise" and that the context+sequence setting "consistently" degrades performance. Table 1 shows the following patterns:

   - **Specialized Sci-LLMs** (3 models): All show modest degradation (Intern-S1: −2.12, Evolla: −3.49, NatureLM: −0.64).
   - **General-purpose LLMs** (4 models): 3 of 4 show *improvement* when sequence is added (Deepseek-v3: +1.04, GPT-5: +0.69, Qwen3: +0.91; Gemini2.5 Pro: −0.21).

   The claim of *consistent* degradation is false — it is a mixed pattern that appears to be model-class-specific and small in magnitude. This overclaiming weakens the paper's central narrative and should be corrected.

### Minor

3. **Internal contradiction between main text and figure caption in the wet-lab validation.** The main text (line 252) states that Evolla "attains a reasonable 80.0% accuracy on Rhodopsin" and "fails catastrophically on PETase." However, the Figure 6 caption (lines 262–264) reports Rhodopsin at 5.00% accuracy (1 correct, 19 incorrect) and PETase at 83.78% accuracy (31 correct, 6 incorrect). These are contradictory — the text describes good performance on Rhodopsin and catastrophic failure on PETase, while the caption shows the opposite. This is likely a labeling error (the text description may have swapped the two families), but as presented it undermines trust in the experimental reporting.

4. **ARI analysis (Section 5.2) compares fundamentally different quantities across paradigms and is uninformative.** For the sequence-based models, the paper extracts the models' *own output embeddings* and clusters them. For the context-driven approach, it generates embeddings from the *context text itself* using a separate text embedding model (Qwen-embedding, line 188). The context text already contains functional descriptions (GO terms, domain annotations) that are directly correlated with the MMseqs2 homology-based ground-truth clusters. It is nearly tautological that text descriptions of protein function cluster near-perfectly against functional ground truth (ARI of 0.958 in Figure 2d). This procedure tests whether text embeddings capture function (they trivially do) rather than providing a meaningful comparison between paradigms.

5. **The LLM-Score metric is used without validation against human judgment.** The paper leverages "a general-purpose LLM as an expert judge" (line 148) but provides no analysis of how well this automated metric correlates with human expert judgment, no inter-rater reliability, and no discussion of potential systematic biases. Given that the context-driven approach produces outputs that read like database annotations (which an LLM judge may recognize as "correct"-sounding), this could systematically favor the context-driven paradigm.

6. **No statistical characterization of results.** All results in Table 1 are reported as single point estimates with no confidence intervals, standard deviations, or significance tests. Given that several differences are very small (e.g., Gemini2.5 Pro: Context-Only 87.19 vs. Seq+Context 86.98, a 0.21-point gap), readers cannot assess which differences are reliable. This is especially important because the "sequence degrades" claim rests partly on small-magnitude differences.

7. **The prompt format for the Seq+Context condition is not described.** The paper provides the prompt template for the context-only condition (lines 107–134) but does not describe how the combined sequence+context input was structured for the Seq+Context condition. The degradation observed for specialized Sci-LLMs in this condition could be an artifact of suboptimal prompt engineering (e.g., naive concatenation) rather than an inherent property of sequences. Without this description, the finding is difficult to interpret.

### Trivial

- None that are paper-quality-relevant beyond the above.

## Nice-to-Haves

- **Test on questions whose answers are not directly retrievable from homolog annotations.** To strengthen the claim that LLMs are "reasoning" over context rather than extracting answers, the paper could evaluate on tasks such as mutational effect prediction, structural stability consequences, or binding specificity — questions that cannot be answered by reading GO terms from homologous sequences.

- **Ablate or analyze the case where BLASTp/InterProScan find no close homologs or domains.** The paper mentions ProTrek as a fallback (line 103) but does not separately evaluate how the context-driven approach performs when it must rely on this fallback. This is precisely the regime where the approach's limitations would be most informative.

- **Control for information content asymmetry.** The context provided to the LLM is far more information-dense than the raw sequence. A fairer comparison could involve giving the sequence-only condition additional guidance (e.g., few-shot examples with worked reasoning) to isolate whether the advantage comes from the *format* of the information or its *presence*.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *"The counter-intuitive 'sequence degrades' finding is worth investigating" (Strength 3 from harsh critic).* This strength is in tension with a verified weakness (the claim is not supported by the full data). While the finding is potentially interesting for a subset of models, the general claim is overstated and the strength as framed overstates the paper's reliability.

- *Criticism about missing appendix (Appendix N) being unavailable.* Removed per rule: the parser strips appendices; they exist in the original submission.

- *Claim that the context-driven paradigm is "not a new paradigm" / similar to RAG.* The paper cites tool-augmented approaches (GeneAgent, ChemCrew) in Section 2.3 and positions its contribution as a systematic comparison of input paradigms, not a claim of radical novelty in the tool-augmented approach itself. The framing is fair and this criticism misreads the paper's stated contribution.

## Novel Insights

The most interesting observation to emerge from the reviews — and one the paper itself notices but does not make central — is the *divergence between specialized Sci-LLMs and general-purpose LLMs* in how they handle the sequence+context condition. Specialized models show a small degradation when sequence is added to context, while most general-purpose models show a small improvement. This asymmetry is worth investigating as a phenomenon in its own right: it may reveal that specialized tokenization schemes (e.g., per-residue vocabularies) create interference patterns when combined with structured text, while general-purpose tokenizers treat the raw sequence as a benign additional string. The paper's current framing ("sequences are universally noise") obscures this potentially more interesting finding.

## Suggestions

1. **Revise the abstract and Section 5.1 claims** to accurately reflect the actual data: the sequence+context condition shows a mixed pattern (modest degradation for specialized Sci-LLMs, slight improvement for most general LLMs), not consistent degradation.
2. **Fix the contradiction** between the main text and Figure 6 caption in the wet-lab validation (Section 5.6).
3. **Reframe the paper's contribution** as a systematic comparison of input paradigms for biomolecular QA, rather than as a discovery about LLM reasoning capabilities. Acknowledge more explicitly that the context-driven pipeline incorporates external knowledge retrieval, which is an apples-to-oranges comparison with end-to-end sequence models.
4. **Clarify the ARI analysis** (Section 5.2) or remove the comparison — embedding the context text and clustering against functional ground truth is tautological and does not inform the paradigm comparison.
5. **Report variance** or at minimum note the lack of statistical precision in Table 1, especially for comparisons with sub-1-point differences.
6. **Describe the Seq+Context prompt format** so readers can assess whether the degradation for specialized models is a genuine phenomenon or a prompt-engineering artifact.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>