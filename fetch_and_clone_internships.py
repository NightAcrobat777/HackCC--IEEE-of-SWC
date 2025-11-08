#!/usr/bin/env python3
"""
Script to clone the 2026-SWE-College-Jobs repository and fetch internships
Combines repository cloning with internship data extraction
"""

import os
import sys
import re
import json
from datetime import datetime
import subprocess


class InternshipFetcher:
    def __init__(self):
        self.repo_dir = "2026-SWE-College-Jobs"
        self.readme_path = os.path.join(self.repo_dir, "README.md")
        self.internships = []

    def clone_or_update_repo(self):
        """Clone the repository or update it if it already exists"""
        repo_url = "https://github.com/speedyapply/2026-SWE-College-Jobs.git"

        if os.path.exists(self.repo_dir):
            print(f"[*] Repository already exists. Updating...")
            try:
                # Pull latest changes
                result = subprocess.run(
                    ["git", "-C", self.repo_dir, "pull"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                print(f"[+] Repository updated successfully")
                return True
            except subprocess.CalledProcessError as e:
                print(f"[!] Error updating repository: {e.stderr}")
                return False
        else:
            print(f"[*] Cloning repository: {repo_url}")
            try:
                result = subprocess.run(
                    ["git", "clone", repo_url],
                    capture_output=True,
                    text=True,
                    check=True
                )
                print(f"[+] Repository cloned successfully")
                return True
            except subprocess.CalledProcessError as e:
                print(f"[!] Error cloning repository: {e.stderr}")
                return False
            except FileNotFoundError:
                print("[!] Error: git is not installed or not in PATH")
                return False

    def parse_markdown_table(self, content, category):
        """Parse markdown table and extract internship data"""
        lines = content.split('\n')
        in_table = False
        internships = []

        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue

            # Check if we're in a table
            if '| Company | Position | Location |' in line:
                in_table = True
                continue

            # Skip the separator line (contains --- )
            if in_table and '|---' in line:
                continue

            # Parse table rows
            if in_table and line.startswith('|'):
                # Stop if we hit the end marker
                if '<!-- TABLE' in line and 'END' in line:
                    in_table = False
                    continue

                # Split by | and clean up
                parts = [p.strip() for p in line.split('|')]

                # Filter out empty parts
                parts = [p for p in parts if p]

                if len(parts) >= 4:  # Company, Position, Location, Posting (minimum)
                    try:
                        # Extract company name from markdown link
                        company_match = re.search(r'\*\*([^*]+)\*\*', parts[0])
                        company = company_match.group(1) if company_match else parts[0]
                        # Clean any remaining HTML tags
                        company = re.sub(r'<[^>]+>', '', company).strip()

                        # Extract company URL
                        company_url_match = re.search(r'href="([^"]+)"', parts[0])
                        company_url = company_url_match.group(1) if company_url_match else ""

                        # Extract position
                        position = re.sub(r'<[^>]+>', '', parts[1]).strip()

                        # Extract location
                        location = re.sub(r'<[^>]+>', '', parts[2]).strip()

                        # Extract salary if available (FAANG+ and Quant tables have it)
                        salary = ""
                        posting_idx = 3
                        if len(parts) >= 5:
                            # Check if this column looks like salary
                            if '$' in parts[3] or 'hr' in parts[3].lower():
                                salary = re.sub(r'<[^>]+>', '', parts[3]).strip()
                                posting_idx = 4

                        # Extract application link from the Posting column
                        apply_link = ""
                        if len(parts) > posting_idx:
                            link_match = re.search(r'href="([^"]+)"', parts[posting_idx])
                            apply_link = link_match.group(1) if link_match else ""

                        # Extract age (days posted)
                        age = ""
                        age_idx = posting_idx + 1
                        if len(parts) > age_idx:
                            age = re.sub(r'<[^>]+>', '', parts[age_idx]).strip()

                        internship = {
                            'company': company,
                            'company_url': company_url,
                            'position': position,
                            'location': location,
                            'salary': salary,
                            'apply_link': apply_link,
                            'age': age,
                            'category': category,
                            'date_fetched': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }

                        internships.append(internship)

                    except Exception as e:
                        print(f"[!] Error parsing row: {e}")
                        print(f"    Row: {line}")
                        continue

        return internships

    def fetch_internships(self):
        """Read README.md and extract all internship listings"""
        if not os.path.exists(self.readme_path):
            print(f"[!] Error: README.md not found at {self.readme_path}")
            return False

        print(f"[*] Reading internships from README.md...")

        try:
            with open(self.readme_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find and parse FAANG+ section
            faang_start = content.find('<!-- TABLE_FAANG_START -->')
            faang_end = content.find('<!-- TABLE_FAANG_END -->')
            if faang_start != -1 and faang_end != -1:
                faang_content = content[faang_start:faang_end]
                faang_internships = self.parse_markdown_table(faang_content, 'FAANG+')
                self.internships.extend(faang_internships)
                print(f"[+] Found {len(faang_internships)} FAANG+ internships")

            # Find and parse Quant section
            quant_start = content.find('<!-- TABLE_QUANT_START -->')
            quant_end = content.find('<!-- TABLE_QUANT_END -->')
            if quant_start != -1 and quant_end != -1:
                quant_content = content[quant_start:quant_end]
                quant_internships = self.parse_markdown_table(quant_content, 'Quant')
                self.internships.extend(quant_internships)
                print(f"[+] Found {len(quant_internships)} Quant internships")

            # Find and parse Other section
            other_start = content.find('<!-- TABLE_START -->')
            other_end = content.find('<!-- TABLE_END -->')
            if other_start != -1 and other_end != -1:
                other_content = content[other_start:other_end]
                other_internships = self.parse_markdown_table(other_content, 'Other')
                self.internships.extend(other_internships)
                print(f"[+] Found {len(other_internships)} Other internships")

            print(f"[+] Total internships fetched: {len(self.internships)}")
            return True

        except Exception as e:
            print(f"[!] Error reading README.md: {e}")
            return False

    def save_to_json(self, filename='2026_internships.json'):
        """Save internships to a JSON file"""
        output_data = {
            'metadata': {
                'total_count': len(self.internships),
                'date_fetched': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': '2026-SWE-College-Jobs Repository',
                'repository_url': 'https://github.com/speedyapply/2026-SWE-College-Jobs',
                'categories': {
                    'FAANG+': len([i for i in self.internships if i['category'] == 'FAANG+']),
                    'Quant': len([i for i in self.internships if i['category'] == 'Quant']),
                    'Other': len([i for i in self.internships if i['category'] == 'Other'])
                }
            },
            'internships': self.internships
        }

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            print(f"\n[+] Internships saved to {filename}")
            return True
        except Exception as e:
            print(f"[!] Error saving to JSON: {e}")
            return False

    def display_summary(self):
        """Display a summary of fetched internships"""
        if not self.internships:
            print("\n[!] No internships to display")
            return

        print("\n" + "="*100)
        print("INTERNSHIP SUMMARY")
        print("="*100)

        # Group by category
        by_category = {}
        for internship in self.internships:
            cat = internship['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(internship)

        # Display by category
        for category, jobs in sorted(by_category.items()):
            print(f"\n[{category}] - {len(jobs)} positions")
            print("-" * 100)

            # Show first 5 from each category
            for idx, job in enumerate(jobs[:5], 1):
                print(f"\n  {idx}. {job['company']} - {job['position']}")
                print(f"     Location: {job['location']}")
                if job['salary']:
                    print(f"     Salary: {job['salary']}")
                print(f"     Apply: {job['apply_link'][:80]}..." if len(job['apply_link']) > 80 else f"     Apply: {job['apply_link']}")

            if len(jobs) > 5:
                print(f"\n  ... and {len(jobs) - 5} more positions")

        print("\n" + "="*100)
        print(f"TOTAL: {len(self.internships)} internships")
        print("="*100)

    def run(self):
        """Main execution flow"""
        print("="*100)
        print("2026 SOFTWARE ENGINEERING INTERNSHIP FETCHER")
        print("="*100 + "\n")

        # Step 1: Clone or update repository
        if not self.clone_or_update_repo():
            print("\n[!] Failed to clone/update repository")
            return False

        # Step 2: Parse README and fetch internships
        if not self.fetch_internships():
            print("\n[!] Failed to fetch internships")
            return False

        # Step 3: Display summary
        self.display_summary()

        # Step 4: Save to JSON
        if not self.save_to_json():
            print("\n[!] Failed to save internships to JSON")
            return False

        print("\n[+] Success! Internships fetched and saved.")
        return True


if __name__ == "__main__":
    fetcher = InternshipFetcher()
    success = fetcher.run()
    sys.exit(0 if success else 1)
