

{0}------------------------------------------------

# ZS-VCOS: Zero-Shot Video Camouflaged Object Segmentation By Optical Flow and Open Vocabulary Object Detection

Wenqi Marshall Guo<sup>1,2</sup> Mohamed Shehata<sup>1</sup> Shan Du<sup>1,\*</sup>

<sup>1</sup>Department of CMPS, University of British Columbia, Canada

<sup>2</sup>Group of Methane Emission Observation & Warning (MEOW), Weathon Software, Canada

wg25r@student.ubc.ca, mohamed.sami.shehata@ubc.ca, shan.du@ubc.ca \*Corresponding Author

## Abstract

*Camouflaged object segmentation presents unique challenges compared to traditional segmentation tasks, primarily due to the high similarity in patterns and colors between camouflaged objects and their backgrounds. Effective solutions to this problem have significant implications in critical areas such as pest control, defect detection, and lesion segmentation in medical imaging. Prior research has predominantly emphasized supervised or unsupervised pre-training methods, leaving zero-shot approaches significantly underdeveloped. Existing zero-shot techniques commonly utilize the Segment Anything Model (SAM) in automatic mode or rely on vision-language models to generate cues for segmentation; however, their performances remain unsatisfactory, due to the similarity of the camouflaged object and the background. This work studies how to avoid training by integrating large pre-trained models like SAM-2 and Owl-v2 with temporal information into a modular pipeline. Evaluated on the MoCA-Mask dataset, our approach achieves outstanding performance improvements, significantly outperforming existing zero-shot methods by raising the  $F$ -measure ( $F_{\beta}^{w}$ ) from 0.296 to 0.628. Our approach also surpasses supervised methods, increasing the  $F$ -measure from 0.476 to 0.628. Additionally, evaluation on the MoCA-Filter dataset demonstrates an increase in the success rate from 0.628 to 0.697 when compared with FlowSAM, a supervised transfer method. A thorough ablation study further validates the individual contributions of each component. Besides our main contributions, we also highlight inconsistencies in previous work regarding metrics and settings.*<sup>1</sup>

## 1. Introduction

Camouflaged object detection and segmentation (COD and COS) is an image detection/segmentation task for objects

that are concealed in the background (See Figure 2 for example). It poses significant challenges beyond traditional object detection and segmentation tasks. This increased difficulty primarily stems from the inherent nature of camouflaged objects, which are visually similar to their backgrounds in terms of patterns, colors, and textures [7, 45], effectively blending into their surroundings and complicating accurate identification and delineation. Despite these challenges, effective solutions for COD and COS have considerable real-world significance, especially in critical fields such as defect detection [17], pest control [35], and medical imaging for lesion segmentation [11].

Extending these image-based tasks into the temporal domain, video camouflage object detection and segmentation (VCOD and VCOS) have emerged as specialized subsets derived from video object detection (VOD) and video object segmentation (VOS), respectively. By leveraging motion cues, such methods can potentially overcome some limitations inherent to static images. Optical flow, for instance, has proven particularly useful by measuring pixel-level movements, thus enabling differentiation of moving camouflaged entities from their backgrounds.

However, camouflage-related tasks in both static and dynamic contexts remain relatively underdeveloped compared to traditional detection and segmentation methods. Most prior work in this area has focused on supervised learning, relying on complex architectures and labelled data. Yet, even these supervised models often struggle with camouflaged objects due to the lack of distinct features. On the other hand, zero-shot methods, which avoid training by using large pre-trained models like SAM and vision-language models, are severely less explored and currently perform worse than supervised methods.

To address this gap, we propose a method that integrates optical flow, a vision-language model, and SAM in a modular pipeline. Each stage of the pipeline uses the output of the previous one to refine its segmentation cues. Rather than relying on any training or fine-tuning, our approach operates in a zero-shot setting and achieves strong performance. On

<sup>1</sup>Code can be found on GitHub after publication.

{1}------------------------------------------------

the MoCA-Mask dataset, our method improves mIoU from 0.273 (baseline zero-shot methods) to 0.561. It also outperforms multiple supervised methods, which typically score around 0.422. Furthermore, on the MoCA-Filtered dataset, our method raises the detection success rate from 0.628 to 0.697. These gains highlight the effectiveness of combining motion-based cues with strong foundation models.

In summary, our technical contributions are (1) a zero-shot framework for camouflaged object segmentation in video that surpasses supervised baselines, (2) extensive experimentation on different components and prompting strategies of our methods, and (3) insights demonstrating that properly designed zero-shot pipelines can not only compete with but in some cases outperform traditional supervised approaches.

Additionally, we noticed that previous works often failed to systematically compare their results against other methods evaluated under the same settings (test-time supervised, also known as tracking, and test-time unsupervised). Furthermore, metric calculation in these benchmarks frequently suffered from inconsistent aggregation methods and inadequate handling of special cases. In this work, we highlight these issues, re-evaluate the state-of-the-art methods using a consistent and corrected metric, and ensure a direct and fair comparison between our method and the current state-of-the-art. We urge the research community to adopt standardized evaluation practices to enable clearer and more meaningful comparisons in future studies.

## 2. Related Work

### 2.1. Optical Flow

Optical flow is a technique used to measure pixel movement in videos. It has been used in video processing or recognition for a long time; one of the most significant works is the two-stream network published in 2014 [36]. There are two types of optical flow: sparse and dense optical flow. Sparse optical flow gives a movement vector for points of interest in the image, whereas dense optical flow estimates movement for all pixels in the image. One of the most famous sparse optical flows is the Lucas-Kanade method [24], which uses the assumption that local pixels have similar motion. It can be used in camera motion estimation for panoramic image generation or motion compensation. Dense optical methods, like RAFT [39] and GMFlow [48], can provide movement information for every pixel in the frame, and it has demonstrated promising performance in camouflaged object detection based on movement differences between foreground and background, although their methods rely on training and the performance can be further improved.

### 2.2. Moving Object Segmentation

Moving object segmentation is a task aiming to segment moving objects within a video sequence. These objects could be general entities, as in DAVIS [33] and YouTube-VOS [49], or camouflaged ones, as presented in MoCA-Mask [7] and CAD [2]. The segmentation task can be performed in two scenarios: test-time semi-supervised, where one annotated frame is provided and the model propagates this annotation to subsequent frames, and test-time unsupervised, where no annotation is provided during testing. These two methods have distinct difficulty levels and should be compared separately.

Optical flow has been extensively used in video object segmentation, primarily in two ways: propagating segmentation masks and differentiating objects from background based on different motions.

#### 2.2.1. Methods Leveraging Optical Flow as Motion Cues

