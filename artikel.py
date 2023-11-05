import requests
import csv
import time
from datetime import date
import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger()

baseUrl = "https://api.hellocash.business/api/v1"
urlArticles = "/articles"
urlInvoices = "/invoices"
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
        'offset' : 100
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

    with open('eggs_back.csv', newline='', encoding="utf8") as csvfile:
        header_read = False
        res = []
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in spamreader:
            if not header_read:
                # hellocash isue: response field names are different from request field names
                for i in range(len(row)):
                    if row[i] == 'article_eanCode':
                        row[i] = 'article_ean_code'
                    elif row[i] == 'article_taxRate':
                        row[i] = 'article_tax_rate'
                    elif row[i] == 'article_net_purchasePrice':
                        row[i] = 'article_net_purchase_price'
                    elif row[i] == 'article_net_sellingPrice':
                        row[i] = 'article_net_selling_price'
                    elif row[i] == 'article_gross_sellingPrice':
                        row[i] = 'article_gross_selling_price'
                    elif row[i] == 'article_minStock':
                        row[i] = 'article_min_stock'
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

def read_invoices(datum_von: str, datum_bis: str):
    if not check_date(datum_von) or not check_date(datum_bis):
        logger.error("Datumsfehler")
        if not check_date(datum_von):
            logger.error(f'datum_von: {datum_von}')
        if not check_date(datum_bis):
            logger.error(f'datum_von: {datum_bis}')
        return

    datum_von = datum_von + " 00:00:00"
    datum_bis = datum_bis + " 23:59:59"

    headers = {
        'Authorization' : 'Bearer ' + auth_token,
        'Content-Type' : 'application/json'
    }

    parameters = {
        'dateFrom' : datum_von,
        'dateTo' : datum_bis
    }

    # getting a list of invoices
    response = requests.get(baseUrl + urlInvoices, params=parameters, headers=headers)
   
    if len(response.json()['invoices']) == 0:
        print("keine Rechnungen vorhanden!")
        return
    
    rows = []
    fields = ['MENGE', 'ARTIKELNUMMER', 'Einzelpreis', 'Artikelname', 'Datum', 'invoice_mode', 'invoice_cancellation'] #[Datum', 'article_code', 'article_name', 'Anzahl', 'Gesamtpreis', 'Einzelpreis', 'Einzelnachlass']
    total = 0
    for invoice in response.json()['invoices']:
        logger.debug(f'invoice_number: {invoice["invoice_number"]}, total: {invoice["invoice_total"]}, timestamp: {invoice["invoice_timestamp"]}, cancellation: {invoice["invoice_cancellation"]}')
        if invoice['invoice_cancellation'] == '1':
            continue
        total = float(invoice['invoice_total']) + total
        # getting a specific inovoice
        response = requests.get(baseUrl + urlInvoices + "/" + invoice['invoice_id'], headers=headers)
        article_rows = []
        for article in response.json()['items']:
            logger.debug(f"Artikel: {article['item_name']}, {int(float(article['item_quantity']))} Stück, gesamt: {article['item_total']}, Einzelpreis: {article['item_price']}, discount: {article['item_discount']}")
            if int(article['item_article_id']) != 0:
                response = requests.get(baseUrl + urlArticles + "/" + article['item_article_id'], headers=headers)
                article_info = response.json()
                logger.debug(f"article_code: {article_info['article_code']}")
                article_code = article_info['article_code']
            else:
                logger.debug(f"article_code: kein Artikel hinterlegt")
                article_code = 'kein Artikel hinterlegt'

            menge = int(float(article['item_quantity']))
            artikelnummer = article_code
            if artikelnummer == 'kein Artikel hinterlegt':
                artikelnummer = 'DIVERSE'
            addressnummer = 176390
            einzelpreis = float(article['item_total']) / menge
            bestellnr = invoice['invoice_timestamp'][0:11]

            article_rows.append([menge,
                         artikelnummer,
                         str(einzelpreis).replace('.', ','),
                         article['item_name'],
                         invoice['invoice_timestamp'][0:11],
                         invoice['invoice_mode'],
                         invoice['invoice_cancellation']
            ])
        if invoice.get('invoice_discount') is not None:
            invoice_articles_total = 0
            for article_row in article_rows:
                invoice_articles_total = invoice_articles_total + (float(str(article_row[2]).replace(',', '.')) * article_row[0])
            invoice_discount = float(invoice['invoice_discount'])
            for i in range(len(article_rows)):
                article_row = article_rows[i]
                einzelpreis = float(str(article_row[2]).replace(',', '.'))
                invoice_discount_anteil = invoice_discount * einzelpreis / invoice_articles_total
                einzelpreis = einzelpreis + invoice_discount_anteil # invoice_discount ist negativ, daher das +
                article_row[2]=str(einzelpreis).replace('.', ',')
                article_rows[i] = article_row

        rows = rows + article_rows


    logger.info("Total: " + str(total))
    

    with open('invoices.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(fields)
        spamwriter.writerows(rows)
    




def check_date(datum: str) -> bool:
    if len(datum) != 10:
        return False
    
    if datum[4] != "-" or datum[7] != "-":
        return False
    
    year = int(datum[0:4])
    month = int(datum[5:7])
    day = int(datum[8:10])

    try:
        this_date = date(year, month, day)
    except:
        return False
    
    return True

    

    


if __name__ == "__main__":
    # read_articles()
    # read_all_articles()
    write_articles()
    # print(check_date('2023-09-31'))
    # read_invoices('2023-11-03', '2023-11-03')
