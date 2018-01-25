# Yolo-v2 running on TX2 with ROS and training tutorial

## Getting Started
Download the ROS package from this repository. If you don’t need to run on ROS, you can find the regular version on https://github.com/pjreddie/darknet, which can be run on Linux or Windows.

### Building Environment
* Linux 16.04
* NVIDIA GPU with CUDA 8.0
* OpenCV 3.x or OpenCV 2.4.13
* ROS Kinetic

### Installing
You can find the make list in side the “darknet_ros” folder, which is called CMakeLists.txt. To install YOLO, you have to check your GPU compute capacity. If it’s not matched with the default parameters, you can add another line in the CUDA_NVCC_FLAGS with your computer capacity. For example:
```
-gencode arch=compute_62,code=sm_62
```
To install YOLO on ros, copy the “darknet_ros” folder you just downloaded to the “src” folder inside your ros workspace, and compile it on ROS. 

## How to run

### Prerequisites
In order to run the detection, you need to get the weight file and the cfg file prepared.
The cfg file is the configuration file, which helps setting up the training and detection neural network. Darknet provides some cfg examples, which are included in this directory:
/darknet_ros/darknet_ros/yolo_network_config/cfg/
The weight file is the model you need to train before the detection. Darknet provides some pre-trained weights. You can run this to download the weights:
```
wget http://pjreddie.com/media/files/yolo.weights
```
In order to download other weights, you may change “yolo.weights” in the link to other weights, such as tiny-yolo.weights or yolo-voc.weights.
After getting the weights file, you need to copy them into this folder: /darknet_ros/darknet_ros/yolo_network_config/weights/


### Running on ROS
Open the terminal, and go into the launch folder inside the darknet_ros folder. Enter the following command:
```
$ roslaunch darknet_ros.launch
```

## Training your own model
The Training process can not work on ROS. You have to use the original darknet version to run that. As it runs very slow, it’s necessary to train with GPU. Or you can train it on BU ssh, which would much faster than running on your own machine.

### Prepare the image dataset and labels
After collecting your image set, you need to draw the bounding boxes of objects in the images. There is a very convenient label tool to get the bounding boxes. You can download from here:
```
git clone https://github.com/puzzledqs/BBox-Label-Tool
```
The result labels are not in the desired format. In YOLO training, you have to use absolute width and height. In the robot_data_convert folder, you can find a python script “transfer.py”, which can help you transferring the labels. 
Before training, you need to create a folder “images”, which contains all your image data. And also create a folder “labels”, which contains all you labels. In addition, the image folder and the label folder have to be under the same directory.
Next, you need to build a train.txt and a test.txt, which split the dataset to training set and test set. In these txt, you need to include the images directories. For example:
```
\images\m1.jpg
\images\m2.jpg
```
You can copy the txt to the same directory with the image folder.

### Prepare the cfg file and weight
You can download the pre-trained weight from here: http://pjreddie.com/media/files/darknet19_448.conv.23 Copy it to the same directory with the image folder. 
In order to create your own cfg file, you could take the yolo-voc.cfg as an example. There are some parameters you need to change.
* change the batch line [`batch=64`]
* change subdivisions line [`subdivisions=32`]
* change the classes to your object numbers under [`[region]`]
* in the last convolutional layer, change the filters to (classes + 5)*5. For example, if your classes = 5, then filters=50.
* The learning_rate is set to be 0.001 by default. However, if your find your loss is always too high, you could consider to set the learning_rate to 0.0005.
* The width and height are set to 416 by default. If your objects are too small to detect, you could consider make it larger. It can be set as any value multiply of 32.
Copy your cfg file inside you cfg folder.

### Prepare data and names
In the data folder, you can find a file called “voc.names”. Create a name file, which contains all your object names. In the cfg folder, you can find a file called “voc.data”. Create a data file, which contains object classes, train directory, test directory, names, backup.

### Start training
With all the files ready, you can train it using this code:
```
./darknet detector train cfg/obj.data cfg/yolo-obj.cfg darknet19_448.conv.23
```
The training result would be saved in the backup folder. 
