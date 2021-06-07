---
title: "Compiling C++ OpenVDB Hello World example using Houdini libraries on Linux"
date: "2017-11-23"
categories: 
  - "cg"
  - "hdk"
  - "houdini"
  - "pipeline"
---

In this post I will describe a process of compiling Hello World example from OpenVDB library. I will take the [first](http://www.openvdb.org/documentation/doxygen/codeExamples.html#sHelloWorld) example from OpenVDB Cookbook. However instead of building the whole OpenVDB library I will take advantage of precompiled OpenVDB library shipping with Houdini. In this post I will assume that you have at least very basic understanding of compiling process.

Note, that Houdini does not have the latest version of [OpenVDB](https://github.com/dreamworksanimation/openvdb). At the time of writing this post the latest OpenVDB version is 5.0.0, while Houdini 16.0.736 comes with 3.3.0. You can check your OpenVDB version in [docs](http://www.sidefx.com/docs/houdini16.0/licenses/). OpenVDB version is not important for this simple example, so 3.3.0 will be fine, but compiling code using newer OpenVDB features will not work.

The first step is to check which g++ version is used in your system. Run in terminal:

$ g++ --version

It is important to use the same version of a compiler as the one Houdini was built with. In my case I have Ubuntu with g++ 5.4.0 and I have installed this Houdini version: _houdini-16.0.736-linux\_x86\_64\_gcc4.8_. This means trouble and the Hello World example will not compile with g++ 5.4.0. If your system is using g++ 4.8 then you are fine, if not then use your package manager to install required g++ (_sudo apt install g++-4.8_) and in following commands use _g++-4.8_ instead of _g++_.

Once your compiler is installed, create _hello\_world.cpp_ with the code from OpenVDB Cookbook.

There are more ways of compiling _hello\_world.cpp_, I will show two of them. Since we will be using Houdini libraries and headers we need to make our system environment aware of them. Fortunately there is an environment setup script coming with Houdini. It can be found in Houdini installation directory, in my case it is _/opt/hfs16.0.736/_. Change your working directory to it and run in terminal:

$ source houdini\_setup

You should get message like this: _The Houdini 16.0.736 environment has been initialized._ This script initializes couple of variables which we will use and also adds Houdini binaries to _PATH_ environment variable.

#### Compiling method one.

Houdini is coming with neat utility called _hcustom_. It is a tool made for simplifying process of compiling Houdini plugins (C++ libraries). However it is also capable of compiling standalone applications which is our case. You might need to install csh in order to use it in your system (_sudo apt install csh_). _Hcustom_ has some neat options and can also take custom compiling flags. We need to add _\-DOPENVDB\_3\_ABI\_COMPATIBLE_ in order to run the program (Houdini's OpenVDB library was built with _abi=3_) Execute following commands.

$ export HCUSTOM\_CFLAGS="-DOPENVDB\_3\_ABI\_COMPATIBLE"
$ hcustom -i . -s -e -l tbb -l Half -l openvdb\_sesi ./hello\_world.cpp

Flag _\-s_ means to build a standalone application instead of building a library, _\-i_ points to target installation directory, _\-e_ means to show which commands are actually being executed, _\-l_ is pointing to the libraries required.

Also note, that hcustom by default uses _g++_ command, so you might need to point _g++_ in your environment to the correct version (_g++-4.8_).

#### Compiling method two.

$ g++ -DOPENVDB\_3\_ABI\_COMPATIBLE -c -std=c++11 -isystem $HT/include -o hello\_world.o hello\_world.cpp
$ g++ hello\_world.o -L $HDSO -ltbb -lHalf -lopenvdb\_sesi -o ./hello\_world -Wl,-rpath,$HDSO

 

After that you should be able to run _./hello\_world_ and get following result.

Testing random access:
Grid\[1000, -200000000, 30000000\] = 1
Grid\[1000, 200000000, -30000000\] = 0
Testing sequential access:
Grid\[-2147483648, -2147483648, -2147483648\] = 3
Grid\[1000, -200000000, 30000000\] = 1
Grid\[1000, 200000000, -30000000\] = 2
Grid\[2147483647, 2147483647, 2147483647\] = 4

 

Hope everything works well, if you have any suggestions/errors feel free to contact me :)
