#!/usr/bin/env python
#
# Parse json output of https://github.com/innolitics/dicom-standard/standard to get
# an organized list of DICOM tags

import copy
import json
import os
import yaml

std_dir = 'dicom-standard/standard'

with open(os.path.join(std_dir,'ciods.json')) as f:
    ciods = json.load(f)
with open(os.path.join(std_dir,'ciod_to_modules.json')) as f:
    ciod_to_modules = json.load(f)
with open(os.path.join(std_dir,'module_to_attributes.json')) as f:
    module_to_attributes = json.load(f)
with open(os.path.join(std_dir,'attributes.json')) as f:
    attributes = json.load(f)

# We just need Enhanced MR modules
emr_modules = [x['moduleId'] for x in ciod_to_modules 
    if x['ciodId']=='enhanced-mr-image']

# Get all the attribute paths that match each module
paths = list()
for m in emr_modules:
    paths = paths + [x['path'] for x in module_to_attributes if x['moduleId']==m]

# Replace tags with tag names and split to list of tags
dotpaths = copy.deepcopy(paths)
for ip, path in enumerate(paths):
    tags = path.split(':')[1:]
    for it,tag in enumerate(tags):
        tags[it] = [x['keyword'] for x in attributes if x['id']==tag][0]
    dotpaths[ip] = '.'.join(tags)
    paths[ip] = tags

# Testing
#paths = [x for x in paths if 'ReasonForVisit' in x[0]]

  
  # Put into hierarchy recursively. This:
#    [['A'], ['B', 'C'], ['B','D'], ['B', 'C', 'E'],['B', 'C', 'G']]
#
# Should end up as this:
# { 
#     'A': {},
#     'B': {
#         'C': {
#             'E': {},
#             'G': {},
#         },
#         'D': {},
#     },
# }
def pull_all(paths):
    
    if isinstance(paths, list):
        # The initial call with list of paths given
        ufirsts = {k: [] for k in sorted(list({x[0] for x in paths}))}
    else:
        # Otherwise we're getting a dict from a recursive call
        ufirsts = paths

    for k in ufirsts.keys():
        ufirsts[k] = [p[1:] for p in paths if p[0]==k and len(p[1:])>0]
        if ufirsts[k]:
            ufirsts[k] = pull_all(ufirsts[k])
    
    return ufirsts


def pull_first(paths):
    ufirsts = [k for k in sorted(list({x[0] for x in paths}))]
    return ufirsts


# Testing
#paths = [['A'], ['B', 'C'], ['B','D'], ['B', 'C', 'E'],['B', 'C', 'G']]

newpaths = pull_all(paths)
rootpaths = pull_first(paths)

with open('enhanced-mr-image.yaml', 'w') as of:
    yaml.dump(newpaths, of, default_flow_style=False)

with open('enhanced-mr-image-root.yaml', 'w') as of:
    yaml.dump(rootpaths, of, default_flow_style=False)

#with open('enhanced-mr-image-pathlist.yaml', 'w') as of:
#    yaml.dump(dotpaths, of, default_flow_style=False)
