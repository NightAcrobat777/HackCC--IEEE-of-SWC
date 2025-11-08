import requests
from bs4 import BeautifulSoup
import json
from playwright.sync_api import sync_playwright
import time

def scrape_assist_org_with_javascript(url="https://www.assist.org"):
    """
    Scrape assist.org using Playwright to handle JavaScript rendering
    
    Args:
        url: The URL to scrape (default: assist.org homepage)
    
    Returns:
        Dictionary containing scraped data
    """
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until='networkidle')
            time.sleep(2)
            
            html = page.content()
            browser.close()
        
        return scrape_from_html(html)
    
    except Exception as e:
        return {'error': f'Failed to scrape {url}: {str(e)}'}

def scrape_assist_org_with_selenium(url="https://www.assist.org"):
    """
    Alias for scrape_assist_org_with_javascript
    """
    return scrape_assist_org_with_javascript(url)

def get_institutions_list(url="https://www.assist.org"):
    """
    Get the list of academic institutions from assist.org dropdowns
    
    Args:
        url: The URL to scrape (default: assist.org homepage)
    
    Returns:
        Dictionary containing institution lists for different categories
    """
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until='networkidle')
            time.sleep(2)
            
            institutions = {
                'from_institution': [],
                'transfer_institution': []
            }
            
            try:
                page.click('#None-governing-institution-select')
                time.sleep(1.5)
                options = page.query_selector_all('ul[role="listbox"] li, .ng-option, [role="option"]')
                for option in options:
                    text = option.inner_text().strip()
                    if text and len(text) > 0 and not text.startswith('link') and not 'Don\'t see' in text:
                        institutions['from_institution'].append(text)
            except Exception as e:
                pass
            
            try:
                page.keyboard.press('Escape')
                time.sleep(1)
                page.reload(wait_until='networkidle')
                time.sleep(2)
                page.click('#institution')
                time.sleep(2)
                options = page.query_selector_all('ul[role="listbox"] li, .ng-option, [role="option"]')
                for option in options:
                    text = option.inner_text().strip()
                    if text and len(text) > 0 and not text.startswith('link') and not 'Don\'t see' in text:
                        institutions['transfer_institution'].append(text)
            except Exception as e:
                pass
            
            browser.close()
        
        institutions['from_institution'] = list(dict.fromkeys(institutions['from_institution']))
        institutions['transfer_institution'] = list(dict.fromkeys(institutions['transfer_institution']))
        
        return institutions
    
    except Exception as e:
        return {'error': f'Failed to get institutions: {str(e)}'}

def scrape_assist_org(url="https://www.assist.org"):
    """
    Simple webscraper for assist.org (static content)
    
    Args:
        url: The URL to scrape (default: assist.org homepage)
    
    Returns:
        Dictionary containing scraped data
    """
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data = {
            'url': url,
            'title': soup.title.string if soup.title else 'No title found',
            'headings': [],
            'links': [],
            'paragraphs': [],
            'form_labels': [],
            'form_fields': []
        }
        
        for h in soup.find_all(['h1', 'h2', 'h3'], limit=10):
            text = h.get_text(strip=True)
            if text:
                data['headings'].append(text)
        
        for link in soup.find_all('a', limit=20):
            href = link.get('href')
            text = link.get_text(strip=True)
            if href and text:
                data['links'].append({'text': text, 'url': href})
        
        for p in soup.find_all('p', limit=10):
            text = p.get_text(strip=True)
            if text:
                data['paragraphs'].append(text)
        
        for label in soup.find_all('label', limit=20):
            text = label.get_text(strip=True)
            if text:
                data['form_labels'].append(text)
        
        for field in soup.find_all(['input', 'select', 'textarea'], limit=20):
            field_type = field.get('type', field.name)
            field_id = field.get('id', 'no-id')
            field_name = field.get('name', 'no-name')
            data['form_fields'].append({
                'type': field_type,
                'id': field_id,
                'name': field_name
            })
        
        return data
    
    except requests.exceptions.RequestException as e:
        return {'error': f'Failed to fetch {url}: {str(e)}'}

