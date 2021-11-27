#!/bin/bash

# note: some of the below numbers currently act as placeholders.
# should get up-to-date numbers from Component Selection team.

python ./src/main.py \
# examples - update based on code
--spectral_lower 1590 \
--spectral_upper 1680 \
--spectral_res 1.5 \ 
--foreoptics_focal_len 100 \
--groove_density 300 \
# etc
--output_folder './outputs'
