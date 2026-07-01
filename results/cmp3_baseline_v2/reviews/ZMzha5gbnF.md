## Summary
This paper identifies a novel vulnerability in Masked Diffusion Language Models (MDLMs) called the "priming vulnerability," where an affirmative token appearing at an intermediate denoising step can steer the model toward generating harmful responses even in safety-aligned models. The authors demonstrate this vulnerability under two threat models (intervention and non-intervention), propose First-Step GCG as an efficient attack that exploits this vulnerability, and introduce Recovery Alignment (RA), a safety alignment method that trains models to generate safe responses from contaminated intermediate states. Experiments across three MDLMs show RA significantly mitigates the vulnerability with minimal impact on general task performance.

## Strengths
- **Novel and timely research direction**: The paper addresses an underexplored area—safety vulnerabilities specific to the inference mechanism of diffusion language models. This is genuinely novel and important as DLMs gain traction.
- **Rigorous problem characterization**: The anchoring attack provides a clean, controlled way to isolate and measure the priming vulnerability, and the theoretical lower bound (Theorem 4.1) is a principled contribution that connects the vulnerability to practical attack design.
- **Strong empirical validation**: The paper evaluates RA across three different MDLMs (LLaDA, LLaDA 1.5, MMaDA), two benchmark datasets, and multiple attack methods (intervention-based and non-intervention-based). RA consistently outperforms all baselines (SFT, DPO, MOSA), often reducing ASR by 80-90% for early intervention steps.
- **Practical countermeasure with minimal utility cost**: RA is scalable (uses existing datasets, pretrained reward models, no additional data construction), and Table 4 shows that the substantial safety improvements come with essentially no degradation across 11 general capability benchmarks.

## Weaknesses
### Major
- **Limited theoretical grounding for RA**: The paper convincingly identifies the vulnerability and shows that RA mitigates it, but the theoretical justification for RA is informal (Equation 5-6). The paper would benefit from a more formal treatment of why conditioning on contaminated states during training leads to generalization, or from a theoretical guarantee that RA reduces the probability of harmful generation from contaminated states. This is not fatal—the method works empirically—but it weakens the paper's depth.

- **Performance degradation at late intervention steps**: While RA is highly effective for early intervention steps (t_inter ≤ 8), Table 2 shows that for t_inter = 32, RA still yields 43-79% ASR across models. The paper acknowledges this as a limitation ("practically impossible to generate a contextually safe response due to many anchors"), but this severely limits the scope of the claimed mitigation. For practical deployment, attackers could easily use late-step interventions.

- **Limited evaluation of practical exploitability of non-intervention attacks**: The First-Step GCG attack achieves 49-58% ASR on aligned models (Table 1), which is concerning but still far from universal. The paper claims the vulnerability is a "pressing issue" but doesn't demonstrate that real-world attackers can reliably exploit it without intervention (GCG requires hundreds of optimization steps and white-box access). The framing somewhat overstates the practical threat level compared to what the evidence shows.

### Minor
- **Single instantiation of RA**: The paper only tests an RLHF-style RA with GRPO. The limitations section mentions DPO-style alternatives but does not implement them. Providing even a preliminary comparison would strengthen the claim that RA is a general framework rather than a single algorithmic choice.

- **Scheduling ablation interpretation**: Figure 3b shows that linear scheduling and uniform scheduling achieve similar performance in many settings, yet the paper claims linear is clearly superior. The difference appears marginal in some subplots. The conclusion that linear scheduling is definitively better is not fully supported.

### Trivial
- None significant.

## Nice-to-Haves
- An analysis of what types of "affirmative tokens" are most influential (steering toward harm)—is it the first token? Specific semantic categories? This could inform more targeted defenses.
- A qualitative analysis of failure cases for RA at late intervention steps—do these failures correspond to queries that are inherently more harmful or more ambiguous?
- Evaluation of RA's effectiveness against adaptive attacks that are aware of the defense mechanism.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Provide a theoretical or formal analysis of RA's generalization properties: under what conditions does training on contaminated states guarantee reduced harmful generation probability at test time?
- Address the late-intervention failure case more thoroughly—either propose a complementary defense (e.g., detection of affirmative token injection before denoising) or acknowledge it as an inherent limitation that RA alone cannot overcome.
- Consider comparing RA against a simpler baseline: standard DPO/RLHF training with data augmentation that includes diverse contaminated states (not just fully masked starts). This would isolate the benefit of the intervention curriculum from the RL method itself.

## Score and Decision
The paper makes a genuinely novel contribution by identifying and characterizing a vulnerability specific to an emerging model class (MDLMs). The empirical work is thorough, the proposed method is practical and effective within its scope, and the paper is well-structured. However, the theoretical depth is limited, and the mitigation is incomplete for stronger attacks (late intervention). The contribution is meaningful and well-executed but not breakthrough-level; it fits solidly in the borderline accept to accept range.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept