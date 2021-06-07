---
title: "Running Houdini job on a remote Windows machine"
date: "2019-03-01"
categories: 
  - "cg"
  - "houdini"
  - "pipeline"
  - "rendering"
---

In this post I will show you how to execute a Houdini (or any other) job remotely on a Windows machine. The remote machine in our case did not have a GPU and my goal was to make it automatic so the job was started from command line.

 

## Batch file

 

For running the job we can create a batch file (e.g. generate it with Python) and execute it on the remote computer.

The file can look like this, I will go briefly over the commands bellow.

https://gist.github.com/jtomori/f865ed53e4a9937f1f73b223c93ce028

The lines starting with _%RR\_ROOT%_ are related to _Royal Render_ renderfarm manager which was was running in our environment. This kind of jobs are presumed to be higher priority so we are temporarily disabling _Royal Render_ during our job.

The line calling _\\\\network\_share\\project\\pipeline\\houdini\\houdini\_remote.bat_ is setting up an project-related environment (setting bunch of variables for plugins, paths, configs etc.).

_Pushd_ command is related to mounting and entering a network drive containing the project. After our job is finished we unmount it with _popd_. This is quite site-specific and will depend on your studio setup.

_Cd_ enters a directory containing the project file to be executed.

_Hbatch_ is a _hscript_\-based command line utility which can open Houdini scenes. It should be available in your _%PATH%_ environment variable (set with _houdini\_remote.bat)._ _Hbatch_ can execute _hscript_ commands passed with _\-c_ argument. _[Render](http://www.sidefx.com/docs/houdini/commands/render.html) hscript_ command is executing a ROP with a nice verbose output (the _\-Va_ argument). After the rendering is finished the _quit_ command exits Houdini, so the next lines in our batch file can be executed. The rest of this line redirects standard out and error outputs to a file where we can take a look at it during or after rendering. It is handy for checking progress or debugging problems.

_Move_ command simply renames our log file. It appends to its name _.finished_ part so you can easily see if it is finished without actually opening it.

 

## Running

 

One approach could be running our batch file through **Remote Desktop Connection** app on Windows. This might however slow down user's workflow.

Luckily it is possible to execute commands remotely on windows machines with [PsExec](https://docs.microsoft.com/en-us/sysinternals/downloads/psexec) utility. One downside is that you need to have admin rights at remote PC for your account. If you have them, then following command should trigger execution of our batch file.

psexec \\\\remote\_machine\_name -accepteula -d -l -u domain\\user\_name -p secret\_password cmd /c "\\\\network\_share\\project\\Production\\shot\\task\\bat\\project\_file\_v003.hipnc.bat"

A better way would be to connect and execute our job on the remote machine via [SSH](https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_overview) server. In our setup we unfortunately didn't have this option.

In our project I made this a fully automatic workflow directly from Houdini. I will share the whole tool in near future after I will wrap up couple of things :).

<!-- Markdeep: --><style class="fallback">body{visibility:hidden;white-space:pre;font-family:monospace}</style><script src="../markdeep.min.js" charset="utf-8"></script><script>window.alreadyProcessedMarkdeep||(document.body.style.visibility="visible")</script>

