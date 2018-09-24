import requests
import csv
import sys


BASE_URL = 'https://ocd.datamade.us/'
SEARCH_PATH = 'votes/?votes__option=yes&votes__option=no&organization__id=ocd-organization/ef168607-9135-4177-ad8e-c1f7a4806c3a&bill__legislative_session__identifier=2015&page={}'

page = 1
max_page = None
seen_votes = set()
all_alderman = set()
all_votes = []

while page != max_page:
    url = BASE_URL + SEARCH_PATH.format(page)
    search_results = requests.get(url)
    page += 1
    for result in search_results.json()['results']:
        vote_id = result['id']
        if vote_id not in seen_votes:
            url = BASE_URL + vote_id
            vote_details = requests.get(url)

            alderman = {}
            for vote in vote_details.json()['votes']:
                alderman[vote['voter_name']] = vote['option']
            all_alderman.update(alderman)

            alderman['bill'] = result['bill']['identifier']
            alderman['date'] = result['start_date']
            alderman['motion'] = result['motion_text']

            all_votes.append(alderman)

            seen_votes.add(vote_id)
    max_page = search_results.json()['meta']['max_page']

field_names = ['date', 'bill', 'motion'] + sorted(all_alderman)
writer = csv.DictWriter(sys.stdout, field_names)
writer.writeheader()
for result in all_votes:
    writer.writerow(result)
