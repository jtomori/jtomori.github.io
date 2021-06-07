---
title: "Compiling DreamWorks OpenVDB C++ nodes for Houdini on Linux"
date: "2017-11-23"
categories: 
  - "cg"
  - "hdk"
  - "houdini"
  - "pipeline"
---

In this post I will describe a process of compiling DreamWorks OpenVDB nodes. Official DreamWorks nodes have a bit more functionality and are sometimes really useful. Even though Houdini OpenVDB nodes cover most of the functionality of the DreamWorks nodes, it might be useful to have both sets of nodes at hand. In this post I will describe how to build the nodes using existing precompiled OpenVDB library shipped with Houdini. By doing so we do not need to build the OpenVDB core (and all its dependencies) ourselves but we take can take advantage of the one coming with Houdini.

Note, that Houdini is not using the latest version of [OpenVDB](https://github.com/dreamworksanimation/openvdb). At the time of writing this post the latest OpenVDB version is 5.0.0, while Houdini 16.0.736 comes with 3.3.0. You can check your OpenVDB version in [docs](http://www.sidefx.com/docs/houdini16.0/licenses/).

The official OpenVDB repository can be found [here](https://github.com/dreamworksanimation/openvdb) and it contains some standalone utilities, tools for Maya, Python bindings, Houdini nodes etc. There is a lot of useful content, take a look :) For this example we need to [download the v3.3.0](https://github.com/dreamworksanimation/openvdb/archive/v3.3.0.zip) branch of the repository.

Once downloaded, extract the archive contents into a folder e.g. _vdb\_root_. Before starting to build the nodes we need to modify a bit CMake project to disable building of OpenVDB core and to point it to use Houdini's OpenVDB library.

To do so, modify following files: _in vdb\_root/CMakeLists.txt_ comment out line 56, it should look like this:

#INCLUDE\_DIRECTORIES ( ${OPENVDB\_TOP\_LEVEL\_DIR} )

comment out line 60, it should look like this:

#ADD\_SUBDIRECTORY ( openvdb )

in _vdb\_root/openvdb\_houdini/CMakeLists.txt_ replace "_openvdb\_shared_" with "_openvdb\_sesi_" (two times, at lines 94 and 159)

After that we need to check our compiler version. Houdini 16.0.736 was built with g++ 4.8. Run

$ g++ --version

in your system to check g++'s version. If it is 4.8 then you are fine. On my system g++ refers to version 5.4 and I need to point CMake to use g++-4.8 instead. I can do so by setting environment variables in my current shell, which will be automatically picked up by CMake.

$ export CC=/usr/bin/gcc-4.8
$ export CXX=/usr/bin/g++-4.8

The next step is to set up Houdini related environment variables in our shell, which will be picked up by OpenVDB's CMake. By doing so CMake will be able to automatically figure out where to look for header files, where to find libraries, what Houdini version we are using etc. In your shell navigate to Houdini installation directory (in my case _/opt/hfs16.0.736/_) and run

$ source houdini\_setup

After that everything should be set up, in _vdb\_root_ you can create folder _build_, change your working directory to it and then run following commands.

$ cmake \\
    -D OPENVDB\_BUILD\_HOUDINI\_SOPS=ON \\
    -D OPENVDB\_BUILD\_UNITTESTS=OFF \\
    -D CMAKE\_CXX\_FLAGS="-fPIC -std=c++11" \\
    -D CMAKE\_INSTALL\_PREFIX=./ \\
    ..

$ make -j16 && make install

_(16 refers to number of threads, set it according to your cpu)_

If you did not get any errors, then your OpenVDB Houdini nodes should be installed into the _build_ directory. The full path to the nodes is in my case this: _vdb\_root/build/houdini16.0/dso_. The last step we need to do is to tell Houdini the location of our new nodes. We could copy them into standard location, where Houdini is looking for nodes: _~/houdini16.0/dso_. However I prefer to keep them at their current location and I will set environment variable in _~/houdini16.0/houdini.env_ instead. In my case I added this line:

HOUDINI\_DSO\_PATH = "&:/home/juraj/OpenVDB\_guide/openvdb-3.3.0/build/houdini16.0/dso"

(It is important to use the _&:_ symbol, which means to include all the default locations and then to append our new one. Without it we would lost all standard Houdini nodes :) )

Happy Houdining, if you have any suggestions/errors feel free to contact me :)

<!-- Markdeep: --><style class="fallback">body{visibility:hidden;white-space:pre;font-family:monospace}</style><script src="../markdeep.min.js" charset="utf-8"></script><script>window.alreadyProcessedMarkdeep||(document.body.style.visibility="visible")</script>

