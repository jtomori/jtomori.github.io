---
title: "Houdini tip | CAMERA AUTO FOCUS"
date: "2018-02-06"
categories: 
  - "cg"
  - "houdini"
  - "rendering"
---

Hello, in this post I will show a quick way of adding auto-focus support to Houdini camera. By setting a target, following couple lines of code will determine correct distance to focus on. This approach will work for any renderer.

![out](images/out.gif)

 

The setup is pretty simple, we need to add two parameters to our camera: **target** which is a string pointing to OBJ node we want to focus on and **dist** parameter which will contain following Python expression.

https://gist.github.com/jtomori/64a83a252056b2675b710a103d927fb2

 

After that we can link **Focal Distance** parameter to our **dist**. Feel free to drop a helper Null object for visualizing focus plane :)

 

[You can download project file here.](https://drive.google.com/open?id=1NsrfBPg6Gz-cpP32U6sqs4slzck7xpu3)
