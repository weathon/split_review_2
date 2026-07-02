## Summary

This paper introduces a new task paradigm called "grounding-IQA" that integrates multimodal referring and grounding with image quality assessment. It defines two subtasks (GIQA-DES for grounded quality descriptions and GIQA-VQA for region-level visual question answering), constructs a dataset of 167K instruction-tuning samples (GIQA-160K) via an automated four-stage annotation pipeline using Llama3, Grounding DINO, and Q-Instruct, and proposes a benchmark (GIQA-Bench, 100 images, 250 test samples) to evaluate description quality, VQA accuracy, and grounding precision. Fine-tuning several MLLMs (LLaVA variants, mPLUG-Owl2) on GIQA-160K yields models that can produce quality descriptions with spatial grounding.

## Strengths

- **Novel task formulation with clear motivation.** The paper correctly identifies a genuine gap: existing MLLM-based IQA methods produce quality descriptions or scores but cannot localize quality-affecting regions. The proposed grounding-IQA paradigm (Sec. 3.1, Figs. 1–2) is a natural and practically useful extension that combines referring, grounding, and IQA.
- **Thoughtfully engineered annotation pipeline.** The four-stage pipeline (Llama3-based object tag extraction → Grounding DINO detection → IQA-Filter + Box-Merge refinement → coordinate discretization) addresses real engineering challenges. Using the description phrase $\mathcal{T}_r$ rather than the plain object name (Sec. 3.2, Stage-2, Fig. 4) and the IQA-Filter that prunes detections via Q-Instruct quality queries (Alg. 1) are clever design choices. Tab. 2a shows the refinement pipeline improves mIoU from 0.5624 to 0.5851 and Tag-Recall from 0.5045 to 0.5497.
- **Substantial data diversity and scale.** The dataset draws from multiple sources (KonIQ-10k, SPAQ, LIVE-FB, LIVE-itw, AGIQA-3K, ImageRewardDB, KADIS-700K), covering in-the-wild, AI-generated, and artificially degraded images. At 167K samples from 43K images, it is large enough to support supervised fine-tuning of 7B-parameter models.
- **Multi-aspect benchmark design.** GIQA-Bench evaluates three distinct dimensions (description quality via BLEU@4 + LLM-Score, VQA accuracy via Acc(Y)/Acc(W), grounding precision via mIoU + Tag-Recall), giving a fuller picture of model capabilities than a single metric would provide.

## Weaknesses

### Major

- **Main comparison (Table 5) conflates task definition with fine-tuning data advantage.** The paper compares models fine-tuned on GIQA-160K ("Ours") against models that were *not* fine-tuned on GIQA-160K (General, Ground, and IQA groups, with the partial exception of Q-Instruct models fine-tuned on different data). The result — fine-tuned models outperform non-fine-tuned models on a test set drawn from related distributions — is expected and does not isolate the value of the *grounding annotations* specifically. To support the claim that grounding information specifically drives improvement, the paper needs a controlled experiment that fine-tunes the same base model on an equal amount of source IQA data (Q-Pathway/DQ-495K descriptions) converted to the same format *without* coordinates. Without this control, the experiment primarily validates that GIQA-160K functions as a fine-tuning dataset, which is a real but weaker claim.

- **Q-Ground, the most directly related prior work, is absent from experiments.** The Related Work (Sec. 2.2) identifies Q-Ground (Chen et al., 2024b) as achieving "degradation region grounding" in IQA — the closest existing method to the paper's proposed paradigm. Yet Q-Ground does not appear in Table 5 or any experimental comparison. Including it (e.g., zero-shot or fine-tuned on GIQA-160K) would either strengthen the paper's claim that a unified referring+grounding approach is necessary or provide important contextual information about where the novelty lies. Its omission is a significant gap.

### Minor

- **No uncertainty quantification for a very small benchmark.** GIQA-Bench contains only 100 images (100 DES + 150 VQA samples). With only 90 Yes/No questions and 60 open-ended questions, a single question's outcome can shift accuracy by >1 percentage point. No confidence intervals, standard deviations, or statistical significance tests are reported for any result in Tables 2–5. The reported mIoU and accuracy differences across conditions may be variance-bound rather than reflecting true performance differences.

- **Discretization precision loss selectively reported.** Tab. 2b shows that discrete coordinate representation (Disc-Coord) reduces mIoU from 0.6046 (Norm-Coord) to 0.5851, yet the paper only highlights that Disc-Coord "enhances description quality" without acknowledging or discussing this precision loss. The 20×20 grid (each cell covering 5% of the image dimension) is a coarse spatial resolution for fine-grained IQA.

- **LLM-Score judge may share lineage with the annotation pipeline.** The LLM-Score evaluation metric uses Llama3 as a judge, while Llama3 is also used in the annotation pipeline (Stage-1 object tag extraction and GIQA-VQA generation). This raises potential circularity: the judge may systematically favor outputs that resemble the format it was used to produce. The narrow LLM-Score differences between Ours and Q-Instruct models in Table 5 (60–63 vs. up to 62.00) make it hard to argue that grounding-IQA fine-tuning produces substantially better *descriptions* specifically.

### Trivial

- **Grammatical error in the IQA-Filter prompt.** Line 135: the prompt reads "Is the image quality is $< \mathcal{T}_q >$" with a double "is," which could affect Q-Instruct's reliability.

## Nice-to-Haves

- Report the average number of boxes per DES sample and the distribution of box sizes in the dataset (Sec. 3.3).
- Disclose the 15 questions in the DES question pool (Sec. 3.2), as their diversity affects what the evaluation actually tests.
- Fine-tune one or two existing grounding models (e.g., Ferret-7B, GroundingGPT-7B) on GIQA-160K and compare — this would complement the current approach of fine-tuning general models.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"No code/dataset release link (Code: .)"** — Removed per parser-artifact rule; the URL is likely stripped by the PDF extraction process.
- **"No user study in main text"** — Removed per missing-appendix rule; the paper states the user study is in the supplementary material (line 343), which was stripped by the parser.
- **"BLEU@4 is a poor metric" standalone criticism** — Partially valid but the paper also uses LLM-Score as a complementary metric. The circularity concern is retained above as a minor weakness.
- **"grounding-GPT typo in Figure 1 caption"** — Removed as a formatting artifact from PDF extraction.
- **"IQG/IQA inconsistency"** — Removed as a trivial naming issue caused by incomplete find-and-replace; does not affect the scientific content.
- **Claim about missing analysis of annotation pipeline accuracy** — Removed because the paper provides Fig. 6 (box area distribution) and Tab. 2a (refinement improvements) as indirect validation, and a full human precision/recall audit is scope beyond what is standard for this type of automated pipeline paper.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Add the critical controlled experiment: fine-tune the same base model (e.g., mPLUG-Owl2-7B) on (a) GIQA-160K v.s. (b) an equal-sized subset of the source IQA descriptions formatted *without* coordinates. If (a) outperforms (b) on GIQA-Bench, this directly validates that grounding annotations specifically drive improvement.
- Include Q-Ground as a baseline in Table 5.
- Report results with variance over at least 3 random seeds, or at minimum acknowledge the small benchmark size as a limitation.

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>