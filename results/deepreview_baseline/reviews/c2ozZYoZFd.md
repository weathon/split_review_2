##Summary

This paper presents a detailed case study re-examining a high-visibility ICLR 2025 Oral paper on `min-p` sampling. Through re-analysis of the original paper’s four lines of evidence—human evaluations, NLP benchmarks, LLM-as-a-Judge evaluations, and community adoption claims—the authors demonstrate that the original conclusions are unsupported by its own data. From this case study, the paper derives a blueprint for more rigorous empirical ML research, including a novel Best-of-N methodology for fairly comparing methods that require hyperparameter tuning.

## Strengths

- **Timely and important topic**: The paper directly addresses the growing crisis of rigor in empirical ML research, providing concrete evidence of common methodological flaws through a high-profile case study. This is a valuable contribution to the community’s self-correction efforts.
- **Thorough and convincing re-analysis**: The authors meticulously re-examine each line of evidence from the original paper, uncovering omitted data (1/3 of human evaluation scores), incorrect statistical testing (pooling across conditions, no multiple comparison correction), selective reporting (higher score for `min-p`, lower for `top-p` in LLM-as-a-Judge), and unsubstantiated claims (retracted community adoption numbers). The evidence is well-documented and reproducible.
- **Novel methodological contribution**: The Best-of-N analysis for controlling hyperparameter tuning volume (Section 3.1) is a practical, generalizable tool for fair comparison of methods with different hyperparameter spaces. This addresses a subtle but pervasive source of bias in empirical comparisons.
- **Clear and actionable blueprint**: The six general lessons (control for hyperparameter volume, rigorous statistical testing, data transparency, scrutinize qualitative summaries, methodological clarity, watch for selective reporting) are concrete, well-motivated by the case study, and directly applicable to future research and reviewing.
- **Well-structured and transparent**: The paper clearly separates its own claims from the original paper’s claims, provides visualizations with uncertainty estimates, and openly discusses limitations. The authors also engaged with the original authors and publicly shared their annotations and code.

## Weaknesses

### Fatal
None.

### Major
- **Single case study limits generalizability**: The blueprint is derived entirely from one paper. While the errors are common, the paper does not systematically demonstrate that these lessons generalize across a broader set of ML papers. The authors acknowledge this limitation, but it weakens the claim of a general “blueprint” somewhat.
- **The Best-of-N methodology, while novel, has assumptions**: It assumes hyperparameters are independent and that the maximum over a random subset is a fair measure. In practice, hyperparameters are often correlated, and the optimal hyperparameter may depend on the method’s sensitivity. The paper does not discuss these limitations or validate the approach on synthetic or known cases.

### Minor
- **The paper is primarily a critique**: While the blueprint is a positive contribution, the majority of the paper is devoted to deconstructing the original work. Some readers may view this as a rebuttal rather than a standalone contribution. The paper would be stronger if it also applied its blueprint to a new, constructive experiment (e.g., designing a rigorous evaluation of `min-p` from scratch).
- **The LLM-as-a-Judge analysis (Section 4) is less rigorous than other sections**: The authors point out under-specification and selective reporting, but they do not re-run the experiments with proper controls. The evidence is circumstantial (e.g., the Telegram link showing two scores). This is understandable given the lack of full details, but it makes this part of the case study weaker than the human evaluation and benchmark analyses.

### Trivial
- The paper occasionally uses informal language (e.g., “publicly told us to focus on the high diversity setting”) that could be more precise.

## Nice-to-Haves

- Apply the Best-of-N methodology to a broader set of ML papers to demonstrate its general utility and validate its assumptions.
- Include a positive example: design and execute a rigorous evaluation of `min-p` following the blueprint, to show what proper science looks like.
- Provide a checklist or template for reviewers based on the six lessons.

## Novel Insights

Beyond the paper’s own contributions, the key insight is that even in a high-profile, highly-scored ICLR Oral paper, multiple fundamental methodological errors can coexist and collectively invalidate the central claims. The paper demonstrates that these errors are not random but follow a pattern: selective reporting, unequal hyperparameter tuning, incorrect statistical inference, and unverifiable claims. This suggests that the current review process may systematically fail to catch such issues, and that the field needs structural changes (e.g., mandatory data/code release, pre-registration of evaluations) rather than just exhortations to be more careful. The Best-of-N analysis is a concrete step toward fair comparison, but the paper implicitly raises the question of whether the incentive structure in ML conferences encourages cherry-picking and overclaiming.

## Suggestions

- Strengthen the generalizability claim by briefly surveying how often the identified errors appear in a random sample of recent ICLR/NeurIPS papers (even a small sample would help).
- Discuss the limitations of the Best-of-N approach more explicitly, and suggest alternative or complementary methods for controlling hyperparameter tuning.
- Consider framing the paper as a “reproducibility study + methodology” rather than a “blueprint,” to better match the content.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>