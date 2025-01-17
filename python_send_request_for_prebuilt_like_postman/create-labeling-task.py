import requests
import json

# Define the API URL
url = "https://vdi-prebuilt-dte.azurewebsites.net/api/create_onedoc_task"  # Replace with the actual API endpoint

# Define the payload
payload = {
    "programId": "ac6ef143-30a3-4b9f-9e70-7e96f67caee3",
    "createConfigs": [
        {
            "batchName": "batchName1357",
            "sources": {
                "display": {
                    "containerUri": "https://vdiprebuiltdte.blob.core.windows.net/prebuilt-lab-data/",
                    "directoryPath": "91152bac-46ea-47c5-8276-ff7a08c87e10/document/"
                },
                "data": {
                    "containerUri": "https://vdiprebuiltdte.blob.core.windows.net/prebuilt-lab-data/",
                    "directoryPath": "91152bac-46ea-47c5-8276-ff7a08c87e10/ocr_renamed/"
                }
            },
            "granularity": 60,
            "converterName": "OcrResultV3",
            "taskGroupInfo": {
                "taskGroupName": "taskGroupName",
                "boundingBoxInfo": {
                    "originLocation": "",
                    "pointStructure": ""
                },
                "modules": [
                    "ImageMap",
                    "TaskPanel"
                ],
                "tasks": [
                    {
                        "taskType": "choice",
                        "taskConfig": {
                            "fieldName": "InvalidDocument",
                            "type": "Single",
                            "title": "Choice group 1: Invalid document",
                            "defaultValue": "Valid",
                            "options": [
                                {
                                    "key": "Valid",
                                    "text": "Valid"
                                },
                                {
                                    "key": "Invalid",
                                    "text": "Invalid"
                                },
                                {
                                    "key": "Mixed",
                                    "text": "Mixed Documents"
                                }
                            ],
                            "dependencies": []
                        }
                    },
                    {
                        "taskType": "choice",
                        "taskConfig": {
                            "fieldName": "ImageQuality",
                            "type": "Single",
                            "title": "Choice group 2: Image quality",
                            "defaultValue": "Good",
                            "options": [
                                {
                                    "key": "Good",
                                    "text": "Good Quality"
                                },
                                {
                                    "key": "Bad",
                                    "text": "Bad Quality"
                                }
                            ],
                            "dependencies": [
                                {
                                    "fieldName": "InvalidDocument",
                                    "targetValue": [
                                        "Valid"
                                    ]
                                }
                            ]
                        }
                    },
                    {
                        "taskType": "choice",
                        "taskConfig": {
                            "fieldName": "DocumentPage",
                            "type": "Single",
                            "title": "Choice group 3: Document page",
                            "defaultValue": "SinglePage",
                            "options": [
                                {
                                    "key": "SinglePage",
                                    "text": "Single Page"
                                },
                                {
                                    "key": "MultiplePages",
                                    "text": "Multiple Pages"
                                }
                            ],
                            "dependencies": [
                                {
                                    "fieldName": "InvalidDocument",
                                    "targetValue": [
                                        "Valid"
                                    ]
                                },
                                {
                                    "fieldName": "ImageQuality",
                                    "targetValue": [
                                        "Good"
                                    ]
                                }
                            ]
                        }
                    },
                    {
                        "taskType": "choice",
                        "taskConfig": {
                            "fieldName": "DocumentCount",
                            "type": "Single",
                            "title": "Choice group 4: Document count",
                            "defaultValue": "SingleSet",
                            "options": [
                                {
                                    "key": "SingleSet",
                                    "text": "Single Set"
                                },
                                {
                                    "key": "MultipleSet",
                                    "text": "Multiple Set"
                                }
                            ],
                            "dependencies": [
                                {
                                    "fieldName": "InvalidDocument",
                                    "targetValue": [
                                        "Valid"
                                    ]
                                },
                                {
                                    "fieldName": "ImageQuality",
                                    "targetValue": [
                                        "Good"
                                    ]
                                },
                                {
                                    "fieldName": "DocumentPage",
                                    "targetValue": [
                                        "MultiplePages"
                                    ]
                                }
                            ]
                        }
                    },
                    {
                        "taskType": "choice",
                        "taskConfig": {
                            "fieldName": "MultipleDocumentsInAPage",
                            "type": "Single",
                            "title": "Choice group 5: Multiple documents in a page",
                            "defaultValue": "SingleInPage",
                            "options": [
                                {
                                    "key": "SingleInPage",
                                    "text": "Single in Page"
                                },
                                {
                                    "key": "FrontAndBackInPage",
                                    "text": "Front and Back in Page"
                                },
                                {
                                    "key": "MultipleInPage",
                                    "text": "Multiple in Page"
                                }
                            ],
                            "dependencies": [
                                {
                                    "fieldName": "InvalidDocument",
                                    "targetValue": [
                                        "Valid"
                                    ]
                                },
                                {
                                    "fieldName": "ImageQuality",
                                    "targetValue": [
                                        "Good"
                                    ]
                                },
                                {
                                    "fieldName": "DocumentPage",
                                    "targetValue": [
                                        "SinglePage"
                                    ]
                                }
                            ]
                        }
                    },
                    {
                        "taskType": "choice",
                        "taskConfig": {
                            "fieldName": "FrontOrBack",
                            "type": "Single",
                            "title": "Choice group 6: Front or back",
                            "defaultValue": "Front",
                            "options": [
                                {
                                    "key": "Front",
                                    "text": "Front"
                                },
                                {
                                    "key": "Back",
                                    "text": "Back"
                                }
                            ],
                            "dependencies": [
                                {
                                    "fieldName": "InvalidDocument",
                                    "targetValue": [
                                        "Valid"
                                    ]
                                },
                                {
                                    "fieldName": "ImageQuality",
                                    "targetValue": [
                                        "Good"
                                    ]
                                },
                                {
                                    "fieldName": "DocumentPage",
                                    "targetValue": [
                                        "SinglePage"
                                    ]
                                },
                                {
                                    "fieldName": "MultipleDocumentsInAPage",
                                    "targetValue": [
                                        "SingleInPage"
                                    ]
                                }
                            ]
                        }
                    },
                    {
                        "taskType": "choice",
                        "taskConfig": {
                            "fieldName": "BackgroundText",
                            "type": "Single",
                            "title": "Choice group 7: Background text",
                            "defaultValue": "CleanBackground",
                            "options": [
                                {
                                    "key": "CleanBackground",
                                    "text": "Clean Background"
                                },
                                {
                                    "key": "TextsInBackground",
                                    "text": "Texts in Background"
                                }
                            ],
                            "dependencies": [
                                {
                                    "fieldName": "InvalidDocument",
                                    "targetValue": [
                                        "Valid"
                                    ]
                                },
                                {
                                    "fieldName": "ImageQuality",
                                    "targetValue": [
                                        "Good"
                                    ]
                                }
                            ]
                        }
                    },
                    {
                        "taskType": "choice",
                        "taskConfig": {
                            "fieldName": "ImageOrientation",
                            "type": "Single",
                            "title": "Choice group 8: Image orientation",
                            "defaultValue": "Unrotated",
                            "options": [
                                {
                                    "key": "Unrotated",
                                    "text": "Unrotated"
                                },
                                {
                                    "key": "Rotated",
                                    "text": "Rotated"
                                }
                            ],
                            "dependencies": [
                                {
                                    "fieldName": "InvalidDocument",
                                    "targetValue": [
                                        "Valid"
                                    ]
                                },
                                {
                                    "fieldName": "ImageQuality",
                                    "targetValue": [
                                        "Good"
                                    ]
                                }
                            ]
                        }
                    },
                    {
                        "taskType": "choice",
                        "taskConfig": {
                            "fieldName": "CoveredCroppedRedacted",
                            "type": "Single",
                            "title": "Choice group 9: Covered/Cropped/Redacted",
                            "defaultValue": "Clean",
                            "options": [
                                {
                                    "key": "Clean",
                                    "text": "Clean"
                                },
                                {
                                    "key": "CoveredCropped",
                                    "text": "Covered/Cropped"
                                },
                                {
                                    "key": "Redacted",
                                    "text": "Redacted"
                                }
                            ],
                            "dependencies": [
                                {
                                    "fieldName": "InvalidDocument",
                                    "targetValue": [
                                        "Valid"
                                    ]
                                },
                                {
                                    "fieldName": "ImageQuality",
                                    "targetValue": [
                                        "Good"
                                    ]
                                }
                            ]
                        }
                    },
                    {
                        "taskType": "choice",
                        "taskConfig": {
                            "fieldName": "Watermark",
                            "type": "Single",
                            "title": "Choice group 10: Watermark/Stamp/Graffiti/Additional Description/Visual Back",
                            "defaultValue": "DoesNotAffectFieldRecognition",
                            "options": [
                                {
                                    "key": "DoesNotAffectFieldRecognition",
                                    "text": "Does not affect field recognition"
                                },
                                {
                                    "key": "AffectsFieldRecognition",
                                    "text": "Affects field recognition"
                                }
                            ],
                            "dependencies": [
                                {
                                    "fieldName": "InvalidDocument",
                                    "targetValue": [
                                        "Valid"
                                    ]
                                },
                                {
                                    "fieldName": "ImageQuality",
                                    "targetValue": [
                                        "Good"
                                    ]
                                }
                            ]
                        }
                    },
                    {
                        "taskType": "dropdown",
                        "taskConfig": {
                            "fieldName": "Locale",
                            "type": "Single",
                            "title": "Choice group 11: Locale",
                            "options": [
                                {
                                    "key": "AD",
                                    "text": "AD"
                                },
                                {
                                    "key": "AE",
                                    "text": "AE"
                                },
                                {
                                    "key": "AF",
                                    "text": "AF"
                                },
                                {
                                    "key": "AG",
                                    "text": "AG"
                                },
                                {
                                    "key": "AI",
                                    "text": "AI"
                                },
                                {
                                    "key": "AL",
                                    "text": "AL"
                                },
                                {
                                    "key": "AM",
                                    "text": "AM"
                                },
                                {
                                    "key": "AO",
                                    "text": "AO"
                                },
                                {
                                    "key": "AQ",
                                    "text": "AQ"
                                },
                                {
                                    "key": "AR",
                                    "text": "AR"
                                },
                                {
                                    "key": "AS",
                                    "text": "AS"
                                },
                                {
                                    "key": "AT",
                                    "text": "AT"
                                },
                                {
                                    "key": "AU",
                                    "text": "AU"
                                },
                                {
                                    "key": "AW",
                                    "text": "AW"
                                },
                                {
                                    "key": "AX",
                                    "text": "AX"
                                },
                                {
                                    "key": "AZ",
                                    "text": "AZ"
                                },
                                {
                                    "key": "BA",
                                    "text": "BA"
                                },
                                {
                                    "key": "BB",
                                    "text": "BB"
                                },
                                {
                                    "key": "BD",
                                    "text": "BD"
                                },
                                {
                                    "key": "BE",
                                    "text": "BE"
                                },
                                {
                                    "key": "BF",
                                    "text": "BF"
                                },
                                {
                                    "key": "BG",
                                    "text": "BG"
                                },
                                {
                                    "key": "BH",
                                    "text": "BH"
                                },
                                {
                                    "key": "BI",
                                    "text": "BI"
                                },
                                {
                                    "key": "BJ",
                                    "text": "BJ"
                                },
                                {
                                    "key": "BL",
                                    "text": "BL"
                                },
                                {
                                    "key": "BM",
                                    "text": "BM"
                                },
                                {
                                    "key": "BN",
                                    "text": "BN"
                                },
                                {
                                    "key": "BO",
                                    "text": "BO"
                                },
                                {
                                    "key": "BQ",
                                    "text": "BQ"
                                },
                                {
                                    "key": "BR",
                                    "text": "BR"
                                },
                                {
                                    "key": "BS",
                                    "text": "BS"
                                },
                                {
                                    "key": "BT",
                                    "text": "BT"
                                },
                                {
                                    "key": "BV",
                                    "text": "BV"
                                },
                                {
                                    "key": "BW",
                                    "text": "BW"
                                },
                                {
                                    "key": "BY",
                                    "text": "BY"
                                },
                                {
                                    "key": "BZ",
                                    "text": "BZ"
                                },
                                {
                                    "key": "CA",
                                    "text": "CA"
                                },
                                {
                                    "key": "CC",
                                    "text": "CC"
                                },
                                {
                                    "key": "CD",
                                    "text": "CD"
                                },
                                {
                                    "key": "CF",
                                    "text": "CF"
                                },
                                {
                                    "key": "CG",
                                    "text": "CG"
                                },
                                {
                                    "key": "CH",
                                    "text": "CH"
                                },
                                {
                                    "key": "CI",
                                    "text": "CI"
                                },
                                {
                                    "key": "CK",
                                    "text": "CK"
                                },
                                {
                                    "key": "CL",
                                    "text": "CL"
                                },
                                {
                                    "key": "CM",
                                    "text": "CM"
                                },
                                {
                                    "key": "CN",
                                    "text": "CN"
                                },
                                {
                                    "key": "CO",
                                    "text": "CO"
                                },
                                {
                                    "key": "CR",
                                    "text": "CR"
                                },
                                {
                                    "key": "CU",
                                    "text": "CU"
                                },
                                {
                                    "key": "CV",
                                    "text": "CV"
                                },
                                {
                                    "key": "CW",
                                    "text": "CW"
                                },
                                {
                                    "key": "CX",
                                    "text": "CX"
                                },
                                {
                                    "key": "CY",
                                    "text": "CY"
                                },
                                {
                                    "key": "CZ",
                                    "text": "CZ"
                                },
                                {
                                    "key": "DE",
                                    "text": "DE"
                                },
                                {
                                    "key": "DJ",
                                    "text": "DJ"
                                },
                                {
                                    "key": "DK",
                                    "text": "DK"
                                },
                                {
                                    "key": "DM",
                                    "text": "DM"
                                },
                                {
                                    "key": "DO",
                                    "text": "DO"
                                },
                                {
                                    "key": "DZ",
                                    "text": "DZ"
                                },
                                {
                                    "key": "EC",
                                    "text": "EC"
                                },
                                {
                                    "key": "EE",
                                    "text": "EE"
                                },
                                {
                                    "key": "EG",
                                    "text": "EG"
                                },
                                {
                                    "key": "EH",
                                    "text": "EH"
                                },
                                {
                                    "key": "ER",
                                    "text": "ER"
                                },
                                {
                                    "key": "ES",
                                    "text": "ES"
                                },
                                {
                                    "key": "ET",
                                    "text": "ET"
                                },
                                {
                                    "key": "FI",
                                    "text": "FI"
                                },
                                {
                                    "key": "FJ",
                                    "text": "FJ"
                                },
                                {
                                    "key": "FK",
                                    "text": "FK"
                                },
                                {
                                    "key": "FM",
                                    "text": "FM"
                                },
                                {
                                    "key": "FO",
                                    "text": "FO"
                                },
                                {
                                    "key": "FR",
                                    "text": "FR"
                                },
                                {
                                    "key": "GA",
                                    "text": "GA"
                                },
                                {
                                    "key": "GB",
                                    "text": "GB"
                                },
                                {
                                    "key": "GD",
                                    "text": "GD"
                                },
                                {
                                    "key": "GE",
                                    "text": "GE"
                                },
                                {
                                    "key": "GF",
                                    "text": "GF"
                                },
                                {
                                    "key": "GG",
                                    "text": "GG"
                                },
                                {
                                    "key": "GH",
                                    "text": "GH"
                                },
                                {
                                    "key": "GI",
                                    "text": "GI"
                                },
                                {
                                    "key": "GL",
                                    "text": "GL"
                                },
                                {
                                    "key": "GM",
                                    "text": "GM"
                                },
                                {
                                    "key": "GN",
                                    "text": "GN"
                                },
                                {
                                    "key": "GP",
                                    "text": "GP"
                                },
                                {
                                    "key": "GQ",
                                    "text": "GQ"
                                },
                                {
                                    "key": "GR",
                                    "text": "GR"
                                },
                                {
                                    "key": "GS",
                                    "text": "GS"
                                },
                                {
                                    "key": "GT",
                                    "text": "GT"
                                },
                                {
                                    "key": "GU",
                                    "text": "GU"
                                },
                                {
                                    "key": "GW",
                                    "text": "GW"
                                },
                                {
                                    "key": "GY",
                                    "text": "GY"
                                },
                                {
                                    "key": "HK",
                                    "text": "HK"
                                },
                                {
                                    "key": "HM",
                                    "text": "HM"
                                },
                                {
                                    "key": "HN",
                                    "text": "HN"
                                },
                                {
                                    "key": "HR",
                                    "text": "HR"
                                },
                                {
                                    "key": "HT",
                                    "text": "HT"
                                },
                                {
                                    "key": "HU",
                                    "text": "HU"
                                },
                                {
                                    "key": "ID",
                                    "text": "ID"
                                },
                                {
                                    "key": "IE",
                                    "text": "IE"
                                },
                                {
                                    "key": "IL",
                                    "text": "IL"
                                },
                                {
                                    "key": "IM",
                                    "text": "IM"
                                },
                                {
                                    "key": "IN",
                                    "text": "IN"
                                },
                                {
                                    "key": "IO",
                                    "text": "IO"
                                },
                                {
                                    "key": "IQ",
                                    "text": "IQ"
                                },
                                {
                                    "key": "IR",
                                    "text": "IR"
                                },
                                {
                                    "key": "IS",
                                    "text": "IS"
                                },
                                {
                                    "key": "IT",
                                    "text": "IT"
                                },
                                {
                                    "key": "JE",
                                    "text": "JE"
                                },
                                {
                                    "key": "JM",
                                    "text": "JM"
                                },
                                {
                                    "key": "JO",
                                    "text": "JO"
                                },
                                {
                                    "key": "JP",
                                    "text": "JP"
                                },
                                {
                                    "key": "KE",
                                    "text": "KE"
                                },
                                {
                                    "key": "KG",
                                    "text": "KG"
                                },
                                {
                                    "key": "KH",
                                    "text": "KH"
                                },
                                {
                                    "key": "KI",
                                    "text": "KI"
                                },
                                {
                                    "key": "KM",
                                    "text": "KM"
                                },
                                {
                                    "key": "KN",
                                    "text": "KN"
                                },
                                {
                                    "key": "KP",
                                    "text": "KP"
                                },
                                {
                                    "key": "KR",
                                    "text": "KR"
                                },
                                {
                                    "key": "KW",
                                    "text": "KW"
                                },
                                {
                                    "key": "KY",
                                    "text": "KY"
                                },
                                {
                                    "key": "KZ",
                                    "text": "KZ"
                                },
                                {
                                    "key": "LA",
                                    "text": "LA"
                                },
                                {
                                    "key": "LB",
                                    "text": "LB"
                                },
                                {
                                    "key": "LC",
                                    "text": "LC"
                                },
                                {
                                    "key": "LI",
                                    "text": "LI"
                                },
                                {
                                    "key": "LK",
                                    "text": "LK"
                                },
                                {
                                    "key": "LR",
                                    "text": "LR"
                                },
                                {
                                    "key": "LS",
                                    "text": "LS"
                                },
                                {
                                    "key": "LT",
                                    "text": "LT"
                                },
                                {
                                    "key": "LU",
                                    "text": "LU"
                                },
                                {
                                    "key": "LV",
                                    "text": "LV"
                                },
                                {
                                    "key": "LY",
                                    "text": "LY"
                                },
                                {
                                    "key": "MA",
                                    "text": "MA"
                                },
                                {
                                    "key": "MC",
                                    "text": "MC"
                                },
                                {
                                    "key": "MD",
                                    "text": "MD"
                                },
                                {
                                    "key": "ME",
                                    "text": "ME"
                                },
                                {
                                    "key": "MF",
                                    "text": "MF"
                                },
                                {
                                    "key": "MG",
                                    "text": "MG"
                                },
                                {
                                    "key": "MH",
                                    "text": "MH"
                                },
                                {
                                    "key": "MK",
                                    "text": "MK"
                                },
                                {
                                    "key": "ML",
                                    "text": "ML"
                                },
                                {
                                    "key": "MM",
                                    "text": "MM"
                                },
                                {
                                    "key": "MN",
                                    "text": "MN"
                                },
                                {
                                    "key": "MO",
                                    "text": "MO"
                                },
                                {
                                    "key": "MP",
                                    "text": "MP"
                                },
                                {
                                    "key": "MQ",
                                    "text": "MQ"
                                },
                                {
                                    "key": "MR",
                                    "text": "MR"
                                },
                                {
                                    "key": "MS",
                                    "text": "MS"
                                },
                                {
                                    "key": "MT",
                                    "text": "MT"
                                },
                                {
                                    "key": "MU",
                                    "text": "MU"
                                },
                                {
                                    "key": "MV",
                                    "text": "MV"
                                },
                                {
                                    "key": "MW",
                                    "text": "MW"
                                },
                                {
                                    "key": "MX",
                                    "text": "MX"
                                },
                                {
                                    "key": "MY",
                                    "text": "MY"
                                },
                                {
                                    "key": "MZ",
                                    "text": "MZ"
                                },
                                {
                                    "key": "NA",
                                    "text": "NA"
                                },
                                {
                                    "key": "NC",
                                    "text": "NC"
                                },
                                {
                                    "key": "NE",
                                    "text": "NE"
                                },
                                {
                                    "key": "NF",
                                    "text": "NF"
                                },
                                {
                                    "key": "NG",
                                    "text": "NG"
                                },
                                {
                                    "key": "NI",
                                    "text": "NI"
                                },
                                {
                                    "key": "NL",
                                    "text": "NL"
                                },
                                {
                                    "key": "NO",
                                    "text": "NO"
                                },
                                {
                                    "key": "NP",
                                    "text": "NP"
                                },
                                {
                                    "key": "NR",
                                    "text": "NR"
                                },
                                {
                                    "key": "NU",
                                    "text": "NU"
                                },
                                {
                                    "key": "NZ",
                                    "text": "NZ"
                                },
                                {
                                    "key": "OM",
                                    "text": "OM"
                                },
                                {
                                    "key": "PA",
                                    "text": "PA"
                                },
                                {
                                    "key": "PE",
                                    "text": "PE"
                                },
                                {
                                    "key": "PF",
                                    "text": "PF"
                                },
                                {
                                    "key": "PG",
                                    "text": "PG"
                                },
                                {
                                    "key": "PH",
                                    "text": "PH"
                                },
                                {
                                    "key": "PK",
                                    "text": "PK"
                                },
                                {
                                    "key": "PL",
                                    "text": "PL"
                                },
                                {
                                    "key": "PM",
                                    "text": "PM"
                                },
                                {
                                    "key": "PN",
                                    "text": "PN"
                                },
                                {
                                    "key": "PR",
                                    "text": "PR"
                                },
                                {
                                    "key": "PS",
                                    "text": "PS"
                                },
                                {
                                    "key": "PT",
                                    "text": "PT"
                                },
                                {
                                    "key": "PW",
                                    "text": "PW"
                                },
                                {
                                    "key": "PY",
                                    "text": "PY"
                                },
                                {
                                    "key": "QA",
                                    "text": "QA"
                                },
                                {
                                    "key": "RE",
                                    "text": "RE"
                                },
                                {
                                    "key": "RO",
                                    "text": "RO"
                                },
                                {
                                    "key": "RS",
                                    "text": "RS"
                                },
                                {
                                    "key": "RU",
                                    "text": "RU"
                                },
                                {
                                    "key": "RW",
                                    "text": "RW"
                                },
                                {
                                    "key": "SA",
                                    "text": "SA"
                                },
                                {
                                    "key": "SB",
                                    "text": "SB"
                                },
                                {
                                    "key": "SC",
                                    "text": "SC"
                                },
                                {
                                    "key": "SD",
                                    "text": "SD"
                                },
                                {
                                    "key": "SE",
                                    "text": "SE"
                                },
                                {
                                    "key": "SG",
                                    "text": "SG"
                                },
                                {
                                    "key": "SH",
                                    "text": "SH"
                                },
                                {
                                    "key": "SI",
                                    "text": "SI"
                                },
                                {
                                    "key": "SJ",
                                    "text": "SJ"
                                },
                                {
                                    "key": "SK",
                                    "text": "SK"
                                },
                                {
                                    "key": "SL",
                                    "text": "SL"
                                },
                                {
                                    "key": "SM",
                                    "text": "SM"
                                },
                                {
                                    "key": "SN",
                                    "text": "SN"
                                },
                                {
                                    "key": "SO",
                                    "text": "SO"
                                },
                                {
                                    "key": "SR",
                                    "text": "SR"
                                },
                                {
                                    "key": "SS",
                                    "text": "SS"
                                },
                                {
                                    "key": "ST",
                                    "text": "ST"
                                },
                                {
                                    "key": "SV",
                                    "text": "SV"
                                },
                                {
                                    "key": "SX",
                                    "text": "SX"
                                },
                                {
                                    "key": "SY",
                                    "text": "SY"
                                },
                                {
                                    "key": "SZ",
                                    "text": "SZ"
                                },
                                {
                                    "key": "TC",
                                    "text": "TC"
                                },
                                {
                                    "key": "TD",
                                    "text": "TD"
                                },
                                {
                                    "key": "TF",
                                    "text": "TF"
                                },
                                {
                                    "key": "TG",
                                    "text": "TG"
                                },
                                {
                                    "key": "TH",
                                    "text": "TH"
                                },
                                {
                                    "key": "TJ",
                                    "text": "TJ"
                                },
                                {
                                    "key": "TK",
                                    "text": "TK"
                                },
                                {
                                    "key": "TL",
                                    "text": "TL"
                                },
                                {
                                    "key": "TM",
                                    "text": "TM"
                                },
                                {
                                    "key": "TN",
                                    "text": "TN"
                                },
                                {
                                    "key": "TO",
                                    "text": "TO"
                                },
                                {
                                    "key": "TR",
                                    "text": "TR"
                                },
                                {
                                    "key": "TT",
                                    "text": "TT"
                                },
                                {
                                    "key": "TV",
                                    "text": "TV"
                                },
                                {
                                    "key": "TW",
                                    "text": "TW"
                                },
                                {
                                    "key": "TZ",
                                    "text": "TZ"
                                },
                                {
                                    "key": "UA",
                                    "text": "UA"
                                },
                                {
                                    "key": "UG",
                                    "text": "UG"
                                },
                                {
                                    "key": "UM",
                                    "text": "UM"
                                },
                                {
                                    "key": "US",
                                    "text": "US"
                                },
                                {
                                    "key": "UY",
                                    "text": "UY"
                                },
                                {
                                    "key": "UZ",
                                    "text": "UZ"
                                },
                                {
                                    "key": "VA",
                                    "text": "VA"
                                },
                                {
                                    "key": "VC",
                                    "text": "VC"
                                },
                                {
                                    "key": "VE",
                                    "text": "VE"
                                },
                                {
                                    "key": "VG",
                                    "text": "VG"
                                },
                                {
                                    "key": "VI",
                                    "text": "VI"
                                },
                                {
                                    "key": "VN",
                                    "text": "VN"
                                },
                                {
                                    "key": "VU",
                                    "text": "VU"
                                },
                                {
                                    "key": "WF",
                                    "text": "WF"
                                },
                                {
                                    "key": "WS",
                                    "text": "WS"
                                },
                                {
                                    "key": "XK",
                                    "text": "XK"
                                },
                                {
                                    "key": "YE",
                                    "text": "YE"
                                },
                                {
                                    "key": "YT",
                                    "text": "YT"
                                },
                                {
                                    "key": "ZA",
                                    "text": "ZA"
                                },
                                {
                                    "key": "ZM",
                                    "text": "ZM"
                                },
                                {
                                    "key": "ZW",
                                    "text": "ZW"
                                },
                                {
                                    "key": "Other",
                                    "text": "Other"
                                },
                                {
                                    "key": "Skip",
                                    "text": "Skip"
                                }
                            ],
                            "dependencies": [
                                {
                                    "fieldName": "InvalidDocument",
                                    "targetValue": [
                                        "Valid"
                                    ]
                                },
                                {
                                    "fieldName": "ImageQuality",
                                    "targetValue": [
                                        "Good"
                                    ]
                                }
                            ]
                        }
                    }
                ]
            }
        }
    ]
}

# Define headers (if required)
headers = {
    "Content-Type": "application/json",
    # "Authorization": "Bearer YOUR_TOKEN"  # Replace with your API token
}

# Send the POST request
response = requests.post(url, headers=headers, json=payload)

# Check the response
print(f"Status Code: {response.status_code}")
try:
    print("Response JSON:", response.json())
except json.JSONDecodeError:
    print("Response Text:", response.text)