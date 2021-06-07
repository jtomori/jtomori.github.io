---
title: "VFX Good Night Reading update"
date: "2018-11-03"
categories: 
  - "cg"
---

I did couple of updates to my VFX, CG learning resources database **[VFX Good Night Reading](https://github.com/jtomori/vfx_good_night_reading)**. It features new content, library update and link to **FREE** access to ACM Siggraph content.

 

## New content

 

The most significant one is a bunch of new content :). Or 34 new entries to be precise.I browsed through new Siggraph pages and downloaded anything that got my interest in hope of reading it and adding to the database. While I am not finished yet with the reading, I managed to put the content into the database. It contains new papers and also new categories - _VR, Computer Vision, Machine Learning, USD, Fractals, Motion Capture and Photogrammetry_. You can check [the latest commits](https://github.com/jtomori/vfx_good_night_reading/commits/master) to see exact changes.

## Library update

 

The next new feature is concerning database of the research papers. I am not writing entries into the _README.md_ file, but rather to a database and then use Python to generate the _README.md_ file for me. It has benefits that it organizes and updates categories and tags for me automatically and thus makes it easier to overcome my laziness to maintain the library :) Before the update I used _JSON_ format but that involved too much of syntax structure for my taste, so I [ported](https://github.com/jtomori/vfx_good_night_reading/blob/master/json_to_yaml.py) the library to _YAML_ format which is more easily human readable/writeable. Along the way I realized that I initially used ancient _Python 2.\*_, so I quickly udpated to _Python 3.\*_.

I also hope that maybe somebody will share their collection of papers and contribute to the library :D.

For reference, this is how an entry looked in _JSON_:

...
"3D Fractal Flame Wisps": {
        "categories": \[
            "Volumetrics", 
            "Lighting & Rendering"
        \], 
        "format": "thesis", 
        "link": "https://tigerprints.clemson.edu/cgi/viewcontent.cgi?article=2704&context=all\_theses", 
        "tags": \[
            "clemson"
        \]
},
...

And the same in _YAML_:

3D Fractal Flame Wisps:
    categories:
        - Volumetrics
        - Lighting & Rendering
    format: thesis
    link: https://tigerprints.clemson.edu/cgi/viewcontent.cgi?article=2704&context=all\_theses
    tags:
        - clemson

Neat, isn't it? It asks for your contribution to the library.

## Open access to ACM Siggraph content

 

Lot of the links here refer to ACM Digital Library. The advantage is that they keep everything at one place, have nice structure, etc. The disadvantage can be that you might need to buy access to the content of the library. However during some period of time all of this content is available for free. [Find out more here](https://www.siggraph.org//learn/conference-content). Make sure to check this out and get papers and videos that interest you.

Here is excerpt from their site:

> ACM SIGGRAPH has participated in the ACM open access program since it was founded in 2015. As a result, [SIGGRAPH](http://siggraph.org/current-conference) conference content from 2015 forward is available through this program.
> 
> For both SIGGRAPH and SIGGRAPH Asia, conference content is freely accessible in the [ACM Digital Library](http://dl.acm.org/) for a one-month period that begins two weeks before each conference, and ends a week after it concludes. Following this one-month "free access" window, the content is available at no cost in perpetuity, exclusively through the open access links on the page below. ACM SIGGRAPH also provides the same open access to [sponsored and co-sponsored conference content](http://www.siggraph.org/learn/sponsored-conference-content) in the ACM Digital Library.
