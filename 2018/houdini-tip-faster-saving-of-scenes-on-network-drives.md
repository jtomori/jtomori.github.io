---
title: "Houdini tip | Faster saving of scenes on network drives"
date: "2018-01-15"
categories: 
  - "houdini"
  - "pipeline"
---

In this short post I will show how to speed up saving of scenes.

When saving large Houdini project files, especially with locked FBX data in nodes, it might take up to couple of minutes to save a scene on a network location. It is really annoying when whole Houdini session freezes and an artist has to wait till everything is written down to the disk. It also discourages artists from doing often incremental saves which might lead to loss of work.

Fortunately Houdini has a way to change this behavior - by enabling **HOUDINI\_BUFFEREDSAVE** environment variable. (More about this topic [here](https://jurajtomori.wordpress.com/2018/01/15/houdini-tip-taking-advantage-of-environment-variables/)) Simply setting this value to 1 will make saving of your scenes much faster and less annoying.

On windows add this line to your starting script:

set "HOUDINI\_BUFFEREDSAVE=1"

On linux:

export HOUDINI\_BUFFEREDSAVE=1

I am not aware of any disadvantages of using this option so I am not sure why so useful option is disabled by default. Make sure to include it in all your setups.

Happy saving :)
