---
title: "Artistic style transfer setup guide"
date: "2017-07-18"
categories: 
  - "pipeline"
---

In this post I will explain how to set up a linux environment for running style transfer implementations from GitHub repositories. I assume that you have a Nvidia GPU, linux distribution and a working knowledge of linux. If you get into any troubles, just drop me a line. It was done as a part of my studies at Filmakademie Baden-Wuerttemberg.

There are many implementations on a GitHub and here I will show how to make the three of them working (which I had previously tested and used):

- [https://github.com/anishathalye/neural-style](https://github.com/anishathalye/neural-style)
- [https://github.com/yusuketomoto/chainer-fast-neuralstyle/tree/resize-conv](https://github.com/yusuketomoto/chainer-fast-neuralstyle/tree/resize-conv)
- [https://github.com/lengstrom/fast-style-transfer](https://github.com/lengstrom/fast-style-transfer)

Here you can check some tests and results which I did with those three implementations.

- ![mtx2_low](images/mtx2_low.jpg) [full image](https://jurajtomori.files.wordpress.com/2017/07/mtx2_low.jpg)
    - In the columns different implementations are used (in the same order as in the list above), the rows are using different styles.
- ![mtx_low](images/mtx_low.jpg)[full image](https://jurajtomori.files.wordpress.com/2017/07/mtx_low.jpg)
    - I also tested the last implementation with a CG rendering, here you can see comparison of different rendering output vs different styles (renderings by _Kiana Naghshineh_)

**UPDATE:** Check my [more recent post](https://jurajtomori.wordpress.com/2019/01/30/style-transfer-docker-images/) about much easier setup process for all of this.

At the end I used the last implementation with a video. I converted input video into a image sequence and with the help of a simple bash script I have run it on the each frame. I also added a bit of motion blur in Nuke on top of it, to make it seem smoother in motion.

- [https://www.youtube.com/watch?v=7csymcO4MAA](https://www.youtube.com/watch?v=7csymcO4MAA)
- [https://vimeo.com/223502033](https://vimeo.com/223502033)
- [https://vimeo.com/222518380](https://vimeo.com/222518380)

Each implementation is based on a different papers and have slightly different options and results. Feel free to try them out and use the one which works best for you. Also the requirements for running them are almost the same, so once the one is running it is easy to try out different implementations.

Also note that I am not a machine learning expert and I have not coded the logic behind it, I just played with the existing code to see what results it can output. More details on how it works and which research papers it is based on can be found on GitHub repositories.

Those implementations can be split into two categories, the first implementation is being trained for each frame. It takes some time and lots of GPU memory, it cannot handle high resolution images. The other two implementations are being trained for a specific style only once (takes more time though), but afterwards it is very fast (almost realtime) to apply those pre-trained models on any images (even high resolution), which makes it ideal for style transferring videos.

## Installing the requirements.

All those implementations are GPU based which makes them so damn fast. In order to utilize your GPU on linux you need at first to have Nvidia driver installed. Installing it is out of the scope of this post, but a bit of googling will show you many setup guides based on your linux distribution. After your driver is working you can move to the next steps :) (you should be able to run _**nvidia-settings**_ and see correct information there)

The next thing you need to set up is _CUDA_ and _cuDNN_ from _Nvidia_.

### CUDA

Download and install CUDA from [here](https://developer.nvidia.com/cuda-downloads). (select installer depending on your distribution) And run it, you may also need to check [installation guide](http://docs.nvidia.com/cuda/pdf/CUDA_Installation_Guide_Linux.pdf) or [this](https://askubuntu.com/a/874421) if you are Ubuntu based. Installation of CUDA might differ on different distributions therefore it makes no sense it include it into this post. After successful installation you should be able to run _**nvcc --version**_

### cuDNN

Register a Nvidia developer accound and [download](https://developer.nvidia.com/cudnn) cuDNN (some version might have problems with running in TensorFlow, for me 5.1.10 worked fine, but google a bit to find out more) Check where your CUDA installation is. For the installation from the repository it is _/usr/lib/_... and _/usr/include_. Otherwise, it will be _/usr/local/cuda/_ or _/usr/local/cuda-_. You can check it with _**which nvcc**_ or _**ldconfig -p | grep cuda**_ Copy the files: (commands which I used on my system)

> cd folder/extracted/contents
> sudo cp -P include/cudnn.h /usr/local/cuda-8.0/include/
> sudo cp-P lib64/libcudnn\* /usr/local/cuda-8.0/lib64/
> sudo chmod a+r /usr/local/cuda-8.0/lib64/libcudnn\*

[(source)](https://askubuntu.com/a/767270)

### Python

Now we should be able to move on setting up Python modules. All of those style transfer implementations are based on Python. They require those Python packages:

- TensorFlow
- NumPy
- SciPy
- Pillow
- Chainer

Installing those on linux is simple with a bit of help from pip. Create a text document _requirements.txt_

> tensorflow-gpu >= 1.0
> numpy
> scipy
> Pillow
> chainer

Then run _**pip install -r requirements.txt**_ If you are behind a proxy, you need to alter the command a bit: _**pip install -r requirements.txt --proxy [http://user@server.com:port](http://user@quake.medianet.animationsinstitut.de:3128)**_ (replace user, server and port based on the place where you are) And you might need to run it with user with root privileges (_**sudo pip -r**_ ...)

### Data

Now your system is prepared to do some heavy machine learning, but we still need some data related to training, download those things:

- [http://www.vlfeat.org/matconvnet/models/beta16/imagenet-vgg-verydeep-19.mat](http://www.vlfeat.org/matconvnet/models/beta16/imagenet-vgg-verydeep-19.mat)
- [http://www.robots.ox.ac.uk/~vgg/software/very\_deep/caffe/VGG\_ILSVRC\_16\_layers.caffemodel](http://www.robots.ox.ac.uk/%7Evgg/software/very_deep/caffe/VGG_ILSVRC_16_layers.caffemodel)
- [http://msvocds.blob.core.windows.net/coco2014/train2014.zip](http://msvocds.blob.core.windows.net/coco2014/train2014.zip)

## Setting up implementations

Now we should have almost everything set up, we can move on cloning the actual implementations from GitHub. The previous part is just one-time setup process, getting new implementations will be much easier process.

> git clone https://github.com/anishathalye/neural-style
> git clone https://github.com/yusuketomoto/chainer-fast-neuralstyle.git -b resize-conv
> git clone https://github.com/lengstrom/fast-style-transfer.git

Afterwards, move previously downloaded _VGG\_ILSVRC\_16\_layers.caffemodel_ into _chainer-fast-neuralstyle_ directory, then run _**python create\_chainer\_model.py**_ Now you should have everything prepared, it is up to you to take different styles and experiment with them. Depending on your GPU it will take some time, but the results are worth it. For detailed usage and information on different options check with repositories on GitHub, I am attaching here some commands which worked in my case (you might need to alter them based on file locations, etc.)

## Running artistic style transfer

### anishathalye/neural-style

This does not require pre-training style, you can directly run this command, where _me\_1k.jpg_ is input image, _style8.png_ is style to be applied, _\--output_ specifies well, otuput :) and _\--checkpoint-output_ creates intermediate outputs after each 100 iterations to check it in progress and terminate earlier if the result is good enough, _\--network_ needs to be pointing to _imagenet-vgg-verydeep-19.mat_ which we previously downloaded

> python neural\_style.py --content ../me\_1k.jpg --styles ../styles/style8.png --output ../out/anishathalye/me\_8.jpg --iterations 2000 --checkpoint-output ../checkpoints/me\_8\_chk\_%s.jpg --checkpoint-iterations 100 --network ../imagenet-vgg-verydeep-19.mat

### yusuketomoto/chainer-fast-neuralstyle

At first we need to train a model based on _style1.jpg_ and _train2014_ dataset (previously downloaded), _\-g_ specifies which GPU device to use:

> python train.py -s ../styles/style1.jpg -d ../train2014/ -g 0

this will output model into _models_ directory, now we are prepared to transfer style on _me\_1k.jpg_ image with this command, _\-o_ is for the output directory:

> python generate.py ../me\_1k.jpg -m models/style1.model -o ../out/chainer/me\_1.jpg -g 0

you might want to test it at first with included pre-trained styles coming in models directory

I also created a simple Bash script for transforming image sequence, put it into the current directory and run without any parameters for instructions on how to run it.

> #!/usr/bin/env bash
> 
> text="usage: ./generate\_video.sh \\"path\_to\_src\_frames\\" \\"path\_to\_style\\" \\"path\_to\_output\_dir\\"\\nfor example:\\n./generate\_video.sh \\"../video/vid\_1/\\\*.png\\" \\"models/composition.model\\" \\"../out/chainer/video/vid\_1/\\"\\n\\n"
> echo -e $text
> 
> if \[ $# != 3 \]
>    then
>    echo "not 3 parameters specified, terminating"
>    exit
> fi
> 
> for i in $1;
> do
>    file=\`basename $i\`
>    cmd="python generate.py $i -m $2 -o $3/$file -g 0"
>    echo $cmd
>    ${cmd}
> done

 

### lengstrom/fast-style-transfer

At first you need to pre-train a model yourself, or you can use some published models from [here](https://drive.google.com/drive/folders/0B9jhaT37ydSyRk9UX0wwX3BpMzQ), just put them into the _models_ directory

this command will train a network based on _jf.jpg_ style reference, will output it into _ch\_jf_ directory, will use _test.jpg_ as a testing image (for in-progress checking, which will be put into test directory), will use _train2014_ dataset and _imagenet-vgg-verydeep-19.mat_ (both previously downloaded):

> python style.py --style ../styles/jf.jpg --checkpoint-dir ch\_jf/ --test ../video/jf/test.jpg --test-dir test/ --train-path ../train2014 --vgg-path ../imagenet-vgg-verydeep-19.mat

to apply a style to _in.jpg_ we can use this command, which will output _out\_wreck.jpg_ file:

> python evaluate.py --checkpoint models/wreck.ckpt --in-path ../src/in.jpg --out-path ../out/out\_wreck.jpg

for downloaded model, or this for our own trained model:

> python evaluate.py --checkpoint ch\_jf --in-path ../src/in.jpg --out-path ../out/out\_jf.jpg

I also created a simple Bash script for transforming image sequence, put it into the current directory and run without any parameters for instructions on how to run it.

> #!/usr/bin/env bash
> 
> text="usage: ./generate\_video.sh \\"path\_to\_src\_frames\\" \\"path\_to\_style\\" \\"path\_to\_output\_dir\\"\\nfor example:\\n./generate\_video.sh \\"../video/vid\_1/\\\*.png\\" \\"models/composition.model\\" \\"../out/chainer/video/vid\_1/\\"\\n\\n"
> echo -e $text
> 
> if \[ $# != 3 \]
>    then
>    echo "not 3 parameters specified, terminating"
>    exit
> fi
> 
> for i in $1;
> do
>    file=\`basename $i\`
>    cmd="python evaluate.py --in-path $i --checkpoint $2 --out-path $3/$file"
>    echo $cmd
>    ${cmd}
> done

 

That should be all, for more settings and how to tune parameters to get the best results check the descriptions on the GitHub repos. Have a fun, and if you find any mistakes / suggestions for improvements, just let me know.

<!-- Markdeep: --><style class="fallback">body{visibility:hidden;white-space:pre;font-family:monospace}</style><script src="../markdeep.min.js" charset="utf-8"></script><script>window.alreadyProcessedMarkdeep||(document.body.style.visibility="visible")</script>

