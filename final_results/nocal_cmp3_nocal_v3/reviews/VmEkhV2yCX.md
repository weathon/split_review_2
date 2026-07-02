## Summary

This paper systematically investigates *when* reasoning data should be introduced in LLM training (pretraining vs. SFT) and *what kind* of data (diverse vs. high-quality) is most beneficial at each stage. The authors pretrain an 8B hybrid Mamba2+attention model from scratch for 1 trillion tokens under four controlled conditions, then apply SFT and RL. The headline findings are: (1) front-loading reasoning data into pretraining creates durable advantages that SFT cannot recover, (2) the optimal data strategy is asymmetric (diversity in pretraining, quality in SFT), and (3) naive scaling of mixed-quality SFT data can be harmful. The large-scale systematic design and the "catch-up" experiment (Table 4) are notable contributions.

## Strengths

- **Timely and well-motivated research question.** The paper asks *when* (not just *which*) reasoning data should be introduced, and disentangles pretraining vs. SFT roles. This is genuinely underexplored in published work, and the framing around the catch-up hypothesis and asymmetric allocation is clear and structured (Section 1, lines 27–38).

- **Large-scale, systematic experimental design.** Pretraining an 8B model from scratch for 1T tokens with controlled data injection is a significant undertaking. The fully crossed setup (4 pretraining conditions × 3 SFT conditions = 12 models, plus RL runs) provides a more comprehensive view than prior work examining only one stage at a time (Sections 2.3, 4).

- **Robust catch-up experiment.** Table 4's finding that even 2× SFT epochs on the baseline cannot match the weakest reasoning-pretrained model is the paper's cleanest and most practically important result. It directly refutes the catch-up hypothesis with a controlled comparison.

- **Clean, actionable headline heuristic.** The asymmetric principle (diversity in pretraining, quality in SFT) is a memorable guideline practitioners can use, even if the precise percentages are less clean than claimed.

## Weaknesses

### Major

- **The central "diversity in pretraining" claim is confounded with repetition and unique sample count.** The paper compares $\mathcal{M}_{\text{LDQ}}$ (268M unique samples, diverse, mixed quality) against $\mathcal{M}_{\text{SHQ}}$ (1.2M unique samples, narrow, high quality) while controlling for total reasoning tokens at 80B (line 93). To reach 80B tokens from 1.2M samples, $\mathcal{D}_{\text{SHQ}}$ must be repeated far more than $\mathcal{D}_{\text{LDQ}}$. The performance gap attributed to "diversity" (e.g., line 99: "isolate the effect of data quality versus the quantity and diversity") is entangled with: (a) dataset size / number of unique examples, (b) repetition factor, (c) domain composition (56% math vs. 71% math), and (d) quality. The paper often uses "scale and diversity" jointly, but the abstract's claim of "11% average gain" from "broad diversity in reasoning patterns" overstates the precision of what the experimental design isolates.

- **The "quality dominates SFT" claim similarly confounds quality with dataset size.** Table 5 compares $\mathcal{M}_{\text{res}} + \text{SFT}_{\text{SHQ}}$ (44.99 avg) vs. $\mathcal{M}_{\text{res}} + \text{SFT}_{\text{LDQ}}$ (31.54 avg) as evidence that quality drives SFT. But $\mathcal{D}_{\text{SHQ}}$ (1.2M samples, high quality) and $\mathcal{D}_{\text{LDQ}}$ (268M samples, mixed quality) differ along quality *and* dataset size. The SFT recipe uses 4.8M samples (line 124); applied to $\mathcal{D}_{\text{SHQ}}$ this means ~4 epochs, while for $\mathcal{D}_{\text{LDQ}}$ it is a tiny fraction. Whether the performance difference is driven by quality, dataset size, repetition, or training dynamics is not disentangled.

- **The RL evidence supporting the headline "19% gain" is thin.** Only 2 out of 12 possible model pairs are taken through RL (Table 3): $\mathcal{M}_{\text{LMQ}} + \text{SFT}_{\text{SHQ}}$ vs. $\mathcal{M}_{\text{base}} + \text{SFT}_{\text{SHQ}}$. The paper calls this "conclusive evidence" (line 193), but with one data point at the RL stage, we do not know whether $\mathcal{M}_{\text{LDQ}} + \text{SFT}_{\text{SHQ}} + \text{RL}$ or $\mathcal{M}_{\text{SHQ}} + \text{SFT}_{\text{SHQ}} + \text{RL}$ would show similar patterns. The 19% figure is a single comparison, not a robust measurement.

- **No decontamination analysis.** The reasoning datasets ($\mathcal{D}_{\text{LDQ}}$ from Nemotron-Pretraining-SFT-v1, $\mathcal{D}_{\text{SHQ}}$ from Guha et al. 2025) are SFT-style datasets built from web-sourced problems. The evaluation benchmarks (GSM8K, MATH-500, MMLU, MMLU-Pro, GPQA-Diamond, LiveCodeBench) are all commonly included in SFT training mixtures. The paper reports no decontamination procedure. Given that some of the largest gains appear on exactly these benchmarks (e.g., +28.4% on math for $\mathcal{M}_{\text{LDQ}}$, Table 1), the possibility of benchmark contamination inflating results must be addressed.

