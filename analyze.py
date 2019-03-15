#!/usr/bin/python
# clampz
# analyze snoopy w ttylog
# 7/27/18

# find ttylog commands and associated shell pids
# for each ttlog sess id find all execves with that ttylog sess id
# for each ttylog find the ones relating to that ttylog sess id - marked from the start_ttylog script

import csv
import string
import sys
import os.path
import subprocess
import logging
import re

#logpath = '/var/log/ttylog/analysis.log.'; preprocpath = '/var/log/ttylog/preproc_snoopy.log' # prod
logpath = './analysis.log'; preprocpath = './preproc_snoopy.log' #dbg
logging.basicConfig(filename=logpath, filemode='w', level=logging.DEBUG)

logging.debug("running with __name__ == {}".format(__name__))

bash_op_list = ['=', '<', '>', '<<', '>>', '<&', '>&', '<<-', '<>', '>|', '|', ';', '{', '}',';;', '(', ')', '&', '||', '&&', '!']

# prints the string given but with all
# hex bytes in blacklist replaced with tags
# to differentiate.

unprintable_list = {'00': '<NUL>', '01': '<SOH>', '02': '<STX>', '03': '<ETX>', '04': '<EOT>', '05': '<ENQ>', '06': '<ACK>', '07': '<BEL>', '08': '<BS>', '09': '<HT>', '0a': '<NL>', '0b': '<VT>', '0c': '<NP>', '0d': '<CR>', '0e': '<SO>', '0f': '<SI>', '10': '<DLE>', '11': '<DC1>', '12': '<DC2>', '13': '<DC3>', '14': '<DC4>', '15': '<NAK>', '16': '<SYN>', '17': '<ETB>', '18': '<CAN>', '19': '<EM>', '1a': '<SUB>', '1b': '<ESC>', '1c': '<FS>', '1d': '<GS>', '1e': '<RS>', '1f': '<US>', '7f': '<DEL>', '80': '<EURO>', '81': '<81>', '82': '<82>', '83': '<83>', '84': '<84>', '85': '<85>', '86': '<86>', '87': '<87>', '88': '<88>', '89': '<89>', '8a': '<8A>', '8b': '<8B>', '8c': '<8C>', '8d': '<8D>', '8e': '<8E>', '8f': '<8F>', '90': '<90>', '91': '<91>', '92': '<92>', '93': '<93>', '94': '<94>', '95': '<BULL>', '96': '<96>', '97': '<97>', '98': '<98>', '99': '<99>', '9a': '<9A>', '9b': '<9b>', '9c': '<L_OE>', '9d': '<9D>', '9e': '<9E>', '9f': '<9F>', 'a0': '<A0>', 'a1': '<A1>', 'a2': '<CENT>', 'a3': '<POUND>', 'a4': '<CURR>', 'a5': '<YEN>', 'a6': '<A6>', 'a7': '<SECT>', 'a8': '<UMLT>', 'a9': '<COPY>', 'aa': '<ORDF>', 'ab': '<AB>', 'ac': '<NOT>', 'ad': '<SHY>', 'ae': '<REG>', 'af': '<MACR>', 'b0': '<DEG>', 'b1': '<PLSMN>', 'b2': '<B2>', 'b3': '<B3>', 'b4': '<ACUTE>', 'b5': '<MICRO>', 'b6': '<PARA>', 'b7': '<MIDDOT>', 'b8': '<CEDIL>', 'b9': '<B9>', 'ba': '<ORDM>', 'bb': '<BB>', 'bc': '<BC>', 'bd': '<BD>', 'be': '<BE>', 'bf': '<BF>', 'c0': '<C0>', 'c1': '<C1>', 'c2': '<C2>', 'c3': '<C3>', 'c4': '<C4>', 'c5': '<C5>', 'c6': '<C6>', 'c7': '<C7>', 'c8': '<C8>', 'c9': '<C9>', 'ca': '<CA>', 'cb': '<CB>', 'cc': '<CC>', 'cd': '<CD>', 'ce': '<CE>', 'cf': '<CF>', 'd0': '<D0>', 'd1': '<D1>', 'd2': '<D2>', 'd3': '<D3>', 'd4': '<D4>', 'd5': '<D5>', 'd6': '<D6>', 'd7': '<MUL>', 'd8': '<D8>', 'd9': '<D9>', 'da': '<DA>', 'db': '<DB>', 'dc': '<DC>', 'dd': '<DD>', 'de': '<DE>', 'df': '<DF>', 'e0': '<E0>', 'e1': '<E1>', 'e2': '<E2>', 'e3': '<E3>', 'e4': '<E4>', 'e5': '<E5>', 'e6': '<E6>', 'e7': '<E7>', 'e8': '<E8>', 'e9': '<E9>', 'ea': '<EA>', 'eb': '<EB>', 'ec': '<EC>', 'ed': '<ED>', 'ee': '<EE>', 'ef': '<EF>', 'f0': '<F0>', 'f1': '<F1>', 'f2': '<F2>', 'f3': '<F3>', 'f4': '<F4>', 'f5': '<F5>', 'f6': '<F6>', 'f7': '<F7>', 'f8': '<F8>', 'f9': '<F9>', 'fa': '<FA>', 'fb': '<FB>', 'fc': '<FC>', 'fd': '<FD>', 'fe': '<FE>', 'ff': '<FF>'}