Brox *et al.* [3] utilized long-term optical flow trajectories combined with clustering for segmenting videos. Ochs *et al.* [30] applied flow-based motion cues to resolve ambiguities in color-based segmentation. Xiao *et al.* [46] employed optical flow cues to reinforce target frame representations. Yang *et al.* [52] used both optical flow and RGB input to assist video object segmentation. FlowI-SAM and FlowP-SAM [47] utilized optical flow either exclusively as input (FlowI-SAM) or as a prompt guiding segmentation of RGB frames (FlowP-SAM). Both FlowI-SAM and FlowP-SAM handled standard and camouflaged objects effectively.

#### 2.2.2. Methods Employing Optical Flow for Mask Propagation

Tsai *et al.* [40] considered segmentation and optical flow simultaneously, using optical flow to propagate masks and segmentation masks to refine flow boundaries. TR-OVIS [50] employed optical flow to propagate key-frame information, thus enhancing inference speed for open-vocabulary video instance segmentation.

#### 2.2.3. Joint Modeling of Segmentation and Flow without Using Flow as Input

Cheng *et al.* [5] (SegFlow) treated segmentation and optical flow estimation as similar tasks and jointly trained a network to take in video frames and output segmentation masks and optical flow.

#### 2.2.4. Alternative Motion Methods without Optical Flow

LangGas [14] applied background subtraction to isolate moving regions, followed by an open vocabulary object detector and SAM2 [34] to segment gas leaks in synthetic datasets. Zero-shot Background Subtraction (ZBS) [1] detected the displacement of objects across frames using object detection techniques to classify their motion status, thus identifying moving objects without optical flow.

{2}------------------------------------------------

![Figure 1: Overview of Our Method. This flowchart illustrates the process of camouflage object detection and segmentation. It starts with two input frames, 'Frame 1' and 'Frame 1+1'. 'Frame 1' is processed by 'Flow Extraction' to produce 'Momentum Update of Optical Flow'. This is then combined with 'Frame 1+1' in an 'Overlay' step. The 'Overlay' result goes to 'Open Vocabulary Object Detection', which produces a heatmap. This heatmap is then processed by 'SAM Segmentation and Tracking' to produce the final 'Output' segmentation mask. A 'Bidirectional Mask Propagation' step connects the 'Output' back to the 'Open Vocabulary Object Detection' heatmap.](b230b8f21d8e82d55c0d311c8c32ef73_img.jpg)

Figure 1: Overview of Our Method. This flowchart illustrates the process of camouflage object detection and segmentation. It starts with two input frames, 'Frame 1' and 'Frame 1+1'. 'Frame 1' is processed by 'Flow Extraction' to produce 'Momentum Update of Optical Flow'. This is then combined with 'Frame 1+1' in an 'Overlay' step. The 'Overlay' result goes to 'Open Vocabulary Object Detection', which produces a heatmap. This heatmap is then processed by 'SAM Segmentation and Tracking' to produce the final 'Output' segmentation mask. A 'Bidirectional Mask Propagation' step connects the 'Output' back to the 'Open Vocabulary Object Detection' heatmap.

Figure 1. Overview of Our Method.

![Figure 2: Visual Comparison Of Our Methods and Previous Supervised Methods. This figure shows a grid of 16 columns and 5 rows. The columns represent different video sequences: 'shoe_basket_10', 'feeding_3', 'dick_head_3', 'lion_dog_0', 'ant5_fox', 'ants_corned_out_0', 'copperhead_snake', 'flower_cup_outdoor_0', 'flower_cup_outdoor_2', 'fox', 'ant5_fox_3', 'flower_cup_outdoor_2', 'Mask_out_1', 'copperhead_snake_0', 'moth', and 'morgue'. The rows represent different methods: 'Image' (original frames), 'CF' (Canny Filter), 'U-Net', 'ZoomNet', and 'Ours' (the proposed method). The 'Ours' row shows significantly better segmentation results compared to the other methods, especially in complex backgrounds.](7e2f2d03a5dda38b038fd4884629a2b4_img.jpg)

Figure 2: Visual Comparison Of Our Methods and Previous Supervised Methods. This figure shows a grid of 16 columns and 5 rows. The columns represent different video sequences: 'shoe\_basket\_10', 'feeding\_3', 'dick\_head\_3', 'lion\_dog\_0', 'ant5\_fox', 'ants\_corned\_out\_0', 'copperhead\_snake', 'flower\_cup\_outdoor\_0', 'flower\_cup\_outdoor\_2', 'fox', 'ant5\_fox\_3', 'flower\_cup\_outdoor\_2', 'Mask\_out\_1', 'copperhead\_snake\_0', 'moth', and 'morgue'. The rows represent different methods: 'Image' (original frames), 'CF' (Canny Filter), 'U-Net', 'ZoomNet', and 'Ours' (the proposed method). The 'Ours' row shows significantly better segmentation results compared to the other methods, especially in complex backgrounds.

Figure 2. Visual Comparison Of Our Methods and Previous Supervised Methods.

Wang *et al.* [41], Wang *et al.* [42], and Li *et al.* [21] performed segmentation directly from raw RGB frames with text as queries, without incorporating explicit motion signals or optical flow.

### 2.3. Moving Camera Background Subtraction

Moving camera background subtraction (MCBS) is very similar to the VOS task, where it extracts the moving foreground from the background by using a background model. Unlike fixed camera background subtraction, where pixels from the same object/background are mostly aligned throughout the video, MCBS is challenging as the background is moving, and the algorithm cannot simply compare the pixel value at the same absolute location. Kurnianggoro *et al.* [18] used motion compensation to solve this problem, while DeepMCBM [8] and PanoramicPCA [29] built a panoramic background model.

### 2.4. Camouflage Object Detection and Segmentation

Unlike regular object detection and segmentation, camouflage object tasks are significantly more challenging because the foreground usually seamlessly blends into the

background. There are two tasks in camouflage object detection: image-based camouflage object detection (usually referred to as COD) and video-based camouflage object detection (VCOD). They could also be extended to segmentation, namely COS and VCOS. VCOD/S allows the model to use motion cues to detect the foreground but also brings in the challenges of temporal changes [45].

#### 2.4.1. Datasets

Since this paper focuses on VCOS, we mainly introduce video-based datasets here. For image-based datasets like COD10K [10], N4K [25], and CAMO [20], readers can refer to the review article [45].

