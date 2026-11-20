#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Extract graph data from HTML and save as JSON"""

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

data_json_str = data_match.group(1)

# Parse to validate
print("Validating JSON...")
try:
    data = json.loads(data_json_str)
    print(f"Parsed {len(data['nodes'])} nodes and {len(data['edges'])} edges")
except json.JSONDecodeError as e:
    print(f"ERROR parsing JSON: {e}")
    exit(1)

# Save as properly formatted JSON
print("Writing JSON data...")
output_path = r'C:\Users\maciu\OneDrive\Pulpit\AnyLearn Labs\static\js\knowledge-graph-data.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Success! Data saved to {output_path}")
print(f"Sample label: {data['nodes'][3]['label']}")
