import requests

baseUrl = "https://api.hellocash.business/api/v1"
urlArticles = "/articles"
authToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2OTc1MzMwNjYuNDE1MTMsImNyaWQiOiIxNTI0MjgifQ.RZLb8n7BmvfEoXUy6GwR19Y40sSp2hxP_WtCG5SN_eU"

def write_article_test():

    headers = {
        "Authorization" : "Bearer " + authToken,
        "Content-Type" : "application/json"
    }

    article = {
        "article_id" : 13693074,
        "article_category_id": 548514,
        "article_name" : "Seiko Uhr SRPD51K1",
        "article_code" : "SRPD51K1-023",
        "article_eanCode" : "4954628232106",
        "article_taxRate" : 19.0,
        "article_net_purchasePrice" : 150.76,
        "article_net_sellingPrice" : 260.504,
        "article_gross_sellingPrice" : 310.0,
        "article_stock" : 13,
        "article_comment" : "SEIKO 5 SPORTS SS HD"
    }

    print("-------------- uploading -----------------")
    print(article)
    response = requests.post(baseUrl + urlArticles, json=article, headers=headers)
    print("----------uploaded - response     --------")
    print(response)
    print(response.json())


if __name__ == "__main__":
    write_article_test()
