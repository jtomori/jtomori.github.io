---
title: "Houdini 2 Open3D | First tests"
date: "2019-05-09"
categories: 
  - "cg"
  - "houdini"
  - "photogrammetry"
  - "pipeline"
---

I would like to share the first test of a fun project I recently started working on in my spare time - [Open3D](http://www.open3d.org/) to Houdini integration.

I built Houdini wrappers around Open3D functionality, which enable me to load point clouds, pre-process (downsample, estimate normals, compute FPFH feature) and perform Global and ICP registration on them to align them tightly:

https://www.youtube.com/watch?v=vMOuM1C-AJc

This already seems quite versatile when combined with the Houdini toolset. Combined with [GameDev](https://www.sidefx.com/tutorials/game-development-toolset-overview/) and [Alice Vision](https://www.sidefx.com/tutorials/alicevision-plugin/) tools it can result in a powerful and automatic photogrammetry pipeline - [something I like to explore :)](https://jurajtomori.wordpress.com/category/photogrammetry/).

I bidirectionally translate Houdini and Open3D geometry, so the Open3D operations can be seamlessly combined with Houdini SOPs. This doesn't seem to be the case in the [Reality Capture](https://www.sidefx.com/tutorials/reality-capture-plugin-open-beta/) or [Alice Vision](https://www.sidefx.com/tutorials/alicevision-plugin/) plugins, which don't enable Houdini to modify the geometry.

The integration is in early version and has some issues. I tested it only on a Linux so far. I will open-source it after I fix the problems and write some info on setting it up.

Thanks for reading :)