def scrape_from_html(html_content):
    """
    Scrape data from raw HTML content
    
    Args:
        html_content: Raw HTML string to parse
    
    Returns:
        Dictionary containing scraped data
    """
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    data = {
        'headings': [],
        'descriptions': [],
        'form_labels': [],
        'form_fields': [],
        'text_content': []
    }
    
    for h in soup.find_all(['h1', 'h2', 'h3']):
        text = h.get_text(strip=True)
        if text:
            data['headings'].append(text)
    
    for p in soup.find_all('p'):
        text = p.get_text(strip=True)
        if text:
            data['descriptions'].append(text)
    
    for label in soup.find_all('label'):
        text = label.get_text(strip=True)
        if text:
            data['form_labels'].append(text)
    
    for field in soup.find_all(['input', 'select', 'textarea']):
        field_type = field.get('type', field.name)
        field_id = field.get('id', 'no-id')
        field_name = field.get('name', 'no-name')
        aria_label = field.get('aria-label', '')
        data['form_fields'].append({
            'type': field_type,
            'id': field_id,
            'name': field_name,
            'aria-label': aria_label
        })
    
    all_text = soup.get_text(strip=True)
    if all_text:
        data['raw_text'] = all_text[:500]
    
    return data

def get_institution_id(name):
    """
    Get institution ID from assist.org API
    
    Args:
        name: Institution name
    
    Returns:
        Institution ID or None
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get('https://www.assist.org/api/institutions', headers=headers, timeout=10)
        response.raise_for_status()
        institutions = response.json()
        
        for inst in institutions:
            inst_names = inst.get('names', [])
            for name_obj in inst_names:
                if name_obj.get('name', '').lower() == name.lower():
                    return inst.get('id')
        
        return None
    except Exception as e:
        return None

def scrape_transfer_articulation(from_school, to_school, debug=False):
    """
    Get transfer articulation data from assist.org API
    
    Args:
        from_school: Name of the school student is transferring from
        to_school: Name of the school student is transferring to
        debug: If True, include additional debugging info
    
    Returns:
        Dictionary containing transfer articulation data
    """
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        from_id = get_institution_id(from_school)
        to_id = get_institution_id(to_school)
        
        result = {
            'from_school': from_school,
            'to_school': to_school,
            'from_id': from_id,
            'to_id': to_id,
            'agreements': [],
            'error': None
        }
        
        if not from_id or not to_id:
            result['error'] = f'Could not find institution IDs. From: {from_id}, To: {to_id}'
            return result
        
        agreements_url = f'https://www.assist.org/api/institutions/{to_id}/agreements'
        response = requests.get(agreements_url, headers=headers, timeout=10)
        response.raise_for_status()
        agreements = response.json()
        
        if debug:
            result['all_agreements_count'] = len(agreements)
        
        seen_institution_ids = set()
        for agreement in agreements:
            if agreement.get('institutionParentId') == from_id:
                inst_id = agreement.get('institutionParentId')
                if inst_id not in seen_institution_ids:
                    seen_institution_ids.add(inst_id)
                    result['agreements'].append({
                        'institution_name': agreement.get('institutionName'),
                        'institution_code': agreement.get('code'),
                        'is_community_college': agreement.get('isCommunityCollege'),
                        'sending_year_ids': agreement.get('sendingYearIds'),
                        'receiving_year_ids': agreement.get('receivingYearIds'),
                        'from_id': from_id,
                        'to_id': to_id
                    })
        
        if result['agreements'] and result['agreements'][0].get('id'):
            agreement_id = result['agreements'][0]['id']
            courses_url = f'https://www.assist.org/api/agreements/{agreement_id}/courses'
            try:
                courses_response = requests.get(courses_url, headers=headers, timeout=10)
                courses_response.raise_for_status()
                courses = courses_response.json()
                result['courses'] = courses
            except Exception as e:
                result['courses_error'] = str(e)
        
        return result
    
    except Exception as e:
        return {'error': f'Failed to scrape articulation data: {str(e)}'}

def scrape_course_articulation(from_school, to_school, year_name="2025-2026", debug=False, max_retries=2):
    """
    Scrape detailed course articulation from assist.org using Playwright
    
    Args:
        from_school: Name of the school student is transferring from
        to_school: Name of the school student is transferring to
        year_name: Academic year (e.g., "2025-2026")
        debug: If True, include additional debugging info
        max_retries: Number of times to retry on failure
    
    Returns:
        Dictionary containing course articulation data
    """
    
    def attempt_scrape():
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.set_default_timeout(15000)
                page.goto("https://www.assist.org", wait_until='domcontentloaded')
                time.sleep(2)
                
                result = {
                    'from_school': from_school,
                    'to_school': to_school,
                    'year': year_name,
                    'courses': [],
                    'error': None,
                    'debug_info': {}
                }
                
                try:
                    page.wait_for_selector('ng-select', timeout=15000)
                    ng_selects = page.query_selector_all('ng-select')
                    
                    if debug:
                        result['debug_info']['ng_selects_found'] = len(ng_selects)
                    
                    if len(ng_selects) >= 2:
                        to_selector = ng_selects[1]
                        from_selector = ng_selects[0]
                        
                        try:
                            to_input = to_selector.query_selector('input[type="search"]')
                            if not to_input:
                                to_input = to_selector.query_selector('input')
                            
                            if to_input:
                                to_input.click(timeout=5000)
                                time.sleep(0.5)
                                to_input.fill("")
                                to_input.fill(to_school)
                                time.sleep(1)
                                
                                page.wait_for_selector('[role="option"]', timeout=8000)
                                options = page.query_selector_all('[role="option"]')
                                if options:
                                    options[0].click(timeout=5000)
                                    time.sleep(1.5)
                        except Exception as e:
                            if debug:
                                result['debug_info']['to_school_error'] = str(e)
                        
                        try:
                            from_input = from_selector.query_selector('input[type="search"]')
                            if not from_input:
                                from_input = from_selector.query_selector('input')
                            
                            if from_input:
                                from_input.click(timeout=5000)
                                time.sleep(0.5)
                                from_input.fill("")
                                from_input.fill(from_school)
                                time.sleep(1)
                                
                                page.wait_for_selector('[role="option"]', timeout=8000)
                                options = page.query_selector_all('[role="option"]')
                                if options:
                                    options[0].click(timeout=5000)
                                    time.sleep(1.5)
                        except Exception as e:
                            if debug:
                                result['debug_info']['from_school_error'] = str(e)
                        
                        try:
                            page.wait_for_selector('table tbody tr, .course-table tr, [class*="course"] tr', timeout=12000)
                            time.sleep(1)
                        except:
                            if debug:
                                result['debug_info']['no_table_found'] = True
                    
                    html = page.content()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    course_rows = soup.find_all('tr')
                    
                    for row in course_rows:
                        cells = row.find_all(['td', 'th'])
                        if len(cells) >= 2:
                            from_course = cells[0].get_text(strip=True)
                            to_course = cells[1].get_text(strip=True)
                            
                            if (from_course and to_course and 
                                len(from_course) > 1 and len(to_course) > 1 and
                                from_course.lower() not in ['course', 'courses', 'from course', 'prerequisite'] and
                                to_course.lower() not in ['course', 'courses', 'to course', 'transfer to']):
                                
                                units = None
                                if len(cells) > 2:
                                    units_text = cells[2].get_text(strip=True)
                                    try:
                                        units = float(units_text)
                                    except:
                                        units = units_text if units_text else None
                                
                                result['courses'].append({
                                    'from_course': from_course,
                                    'to_course': to_course,
                                    'units': units
                                })
                    
                    if debug:
                        result['debug_info']['courses_found'] = len(result['courses'])
                
                except Exception as e:
                    result['error'] = f'Failed during scraping: {str(e)}'
                    if debug:
                        result['debug_info']['scrape_error'] = str(e)
                
                browser.close()
                
                return result
        
        except Exception as e:
            return {
                'from_school': from_school,
                'to_school': to_school,
                'year': year_name,
                'error': f'Failed to scrape course articulation: {str(e)}',
                'courses': []
            }
    
    for attempt in range(max_retries + 1):
        result = attempt_scrape()
        if not result.get('error') or attempt == max_retries:
            if debug and attempt > 0:
                result['debug_info']['retry_attempt'] = attempt
            return result
        time.sleep(2 ** attempt)
    
    return result

def get_degree_information(from_school, to_school, year_name="2025-2026", debug=False):
    """
    Get degree transfer information with REST API agreement data
    
    Args:
        from_school: Name of the school student is transferring from
        to_school: Name of the school student is transferring to
        year_name: Academic year (e.g., "2025-2026")
        debug: If True, include additional debugging info
    
    Returns:
        Dictionary containing degree transfer information with assist.org link
    """
    
    result = {
        'from_school': from_school,
        'to_school': to_school,
        'year': year_name,
        'agreement': None,
        'assist_url': 'https://www.assist.org',
        'error': None
    }
    
    agreement_result = scrape_transfer_articulation(from_school, to_school, debug=debug)
    
    if agreement_result.get('error'):
        result['error'] = agreement_result['error']
        return result
    
    agreements = agreement_result.get('agreements', [])
    if not agreements:
        result['error'] = 'No transfer agreement found for this school pair'
        return result
    
    agreement = agreements[0]
    result['agreement'] = {
        'from_school': from_school,
        'to_school': to_school,
        'institution_name': agreement.get('institution_name'),
        'institution_code': agreement.get('institution_code'),
        'is_community_college': agreement.get('is_community_college'),
        'years_supported': len(agreement.get('sending_year_ids', []))
    }
    
    return result

if __name__ == "__main__":
    result = scrape_transfer_articulation("Berkeley City College", "University of California, Berkeley")
    print(json.dumps(result, indent=2))
