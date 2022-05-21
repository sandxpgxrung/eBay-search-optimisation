from ebaysdk.finding import Connection
from bs4 import BeautifulSoup


def search_items(keyword):
    api = Connection(appid='sandipgu-sandbox-PRD-7d4b2781a-07305143', config_file=None)
    api_request = {'keywords': keyword, 'outputSelector': 'SellerInfo'}
    response = api.execute('findItemsByKeywords', api_request)
    soup = BeautifulSoup(response.content, 'lxml')

    items = soup.find_all('item')
    return items


if __name__ == '__main__':
    keyword_test = input('Enter your Keyword/s (ex: white piano):\n')
    items_test = search_items(keyword_test)
