import json
import requests
from bs4 import BeautifulSoup
import logging

# Initalize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# License type constants
EMT = "EMT"
AHA = "AHA"
ARC = "ARC"
DCA = "DCA"

# Lambda event key constants
LICENSE_TYPE = "license_type"
LICENSE_NUMBER = "license_number"
LAST_NAME = "last_name"


# Message constants
LAMBDA_SUCCESS_MESSAGE = "License information successfully retrieved"
INVALID_LICENSE_TYPE_MESSAGE = "Invalid or unsupported license type. Allowed values are: EMT, AHA, ARC or DCA"
MISSING_LICENSE_TYPE = "Missing required key: license_type"
MISSING_LICENSE_NUMBER = "Missing required key: license_number"
MISSING_LAST_NAME_DCA_MESSAGE = "last_name is required for DCA license lookups"



def lambda_handler(event, context):
    """
    Lambda handler invoked by api gateway event
    """
    logger.info("Lambda event: " + json.dumps(event))
    license_type = event.get(LICENSE_TYPE, None)
    license_number = event.get(LICENSE_NUMBER, None)
    last_name = event.get(LAST_NAME, None)

    # Validation checks
    if license_type is None:
        return build_response(400, MISSING_LICENSE_TYPE)
    elif license_number is None:
        return build_response(400, MISSING_LICENSE_NUMBER)
    elif license_type == AHA and last_name is None:
        return build_response(400, MISSING_LAST_NAME_DCA_MESSAGE)


    if license_type == "EMT":
        return validate_esma(license_number)
    elif license_type == "AHA":
        return validate_aha(license_number)
    elif license_type == "ARC":
        return validate_arc(license_number)
    elif license_type == "DCA":
        return validate_dca(license_number, last_name)
    else:
        return build_response(400, INVALID_LICENSE_TYPE_MESSAGE)
    

def build_response(status_code, message, license_status ="null", exp_date = "null"):
    response = {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "status ": message,
            "license_status ": license_status,
            "exp_date": exp_date
        })
    }
    logger.info("Lambda response: " + json.dumps(response))
    return response


def validate_esma(license_number):
    """
    Validate EMT licenses against the CA EMSA database
    :param license_number: State issued EMT license number
    """
    print("Entering function: validate_esma")
    
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
    return build_response(200, LAMBDA_SUCCESS_MESSAGE, str(license_status), str(exp_date))


def validate_aha(license_number):
    """
    Validate AHA BLS/CPR cert against the AHA database
    :param license_number: AHA BLS card number
    """
    print("Entering function: validate_aha")
    url = "https://ecards.heart.org/Student/MyeCards/VerifyECards"

    payload = 'codes={}'.format(license_number)
    headers = {
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'Request-Id': '|U0Hjw.ACgYH',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.105 Safari/537.36',
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
    return build_response(200, LAMBDA_SUCCESS_MESSAGE, str(license_status), str(renewal_date))


def validate_arc(license_number):
    """
    Validate BLS/CPR cert against the American Red Cross database
    :param license_number: AHA card number
    """
    print("Entering function: validate_arc")
    
    url = "https://www.redcross.org/on/demandware.store/Sites-RedCross-Site/default/Certificates-SearchCerts" \
          "?certnumber={}&format=ajax".format(license_number)

    payload = {}
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    soup_results_page = BeautifulSoup(response.text, "html.parser")

    print("\n-----------AMERICAN RED CROSS CERTIFICATION STATUS-----------\n")

    full_name = soup_results_page.select(".col-st-name")[1].text
    print("FULL NAME: " + str(full_name))

    cert_type = soup_results_page.select(".col-class")[1].text
    print("CERT TYPE: " + str(cert_type))

    completion_date = soup_results_page.select(".col-date")[1].text
    print("COMPLETION DATE: " + str(completion_date))

    cert_status = soup_results_page.select(".col-status")[1].text
    print("CERT STATUS: " + str(cert_status))

    print("\n-----------AMERICAN RED CROSS CERTIFICATION STATUS-----------\n")
    return build_response(200, LAMBDA_SUCCESS_MESSAGE, str(cert_status), "NA")


def validate_dca(license_number, last_name):
    """
    Validate medical license against the CA state DCA database
    :param license_number: State issued license number
    :param last_name: Last name as shown on provider license card
    """
    print("Entering function: validate_dca")
    
    url = "https://search.dca.ca.gov/results"

    license_number_formatted = license_number.replace(" ", "%20")

    payload = 'boardCode=0&busName=&firstName=&lastName={}&licenseNumber={}&licenseType=0&registryNumber='.format(
        last_name, license_number_formatted)
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://search.dca.ca.gov',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9 '
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    soup_results_page = BeautifulSoup(response.text, "html.parser")

    details_page_link = soup_results_page.select("#mD0")[0]["href"]

    details_page_response = requests.get("https://search.dca.ca.gov" + details_page_link)
    soup_details_page = BeautifulSoup(details_page_response.text, "html.parser")

    print("\n-----------CALIFORNIA DCA MEDICAL LICENSE STATUS-----------\n")

    full_name = soup_details_page.select("#name")[0].text
    full_name_formatted = full_name.replace("Name: ", "")
    print("FULL NAME: " + str(full_name_formatted.strip()))

    license_type = soup_details_page.select("#licType")[0].text
    license_type_formatted = license_type.replace("License Type: ", "")
    print("LICENSE TYPE: " + str(license_type_formatted.strip()))

    license_status = soup_details_page.select("#primaryStatus")[0].text
    license_status_formatted = license_status.replace("Primary Status: ", "")
    print("LICENSE STATUS: " + str(license_status_formatted.strip()))

    issue_date = soup_details_page.select("#issueDate")[0].text
    issue_date_formatted = issue_date.replace("Issuance Date: ", "")
    print("ISSUE DATE: " + str(issue_date_formatted.strip()))

    exp_date = soup_details_page.select("#expDate")[0].text
    exp_date_formatted = exp_date.replace("Expiration Date: ", "")
    print("EXP DATE: " + str(exp_date_formatted.strip()))

    print("\n-----------CALIFORNIA DCA MEDICAL LICENSE STATUS-----------\n")
    return build_response(200, LAMBDA_SUCCESS_MESSAGE, str(license_status), str(exp_date_formatted.strip()))
