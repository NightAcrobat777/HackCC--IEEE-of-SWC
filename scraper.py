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

def scrape_course_articulation(from_school, to_school, year_name="2025-2026", debug=False):
    """
    Scrape detailed course articulation from assist.org using Playwright
    
    Args:
        from_school: Name of the school student is transferring from
        to_school: Name of the school student is transferring to
        year_name: Academic year (e.g., "2025-2026")
        debug: If True, include additional debugging info
    
    Returns:
        Dictionary containing course articulation data
    """
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://www.assist.org", wait_until='networkidle')
            time.sleep(3)
            
            result = {
                'from_school': from_school,
                'to_school': to_school,
                'year': year_name,
                'courses': [],
                'error': None,
                'debug_info': {}
            }
            
            # Debug: Check page structure
            if debug:
                inputs = page.query_selector_all('input')
                result['debug_info']['total_inputs'] = len(inputs)
                selects = page.query_selector_all('select')
                result['debug_info']['total_selects'] = len(selects)
            
            # Try to find and fill school dropdowns
            try:
                # Wait for inputs to be available
                page.wait_for_selector('input[placeholder*="institution"]', timeout=5000)
                
                # Look for school selector inputs
                inputs = page.query_selector_all('input[placeholder*="institution"]')
                
                if debug:
                    result['debug_info']['institution_inputs_found'] = len(inputs)
                
                if len(inputs) >= 2:
                    # Fill "to" school (receiving institution)
                    to_input = inputs[1]
                    to_input.click()
                    to_input.fill(to_school)
                    time.sleep(1)
                    page.keyboard.press('ArrowDown')
                    time.sleep(0.5)
                    page.keyboard.press('Enter')
                    time.sleep(2)
                    
                    # Fill "from" school (sending institution)
                    from_input = inputs[0]
                    from_input.click()
                    from_input.fill(from_school)
                    time.sleep(1)
                    page.keyboard.press('ArrowDown')
                    time.sleep(0.5)
                    page.keyboard.press('Enter')
                    time.sleep(2)
                    
                    if debug:
                        result['debug_info']['schools_filled'] = True
            except Exception as e:
                if debug:
                    result['debug_info']['schools_error'] = str(e)
            
            # Try to select year
            try:
                selects = page.query_selector_all('select')
                if selects:
                    page.select_option(selects[0], year_name)
                    time.sleep(3)
            except Exception as e:
                if debug:
                    result['debug_info']['year_error'] = str(e)
            
            # Wait for content
            time.sleep(3)
            
            # Try multiple selectors to find course data
            try:
                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Look for course rows in various table formats
                course_rows = soup.find_all('tr')
                
                for row in course_rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        from_course = cells[0].get_text(strip=True)
                        to_course = cells[1].get_text(strip=True)
                        
                        # Filter out header rows and empty rows
                        if (from_course and to_course and 
                            len(from_course) > 2 and len(to_course) > 2 and
                            'course' not in from_course.lower() and 'course' not in to_course.lower()):
                            result['courses'].append({
                                'from_course': from_course,
                                'to_course': to_course
                            })
            except Exception as e:
                if debug:
                    result['debug_info']['scrape_error'] = str(e)
            
            if debug:
                result['debug_info']['courses_found'] = len(result['courses'])
            
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

if __name__ == "__main__":
    result = scrape_transfer_articulation("Berkeley City College", "University of California, Berkeley")
    print(json.dumps(result, indent=2))
