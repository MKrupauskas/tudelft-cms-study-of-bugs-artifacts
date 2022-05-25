#! /bin/bash
NUMBER_OF_BUGS=$1
NAME_OF_OUTPUT_FILE=$2
main () 
{

local lines=$(python3 get_n_random_samples.py $NUMBER_OF_BUGS)
local old_pwd=$(pwd)
cd downloads/bugs/fixes
local result=""
for linenumber in $lines; do
  local fix=$(sed -n "${linenumber}p" < salt.txt)
  result="${result}${fix}\n"
done
cd $old_pwd
touch "${NAME_OF_OUTPUT_FILE}_sampled_numbers.txt"
echo $lines > "${NAME_OF_OUTPUT_FILE}_sampled_numbers.txt"

touch "${NAME_OF_OUTPUT_FILE}.txt"
echo -e "$result" > "${NAME_OF_OUTPUT_FILE}.txt"  #change name of outputfile everytime you run this function

}
main