There are two major datasets and 3 variants in video camouflage object detection: Camouflaged Animal Dataset (CAD) [2] and Moving Camouflaged Animal Dataset (MoCA) [19]. However, MoCA is an object detection dataset but not a segmentation dataset. It contains some non-camouflaged animals or animals that do not have locomotion. Thus, two variances of MoCA were proposed. MoCA-filtered [51] and MoCA-Mask [7].

MoCA-filtered mainly removed non-locomotive videos from the dataset, with additional processing such as cropping away logos and borders, resampling frames, and incor-

{3}------------------------------------------------

| Method | Pub. | Setting | $S_a \uparrow$ | $F_{\beta}^w \uparrow$ | MAE↓ | $E_d \uparrow$ | mDice↑ | mIoU↑ |
|-|-|-|-|-|-|-|-|-|
| SLT-Net [7] | CVPR 22 | SV Tr | 0.656 | 0.357 | 0.021 | 0.785 | 0.397 | 0.310 |
| ZoomNeXt [32] | TPAMI 24 | SV Tr | <b>0.734</b> | <b>0.476</b> | 0.010 | 0.736 | <b>0.497</b> | <b>0.422</b> |
| TSP-SAM(M+B) [15] | CVPR 24 | SV Tr | 0.689 | 0.444 | <b>0.008</b> | <b>0.808</b> | 0.458 | 0.388 |
| Gao <i>et al.</i> [12] | arXiv 25 | SV Tr | 0.706 | 0.455 | 0.011 | - | 0.495 | 0.404 |
| SAM2 Tracking [37] | arXiv 24 | SV Te | 0.804 | 0.691 | 0.004 | - | - | - |
| SAM-PM [27] | CVPRW 24 | SV Tr+Te | 0.728 | 0.567 | 0.009 | 0.813 | 0.594 | 0.502 |
| Finetuned SAM2-T + Prompts [53] | arXiv 24 | SV Tr+Te | <b>0.832</b> | <b>0.726</b> | <b>0.005</b> | <b>0.908</b> | <b>0.756</b> | <b>0.652</b> |
| CVP [38] | ACM MM 24 | ZS | 0.569 | 0.196 | 0.031 | - | - | - |
| SAM-2-S Auto [53] | arXiv 24 | ZS | 0.497 | 0.201 | 0.141 | 0.608 | 0.202 | 0.174 |
| LLaVA + SAM2-L [53] | arXiv 24 | ZS | 0.624 | 0.315 | 0.046 | 0.688 | 0.334 | 0.291 |
| Shikra + SAM2-L [53] | arXiv 24 | ZS | 0.502 | 0.146 | 0.107 | 0.590 | 0.157 | 0.124 |
| Ours | - | ZS | <b>0.776</b> | <b>0.628</b> | <b>0.008</b> | <b>0.878</b> | <b>0.648</b> | <b>0.550</b> |

Table 1. **Performance comparison on the MoCA-Mask dataset [7].** “SV Tr” denotes supervised training. “SV Te” denotes supervised testing, where one frame from the video was provided to the model along with prompts. “ZS” indicates zero-shot learning. The grouping of methods is based on settings. Metrics shown in gray represent results from prior work that may contain methodological inconsistencies. These are included for transparency and completeness but should be interpreted with caution. Our method significantly outperforms all zero-shot and even supervisely trained and unsupervisely tested methods.

porating the bounding boxes. Since it still lacks segmentation masks, papers using this dataset ([51] [47]) used the detection success rate based on the IoU threshold to evaluate the results. MoCA-Mask improved MoCA by removing scenes with obvious animals and converting bounding boxes into masks. In addition to ground truth masks provided every 5 frames, they also used bidirectional optical flow to generate pseudo masks for unlabelled frames.

#### 2.4.2. Algorithms

Existing methods can be classified into supervised, unsupervised, and zero-shot categories based on training settings and into test-time semi-supervised or test-time unsupervised categories based on inference settings.

SLT-Net [7] is a supervisely trained and unsupervisely tested model. It argued that when using optical flow and homography, the error might be accumulated from both the motion estimation and segmentation. Thus, they proposed to use a unified framework for both motion estimation and segmentation. Additionally, they used a long-term spatiotemporal transformer to refine short-term predictions, although this long-term module provides marginal improvement. ZoomNeXt [32] is an improved version of ZoomNet [31], mainly adapted from image-based COS to video-based COS and improved performance by introducing more structural extensions. ZoomNeXt is trained on both image COS datasets and video COS datasets, including MoCA-Mask [7]. ZoomNet and ZoomNeXt both use zooming to capture features at different scales. Similar to SLT-Net, they are both supervisely trained and unsupervisely tested methods.

Previous studies have sometimes failed to clearly differentiate between test-time semi-supervised and unsupervised tasks, despite their differing levels of difficulty. For

example, SAM-PM [27], requiring supervision during both training and inference, reported state-of-the-art results compared with SLT-Net [7]. However, SLT-Net operates under supervised training but unsupervised testing conditions. This fundamental difference in evaluation criteria renders direct comparisons between these two methods somewhat inequitable. Although the authors of SAM-PM described their method as semi-supervised (which we refer to in this paper as test-time supervised), they did not clearly acknowledge this distinction when making comparisons or drawing conclusions.

Flow-SAM [47] and Motion Grouping [51], though trained initially for video object segmentation tasks, demonstrated robust performance on VCOS tasks. Specifically, Flow-SAM utilizes supervised training, while Motion Grouping employs self-supervised training. Neither method requires supervision during inference.

For zero-shot unsupervised testing neither training nor inference is supervised), Chain of Vision Perception (CVP) [38] represents an early effort employing vision-language models (VLMs) for COD/S tasks, with a primary focus on images rather than videos. CVP prompts a vision-language model to identify the location of camouflaged objects. Subsequently, these locations are refined and given to a segmentation model. Properly designed prompting can further enhance the model’s performance. CVP achieved higher performance than several supervised methods on datasets such as CAMO [20], COD10K [10], and NC4K [25]. However, its results on the MoCA-Mask were suboptimal, with a weighted F-score ( $F_{\beta}^w$ ) of 0.196. Zhou *et al.* [53] improved upon this by employing LLaVA [22] or Shikra [4] as the vision-language model and utilizing SAM-2 for segmentation. A similar approach is evident in Grounded SAM

{4}------------------------------------------------

[23], which integrates Grounding DINO and SAM for open-vocabulary segmentation of regular objects.

While comparing test-time unsupervised methods with semi-supervised methods is inherently unfair, semi-supervised inference methods without prior training have demonstrated that SAM-2 can reasonably track camouflaged objects when provided with accurate prompts.

Detailed performance comparisons of these methods can be found in Table 1.

## 3. Proposed Methods

### 3.1. Motion Detection

