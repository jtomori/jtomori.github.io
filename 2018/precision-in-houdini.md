---
title: "Precision in Houdini"
date: "2018-11-24"
categories: 
  - "cg"
  - "houdini"
---

In my recent project in Houdini I was often hitting precision limits of 32-bit floating point numbers. This led me to figuring out what number precisions are used in Houdini and how can they be accessed.

In this post I will take a look at various contexts of Houdini and will mention floats, but the situation for integers should be the same.

Currently it looks that single precision (32-bit) floating point numbers are used in most operations and transferring data between nodes often happens in this format too. However this situation seems to be likely changed in the future releases of Houdini.

## Contexts

 

### Attributes

Houdini supports attributes with multiple precisions. They can be created with **Attribute Create SOP** and it can be set in **Precision** parameter, which can be set to 8, 16, 32 and 64 bits. There is also a **Attribute Cast SOP**, which can cast one type into another. That being said most nodes work with single precision and if input attribute has higher precision, it will be silently downcasted to single float.

### VEX

As for VEX, [only 32 bit attributes](http://www.sidefx.com/docs/houdini17.0/vex/lang#data-types) and types are supported in most contexts. However with Houdini 17 release a [64 bit support was added](http://www.sidefx.com/docs/houdini17.0/news/17/vex.html#vex). That looks like great news, but it is only in case of CHOPs context so far. So reading a 64 bit attribute will be silently downcasted to 32 bits too.

### Parameters

Parameters/channels with expressions [seem to work](https://www.sidefx.com/forum/topic/43740/#post-196004) natively in double precision (64 bits). That is a nice feature and precision can be preserved when using VEX in CHOPs, or when doing the logic with use of expression functions. However for some more complex tasks this might not be the cleanest way of doing it. Long expressions can get messy, are hard to debug and data can easily get downcasted by some nodes which do not support it.

### Python

Python is able to read parameter expressions in 64 bits and floats in Python [are stored internally in 64 bits](https://docs.python.org/2/tutorial/floatingpoint.html). What is a bit pity is that I didn't find a way to read double precision float attributes, they are silently downcast to single precision as you can see in the output. So you can do your logic inside of Python in double floats, but your inputs and outputs will have limited precision of single floats.

### OpenCL

OpenCL [supports natively](https://www.khronos.org/registry/OpenCL/sdk/1.0/docs/man/xhtml/scalarDataTypes.html) half, single and double precisions (16, 32, 64 bits respectively). Half and double precision need to have [extensions enabled](https://www.khronos.org/registry/OpenCL/sdk/1.0/docs/man/xhtml/) with pragma directives. So within OpenCL you are free to use double precision, but it has one caveat - Houdini can bind only single precision float attributes and parameters into OpenCL. So your input and output data from OpenCL node will be in single floats, but doing the calculations in doubles in OpenCL can be sometimes useful too.

 

## Technique

 

For determining the precision I used a simple way: printing result of 1/3 into the console. I did it in various contexts to see what is available.

Cooking the [attached scene](https://drive.google.com/open?id=1Egw7R7f0VxTX56Yb1Kk0jPp85IqdhMgM) will produce this output:

VEX
float:  0.3333333432674407958984375000000000000000000000000000000000000000000000
attr32: 0.3333333432674407958984375000000000000000000000000000000000000000000000
attr64: 0.3333333432674407958984375000000000000000000000000000000000000000000000

Parameter expressions
param:  0.33333333333333331
attr32: 0.3333333432674408
attr64: 0.3333333432674408

Python
param:  0.3333333333333333148296162562473909929394721984863281250000000000000000
attr32: 0.3333333432674407958984375000000000000000000000000000000000000000000000
attr64: 0.3333333432674407958984375000000000000000000000000000000000000000000000

OpenCL
parm:   0.3333333432674407958984375000000000000000000000000000000000000000000000
attr32: 0.3333333432674407958984375000000000000000000000000000000000000000000000
attr64: 0.0000000000000000000000000000000000000000000000000000000000000000000000

OpenCL types
half:   0.3332519531250000000000000000000000000000000000000000000000000000000000
float:  0.3333333432674407958984375000000000000000000000000000000000000000000000
double: 0.3333333333333333148296162562473909929394721984863281250000000000000000

As you can see single floats can represent 1/3 number accurately within 7 digits and doubles with 16 digits.

 

## What's next?

 

So this is the current situation. If you need more precision you will need to do your logic in Python or OpenCL languages with the limitation of being able to input/output only single float attributes. Expressions can be fine too for simple operations. Those limitations seem to make it impossible to pass double float values between the nodes as attributes.

If higher precision is needed in VEX, then you need to resort to emulating doubles by storing one number in two variables, but this will require more complex setups and custom functions for performing math operations on them. [(src1)](https://hal.archives-ouvertes.fr/file/index/docid/63356/filename/float-float.pdf) [(src2)](http://andrewthall.org/papers/df64_qf128.pdf)

However with the latest release adding support for 64 bits in CHOPs we can hope that 64 bit support will be added into other areas of Houdini in the following versions :)

Hope you will find this summary helpful. If you will find any mistakes or will think of any improvements, please let me know :)
