Now let me compose the final authoritative review.

## Summary

This paper presents a systematic empirical study of when and what kind of reasoning data should be introduced during LLM training. Using an 8B hybrid model pretrained from scratch for 1T tokens, the authors vary the diversity, scale, and quality of reasoning data injected at pretraining vs. SFT stages, while controlling total token budget. The core finding is that front-loading reasoning data into pretraining creates durable advantages that SFT alone cannot replicate, with an asymmetric principle: diversity matters more in pretraining while quality matters more in SFT. The paper also claims that high-quality pretraining data has "latent effects" activated only after SFT.

## Strengths

- **Timely and well-motivated research question.** The paper asks whether introducing reasoning data during pretraining (rather than only at SFT) yields different outcomes, controlling for total token budget — a genuinely under-explored question given the field's near-exclusive focus on post-training for reasoning.

- **Budget-controlled experimental design** with a fixed 80B reasoning token budget across all pretraining variants and a fully crossed design (4 pretraining models × multiple SFT recipes), allowing attribution of differences to *what kind* of reasoning data rather than *how much*.

- **Computationally serious experiments:** pretraining an 8B hybrid model from scratch for 1T tokens with systematic ablations gives the findings practical weight.

- **Clean "catch-up" test (Table 4):** directly testing whether doubling SFT epochs on the baseline closes the gap — it does not — concretely refutes the "just do more SFT" hypothesis.

- **Actionable asymmetric principle** (diversity in pretraining, quality in SFT) that provides a clear, memorable heuristic for data allocation, even if the evidence for it is partially confounded.

## Weaknesses

### Fatal

None.

### Major

- **Diversity/scale confound in the central pretraining comparison.** The paper's claim that "pretraining benefits most from diversity" is based on comparing M_SHQ (1.2M high-quality, narrow-domain samples, 71% math) against M_LDQ (268M diverse, mixed-quality samples, 56% math/17% code/27% science). These differ along three simultaneously entangled axes: (a) unique sample count (1.2M vs 268M — M_SHQ's ~1.2M samples must be repeated ~33× to reach the 80B token budget while M_LDQ's 268M samples are hardly repeated), (b) domain diversity, and (c) per-sample quality. The paper acknowledges that small datasets are repeated (Section 2.3) but never discusses the confound this creates, nor disentangles whether M_LDQ's advantage comes from broader domain coverage, having 200× more unique examples (reducing overfitting to repeated instances), or its specific domain distribution (e.g., 27% science vs. 8%). This weakens the precision of the central asymmetric claim.

- **The "latent effect" finding has a plausible alternative explanation not ruled out by the paper.** M_LMQ (pretrained on D_LDQ + D_SHQ) shows +4.25% over M_LDQ (pretrained on D_LDQ only) after both are SFT'ed on D_SHQ. The paper attributes this to a deep "latent effect" where high-quality data unlocks potential during alignment. However, M_LMQ has already seen D_SHQ's exact examples during pretraining, so it receives additional training on those same examples during SFT — effectively more epochs on the same data. M_LDQ has never seen D_SHQ's data before SFT. The observed advantage could simply reflect more total exposure to the same training examples rather than an emergent synergistic property.

### Minor

- **Headline percentage claims (19%, 11%, 15%) are imprecise in scope.** The 19% comes from the single largest gap in the paper (M_base+SFT_SHQ+RL vs M_LMQ+SFT_SHQ+RL, ~18.74pp), not an average across conditions. The 11% compares M_base (no reasoning data) against M_LDQ, conflating "any reasoning data" with "diverse reasoning data." The 15% for SFT quality cannot be cleanly mapped to a single comparison. The qualitative direction is correct, but the precise quantitative framing is loose.

- **The RL phase evaluates only two model conditions** (M_base+SFT_SHQ+RL vs M_LMQ+SFT_SHQ+RL). The paper's strongest claims about compounding gains through RL rest on a single pair comparison. Including at least one additional condition (e.g., M_LDQ+SFT_SHQ+RL) would substantially strengthen the RL-phase conclusions.

- **No error bars, confidence intervals, or variance estimates** are reported for any benchmark results. Given that 16/4 evaluation runs are conducted per benchmark, bootstrap estimates could be provided, or the absence should be acknowledged as a limitation.

- **The SFT scaling ablation (Table 8) uses M_LDQ as the base model SFT'ed on D_LDQ** — the same distribution the model was pretrained on. The poor results from "naive scaling" could partly reflect data overlap or overfitting rather than a general property of scaling SFT data.

### Trivial

None.

## Nice-to-Haves

- A control experiment isolating diversity from scale: subsample D_LDQ to match D_SHQ's 1.2M sample count while preserving domain diversity, then compare M_SHQ vs this subsampled model.
- A control experiment for the latent effect: pretrain a model on D_LDQ only, SFT on D_SHQ, and compare to M_LMQ+SFT_SHQ. If the +4.25% advantage persists, it supports the latent-effect story; if it disappears, the effect is just more epochs on the same data.
- Report bootstrap variance estimates from the 16/4 evaluation runs per benchmark.
- Extend RL evaluation to at least one more condition (e.g., M_LDQ+SFT_SHQ+RL).

## Removed Points

These points were flagged in the input review but are removed with justification:

- **"M_base framed as having no reasoning data" while D_base contains math/code text:** REMOVED — the paper clearly distinguishes raw text from QA-paired CoT reasoning data, a legitimate controlled comparison.
- **D_ALF being a noisy proxy for reasoning complexity:** REMOVED — the paper acknowledges this limitation ("longer responses often correspond to more complex CoT reasoning").
- **Terminology nitpick about "front-loading" vs. the staged schedule:** REMOVED — the paper uses "front-loading" to mean adding reasoning data during pretraining (earlier than SFT), not at the very first token.
- **Observation that Table 2 averages are low:** REMOVED — this merely describes results, not a weakness.
- **Generic demands for larger datasets or more models:** REMOVED as scope creep.

## Novel Insights

The most valuable insight from the review process is that the paper's diversity claim is confounded with dataset size/repetition in a way the paper does not discuss. When datasets differ on multiple axes (size, diversity, quality), attributing effects to one axis requires explicit controls or careful discussion. The repetition issue (1.2M samples repeated ~33× vs 268M samples essentially unrepeated) is a design artifact the paper mentions in passing but never analyzes. Similarly, the latent effect finding would benefit from ruling out the simple "more epochs on same data" explanation — a control experiment where the model does not see D_SHQ during pretraining would cleanly resolve this.

## Suggestions

1. Add a discussion section explicitly addressing the repetition confound between D_SHQ and D_LDQ in pretraining, including analysis of training vs. validation loss curves to check for overfitting from repeated narrow data.
2. Add a simple control experiment (or at minimum a discussion) disentangling the latent effect from simple data repetition — e.g., compare M_LDQ+SFT_SHQ vs M_LMQ+SFT_SHQ. If the gap appears only when D_SHQ is seen twice, the "latent effect" narrative needs revision.
3. Temper the precise percentage claims in the abstract and introduction to match the actual scope of the comparisons they are drawn from.
4. Add one more RL condition (at minimum M_LDQ+SFT_SHQ+RL) to broaden the evidence for the compounding-gains claim.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>