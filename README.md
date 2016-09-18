# Setup
Groupme Leaderboard depends on [GroupyAPI](https://github.com/rhgrant10/Groupy).
Groupy install instructions here: (http://groupy.readthedocs.io/en/latest/pages/installation.html).

## TL;DR:
1. Install python3
2. `pip3 install GroupyAPI`
3. Get a GroupMe API token from [here](https://dev.groupme.com/)
4. Save your API token in a file ~/.groupy.key

# Usage
1. Run `python3 download_messages.py "MY GROUP NAME"` - this will generate a CSV file
2. Run `python3 print_stats.py groupme_MYGROUPNAME.csv`
3. For Markov run `python3 csv_to_markov.py groupme_MYGROUPNAME.csv "person's name"` ([more info](csv_to_markov.py))
