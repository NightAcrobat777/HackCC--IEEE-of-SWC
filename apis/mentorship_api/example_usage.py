#!/usr/bin/env python3
"""
Example usage of the Mentorship API
Demonstrates how to interact with the API endpoints
"""

import requests
import json

# API base URL
BASE_URL = 'http://localhost:5002'


def print_separator():
    """Print a visual separator"""
    print("\n" + "="*80)


def example_1_get_all_mentorships():
    """Example 1: Get all mentorship programs"""
    print_separator()
    print("EXAMPLE 1: Get all mentorship programs")
    print_separator()

    response = requests.get(f'{BASE_URL}/api/mentorships')

    if response.status_code == 200:
        data = response.json()
        print(f"\nTotal mentorship programs: {data['total_count']}")
        print(f"Returned: {data['returned_count']}")
        print(f"\nFirst 3 programs:")

        for i, mentorship in enumerate(data['mentorships'][:3], 1):
            print(f"\n{i}. {mentorship['organization']} - {mentorship['program_name']}")
            print(f"   Target Audience: {mentorship['target_audience']}")
            print(f"   Cost: {mentorship['cost']}")
            print(f"   Format: {mentorship['format']}")
    else:
        print(f"Error: {response.status_code}")


def example_2_filter_by_major():
    """Example 2: Filter by Computer Science major"""
    print_separator()
    print("EXAMPLE 2: Filter by Computer Science major")
    print_separator()

    params = {'major': 'computer science'}
    response = requests.get(f'{BASE_URL}/api/mentorships', params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"\nComputer Science programs found: {data['total_count']}")

        for i, mentorship in enumerate(data['mentorships'][:5], 1):
            print(f"\n{i}. {mentorship['organization']} - {mentorship['program_name']}")
            print(f"   Majors: {', '.join(mentorship['majors'][:3])}")
            print(f"   Website: {mentorship['website']}")
    else:
        print(f"Error: {response.status_code}")


def example_3_get_free_programs():
    """Example 3: Get only free programs"""
    print_separator()
    print("EXAMPLE 3: Get only free mentorship programs")
    print_separator()

    response = requests.get(f'{BASE_URL}/api/mentorships/free')

    if response.status_code == 200:
        data = response.json()
        print(f"\nFree programs found: {data['total_count']}")

        for i, mentorship in enumerate(data['mentorships'][:5], 1):
            print(f"\n{i}. {mentorship['organization']} - {mentorship['program_name']}")
            print(f"   Description: {mentorship['description'][:80]}...")
            print(f"   Duration: {mentorship['duration']}")
    else:
        print(f"Error: {response.status_code}")


def example_4_community_college_programs():
    """Example 4: Get community college friendly programs"""
    print_separator()
    print("EXAMPLE 4: Get community college friendly programs")
    print_separator()

    response = requests.get(f'{BASE_URL}/api/mentorships/community-college')

    if response.status_code == 200:
        data = response.json()
        print(f"\nCommunity college friendly programs found: {data['total_count']}")

        for i, mentorship in enumerate(data['mentorships'][:5], 1):
            print(f"\n{i}. {mentorship['organization']} - {mentorship['program_name']}")
            print(f"   Target Audience: {mentorship['target_audience']}")
            print(f"   Requirements: {mentorship['requirements']}")
    else:
        print(f"Error: {response.status_code}")


def example_5_filter_by_format():
    """Example 5: Filter by virtual format"""
    print_separator()
    print("EXAMPLE 5: Filter by virtual format")
    print_separator()

    params = {'format': 'virtual'}
    response = requests.get(f'{BASE_URL}/api/mentorships', params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"\nVirtual programs found: {data['total_count']}")

        for i, mentorship in enumerate(data['mentorships'][:5], 1):
            print(f"\n{i}. {mentorship['organization']} - {mentorship['program_name']}")
            print(f"   Format: {mentorship['format']}")
            print(f"   Application: {mentorship['application_process']}")
    else:
        print(f"Error: {response.status_code}")


def example_6_get_stats():
    """Example 6: Get statistics"""
    print_separator()
    print("EXAMPLE 6: Get mentorship statistics")
    print_separator()

    response = requests.get(f'{BASE_URL}/api/mentorships/stats')

    if response.status_code == 200:
        data = response.json()
        print(f"\nTotal programs: {data['total_programs']}")

        print("\nTop organizations:")
        for org, count in list(data['by_organization'].items())[:5]:
            print(f"  - {org}: {count} program(s)")

        print("\nBy format:")
        for fmt, count in data['by_format'].items():
            print(f"  - {fmt}: {count}")

        print("\nBy cost:")
        for cost, count in data['by_cost'].items():
            print(f"  - {cost}: {count}")

        if 'categories' in data:
            print("\nCategories:")
            for category, count in data['categories'].items():
                print(f"  - {category}: {count}")
    else:
        print(f"Error: {response.status_code}")


def example_7_get_organizations():
    """Example 7: Get all organizations"""
    print_separator()
    print("EXAMPLE 7: Get all organizations")
    print_separator()

    response = requests.get(f'{BASE_URL}/api/mentorships/organizations')

    if response.status_code == 200:
        data = response.json()
        print(f"\nTotal organizations: {data['count']}")
        print("\nFirst 10 organizations:")
        for org in data['organizations'][:10]:
            print(f"  - {org}")
    else:
        print(f"Error: {response.status_code}")


