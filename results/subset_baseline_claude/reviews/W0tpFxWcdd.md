## Summary

HINTS (Human-INTuited cues for RL) is a framework that enables humans to serve as "coaches" for RL agents by specifying conceptual hints (e.g., angular velocity, road curvature), which are grounded into numerical cues by a programmatic generator G that has access to ground-truth state information. Four conditioning schemes (LC, AC, FC, MC) fuse these cues with image observations. Experiments on classic control, car racing, and MuJoCo locomotion show improvements over vision-only (PPO-RGB) agents under tight training budgets.

## Strengths

- **Novel framing of human-in-the-loop RL**: Positioning the human as a "coach" who identifies task-relevant conceptual features—rather than a supervisor providing full demonstrations—is an interesting middle ground with genuine practical appeal. The four conditioning mechanisms offer a systematic exploration of how to integrate such cues.
- **Diverse experimental coverage**: The paper evaluates across classic control (Pendulum, Acrobot, IDP), car racing with a challenging hairpin variant, and high-dimensional locomotion (Ant, Humanoid, Cheetah), providing breadth of evidence for the approach.
- **Ablations on hint composition**: The systematic study of how individual vs. composite hints affect performance (O5, O6) is genuinely informative. Finding that "more information ≠ better performance" and that composite hints can overfit to training distributions (Swingto) adds nuanced insight.

## Weaknesses

### Fatal
None that fully invalidate the paper, but one major structural issue dominates:

### Major

1. **Unfair baseline comparison due to privileged state access.** The programmatic generator G requires access to ground-truth state (position, angular velocity, curvature, etc.)—information explicitly unavailable to vision-only agents. As a result, comparing HINTs to PPO-RGB is not a fair test of the coaching framework; it is essentially comparing an agent with privileged state information against one without. The more meaningful comparison is against PPO-x (state-only agents), and those results are far less impressive—on Cheetah, HINTs variants barely outperform PPO-x; on Ant, individual HINTs hints outperform PPO-x but composite HINTs does not. The paper acknowledges this limitation but does not adjust its framing or headline claims accordingly ("+80% over vision-only agents" is misleading without this context).

2. **The "human coaching" claim overstates the novelty.** The practical contribution reduces to: (a) a human selects which state variables to include, and (b) G computes those features from ground truth state. This is essentially privileged information RL with a human-designed feature selector—a well-studied paradigm. The gap between "human provides conceptual hints" and "programmatic generator computes ground-truth features" is large, and the paper's framework does not close it. The title and framing imply broader applicability than the implementation supports.

3. **Several results undermine key hypotheses.** On Acrobot (Table 2), all HINTS variants including the "joint composite" perform significantly worse than Expert/DAGGER (−302 vs. −67), which contradicts H1 and H3. On IDP, the "joint composite" hint (40.07) dramatically underperforms individual hint components (281, 400). These anomalies are not adequately explained and raise questions about the robustness and generality of the approach.

### Minor

- The Cheetah results (Table 3) are concerning: PPO-RGB achieves 1.82 and all HINTs variants are in the range 21–138, far from the DAGGER/PPO-x baseline (~2327). This suggests the approach scales poorly on some high-dimensional locomotion tasks.
- Training budgets are inconsistently set across domains (1k for Cheetah, 5k for Ant, 10k for Humanoid), making cross-domain comparisons difficult to interpret.
- The Swingto "deploy" row in Table 2 seems to reverse the direction of the training/eval split vs. what is described in the text—this is confusing and could indicate a setup or reporting issue.

### Trivial
- Minor inconsistencies in table label formatting.

## Nice-to-Haves

- An experiment where G uses estimated rather than ground-truth state (e.g., learned perception modules) would be needed to substantiate real-world applicability claims.
- A direct comparison against privileged-information RL baselines (e.g., asymmetric actor-critic) would clarify where the novelty actually lies.

## Novel Insights

The observation that human-selected partial state hints can outperform full state conditioning (O5) is genuinely interesting and non-obvious. It suggests that task-irrelevant state dimensions introduce noise into the policy input that hampers learning under tight budgets—a finding that could inform feature selection in privileged information RL more broadly. The demonstration that composite hints can overfit to training distributions and fail to generalize (O6, Swingto) is also a useful caution for hint design.

## Suggestions

- Reframe the contribution within the privileged information / asymmetric actor-critic literature and add those baselines.
- Include at least one experiment where the generator G does not have ground-truth access (e.g., uses a perception module) to support the real-world applicability claim.
- Provide a clear explanation for the anomalous IDP composite hint failure (40.07) and the Acrobot results, or acknowledge these as limitations.

## Score and Decision

The paper has a genuinely interesting idea—human-specified feature selection as a form of coaching—but the evaluation conflates this with privileged information access in a way that inflates the apparent gains. The headline claims rest on an unfair comparison. The core hypotheses receive mixed experimental support, with several notable failures inadequately discussed. The framework as implemented requires ground-truth state access, severely limiting its practical scope. These are significant issues for a method paper, though the breadth of experimentation and some genuine insights on hint composition provide value.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>