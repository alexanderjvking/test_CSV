# No arguments needed, will get them from machine
#$fh=new IO::File("/var/emulab/boot/nickname");
#while(<$fh>)
#{
#	$line = $_;
#	$line =~ s/\R//g;
#   @items = split /\./, $line;
#   $host=$items[0];
#   $exp=$items[1];
#   $proj=$items[2];
#}
#print "$host $exp $proj\n";
#$fn = "/proj/" . $proj . "/exp/" . $exp . "/logs/cli." . $host . ".csv";
#$time=time;
#if (-e $fn)
#{
#    system("mv $fn $fn.$time");
#}
system("sed -i 's/\"\[uid:\%{uid} sid:\%{sid} tty:\%{tty} cwd:\%{cwd} filename:\%{filename}\]: \%{cmdline}\"/\"\[un:\%{username} tty_sid:\%{env:TTY_SID} hn:\%{hostname} cwd:\%{cwd} filename:\%{filename}\]: \%{cmdline}\"/g' /usr/local/src/snoopy-install-from.git/config.h")
system("cd /usr/local/src/snoopy-install-from.git")
system("make")
system("make install")
while(1)
{
    system("cat /var/log/ttylog/ttylog.* > /var/log/ttylog/alltty.");
    system("python /usr/local/src/analyze.py /var/log/auth.log /var/log/ttylog/alltty." . " /var/log/ttylog/cli" . ".csv");
    #system("cp /var/log/ttylog/cli." . $host . ".csv /proj/" . $proj . "/exp/" . $exp . "/logs/cli." . $host . ".csv");
    sleep(60);
}