Our method builds upon LangGas [14]. Gas leakage shares many similarities with a camouflage object: they both have low contrast against the background, but they often have different relative motion with respect to the background. Previous studies, including LangGas [14] and VideoGasNet [43], have shown that background subtraction effectively captures subtle changes in the input. High-quality masks can then be extracted from the resulting foreground using vision-language models (VLMs) together with SAM2 [34] [14]. However, traditional BGS methods can only be used in fixed camera settings, and most camouflage object segmentation datasets and real-world applications do not feature a fixed camera; while a moving camera background subtraction method can sometimes work, it may fail under complex camera motion. In addition, if an object does not fully move away to expose the background behind it, a valid background model cannot be built.<sup>2</sup>

To address such challenges, we turn to another commonly used motion detection method: optical flow. By tracking the movement of each pixel between two adjacent frames, optical flow can show different movement patterns in the image. Following Motion Grouping [51] and FlowSAM [47], we employ RAFT [39] to compute optical flow. However, we found that highly repetitive backgrounds or videos with margins can compromise RAFT optical flow, thereby diminishing its usefulness. Thus, we combine optical flow with background subtraction, applying the latter (BGS) when there is no camera motion and using optical flow otherwise. To detect camera motion, we use a simple Lucas-Kanade method [24] to track points in the video. The movement is used to estimate the affine transformation throughout the video and detect the furthest point the camera reached.

For videos processed using optical flow, we compute an optical flow tensor  $F \in \mathbb{R}^{(t-1) \times h \times w \times 2}$ , where  $t$  is the total number of frames,  $h$  and  $w$  denote frame height and width, respectively, and the two channels represent horizontal and

vertical pixel displacements. The corresponding intensity map is obtained by calculating the magnitude of displacement vectors at each pixel location, and the intensity map is normalized to 0-255, as shown in Equation (1). We also experimented with maintaining a momentum-based moving average over the flow vector map to address cases where the object temporarily stops moving. The formulation is given in Equation (2). We also experimented with subtracting the mean displacement vector (averaged over the frame) from every pixel to reduce camera motion, inspired by the Two-Stream Network approach [36].

$$I_{i,x,y} = \text{normalize}_{[0,255]}(\|F_{i,x,y}\|_2) \quad (1)$$

$$F_i = \begin{cases} F_i, & i = 1 \\ (1 - m) \cdot F_i + m \cdot F_{i-1}, & i > 1 \end{cases} \quad (2)$$

For videos analyzed using background subtraction, we followed [14]. First, we obtain a background model tensor  $B \in \mathbb{R}^{t \times h \times w \times 3}$  using MOG2 [54, 55]. Here, each frame in the background model matches the dimensions and RGB channels of the input frames. The intensity map in this scenario is computed by taking the absolute pixel-wise difference between the current frame  $C_i$  and the background frame  $B_t$ , and normalized to 0-255, as detailed in Equation (3).

$$I_{i,x,y} = \text{normalize}_{[0,255]}(\|C_{i,x,y} - B_{i,x,y}\|_1) \quad (3)$$

The intensity map is then blended into the current frame using a specific color (e.g. blue) to highlight the moving parts in the current frame.

### 3.2. Open Vocabulary Detection

We used OwlV2 [28] as our detection vision language model (VLM), same as in LangGas [14]. Since all videos in MoCA are about animals or insects, following [53], we included that in the prompt. Following LangGas [14], we used one positive prompt and 3 negative prompts so that when the object is closer to the negative prompts, it can be correctly classified into the negative prompt and reduce interference. We used “an animal or insect being highlighted in blue” as a positive prompt and “background”, “logo or sign,” and “plant” as negative prompts. Since the camouflage object segmentation is usually a single object problem, we select the box with the highest score after the VLM.

### 3.3. Segmentation and Tracking

Given that camouflage can significantly reduce object detection performance for VLM, many frames might result in missed detections. However, previous research [53] [27] [37] has demonstrated that vanilla SAM-2 [37], when

<sup>2</sup>Although the object’s edges could be shown in the foreground map, camera movements may also highlight these edges, making it hard for the algorithm to distinguish them.

{5}------------------------------------------------

|  | Motion Detection | Mean Subtraction | Momentum | Tracking | $S_\alpha \uparrow$ | $E_\phi \uparrow$ | mIoU $\uparrow$ |
|-|-|-|-|-|-|-|-|
| (a) | None | - | - | None | 0.621 | 0.596 | 0.252 |
| (b) | None | - | - | Bidirectional | 0.643 | 0.657 | 0.301 |
| (c) | OF Only | ✓ |  | Bidirectional | 0.752 | 0.832 | 0.508 |
| (d) | OF Only | ✓ | ✓ | Bidirectional | 0.750 | 0.824 | 0.513 |
| (e) | OF/BGS | ✓ |  | Bidirectional | 0.759 | 0.843 | 0.522 |
| (f) | OF/BGS | ✓ |  | None | 0.676 | 0.698 | 0.363 |
| (g) | OF/BGS | ✓ | ✓ | None | 0.683 | 0.723 | 0.372 |
| (h) | OF/BGS | ✓ | ✓ | Forward Only | 0.747 | 0.825 | 0.497 |
| (i) | OF/BGS |  | ✓ | Bidirectional | <b>0.782</b> | <b>0.859</b> | <b>0.561</b> |
| Ours | OF/BGS | ✓ | ✓ | Bidirectional | 0.776 | <b>0.878</b> | 0.550 |

Table 2. Ablation study of different components including motion detection (optical flow and background subtraction), mean subtraction, momentum update, and tracking strategies. Motion detection includes either optical flow only (OF) or a combination of optical flow and background subtraction (OF/BGS). We evaluate each configuration using  $S_\alpha$ ,  $E_\phi$ , and mean IoU (mIoU).

guided by explicit prompts, can achieve effective object tracking. We utilized this tracking capability by supplying SAM-2 with all prompts obtained from VLM detections and allowed it to propagate these prompts across all video frames. These prompts consist of the bounding boxes generated by the VLM and the center of mass of the intensity map within each bounding box as a point prompt.

Since forward propagation alone limits object tracking to frames following the initial successful detection, we implemented a bidirectional propagation approach. We provided prompts for both the original forward-playing video and its reversed sequence. Masks generated from both directions are combined using an OR operation, producing the final robust masks across the entire video sequence.

## 4. Experiments and Results

### 4.1. Benchmark

#### 4.1.1. Metrics and Datasets

