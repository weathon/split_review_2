## Summary

The paper introduces DemoGrasp, a framework for learning universal dexterous grasping policies from a single demonstration trajectory. The core insight is to formulate each grasping trial as a demonstration-editing process: an RL policy learns to modify the wrist pose (changing *where* to grasp) and hand joint angles (changing *how* to grasp) of the single demonstration, which is then replayed as a closed-loop trajectory. This reduces the problem to a single-step MDP with a compact action space, enabling efficient multi-task RL with a simple binary reward. The learned state-based policy is distilled into a vision-based flow-matching policy for zero-shot sim-to-real deployment. Experiments show state-of-the-art results on DexGraspNet (95% success), strong cross-dataset generalization across six unseen datasets and multiple robotic embodiments, and successful real-world grasping of 110 unseen objects including small, thin items.

## Strengths

- **Novel and effective problem formulation.** Casting dexterous grasping as a demonstration-editing task within a single-step MDP is a creative and well-motivated contribution. It significantly reduces the exploration burden compared to standard multi-step RL, allowing the use of a simple binary reward without complex reward shaping.
- **Strong empirical results.** The method achieves state-of-the-art success rates on DexGraspNet (95.2% on training objects, 94.4% on unseen categories) and demonstrates impressive cross-dataset generalization (84.6% average on six unseen datasets across six different robotic hands). Real-world results on 110 objects (86.5% overall, 71.1% on small/thin objects) are compelling and address a known weakness of prior work.
- **Thorough evaluation and ablations.** The paper provides extensive experiments: large-scale simulation comparisons, cross-embodiment transfer, real-world tests, and detailed ablation studies on action spaces, demonstration quality, training set size, camera configurations, and the necessity of RL. Each ablation gives clear insight into the method's design choices.
- **Practical sim-to-real transfer.** The vision-based policy trained via flow matching with domain randomization achieves zero-shot deployment on a physical robot, and the framework supports multiple camera types and cluttered scenes with language conditioning, demonstrating real-world applicability.

## Weaknesses

### Fatal
None.

### Major
- **Comparison to baselines may be unfair on spatial generalization.** The baselines (UniDexGrasp, UniDexGrasp++, UniGraspTransformer) are reported without object position randomization, whereas DemoGrasp trains and tests with a large 50cm×50cm region. While the paper argues this demonstrates stronger spatial generalization, the gap in Table 1 could partially reflect different evaluation protocols. The paper should report baseline performance under the same randomized conditions to enable an apples-to-apples comparison.
- **Limited analysis of failure modes.** The paper does not systematically analyze why certain objects (especially in the small/flat category) still fail. Understanding the primary failure causes (e.g., object geometry, visual ambiguity, collision constraints) would strengthen the claims and guide future work. The real-world results on "flat & thin tools" (60%) and "small" objects (76.7%) leave room for improvement without explanation.

### Minor
- **Generalization claim relies on a moderate training set.** The method trains on 175 objects for the cross-dataset experiments and 3,200 for DexGraspNet. While the paper shows marginal gains from training directly on test sets, the phrase "universal" might overstate the scope; the method is still trained on a finite set of object geometries. Performance on truly out-of-distribution objects (e.g., non-rigid, articulated, or transparent objects) is not explored.
- **Single-demonstration dependency.** The method assumes a single successful demonstration exists. While the ablation shows insensitivity to demonstration quality, the need for any demonstration is a mild limitation compared to methods that learn from scratch. The paper could discuss how to obtain such a demonstration on a real robot without simulation access.

### Trivial
- The paper's Figure 3 and the corresponding table contain identical numbers in all rows, suggesting a data entry error in the radar chart. The caption and surrounding text indicate that values differ across embodiments, so this is likely a formatting artifact from the PDF extraction.

## Nice-to-Haves

- Include failure case visualizations and analysis (e.g., what types of objects are most likely to fail and why).
- Compare against a baseline that uses a learned grasp sampler instead of a single demonstration to further justify the demonstration-editing approach.
- Provide open-source code and trained models to facilitate reproduction.

## Novel Insights

Beyond the paper's own contributions, the most novel insight is that a single demonstration trajectory, when appropriately parameterized by wrist and hand editing, can serve as a universal "prior" for dexterous grasping. This demonstrates that the exploration problem in multi-task RL can be dramatically simplified by constraining the policy to only modify a few high-level parameters of a known successful behavior, rather than searching in raw joint space. This idea may generalize to other manipulation tasks beyond grasping, where a single demonstration encodes the essential temporal structure.

## Suggestions

- For camera-ready, correct the apparent data error in the radar chart / table (Figure 3 appears to have identical success rates for all embodiments, which contradicts the text and likely reflects a copy-paste mistake).
- Report baseline performance under the same randomized object positions to confirm that the performance gap in Table 1 is not due to evaluation protocol differences.
- Add a brief discussion of failure cases: what visual or geometric properties cause the policy to fail on small/flat objects, and what future work could address these.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>