import io

from copy_cat.parsers.xml_parser import XMLParser


def test_parse_returns_json_object():
    xml_data = """
        <Invoice>
            <Header>
                <InvoiceHeader>
                    <TradingPartnerId>009ACH1G1A1G1</TradingPartnerId>
                    <InvoiceNumber>4714370244</InvoiceNumber>
                </InvoiceHeader>
            </Header>
            <LineItem>
                <InvoiceLine>
                    <BuyerPartNumber>081070041</BuyerPartNumber>
                    <VendorPartNumber>85401-SL</VendorPartNumber>
                </InvoiceLine>
                </LineItem>
            <Summary>
                <TotalAmount>31.28</TotalAmount>
            </Summary>
        </Invoice>
    """
    expected_result = {
        "children": [
            {
                "children": [
                    {
                        "children": [
                            {
                                "length": 13,
                                "location": "/Invoice/Header/InvoiceHeader/TradingPartnerId",
                                "name": "TradingPartnerId",
                                "text": "009ACH1G1A1G1",
                                "type": "str",
                            },
                            {
                                "length": 10,
                                "location": "/Invoice/Header/InvoiceHeader/InvoiceNumber",
                                "name": "InvoiceNumber",
                                "text": "4714370244",
                                "type": "int",
                            },
                        ],
                        "location": "/Invoice/Header/InvoiceHeader",
                        "name": "InvoiceHeader",
                    }
                ],
                "location": "/Invoice/Header",
                "name": "Header",
            },
            {
                "children": [
                    {
                        "children": [
                            {
                                "length": 9,
                                "location": "/Invoice/LineItem/InvoiceLine/BuyerPartNumber",
                                "name": "BuyerPartNumber",
                                "text": "081070041",
                                "type": "int",
                            },
                            {
                                "length": 8,
                                "location": "/Invoice/LineItem/InvoiceLine/VendorPartNumber",
                                "name": "VendorPartNumber",
                                "text": "85401-SL",
                                "type": "str",
                            },
                        ],
                        "location": "/Invoice/LineItem/InvoiceLine",
                        "name": "InvoiceLine",
                    }
                ],
                "location": "/Invoice/LineItem",
                "name": "LineItem",
            },
            {
                "children": [
                    {
                        "length": 5,
                        "location": "/Invoice/Summary/TotalAmount",
                        "name": "TotalAmount",
                        "text": "31.28",
                        "type": "float",
                    }
                ],
                "location": "/Invoice/Summary",
                "name": "Summary",
            },
        ],
        "location": "/Invoice",
        "name": "Invoice",
    }
    result = XMLParser().parse(xml_data)
    assert result == expected_result
