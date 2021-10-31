# Neural network navigation with omnidirectional images
I use this repo as a convenient way of storing and describing my progress in completing my thesis.

### Resources available at the beginning:
1. Articles about vision-based navigation and neural networks.
2. Omnidirectional sensor documentation.
3. Existing [LabBot driver](https://github.com/PUTvision/ROS-labbot) for ROS Melodic.

### Roadmap:
1. [Analysis of the articles about navigation based on vision data.](#system-architecture)
2. Choosing system architecture that contains neural network.
3. Preparing dataset and carrying out the learning process. 
4. Implementing this architecture on real robot (Labbot).
5. Documenting experiments and its results.

 ### Technologies I use:
- Google Colab for training neural nets, so I don't have to burn my poor laptop
- CVAT for marking image masks
- Linux (Ubuntu 20.04), simple Bash scripting
- Python and its frameworks and libraries: TensorFlow 2, OpenCV, numpy, [tf-semantic-segmentation](https://github.com/baudcode/tf-semantic-segmentation), [albumentations](https://github.com/albumentations-team/albumentations)
- ROS Melodic

### LabBot robot

### System architecture
Thesis is all about navigation and avoiding obstacles, so one of the main tasks is allowing our robot to actually recognize them before doing some avoiding-related stuff. Obstacle detection can be implemented in many ways, such as using typical YOLO or R-CNN detector, however choosing this path generates a huge drawback (which, in my opinion, makes this approach kinda dumb - in my specific case, of course) - such models can recognize only objects that were shown to them during training process. Let's assume, that we put something in front of the working robot, that its model sees this object a very first time. There's possibility, that our robot will simply go straight, it won't care about any unknown stuff and... cause collision.
That's why I've given my attention to a way more universal solution - binary semantic segmentation.
(obraz jakis)
I'm still a beginner in machine learning, so I don't want to do some fancy overcomplicated stuff. My main priority is simplicity, therefore I want my neural network to have two classes: free space and everything else.
1. [Deep Learning based Background Subtraction: A Systematic Survey](https://www.researchgate.net/publication/341049745_Deep_Learning_based_Background_Subtraction_A_Systematic_Survey/link/5f040841299bf1881607d9a5/download)
2. [Where to drive: free space detection with one fisheye camera](https://arxiv.org/abs/2011.05822)
These articles were kinda helpful. 





Model used in the project: ERFnet based on [this]() repository.
