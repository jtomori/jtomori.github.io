---
title: "Updating GPU drivers on Nvidia VCA"
date: "2019-03-02"
categories: 
  - "cg"
  - "houdini"
  - "pipeline"
  - "rendering"
---

In this post I will describe process of updating GPU drivers on [Nvidia VCA](https://www.nvidia.com/en-us/design-visualization/visual-computing-appliance/) machine. It assumes that you have ssh connection to the machine and root privileges.

In our environment we have been using Redshift renderer (through Houdini) on the VCA. It scaled well with 8 GPUs and provided us with quick renders.

However after some time newer Redshift versions required more recent GPU driver version.

After you are SSH-ed into the VCA you can check the current driver version by running

$ nvidia-smi

In the top line you will see version of current driver.

 

## Updating

 

First download the most recent driver from [Nvidia website](https://www.nvidia.com/Download/index.aspx?lang=en-in). Choose the correct hardware,  in our case it was: **Quadro** type, **Quadro P6000** product and **Linux 64bit** OS. After the driver is downloaded copy it to VCA for example via **scp**.

Before driver update we need to stop VCA services:

$ sudo systemctl stop cluster-manager node-manager cache-manage

Install  the new driver

$ sh ./NVIDIA-Linux-x86\_64-390.77.run -s

Check if GPUs are recognized

$ nvidia-smi

Start VCA services

$ systemctl start cluster-manager node-manager cache-manager

You can check logs if everything has started up correctly

$ cd /var/log/iray
$ tail -f cluster-manager.log
$ tail -f node-manager.log

That should be it, enjoy rendering :)

<!-- Markdeep: --><style class="fallback">body{visibility:hidden;white-space:pre;font-family:monospace}</style><script src="../markdeep.min.js" charset="utf-8"></script><script>window.alreadyProcessedMarkdeep||(document.body.style.visibility="visible")</script>

