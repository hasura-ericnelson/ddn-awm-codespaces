

# AWM Hasura DDN POC w/ Elasticsearch and TS Codespace 

Hasura DDN POC-in-a-box!  This is a pre-configured Hasura DDN project that is pre-configured with Elasticsearch and TypeScript connectors and an Elasticserach database filled with sample financial data.  Details of the data can be found below.

## Getting Started

### Step 1: Authenticate with Hasura DDN CLI
To begin, authenticate with the Hasura DDN CLI using your Personal Access Token (PAT). Don't have a PAT yet? Generate one [here](https://hasura.io/docs/latest/api-reference/cloud-api-reference/#authentication).

Run the following command to log in:

```sh
ddn login --pat {{YOUR_HASURA_PAT}}
```

> **Note**: Since GitHub Codespaces operate on remote machine configurations, the OAuth login with redirect won't function. Please use your PAT for authentication.  Ensure you use a PAT for the correct environment.  Ie, use a PAT from staging if using the staging `ddn` CLI.  

### Step 2: Experiment with your DDN Supergraph Project
With authentication complete, you can now create a new DDN supergraph project and dive into development. Follow the steps outlined [here](https://hasura.io/docs/3.0/getting-started/create-a-project#step-3-create-a-new-project) to set up your project and begin building your supergraph.


### Sample Elasticsearch Document
<details>
  <summary>Sample Document</summary>

```json
 {
        "accountBaseCurrency": "KWD",
        "accountBusinessSystem": "Dietrich, Hahn and Ward",
        "accountLobCode": "Commercial",
        "accountNumber": "KZ650063274383N7G88Y",
        "accountServiceCode": "da8qtNBYbf",
        "accountStatusCode": "Active",
        "accountStatusName": "solidly",
        "accountTypeGroup": "Savings",
        "areaNodeIdentifiers": "626c1388-35d1-43bc-a5da-a23b48dd076b",
        "branchCode": "K3lBB",
        "branchName": "Powlowski, Leannon and Reichel",
        "businessDate": "Sun Jun 02 2024 09:24:00 GMT-0400 (Eastern Daylight Time)",
        "businessSystemCode": "48oM8jr1",
        "cashPercentage": 0.1691,
        "cbosOrDfiAccount": false,
        "corporateLobGroupCode": "QOw4e",
        "costCenterCodes": "l4kjm6s",
        "coverageUsers": "Retha_Macejkovic49",
        "dmEciIdentifier": "ZGc7MK6j9f",
        "eciIdentifier": "pesfINxNbj",
        "financialAdvisorSid": "bee3491c-f03e-48db-b931-e40a6ce391b2",
        "gwmIdentifier": "3f55a2a3-1ade-4405-b414-76f7436b1223",
        "id": "1",
        "instrumentCodes": "INSTRkNHqdJ",
        "marketNodeIdentifiers": "cde77e8d-4d8b-4b18-8d0e-0f1859ebc498",
        "occdNumber": "GOYMdvFnAH",
        "partyTypeName": "Individual",
        "largeCashPositionAlert": false,
        "investmentObjectiveCode": [
          {
            "raw": "communities"
          }
        ],
        "investmentObjectiveName": [
          {
            "raw": "database"
          }
        ],
        "modelStrategyName": [
          {
            "raw": "eco-centric"
          }
        ],
        "transactions": [
          {
            "baseGrossAmount": -61781.26,
            "accountNumber": "KZ650063274383N7G88Y",
            "instrumentCode": "INSTRS5oK9"
          },
          {
            "baseGrossAmount": -61502.17,
            "accountNumber": "KZ650063274383N7G88Y",
            "instrumentCode": "INSTRaU1d2"
          },
        ],
        "positions": [
          {
            "accountBaseCurrency": "KZT",
            "accountNumber": "KZ650063274383N7G88Y",
            "baseAdjustedCostAmount": 13430.29,
            "baseExpectedIncomeAmount": 533.59,
            "baseMarketPrice": 1242.6,
            "baseSettledMarketValueAmount": 9966.76,
            "baseTradedMarketValueAmount": 161996.8,
            "companyName": [
              {
                "raw": "Prosacco - Barrows"
              }
            ],
            "instrumentCode": "INSTRDJ3Ta"
          },
        ]
     }
}
```
<details>