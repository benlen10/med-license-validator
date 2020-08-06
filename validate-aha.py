import requests
import argparse
from bs4 import BeautifulSoup

# USAGE EXAMPLE: python3 validate-aha.py 195506016954

SESSION_URL='https://ecards.heart.org/student/myecards'

def main():
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('license_numbers', help='CSV seperated AHA ID numbers')
  args = parser.parse_args()
  license_number = args.license_numbers

  url = "https://ecards.heart.org/Student/MyeCards/VerifyECards"

  payload = 'codes=195506016954'
  headers = {
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'Request-Id': '|U0Hjw.ACgYH',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'Request-Context': 'appId=cid-v1:d39741ef-33b3-4dd6-bd05-8a42831df1ef'
  }

  response = requests.request("POST", url, headers=headers, data = payload)

  print(response.text.encode('utf8'))

  


if __name__ == "__main__":
    main()