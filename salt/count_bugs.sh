#! /bin/bash
main () 
{
local old_pwd=$(pwd)
cd downloads/bugs/fixes

local total=$(wc -l < salt.txt)
echo "total number of bugs with fixes:"
echo $total

echo "Number of issues with a fix that is a pull request:"
grep -c pull salt.txt

echo "Number of issues with a fix that is a commit but no pr fix:"
grep -v -c pull salt.txt #| grep -c commit

cd ../.. 
echo "Number of issues with fix but without test case:"
local withouttest=$(grep -c 'Warning: could not find test case for' logs)
echo $withouttest

echo "Number of issues with fix and test cases:"
local withTtest="$(($total-$withouttest))"
echo  $withTtest
# cd $old_pwd

cd $old_pwd
}

main