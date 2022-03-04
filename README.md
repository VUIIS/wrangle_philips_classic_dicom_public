NOTE: Edit the UID root in classic_to_enhanced_Philips_fMRI.py to appropriate value for your site.

Python code to 

1. Re-order classic DICOMs by slice position and temporal position, by updating filenames and InstanceNumber

2. Convert the set of classics to a single enhanced DICOM

Probably only works for Philips fMRI series.

Strategy:

- Assume 3 dimensions stack/slice/time. Assume single stack.

- Fill required DICOM fields only.

- Assign all DICOM groups/modules to shared, unless they need to be in per-frame.

