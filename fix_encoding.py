#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fix encoding issues in knowledge-graph.js"""

import json
import re

# Read the HTML source
source_path = r'C:\Users\maciu\Downloads\Graf wiedzy o nauce uczenia się.html'

print("Reading source file...")
with open(source_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Extract the DATA object
print("Extracting DATA...")
data_match = re.search(r'const DATA = ({.*?});', html_content, re.DOTALL)

if not data_match:
    print("ERROR: Could not find DATA in source")
    exit(1)

data_json = data_match.group(1)

# Replace smart quotes with straight quotes
print("Fixing quotes...")
replacements = [
    ('\u201c', '"'),  # "
    ('\u201d', '"'),  # "
    ('\u2018', "'"),  # '
    ('\u2019', "'"),  # '
    ('\u2013', '-'),  # –
    ('\u2014', '--'), # —
]

for old, new in replacements:
    data_json = data_json.replace(old, new)

# Parse to validate
print("Validating JSON...")
try:
    data = json.loads(data_json)
    print(f"✓ Parsed {len(data['nodes'])} nodes and {len(data['edges'])} edges")
    print(f"✓ Sample label: {data['nodes'][3]['label']}")
except json.JSONDecodeError as e:
    print(f"ERROR parsing JSON: {e}")
    exit(1)

# Save as properly formatted JSON
print("Writing corrected JSON...")
with open('static/js/knowledge-graph-data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✓ Success! Data saved to static/js/knowledge-graph-data.json")
