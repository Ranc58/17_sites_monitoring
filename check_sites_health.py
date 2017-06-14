from datetime import datetime
import argparse
import requests
import whois


def create_url_list(urls):
    url_list = [url.strip() for url in urls]
    return url_list


def get_server_response(url):
    response = requests.get(url).status_code
    url_response = {'url': url,
                    'response': response}
    return url_response


def get_domain_expiration_date(url):
    domain = whois.whois(url)
    expiration_date = domain.expiration_date[0]
    exp_date = {'exp_date': expiration_date}
    return exp_date


def get_output_urls_info(response_list, exp_date):
    date_diff = exp_date['exp_date'] - datetime.today()
    months_diff = date_diff.days // 30
    site = {'url': response_list['url'],
            'response_code': response_list['response'],
            'expiration': months_diff}
    return site


def create_parser_for_user_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True,
                        help='path to file with list of URLs',
                        type=argparse.FileType())
    namespace = parser.parse_args()
    return namespace


if __name__ == '__main__':
    namespace = create_parser_for_user_arguments()
    filepath = namespace.file.readlines()
    url_list = create_url_list(filepath)
    for url in url_list:
        try:
            response_list = get_server_response(url)
        except (requests.exceptions.ConnectionError):
            print('\nError!\nPlease check that URL for correctness: {}'
                  .format(url))
        else:
            exp_date_list = get_domain_expiration_date(url)
            output_info_list = get_output_urls_info(response_list,
                                                    exp_date_list)
            print("\nUrl: {url}\n"
                  "Server response: {response_code}\n"
                  "To end of domen expiration: {expiration} months"
                  .format(**output_info_list))
