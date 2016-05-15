import sys
import csv
import pprint
import datetime

def get_infile_name():
    if len(sys.argv) < 2:
        print('Usage: python3 print_stats.py groupme_MYGROUPNAME.csv')
        sys.exit(1)

    infile_name = sys.argv[1]
    return infile_name

def print_stats(memberdict, uid_to_name, first_message_date):

    def print_leaders(memberdict, uid_to_name, key, display_key):
        print(display_key + ' leaders:')
        leaders = sorted(memberdict, key=lambda uid: float(memberdict[uid][key]), reverse=True)
        for uid in leaders:
            print('   ' + uid_to_name[uid] + ' (' + str(memberdict[uid][key]) + ')')
        print('')

    print('First message on ' + first_message_date)
    print('')

    for uid, member in memberdict.items():
        member_name = uid_to_name[uid]

        print('=== ' + member_name + ' ===')
        print('Messages: ' + str(member['messages']))
        print('Modest sweeps: ' + str(member['modest_sweeps']))
        print('Sweeps: ' + str(member['sweeps']))
        print('Sweeps per message: ' + str(member['sweeps_per_message']))
        print('Likes given: ' + str(member['total_likes_given']))
        for l_uid, count in member['liked'].items():
            print('    ' + uid_to_name[l_uid] + ': ' + str(count))
        print('Likes recieved: ' + str(member['total_likes_received']))
        for l_uid, count in member['liked_by'].items():
            print('    ' + uid_to_name[l_uid] + ': ' + str(count))
        print('Likes per message: ' + str(member['likes_per_message']))
        print('Given to received ratio: ' + str(member['given_to_received']))
        print('')

    print('')
    print('')

    print_leaders(memberdict, uid_to_name, 'messages', 'Messages Sent')
    print_leaders(memberdict, uid_to_name, 'sweeps', 'Sweep')
    print_leaders(memberdict, uid_to_name, 'modest_sweeps', 'Modest Sweep')
    print_leaders(memberdict, uid_to_name, 'sweeps_per_message', 'Sweep Per Message')
    print_leaders(memberdict, uid_to_name, 'total_likes_given', 'Likes Given')
    print_leaders(memberdict, uid_to_name, 'total_likes_received', 'Likes Received')
    print_leaders(memberdict, uid_to_name, 'given_to_received', 'Given to Received Ratio')
    print_leaders(memberdict, uid_to_name, 'likes_per_message', 'Likes Per Message')

def read_csv(infile_name):
    def build_memberdict(uids):
        memberdict = {}

        def build_liked_dict(uids):
            return {uid: 0 for uid in uids}

        for uid in uids:
            memberdict[uid] = {
                'messages': 0,
                'modest_sweeps': 0,
                'sweeps': 0,
                'total_likes_given': 0,
                'total_likes_received': 0,
                'liked': build_liked_dict(uids),
                'liked_by': build_liked_dict(uids)
            }

        return memberdict

    def parse_row(memberdict, row):
        timestamp = row[0]
        uid = row[1]
        if row[2] != '':
            liked_by = row[2].split(',')
        else:
            liked_by = []
        text = row[3]

        # Reject rows with member id 'system' and 'calendar'
        try:
            int(uid)
        except ValueError:
            return

        member = memberdict[uid]
        member['messages'] += 1

        if len(liked_by) == (len(uids) - 1) and uid not in liked_by:
            member['modest_sweeps'] += 1
            member['sweeps'] += 1
        elif len(liked_by) == len(uids):
            member['sweeps'] += 1

        for l_uid in liked_by:
            member['liked_by'][l_uid] += 1
            memberdict[l_uid]['liked'][uid] += 1

    with open(infile_name, newline='') as csvfile:
        reader = csv.reader(csvfile, dialect='excel')
        uids = next(reader)
        member_names = next(reader)

        memberdict = build_memberdict(uids)
        uid_to_name = dict(zip(uids, member_names))


        bottomrow = None
        for row in reader:
            parse_row(memberdict, row)
            bottomrow = row

        first_message_date = datetime.datetime.fromtimestamp(float(bottomrow[0])).strftime('%m-%d-%Y')

        for uid, member in memberdict.items():
            member['sweeps_per_message'] = member['sweeps'] / member['messages']
            member['total_likes_given'] = sum(member['liked'].values()) - member['liked'][uid]
            member['total_likes_received'] = sum(member['liked_by'].values()) - member['liked_by'][uid]
            member['likes_per_message'] = member['total_likes_received'] / member['messages']
            member['given_to_received'] = member['total_likes_given'] / member['total_likes_received']

        print_stats(memberdict, uid_to_name, first_message_date)

def main():
    read_csv(get_infile_name())

main()
