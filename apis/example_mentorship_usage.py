#!/usr/bin/env python3
"""
Example usage of the mentorship scraper
Demonstrates different ways to use the scraper
"""

from apis.mentorship_scraper import MentorshipScraper

def example_1_run_interactive():
    """
    Example 1: Run the full interactive scraper
    """
    print("Example 1: Running interactive mentorship scraper")
    print("="*80)

    scraper = MentorshipScraper()
    scraper.run()


def example_2_filter_by_major():
    """
    Example 2: Get mentorships for a specific major
    """
    print("\n\nExample 2: Filtering by Computer Science major")
    print("="*80)

    scraper = MentorshipScraper()

    # Collect all programs
    scraper.add_tech_mentorship_programs()
    scraper.add_general_mentorship_programs()
    scraper.add_community_college_specific()

    # Filter by major
    cs_programs = scraper.filter_by_criteria(major="Computer Science")

    # Display
    scraper.display_mentorships(cs_programs)


def example_3_community_college_focus():
    """
    Example 3: Get mentorships specifically for community college students
    """
    print("\n\nExample 3: Community College Focused Programs")
    print("="*80)

    scraper = MentorshipScraper()

    # Collect all programs
    scraper.add_tech_mentorship_programs()
    scraper.add_general_mentorship_programs()
    scraper.add_community_college_specific()

    # Filter for community college
    cc_programs = scraper.filter_by_criteria(target_audience="community college")

    # Display
    scraper.display_mentorships(cc_programs)


def example_4_free_programs_only():
    """
    Example 4: Get only free mentorship programs
    """
    print("\n\nExample 4: Free Mentorship Programs Only")
    print("="*80)

    scraper = MentorshipScraper()

    # Collect all programs
    scraper.add_tech_mentorship_programs()
    scraper.add_general_mentorship_programs()
    scraper.add_community_college_specific()

    # Filter for free programs
    free_programs = scraper.filter_by_criteria(cost="free")

    # Display
    scraper.display_mentorships(free_programs)

    # Save to JSON
    scraper.save_to_json('free_mentorship_programs.json')


def example_5_engineering_majors():
    """
    Example 5: Get mentorships for engineering majors
    """
    print("\n\nExample 5: Engineering Major Mentorships")
    print("="*80)

    scraper = MentorshipScraper()

    # Collect all programs
    scraper.add_tech_mentorship_programs()
    scraper.add_general_mentorship_programs()
    scraper.add_community_college_specific()

    # Filter by engineering
    eng_programs = scraper.filter_by_criteria(major="Engineering")

    # Display
    scraper.display_mentorships(eng_programs)


def example_6_programmatic_access():
    """
    Example 6: Access mentorship data programmatically
    """
    print("\n\nExample 6: Programmatic Access to Mentorship Data")
    print("="*80)

    scraper = MentorshipScraper()

    # Collect all programs
    scraper.add_tech_mentorship_programs()
    scraper.add_general_mentorship_programs()
    scraper.add_community_college_specific()

    # Access data directly
    print(f"Total programs: {len(scraper.mentorships)}")

    # Get all virtual programs
    virtual_programs = [m for m in scraper.mentorships if 'virtual' in m['format'].lower()]
    print(f"Virtual programs: {len(virtual_programs)}")

    # Get programs for women
    women_programs = [m for m in scraper.mentorships if 'women' in m['target_audience'].lower()]
    print(f"Programs targeting women: {len(women_programs)}")

    # Get all organizations
    organizations = set(m['organization'] for m in scraper.mentorships)
    print(f"\nOrganizations offering mentorship ({len(organizations)}):")
    for org in sorted(organizations)[:10]:  # Show first 10
        print(f"  - {org}")


def main():
    """
    Main function to demonstrate different examples
    """
    print("MENTORSHIP SCRAPER - EXAMPLE USAGE")
    print("="*80)
    print("\nAvailable examples:")
    print("1. Run full interactive scraper")
    print("2. Filter by Computer Science major")
    print("3. Community College focused programs")
    print("4. Free programs only")
    print("5. Engineering major mentorships")
    print("6. Programmatic data access")
    print("\n0. Run default (interactive)")

    try:
        choice = input("\nSelect example to run (0-6): ").strip()

        if choice == "1" or choice == "0" or choice == "":
            example_1_run_interactive()
        elif choice == "2":
            example_2_filter_by_major()
        elif choice == "3":
            example_3_community_college_focus()
        elif choice == "4":
            example_4_free_programs_only()
        elif choice == "5":
            example_5_engineering_majors()
        elif choice == "6":
            example_6_programmatic_access()
        else:
            print("Invalid choice. Running default interactive scraper.")
            example_1_run_interactive()

    except KeyboardInterrupt:
        print("\n\nExiting...")


if __name__ == "__main__":
    main()
