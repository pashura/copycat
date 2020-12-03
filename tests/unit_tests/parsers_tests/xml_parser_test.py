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
        "name": "Invoice",
        "children": [
            {
                "name": "Header",
                "children": [
                    {
                        "name": "InvoiceHeader",
                        "children": [
                            {
                                "name": "TradingPartnerId",
                                "text": "009ACH1G1A1G1",
                                "length": 13,
                                "location": "/Invoice/Header/InvoiceHeader/TradingPartnerId",
                                "type": " 'str'"
                            },
                            {
                                "name": "InvoiceNumber",
                                "text": "4714370244",
                                "length": 10,
                                "location": "/Invoice/Header/InvoiceHeader/InvoiceNumber",
                                "type": " 'int'"
                            }
                        ]
                    }
                ]
            },
            {
                "name": "LineItem",
                "children": [
                    {
                        "name": "InvoiceLine",
                        "children": [
                            {
                                "name": "BuyerPartNumber",
                                "text": "081070041",
                                "length": 9,
                                "location": "/Invoice/LineItem/InvoiceLine/BuyerPartNumber",
                                "type": " 'int'"
                            },
                            {
                                "name": "VendorPartNumber",
                                "text": "85401-SL",
                                "length": 8,
                                "location": "/Invoice/LineItem/InvoiceLine/VendorPartNumber",
                                "type": " 'str'"
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Summary",
                "children": [
                    {
                        "name": "TotalAmount",
                        "text": "31.28",
                        "length": 5,
                        "location": "/Invoice/Summary/TotalAmount",
                        "type": " 'float'"
                    }
                ]
            }
        ]
    }
    result = XMLParser(io.StringIO(xml_data)).parse()
    assert result == expected_result