def listify_hexstr(hexbuf):
	newbuf = hexbuf
	newbufbytes = []
	while len(newbuf) > 0:
		newbufbytes.append(newbuf[:2])
		newbuf = newbuf[2:]
	return newbufbytes

def revealhex(buf):
	bufhex = buf.encode("hex")
	l_bufhex = listify_hexstr( bufhex )
	for i in unprintable_list:
		if i in l_bufhex:
			while i in l_bufhex:
				l_bufhex[l_bufhex.index(i):l_bufhex.index(i) + 1] = listify_hexstr( unprintable_list[i].encode("hex") )
	bufhex = "".join(l_bufhex)
	return bufhex.decode("hex")

# split string on more than one delimiter
def multi_delim_split(s, seps):
    res = [s]
    for sep in seps:
        s, res = res, []
        for seq in s:
            res += seq.split(sep)
    return res

# evaluate the control characters as a terminal would (mainly for backspace characters)
def decode(input_string):
    # Initial state
    # String is stored as a list because
    # python forbids the modification of
    # a string
    buf = []
    i_line = 0
    i_stream_line = 0
    i_buf = 0
    buf.append([])

    while i_stream_line < len(input_string):
	if input_string[i_stream_line] == '\x08':
	     i_buf -= 0 if i_buf == 0 else 1
             i_stream_line += 1
        elif input_string[i_stream_line] == '\x1b' and input_string[i_stream_line + 1] == '[':
             i_stream_line += 2
             if input_string[i_stream_line] == 'K':
                 """ erase to end of line """
                 buf[i_line] = buf[i_line][:i_buf]
                 i_stream_line += 1
             elif (input_string[i_stream_line] == '@') or (input_string[i_stream_line] in string.digits and input_string[i_stream_line + 1] == '@'):
                 """ make room for n characters at cursor """
                 n = int(input_string[i_stream_line]) if input_string[i_stream_line] in string.digits else 1
                 i = 0
                 while i < n:
                     if i_buf < len(buf[i_line]):
                         buf[i_line][i_buf] = ''
                     else:
                         buf[i_line] += ''
                     i_buf += 1
                     i += 1
                 i_stream_line += 2 if input_string[i_stream_line] in string.digits else 1
             elif (input_string[i_stream_line] == 'C') or (input_string[i_stream_line] in string.digits and input_string[i_stream_line + 1] == 'C'):
                 """ move the cursor forward n columns """
                 n = int(input_string[i_stream_line]) if input_string[i_stream_line] in string.digits else 1
                 i_buf += n
                 i_stream_line += 2 if input_string[i_stream_line] in string.digits else 1
             elif (input_string[i_stream_line] == 'P') or (input_string[i_stream_line] in string.digits and input_string[i_stream_line + 1] == 'P'):
                 """ delete n chars  """
                 n = int(input_string[i_stream_line]) if input_string[i_stream_line] in string.digits else 1
                 buf[i_line] = buf[i_line][:i_buf] + buf[i_line][i_buf + n:]
                 i_stream_line += 2 if input_string[i_stream_line] in string.digits else 1
        else:
             if i_buf < len(buf[i_line]):
                 #import pdb; pdb.set_trace()
                 buf[i_line][i_buf] = input_string[i_stream_line]
             else:
                 buf[i_line] += input_string[i_stream_line]
             i_buf += 1
             i_stream_line += 1
    buf[i_line] = ''.join(buf[i_line])
    #i_line += 1
    # We transform our "list" string back to a real string
    return "".join(buf)

