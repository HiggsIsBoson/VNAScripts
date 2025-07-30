#!/usr/bin/env python

from vna_solib import vna

v = vna()

if v.get_tool_keys():
    v.tool_keys(False)
    v.tool_entry(False)
else:
    v.tool_keys(True)
    pass
