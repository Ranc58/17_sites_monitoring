from datetime import datetime, timedelta
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
        w = whois.whois(url)
        expiration_date = w.expiration_date
        exp_date = {'exp_date': expiration_date}
        urls_expiration_date_list.append(exp_date)
    return urls_expiration_date_list


def get_full_info_list(response_list, exp_date_list):
    full_info_list = [dict(x, **y)
                      for x, y in zip(response_list, exp_date_list)]
    return full_info_list


def output_urls_info(full_info_list):
    for list in full_info_list:
        date_diff = list['exp_date'] - datetime.today()
        months_diff = int(int(date_diff.days) / 30)
        print("\nUrl: {}\n"
              "Server response: {}\n"
              "To end of domen expiration: {} months"
              .format(list['url'], list['response'], months_diff))


if __name__ == '__main__':
    filepath = 'sites.txt'
    with open(filepath) as urls:
        url_list = create_url_list(urls)
    response_list = get_server_response(url_list)
    exp_date_list = get_domain_expiration_date(url_list)
    full_info_list = get_full_info_list(response_list, exp_date_list)
    output_urls_info(full_info_list)
