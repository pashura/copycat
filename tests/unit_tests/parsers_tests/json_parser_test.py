from copy_cat.parsers.json_parser import JSONParser


def test_parse_returns_flatten_object():
    json_obj = {
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
                                "text": "009ACH1G1A1G1"
                            }
                        ]
                    },
                    {
                        "name": "Dates",
                        "children": [
                            {
                                "name": "DateTimeQualifier",
                                "text": "024"
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
                                "text": "081070041"
                            }
                        ]
                    },
                ]
            },
            {
                "name": "Summary",
                "children": [
                    {
                        "name": "TotalAmount",
                        "text": "31.28"
                    }
                ]
            }
        ]
    }
    expected_result = [
        {
            "name": "TradingPartnerId",
            "text": "009ACH1G1A1G1"
        },
        {
            "name": "DateTimeQualifier",
            "text": "024"
        },
        {
            "name": "BuyerPartNumber",
            "text": "081070041"
        },
        {
            "name": "TotalAmount",
            "text": "31.28"
        }
    ]
    result = JSONParser(json_obj).parse()
    assert result == expected_result
