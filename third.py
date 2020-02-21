import os
import sys
import json

data = {'a': 3, 'b': 4}
f = open('fonts/messages_count.json')
d = json.load(f)
general_count = 0
for chat, contacts in d.items():
    print(f'{chat}:')
    count_sorted = sorted(contacts.keys(),
                          key=lambda x: contacts[x]['count'],
                          reverse=True)
    total_count = 0
    i = 1
    for contact_id in count_sorted:
        contact_info = contacts[contact_id]
        count = contact_info['count']
        print(f'\t{i}. {contact_info["contact"]} ({contact_id})({count})')
        i += 1
        total_count += count
    general_count += total_count
    print(f'Total: {total_count}\n\n')
print(f'All count: {general_count}')

