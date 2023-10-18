import requests
import csv

baseUrl = "https://api.hellocash.business/api/v1"
urlArticles = "/articles"
authToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2OTc1MzMwNjYuNDE1MTMsImNyaWQiOiIxNTI0MjgifQ.RZLb8n7BmvfEoXUy6GwR19Y40sSp2hxP_WtCG5SN_eU"



def main():
    print("Hey!")

    headers = {
        'Authorization' : 'Bearer ' + authToken,
        'Content-Type' : 'application/json'
    }

    parameters = {
        'limit' : 2,
        'offset' : 1
    }

    response = requests.get(baseUrl + urlArticles, params=parameters, headers=headers)
    print("articles:")
    # print(response.json())

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
    


if __name__ == "__main__":
    main()
