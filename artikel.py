import requests
import csv
import time

baseUrl = "https://api.hellocash.business/api/v1"
urlArticles = "/articles"
auth_test_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2OTc1MzMwNjYuNDE1MTMsImNyaWQiOiIxNTI0MjgifQ.RZLb8n7BmvfEoXUy6GwR19Y40sSp2hxP_WtCG5SN_eU"
auth_live_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2OTc4ODUyNzYuODc3MTA5LCJjcmlkIjoiMTUyNDIwIn0.BdXKBbMqlJhZqOE2PLzEkYntbTd1DPL2MGVMUWRhf6I"
auth_token = auth_live_token

def read_articles():
    print("Hey!")

    headers = {
        'Authorization' : 'Bearer ' + auth_token,
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
        'Authorization' : 'Bearer ' + auth_token,
        'Content-Type' : 'application/json'
    }

    # holt in Abschnitten von 900 Datensätzen die Artikel von hellocash ab und speichert sie im Array 'rows'
    # Schleife bricht ab, wenn keine Artikel mehr zu holen sind (oder ein Fehler auftritt)
    offset = 1
    limit = 900
    total = 0
    header_line = False # beim ersten Abruf der Artikel werden einmalig die keys als Überschrift für die resultierende csv-Datei ausgelesen
    rows = []
    while True:
        parameters = {
            'limit' : limit,
            'offset' : offset
        }

        response = requests.get(baseUrl + urlArticles, params=parameters, headers=headers)
    
        if len(response.json()['articles']) == 0:
            print("keine Artikel (mehr) vorhanden!")
            break
        
        i = 0
        
        for article in response.json()['articles']:
            if header_line == False:
                fields = list(article.keys())
                header_line = True
            
            my_list = list(article.values())
            new_list = [x if not isinstance(x, str) else x.encode('ascii', 'ignore').decode('ascii') for x in my_list]
            rows.append(new_list)
            i = i + 1

        offset = offset + 1

        total = total + i
        print(f"{i} Datensäte gelesen, damit total {total}")


    with open('all_eggs2.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(fields)
        spamwriter.writerows(rows) 

def write_articles():
    print("Hej!")

    with open('eggs_test.csv', newline='') as csvfile:
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
        'Authorization' : 'Bearer ' + auth_token,
        'Content-Type' : 'application/json'
    }

    i = 0
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
        i = i + 1
        print(f'das war der {i}-te Artikel')
        time.sleep(1)

    


if __name__ == "__main__":
    # read_all_articles()
    write_articles()
