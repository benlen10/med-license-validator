import requests
import argparse
from bs4 import BeautifulSoup

# USAGE EXAMPLE: python3 validate.py E142304

SESSION_URL='https://emsverification.emsa.ca.gov/Verification/'

def main():
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('license_number', help='CA EMT license number')
  args = parser.parse_args()
  license_number = args.license_number

  session = requests.Session()
  r = session.get(SESSION_URL)

  search_page = session.get(r.url)
  soup = BeautifulSoup(search_page.text,"html.parser")

  view_state = soup.select("#__VIEWSTATE")[0]['value']
  event_validation = soup.select("#__EVENTVALIDATION")[0]['value']

  item_request_body = {
  "__VIEWSTATE":view_state,
  "__EVENTVALIDATION":event_validation,
  "sch_button":"Search",
  "t_web_lookup__license_no":license_number
  }

  response = session.post(url=r.url, data=item_request_body, headers={"Referer": r.url})

  soup_results_page = BeautifulSoup(response.text,"html.parser")
  find_results = soup_results_page.find('a', id="datagrid_results__ctl3_hl")

  details_page_response = session.get(SESSION_URL + find_results["href"])
  soup_details_page = BeautifulSoup(details_page_response.text,"html.parser")

  full_name = soup_details_page.find('span', id="_ctl25__ctl1_full_name").text
  print("FULL NAME: " + str(full_name))

  license_status = soup_details_page.find('span', id="_ctl32__ctl1_status").text
  print("LICENSE STATUS: " + str(license_status))

  license_type = soup_details_page.find('span', id="_ctl32__ctl1_license_type").text
  print("LICENSE TYPE: " + str(license_type))
  


if __name__ == "__main__":
    main()