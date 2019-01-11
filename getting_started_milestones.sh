#!/bin/bash
while [ 1 ]
do
	if [ -e ~/.milestones.$(whoami).$(hostname).txt ]; then
		rm ~/.milestones.$(whoami).$(hostname).txt
	fi

	if grep -Eq "$(whoami).*cd /bin" /var/log/ttylog/cli.ip-10-0-0-4.csv; then
		echo "Milestone 1: command 'cd /bin' found" >> ~/.milestones.$(whoami).$(hostname).txt
	else
		echo "Milestone 1: NOT COMPLETED" >> ~/.milestones.$(whoami).$(hostname).txt
	fi

	if grep -Eq "$(whoami).*okYouAreHERE" /var/log/ttylog/cli.ip-10-0-0-4.csv; then
		echo "Milestone 2: Traversal to okYouAreHERE! found" >> ~/.milestones.$(whoami).$(hostname).txt
	else
		echo "Milestone 2: NOT COMPLETED" >> ~/.milestones.$(whoami).$(hostname).txt
	fi

	if grep -Eq "$(whoami).*man file" /var/log/ttylog/cli.ip-10-0-0-4.csv; then
		echo "Milestone 3: command 'man file' was found" >> ~/.milestones.$(whoami).$(hostname).txt
	else
		echo "Milestone 3: NOT COMPLETED" >> ~/.milestones.$(whoami).$(hostname).txt
	fi

	if grep -Eq "$(whoami).*imatextfiletoo.txt" /var/log/ttylog/cli.ip-10-0-0-4.csv; then
		echo "Milestone 4: command 'cat imatextfiletoo.txt' found" >> ~/.milestones.$(whoami).$(hostname).txt
	else
		echo "Milestone 4: NOT COMPLETED" >> ~/.milestones.$(whoami).$(hostname).txt
	fi

	if grep -Eq "$(whoami).*cat one.txt two.txt three.txt > alltogether.txt" /var/log/ttylog/cli.ip-10-0-0-4.csv; then
		echo "Milestone 5: command 'cat one.txt two.txt three.txt > alltogether.txt' found" >> ~/.milestones.$(whoami).$(hostname).txt
	else
		echo "Milestone 5: NOT COMPLETED" >> ~/.milestones.$(whoami).$(hostname).txt
	fi

	if grep -Eq "$(whoami).*vim editme.txt" /var/log/ttylog/cli.$(hostname).csv; then
		echo "Milestone 6: command 'vim editme.txt' found" >> ~/.milestones.$(whoami).$(hostname).txt
	else
		echo "Milestone 6: NOT COMPLETED" >> ~/.milestones.$(whoami).$(hostname).txt
	fi

	#if grep -q -o -a -m 1 -h -r "edurange5meow.jpg" cli.ip-10-0-0-4.csv && grep -q -o -a -m 1 -h -r "edurange001.gif" cli.ip-10-0-0-4.csv && grep -q -o -a -m 1 -h -r "4edurange.jpeg" cli.ip-10-0-0-4.csv && grep -q -o -a -m 1 -h -r "edurange006weeeeeee.png" cli.ip-10-0-0-4.csv && grep -q -o -a -m 1 -h -r "002edurange.jpg" cli.ip-10-0-0-4.csv && grep -q -o -a -m 1 -h -r "edurange3.GIF" cli.ip-10-0-0-4.csv | grep $(whoami); then
		#echo "Milestone 7: all images were found" >> /var/log/ttylog/milestones.$(whoami).$(hostname).txt
	#else
		#echo "Milestone 7: NOT COMPLETED" >> /var/log/ttylog/milestones.$(whoami).$(hostname).txt
	#fi
	sleep 60s
done
