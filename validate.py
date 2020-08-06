#!/usr/bin/python3

import requests
import argparse
from bs4 import BeautifulSoup

# USAGE EXAMPLE #1: python3 validate.py EMT E142304
# USAGE EXAMPLE #2: python3 validate.py AHA 195506016954

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('license_type', help='License type (EMT, AHA or RN)')
  parser.add_argument('license_number', help='License number')
  args = parser.parse_args()
  license_type = args.license_type
  license_number = args.license_number

  if license_type == "EMT":
    validate_esma(license_number)
  if license_type == "AHA":
    validate_aha(license_number)

def validate_esma(license_number):
  session_url = 'https://emsverification.emsa.ca.gov/Verification/'
  session = requests.Session()
  r = session.get(session_url)

  search_page = session.get(r.url)
  soup = BeautifulSoup(search_page.text, "html.parser")

  view_state = soup.select("#__VIEWSTATE")[0]['value']
  event_validation = soup.select("#__EVENTVALIDATION")[0]['value']

  item_request_body = {
  "__VIEWSTATE": view_state,
  "__EVENTVALIDATION": event_validation,
  "sch_button": "Search",
  "t_web_lookup__license_no": license_number
  }

  response = session.post(
      url=r.url, data=item_request_body, headers={"Referer": r.url})

  soup_results_page = BeautifulSoup(response.text, "html.parser")
  find_results = soup_results_page.find('a', id="datagrid_results__ctl3_hl")

  details_page_response = session.get(session_url + find_results["href"])
  soup_details_page = BeautifulSoup(details_page_response.text, "html.parser")

  print("\n-----------CALIFORNIA EMSA CENTRAL REGISTRY LICENSE STATUS-----------\n")

  full_name = soup_details_page.find('span', id="_ctl25__ctl1_full_name").text
  print("FULL NAME: " + str(full_name))

  license_status = soup_details_page.find(
      'span', id="_ctl32__ctl1_status").text
  print("LICENSE STATUS: " + str(license_status))

  ca_license_type = soup_details_page.find(
      'span', id="_ctl32__ctl1_license_type").text
  print("LICENSE TYPE: " + str(ca_license_type))

  issue_date = soup_details_page.find(
      'span', id="_ctl32__ctl1_issue_date").text
  print("ISSUE DATE: " + str(issue_date))

  exp_date = soup_details_page.find('span', id="_ctl32__ctl1_expiry").text
  print("EXP DATE: " + str(exp_date))

  print("\n-----------CALIFORNIA EMSA CENTRAL REGISTRY LICENSE STATUS-----------\n")


def validate_aha(license_number):
  url = "https://ecards.heart.org/Student/MyeCards/VerifyECards"

  payload = 'codes={}'.format(license_number)
  headers = {
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'Request-Id': '|U0Hjw.ACgYH',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'Request-Context': 'appId=cid-v1:d39741ef-33b3-4dd6-bd05-8a42831df1ef'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  soup_results_page = BeautifulSoup(response.text, "html.parser")
  table = soup_results_page.find('table', id="tblECards")
  print("SOUP RESULTS: " + str(table))
  table_body = table.find('tbody')
  table_rows = table_body.find_all('tr')
  row0 = table_rows[0]
  cols = row0.find_all('td')

  print("\n-----------AHA CPR/BLS CERTIFICATION STATUS-----------\n")

  full_name = cols[2].text.strip()
  print("FULL NAME: " + full_name)

  license_status = cols[3].text.strip()
  print("LICENSE STATUS: " + license_status)

  renewal_date = cols[4].text.strip()
  print("RENEWAL DATE: " + renewal_date)

  print("\n-----------AHA CPR/BLS CERTIFICATION STATUS-----------\n")


if __name__ == "__main__":
    main()