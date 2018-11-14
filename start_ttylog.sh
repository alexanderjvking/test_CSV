 #!/bin/bash

 if [ -z "$SSH_ORIGINAL_COMMAND" ]; then

     TTY_CMD=$(tty)
     TTY=${TTY_CMD:5}
     #HN=$(cat /var/log/ttylog/nickname)
     #HOST=$(echo $HN | awk -F. '{print $(NF - 1)}')
     #EXP=$(echo $HN | awk -F. '{print $(NF - 1)}')
     #PROJ=$(echo $HN | awk -F. '{print $(NF)}')

     sudo mkdir -p /var/log/ttylog/

     if [ -e "/var/log/ttylog/count.$HOST" ]; then
         CNT=$(cat /var/log/ttylog/count.$HOST)
         let CNT++
         echo $CNT > /var/log/ttylog/count.$HOST
     else
         sudo touch /var/log/ttylog/count.$HOST
         sudo chmod ugo+rw /var/log/ttylog/count.$HOST
         echo "0" > /var/log/ttylog/count.$HOST
         CNT=$(cat /var/log/ttylog/count.$HOST)
     fi

     export TTY_SID=$CNT
     LOGPATH=/var/log/ttylog/ttylog.$HOST.$CNT

     sudo touch $LOGPATH
     sudo chmod ugo+rw $LOGPATH

     echo "starting session w tty_sid:$CNT" >> $LOGPATH

     sudo /usr/local/src/ttylog/ttylog $TTY >> $LOGPATH 2>/dev/null &

     bash
     echo "END tty_sid:$CNT" >> $LOGPATH

 elif [ "$(echo ${SSH_ORIGINAL_COMMAND} | grep '^sftp' )" ]; then

     #sudo touch /var/log/tty.log
     #sudo chmod ugo+rw /var/log/tty.log
     #echo "$SSH_ORIGINAL_COMMAND" >> /var/log/tty.log
     /usr/lib/openssh/sftp-server
     #exec ${SSH_ORIGINAL_COMMAND}

 elif [ "$(echo ${SSH_ORIGINAL_COMMAND} | grep '^scp' )" ]; then

     #HN=$(cat /var/emulab/boot/nickname)
     #HOST=$(echo $HN | awk -F. '{print $(NF - 2)}')
     #EXP=$(echo $HN | awk -F. '{print $(NF - 1)}')
     #PROJ=$(echo $HN | awk -F. '{print $(NF)}')

     #LOGPATH=/var/log/ttylog/ttylog.null.$HOST
     #touch $LOGPATH
     #echo "$SSH_ORIGINAL_COMMAND" >> $LOGPATH
     exec ${SSH_ORIGINAL_COMMAND}

 elif [ "$(echo ${SSH_ORIGINAL_COMMAND})" ]; then

     #HN=$(cat /var/emulab/boot/nickname)
     #HOST=$(echo $HN | awk -F. '{print $(NF - 2)}')
     #EXP=$(echo $HN | awk -F. '{print $(NF - 1)}')
     #PROJ=$(echo $HN | awk -F. '{print $(NF)}')

     #LOGPATH=/var/log/ttylog/ttylog.null.$HOST
     #echo "$SSH_ORIGINAL_COMMAND" >> $LOGPATH
     exec ${SSH_ORIGINAL_COMMAND}

 fi
