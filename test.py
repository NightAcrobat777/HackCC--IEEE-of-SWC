from scraper import scrape_course_articulation
import json

schools = [
    ("Berkeley City College", "University of California, Berkeley"),
]

print("Scraping course articulation data using Playwright...")
print()

for from_school, to_school in schools:
    print(f"{from_school} → {to_school}:")
    result = scrape_course_articulation(from_school, to_school, year_name="2025-2026", debug=True)
    
    if result.get('error'):
        print(f"  Error: {result['error']}")
    else:
        print(f"  Courses found: {len(result['courses'])}")
        if result['courses']:
            print(f"\n  First 10 courses:")
            for i, course in enumerate(result['courses'][:10]):
                print(f"    {course['from_course']} → {course['to_course']}")
        
    print(f"\n  Full result:")
    print(json.dumps(result, indent=2))
