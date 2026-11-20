#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fix smart quotes in knowledge-graph.js"""

# Read the file
with open(r'C:\Users\maciu\OneDrive\Pulpit\AnyLearn Labs\static\js\knowledge-graph.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace smart quotes with straight quotes
replacements = [
    ('\u201c', '"'),  # "
    ('\u201d', '"'),  # "
    ('\u201e', '"'),  # „
    ('\u201f', '"'),  # ‟
    ('\u2018', "'"),  # '
    ('\u2019', "'"),  # '
    ('\u2013', '-'),  # –
    ('\u2014', '--'), # —
]

for old, new in replacements:
    content = content.replace(old, new)

# Write back
with open(r'C:\Users\maciu\OneDrive\Pulpit\AnyLearn Labs\static\js\knowledge-graph.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done: Fixed smart quotes in knowledge-graph.js')