if __name__ == "__main__":
    logging.debug("running main with len(sys.argv) == {}".format(len(sys.argv)))
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print("usage:\n$ analyze.py <snoopy log file> <ttylog log file> <out csv file> [-preproc]\nexiting.")
        logging.critical("usage:\n$ analyze.py <snoopy log file> <ttylog log file> <out csv file> [-preproc]")
        exit(1)
    snoopylog = sys.argv[1]
    ttylog = sys.argv[2]
    csvfile = sys.argv[3]
    try:
        if sys.argv[4] == '-preproc':
            preproc = True 
    except IndexError:
        preproc = False

    logging.debug("using {}, {} and outputting to {}.".format(snoopylog, ttylog, csvfile))

    if not os.path.isfile(snoopylog) or not os.path.isfile(ttylog):
        logging.critical("there's a problem with one or both of the log files! aborting.")
        exit(1)

    f = open(snoopylog, 'r')

    s = f.read()

    lines = s.splitlines()

    ttylog_sessions = []

    user = ''
    host = ''
	
    # initialize list of terminal sessions and what our shell prompt looks like
    for i in range(0, len(lines)):
        if 'sudo /usr/local/src/ttylog/ttylog pts' in lines[i]:
            split_line = lines[i].split()
            for x in split_line:
                if 'un:' in x:
                    user = x.split('un:')[-1].split(' ')[0]
                if 'hn:' in x:
                    host = x.split('hn:')[-1].split(' ')[0]
            prompt = '@{}'.format(host)
            if 'bash' in lines[i-1] or 'bash' in lines[i+1]:
                split_line = ( lines[i-1] if 'bash' in lines[i-1] else lines[i+1] ).split()
                for x in split_line:
                    if 'tty_sid:' in x and x not in ttylog_sessions:
                        ttylog_sessions.append( x )

    sessions = {}
    snoopy_lines = []

    # find all relevant snoopy log events and associate with relevant terminal session
    for s in ttylog_sessions:
        sessions[s] = {}
        sessions[s]['snoopy'] = []
        for line in lines:
            if s in line: #tty_sid:num in line
                snoopy_lines.append(line)
                # append a dict {snoopy_cmd : timestamp}
                sessions[s]['snoopy'].append( { ' '.join(line.split()[5:]) :  ' '.join(line.split()[:3])  } )
        # trim out all the noise at the beginning
        sessions[s]['snoopy'] = sessions[s]['snoopy'][8:]

    logging.debug("found sessions {}".format(repr(sessions.keys())))

    f.close()

    if preproc:
        f = open(preprocpath, 'w')
        for line in snoopy_lines:
            f.write(line+'\n')
        f.close()
        print('wrote preprocessed snoopy data to {}'.format(preprocpath)) 
        logging.info('wrote preprocessed snoopy data to {}'.format(preprocpath)) 

    f = open(ttylog, 'r')
    s = f.read()
    lines = s.splitlines()

    append = False
    tty_sess = ''
    cmd = ''
    tty_user = ''
    # for every line in ttylog detect the beginning and end of a given ttylog session and grab everything in between
    ordering = {}
    user_order = {}
    for l in lines:
        if 'starting session w tty_sid' in l:
            for s in ttylog_sessions:
                if s in l:
                    append = True
                    tty_sess = s
                    ordering[tty_sess] = []
                    user_order[tty_sess] = []
                    count = -1 
                    sessions[tty_sess]['ttylog'] = {}
                    cmd = ''
                    tty_user = ''
            continue
        if append:
            # append the line to ttylog session list
            if 'END {}'.format(tty_sess) in l:
                append = False
            else:
                # seperate the command from its output
                if prompt in l:
                    cmd = l.split('$', 1)[-1][1:]
                    tty_user = l.split(']0',1)[1].split('@',1)[0][1:]
                    if cmd != '':
                        count += 1
                        ordering[tty_sess].append(cmd)
                        sessions[tty_sess]['ttylog'][str(count)+cmd] = []
                        user_order[tty_sess].append(tty_user)
                elif cmd != '':
                    sessions[tty_sess]['ttylog'][str(count)+cmd].append(l)

    f.close()

    logging.debug("the sessions dict looks like {}, about to analyze".format(repr(sessions)))

    # write output to file

    csvfile = open(csvfile, 'w')
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='%', quoting=csv.QUOTE_MINIMAL)

    # for every line in the ttylog commands associate all related snoopy information include timestamp as its own collumn
    # timestamp, ttylog command, ttylog output, snoopy cmd(s) - the form of the csv will be as follows:
    # timestamp, cwd, command as appears in ttylog, command output, {one or more commands as shown in snoopy}
    for s in ttylog_sessions:
        if 'ttylog' not in sessions[s].keys():
            continue
        ttylogs = ordering[s]
        ttylog_user_data = user_order[s]
        #for ttylog_entry in ttylogs:
        for count in range(0, len(ttylogs)):
            ttylog_entry = ttylogs[count]
            ttylog_users = ttylog_user_data[count]
            ttylog_cmd = decode(ttylog_entry)
            ttylog_return_data = sessions[s]['ttylog'][str(count)+ttylog_entry]
            logging.debug('starting csv entry loop for command {}, hex for command: {}'.format(revealhex(ttylog_entry), ttylog_entry.encode('hex')))
            snoopylogs = sessions[s]['snoopy']
            csv_row = []
            i = 0
            # we've got to loop over the snoopy log entries this way so we can avoid running into doubles of the same command
            # this should appear somewhat chronologically
            while i < len(snoopylogs):
                snoopy_entry = snoopylogs[i]
                snoopy_data = list(snoopy_entry.keys())[0]
                snoopy_cmd = snoopy_data.split(': ')[-1]
                ttylog_cmd_list = [re.sub(r"^\s+|\s+$",'',j) for j in multi_delim_split(ttylog_cmd, bash_op_list)]
                found = False
                for c in ttylog_cmd_list:
                    if re.match(snoopy_cmd, c):
                        if re.match(snoopy_cmd, c).pos == 0:
                            found = True
                if found:
                    logging.debug('found matching snoopy entry for command {}'.format(decode(ttylog_entry)))
                    del snoopylogs[i]
                    timestamp = snoopy_entry[snoopy_data]
                    cwd = snoopy_data.split()[3][4:]
                    if len(csv_row) == 0:
                        csv_row = ['CMBEGIN', ttylog_users, timestamp, cwd, decode(ttylog_entry), decode('\n'.join([decode(j) for j in ttylog_return_data])).replace(',','%'), snoopy_cmd]
                    else:
                        csv_row.append(snoopy_cmd)
                    ttylog_cmd = ttylog_cmd.replace(snoopy_cmd, '', 1)
                else:
                    i += 1
            if '' != decode(ttylog_entry):
                logging.debug('writing csv row for command {}'.format(revealhex(ttylog_entry)))
                csvwriter.writerow( csv_row if len(csv_row) != 0 else [ 'CMBEGIN', ttylog_users, '','', decode(ttylog_entry), '!TRUNCATED TO 500L! ' + decode('\n'.join(ttylog_return_data[:501])).replace(',','%') if len(ttylog_return_data) > 500 else decode('\n'.join(ttylog_return_data)).replace(',','%'), ''] )
    csvfile.close()


