Now let me compile the final review.

**Final calibration assessment**: The calibration search tool encountered a persistent file error, so I proceed without retrieval-based anchoring. Based on direct reading of the paper and the review inputs, I calibrate against my knowledge of ICLR scoring standards.

---

## Summary

EmoSign introduces the first ASL video dataset annotated for sentiment and emotion by Deaf native signers. The dataset contains 200 clips (~16 min, 4 signers) with 7-point sentiment ratings, intensity-labeled presence of 10 emotion categories, and—most distinctively—open-ended qualitative descriptions of emotion cues from the annotators' perspective. The paper benchmarks four multimodal LLMs (GPT-4o, AffectGPT, Qwen2.5-VL, MiniGPT4) across caption-only, video-only, and video+caption conditions on sentiment analysis and emotion classification.

## Strengths

1. **First ASL dataset annotated by Deaf native signers who can distinguish grammatical from affective facial expressions.** This is a clear methodological improvement over prior work (e.g., FePh used hearing annotators). The inter-annotator agreement (Krippendorff's alpha = 0.593 average) is reasonable for the challenging task and is contextualized against spoken-language emotion benchmarks. (Table 2, Section 3.3)

2. **Open-ended qualitative emotion cue descriptions from native signers.** The paper documents non-manual markers (furrowed brows, pursed lips, head thrusts, mouth shapes), sign modifications (size, speed, repetition, fingerspelling), and the importance of discourse context (Section 3.4). This descriptive layer is unique among sign language datasets and provides a concrete foundation for future work on visual emotion understanding.

3. **Three-condition ablation design (caption-only, video-only, video+caption) cleanly diagnoses modality reliance.** The controlled experimental setup across all benchmark tasks isolates the contribution of each modality. The results confirm that models perform at near-chance levels in the video-only condition (e.g., GPT-4o wAcc = 11.50% on emotion classification, Table 4) while captions dominate, providing empirical evidence for the gap the dataset is designed to address.

## Weaknesses

### Fatal
None.

### Major

1. **VADER-based selection creates a confound between text sentiment and visual emotion.** The dataset selected the 100 most positive and 100 most negative utterances based on VADER sentiment analysis of the English captions (Section 3.1). This systematically biases the dataset toward clips where the English translation already carries strong emotional valence. The paper's central empirical finding—that models rely on text captions—is partially confounded by this construction choice: the dataset was curated so that text and strong sentiment correlate. The Limitations section (Section 6) mentions this briefly but does not quantify the divergence between VADER-based selection and annotator-judged emotion, nor does it report analyses on the subset where text and visual emotion disagree. This weakens the benchmark conclusions.

2. **Dataset scale (200 utterances, ~16 min, 4 signers) constrains the reliability of benchmark conclusions.** Several emotion categories have very few examples (surprise_negative: 25, anger: 25, disgust: 30, fear: 30 out of 200 clips). Per-class accuracy estimates from Table 4 are consequently unreliable—many categories show 0% accuracy across all models even with captions. The paper frames itself as "the first comprehensive dataset" (Abstract, Section 1), which overstates what 200 samples from 4 signers can support. The data is better positioned as a pilot/proof-of-concept.

3. **Inter-annotator agreement is unacceptably low for several emotion categories, undermining ground-truth reliability.** Krippendorff's alpha for surprise_negative (0.119), disgust (0.166), frustration (0.330), sadness (0.333), and fear (0.351) (Table 2) are well below conventional thresholds (alpha < 0.667 is considered low). These low-agreement categories are precisely the ones where models perform at or near chance in Table 4 (e.g., surprise_negative: most models score 0% in video conditions). This makes it impossible to distinguish genuine model failure from label noise. The paper does not report analyses on a filtered high-agreement subset.

### Minor

4. **Emotion cue grounding analysis is qualitative, not a benchmark task.** Section 5.3 describes manual inspection of "several randomly selected videos" with cherry-picked examples in Figure 3. There is no quantitative metric, no systematic comparison of grounding accuracy across models, and no defined evaluation protocol. Presenting this as one of "three tasks of increasing complexity" (Section 4.1) overstates its rigor.

5. **Different prompting strategies across models make cross-model comparisons noisy.** GPT-4o received a single prompt for all three tasks, while AffectGPT, Qwen2.5, and MiniGPT4 were given separate prompts per task (Section 4.2). Performance differences could partly reflect prompt engineering rather than model capability.

6. **No train/validation/test split is provided.** The dataset is currently only usable for zero-shot evaluation, limiting its utility for fine-tuning or model development that would be needed to advance the area.

7. **Comparison of Krippendorff's alpha to Fleiss' kappa from MELD/IEMOCAP (Section 3.3) is approximate at best.** Krippendorff's alpha is typically more conservative than Fleiss' kappa, so the favorable numerical comparison (0.593 vs 0.43/0.48) is potentially misleading without caveats about metric differences.

### Trivial
None.

## Nice-to-Haves
- Include at least one sign-language-aware baseline (e.g., LLaVA-SLT, cited in Related Work)
- Report bootstrapped confidence intervals for benchmark results
- Provide a standard data split for future fine-tuning
- Analyze signer-specific expression patterns (4 signers would permit this)
- Report benchmark results on the subset of high-agreement emotion categories

## Removed Points

These points were considered but removed during filtering. They should be treated with caution:

1. **Harsh Critic's claim that VADER selection is a "structural fatal flaw"** — Overstated. The three-condition ablation partially controls for this, and the paper acknowledges the issue in Limitations. The confound is real and significant but not fatal; it weakens rather than invalidates the results.

2. **Harsh Critic's description of the dataset as "200 ASL utterances whose English captions have strong sentiment"** — Reductive and disregards that Deaf annotators provided genuine emotion labels based on visual cues independent of captions. The annotator labels represent real judgments of emotional expression in signing.

3. **Harsh Critic's complaint about lack of statistical significance / confidence intervals** — Not standard practice for all benchmarking papers, especially at this scale and with a zero-shot evaluation design.

4. **Strength Finder's generic/superficial claimed strengths** (e.g., "addressed a critical gap", "important problem") — Dropped per filtering rules; only concrete, evidence-grounded strengths were retained.

## Novel Insights

One synthesis that emerges from combining the reviews is that the paper's most durable contribution is not the benchmark results (which are unsurprising given the dataset's construction and scale) but rather the annotation methodology and the qualitative descriptions of emotion cues. The paper could be significantly strengthened by leaning into this: presenting the qualitative descriptions as the primary contribution, framing the dataset explicitly as a pilot, and using the benchmark results as illustrative rather than definitive evidence of a gap.

## Suggestions

1. **Scale back the framing.** Replace "comprehensive dataset" with "pilot dataset" or "proof-of-concept." The contribution is real at the pilot scale; overclaiming invites justified skepticism.
2. **Quantify the VADER confound.** Report the agreement rate between VADER sentiment and annotator sentiment for the selected clips. Present a separate analysis on the subset where they disagree — this subset, though small, is the most informative test case.
3. **Report results on a high-agreement subset.** Filter to emotion categories with alpha > 0.4 (or collapse low-agreement categories) and show whether model failures persist.
4. **Reposition the emotion cue grounding section** as qualitative analysis / case studies, not a benchmark task.
5. **Provide a standard train/val/test split** so the dataset can be used for fine-tuning in future work.

## Score and Decision

Based on my assessment, this paper presents a genuine contribution (annotation methodology, qualitative descriptions) but the evidence base — 200 clips, 4 signers, VADER selection confound, unreliable labels for several categories — is too thin to support the "comprehensive dataset" and "new benchmark" claims made. The paper overclaims its contributions relative to what the data supports. At a venue like ICLR, this is a borderline-reject case that could become acceptable with substantially more data, reframing, and analysis of the confounds.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>