def example_8_get_majors():
    """Example 8: Get all majors"""
    print_separator()
    print("EXAMPLE 8: Get all majors")
    print_separator()

    response = requests.get(f'{BASE_URL}/api/mentorships/majors')

    if response.status_code == 200:
        data = response.json()
        print(f"\nTotal majors: {data['count']}")
        print("\nAvailable majors:")
        for major in data['majors']:
            print(f"  - {major}")
    else:
        print(f"Error: {response.status_code}")


def example_9_pagination():
    """Example 9: Use pagination"""
    print_separator()
    print("EXAMPLE 9: Use pagination (limit and offset)")
    print_separator()

    params = {'limit': 5, 'offset': 0}
    response = requests.get(f'{BASE_URL}/api/mentorships', params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"\nTotal programs: {data['total_count']}")
        print(f"Showing results {data['offset']+1}-{data['offset']+data['returned_count']}")

        for i, mentorship in enumerate(data['mentorships'], data['offset']+1):
            print(f"\n{i}. {mentorship['organization']} - {mentorship['program_name']}")
    else:
        print(f"Error: {response.status_code}")


def example_10_combined_filters():
    """Example 10: Combine multiple filters"""
    print_separator()
    print("EXAMPLE 10: Combine multiple filters (free + virtual + engineering)")
    print_separator()

    params = {
        'cost': 'free',
        'format': 'virtual',
        'major': 'engineering'
    }
    response = requests.get(f'{BASE_URL}/api/mentorships', params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"\nPrograms matching all filters: {data['total_count']}")

        for i, mentorship in enumerate(data['mentorships'], 1):
            print(f"\n{i}. {mentorship['organization']} - {mentorship['program_name']}")
            print(f"   Majors: {', '.join(mentorship['majors'][:3])}")
            print(f"   Cost: {mentorship['cost']} | Format: {mentorship['format']}")
    else:
        print(f"Error: {response.status_code}")


def example_11_get_specific_program():
    """Example 11: Get a specific program by index"""
    print_separator()
    print("EXAMPLE 11: Get specific mentorship program by index")
    print_separator()

    index = 0  # Get the first program
    response = requests.get(f'{BASE_URL}/api/mentorships/{index}')

    if response.status_code == 200:
        mentorship = response.json()
        print(f"\nOrganization: {mentorship['organization']}")
        print(f"Program: {mentorship['program_name']}")
        print(f"Description: {mentorship['description']}")
        print(f"Target Audience: {mentorship['target_audience']}")
        print(f"Majors: {', '.join(mentorship['majors'])}")
        print(f"Cost: {mentorship['cost']}")
        print(f"Format: {mentorship['format']}")
        print(f"Duration: {mentorship['duration']}")
        print(f"Website: {mentorship['website']}")
        print(f"Application: {mentorship['application_process']}")
        print(f"Requirements: {mentorship['requirements']}")
    else:
        print(f"Error: {response.status_code}")


def example_12_refresh_data():
    """Example 12: Refresh mentorship data"""
    print_separator()
    print("EXAMPLE 12: Refresh mentorship data from scraper")
    print_separator()

    print("\nSending refresh request...")
    response = requests.post(f'{BASE_URL}/api/mentorships/refresh')

    if response.status_code == 200:
        data = response.json()
        print(f"\nSuccess: {data['message']}")
        print(f"Total programs: {data['total_programs']}")
        print(f"Timestamp: {data['timestamp']}")
    else:
        print(f"Error: {response.status_code}")


def main():
    """Main function to run examples"""
    print("\n" + "="*80)
    print("MENTORSHIP API - CLIENT EXAMPLES")
    print("="*80)
    print("\nMake sure the API server is running on http://localhost:5002")
    print("Run: python mentorship_api/start.py")

    try:
        # Check if API is running
        response = requests.get(f'{BASE_URL}/', timeout=2)
        if response.status_code != 200:
            print("\nError: API server is not responding correctly")
            return
    except requests.exceptions.RequestException:
        print("\nError: Cannot connect to API server at http://localhost:5002")
        print("Please start the server first: python mentorship_api/start.py")
        return

    print("\nAvailable examples:")
    print("1.  Get all mentorship programs")
    print("2.  Filter by Computer Science major")
    print("3.  Get only free programs")
    print("4.  Get community college friendly programs")
    print("5.  Filter by virtual format")
    print("6.  Get statistics")
    print("7.  Get all organizations")
    print("8.  Get all majors")
    print("9.  Use pagination")
    print("10. Combine multiple filters")
    print("11. Get specific program by index")
    print("12. Refresh data from scraper")
    print("0.  Run all examples")

    try:
        choice = input("\nSelect example to run (0-12): ").strip()

        examples = {
            "1": example_1_get_all_mentorships,
            "2": example_2_filter_by_major,
            "3": example_3_get_free_programs,
            "4": example_4_community_college_programs,
            "5": example_5_filter_by_format,
            "6": example_6_get_stats,
            "7": example_7_get_organizations,
            "8": example_8_get_majors,
            "9": example_9_pagination,
            "10": example_10_combined_filters,
            "11": example_11_get_specific_program,
            "12": example_12_refresh_data
        }

        if choice == "0":
            # Run all examples
            for example_func in examples.values():
                example_func()
        elif choice in examples:
            examples[choice]()
        else:
            print("Invalid choice")

        print_separator()
        print("Done!")
        print_separator()

    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
