## Summary

GUI-Spotlight proposes a *think-with-image* visual grounding model that uses iterative tool invocation (crop, extract, find_color) guided by reinforcement learning to progressively narrow focus on GUI elements. The key claims are: (1) strong accuracy on ScreenSpot-Pro (52.8%) and UI-Vision (23.4%) with only 18.5K training samples—far fewer than competing methods; (2) a stabilized variant of GSPO that prevents training collapse in multi-turn tool-use settings; (3) thorough documentation of negative results in algorithm and reward design choices.

## Strengths

- **Remarkable data efficiency.** GUI-Spotlight achieves 52.8% on ScreenSpot-Pro with 18.5K curated samples, outperforming V2P-7B (50.6%, 9.6M samples) and GTA-1-7B (50.1%, 1.56M samples). This demonstrates that high-quality data curation and iterative reasoning can reduce reliance on massive datasets.
- **Comprehensive empirical analysis.** The paper systematically ablates RL algorithms, reward components, and training strategies (Sections 4.1, 4.2), including failure cases (e.g., continuously updating the reference policy degrades accuracy, dense Answer rewards hurt convergence). This level of documented negative results provides actionable guidance for future work on tool-augmented grounding.
- **Clear and well-motivated pipeline.** The three-tool design (extract, find_color, crop) is intuitive for progressive zooming, and the offset-tracking registry elegantly handles coordinate transformations across multiple crops. The inference algorithm (Algorithm 1) is straightforward and reproducible.
- **Strong generalization across backbones.** Starting from Qwen2.5-VL-7B-Instruct (non-UI-specialized) yields an absolute +11.9 point gain on ScreenSpot-Pro, showing the RL+muli-tool approach is not tied to a single base model.

## Weaknesses

### Minor

- **Inconsistent stage numbering in Figure 2.** The figure labels stages 0–3, while the text describes Stages 1–3. The caption calls Stage 1 "SFT warm-up" but the x-axis suggests Stage 0 corresponds to the initial SFT checkpoint. This misalignment makes it harder to interpret the 39.3% → 17.8% drop after the first training phase. The authors should resolve the numbering to match the text description of three training stages.
- **Overclaimed "think-with-image" framing.** The core novelty is iterative tool invocation trained via RL, which is more "act-then-observe" than a fundamentally new reasoning paradigm. The biological attention analogy (Shu et al., 2022) is superficial and does not add technical insight. This framing does not detract from the empirical contribution but should be tempered.
- **Missing failure case analysis.** The paper reports high accuracy on three benchmarks but does not analyze typical failure modes (e.g., does the model take too many steps? Does find_color often fail? Are there GUI categories where accuracy remains low?). Such analysis would strengthen the practical guidance claimed in Contribution 3.

## Nice-to-Haves

- A study on the optimal maximum number of tool-use steps (*T_max* in Algorithm 1) and how accuracy varies with allowed steps.
- Sensitivity analysis on crop sizes for *find_color* (currently fixed at 200×200) and *extract* (always quarter crops) to justify these design choices.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Unify the stage numbering between the text (Stages 1–3) and Figure 2 (Stages 0–3) so that readers can directly map the accuracy curve to the described training phases.
- Add a paragraph categorizing typical failure cases (e.g., targets smaller than the *extract* quarter-crop, or color ambiguity for *find_color*) to help practitioners understand where the method may still struggle.

## Score and Decision

The paper presents a well-executed, data-efficient approach to GUI grounding with thorough ablation studies. The iterative tool-use with stabilized RL is a practical contribution, and the documented negative results are valuable. The minor clarity issues do not undermine the overall soundness. I recommend acceptance.

MY FINAL SCORE: <score>7</score>  
MY FINAL DECISION: <decision>Accept</decision>