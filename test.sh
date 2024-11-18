#!/bin/bash

# Loop for 3 runs
for n in {1..3}; do
  # Choose meaningful fixed values for each parameter
  if [ $n -eq 1 ]; then
    CACHE_SIZE=128  # Cache size in KB
    BLOCK_SIZE=16  # Block size in bytes
    ASSOCIATIVITY=4  # 4-way set associative
    PHYSICAL_MEM_SIZE=1024  # Physical memory size in MB
  elif [ $n -eq 2 ]; then
    CACHE_SIZE=256
    BLOCK_SIZE=32
    ASSOCIATIVITY=8
    PHYSICAL_MEM_SIZE=2048
  else
    CACHE_SIZE=512
    BLOCK_SIZE=64
    ASSOCIATIVITY=16
    PHYSICAL_MEM_SIZE=4096
  fi

  REPLACEMENT_POLICY="rr" # Fixed replacement policy

  # Define trace file name (assume it remains constant)
  TRACE_FILE="A-9_new_1.5.pdf.trc"

  # Run the command and save the output
  OUTPUT_FILE="Team_11_Sim_${n}_M#2.txt"
  python3 main.py -s $CACHE_SIZE -b $BLOCK_SIZE -a $ASSOCIATIVITY -r $REPLACEMENT_POLICY -p $PHYSICAL_MEM_SIZE -n $n -u 50 -f $TRACE_FILE > $OUTPUT_FILE

  echo "main.py -s $CACHE_SIZE -b $BLOCK_SIZE -a $ASSOCIATIVITY -r $REPLACEMENT_POLICY -p $PHYSICAL_MEM_SIZE -n $n -u 50 -f $TRACE_FILE"

done

echo "All runs completed. Results saved to Team_11_Sim_<n>_M#2.txt."
