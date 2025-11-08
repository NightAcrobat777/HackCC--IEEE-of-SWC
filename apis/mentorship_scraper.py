import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time

class MentorshipScraper:
    """
    A comprehensive scraper for mentorship opportunities targeting:
    - Community college students
    - Students by major (general and major-specific)
    - General mentorship programs
    """

    def __init__(self):
        self.mentorships = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def add_tech_mentorship_programs(self):
        """
        Add curated tech and STEM mentorship programs
        """
        print("[*] Adding tech mentorship programs...")

        tech_mentorships = [
            # General Tech Mentorship
            {
                'organization': 'CodePath',
                'program_name': 'Tech Mentorship Program',
                'description': 'Free tech courses with built-in mentorship from industry professionals',
                'target_audience': 'All students, community college friendly',
                'majors': ['Computer Science', 'Software Engineering', 'General'],
                'website': 'https://www.codepath.org/',
                'application_process': 'Online application with courses starting multiple times per year',
                'cost': 'Free',
                'format': 'Virtual',
                'duration': '10-12 weeks per course',
                'requirements': 'Basic programming knowledge for some courses',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'ColorStack',
                'program_name': 'ColorStack Mentorship',
                'description': 'Career development and mentorship for Black and Latinx CS students',
                'target_audience': 'Black and Latinx CS students, all college levels',
                'majors': ['Computer Science', 'Software Engineering'],
                'website': 'https://www.colorstack.org/',
                'application_process': 'Join ColorStack community and opt into mentorship',
                'cost': 'Free',
                'format': 'Virtual and in-person events',
                'duration': 'Ongoing',
                'requirements': 'Must be pursuing CS or related degree',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'Rewriting the Code',
                'program_name': 'RTC Mentorship',
                'description': 'Mentorship and community for women in tech',
                'target_audience': 'Women and non-binary college students in tech',
                'majors': ['Computer Science', 'Software Engineering', 'Data Science', 'General Tech'],
                'website': 'https://rewritingthecode.org/',
                'application_process': 'Apply through website',
                'cost': 'Free',
                'format': 'Virtual',
                'duration': 'Year-long program',
                'requirements': 'Must be pursuing tech degree',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'Management Leadership for Tomorrow (MLT)',
                'program_name': 'MLT Career Prep',
                'description': 'Career coaching and mentorship for high-achieving diverse talent',
                'target_audience': 'Underrepresented minorities, community college students welcome',
                'majors': ['All majors', 'General'],
                'website': 'https://mlt.org/career-prep/',
                'application_process': 'Competitive application process',
                'cost': 'Free',
                'format': 'Virtual and in-person',
                'duration': '18 months',
                'requirements': 'Strong academic record',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'Break Through Tech',
                'program_name': 'Break Through Tech Program',
                'description': 'Tech education and mentorship for women and non-binary students',
                'target_audience': 'Women and non-binary students, community college friendly',
                'majors': ['Computer Science', 'Data Science', 'Information Technology'],
                'website': 'https://breakthroughtech.org/',
                'application_process': 'Apply through partner universities',
                'cost': 'Free',
                'format': 'Hybrid',
                'duration': 'Multi-year program',
                'requirements': 'Must attend partner institution',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            # Community College Specific
            {
                'organization': 'Phi Theta Kappa',
                'program_name': 'PTK Mentorship',
                'description': 'Honor society with mentorship opportunities for community college students',
                'target_audience': 'Community college students',
                'majors': ['All majors', 'General'],
                'website': 'https://www.ptk.org/',
                'application_process': 'Must be PTK member (GPA requirement)',
                'cost': 'PTK membership fee',
                'format': 'Virtual and in-person',
                'duration': 'Ongoing',
                'requirements': '3.5+ GPA',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'Jack Kent Cooke Foundation',
                'program_name': 'Cooke Community College Scholars',
                'description': 'Comprehensive support including mentorship for community college students',
                'target_audience': 'High-achieving community college students',
                'majors': ['All majors', 'General'],
                'website': 'https://www.jkcf.org/our-scholarships/college-scholarship-program/',
                'application_process': 'Competitive scholarship application',
                'cost': 'Free (provides scholarship)',
                'format': 'Virtual and in-person',
                'duration': 'Through degree completion',
                'requirements': 'Strong academic record, financial need',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            # Engineering/STEM Specific
            {
                'organization': 'Society of Women Engineers (SWE)',
                'program_name': 'SWE Mentorship',
                'description': 'Mentorship program for women in engineering',
                'target_audience': 'Women engineering students at all levels',
                'majors': ['Engineering', 'Mechanical Engineering', 'Electrical Engineering', 'Chemical Engineering'],
                'website': 'https://swe.org/membership/mentoring/',
                'application_process': 'Join SWE and sign up for mentorship',
                'cost': 'SWE membership fee',
                'format': 'Virtual',
                'duration': 'Flexible',
                'requirements': 'SWE membership',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'National Society of Black Engineers (NSBE)',
                'program_name': 'NSBE Mentorship',
                'description': 'Mentorship for Black engineering students',
                'target_audience': 'Black engineering students, all college levels',
                'majors': ['Engineering', 'Computer Science', 'STEM'],
                'website': 'https://www.nsbe.org/',
                'application_process': 'NSBE membership required',
                'cost': 'NSBE membership fee',
                'format': 'Virtual and in-person',
                'duration': 'Ongoing',
                'requirements': 'NSBE membership',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'Society of Hispanic Professional Engineers (SHPE)',
                'program_name': 'SHPE Mentorship',
                'description': 'Mentorship for Hispanic engineering students',
                'target_audience': 'Hispanic STEM students, community college welcome',
                'majors': ['Engineering', 'Computer Science', 'STEM'],
                'website': 'https://www.shpe.org/',
                'application_process': 'Join SHPE and access mentorship',
                'cost': 'SHPE membership fee',
                'format': 'Virtual and in-person',
                'duration': 'Ongoing',
                'requirements': 'SHPE membership',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            # Data Science/Analytics
            {
                'organization': 'Women in Data',
                'program_name': 'WiD Mentorship',
                'description': 'Mentorship for women pursuing data science careers',
                'target_audience': 'Women in data science and analytics',
                'majors': ['Data Science', 'Statistics', 'Computer Science'],
                'website': 'https://www.womenindata.org/',
                'application_process': 'Join community and apply for mentorship',
                'cost': 'Free',
                'format': 'Virtual',
                'duration': '6 months',
                'requirements': 'Interest in data field',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            # General Business/All Majors
            {
                'organization': 'MentorNet',
                'program_name': 'MentorNet E-Mentoring',
                'description': 'Online mentoring in STEM fields',
                'target_audience': 'All STEM students',
                'majors': ['STEM', 'Engineering', 'Computer Science', 'Mathematics'],
                'website': 'https://www.mentornet.org/',
                'application_process': 'Register online',
                'cost': 'Free',
                'format': 'Virtual',
                'duration': 'Flexible',
                'requirements': 'Pursuing STEM degree',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'LinkedIn',
                'program_name': 'LinkedIn Career Advice',
                'description': 'Connect with mentors in your field through LinkedIn',
                'target_audience': 'All students',
                'majors': ['All majors', 'General'],
                'website': 'https://www.linkedin.com/help/linkedin/answer/a507663',
                'application_process': 'Set up profile and browse mentors',
                'cost': 'Free',
                'format': 'Virtual',
                'duration': 'Self-paced',
                'requirements': 'LinkedIn account',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'ADPList',
                'program_name': 'Amazing Design People List',
                'description': 'Free mentorship from professionals in tech, design, and product',
                'target_audience': 'All students interested in tech',
                'majors': ['Computer Science', 'Design', 'Product Management', 'General'],
                'website': 'https://adplist.org/',
                'application_process': 'Sign up and book sessions',
                'cost': 'Free',
                'format': 'Virtual',
                'duration': 'Session-based',
                'requirements': 'None',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'Chronus',
                'program_name': 'Open Mentorship Programs',
                'description': 'Platform hosting various corporate mentorship programs',
                'target_audience': 'All students',
                'majors': ['All majors', 'General'],
                'website': 'https://chronus.com/',
                'application_process': 'Find programs through platform',
                'cost': 'Free',
                'format': 'Virtual',
                'duration': 'Varies by program',
                'requirements': 'Varies by program',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            # Cybersecurity
            {
                'organization': 'Women in Cybersecurity (WiCyS)',
                'program_name': 'WiCyS Mentorship',
                'description': 'Mentorship for women in cybersecurity',
                'target_audience': 'Women in cybersecurity',
                'majors': ['Cybersecurity', 'Computer Science', 'Information Technology'],
                'website': 'https://www.wicys.org/mentoring',
                'application_process': 'WiCyS membership and application',
                'cost': 'WiCyS membership fee',
                'format': 'Virtual',
                'duration': '6-12 months',
                'requirements': 'Interest in cybersecurity',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            # Additional Programs
            {
                'organization': 'GitHub Education',
                'program_name': 'GitHub Campus Experts',
                'description': 'Student leadership program with mentorship from GitHub',
                'target_audience': 'Student leaders interested in tech',
                'majors': ['Computer Science', 'Software Engineering'],
                'website': 'https://education.github.com/experts',
                'application_process': 'Application and training program',
                'cost': 'Free',
                'format': 'Virtual',
                'duration': 'Year-long program',
                'requirements': 'Must be student',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'Out in Tech',
                'program_name': 'Digital Corps Mentorship',
                'description': 'Mentorship for LGBTQ+ individuals in tech',
                'target_audience': 'LGBTQ+ students in tech',
                'majors': ['Computer Science', 'Technology', 'General'],
                'website': 'https://outintech.com/digital-corps/',
                'application_process': 'Apply through website',
                'cost': 'Free',
                'format': 'Virtual',
                'duration': '10 weeks',
                'requirements': 'LGBTQ+ identity',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'Techstars',
                'program_name': 'Techstars Mentorship',
                'description': 'Mentorship from entrepreneurs and tech leaders',
                'target_audience': 'Students interested in startups',
                'majors': ['Business', 'Computer Science', 'Entrepreneurship', 'General'],
                'website': 'https://www.techstars.com/communities/mentorship-driven',
                'application_process': 'Through Techstars programs',
                'cost': 'Free',
                'format': 'Virtual and in-person',
                'duration': 'Program-dependent',
                'requirements': 'Participation in Techstars program',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'INROADS',
                'program_name': 'INROADS Internship & Mentorship',
                'description': 'Career development and mentorship for diverse talent',
                'target_audience': 'Underrepresented minorities, community college students',
                'majors': ['Business', 'Engineering', 'Computer Science', 'General'],
                'website': 'https://inroads.org/',
                'application_process': 'Apply through website',
                'cost': 'Free',
                'format': 'Hybrid',
                'duration': 'Multi-year program',
                'requirements': 'Good academic standing',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            }
        ]

        self.mentorships.extend(tech_mentorships)
        print(f"[+] Added {len(tech_mentorships)} tech mentorship programs")

    def add_general_mentorship_programs(self):
        """
        Add general mentorship programs suitable for all majors
        """
        print("[*] Adding general mentorship programs...")

        general_programs = [
            {
                'organization': 'Big Brothers Big Sisters',
                'program_name': 'College Mentorship',
                'description': 'One-on-one mentoring for personal and academic development',
                'target_audience': 'All students',
                'majors': ['All majors', 'General'],
                'website': 'https://www.bbbs.org/',
                'application_process': 'Contact local chapter',
                'cost': 'Free',
                'format': 'In-person',
                'duration': 'Long-term commitment',
                'requirements': 'Background check',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'Score',
                'program_name': 'SCORE Mentorship',
                'description': 'Business mentorship from experienced entrepreneurs',
                'target_audience': 'Students interested in business/entrepreneurship',
                'majors': ['Business', 'Entrepreneurship', 'All majors'],
                'website': 'https://www.score.org/',
                'application_process': 'Request mentor online',
                'cost': 'Free',
                'format': 'Virtual and in-person',
                'duration': 'Flexible',
                'requirements': 'None',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'First-generation College Students',
                'program_name': 'ImFirst Network',
                'description': 'Peer mentorship for first-generation college students',
                'target_audience': 'First-generation college students',
                'majors': ['All majors', 'General'],
                'website': 'https://firstgen.naspa.org/',
                'application_process': 'Join through NASPA',
                'cost': 'Free',
                'format': 'Virtual',
                'duration': 'Ongoing',
                'requirements': 'First-generation status',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'Career Village',
                'program_name': 'Online Career Q&A',
                'description': 'Ask career questions and get advice from professionals',
                'target_audience': 'All students',
                'majors': ['All majors', 'General'],
                'website': 'https://www.careervillage.org/',
                'application_process': 'Create account and post questions',
                'cost': 'Free',
                'format': 'Virtual',
                'duration': 'Self-paced',
                'requirements': 'None',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'Mentor Collective',
                'program_name': 'Campus Mentorship Programs',
                'description': 'Mentorship platform used by many colleges',
                'target_audience': 'Students at partner institutions',
                'majors': ['All majors', 'General'],
                'website': 'https://www.mentorcollective.org/',
                'application_process': 'Through participating colleges',
                'cost': 'Free',
                'format': 'Virtual',
                'duration': 'Semester or year-long',
                'requirements': 'Must attend partner school',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            }
        ]

        self.mentorships.extend(general_programs)
        print(f"[+] Added {len(general_programs)} general mentorship programs")

    def add_community_college_specific(self):
        """
        Add mentorship programs specifically for community college students
        """
        print("[*] Adding community college specific programs...")

        cc_programs = [
            {
                'organization': 'Achieving the Dream',
                'program_name': 'ATD Student Success',
                'description': 'Network supporting community college student success',
                'target_audience': 'Community college students',
                'majors': ['All majors', 'General'],
                'website': 'https://www.achievingthedream.org/',
                'application_process': 'Through participating colleges',
                'cost': 'Free',
                'format': 'Varies by institution',
                'duration': 'Ongoing',
                'requirements': 'Attend ATD network college',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'American Association of Community Colleges',
                'program_name': 'AACC Pathways Project',
                'description': 'Guided pathways and mentorship support',
                'target_audience': 'Community college students',
                'majors': ['All majors', 'General'],
                'website': 'https://www.aacc.nche.edu/',
                'application_process': 'Through participating colleges',
                'cost': 'Free',
                'format': 'Varies',
                'duration': 'Ongoing',
                'requirements': 'Attend participating college',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'Aspen Institute',
                'program_name': 'Community College Excellence',
                'description': 'Programs supporting community college student success',
                'target_audience': 'Community college students',
                'majors': ['All majors', 'General'],
                'website': 'https://highered.aspeninstitute.org/',
                'application_process': 'Through participating institutions',
                'cost': 'Free',
                'format': 'Varies',
                'duration': 'Varies',
                'requirements': 'Attend partner college',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            }
        ]

        self.mentorships.extend(cc_programs)
        print(f"[+] Added {len(cc_programs)} community college specific programs")

    def filter_by_criteria(self, major=None, target_audience=None, cost=None):
        """
        Filter mentorship programs by various criteria
        """
        filtered = self.mentorships.copy()

        if major:
            filtered = [m for m in filtered if
                       major.lower() in str(m['majors']).lower() or
                       'all majors' in str(m['majors']).lower() or
                       'general' in str(m['majors']).lower()]

        if target_audience:
            filtered = [m for m in filtered if
                       target_audience.lower() in m['target_audience'].lower()]

        if cost:
            filtered = [m for m in filtered if cost.lower() in m['cost'].lower()]

        return filtered

    def display_mentorships(self, filtered_list=None):
        """
        Display mentorship opportunities in a formatted way
        """
        programs = filtered_list if filtered_list is not None else self.mentorships

        if not programs:
            print("\n[!] No mentorship programs found matching your criteria")
            return

        print("\n" + "="*100)
        print("MENTORSHIP OPPORTUNITIES FOR STUDENTS")
        print("="*100)

        for idx, program in enumerate(programs, 1):
            print(f"\n{idx}. {program['organization']} - {program['program_name']}")
            print("-" * 100)
            print(f"   Description: {program['description']}")
            print(f"   Target Audience: {program['target_audience']}")
            print(f"   Majors: {', '.join(program['majors'])}")
            print(f"   Cost: {program['cost']}")
            print(f"   Format: {program['format']}")
            print(f"   Duration: {program['duration']}")
            print(f"   Website: {program['website']}")
            print(f"   Application: {program['application_process']}")
            print(f"   Requirements: {program['requirements']}")

        print("\n" + "="*100)
        print(f"TOTAL PROGRAMS: {len(programs)}")
        print("="*100)

    def save_to_json(self, filename='mentorship_opportunities.json'):
        """
        Save mentorship data to JSON file
        """
        data = {
            'mentorships': self.mentorships,
            'total_count': len(self.mentorships),
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'categories': {
                'tech_programs': len([m for m in self.mentorships if any(maj in str(m['majors']).lower() for maj in ['computer science', 'engineering', 'data science'])]),
                'community_college_friendly': len([m for m in self.mentorships if 'community college' in m['target_audience'].lower()]),
                'free_programs': len([m for m in self.mentorships if m['cost'].lower() == 'free']),
                'virtual_programs': len([m for m in self.mentorships if 'virtual' in m['format'].lower()])
            }
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"\n[+] Mentorship data saved to {filename}")

    def show_filter_menu(self):
        """
        Interactive menu for filtering mentorship programs
        """
        print("\n" + "="*100)
        print("FILTER MENTORSHIP PROGRAMS")
        print("="*100)
        print("\n1. View All Programs")
        print("2. Filter by Major")
        print("3. Filter by Community College Focus")
        print("4. Filter by Free Programs Only")
        print("5. Filter by Virtual Programs")
        print("6. Exit")
        print("="*100)

        try:
            choice = input("\nEnter your choice (1-6): ").strip()

            if choice == "1":
                return self.mentorships
            elif choice == "2":
                print("\nCommon majors:")
                print("- Computer Science")
                print("- Engineering")
                print("- Data Science")
                print("- Business")
                print("- General (for all majors)")
                major = input("\nEnter your major: ").strip()
                return self.filter_by_criteria(major=major)
            elif choice == "3":
                return self.filter_by_criteria(target_audience="community college")
            elif choice == "4":
                return self.filter_by_criteria(cost="free")
            elif choice == "5":
                filtered = [m for m in self.mentorships if 'virtual' in m['format'].lower()]
                return filtered
            elif choice == "6":
                return None
            else:
                print("[!] Invalid choice. Showing all programs.")
                return self.mentorships
        except KeyboardInterrupt:
            print("\n\nExiting...")
            return None

    def run(self):
        """
        Run the scraper and display results
        """
        print("="*100)
        print("MENTORSHIP OPPORTUNITIES SCRAPER FOR STUDENTS")
        print("Targeting: Community College Students, Major-Specific, and General Programs")
        print("="*100 + "\n")

        # Collect all mentorship programs
        self.add_tech_mentorship_programs()
        self.add_general_mentorship_programs()
        self.add_community_college_specific()

        print(f"\n[+] Total mentorship programs collected: {len(self.mentorships)}")

        # Show filter menu
        filtered_programs = self.show_filter_menu()

        if filtered_programs is None:
            print("\nExiting...")
            return

        # Display results
        self.display_mentorships(filtered_programs)

        # Save to file
        self.save_to_json()

        # Print summary statistics
        print("\n" + "="*100)
        print("SUMMARY STATISTICS")
        print("="*100)
        print(f"Tech/STEM Programs: {len([m for m in self.mentorships if any(maj in str(m['majors']).lower() for maj in ['computer science', 'engineering', 'data science'])])}")
        print(f"Community College Friendly: {len([m for m in self.mentorships if 'community college' in m['target_audience'].lower()])}")
        print(f"Free Programs: {len([m for m in self.mentorships if m['cost'].lower() == 'free'])}")
        print(f"Virtual Programs: {len([m for m in self.mentorships if 'virtual' in m['format'].lower()])}")
        print(f"All Majors Welcome: {len([m for m in self.mentorships if 'all majors' in str(m['majors']).lower()])}")
        print("="*100)


if __name__ == "__main__":
    scraper = MentorshipScraper()
    scraper.run()
