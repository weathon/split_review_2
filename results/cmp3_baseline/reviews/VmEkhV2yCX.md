## Summary
This paper presents a systematic study investigating how reasoning data—varying in scale, diversity, and quality—affects LLM performance when introduced at different stages of training (pretraining vs. SFT). The authors pretrain 8B models from scratch under controlled conditions and find that front-loading reasoning data into pretraining creates a durable advantage (+19% average gain after RL), that pretraining benefits most from diversity while SFT benefits most from quality (asymmetric allocation principle), and that naive scaling of SFT data with mixed quality can be actively harmful. The work provides one of the first large-scale, controlled empirical investigations of this important data allocation question across the full training pipeline.

## Strengths
- **Important and timely research question**: The paper tackles a fundamental but under-explored issue in LLM development—how reasoning data should be allocated across pretraining and post-training phases. This is highly relevant given the increasing compute costs and proprietary nature of training recipes.
- **Large-scale, systematic experimental design**: The authors conduct the first controlled study that varies reasoning data characteristics (diversity, quality, scale) across both pretraining (from scratch for 1T tokens) and SFT, with 8B models. This level of thoroughness is rare and valuable given the prohibitive cost of such experiments.
- **Clear, actionable findings**: The asymmetric principle (diversity in pretraining, quality in SFT) and the demonstration that SFT cannot compensate for a weak pretraining foundation are concrete, practical insights that directly inform data allocation strategies.
- **Latent effect discovery**: The finding that high-quality pretraining data can have a "latent" benefit that only emerges after SFT (+4% gain) is a genuinely novel and non-obvious insight that challenges simple "more is better" thinking at each stage.
- **Multi-phase evaluation**: The paper evaluates models after pretraining, after SFT, and after RL, showing that the pretraining advantage compounds across stages rather than diminishing—a strong validation of the core thesis.

## Weaknesses
### Fatal
None identified.

### Major
- **Single architecture, single scale**: All experiments use one 8B hybrid Mamba2-Transformer architecture from a single source (NVIDIA). While the authors include a smaller 1.2B ablation (Table 14, mentioned briefly), the generalizability of the findings to other architectures (purely dense Transformers, MoE models), other model families (LLaMA, Qwen), and larger scales (70B+) remains unclear. The claim that this is a "principled guide" would be stronger with at least one cross-architecture validation.
- **Confounding between diversity and scale in pretraining comparison**: The comparison between $\mathcal{M}_{SHQ}$ (1.2M samples, narrow diversity) and $\mathcal{M}_{LDQ}$ (268M samples, broad diversity) confounds scale with diversity. The paper attributes the performance difference to "diversity," but it could equally be driven by sheer volume—even if the SHQ data were repeated to match token count, the number of unique reasoning patterns exposed is vastly different. Without an ablation that matches both token count *and* unique sample count while varying only diversity, this conclusion is overstated.
- **Limited exploration of the SFT "catch-up" counterfactual**: The catch-up experiment doubles SFT epochs on $\mathcal{M}_{base}$, but the paper does not explore scaling SFT *data* (rather than epochs) for the baseline, nor does it explore whether a *different* SFT recipe (higher learning rate, different curriculum) could close the gap. The claim that pretraining advantage "cannot be fully replicated" is supported by one specific counterfactual, which is a relatively narrow test.
- **The "naive scaling harms" claim is based on a specific noisy data condition**: The conclusion that naive SFT scaling is "harmful" (-5% math) comes from comparing $\mathcal{M}_{LDQ} + SFT_{LDQ}$ to $\mathcal{M}_{LDQ} + SFT_{2\times LDQ}$. But $\mathcal{D}_{LDQ}$ is described as "heterogeneous quality"—this shows that scaling *low-quality* data can hurt, which is already well-known in the SFT literature (Zhou et al., 2023). The paper's framing suggests a broader caution against scaling *per se*, but the evidence only addresses scaling with mixed/noisy data, not scaling with consistently high-quality data.

### Minor
- **Pretraining data mixture is not fully described**: The paper mentions the ratio (80/20) and token counts but does not specify how the reasoning data is mixed with the base corpus at the batch level (e.g., is it stratified, uniform, or proportional sampling?). This matters for reproducibility.
- **The "19% average gain" headline is from the RL phase (Table 3) but only compares two specific models** ($\mathcal{M}_{LMQ} + SFT_{SHQ} + RL$ vs. $\mathcal{M}_{base} + SFT_{SHQ} + RL$). The gain is large and impressive, but it would be helpful to see RL results for more of the intermediate conditions (e.g., $\mathcal{M}_{LDQ}$ + RL) to understand whether the gain is mostly from pretraining diversity or from the LMQ quality injection.
- **Instruction-following (IFEval) shows an inverted pattern**: In several tables (e.g., Table 7), the model with higher reasoning content (60/40 ratio) shows *lower* instruction-following accuracy. The paper acknowledges this as a "breadth-alignment trade-off" but does not deeply analyze why, leaving the practical recommendation ambiguous for practitioners who care about both reasoning and instruction following.

### Trivial
- The paper claims "the first systematic study" multiple times; this is slightly overstated as concurrent or very recent work (e.g., AI et al., 2025; Liang et al., 2025) has partially addressed related questions, though the paper fairly discusses these.

## Nice-to-Haves
- Include at least one experiment with a purely dense Transformer architecture to validate that the findings are not specific to the hybrid Mamba2 design.
- Provide a matched-scale comparison for diversity: e.g., subsample $\mathcal{D}_{LDQ}$ to the same unique sample count as $\mathcal{D}_{SHQ}$ (while still repeating to match token budget) to isolate diversity from scale.
- Show RL results for the full set of intermediate model conditions, not just the two extremes, to better understand where gains originate.

## Novel Insights
The paper's most novel insight is the **asymmetric allocation principle**: the data characteristics that matter most are phase-dependent, and the optimal strategy is not simply "use good data everywhere" but rather "use diverse data early, high-quality data late." A second genuinely novel observation is that **high-quality pretraining data can have a latent effect that is only "unlocked" after SFT**—this implies that evaluations conducted immediately after pretraining may significantly underestimate the value of certain data choices, which has important implications for how pretraining ablations are conducted and interpreted. Finally, the demonstration that the pretraining advantage **compounds through RL** (widening rather than shrinking) provides a strong empirical argument against the "catch-up" hypothesis that many practitioners might intuitively hold.

## Suggestions
- Clarify the confound between diversity and scale in the $\mathcal{M}_{SHQ}$ vs. $\mathcal{M}_{LDQ}$ comparison, and either add an ablation or soften the attribution to "diversity" alone.
- Add RL results for at least one intermediate condition (e.g., $\mathcal{M}_{LDQ} + SFT_{SHQ} + RL$) to show whether the large gains in Table 3 are driven mainly by pretraining diversity or by the specific LMQ quality blend.
- Discuss the instruction-following trade-off more concretely—under what conditions would a practitioner prioritize one over the other?

## Score and Decision
The paper addresses a genuinely important and under-studied question with a large-scale, systematic experimental design that is rare in the open literature. The findings are practically relevant and generally well-supported. The main limitations are the single architecture/scale and the confound between diversity and scale in a key comparison, which prevent the paper from being a definitive "principled guide" as claimed but still make it a strong and valuable contribution.

MY FINAL SCORE: 7.0</score>
MY FINAL DECISION: Accept</decision>