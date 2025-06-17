# ChatGPT-Reviewer

🤖 **Automated pull request reviews and issue triaging powered by ChatGPT**

[![GitHub](https://img.shields.io/github/license/danylevych/ChatGPT-Reviewer)](LICENSE)
[![OpenAI API](https://img.shields.io/badge/OpenAI-API%20v1.86+-blue)](https://platform.openai.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)](Dockerfile)

An intelligent GitHub Action that automatically reviews pull requests using OpenAI's ChatGPT models. This fork includes the latest OpenAI API (v1.86+) with enhanced features, better error handling, and support for both OpenAI and Azure OpenAI services.

## ✨ Features

- 🔍 **Comprehensive Code Review**: Analyzes code changes, identifies issues, and suggests improvements
- 🛡️ **Security Analysis**: Detects potential security vulnerabilities in your code
- 🚀 **Latest OpenAI Models**: Support for GPT-4.1 Mini, GPT-4, GPT-4 Turbo, GPT-4o, and GPT-3.5 Turbo
- ☁️ **Multi-Provider Support**: Works with both OpenAI and Azure OpenAI
- 📁 **Flexible Review Modes**: Review entire PRs or individual files
- ⚡ **Streaming Responses**: Real-time review generation
- 🔄 **Automatic Retry**: Built-in retry logic with exponential backoff
- 🎯 **Customizable**: Configurable temperature, penalties, and review behavior

## 🚀 Quick Start

### 1. Get Your OpenAI API Key

Create an OpenAI API key at [platform.openai.com](https://platform.openai.com/account/api-keys)

### 2. Configure Repository Secrets

Add the following secrets to your repository ([guide](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository)):

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_API_BASE`: Your Azure OpenAI endpoint (optional, for Azure users)

### 3. Create Workflow File

Create `.github/workflows/chatgpt-review.yml`:

```yaml
name: ChatGPT Review

on: [pull_request]

jobs:
  chatgpt-review:
    name: ChatGPT Review
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      contents: read
    steps:
    - name: ChatGPT Reviewer
      uses: danylevych/ChatGPT-Reviewer@main
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        # OPENAI_API_BASE: ${{ secrets.OPENAI_API_BASE }}  # For Azure OpenAI
      with:
        model: "gpt-4"  # or gpt-4.1-mini, gpt-3.5-turbo, gpt-4-turbo, gpt-4o
        temperature: 0.2
        review_per_file: true
        comment_per_file: true
```

### For Public Repository Forks

If you're working with public repositories and forks, use `pull_request_target` instead of `pull_request` to ensure proper permissions:

```yaml
name: ChatGPT Review

on:
  pull_request_target:
    types: [opened, synchronize]

jobs:
  chatgpt-review:
    name: ChatGPT Review
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      contents: read
    steps:
    - name: ChatGPT Reviewer
      uses: danylevych/ChatGPT-Reviewer@main
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      with:
        model: "gpt-4.1-mini"
        temperature: 0.2
        review_per_file: true
        comment_per_file: true
```

⚠️ **Security Note**: `pull_request_target` runs in the context of the base repository, so it has access to secrets. Only use this for trusted contributors.

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `GITHUB_TOKEN` | GitHub token for posting comments | ✅ | `${{ secrets.GITHUB_TOKEN }}` |
| `OPENAI_API_KEY` | OpenAI API key | ✅ | `sk-...` |
| `OPENAI_API_BASE` | Azure OpenAI endpoint | ❌ | `https://your-resource.openai.azure.com/` |

### Input Parameters

| Parameter | Description | Default | Options |
|-----------|-------------|---------|---------|
| `model` | OpenAI model to use | `gpt-4.1-mini` | `gpt-4.1-mini`, `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo`, `gpt-4o` |
| `temperature` | Creativity level (0.0-2.0) | `0.2` | `0.0` (focused) to `2.0` (creative) |
| `frequency_penalty` | Penalty for repetition | `0` | `-2.0` to `2.0` |
| `presence_penalty` | Penalty for new topics | `0` | `-2.0` to `2.0` |
| `review_per_file` | Review each file separately | `false` | `true`, `false` |
| `comment_per_file` | Comment on each file | `true` | `true`, `false` |
| `blocking` | Block PR on OpenAI failures | `false` | `true`, `false` |

## 🔧 Advanced Usage

### Using GPT-4 for Better Reviews

```yaml
- name: ChatGPT Reviewer
  uses: danylevych/ChatGPT-Reviewer@main
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  with:
    model: "gpt-4"
    temperature: 0.1
    review_per_file: true
```

### Azure OpenAI Configuration

```yaml
- name: ChatGPT Reviewer
  uses: danylevych/ChatGPT-Reviewer@main
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    OPENAI_API_KEY: ${{ secrets.AZURE_OPENAI_KEY }}
    OPENAI_API_BASE: ${{ secrets.AZURE_OPENAI_ENDPOINT }}
  with:
    model: "gpt-35-turbo"  # Azure deployment name
```

### File-by-File Review for Large PRs

```yaml
with:
  review_per_file: true
  comment_per_file: true
  temperature: 0.2
```

## 🏗️ What's New in This Fork

- ✅ **Updated to OpenAI API v1.86+**: Latest features and improvements
- ✅ **Enhanced Error Handling**: Better retry logic and error messages
- ✅ **Azure OpenAI Support**: Full compatibility with Azure OpenAI services
- ✅ **Improved Streaming**: More efficient real-time response processing
- ✅ **Modern Client**: Uses the new OpenAI Python client architecture
- ✅ **Better Security**: Updated dependencies and security practices

## 🔒 Security & Privacy

- The action only has access to the PR diff, not your entire codebase
- API keys are securely handled through GitHub Secrets
- No code is stored or logged by the action
- All communication with OpenAI uses encrypted HTTPS

## 🐛 Troubleshooting

### Common Issues

**Q: Getting "403 Forbidden" or "Resource not accessible by integration"**
A: Add the `permissions` section to your workflow as shown above. Ensure your workflow has:
```yaml
permissions:
  pull-requests: write
  contents: read
```

**Q: Getting "OpenAI API key not found"**
A: Ensure `OPENAI_API_KEY` is set in your repository secrets

**Q: Reviews not appearing**
A: Check that `GITHUB_TOKEN` has write permissions for pull requests

**Q: Azure OpenAI not working**
A: Verify `OPENAI_API_BASE` is set and model name matches your deployment

**Q: Rate limiting errors**
A: The action includes automatic retry logic, but consider using GPT-4.1-mini for high-volume usage

**Q: Getting "ResolutionImpossible" error during Docker build**
A: This indicates dependency conflicts. Make sure your `requirements.txt` doesn't have:
- Duplicate package entries
- Conflicting version requirements
- Unnecessary packages (like `argparse` which is built into Python)

### Repository Settings

For the action to work properly, ensure:

1. **Repository Settings**: Go to Settings → Actions → General → Workflow permissions
   - Select "Read and write permissions"
   - Check "Allow GitHub Actions to create and approve pull requests"

2. **Branch Protection**: If you have branch protection rules, ensure the action can post comments

3. **Fork Handling**: For public repositories with external contributors, use `pull_request_target` with caution

## 🔄 Migration from Original Version

If you're migrating from `feiskyer/ChatGPT-Reviewer`, simply update your workflow:

```yaml
# Old
uses: feiskyer/ChatGPT-Reviewer@v0

# New
uses: danylevych/ChatGPT-Reviewer@main
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original project by [feiskyer](https://github.com/feiskyer/ChatGPT-Reviewer)
- Powered by [OpenAI](https://openai.com/)

---

**⭐ If this action helps you, please consider giving it a star!**
