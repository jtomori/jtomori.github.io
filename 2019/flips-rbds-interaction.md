---
title: "FLIPs - RBDs interaction"
date: "2019-03-23"
categories: 
  - "cg"
  - "fx"
  - "houdini"
---

In this post I will show a simple technique for FLIPs and RBDs interaction. Like in this example:

https://youtu.be/7WegEBqVqB4

I decided to give it a try after talking to great FX TD [Adam Guzowski](https://www.linkedin.com/in/adam-guzowski-ba2049146/). The task was like this: doing a setup where water would fracture RBD objects, would break RBD constraints and RBD objects would be pre-fractured based on the expected water flow.

Firstly disclaimer: this is not a true two-way coupling between RBDs and FLIPs. It is rather a quick hack that works well in this case. For more accurate results you should use unpacked RBDs workflow which would give you accurate interaction between the two (e.g. RBDs floating in FLIPs based on its density), but this workflow would be slower and not needed in this kind of scenario.

You can download the project file with comments which are explaining the workflow [here](https://drive.google.com/open?id=1nV5116-OrkXttR0CJRcBtcVZgBFc2L8a) (there are two versions doing the same thing, with VEX and VOPs). I will go through the process bellow and will include some videos illustrating it.

Because the RBDs should be pre-fractured based on the water flow the workflow is split into two simulations.

 

## The first simulation

 

The first simulation is low resolution and includes a simple water stream colliding with static colliders:

https://www.youtube.com/watch?v=eknrl\_IiF40

I use this collision for determining which areas of colliders are hit by water.

First I isloate FLIP particles which are in close proximity to colliders. I do it by sampling collision SDF field and getting distance values. I delete all particles which are too far apart from colliders - they didn't hit the colliders.

In the next step I isolate particles which have high impact on colliders - they are in high pressure areas. You can imagine it as particles slowly falling on colliders vs particles hitting colliders with full force. I want to keep only the latter as they should produce more impact on the colliders. I do it by exporting pressure field from DOP simulation. You can go to the first DOP simulation and visualize the pressure field in _flipfluidobject_ node. It will show areas with high pressure which seems like what I could use to determine realistic fracturing. In the following video you can see pressure visualization (pink fog volume) without simulated particles:

https://www.youtube.com/watch?v=eqgdmupy9ww

After that I collect all the particles during the course of the first simulation. I want to have them all, so I merge them together in Solver SOP and use Timeshift SOP to keep only the last frame. Next I add a bit of noise to them and reduce their count. You could also merge in your own fracture centers for more control. You can see how collision points accumulate in the video:

https://www.youtube.com/watch?v=KTPED2Oew2Y

Now I have good fracture points, so I fracture my colliders and prepare packed RBD pieces and constraints for the second simulation. I deactivate the bottom parts of the colliders so that they are not affected by the water.

 

## The second simulation

 

Now I can go on the next simulation which can be high-res and have more details needed for the shot. When playing with packed RBDs and FLIPs interaction it seems that one-way RBDs affecting FLIPs seems to be stable and to produce nice collisions. So I have half of the job done :)

https://www.youtube.com/watch?v=01dFO8P4fls

To get FLIPs influence RBDs I sample FLIP velocity field at RBD pieces and apply the velocity (fraction of it) to RBDs. This is a cheap interaction and not very accurate but I found it to give fine results so I went with it. You can see velocity applied to RBDs without any constraints in this video:

https://www.youtube.com/watch?v=j\_l5wDkKjAo

The next part needs to tackle constraints breaking. Applying velocity to RBDs doesn't have impact on constraints. No matter how high the velocity is, the constraints won't break. But I can break them manually. I can do it in similar way as I isolated colliding particles - by pressure field from FLIP simulation. I do it in SOP Solver DOP plugged into Constraint Network DOP (which sets RBD constraints). In the Solver I import pressure field from FLIP sim and sample it on constraint points. I set a threshold for killing points in high pressure areas.

That's it, the base setup is done :). My result is not very impressive but it is an example for showing the concept behind it. For the actual shot it would need lots of more work to include secondary elements for the simulation to be more realistic.

Happy simming.
