---
title: "Creating a simple C++ OpenVDB node in HDK"
date: "2017-12-01"
categories: 
  - "cg"
  - "hdk"
  - "houdini"
  - "pipeline"
---

In this post I will describe how to write a simple Houdini node operating on VDB volumes. It is a result of my recent HDK explorations and the purpose of the node is to activate voxels in VDB volume based on input points. Right now it is not possible to activate a voxel at certain position in a VDB volume through VEX and VDB Activate node does not take as input points positions (it will activate voxels within bounding box if geometry is fed into the second input). I will try to describe the process as simple as possible, so even if you do not have much experience with C++ hopefully you will be able to follow along :)

### Intro

For me it is a good exercise to get a bit into OpenVDB and HDK and I will be commenting every step, so that you know what is going on and I can get back to the code in the future. Also this code can serve as a template for creating SOP nodes in HDK. I am not using all features (local vars, changing/creating geometry, attributes...), but only the basics and with the HDK docs you can get more advanced :) Please note that there is a lot of space for improvements in the logic of this node, for example adding support for vector volumes, processing only user-selected volumes (right now it will process only first VDB primitive found). But still I think that this node can be pretty useful. Feel free to contribute to the repository if you have any suggestions! If you find any mistakes in this post please let me know and I will fix them :) One of the main places where to look for information is [HDK docs](https://www.sidefx.com/docs/hdk/_h_d_k__intro__getting_started.html) which include also [many handy examples](https://www.sidefx.com/docs/hdk/examples.html). [Deborah R Fowler](http://www.deborahrfowler.com/C++Resources/HDK-Resources.html) has shared also many great resources. Houdini is coming with _HDK - Houdini Development Kit_, which is set of Houdini libraries and corresponding header files. Headers can be found in _/opt/hfs16.0.736/toolkit/include_ (with using Houdini environment variables: _$HT/include_) and libraries in _/opt/hfs16.0.736/dsolib_ (_$HDSO_). Houdini has a plugin system which enables users to write their own nodes in C++ using Houdini API and to link against Houdini shared libraries. The plugins/nodes are then compiled into shared libraries (_.so_ files) as well and put into one of the paths where Houdini is looking for custom plugins. Those paths are usually _/opt/hfs16.0.736/houdini/dso_ and _~/houdini16.0/dso_. If you want Houdini to pick up plugins from you custom path, then customize _HOUDINI\_DSO\_PATH_ environment variable, e.g.

HOUDINI\_DSO\_PATH="&:/home/juraj/my\_custom\_dso\_folder"

You can check the paths and explanation of the _&_ symbol by using _hconfig_ utility (make sure to _source houdini\_setup_ to have access to all handy utilities and variables)

$ hconfig -ap

 

I tried to put explanatory comments into node's source code, I will split it here into sections and will write a short description to each one.

### Header

 

Header for the node looks like this:

#ifndef \_\_SOP\_vdb\_activate\_from\_points\_h\_\_
#define \_\_SOP\_vdb\_activate\_from\_points\_h\_\_

#include <SOP/SOP\_Node.h>

namespace VdbActivateFromPoints {
class SOP\_VdbActivateFromPoints : public SOP\_Node
{
public:
    // node contructor for HDK
    static OP\_Node \*myConstructor(OP\_Network\*, const char \*, OP\_Operator \*);

    // parameter array for Houdini UI
    static PRM\_Template myTemplateList\[\];

protected:
    // constructor, destructor
    SOP\_VdbActivateFromPoints(OP\_Network \*net, const char \*name, OP\_Operator \*op);

    virtual ~SOP\_VdbActivateFromPoints();

    // labeling node inputs in Houdini UI
    virtual const char \*inputLabel(unsigned idx) const;

    // main function that does geometry processing
    virtual OP\_ERROR cookMySop(OP\_Context &context);

private:
    // helper function for returning value of parameter
    int DEBUG() { return evalInt("debug", 0, 0); }

};
}

#endif

It contains definition of our class (node) and functions for constructing (_myConstructor(),  SOP\_VdbActivateFromPoints(), ~SOP\_VdbActivateFromPoints()_), UI parameters (_myTemplateList\[\]_), labeling of inputs (_inputLabel()_). Function that does the actual geometry processing is _cookMySop()_. For convenience I also set up a _DEBUG()_ function which will evaluate debug parameter in node's UI (the last argument could be frame number of evaluation, but we are not likely to animate debug option). I will describe more those variables and functions in actual source code bellow.

### Source code

 

At first we need to reference our own header, then headers for accessing Houdini functionality and finally headers for OpenVDB shipped with Houdini.

#include "vdb\_activate\_from\_points.h"
#include <limits.h>
#include <SYS/SYS\_Math.h>
#include <UT/UT\_DSOVersion.h>
#include <UT/UT\_Interrupt.h>
#include <OP/OP\_Operator.h>
#include <OP/OP\_OperatorTable.h>
#include <GU/GU\_Detail.h>
#include <GEO/GEO\_PrimPoly.h>
#include <PRM/PRM\_Include.h>
#include <CH/CH\_LocalVariable.h>
#include <OP/OP\_AutoLockInputs.h>
#include <GU/GU\_PrimVDB.h>
#include <openvdb/openvdb.h>

After that we need to [register our node](https://www.sidefx.com/docs/hdk/_h_d_k__op_basics__overview__registration.html) and label node inputs (to be seen in the network editor). _newSopOperator()_ is a function which Houdini will be looking for. Its purpose is to add our node to Houdini's table of operators. It is required and will also categorize our node in the _TAB_ menu.

// register the operator in Houdini, it is a hook ref for Houdini
void newSopOperator(OP\_OperatorTable \*table)
{
    OP\_Operator \*op;

	op = new OP\_Operator(
    		"vdbActivateFromPoints",                      // internal name, needs to be unique in OP\_OperatorTable (table containing all nodes for a network type - SOPs in our case, each entry in the table is an object of class OP\_Operator which basically defines everything Houdini requires in order to create nodes of the new type)
    		"VDB Activate from Points",                   // UI name
    		SOP\_VdbActivateFromPoints::myConstructor,     // how to build the node - A class factory function which constructs nodes of this type
    		SOP\_VdbActivateFromPoints::myTemplateList,    // my parameters - An array of PRM\_Template objects defining the parameters to this operator
    		2,                                            // min # of sources
    		2);                                           // max # of sources

    // place this operator under the VDB submenu in the TAB menu.
    op->setOpTabSubMenuPath("VDB");

    // after addOperator(), 'table' will take ownership of 'op'
    table->addOperator(op);
}

// label node inputs, 0 corresponds to first input, 1 to the second one
const char \*
SOP\_VdbActivateFromPoints::inputLabel(unsigned idx) const
{
    switch (idx){
        case 0: return "VDB";
        case 1: return "Points where active voxels should be";
        default: return "default";
    }
}

[Building parameters UI:](https://www.sidefx.com/docs/hdk/_h_d_k__op_basics__overview__parameters.html)  you can refer to documentation for all available parameter types (_float, int, checkbox, menu_...) After we created our _PRM\_Name_ objects we need to assign them to _PRM\_Template_ array which will be used by Houdini for displaying parameters in UI. Note that even if we wished to have no parameters, we still need to include one empty _PRM\_Template()_ in the array.

// define parameter for debug option
static PRM\_Name debugPRM("debug", "Print debug information"); // internal name, UI name

// assign parameter to the interface, which is array of PRM\_Template objects
PRM\_Template SOP\_VdbActivateFromPoints::myTemplateList\[\] = 
{
    PRM\_Template(PRM\_TOGGLE, 1, &debugPRM, PRMzeroDefaults), // type (checkbox), size (one in our case, but rgb/xyz values would need 3), pointer to a PRM\_Name describing the parameter name, default value (0 - disabled)
    PRM\_Template() // at the end there needs to be one empty PRM\_Template object
};

After that we need to include required functions for class construction, destruction and Houdini-related construction. Usually we do not need to modify anything here. One situation when you might want to modify _SOP\_VdbActivateFromPoints()_ function is when you want to manage data ID's, e.g. for performance reasons and correct viewport updating. You can find more information about it [here](https://www.sidefx.com/docs/hdk/_h_d_k__geometry__intro.html#HDK_Geometry_Intro_Data_IDs).

// constructors, destructors, usually there is no need to really modify anything here, the constructor's job is to ensure the node is put into the proper network
OP\_Node \* 
SOP\_VdbActivateFromPoints::myConstructor(OP\_Network \*net, const char \*name, OP\_Operator \*op)
{
    return new SOP\_VdbActivateFromPoints(net, name, op);
}

SOP\_VdbActivateFromPoints::SOP\_VdbActivateFromPoints(OP\_Network \*net, const char \*name, OP\_Operator \*op) : SOP\_Node(net, name, op) {}

SOP\_VdbActivateFromPoints::~SOP\_VdbActivateFromPoints() {}

Now we should have everything prepared. We can create our _cookMySop()_ function which will do the actual job. I tried to explain all the steps in the comments bellow.

// function that does the actual job
OP\_ERROR
SOP\_VdbActivateFromPoints::cookMySop(OP\_Context &context)
{
    // we must lock our inputs before we try to access their geometry, OP\_AutoLockInputs will automatically unlock our inputs when we return
    OP\_AutoLockInputs inputs(this);
    if (inputs.lock(context) >= UT\_ERROR\_ABORT)
        return error();

    // duplicate our incoming geometry
    duplicateSource(0, context);

    // check for interrupt - interrupt scope closes automatically when 'progress' is destructed.
    UT\_AutoInterrupt progress("Activating voxels...");

    // get pointer to geometry from second input
    const GU\_Detail \*points = inputGeo(1);

    // check if debug parameter is enabled, DEBUG() function is defined in header file
    if (DEBUG())
    {
        std::cout << "number of points: " << points->getNumPoints() << std::endl;
    }

    GEO\_PrimVDB\* vdbPrim = NULL; // empty pointer to vdb primitive

    // iterate over all incoming primitives and find the first one which is VDB
    for (GA\_Iterator it(gdp->getPrimitiveRange()); !it.atEnd(); it.advance())
    {
        GEO\_Primitive\* prim = gdp->getGEOPrimitive(it.getOffset());
        if(dynamic\_cast<const GEO\_PrimVDB \*>(prim))
        {
            vdbPrim = dynamic\_cast<GEO\_PrimVDB \*>(prim);
            break;
        }
    }

    // terminate if volume is not VDB
    if(!vdbPrim)
    {
        addError(SOP\_MESSAGE, "First input must contain a VDB!");
        return error();
    }

    // volume primitives in different nodes in Houdini by default share the same volume tree (for memory optimization) this will make sure that we will have our own deep copy of volume tree which we can write to 
    vdbPrim->makeGridUnique();
    
    // get grid base pointer and cast it to float grid pointer
    openvdb::GridBase::Ptr vdbPtrBase = vdbPrim->getGridPtr();
    openvdb::FloatGrid::Ptr vdbPtr = openvdb::gridPtrCast<openvdb::FloatGrid>(vdbPtrBase);

    // get accessor to the float grid
    openvdb::FloatGrid::Accessor vdb\_access = vdbPtr->getAccessor();

    // get a reference to transformation of the grid
    const openvdb::math::Transform &vdbGridXform = vdbPtr->transform();

    // loop over all the points by handle
    int i = 0;
    GA\_ROHandleV3 Phandle(points->findAttribute(GA\_ATTRIB\_POINT, "P")); // handle to read only attribute
    GA\_Offset ptoff;
    GA\_FOR\_ALL\_PTOFF(points, ptoff)
    {
        // test if user requested abort
        if (progress.wasInterrupted())
            return error();

        // get current pont position
        UT\_Vector3 Pvalue = Phandle.get(ptoff);

        // create openvdb vector with values from houdini's vector, transform it from world space to vdb's index space (based on vdb's transformation) and activate voxel at point position
        openvdb::Vec3R p\_( Pvalue\[0\], Pvalue\[1\], Pvalue\[2\] );
        openvdb::Coord p\_xformed( vdbGridXform.worldToIndexCellCentered(p\_) );
        vdb\_access.setValueOn( p\_xformed );
        
        if (DEBUG())
        {
            std::cout << i << ". point world space position: " << Pvalue << std::endl;
            std::cout << "  volmue index space position: " << p\_xformed << std::endl;
        }

        i++;
    }

    return error();
}

### Setup & compilation

 

You can get more information about compiling nodes for Houdini and OpenVDB in my previous posts: [Compiling C++ OpenVDB Hello World example using Houdini precompiled libraries on Linux](https://jurajtomori.wordpress.com/2017/11/23/compiling-c-openvdb-hello-world-example-using-houdini-precompiled-libraries-on-linux/), [Compiling DreamWorks OpenVDB C++ nodes for Houdini on Linux](https://jurajtomori.wordpress.com/2017/11/23/compiling-dreamworks-openvdb-c-nodes-for-houdini-on-linux/) You can get the final files from [this repository](https://github.com/jtomori/VDB_activate_from_points). Use this [link](https://github.com/jtomori/VDB_activate_from_points/archive/master.zip) to download it, or clone it with git:

$ git clone https://github.com/jtomori/VDB\_activate\_from\_points.git

After that create a folder to build the plugin into and source houdini environment

$ cd VDB\_activate\_from\_points
$ mkdir build$ cd /opt/hfs16.0.736
$ source houdini\_install

_g++_ in your system might not refer to the version which was used for compiling Houdini (4.8), if g++ command in your environment refers to version different from Houdini one we need to set up the correct one:

$ export CC=/usr/bin/gcc-4.8
$ export CXX=/usr/bin/g++-4.8

Set necessary compiler flag and build our code using Houdini _hcustom_ util

$ export HCUSTOM\_CFLAGS="-DOPENVDB\_3\_ABI\_COMPATIBLE"
$ hcustom -i build/ -e -L $HDSO -l openvdb\_sesi src/vdb\_activate\_from\_points.C

Enable displaying of DSO errors (for debugging) and tell Houdini where to find our freshly compiled node, run Houdini. Once in SOPs you should be able to add our _VDB Activate from Points_ node, it can be found in _TAB->VDB_ submenu.

$ export HOUDINI\_DSO\_ERROR=1
$ export HOUDINI\_DSO\_PATH="/your\_path/VDB\_activate\_from\_points/build:&"
$ houdini -foreground

That should be all. After reading this tutorial you should be able to successfully compile VDB Activate from Points node and use it. Feel free to grab pieces of code and use it in your project or use it as a template for your own next node :) If you have any problems or suggestions for improvements, just let me know.

 

### Thanks :)

I would like to thank [Ostap Pochtarenko](https://github.com/RiLights/) for support, good ideas and helping with code :) Also to helpful posts at sidefx and odforce forums and [Deborah R Fowler's](http://www.deborahrfowler.com/C++Resources/HDK-Resources.html) great resources.

<!-- Markdeep: --><style class="fallback">body{visibility:hidden;white-space:pre;font-family:monospace}</style><script src="../markdeep.min.js" charset="utf-8"></script><script>window.alreadyProcessedMarkdeep||(document.body.style.visibility="visible")</script>

