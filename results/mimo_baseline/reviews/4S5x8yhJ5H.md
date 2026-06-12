## Summary
This paper introduces VIBEFACE, a facial biometric dataset comprising 2,250 images and 1,550 videos from 50 demographically diverse subjects, specifically designed to cover eKYC (electronic Know Your Client) verification scenarios. The dataset includes standardized and selfie photographs, selfie videos, and structured eKYC verification videos across multiple lighting conditions, eyeglasses variations, and consumer smartphones. The authors benchmark three face detectors and two face verification models, reporting performance across scenarios, sessions, and demographic groups.

## Strengths
- **Novel and practical problem domain**: The paper identifies a genuine gap—no existing public dataset includes authentic eKYC-style video verification sequences alongside still images. eKYC is a rapidly growing real-world application with direct regulatory relevance (GDPR, AI Act), making this a timely contribution.
- **Thoughtful dataset design**: The 18 scenarios across 5 sessions cover a meaningful range of conditions (4 lighting types, eyeglasses variation, portrait orientation, multiple consumer devices). The eKYC verification scenarios (head rotation, blinking, mouth opening, face touching, etc.) reflect realistic liveness and identity verification workflows.
- **Demographic balance**: The dataset achieves near-equal distribution across gender (50:50), four racial groups (~25% each), and three age bands, with explicit attention to Fitzpatrick skin tone range. This is a notable strength compared to many existing datasets.
- **Ethical and legal rigor**: The paper demonstrates exemplary attention to GDPR compliance, informed consent, controlled-access licensing, and anonymization—a model for sensitive biometric data releases.
- **Informative benchmark experiments**: The demographic breakdowns in Tables 3 and 4 reveal meaningful patterns, such as MTCNN's reduced performance on African subjects and under challenging lighting, and the difficulty that off-angle poses and glasses pose for verification models.

## Weaknesses
### Fatal
None.

### Major
- **Very small scale limits utility**: With only 50 subjects, the dataset is small for a biometric benchmark. This severely limits the statistical power of any demographic fairness analysis—group-level differences could easily be driven by individual subject variation rather than systematic bias. For context, SOTERIA (the closest comparator) has 70 subjects, and most benchmark datasets have hundreds to thousands. The small subject pool also limits training applications and cross-dataset generalizability studies.
- **Controlled studio environment undermines realism claims**: The paper repeatedly emphasizes "realistic operational settings" and "unconstrained conditions," yet all data was collected in a "controlled studio environment" with "standardized instructions" and "trained operators." Genuine eKYC sessions occur in truly uncontrolled settings—users' homes, offices, outdoors—with highly variable device handling, network conditions, and backgrounds. The studio setting, while ensuring data quality, means the dataset may not fully capture the distribution shift encountered in deployment.
- **Benchmark experiments are shallow**: The evaluation consists entirely of running off-the-shelf pretrained models at inference time with an unjustified fixed threshold (0.5) for verification. There are no training experiments, no cross-dataset evaluation protocols, no formal fairness metrics (e.g., equalized odds, demographic parity), and no statistical significance testing. This makes it difficult to assess whether the dataset actually enables research that existing datasets cannot support.

### Minor
- **No liveness/PAD evaluation despite motivation**: The paper mentions presentation attack detection and deepfake detection as potential applications, but provides no experiments or protocols to demonstrate this. Given that eKYC inherently requires liveness detection, this is a missed opportunity to differentiate the dataset further.
- **Verification protocol design**: Using a single flash-session frontal image as the reference (Section 4.2) is a narrow protocol. More comprehensive evaluation (e.g., multiple reference images, gallery-probe splits, closed-set vs. open-set protocols) would better demonstrate the dataset's versatility.
- **Subject diversity within racial categories**: The four racial groups each contain only 12–13 subjects, making intra-group variation very limited and any group-level performance comparison unreliable.

### Trivial
None.

## Nice-to-Haves
- A standardized evaluation protocol/benchmark suite with train/test splits, evaluation metrics, and leaderboards would greatly increase the dataset's adoption and impact.
- Including at least a small set of presentation attack samples (e.g., printed photos, screen replays, 3D masks) would make the dataset directly usable for the PAD use case the authors mention.
- Reporting confidence intervals or bootstrap estimates for group-level metrics would help readers assess whether observed demographic disparities are statistically meaningful.

## Novel Insights
The paper's most novel observation is that existing biometric datasets systematically neglect the eKYC verification workflow, which involves structured user interactions (head rotations, blinking, face touching) rather than passive capture. This is a genuine gap with practical importance. The benchmark results also provide some useful empirical observations—for instance, that MTCNN shows notable racial disparities in detection (0.812 for African vs. 0.984 for East Asian subjects in frontal views) while RetinaFace and MediaPipe are largely invariant, and that the youngest age group (18–30) paradoxically yields the lowest verification rates, which warrants further investigation.

## Suggestions
- Expand the dataset beyond 50 subjects to at least 200+ to enable meaningful fairness analysis and training use cases.
- Develop a standardized benchmark protocol with defined train/validation/test splits, evaluation metrics (TAR@FAR, EER), and fairness-specific measures (e.g., FTE rate by demographic group).
- Consider collecting a portion of data in truly uncontrolled environments to bridge the gap between studio quality and real-world eKYC conditions.
- Add presentation attack samples (2D/3D masks, printouts, screen replays) to support the PAD research direction mentioned in the conclusions.

## Score and Decision
The paper addresses a genuine and practical gap with careful dataset design, good demographic balance, and strong ethical practices. However, the very small scale (50 subjects), the controlled studio setting that limits ecological validity, and the shallow benchmark experiments collectively weaken the contribution. For a dataset/benchmark paper at ICLR, the experiments need to convincingly demonstrate that the dataset enables new research that prior resources cannot—and the current evaluation falls short of this bar. The paper would be substantially strengthened by a larger subject pool and more rigorous evaluation protocols.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: Reject