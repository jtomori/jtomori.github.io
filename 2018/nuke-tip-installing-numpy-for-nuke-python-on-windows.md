---
title: "Nuke tip | Setting up NumPy on Windows"
date: "2018-11-28"
categories: 
  - "nuke"
  - "pipeline"
---

Sometimes it is useful to have NumPy module available in Nuke's Python. It contains powerful tools for image processing and is required by some gizmos, e.g. [mmColorTarget](https://www.marcomeyer-vfx.de/?p=88).

Setting up NumPy on Linux is usually just a matter of running _"$ pip install numpy"_, but on Windows it can get tricky.

In this quick tip I will show you how to easily take advantage of Houdini's NumPy which was compiled with the same compiler as Python in Nuke.

## The first try

 

Here I will show you a simple way you could expect to work, but it won't and I will explain why. So you might try to install Python on Windows, install NumPy with _pip_ and copy _numpy_ folder into Nuke's site-packages (e.g. _C:\\Program Files\\Nuke11.2v4\\pythonextensions\\site-packages_). But after doing it you will probably get a compiler mismatch and this error after attempting to _"import numpy"_ in Nuke session:

ImportError: 
Importing the multiarray numpy extension module failed. Most
likely you are trying to import a failed build of numpy.
If you're working with a numpy git repo, try \`git clean -xdf\` (removes all
files not under version control). Otherwise reinstall numpy.

Original error was: DLL load failed: The specified module could not be found.

_(You could also set a PYTHONPATH variable to an empty folder with numpy copied to it, but I will just go with moving it into Nuke's site-packages for simplicity.)_

So as you can see no luck so far. The reason is that NumPy relies on C libraries which were compiled with a specific version of Microsoft Visual Studio (with MSVC compiler). CPython (Python implementation in our case) is also a C program compiled with a specific version of MSVC. So in order for Python to use NumPy binaries they need to be binary-compatible and compiled with the same compiler.

## Which version

 

So the solution is in theory simple: detect compiler version of Nuke's Python and get correct NumPy binaries. To detect the version, you can just run Python and check the first line.

In case of my system's Python it is:

Python 2.7.15 (v2.7.15:ca079a3ea3, Apr 30 2018, 16:30:26) \[MSC v.1500 64 bit (AMD64)\] on win32

and in case of Nuke's Python (_C:\\Program Files\\Nuke11.2v4\\python.exe_) it is:

Python 2.7.13 (default, Aug 21 2017, 11:46:40) \[MSC v.1900 64 bit (AMD64)\] on win32

Compiler version is in square brackets and you can see a mismatch: system's _MSC v.1500_ vs Nuke's _MSC v.1900_. There is actually also a Python version mismatch, but it is just minor and in our case doesn't make much of a difference.

This number is not really a MSVC version, but can be used to [look up the actual version of MSVC:](https://stackoverflow.com/a/2676904)

```
Visual C++ 4.x                  MSC_VER=1000
Visual C++ 5                    MSC_VER=1100
Visual C++ 6                    MSC_VER=1200
Visual C++ .NET                 MSC_VER=1300
Visual C++ .NET 2003            MSC_VER=1310
Visual C++ 2005  (8.0)          MSC_VER=1400
Visual C++ 2008  (9.0)          MSC_VER=1500
Visual C++ 2010 (10.0)          MSC_VER=1600
Visual C++ 2012 (11.0)          MSC_VER=1700
Visual C++ 2013 (12.0)          MSC_VER=1800
Visual C++ 2015 (14.0)          MSC_VER=1900
Visual C++ 2017 (15.0)          MSC_VER=1910
```

## Get the binaries

 

Now we know that we need NumPy for Python 2.7 compiled with Visual C++ 2015. I tried to find a good place repository of NumPy binaries for various Python and MSVC versions on the internet, but didn't find anything good. _(Please let me know if something like that exists :))_

So instead of too much of googling or trying to build it myself I checked Houdini's Python version which ships with NumPy module.

To do so you need to install Houdini at first place, and the [free apprentice version](https://www.sidefx.com/download/) will be ok. After installing Houdini you can run from your Start menu _"Command Line Tools"_ and _hython_ from there.

For Houdini 17.0.352 I get _MSC v.1915_ and for Houdini 16.5.571 I get _MSC v.1900._

So Houdini 16.5.571 uses Python compiled with the same version as Nuke :) And what is even better we can just copy-paste Houdini's NumPy into Nuke's site-packages. _(I wouldn't recommend setting Nuke's PYTHONPATH to point to Houdini's site-packages as this is a potential for troubles and conflicts)_

This version match isn't hopefully a coincidence but a result of efforts to follow [VFX Reference Platform](http://www.vfxplatform.com/).

So copy _numpy_ folder from _C:\\Program Files\\Side Effects Software\\Houdini 16.5.571\\python27\\lib\\site-packages_ into _C:\\Program Files\\Nuke11.2v4\\pythonextensions\\site-packages_

After that you should be able to "_import numpy"_ inside of Nuke's Script Editor without any issues.

Hope you found this helpful, thanks for reading all the way down :)
