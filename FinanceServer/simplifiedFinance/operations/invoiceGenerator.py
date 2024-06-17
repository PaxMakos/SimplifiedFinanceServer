from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import json
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import requests

FAKTUROWNIA_API_KEY = "Z1LHfTYCXBOGivincBrl"
FAKTUROWNIA_URL = "https://pakostasip.fakturownia.pl/"


def generateInvoice(invoiceData):
    config = json.loads(open("../config.json").read())

    positions = []

    for product in invoiceData["products"]:
        positions.append({
            "name": product["name"],
            "tax": product["VATRate"],
            "total_price_gross": product["totalGross"],
            "quantity": product["quantity"]
        })

    url = FAKTUROWNIA_URL + "invoices.json"

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        "api_token": FAKTUROWNIA_API_KEY,
        "invoice": {
            "kind": "vat",
            "number": invoiceData["invoiceNumber"],
            "sell_date": invoiceData["sellDate"],
            "issue_date": invoiceData["invoiceDate"],
            "payment_to": invoiceData["paymentTo"],
            "seller_name": config["organisation"],
            "seller_tax_no": config["NIP"],
            "seller_post_code": config["postCode"],
            "seller_city": config["city"],
            "seller_street": config["street"],
            "buyer_name": invoiceData["vendorName"],
            "buyer_tax_no": invoiceData["vendorNIP"],
            "buyer_post_code": invoiceData["vendorPostCode"],
            "buyer_city": invoiceData["vendorCity"],
            "buyer_street": invoiceData["vendorStreet"],
            "positions": positions
        }
    }

    response = requests.get(url, headers=headers, data=json.dumps(data))

    if not response.status_code == 200:
        raise Exception("Failed to generate invoice")

    url = FAKTUROWNIA_URL + "invoices/" + response.json()["id"] + ".pdf"

    response = requests.get(url)

    if not response.status_code == 200:
        raise Exception("Failed to download invoice")

    pdfFile = f"faktura_{invoiceData['invoiceNumber']}.pdf"

    with open(pdfFile, "wb") as file:
        file.write(response.content)

    return pdfFile


def generateInvoiceExperimental(invoiceData):
    invoiceNumber = invoiceData['invoiceNumber']

    pdfFile = f"faktura_{invoiceNumber}.pdf"
    document = SimpleDocTemplate(pdfFile, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)

    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleH = styles['Heading1']

    header = Paragraph("Faktura VAT 01/06/2024", styleH)

    config = json.loads(open("../config.json").read())

    sellerName = config["organisation"]
    sellerAddress = config["address"]
    sellerNIP = config["NIP"]

    sellerInfo = Paragraph(f"""
        <b>Sprzedawca</b><br/>
        {sellerName}<br/>
        NIP: {sellerNIP}<br/>
        {sellerAddress}
        """, styleN)

    vendor = invoiceData["vendorName"]
    vendorNIP = invoiceData["vendorNIP"]
    vendorAddress = invoiceData["vendorAddress"]

    buyerInfo = Paragraph(f"""
        <b>Nabywca</b><br/>
        {vendor}<br/>
        NIP: {vendorNIP}<br/>
        {vendorAddress}
        """, styleN)

    # Dane daty
    dates = Paragraph(f"""
        Data wystawienia: f{invoiceData["invoiceDate"]}<br/>
        Data sprzedaży: f{invoiceData["saleDate"]}<br/>
    """, styleN)

    products = invoiceData["products"]

    # Tabela z produktami/usługami
    data = [
        ["Lp.",
         "Nazwa towaru lub usługi",
         "Jm.",
         "Ilość",
         "Cena netto",
         "Wartość netto",
         "Stawka VAT",
         "Kwota VAT",
         "Wartość brutto"]
    ]

    taxes = {}

    for i, product in enumerate(products):
        data.append([
            i+1,
            product["name"],
            product["unit"],
            product["quantity"],
            product["netPrice"],
            int(product["quantity"]) * float(product["netPrice"]),
            product["VATRate"],
            float(product["VATRate"]) * int(product["quantity"]) * float(product["netPrice"]),
            float(product["netPrice"]) * int(product["quantity"]) + float(product["VATRate"]) * int(product["quantity"]) * float(product["netPrice"])
        ])

        if product["VATRate"] in taxes:
            taxes[product["VATRate"]] += int(product["quantity"]) * float(product["netPrice"])
        else:
            taxes[product["VATRate"]] = int(product["quantity"]) * float(product["netPrice"])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    taxesData = []

    for tax in taxes:
        taxesData.append([taxes[tax], tax, taxes[tax] * tax, taxes[tax] + taxes[tax] * tax])

    taxesData.append([invoiceData["totalNet"], "", invoiceData["totalVAT"], invoiceData["totalGross"]])

    summaryTable = Table(taxesData)
    summaryTable.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    paymentInfo = Paragraph(f"""
        Sposób płatności: {invoiceData["paymentMethod"]}<br/>
        Do zapłaty: {invoiceData["totalGross"]}<br/>
        Słownie: {invoiceData["totalGrossStr"]} PLN
    """, styleN)

    signatureInfo = Paragraph("""
        Podpis osoby upoważnionej do wystawienia
    """, styleN)

    elements = [header, sellerInfo, buyerInfo, dates, table, summaryTable, paymentInfo, signatureInfo]

    document.build(elements)

    print(f"Faktura została wygenerowana i zapisana jako {pdfFile}")

    return pdfFile


if __name__ == "__main__":
    invoiceData = {
        "invoiceNumber": "01_06_2024",
        "vendorName": "Vendor 1",
        "vendorNIP": "1234567890",
        "vendorAddress": "Vendor 1 address",
        "invoiceDate": "01/06/2024",
        "saleDate": "01/06/2024",
        "products": [
            {
                "name": "Product 1",
                "unit": "szt.",
                "quantity": 10,
                "netPrice": 10,
                "VATRate": 0.23
            },
            {
                "name": "Product 2",
                "unit": "szt.",
                "quantity": 5,
                "netPrice": 20,
                "VATRate": 0.08
            }
        ],
        "totalNet": 150,
        "totalVAT": 30,
        "totalGross": 180,
        "paymentMethod": "Przelew",
        "totalGrossStr": "sto osiemdziesiąt"
    }
    generateInvoiceExperimental(invoiceData)