---
title: "Houdini tip | Taking advantage of environment variables"
date: "2018-01-15"
categories: 
  - "houdini"
  - "pipeline"
---

Like many other applications, Houdini's configuration can be modified by using environment variables. It is a very useful way of creating different Houdini setups for different purposes - let it be different projects, different plugin versions, sandboxes for testing assets, personal configurations, etc. While this post is written for Houdini and have examples for windows and linux, it is applicable for any other application and operating system.

### A couple of words about environment variables.

At first I will try to explain basic concepts of env vars and later on I will show examples for Houdini (linux and windows).

Environment variables might be a bit hidden to many users, but they can be very helpful. Actually a lot of operating system behavior is controlled by them. Apart from configuring Houdini, env vars can be used to modify a search path for binaries, libraries, can set up proxy settings, get current user's name, path to home, temp directory, hostname, shell and much more.

An useful thing is that they can be applied globally to the whole system, and locally to the current environment in a shell (a terminal session or environment set up and executed from batch/bash script). For example one might specify global settings which are available to the whole system (path to system cache dir, username, path to root directory of all projects...) and local settings for each configured environments (houdini version, project name, project root, path to textures directory, license information about a plugin...). All child environments (set up through batch/bash script) will inherit global settings (available to the whole operating system or an user) and can have specific local settings needed for their purpose.

Here are couple of situations which env vars can efficiently address:

- having a multiple versions of Houdini using different renderer plugin versions and different assets libraries
- using different configurations for different projects / sequences / shots / tasks
- sharing the same settings (home dir, temp dir, cache dir, footage path, rv path) for various applications (Houdini, Nuke, Katana, Maya)

 

### Using environment variables on windows

Here I will show an example of one of my Houdini startup script which sets an environment for a project and executes Houdini: _houdini.bat_. Note that Houdini understands a lot of useful env vars, documentation can be found [here](http://www.sidefx.com/docs/houdini/ref/env).

https://gist.github.com/jtomori/80a14efebd397a57f1c0106a37a97c41

Here I will explain some of batch syntax: **@echo off** - hides printing of commands into the console, it makes output more readable **rem foo** - lines starting with rem are comments **call foo.bat** - executes _foo.bat_ batch script and inherits all env vars specified in it **%MYVAR%** - value of _MYVAR_ variable **set "MYVAR=FOO"** - sets _MYVAR_ variable to _FOO_ - those variables are specific to softwares, which are expecting them **set "PATH=%PATH%;FOO"** \- appends _FOO_ to the _PATH_ variable which is used for locating binaries to be executed (_houdinifx_ command is not known to the whole windows system, only when houdini bin directory (containing _houdinifx.exe_) is appended to the _PATH_ var) **start foo** - executes _foo.exe_ (which must be found in one of the paths in the _PATH_ env var) while passing on all existing variables to this child environment

This script can be used for setting up local environment variables, to define a variable for the whole system environment on windows, follow this [video](https://www.youtube.com/watch?v=bEroNNzqlF4).

 

 

### Using environment variables on linux

(Linux version should be directly transferable to mac OS.)

In linux env vars can be set up on multiple locations _(~/.profile, ~/.bashrc, ~/.bash\_profile, ~/.bash\_login, /etc/environment ...)_ System env vars can be specified in _/etc/environment_. User env vars can be specified in _~/.profile_ (_~_ symbol points to the user _home_ directory). _~/.profile, ~/.bashrc, ~/.bash\_profile,_ and _~/.bash\_login_ have similar usage, but I recommend using _~/.profile_, which is the only one executed when running applications from graphical environment in a desktop session..

In a Bash terminal the quickest way of executing an application inheriting env vars is to use this syntax:

$ MYVAR1=foo MYVAR2=bar houdinifx #executes houdinifx with MYVAR1 and MYVAR2 variables set to "foo" and "bar"

While this is useful for quick testing one might want to create a start script instead of typing the command into the terminal.

To create a bash script, create a file _houdini.sh_ and make it executable (_chmod +x houdini.sh_), then put shebang into the first line. In the script you can set variables using this syntax

#!/usr/bin/env bash
cd /opt/hfsXX.X.XXX/ #replace X with your Houdini version
source houdini\_setup
export MYVAR1="foo"
export MYVAR2="bar"
houdinifx

This simple script will source (inherit) environment from _houdini\_setup_ script shipped with houdini, execute _houdinifx_ command with _MYVAR1_ and _MYVAR2_ variables present.

 

Here is another simple start script which I use when testing a [houdini plugin](https://github.com/RiLights/VDB-Deformer/). It is different from the windows batch script showed before, but you can use this syntax to port it for linux as well :) Also one note - in your linux shell a _houdini_ command might not be available if you have not sourced environment from _/opt/hfsXX.X.XXX/houdini\_setup_ script before:

$ cd /opt/hfsXX.X.XXX/
$ source houdini\_setup

Which is basically calling _houdini\_setup_ script to set up and inherit needed variables (equivalend to the call command in windows batch).

https://gist.github.com/jtomori/580e61807d0ce1254fe5de90b125e5e4

 

### Checking if variables are present in Houdini

Once you have run Houdini from your batch/bash script you can quickly check if your variables are present in your Houdini session.

#### Hscript

Open texport pane and type following

echo $MYVAR1

Output of this command should match the value specified in your starting script. Now you can use _$MYVAR1_ in any parameter inside Houdini, useful, isn't it?

#### Python

Open python shell pane and type following

print hou.getenv("MYVAR1")

With that command you can get value of _MYVAR1_ in any python context inside your Houdini session.

 

### Final words

Those setups can be very useful, it might take a bit of time when setting them up for the first time but it will definitely pay off later on. Especially when your setups will get more complicated :) You also then need to manage your scripts somehow, because your variables will not work when houdini project file will be run in another environment (without executing your starting script). This happens often when running scripts from another user, machine, on renderfarm etc.

Hope you find it helpful, if you spot any mistakes please let me know so that I can correct them.
