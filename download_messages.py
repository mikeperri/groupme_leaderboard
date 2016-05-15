import groupy
import sys
import csv
import unicodedata
import time
import re

OUTFILE_PREFIX = 'groupme_'

def setup():
    if len(sys.argv) < 2:
        print('Usage: python3 download_messages.py "MY GROUP NAME"')

    group_name = sys.argv[1]

    matching_groups = groupy.Group.list().filter(name__eq=group_name)

    if len(matching_groups) == 0:
        print('Group "' + group_name + '" was not found')
        sys.exit(1)

    group = matching_groups[0]
    members = group.members()
    messages = group.messages()

    print('Fetching data for ' + group_name + ' (' + str(group.message_count) + ' messages)...')

    safe_group_name = re.sub(r'\W+', '', group_name) # remove non-alphanumeric chars
    outfile_name = OUTFILE_PREFIX + safe_group_name + '.csv'

    return outfile_name, members, messages

def write_messages(outfile_name, members, messages):
    def write_message_row(writer, message):
        created_at = int(message.created_at.timestamp())
        favorited_by = str(','.join(message.favorited_by))
        if message.text != None:
            text = str(unicodedata.normalize('NFKD', message.text).encode('ascii', 'ignore'), 'ascii')
            #text = message.text
        else:
            text = ''
        writer.writerow([str(created_at), str(message.user_id), favorited_by, text])

    with open(outfile_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')

        writer.writerow(map(lambda m: m.user_id, members))
        writer.writerow(map(lambda m: m.nickname, members))

        while messages:
            for message in messages:
                write_message_row(writer, message)
            messages = messages.older()

    print('Wrote data to ' + outfile_name)

def main():
    write_messages(*setup())

main()