In this paper, we examine two variants of the MoCA dataset [19]: MoCA-Mask [7] and MoCA-Filtered [51]. The Camouflaged Animal Dataset (CAD) [2] is not used due to its inaccessibility, as the server is offline and the dataset is not provided by a third party. MoCA-Mask is a segmentation dataset, and our evaluation approach aligns with SLT-Net [7]. We report the following metrics: S-measure ( $S_\alpha$ ) [6], weighted F-measure ( $F_\beta^w$ ) [26], and Mean Absolute Error (MAE). More details on these metrics can be found in the SLT-Net paper and their original sources. We did not focus on E-measure [9], mean Dice coefficient, and mean Intersection-over-Union (IoU) in our comparison with previous methods because they will yield different results depending on metric calculation methods, which we explain in Section 4.1.2. All standard metrics are provided in Table 1, with metrics that could be miscalculated by the previous method colored in gray. For our internal comparisons in

the ablation study, we primarily focus on a subset of these metrics (using a subset of internal comparisons is used in SLT-Net): S-measure, E-measure, and mean IoU. To ensure consistency and fairness, we adopted the evaluation code and methodology from SLT-Net.

#### 4.1.2. Metric Calculation Inconsistency

Metrics such as mean IoU can be computed in three primary ways: (1) calculating IoU for each frame individually, averaging across frames within one video, and then averaging across videos, (2) calculating IoU for each frame, and averaging all frames’ results, or (3) calculating an IoU for all frames, which is equivalent to treating the entire video sequence as a single, large concatenated image for both the predicted masks and the ground truth masks, and then computing the IoU on these two large, combined frames. The three calculation methods can yield different results, occasionally significant. Additionally, the calculation script for each paper varies slightly, such as SLT-Net omits the last frame to keep for flow-based methods.

In our paper, we computed the metrics using the SLT-Net script. This methodology might differ from other reported methods. We recalculated these metrics using the SLT-Net evaluation implementation for the supervised state-of-the-art method, ZoomNeXt, and it resulted in slightly elevated results of  $E_m=0.755$ , mDice=0.511, and mIoU=0.438 compared to the original reporting (see Table 1). However  $S_\alpha$ ,  $F_\beta^w$ , and MAE remains unchanged. Thus, in this paper, we focus on these 3 metrics when comparing them across previous methods.

Although there are forum discussions about this issue [16], there are only a few publications mentioned about this issue [14, 44]. We encourage future research to clearly specify their metric calculation methodology and consider adopting this standardized frame-then-video averaging approach to facilitate fair comparisons.

{6}------------------------------------------------

Since the SLT-Net method produces soft outputs with continuous pixel values, they considered multiple thresholds and report a max and mean metric. However, as our method produces binary outputs, we used a single threshold value of 0.5.

MoCA-Filtered [51] is a detection dataset. Following [51] and [47], we used the detection success rate based on IoU. Similar to MoCA-Mask, we employed the original evaluation code provided by [51].

#### 4.1.3. Baselines

For MoCA-Mask, we selected SLT-Net [7], ZoomNeXt [32], TSP-SAN (M+B) [15], and the proposed method from the MSVOD dataset paper [12] as our supervised training baselines. For zero-shot baselines, we employed Chain of Visual Perception (CVP) [38], SAM-2-L Auto, and SAM-2 combined with either LLaVA [22] or Shikra [4], following the approach described in [53]. Additionally, we utilized three test-time supervised methods [27, 37, 53] as performance upper bounds.

For MoCA-Filtered, we adopted FlowSAM (including FlowI-SAM and FlowP-SAM) [47] and Motion Grouping [51] as baselines for supervised and self-supervised pre-training, respectively, using non-camouflage object datasets and testing on a camouflage dataset.

#### 4.1.4. Settings

Since our method is zero-shot without training, we directly evaluated it on the testing set. For MoCA-Mask, to minimize overfitting hyperparameters on the limited test set while ensuring reasonable performance in the real world, we slightly adjusted hyperparameters manually and swept the VLM threshold (following [14]) from 0.03 to 0.13 (inclusive) at a step of 0.02. For MoCA-Filtered, we employed a fixed threshold of 0.12 tuned by hand. Optical flow was computed using RAFT-Things [39], employing the implementation provided by Motion Grouping [51] with only forward flow and a frame gap of 1. All input images were passed directly to the model processor without resizing or cropping. The momentum parameter ( $m$ ) was set to 0.9. We used OwlV2-Base-Patch16-Ensemble and Sam2.1-Hiera-Small as our VLM and segmentation models.

### 4.2. Results

#### 4.2.1. MoCA-Mask

The results of our method compared with previous baselines on MoCA-Mask are presented in Table 1. Our approach achieves the highest  $F_{\beta}^w$  and  $S_a$ , as well as the lowest MAE among all methods without test-time prompts (unsupervised at test-time). Specifically, we outperform ZoomNeXt, a supervised method published in 2024 and considered state-of-the-art, by +0.152 on  $F_{\beta}^w$  and +0.042 on  $S_a$ . Compared to previous zero-shot methods, such as LLaVA + SAM2-L

| Model | Pub. | Settings | SR |
|-|-|-|-|
| FlowI-SAM [47] | ACCV 24 | SV Transfer | 0.628 |
| FlowP-SAM [47] | ACCV 24 | SV Transfer | 0.645 |
| Motion Grouping [51] | ICCV 21 | SS Transfer | 0.484 |
| ZS-VCOS | - | ZS w/ PK | <b>0.697</b> |

Table 3. Success rate (SR) of detection success rate on MoCA-Filtered [51]. “SV” stands for supervised training, “SV” stands for self-supervised, and “ZS” stands for zero-shot. Although the previous three methods are trained on VOS datasets, they are not trained on camouflage object datasets. Our method is not trained on any VOS or camouflage datasets and resulted in the highest SR.

[53], we obtain improvements of +0.332 in  $F_{\beta}^w$  and +0.154 in  $S_a$ . Moreover, our method is only -0.098 behind in  $F_{\beta}^w$  and -0.056 in  $S_a$  compared to the test-time supervised upper bound reported in [53]. This indicates that our method is very close to this upper bound. Although our improvement in  $S_a$  is moderate, we observed that  $S_a$  might not be highly discriminative, as even masks with minimal overlap can achieve scores around 0.40.

#### 4.2.2. MoCA-Filtered

Our results for MoCA-Filtered are presented in Table 3. Our method outperforms Flow-SAM [47] and Motion Grouping [51], which are trained on non-camouflage video segmentation datasets using supervised and unsupervised approaches, respectively. We achieve a detection success rate of 0.697, compared to 0.645 for Flow-SAM and 0.484 for Motion Grouping. The improvement here is not as significant as in MoCA-Mask, which may indicate that combining SAM and optical flow, as done in FlowSAM, is already an effective approach.

