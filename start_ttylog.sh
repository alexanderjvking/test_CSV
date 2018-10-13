 #!/bin/bash

 if [ -z "$SSH_ORIGINAL_COMMAND" ]; then

     TTY_CMD=$(tty)
     TTY=${TTY_CMD:5:15}
     HN=$(cat /var/emulab/boot/nickname)
     HOST=$(echo $HN | awk -F. '{print $(NF - 2)}')
     EXP=$(echo $HN | awk -F. '{print $(NF - 1)}')
     PROJ=$(echo $HN | awk -F. '{print $(NF)}')

     sudo mkdir -p /var/log/ttylog/

     if [ -e "/proj/$PROJ/exp/$EXP/count.$HOST" ]; then
         CNT=$(cat /proj/$PROJ/exp/$EXP/count.$HOST)
         let CNT++
         echo $CNT > /proj/$PROJ/exp/$EXP/count.$HOST
     else
         sudo touch /proj/$PROJ/exp/$EXP/count.$HOST
         sudo chmod ugo+rw /proj/$PROJ/exp/$EXP/count.$HOST
         echo "0" > /proj/$PROJ/exp/$EXP/count.$HOST
         CNT=$(cat /proj/$PROJ/exp/$EXP/count.$HOST)
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