### Minor

- **No variance or significance reporting.** All experiments are single runs without confidence intervals, standard deviations, or statistical tests. Key claims involve fine-grained differences (e.g., +4.25% latent effect, -4.92% from naive scaling). While single-run large-scale pretraining is common practice, the absence of any variance estimate should be explicitly acknowledged as a limitation.

- **The "naive scaling harms" finding is contextualized but the abstract's framing is slightly overbroad.** The paper's own text specifies that scaling *mixed-quality* data is harmful (line 253, Table 8 caption). The abstract's phrase "naively scaling SFT data can be detrimental" is an acceptable shorthand, but the paper would benefit from making the qualifier more prominent early on.

- **SFT data sample count is unclear.** Line 124 states "each 8B LLM is finetuned on 4.8M reasoning samples from $\mathcal{D}_{\text{res}}$." It is not specified whether this is the same 4.8M samples across all runs, or how they are drawn from datasets of vastly different sizes (1.2M to 269.2M). This matters for interpreting how different SFT conditions compare (e.g., how many epochs of $\mathcal{D}_{\text{SHQ}}$ vs. what fraction of $\mathcal{D}_{\text{LDQ}}$).

- **Percentage claims in the abstract imply more precision than the design supports.** The 19%, 11%, and 15% figures are presented as clean effect sizes but each reflects confounded comparisons (RL single-pair, pretraining diversity+scale confound, SFT quality+size confound). The abstract should caveat these as aggregate/directional rather than isolated measurements.

### Trivial

- None that carry weight in evaluation.

## Nice-to-Haves

- A control experiment where $\mathcal{D}_{\text{LDQ}}$ is subsampled to match the size of $\mathcal{D}_{\text{SHQ}}$ (1.2M samples) and repeated equally — if the subsampled $\mathcal{D}_{\text{LDQ}}$ still outperforms $\mathcal{D}_{\text{SHQ}}$, "diversity" (domain coverage) is truly the driver.
- At least two additional RL comparisons (e.g., $\mathcal{M}_{\text{LDQ}} + \text{SFT}_{\text{SHQ}} + \text{RL}$ and $\mathcal{M}_{\text{SHQ}} + \text{SFT}_{\text{SHQ}} + \text{RL}$) to test whether the 19% pattern holds across pretraining variants.
- Adding n-gram overlap decontamination between training datasets and evaluation benchmarks.
- A dedicated limitations section (currently absent), which would strengthen the paper's credibility given the strong prescriptive claims from a single experimental setup.

## Removed Points

These points from the input review were removed or demoted with justification:

- **"Formal optimization framing not operationalized"** — The paper uses Eq. 1–2 to frame the problem space, then empirically explores it through discrete comparisons. This is a presentational choice, not a substantive weakness.
- **"Related work downplaying"** — The paper's characterization of Cheng et al. (2024) as targeting "general-purpose reasoning tasks that require minimal reasoning" is an accurate description of the cited work's scope; the criticism is subjective and removed.
- **"First systematic study claim undermined by cited works"** — The cited works (Wang et al., Ai et al., Gandhi et al.) study mid-training on narrow datasets, not full pretraining with controlled data variations across scale, diversity, and quality. The paper's novelty claim is defensible.
- **"Excessive percentage claims"** — Partially retained as a Minor weakness above, but in a tempered form. The original section-by-section note has been merged into the minor points.

## Novel Insights

None beyond the paper's own contributions. The review surfaces the key insight that the confounds between diversity/scale (in pretraining) and quality/size (in SFT) weaken the precision of the paper's headline percentages, but does not introduce a novel re-interpretation beyond identifying these confounds and suggesting control experiments.

## Suggestions

1. **Run a repetition-controlled pretraining experiment.** Sub-sample $\mathcal{D}_{\text{LDQ}}$ to 1.2M samples and repeat it to match $\mathcal{D}_{\text{SHQ}}$'s repetition factor. This would cleanly isolate diversity/domain-coverage from pure sample count.
2. **Expand RL coverage to at least 2 more model pairs** ($\mathcal{M}_{\text{LDQ}}$ and $\mathcal{M}_{\text{SHQ}}$ backbones with $\text{SFT}_{\text{SHQ}}$) to test whether the RL-stage advantage generalizes.
3. **Add decontamination analysis** by checking n-gram overlap between training datasets and evaluation benchmarks; report results with and without detected overlaps removed.
4. **Clarify the SFT data sampling procedure** — how 4.8M samples are drawn from each dataset, and whether training epochs differ across conditions.
5. **Temper the abstract's precise percentage claims** with caveats (e.g., "aggregate," "directional," "reflecting combined effects") and add a limitations paragraph to the paper.
6. **Acknowledge the confounds explicitly** — the paper currently lacks any limitations discussion. An honest section addressing the repetition/scale confound, the single-pair RL evidence, and the absence of decontamination would significantly strengthen the paper.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Reject</decision>