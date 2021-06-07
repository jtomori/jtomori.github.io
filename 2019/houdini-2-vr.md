---
title: "Houdini 2 VR"
date: "2019-03-23"
categories: 
  - "cg"
  - "houdini"
  - "pipeline"
  - "rendering"
---

Hello, I would like to share with you a tool I have been developing lately - [Houdini 2 VR](https://github.com/jtomori/houdini2vr).

Currently Houdini doesn't have a tool for previewing (stereo/mono) VR renders in a VR headset. All renderers support this output format, but the preview process is a bit of a bottleneck. You usually need to leave the DCC application, load the render in another app, e.g. Nuke and judge the visual quality there. This adds a bit of time to each iteration and makes the preview process cumbersome.

So I tried to simplify this process. Sending pictures to HMDs can get very technical and low-level but I rather took a high-level approach: Python + WebVR. Or more precisely Python on the Houdini side and WebVR on the side of a web browser. Using a web browser means that I have to leave Houdini for previewing VR render, but with Python I tried to make it as automatic as possible.

Check this video to see how my tool works:

https://youtu.be/B5eOd3h8jAc

Note that this tool is in experimental stage. It does the job, but user experience could be significantly improved :) It works well as a proof of a concept and can be built upon to improve it.

I will briefly go through the design of this tool and current limitations.

 

## Houdini

To make the tool renderer-agnostic I am grabbing pixels from Render View pane in the Houdini UI. This makes it easy to send rendered picture from any renderer or to display certain AOV. What I do next is I create a NumPy array from the pixels which I afterwards export to a PNG file. After the render is saved I open a web page with image path and other settings stored in URL parameters. This tool also has auto-refresh mode which writes out rendered image every N seconds. If the browser is opened in auto-refresh mode, it will automatically refresh the page to display the latest render.

### Web browser

 

Using web browser for VR display might seem strange but I chose it because of the WebVR support. This feature handles VR device inputs and outputs and provides easy control above it. It is supported in modern browsers and supports major VR devices. You can read more about what is supported [here](https://webvr.rocks/). Initially I had trouble with finding an portable high-level open source solution to controlling VR headsets. But WebVR seems to be quite a good solution and has the following benefits: low-level HMD device support is handled for you, it is HMD device agnostic (for the common features), it is accessible (everybody has a web browser installed) and also is multi platform (VR devices doesn't seem to support Linux well, but you can use it in fallback mode where it behaves as a panorama viewer in this case).

To the tech: WebVR is the underlying technology. I am accessing it through [A-Frame](https://aframe.io/) library which builds on top of [three.js](https://threejs.org/) library which then supports WebVR. A-Frame is very elegant JavaScript library which is easy to get into and is also quite powerful as it gives you access to underlying three.js objects. The web part consists of an A-Frame scene with two spheres, each visible to respective eye in HMD. I created a shader which displays VR renders correctly, taking image layout into consideration. On top of that I added [dat.gui](https://github.com/dataarts/dat.gui) UI with controls of exposure, gamma-correction and auto-reloading. Auto page refreshing is also working fine in VR mode - it keeps you in this mode. Luckily you don't have to enter it on every page reload.

VR mode means that page content is sent to HMD device. By default nothing is displayed in the VR device. User has to initiate it by clicking on HMD icon in the right bottom corner. This shouldn't be done automatically and is a security feature defined in WebVR specification.

## Limitations

 

### HDR image support

 

This workflow relies on PNGs and therefore is limited by this image format: renders are stored in 8bit (per channel) PNGs which means they are also clamped in 0-1 range. This is quite a serious limitation as it discards lots of important image information. For example it is not possible to examine over-exposed areas by lowering exposure as this information is discarded. To solve this limitation I need to find a way of sending floating point HDR images to web browser and using them as a texture in three.js.

One solution would be to encode HDR images into PNGs, which have normalized values in RGB channel and additional exposure information in alpha channel. Like in this [example](https://threejs.org/examples/webgl_hdr.html).

### Auto refreshing

 

Auto reloading is relying on page refreshes. This is the easiest way I found to update three.js texture. I tried to replace the texture without refreshing the page but that gave me some issues with caching as I am always using the same image file name. Auto reloading is synchronized with Houdini auto saving by saving time interval. This is quite a naive approach :) and breaks quickly which often leads to not-finished-saving images which are totally or partially black.

Another issue that is present in the current workflow are short black-outs in HMD between page reloads. They don't take long but are annoying enough to significantly disrupt artists experience in VR.

### Next steps

 

Those are the main current issues which are result of my initial approach. I think that it could be solved by better communication between Houdini and the web browser. I was thinking about giving a try using websockets. I will try to figure out if it could establish a  communication channel for transferring HDR image data and to update VR texture on browser side exactly when needed. I will also try to minimize short freezes between texture replacement. It seems that it cannot be totally suppressed as it takes some time to upload a texture into GPU memory, but maybe something can be done about it - fading to black and back to new texture or something like that. Testing will show :)

Thanks for reading all the way down and I hope that you will find this project useful :) Feel free to contribute to it by building on it or suggesting a workflow which would solve some of the problems.
