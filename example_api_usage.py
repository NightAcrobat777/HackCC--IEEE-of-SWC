#!/usr/bin/env python3

import requests
import json

BASE_URL = "http://localhost:5000"

print("=" * 60)
print("TransferTree API Example")
print("=" * 60)
print()

# Example 1: Check transfer agreement
print("Example 1: Check Transfer Agreement")
print("-" * 60)

response = requests.post(f"{BASE_URL}/api/transfer", json={
    "from_school": "Southwestern College",
    "to_school": "University of California, Berkeley"
})

data = response.json()
print(f"Status: {response.status_code}")
print()

if data.get('error'):
    print(f"❌ Error: {data['error']}")
else:
    agreement = data['agreement']
    print(f"✅ Transfer Agreement Found!")
    print()
    print(f"From: {agreement['from_school']}")
    print(f"To: {agreement['to_school']}")
    print(f"Pathway: {agreement['institution_name']} ({agreement['institution_code'].strip()})")
    print(f"Years Supported: {agreement['years_supported']}")
    print(f"Community College: {agreement['is_community_college']}")
    print()
    print(f"View detailed courses: {data['assist_url']}")

print()
print()

# Example 2: Search for schools
print("Example 2: Search Schools")
print("-" * 60)

response = requests.get(f"{BASE_URL}/api/schools", params={"q": "berkeley"})
data = response.json()

print(f"Schools matching 'berkeley':")
for school in data['schools']:
    print(f"  - {school}")

print()