### 4.3. Video-Level Results

We examined individual results for each video in the test set. Quantitative results for mIoU are presented in Table 5 in supplemental material, and qualitative results are shown in Figure 2. Both results indicate that our method succeeded in *stick\_insect\_1* and *snow\_leopard\_10*, where ZoomNeXt completely failed. Additionally, our approach successfully captured the target in *ibex*, whereas the other two methods missed it. In *arctic\_fox\_3*, our method achieved a significantly higher  $F_{\beta}^w$  score and effectively avoided stationary objects. Although our method struggled in *pygmy\_seahorse\_0*, neither ZoomNeXt nor SLT-Net performed well in this case. In other cases where other methods outperformed ours, the margin of improvement was minimal.

### 4.4. Ablation Study

For our ablation study, we designed 9 configurations, as shown in Table 2. Configuration (a) is a minimum baseline with only object detection, used to compare with prior

{7}------------------------------------------------

|  | SAM-2 Prompt | $S_\alpha$ | $E_\phi$ | mIoU |
|-|-|-|-|-|
| (a) | Box Only | <b>0.776</b> | 0.873 | 0.540 |
| (b) | Point + Box | <b>0.776</b> | <b>0.878</b> | <b>0.550</b> |

Table 4. Effects of different SAM-2 prompts

methods such as LLaVA/Shikra + SAM2 [53]. Our result ( $S_\alpha = 0.621$ ) is nearly identical to theirs ( $S_\alpha = 0.622$ ). In (b), we add bidirectional tracking to (a), which slightly improves  $S_\alpha$  by +0.022 and mIoU by +0.049. In (c), we add optical flow and mean subtraction on top of (b), leading to a significant improvement:  $S_\alpha$  increases by +0.109 and mIoU by +0.207. In (d), we introduce momentum to (c), resulting in a very small drop in  $S_\alpha$  (-0.002) but a minor gain in mIoU (+0.005). In (e), we use both optical flow and background subtraction based on camera movements, along with mean subtraction for optical flow, resulted in a slight increase compared to (d), +0.009 in  $S_\alpha$  and 0.009 in mIoU. In (f) and (g), we remove tracking entirely to assess its impact. Both show a substantial performance drop, especially in mIoU, indicating that tracking is essential. (g) includes momentum, while (f) does not. In (h), we test forward-only tracking instead of bidirectional. It performs worse than Ours (-0.029 in  $S_\alpha$  and -0.053 in mIoU), showing bidirectional tracking is more effective. Finally, we remove mean subtraction from Ours, as shown in (i), which resulted in a slight increase in  $S_\alpha$  and mIoU but a lower  $E_\phi$ . This means that subtraction has a minimum impact on performance. This might be due to the limited number of videos in the dataset featuring camera motion with relatively static objects, or because the pipeline relies more effectively on contrast rather than absolute color for object identification. Compared to other methods, our approach without mean subtraction (i) achieved the highest  $S_\alpha$  and mIoU scores. However, our full method obtained the highest  $E_\phi$ , with  $S_\alpha$  and mIoU scores close to those of (i).

Our final model includes all components: optical flow, background subtraction, mean subtraction, momentum, and bidirectional tracking. It achieves strong performance with  $S_\alpha = 0.776$ ,  $E_\phi = 0.878$ , and mIoU = 0.550.

### 4.5. Prompting Experiments

In supplementary material Section 5.2, we studied the effects of different OwlV2 prompts. Results show that naming the target category and the color of the highlight to OwlV2 gives the best detection.

We also compared the prompt types passed to SAM-2, as shown in Table 4. Using only the bounding box already yields strong performance, and adding the center-of-mass point prompt further improves  $E_\phi$  from 0.873 to 0.878 and mIoU from 0.540 to 0.550, while  $S_\alpha$  remains unchanged. We therefore use both box and point prompts in our final method.

## 5. Conclusion

We introduced ZS-VCOS, a zero-shot method for video camouflaged object segmentation, integrating optical flow, vision-language models, and SAM. Our approach significantly outperformed existing methods, increasing mIoU on the MoCA-Mask dataset from 0.273 to 0.561 and improving detection success on MoCA-Filtered from 0.628 to 0.697. Our findings highlight the potential of zero-shot pipelines for effectively handling camouflaged objects, particularly beneficial in scenarios lacking labelled data. Our modular design enables easy replacement of improved modules at any pipeline stage, enhancing overall performance.

Our method has several limitations. First, it is designed for videos containing one and only one object. In multi-object scenarios, the tracking and matching components would require modification to handle multiple object associations. Second, the approach relies on a textual description of the target object. While this is significantly less costly than collecting annotated training data, generating an accurate and unambiguous prompt can still be non-trivial in some cases. Potential solutions include incorporating few-shot object detection using example image embeddings from VLM as queries, or integrating an image-to-text captioning tool to automatically generate prompts from reference frames.

## Acknowledgement

