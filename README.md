
`
# DDN Codespace Starter Kit

Kickstart your DDN supergraph development with this comprehensive starter kit. When you launch this repository in a GitHub Codespace, you'll be instantly set up with the DDN CLI and the Hasura VS Code extension, providing you with an environment tailored for DDN supergraph development.

## Getting Started

### Step 1: Authenticate with Hasura DDN CLI
To begin, authenticate with the Hasura DDN CLI using your Personal Access Token (PAT). Don't have a PAT yet? Generate one [here](https://hasura.io/docs/latest/api-reference/cloud-api-reference/#authentication).

Run the following command to log in:

\`\`\`sh
ddn login --pat {{YOUR_HASURA_PAT}}
\`\`\`

> **Note**: Since GitHub Codespaces operate on remote machine configurations, the OAuth login with redirect won't function. Please use your PAT for authentication.

### Step 2: Create Your DDN Supergraph Project
With authentication complete, you can now create a new DDN supergraph project and dive into development. Follow the steps outlined [here](https://hasura.io/docs/3.0/getting-started/create-a-project#step-3-create-a-new-project) to set up your project and begin building your supergraph.