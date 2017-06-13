from datetime import datetime
import argparse
import requests
import whois


def create_url_list(urls):
    url_list = [url.strip() for url in urls]
    return url_list


def get_server_response(url_list):
    urls_response_list = []
    for url in url_list:
        response = requests.get(url).status_code
        url_response = {'url': url,
                        'response': response}
        urls_response_list.append(url_response)
    return urls_response_list


def get_domain_expiration_date(url_list):
    urls_expiration_date_list = []
    for url in url_list:
        domain = whois.whois(url)
        expiration_date = domain.expiration_date[0]
        exp_date = {'exp_date': expiration_date}
        urls_expiration_date_list.append(exp_date)
    return urls_expiration_date_list


def get_full_info_list(response_list, exp_date_list):
    full_info_list = [dict(x, **y)
                      for x, y in zip(response_list, exp_date_list)]
    return full_info_list


def get_output_urls_info(full_info_list):
    output_info_list = []
    for url in full_info_list:
        date_diff = url['exp_date'] - datetime.today()
        months_diff = date_diff.days // 30
        site = {'url': url['url'],
                'response_code': url['response'],
                'expiration': months_diff}
        output_info_list.append(site)
    return output_info_list


def print_urls_info(output_info_list):
    for url in output_info_list:
        print("\nUrl: {url}\n"
              "Server response: {response_code}\n"
              "To end of domen expiration: {expiration} months"
              .format(**url))


def create_parser_for_user_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='path to file with list of URLs', type=str)
    return parser.parse_args()


if __name__ == '__main__':
    namespace = create_parser_for_user_arguments()
    filepath = namespace.file
    try:
        with open(filepath) as urls:
            url_list = create_url_list(urls)
        response_list = get_server_response(url_list)
    except (FileNotFoundError, requests.exceptions.ConnectionError) as error:
        print(error)
    else:
        exp_date_list = get_domain_expiration_date(url_list)
        full_info_list = get_full_info_list(response_list, exp_date_list)
        output_info_list = get_output_urls_info(full_info_list)
        print_urls_info(output_info_list)
