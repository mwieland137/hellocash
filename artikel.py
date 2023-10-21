import requests
import csv

baseUrl = "https://api.hellocash.business/api/v1"
urlArticles = "/articles"
authToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2OTc1MzMwNjYuNDE1MTMsImNyaWQiOiIxNTI0MjgifQ.RZLb8n7BmvfEoXUy6GwR19Y40sSp2hxP_WtCG5SN_eU"



def read_articles():
    print("Hey!")

    headers = {
        'Authorization' : 'Bearer ' + authToken,
        'Content-Type' : 'application/json'
    }

    parameters = {
        'limit' : 2,
        'offset' : 200
    }

    response = requests.get(baseUrl + urlArticles, params=parameters, headers=headers)
   
    if len(response.json()['articles']) == 0:
        print("keine Artikel (mehr) vorhanden!")
        return
    
    rows = []
    header_line = False
    for article in response.json()['articles']:
        if header_line == False:
            fields = list(article.keys())
            header_line = True
        
        my_list = list(article.values())
        rows.append(my_list)


    with open('eggs.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(fields)
        spamwriter.writerows(rows)


    print(fields)
    print(rows)   

def read_all_articles():
    print("Hey!")

    headers = {
        'Authorization' : 'Bearer ' + authToken,
        'Content-Type' : 'application/json'
    }

    parameters = {
        'limit' : 2,
        'offset' : 200
    }

    response = requests.get(baseUrl + urlArticles, params=parameters, headers=headers)
   
    if len(response.json()['articles']) == 0:
        print("keine Artikel (mehr) vorhanden!")
        return
    
    rows = []
    header_line = False
    for article in response.json()['articles']:
        if header_line == False:
            fields = list(article.keys())
            header_line = True
        
        my_list = list(article.values())
        rows.append(my_list)


    with open('eggs.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(fields)
        spamwriter.writerows(rows)


    print(fields)
    print(rows)    
    



def write_articles():
    print("Hej!")

    with open('eggs.csv', newline='') as csvfile:
        header_read = False
        res = []
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in spamreader:
            if not header_read:
                # header_dict = dict(enumerate(row))
                header_row = row
                header_read = True
            else:
                res.append(dict(zip(header_row, row)))


    headers = {
        'Authorization' : 'Bearer ' + authToken,
        'Content-Type' : 'application/json'
    }

    for article in res:
        
        # article.pop('article_id')

        '''
        article['article_id'] =  int(article['article_id'])
        article['article_category_id'] = int(article['article_category_id'])
        article['article_name'] = article['article_name']
        article['article_code'] = article['article_code']
        article['article_eanCode'] = article['article_eanCode']
        article['article_taxRate'] = float(article['article_taxRate'])
        article['article_unit'] = article['article_unit']
        article['article_net_purchacePrice'] = float(article['article_net_purchacePrice'])
        article['article_net_purchasePrice'] = float(article['article_net_purchasePrice'])
        article['article_net_sellingPrice'] = float(article['article_net_sellingPrice'])
        article['article_gross_sellingPrice'] = float(article['article_gross_sellingPrice'])
        article['article_stock'] = int(article['article_stock'])
        article['article_minStock'] = article['article_minStock']
        article['article_comment'] = article['article_comment']
        article['article_billReference'] = bool(article['article_billReference'])
        article['article_color'] = article['article_color']
        article.pop('article_color')
        article.pop('article_billReference')
        '''
        print("-------------- loading up -----------------")
        print(article)
        response = requests.post(baseUrl + urlArticles, json=article, headers=headers)
        print("---------------uploaded--------------------")
        print(response.json())
    


if __name__ == "__main__":
    # read_articles()
    write_article_test()
