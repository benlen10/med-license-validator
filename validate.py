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

  response_text = str(response.text.encode('utf8'))

  license_status = "NOT ACTIVE"
  if "Active" in response_text:
    license_status = "ACTIVE"
   

  print("License number {} is {}".format(license_number, license_status))





if __name__ == "__main__":
    main()