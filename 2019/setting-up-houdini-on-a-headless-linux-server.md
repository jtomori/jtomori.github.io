---
title: "Setting up Houdini on a headless linux server"
date: "2019-03-05"
categories: 
  - "cg"
  - "houdini"
  - "pipeline"
  - "rendering"
---

I will go briefly through the process of setting up Houdini on a headless linux server.

In our project we had access to [Nvidia VCA](https://www.nvidia.com/en-us/design-visualization/visual-computing-appliance/) hardware which was running _CentOS 7.3_ and did not have a _X_ server.

This hardware has some decent computing power in it and we wanted to offload some of our rendering on this computer. We were rendering with [Redshift renderer](https://www.redshift3d.com/) which scaled pretty well on multiple GPUs. We also just fitted into Redshift's limit of max 8 GPUs.

To be able to do more general-purpose jobs (simulations, caching) on the VCA and to simplify submission process we decided to setup both Houdini and Redshift on it.

Note that we had SSH access to the machine and root rights. However all of the actions here were done locally and did not have an impact on the whole system.

_You can read some more about managing VCA in this [guide](https://la.nvidia.com/content/vca/nvidia_vca_install_guide.pdf) and about setting up SSH connection in this [article](https://www.digitalocean.com/community/tutorials/ssh-essentials-working-with-ssh-servers-clients-and-keys)._

In order to start jobs on the VCA we decided to use _hbatch_ command-line utility which ships with Houdini installation. It enables to easily open Houdini scenes from command line and to do some actions in it. We also used _hbatch_ for starting Houdini jobs on Windows machines as [described here](https://jurajtomori.wordpress.com/2019/03/01/running-houdini-job-on-a-remote-windows-machine/).

As first step you need to install Houdini. Get linux installer from sidefx website and run it. Running it requires root rights but you can set install directory locally in your home folder.

After installing Houdini and trying to run _hbatch_ you will get this error:

$ hbatch
/var/lib/iray/juraj/houdini.16.5.571/bin/hbatch-bin: error while loading shared libraries: libXmu.so.6: cannot open shared object file: No such file or directory

It looks like _hbatch_ depends on _Xmu_ library which is missing.

We can take a closer look. First locate _hbatch-bin._ Note that _hbatch_ command is just a bash script which sets up couple of things and executes _hbatch-bin_.

_Note that your paths will differ based on your system setup. I contained the whole setup in ~/juraj, which expands to /var/lib/iray/juraj._

$ which hbatch-bin
~/juraj/houdini.16.5.571/bin/hbatch-bin

After we located _hbatch-bin_ file we can check for its dependencies:

$ ldd ~/juraj/houdini.16.5.571/bin/hbatch-bin        
        linux-vdso.so.1 =>  (0x00007fffdc3dd000)
        libjemalloc.so.1 => /var/lib/iray/juraj/houdini.16.5.571/bin/../dsolib/libjemalloc.so.1 (0x00007f90f8d13000)
        libHoudiniOPZ.so => /var/lib/iray/juraj/houdini.16.5.571/bin/../dsolib/libHoudiniOPZ.so (0x00007f90f76c3000)

        ...

        libjpeg.so.62 => /var/lib/iray/juraj/houdini.16.5.571/bin/../dsolib/libjpeg.so.62 (0x00007f90e5da2000)
        libhboost\_program\_options-mt.so.1.61.0 => /var/lib/iray/juraj/houdini.16.5.571/bin/../dsolib/libhboost\_program\_options-mt.so.1.61.0 (0x00007f90e5b30000)
        libstdc++.so.6 => /lib64/libstdc++.so.6 (0x00007f90e5826000)
        libm.so.6 => /lib64/libm.so.6 (0x00007f90e5524000)
        libgcc\_s.so.1 => /lib64/libgcc\_s.so.1 (0x00007f90e530e000)
        libc.so.6 => /lib64/libc.so.6 (0x00007f90e4f4c000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f90f8f53000)
        libnsl.so.1 => /lib64/libnsl.so.1 (0x00007f90e4d32000)
        libicui18n.so.51 => /var/lib/iray/juraj/houdini.16.5.571/bin/../dsolib/libicui18n.so.51 (0x00007f90e4934000)
        libgomp.so.1 => /lib64/libgomp.so.1 (0x00007f90e470d000)
        libGL.so.1 => /lib64/libGL.so.1 (0x00007f90e4468000)
        libXmu.so.6 => not found
        libXi.so.6 => /lib64/libXi.so.6 (0x00007f90e4258000)
        libXext.so.6 => /lib64/libXext.so.6 (0x00007f90e4045000)
        libX11.so.6 => /lib64/libX11.so.6 (0x00007f90e3d07000)
        librt.so.1 => /lib64/librt.so.1 (0x00007f90e3aff000)
        libGLX.so.0 => /lib64/libGLX.so.0 (0x00007f90e38cd000)
        libGLdispatch.so.0 => /lib64/libGLdispatch.so.0 (0x00007f90e35ff000)
        libxcb.so.1 => /lib64/libxcb.so.1 (0x00007f90e33dc000)
        libXau.so.6 => /lib64/libXau.so.6 (0x00007f90e31d8000)

_(truncated ldd's output)_

There are quite a few of them so we can display only missing ones:

$ ldd ~/juraj/houdini.16.5.571/bin/hbatch-bin | grep "not found"
        libXmu.so.6 => not found

So _hbatch_ is missing some _X_ server related libraries even though this utility is command-line only. To solve this we need to install them (_[libXmu](https://centos.pkgs.org/7/centos-x86_64/libXmu-1.1.2-2.el7.x86_64.rpm.html)_ has couple of other dependencies).

In our case the _yum_ package manager was weirdly configured and I also wanted to do all changes locally.

To do that I manually downloaded packages from [here](http://mirror.centos.org/centos/7/os/x86_64/Packages/). _(Note that doing so is not very secure way since we are not checking packages integrity. Definitely use your package manager if you can.)_

After we have our rpm packages we need to extract them. To do so I used _rpm2cpio_ and _cpio_ tools the following way:

$ rpm2cpio package.rpm | cpio -idmv

_You can find more information about this step [here](https://blog.packagecloud.io/eng/2015/10/13/inspect-extract-contents-rpm-packages/)._

Download these libraries and run the _rpm2cpio_ command on them: _libXmu, libXt, libICE, libSM, libXtst_.

After that you should have a _usr_ folder in your current working directory with structure similar to this:

usr/
├── lib
│   ├── libXmu.so.6 -> libXmu.so.6.2.0
│   ├── libXmu.so.6.2.0
│   ├── libXmuu.so.1 -> libXmuu.so.1.0.0
│   └── libXmuu.so.1.0.0
│   ...
└── share
    └── doc
        └── libXmu-1.1.2
            ├── ChangeLog
            ├── COPYING
            └── README
            ...

We are interested only in _usr/lib_ directory as it contains needed libraries. To make them locally available _(for the current user)_ we can use _LD\_LIBRARY\_PATH_ environment variable pointing to our _usr/lib_ directory.

I created _env.sh_ script which is setting up needed variables for libraries (_LD\_LIBRARY\_PATH_) as well as Redshift configuration and mounting network shares, sourcing project environment etc. At login time I execute this script to ensure that everything is set up. I call it from _~/.bashrc._

At this point _hbatch_ should run just well. The next steps involved installing Redshift, but that was quite straight-forward so I won't go much into details. _(Redshift documentation has good guides: [linux install](https://docs.redshift3d.com/display/RSDOCS/Installing+Redshift+on+Linux?product=houdini), [custom install location](https://docs.redshift3d.com/display/RSDOCS/Custom+Install+Locations?product=houdini).)_

At the end of this blog I attach needed configurations for making all of this work.

One more thing we needed to set up was Houdini licence. We had a licensing server located at _"licence\_server"_ address which local DNS would resolve to correct in-house IP address. Remote licensing server can be set with:

$ hserver -S _licence\_server_

This setup worked for us pretty well and speeded up our renderings. The only thing which we found did not work was OpenGL rendering. Except from that it worked quite well. I also built couple of tools for checking and submitting jobs on the VCA, all from Houdini interface, without leaving it. Also the nice thing about using SSH is that it is simple to do tools for both Linux and Windows environments. In case of Windows we used [_plink_](https://www.ssh.com/ssh/putty/putty-manuals/0.68/Chapter7.html) utility. Linux has SSH client by default.

For job submission we generated a linux command (via Python, from Houdini) which was then sent to VCA. It looked like this:

while pgrep hbatch-bin > /dev/null; do sleep 5; done && cd $ROOT && cd "production/rnd/task" && hbatch -c "render -Va /out/rs\_scene ; quit" "task\_scene\_v04.hipnc" &> vca/task\_scene\_v04.hipnc.rs\_scene.log && mv "vca/task\_scene\_v04.hipnc.rs\_scene.log" "vca/task\_scene\_v04.hipnc.rs\_scene.log.finished"

It is a bit long but it can be broken down into couple of steps:

while pgrep hbatch-bin > /dev/null; do sleep 5; done &&

This part waits while there is another _hbatch-bin_ process running. This is to avoid multiple jobs being rendered at once. This is a very naive way of preventing it and does not ensure order of jobs being rendered.

cd $ROOT && cd "production/rnd/task" &&

Move to folder containing scene to be rendered.

hbatch -c "render -Va /out/rs\_scene ; quit" "task\_scene\_v04.hipnc" &> vca/task\_scene\_v04.hipnc.rs\_scene.log &&

Open _task\_scene\_v04.hipnc_ with _hbatch_ and execute this _hscript_ command: _"render -Va /out/rs\_scene ; quit"._ Standard output and errors are captured in _vca/task\_scene\_v04.hipnc.rs\_scene.log_ log file.

mv "vca/task\_scene\_v04.hipnc.rs\_scene.log" "vca/task\_scene\_v04.hipnc.rs\_scene.log.finished"

After rendering is finished append _.finished_ to the log file.

This command was usually sent from Houdini via _plink:_

plink -batch -ssh -hostkey \[hostkey\] -pw \[password\] iray@vca "\[escaped linux command\]"

 

That should be all, thanks for reading :)

Here are scripts/configs I used on VCA side:

https://gist.github.com/jtomori/bd18e35035fc0dce6f334bc61cb34076

<!-- Markdeep: --><style class="fallback">body{visibility:hidden;white-space:pre;font-family:monospace}</style><script src="../markdeep.min.js" charset="utf-8"></script><script>window.alreadyProcessedMarkdeep||(document.body.style.visibility="visible")</script>

