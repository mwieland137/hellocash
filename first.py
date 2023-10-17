import requests

# Vario API
# https://app.swaggerhub.com/apis/variomm/VarioAPI/3

# baseUrl = "https://vario.uhrenschmuckonline.com/vario-api"
baseUrl = "https://api.hellocash.business/api/v1"
urlInvoices = "/invoices"
authToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2OTc1MzMwNjYuNDE1MTMsImNyaWQiOiIxNTI0MjgifQ.RZLb8n7BmvfEoXUy6GwR19Y40sSp2hxP_WtCG5SN_eU"



def main():
    print("Hey!")

    headers = {
        'Authorization' : 'Bearer ' + authToken,
        'Content-Type' : 'application/json'
    }

    response = requests.get(baseUrl + urlInvoices, headers=headers)
    print("invoices:")
    print(response.json())
    print("")
    invoices_array = response.json()['invoices']
    for invoice in invoices_array:
        print(f'invoice_id: {invoice["invoice_id"]}, timestamp: {invoice["invoice_timestamp"]}, number: {invoice["invoice_number"]}, total: {invoice["invoice_total"]}')
        response = requests.get(baseUrl + urlInvoices + "/" + invoice["invoice_id"], headers=headers)
        print(response.json())
        print("\n\n")

    


if __name__ == "__main__":
    main()
