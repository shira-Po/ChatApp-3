#!/bin/bash

# Get the list of sh files in the scripts directory
scripts_dir="scripts"
sh_files=$(find "$scripts_dir" -type f -name "*.sh")

# For each sh file, run it
for sh_file in $sh_files; do
  echo "Running $sh_file"
  bash "$sh_file"
  echo -e "\n **** \n"

done


