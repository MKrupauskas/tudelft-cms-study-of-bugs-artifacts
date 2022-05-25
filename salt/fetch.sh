#! /bin/bash
DOWNLOADS=$1
GH_TOKEN=$2

if [ "$#" -ne 2 ]; then
    echo "usage: fetch.sh DOWNLOADS GH_TOKEN"
    exit
fi

#TODO CHECK FILE PATH PARAMETERs here
echo "Fetching Salt Bugs..."
python3 fetch_bugs.py $DOWNLOADS/bugs/salt.txt \
        $DOWNLOADS/bugs/fixes/bug_issue_descriptions $DOWNLOADS/bugs/salt.json $GH_TOKEN

echo "Cloning salt repository..."
./clone.sh $DOWNLOADS/repos


# PHASE 2
echo "Finding Test Cases & Fixes (Post-Filtering)..."
echo "This requires some time. Please bear with us ..."
./find_fixes.sh $DOWNLOADS/bugs \
        $DOWNLOADS/bugs/fixes/bug_issue_descriptions $DOWNLOADS/repos \
        $DOWNLOADS/bugs/fixes $GH_TOKEN 2>&1 | tee $DOWNLOADS/logs
echo "Done!"


# The code in this file is a modification of the code from https://github.com/hephaestus-compiler-project/types-bug-study-artifact/blob/master/LICENSE
# MIT License

# Copyright (c) 2021 Stefanos Chaliasos, Thodoris Sotiropoulos, Georgios-Petros Drosos, Charalambos Mitropoulos, Dimitris Mitropoulos, and Diomidis Spinellis

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.