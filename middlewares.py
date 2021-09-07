#!/usr/bin/env python
# -*- coding: utf-8 -*-

def mostPopularMovie(list):
    if (len(list) == 0): 
        return 0
    elif (len(list) == 1):
        return list[0]
    else: 
        # We search for the most popular film in the list
        m = list[0] 
        for p in list[1:]: 
            if(p["popularity"]>m["popularity"]):
                m=p
        return m