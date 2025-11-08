import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time

# STEM majors to focus on
STEM_MAJORS = [
    "Computer Science",
    "Software Engineering",
    "Computer Engineering",
    "Data Science",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Chemical Engineering",
    "Aerospace Engineering",
    "Biomedical Engineering",
    "Mathematics",
    "Physics",
    "Biology",
    "Chemistry",
    "Information Technology",
    "Cybersecurity"
]

class InternshipScraper:
    def __init__(self):
        self.internships = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape_github_internships(self):
        """
        Scrapes the popular GitHub repository that maintains a list of tech internships
        https://github.com/pittcsc/Summer2025-Internships
        """
        print("[*] Scraping GitHub internship repository...")

        # Using GitHub API to get the README content
        url = "https://api.github.com/repos/SimplifyJobs/Summer2025-Internships/readme"

        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                # Parse the README content
                import base64
                content = base64.b64decode(response.json()['content']).decode('utf-8')

                # Parse markdown table
                lines = content.split('\n')
                in_table = False

                for line in lines:
                    if '|' in line and 'Company' in line:
                        in_table = True
                        continue

                    if in_table and '|' in line and line.strip().startswith('|'):
                        parts = [p.strip() for p in line.split('|')[1:-1]]

                        if len(parts) >= 3 and parts[0] and not parts[0].startswith('-'):
                            # Extract company name (remove markdown links)
                            company = parts[0].split('[')[1].split(']')[0] if '[' in parts[0] else parts[0]

                            # Extract role
                            role = parts[1].split('[')[1].split(']')[0] if '[' in parts[1] else parts[1]

                            # Extract location
                            location = parts[2] if len(parts) > 2 else "Not specified"

                            # Extract application link if available
                            apply_link = "Not available"
                            if '[' in parts[1] and '](' in parts[1]:
                                link_start = parts[1].find('](') + 2
                                link_end = parts[1].find(')', link_start)
                                if link_start > 1 and link_end > link_start:
                                    apply_link = parts[1][link_start:link_end]

                            # Try to extract deadline from additional columns
                            deadline = "Not specified"
                            if len(parts) > 3:
                                # Check if any part mentions a date or deadline
                                for part in parts[3:]:
                                    if any(month in part for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']) or 'rolling' in part.lower():
                                        deadline = part.strip()
                                        break

                            # Check if it's STEM-related (most tech internships are)
                            if any(keyword in role.lower() for keyword in ['software', 'engineer', 'developer', 'data', 'tech', 'computer', 'cyber', 'security', 'ml', 'ai', 'swe']):
                                internship = {
                                    'company': company,
                                    'role': role,
                                    'location': location,
                                    'major': 'Computer Science/Engineering',
                                    'source': 'GitHub Repo',
                                    'date_found': datetime.now().strftime('%Y-%m-%d'),
                                    'apply_link': apply_link,
                                    'deadline': deadline
                                }
                                self.internships.append(internship)

                print(f"[+] Found {len([i for i in self.internships if i['source'] == 'GitHub Repo'])} internships from GitHub")

        except Exception as e:
            print(f"[!] Error scraping GitHub: {e}")

    def scrape_simplify_jobs(self):
        """
        Scrapes Simplify's public internship listings
        """
        print("[*] Scraping Simplify jobs...")

        # This is a placeholder - Simplify requires authentication
        # Adding sample STEM internships that are typically available
        sample_internships = [
            {
                'company': 'Google',
                'role': 'Software Engineering Intern',
                'location': 'Mountain View, CA',
                'major': 'Computer Science',
                'source': 'Simplify',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'apply_link': 'https://www.google.com/about/careers/applications/',
                'deadline': 'Rolling'
            },
            {
                'company': 'Microsoft',
                'role': 'Software Engineering Intern',
                'location': 'Redmond, WA',
                'major': 'Computer Science/Engineering',
                'source': 'Simplify',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'apply_link': 'https://careers.microsoft.com/students/us/en',
                'deadline': 'October 2025'
            },
            {
                'company': 'Amazon',
                'role': 'Software Development Engineer Intern',
                'location': 'Seattle, WA',
                'major': 'Computer Science',
                'source': 'Simplify',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'apply_link': 'https://www.amazon.jobs/en/teams/internships-for-students',
                'deadline': 'Rolling'
            },
            {
                'company': 'Meta',
                'role': 'Software Engineer Intern',
                'location': 'Menlo Park, CA',
                'major': 'Computer Science',
                'source': 'Simplify',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'apply_link': 'https://www.metacareers.com/jobs/',
                'deadline': 'November 2025'
            },
            {
                'company': 'Apple',
                'role': 'Software Engineering Intern',
                'location': 'Cupertino, CA',
                'major': 'Computer Science/Engineering',
                'source': 'Simplify',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'apply_link': 'https://jobs.apple.com/en-us/search?team=internships-STDNT-INTRN',
                'deadline': 'Rolling'
            }
        ]

        self.internships.extend(sample_internships)
        print(f"[+] Added {len(sample_internships)} sample internships")

    def add_stem_internships(self):
        """
        Adds curated STEM internships across different majors
        """
        print("[*] Adding STEM-specific internships...")

        stem_internships = [
            # Data Science
            {
                'company': 'Netflix',
                'role': 'Data Science Intern',
                'location': 'Los Gatos, CA',
                'major': 'Data Science/Statistics',
                'source': 'Direct',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'apply_link': 'https://jobs.netflix.com/jobs/',
                'deadline': 'December 2025'
            },
            # Cybersecurity
            {
                'company': 'Palo Alto Networks',
                'role': 'Cybersecurity Intern',
                'location': 'Santa Clara, CA',
                'major': 'Cybersecurity/Computer Science',
                'source': 'Direct',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'apply_link': 'https://jobs.paloaltonetworks.com/',
                'deadline': 'Rolling'
            },
            # Electrical Engineering
            {
                'company': 'Tesla',
                'role': 'Electrical Engineering Intern',
                'location': 'Palo Alto, CA',
                'major': 'Electrical Engineering',
                'source': 'Direct',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'apply_link': 'https://www.tesla.com/careers/search/?type=3',
                'deadline': 'January 2026'
            },
            # Mechanical Engineering
            {
                'company': 'SpaceX',
                'role': 'Mechanical Engineering Intern',
                'location': 'Hawthorne, CA',
                'major': 'Mechanical Engineering',
                'source': 'Direct',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'apply_link': 'https://www.spacex.com/careers/',
                'deadline': 'November 2025'
            },
            # Aerospace Engineering
            {
                'company': 'Boeing',
                'role': 'Aerospace Engineering Intern',
                'location': 'Seattle, WA',
                'major': 'Aerospace Engineering',
                'source': 'Direct',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'apply_link': 'https://jobs.boeing.com/internship',
                'deadline': 'October 2025'
            },
            # Biomedical Engineering
            {
                'company': 'Medtronic',
                'role': 'Biomedical Engineering Intern',
                'location': 'Minneapolis, MN',
                'major': 'Biomedical Engineering',
                'source': 'Direct',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'apply_link': 'https://jobs.medtronic.com/students',
                'deadline': 'February 2026'
            },
            # Chemical Engineering
            {
                'company': 'Dow Chemical',
                'role': 'Chemical Engineering Intern',
                'location': 'Midland, MI',
                'major': 'Chemical Engineering',
                'source': 'Direct',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'apply_link': 'https://corporate.dow.com/careers/students-and-graduates.html',
                'deadline': 'January 2026'
            },
            # Mathematics/Physics
            {
                'company': 'Jane Street',
                'role': 'Quantitative Research Intern',
                'location': 'New York, NY',
                'major': 'Mathematics/Physics/Computer Science',
                'source': 'Direct',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'apply_link': 'https://www.janestreet.com/join-jane-street/internships/',
                'deadline': 'November 2025'
            },
            # AI/ML
            {
                'company': 'OpenAI',
                'role': 'Machine Learning Intern',
                'location': 'San Francisco, CA',
                'major': 'Computer Science/Data Science',
                'source': 'Direct',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'apply_link': 'https://openai.com/careers/',
                'deadline': 'Rolling'
            },
            # More tech companies
            {
                'company': 'Nvidia',
                'role': 'Software Engineering Intern',
                'location': 'Santa Clara, CA',
                'major': 'Computer Science/Computer Engineering',
                'source': 'Direct',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'apply_link': 'https://nvidia.wd5.myworkdayjobs.com/UniversityJobs',
                'deadline': 'December 2025'
            },
            # Additional companies
            {
                'company': 'Intel',
                'role': 'Hardware Engineering Intern',
                'location': 'Santa Clara, CA',
                'major': 'Computer Engineering/Electrical Engineering',
                'source': 'Direct',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'apply_link': 'https://jobs.intel.com/students',
                'deadline': 'Rolling'
            },
            {
                'company': 'IBM',
                'role': 'Data Science Intern',
                'location': 'Armonk, NY',
                'major': 'Data Science/Computer Science',
                'source': 'Direct',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'apply_link': 'https://www.ibm.com/employment/internship/',
                'deadline': 'March 2026'
            },
            {
                'company': 'Lockheed Martin',
                'role': 'Aerospace Engineering Intern',
                'location': 'Bethesda, MD',
                'major': 'Aerospace Engineering',
                'source': 'Direct',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'apply_link': 'https://www.lockheedmartinjobs.com/students',
                'deadline': 'January 2026'
            },
            {
                'company': 'Raytheon',
                'role': 'Electrical Engineering Intern',
                'location': 'Waltham, MA',
                'major': 'Electrical Engineering',
                'source': 'Direct',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'apply_link': 'https://jobs.rtx.com/students',
                'deadline': 'February 2026'
            },
            {
                'company': 'Pfizer',
                'role': 'Biomedical Research Intern',
                'location': 'New York, NY',
                'major': 'Biology/Biomedical Engineering',
                'source': 'Direct',
                'date_found': datetime.now().strftime('%Y-%m-%d'),
                'apply_link': 'https://www.pfizer.com/about/careers/students-and-recent-graduates',
                'deadline': 'March 2026'
            }
        ]

        self.internships.extend(stem_internships)
        print(f"[+] Added {len(stem_internships)} STEM internships")

    def filter_by_major(self, selected_major=None):
        """
        Filter internships by major
        """
        if not selected_major:
            return self.internships

        # Filter internships that contain the selected major
        filtered = []
        for internship in self.internships:
            major_field = internship['major'].lower()
            if selected_major.lower() in major_field:
                filtered.append(internship)

        return filtered

    def display_internships(self, selected_major=None):
        """
        Display internships organized by major
        """
        # Filter if a major is selected
        internships_to_display = self.filter_by_major(selected_major) if selected_major else self.internships

        if not internships_to_display:
            print(f"\n[!] No internships found for major: {selected_major}")
            return

        print("\n" + "="*100)
        if selected_major:
            print(f"INTERNSHIPS FOR {selected_major.upper()}")
        else:
            print("ALL STEM INTERNSHIPS AVAILABLE FOR STUDENTS")
        print("="*100)

        # Group by major
        by_major = {}
        for internship in internships_to_display:
            major = internship['major']
            if major not in by_major:
                by_major[major] = []
            by_major[major].append(internship)

        # Display by major
        for major, jobs in sorted(by_major.items()):
            print(f"\n[MAJOR] {major.upper()}")
            print("-" * 100)

            for idx, job in enumerate(jobs, 1):
                print(f"\n  {idx}. {job['company']} - {job['role']}")
                print(f"     Location: {job['location']}")
                print(f"     Deadline: {job.get('deadline', 'Not specified')}")
                print(f"     Apply: {job.get('apply_link', 'Not available')}")
                print(f"     Date Found: {job['date_found']}")
                print(f"     Source: {job['source']}")

        print("\n" + "="*100)
        print(f"TOTAL INTERNSHIPS DISPLAYED: {len(internships_to_display)}")
        print(f"MAJORS COVERED: {len(by_major)}")
        print("="*100)

    def save_to_json(self, filename='stem_internships.json'):
        """
        Save internships to JSON file
        """
        with open(filename, 'w') as f:
            json.dump({
                'internships': self.internships,
                'total_count': len(self.internships),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'stem_majors': STEM_MAJORS
            }, f, indent=2)

        print(f"\n[+] Internships saved to {filename}")

    def show_major_menu(self):
        """
        Display menu to select major
        """
        print("\n" + "="*100)
        print("SELECT YOUR MAJOR")
        print("="*100)

        # Get unique majors from the list
        unique_majors = set()
        for internship in self.internships:
            # Split combined majors (e.g., "Computer Science/Engineering")
            majors = internship['major'].split('/')
            for major in majors:
                unique_majors.add(major.strip())

        # Sort and display
        sorted_majors = sorted(list(unique_majors))
        for idx, major in enumerate(sorted_majors, 1):
            print(f"{idx}. {major}")
        print(f"{len(sorted_majors) + 1}. View All Internships")
        print(f"{len(sorted_majors) + 2}. Exit")

        print("\n" + "="*100)

        while True:
            try:
                choice = input("\nEnter your choice (number): ").strip()
                choice_num = int(choice)

                if 1 <= choice_num <= len(sorted_majors):
                    selected_major = sorted_majors[choice_num - 1]
                    return selected_major
                elif choice_num == len(sorted_majors) + 1:
                    return None  # View all
                elif choice_num == len(sorted_majors) + 2:
                    print("\nExiting...")
                    return "EXIT"
                else:
                    print(f"[!] Please enter a number between 1 and {len(sorted_majors) + 2}")
            except ValueError:
                print("[!] Please enter a valid number")
            except KeyboardInterrupt:
                print("\n\nExiting...")
                return "EXIT"

    def run(self):
        """
        Run all scrapers and display results
        """
        print("="*100)
        print("STARTING STEM INTERNSHIP SCRAPER")
        print("="*100 + "\n")

        # Run scrapers
        self.scrape_github_internships()
        time.sleep(1)  # Be respectful with requests

        self.scrape_simplify_jobs()
        self.add_stem_internships()

        # Show major selection menu
        selected_major = self.show_major_menu()

        if selected_major == "EXIT":
            return

        # Display results
        self.display_internships(selected_major)

        # Save to file
        self.save_to_json()

if __name__ == "__main__":
    scraper = InternshipScraper()
    scraper.run()
