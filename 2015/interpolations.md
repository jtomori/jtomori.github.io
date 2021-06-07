---
title: "Interpolations"
date: "2015-11-12"
categories: 
  - "cg"
  - "houdini"
---

I want to get a little bit more into coding so I am making up small exercices. I want to implement simple things first and hopefully later I will manage to do something bigger :)

For a long time I had this idea of playing with interpolations. They are very often used in CG so why not? Good resources on interpolation methods are [here](http://paulbourke.net/miscellaneous/interpolation/) and [here](http://freespace.virgin.net/hugo.elias/models/m_perlin.htm).

Interpolation was also important to get this tool working. You can find project file in video description. This tool uses linear interpolation because It worked fine and was lazy to do it with 3D cubic :). But similar result can be achieved by smoothing vector field that is used for deformation. I am aslo planning to write detailed blog post about this tool. \[embed\]https://vimeo.com/139814928\[/embed\] First image show a result of VEX code to generate points between red dots.

\[caption id="attachment\_14" align="aligncenter" width="496"\]![interpolations_dot](https://jurajtomori.files.wordpress.com/2015/11/interpolations_dot.png?w=300) comparing various interpolations\[/caption\]

In second image I have cached out to disk simple animation of geometry. When I am loading geometry back subframe data is lost. Subframe data may be important when dealing with motion blur, retiming or using geometry in simulation (e.g. collisions). Interpolation can be used to generate those subframe data.

\[caption id="attachment\_15" align="aligncenter" width="504"\]![interpolations](https://jurajtomori.files.wordpress.com/2015/11/interpolations_sphere.png?w=300) red spheres are on integer frames\[/caption\]

Interesting is hermite interpolation which has two parameters: tension and bias. Both should be in <-1 ; 1> range but I cranked them a bit to show their effect.

You can download project file [here](https://drive.google.com/file/d/0B0hpa2flKntodFp0RUVBRTJsUGM/view?usp=sharing).

I am planning to break down some interesting projects I have been working on. You can check videos on my [vimeo channel](https://vimeo.com/jurajtomori). Hope somebody will find it useful / informative and see you in my next post :)

<!-- Markdeep: --><style class="fallback">body{visibility:hidden;white-space:pre;font-family:monospace}</style><script src="../markdeep.min.js" charset="utf-8"></script><script>window.alreadyProcessedMarkdeep||(document.body.style.visibility="visible")</script>

