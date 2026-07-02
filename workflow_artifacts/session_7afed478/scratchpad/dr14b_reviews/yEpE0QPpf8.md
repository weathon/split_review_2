### Summary

This paper introduces a new task, Grounding-IQA, which integrates multimodal referring and grounding with IQA to realize more fine-grained quality perception. The authors construct a corresponding dataset, GIQA-160K, and a benchmark, GIQA-Bench, to evaluate the grounding-IQA performance from three perspectives: description quality, VQA accuracy, and grounding precision. The experiments demonstrate that the proposed method facilitates the more fine-grained IQA application.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper introduces a novel IQA paradigm, grounding-IQA, which combines multimodal referring and grounding with IQA to enhance quality perception. This is a creative extension of existing IQA methods.
2. The paper constructs a high-quality dataset, GIQA-160K, with an automated annotation pipeline. The dataset is versatile and suitable for fine-tuning existing MLLMs.

### Weaknesses

#### Some Related Works


#### comment

1. The technical contribution is limited. The method appears to be a combination of IQA and grounding tasks, lacking sufficient technical innovation. The approach seems to primarily leverage existing models for object detection and quality assessment, without introducing novel architectures or learning mechanisms that would significantly advance the field. The integration of these components, while useful, does not represent a substantial technical leap.
2. The motivation is unclear. The paper does not adequately explain why grounding is necessary for IQA. It is not clear how grounding enhances the assessment of image quality, especially when compared to existing methods that provide detailed quality descriptions without explicit grounding. The paper needs to articulate the specific scenarios where grounding provides a distinct advantage over traditional IQA methods.

### Suggestions

The paper should more clearly articulate the specific technical innovations that differentiate it from a simple combination of existing IQA and grounding methods. The authors should detail the novel aspects of their approach, such as any new loss functions, training strategies, or model architectures that are specifically designed for the Grounding-IQA task. For example, if the model uses a specific attention mechanism to integrate quality assessment with object localization, this should be clearly explained and justified. Furthermore, the paper should provide a more detailed analysis of the model's performance on different types of image degradations, and how the grounding component contributes to more accurate quality assessment in these scenarios. This would help to demonstrate the technical depth of the proposed method and its advantages over existing approaches.

To better motivate the need for grounding in IQA, the authors should provide concrete examples of scenarios where grounding is essential for accurate quality assessment. For instance, consider a situation where multiple objects in an image have varying degrees of blur. A global quality score might not capture the specific locations and severity of these degradations. In such cases, the paper should explain how the grounding component allows for a more precise and fine-grained assessment, enabling users to identify the specific regions that are affecting the overall image quality. The authors should also compare their approach with existing methods that provide detailed quality descriptions, highlighting the limitations of these methods in terms of spatial localization and how grounding addresses these limitations. This would help to clarify the unique contribution of the proposed method and its practical relevance.

The paper needs to include a more thorough evaluation of existing grounding and IQA models on the proposed task. This would involve testing state-of-the-art models on the GIQA-Bench and demonstrating their limitations in handling fine-grained quality assessment. The authors should provide a detailed analysis of the failure cases of these models, highlighting the specific challenges that the proposed method is designed to address. For example, the authors could show how existing grounding models fail to accurately localize quality issues, or how traditional IQA models lack the spatial resolution to provide fine-grained assessments. This would provide a stronger justification for the proposed task and demonstrate the need for a new approach that integrates both grounding and IQA.

### Questions

1. The paper introduces a new task, Grounding-IQA, which integrates image quality assessment (IQA) with visual grounding. The authors propose a dataset, GIQA-160K, and a benchmark, GIQA-Bench, to support this new task. However, the technical contribution of the proposed method appears to be limited. The approach seems to be a combination of existing IQA and grounding tasks, lacking significant technical innovation. The paper does not clearly articulate the specific technical advancements or novel mechanisms that differentiate this work from a straightforward combination of existing methods. This raises concerns about the originality and depth of the technical contribution.
2. The motivation for introducing the grounding task in IQA is not clearly explained. The paper does not provide sufficient justification for why grounding is necessary or beneficial for IQA. It is unclear how grounding enhances the assessment of image quality, especially when compared to existing methods that provide detailed quality descriptions without explicit grounding. The paper needs to articulate the specific scenarios where grounding provides a distinct advantage over traditional IQA methods. Without a clear motivation, the necessity and value of the proposed task are questionable.
3. The paper lacks sufficient evidence to demonstrate the limitations of existing models in handling the proposed task. While the authors introduce a new task and dataset, they do not adequately show how current state-of-the-art models, particularly those designed for grounding and IQA, fail to address the specific challenges of fine-grained quality assessment that the proposed method aims to solve. The paper should include a more thorough evaluation of existing models on the proposed task, highlighting their shortcomings and justifying the need for a new approach. This would strengthen the paper's argument and demonstrate the significance of the proposed work.

### Rating

6

### Confidence

4

**********