This work was supported by NFRF GR024801 and CFI GR024473. We also thank Weather Software (<https://weasoft.com>) for providing computing credits via Google Colab.

{8}------------------------------------------------

## References

- [1] Yongqi An, Xu Zhao, Tao Yu, Haiyun Guo, Chaoyang Zhao, Ming Tang, and Jinqiao Wang. Zbs: Zero-shot background subtraction via instance-level background modeling and foreground selection. (arXiv:2303.14679), 2023. arXiv:2303.14679. 2
- [2] Pia Bideau and Erik Learned-Miller. It’s moving! a probabilistic model for causal motion segmentation in moving camera videos. (arXiv:1604.00136), 2016. arXiv:1604.00136. 2, 3, 6
- [3] Thomas Brox and Jitendra Malik. Object segmentation by long term analysis of point trajectories. In *Computer Vision – ECCV 2010*, page 282–295, Berlin, Heidelberg, 2010. Springer. 2
- [4] Keqin Chen, Zhao Zhang, Weili Zeng, Richong Zhang, Feng Zhu, and Rui Zhao. Shikra: Unleashing multimodal llm’s referential dialogue magic. (arXiv:2306.15195), 2023. arXiv:2306.15195. 4, 7
- [5] Jingchun Cheng, Yi-Hsuan Tsai, Shengjin Wang, and Ming-Hsuan Yang. Segflow: Joint learning for video object segmentation and optical flow. In *Proceedings of the IEEE International Conference on Computer Vision (ICCV)*, 2017. 2
- [6] Ming-Ming Cheng and Deng-Ping Fan. Structure-measure: A new way to evaluate foreground maps. *International Journal of Computer Vision*, 129(9):2622–2638, 2021. 6
- [7] Xuelian Cheng, Huan Xiong, Deng-Ping Fan, Yiran Zhong, Mehrtash Harandi, Tom Drummond, and Zongyuan Ge. Implicit motion handling for video camouflaged object detection. In *2022 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, pages 13854–13863, 2022. ISSN: 2575-7075. 1, 2, 3, 4, 6, 7
- [8] Guy Erez, Ron Shapira Weber, and Oren Freifeld. A deep moving-camera background model. (arXiv:2209.07923), 2022. arXiv:2209.07923. 3
- [9] Deng-Ping Fan, Cheng Gong, Yang Cao, Bo Ren, Ming-Ming Cheng, and Ali Borji. Enhanced-alignment measure for binary foreground map evaluation. page 698–704, 2018. 6
- [10] Deng-Ping Fan, Ge-Peng Ji, Guolei Sun, Ming-Ming Cheng, Jianbing Shen, and Ling Shao. Camouflaged object detection. page 2777–2787, 2020. 3, 4
- [11] Deng-Ping Fan, Ge-Peng Ji, Tao Zhou, Geng Chen, Huazhu Fu, Jianbing Shen, and Ling Shao. Pranet: Parallel reverse attention network for polyp segmentation. (arXiv:2006.11392), 2020. arXiv:2006.11392. 1
- [12] Shuyong Gao, Yu’ang Feng, Qishan Wang, Lingyi Hong, Xinyu Zhou, Liu Fei, Yan Wang, and Wenqiang Zhang. Msvcod: a large-scale multi-scene dataset for video camouflage object detection. (arXiv:2502.13859), 2025. arXiv:2502.13859. 4, 7
- [13] Shuyong Gao, Yu’ang Feng, Qishan Wang, Lingyi Hong, Xinyu Zhou, Liu Fei, Yan Wang, and Wenqiang Zhang. MSVCOd: A Large-Scale Multi-Scene Dataset for Video Camouflage Object Detection, 2025. arXiv:2502.13859. 1
- [14] Wenqi Guo, Yiyang Du, and Shan Du. Langgas: introducing language in selective zero-shot background subtraction for semi-transparent gas leak detection with a new dataset, 2025. arXiv:2503.02910. 2, 5, 6, 7
- [15] Wenjun Hui, Zhenfeng Zhu, Shuai Zheng, and Yao Zhao. Endow sam with keen eyes: temporal-spatial prompt learning for video camouflaged object detection. pages 19058–19067, 2024. 4, 7
- [16] ignatius. Calculate average intersection over union, 2018. 6
- [17] Ajay Kumar. Computer-vision-based fabric defect detection: A survey. *IEEE Transactions on Industrial Electronics*, 55(1):348–363, 2008. 1
- [18] Laksono Kurnianggoro, Wahyono, Yang Yu, Danilo Caceres Hernandez, and Kang-Hyun Jo. Online background-subtraction with motion compensation for freely moving camera. In *Intelligent Computing Theories and Application*, page 569–578, Cham, 2016. Springer International Publishing. 3
- [19] Hala Lamdouar, Charig Yang, Weidi Xie, and Andrew Zisserman. Betrayed by motion: Camouflaged object discovery via motion segmentation. (arXiv:2011.11630), 2020. arXiv:2011.11630. 3, 6
- [20] Trung-Nghia Le, Tam V. Nguyen, Zhongliang Nie, Minh-Triet Tran, and Akihiro Sugimoto. Anabranch network for camouflaged object segmentation. (arXiv:2105.09451), 2021. arXiv:2105.09451. 3, 4
- [21] Xinhao Li, Yun Liu, Guolei Sun, Min Wu, Le Zhang, and Ce Zhu. Towards open-vocabulary video semantic segmentation. (arXiv:2412.09329), 2024. arXiv:2412.09329. 3
- [22] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. (arXiv:2304.08485), 2023. arXiv:2304.08485. 4, 7
- [23] Shilong Liu, Zhaoyang Zeng, Tianhe Ren, Feng Li, Hao Zhang, Jie Yang, Qing Jiang, Chunyuan Li, Jianwei Yang, Hang Su, Jun Zhu, and Lei Zhang. Grounding dino: Marrying dino with grounded pre-training for open-set object detection. (arXiv:2303.05499), 2024. arXiv:2303.05499. 5
- [24] Bruce D. Lucas and Takeo Kanade. An iterative image registration technique with an application to stereo vision. In *Proceedings of the 7th International Joint Conference on Artificial Intelligence - Volume 2*, page 674–679, San Francisco, CA, USA, 1981. Morgan Kaufmann Publishers Inc. 2, 5
- [25] Yunqiu Lv, Jing Zhang, Yuchao Dai, Aixuan Li, Bowen Liu, Nick Barnes, and Deng-Ping Fan. Simultaneously localize, segment and rank the camouflaged objects. page 11591–11601, 2021. 3, 4
- [26] Ran Margolin, Lili Zelnik-Manor, and Ayellet Tal. How to evaluate foreground maps. In *2014 IEEE Conference on Computer Vision and Pattern Recognition*, page 248–255, Columbus, OH, USA, 2014. IEEE. 6
- [27] Muhammad Nawfal Meeran, Gokul Adethya T, and Bhanu Pratyush Mantha. Sam-pm: Enhancing video camouflaged object detection using spatio-temporal attention. (arXiv:2406.05802), 2024. arXiv:2406.05802. 4, 5, 7
- [28] Matthias Minderer, Alexey Gritsenko, and Neil Houlsby. Scaling open-vocabulary object detection. (arXiv:2306.09683), 2024. arXiv:2306.09683. 5, 1
- [29] Brian E. Moore, Chen Gao, and Raj Rao Nadakuditi. Panoramic robust pca for foreground-background separation

{9}------------------------------------------------

- on noisy, free-motion camera video. (arXiv:1712.06229), 2019. arXiv:1712.06229. 3
- [30] Peter Ochs, Jitendra Malik, and Thomas Brox. Segmentation of moving objects by long term video analysis. *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 36(6): 1187–1200, 2014. 2
- [31] Youwei Pang, Xiaoqi Zhao, Tian-Zhu Xiang, Lihe Zhang, and Huchuan Lu. Zoom in and out: A mixed-scale triplet network for camouflaged object detection. (arXiv:2203.02688), 2022. arXiv:2203.02688. 4
- [32] Youwei Pang, Xiaoqi Zhao, Tian-Zhu Xiang, Lihe Zhang, and Huchuan Lu. Zoomnext: a unified collaborative pyramid network for camouflaged object detection. *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 46(12): 9205–9220, 2024. 4, 7
- [33] Jordi Pont-Tuset, Federico Perazzi, Sergi Caelles, Pablo Arbeláez, Alex Sorkine-Hornung, and Luc Van Gool. The 2017 davis challenge on video object segmentation. (arXiv:1704.00675), 2018. arXiv:1704.00675. 2
- [34] Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang Hu, Chaitanya Ryali, Tengyu Ma, Haitham Khedr, Roman Rädle, Chloe Rolland, Laura Gustafson, Eric Mintun, Juntong Pan, Kalyan Vasudev Alwala, Nicolas Carion, Chaoyuan Wu, Ross Girshick, Piotr Dollár, and Christoph Feichtenhofer. Sam 2: Segment anything in images and videos. (arXiv:2408.00714), 2024. arXiv:2408.00714. 2, 5
- [35] Dan Jeric Arcega Rustia, Chien Erh Lin, Jui-Yung Chung, Yi-Ji Zhuang, Ju-Chun Hsu, and Ta-Te Lin. Application of an image and environmental sensor network for automated greenhouse insect pest monitoring. *Journal of Asia-Pacific Entomology*, 23(1):17–28, 2020. 1
- [36] Karen Simonyan and Andrew Zisserman. Two-stream convolutional networks for action recognition in videos. (arXiv:1406.2199), 2014. arXiv:1406.2199. 2, 5
- [37] Lv Tang and Bo Li. Evaluating sam2’s role in camouflaged object detection: from sam to sam2, 2024. arXiv:2407.21596. 4, 5, 7
- [38] Lv Tang, Peng-Tao Jiang, Zhi-Hao Shen, Hao Zhang, Jin-Wei Chen, and Bo Li. Chain of visual perception: harnessing multimodal large language models for zero-shot camouflaged object detection. In *Proceedings of the 32nd ACM International Conference on Multimedia*, pages 8805–8814, Melbourne VIC Australia, 2024. ACM. 4, 7
- [39] Zachary Teed and Jia Deng. Raft: recurrent all-pairs field transforms for optical flow. (arXiv:2003.12039), 2020. arXiv:2003.12039. 2, 5, 7
- [40] Yi-Hsuan Tsai, Ming-Hsuan Yang, and Michael J. Black. Video segmentation via object flow. In *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2016. 2
- [41] Haochen Wang, Cilin Yan, Shuai Wang, Xiaolong Jiang, Xu Tang, Yao Hu, Weidi Xie, and Efstratios Gavves. Towards open-vocabulary video instance segmentation. In *Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)*, pages 4057–4066, 2023. 3
- [42] Haochen Wang, Cilin Yan, Keyan Chen, Xiaolong Jiang, Xu Tang, Yao Hu, Guoliang Kang, Weidi Xie, and Efstratios Gavves. Ov-vis: Open-vocabulary video instance segmentation. *International Journal of Computer Vision*, 132(11): 5048–5065, 2024. 3
- [43] Jingfan Wang, Jingwei Ji, Arvind P. Ravikumar, Silvio Savarese, and Adam R. Brandt. Videogaset: Deep learning for natural gas methane leak classification using an infrared camera. *Energy*, 238:121516, 2022. 5
- [44] Zifu Wang, Maxim Berman, Amal Rannen-Triki, Philip H. S. Torr, Devis Tuia, Tinne Tuytelaars, Luc Van Gool, Jiaqian Yu, and Matthew B. Blaschke. Revisiting evaluation metrics for semantic segmentation: Optimization and evaluation of fine-grained intersection over union. (arXiv:2310.19252), 2023. arXiv:2310.19252. 6
- [45] Fengyang Xiao, Sujie Hu, Yuqi Shen, Chengyu Fang, Jinfa Huang, Chunming He, Longxiang Tang, Ziyun Yang, and Xiu Li. A survey of camouflaged object detection and beyond, 2024. arXiv:2408.14562. 1, 3
- [46] Huaxin Xiao, Jiashi Feng, Guosheng Lin, Yu Liu, and Maojun Zhang. Monet: Deep motion exploitation for video object segmentation. In *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2018. 2
- [47] Junyu Xie, Charig Yang, Weidi Xie, and Andrew Zisserman. Moving object segmentation: all you need is sam(And flow). In *Computer Vision – ACCV 2024*, pages 291–308, Singapore, 2025. Springer Nature. 2, 4, 5, 7, 1
- [48] Haofei Xu, Jing Zhang, Jianfei Cai, Hamid Rezaatoughi, and Dacheng Tao. Gmflow: Learning optical flow via global matching. (arXiv:2111.13680), 2022. arXiv:2111.13680. 2
- [49] Ning Xu, Linjie Yang, Yuchen Fan, Dingcheng Yue, Yuchen Liang, Jianchao Yang, and Thomas Huang. Youtubevos: A large-scale video object segmentation benchmark. (arXiv:1809.03327), 2018. arXiv:1809.03327. 2
- [50] Bin Yan, Martin Sundermeyer, David Joseph Tan, Huchuan Lu, and Federico Tombari. Towards real-time open-vocabulary video instance segmentation. (arXiv:2412.04434), 2024. arXiv:2412.04434. 2
- [51] Charig Yang, Hala Lamdouar, Erika Lu, Andrew Zisserman, and Weidi Xie. Self-supervised video object segmentation by motion grouping. (arXiv:2104.07658), 2021. arXiv:2104.07658. 3, 4, 5, 6, 7, 1
- [52] Shu Yang, Lu Zhang, Jinqing Qi, Huchuan Lu, Shuo Wang, and Xiaoxing Zhang. Learning motion-appearance co-attention for zero-shot video object segmentation. In *Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)*, pages 1564–1573, 2021. 2
- [53] Yuli Zhou, Guolei Sun, Yawei Li, Luca Benini, and Ender Konukoglu. When sam2 meets video camouflaged object segmentation: A comprehensive evaluation and adaptation. (arXiv:2409.18653), 2024. arXiv:2409.18653. 4, 5, 7, 8, 1
- [54] Z Zivkovic. Improved adaptive gaussian mixture model for background subtraction. In *Proceedings of the 17th International Conference on Pattern Recognition, 2004. ICPR 2004.*, page 28–31 Vol.2. IEEE, 2004. 5
- [55] Zoran Zivkovic and Ferdinand Van Der Heijden. Efficient adaptive density estimation per image pixel for the task of background subtraction. *Pattern Recognition Letters*, 27: 773–780, 2006. 5

 Rest of paper (reference and Appendix) is removed.