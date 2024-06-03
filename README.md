
`
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
