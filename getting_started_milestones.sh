#!/bin/bash

if [ -e milestones.$(whoami).$(hostname).txt ]; then
	rm milestones.$(whoami).$(hostname).txt
fi

if grep -q -o -a -m 1 -h -r "cd /bin" cli.ip-10-0-0-4.csv; then
	echo "Milestone 1: command 'cd /bin' found" >> milestones.$(whoami).$(hostname).txt
else
	echo "Milestone 1: NOT COMPLETED" >> milestones.$(whoami).$(hostname).txt
fi

if grep -q -o -a -m 1 -h -r "okYouAreHERE" cli.ip-10-0-0-4.csv; then
	echo "Milestone 2: Traversal to okYouAreHERE! found" >> milestones.$(whoami).$(hostname).txt
else
	echo "Milestone 2: NOT COMPLETED" >> milestones.$(whoami).$(hostname).txt
fi

if grep -q -o -a -m 1 -h -r "man file" cli.ip-10-0-0-4.csv; then
	echo "Milestone 3: command 'man file' was found" >> milestones.$(whoami).$(hostname).txt
else
	echo "Milestone 3: NOT COMPLETED" >> milestones.$(whoami).$(hostname).txt
fi

if grep -q -o -a -m 1 -h -r "cat imatextfiletoo.txt" cli.ip-10-0-0-4.csv; then
	echo "Milestone 4: command 'cat imatextfiletoo.txt' found" >> milestones.$(whoami).$(hostname).txt
else
	echo "Milestone 4: NOT COMPLETED" >> milestones.$(whoami).$(hostname).txt
fi

if grep -q -o -a -m 1 -h -r "cat one.txt two.txt three.txt > alltogether.txt" cli.ip-10-0-0-4.csv; then
	echo "Milestone 5: command 'cat one.txt two.txt three.txt > alltogether.txt' found" >> milestones.$(whoami).$(hostname).txt
else
	echo "Milestone 5: NOT COMPLETED" >> milestones.$(whoami).$(hostname).txt
fi

if grep -q -o -a -m 1 -h -r "vim editme.txt" cli.ip-10-0-0-4.csv; then
	echo "Milestone 6: command 'vim editme.txt' found" >> milestones.$(whoami).$(hostname).txt
else
	echo "Milestone 6: NOT COMPLETED" >> milestones.$(whoami).$(hostname).txt
fi

if grep -q -o -a -m 1 -h -r "edurange5meow.jpg" cli.ip-10-0-0-4.csv && grep -q -o -a -m 1 -h -r "edurange001.gif" cli.ip-10-0-0-4.csv && grep -q -o -a -m 1 -h -r "4edurange.jpeg" cli.ip-10-0-0-4.csv && grep -q -o -a -m 1 -h -r "edurange006weeeeeee.png" cli.ip-10-0-0-4.csv && grep -q -o -a -m 1 -h -r "002edurange.jpg" cli.ip-10-0-0-4.csv && grep -q -o -a -m 1 -h -r "edurange3.GIF" cli.ip-10-0-0-4.csv; then
	echo "Milestone 7: all images were found" >> milestones.$(whoami).$(hostname).txt
else
	echo "Milestone 7: NOT COMPLETED" >> milestones.$(whoami).$(hostname).txt
fi
