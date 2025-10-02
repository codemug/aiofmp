# aiofmp

[![PyPI Version](https://img.shields.io/pypi/v/aiofmp.svg?color=0A7BBB)](https://pypi.org/project/aiofmp/)

**aiofmp** is a comprehensive Python SDK that provides seamless access to the Financial Modeling Prep API through an intuitive, category-based interface. Built with asyncio for high-performance concurrent operations, it offers:

- **Complete FMP API Coverage**: Access to 22+ API categories including financial statements, market data, news, technical indicators, and more
- **Async-First Design**: Built with asyncio for high-performance concurrent operations and non-blocking I/O
- **MCP Server Integration**: Built-in Model Context Protocol server that exposes all FMP APIs as AI-friendly tools
- **Type Safety**: Full type hints throughout the codebase for better IDE support and error prevention
- **Clean Architecture**: Category-based organization that mirrors the FMP API structure
- **Comprehensive Error Handling**: Robust error handling with custom exceptions and retry logic
- **Rate Limiting**: Built-in rate limiting and retry logic to respect API limits
- **AI-Ready**: MCP tools designed specifically for AI assistants with natural language prompts

### Key Features

- **22 API Categories**: Complete coverage of all FMP API endpoints
- **Flexible Configuration**: Environment-based configuration for easy deployment
- **160+ MCP Tools**: Every FMP API function exposed as an MCP tool for AI assistants
- **Dual Transport Support**: Both STDIO and HTTP transport modes for MCP server
- **Comprehensive Testing**: Full test coverage with 500+ unit tests
- **Production Ready**: Built for reliability and performance in production environments

## Installation

### Prerequisites

- Python 3.10 or higher
- Financial Modeling Prep API key ([Get one here](https://site.financialmodelingprep.com/developer/docs/pricing))

### Install from Source

```bash
# Clone the repository
git clone https://github.com/your-username/aiofmp.git
cd aiofmp

# Install dependencies using uv (recommended)
uv sync

# Install the package in development mode
uv pip install -e .

# Or using pip
pip install -e .

# Activate virtual environment (if using uv)
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## Usage

### Basic Client Usage

```python
import asyncio
from aiofmp import FmpClient

async def main():
    # Initialize client with your API key
    client = FmpClient(api_key="your_api_key_here")

    # Use async context manager for automatic session management
    async with client:
        # Search for symbols
        symbols = await client.search.symbols("AAPL", limit=10)
        print(f"Found {len(symbols)} symbols")

        # Get company profile
        profile = await client.company.profile("AAPL")
        print(f"Company: {profile['companyName']}")
        
        # Get financial statements
        income_statement = await client.statements.income_statement("AAPL", limit=5)
        print(f"Retrieved {len(income_statement)} periods of income statement data")

# Run the example
asyncio.run(main())
```

### MCP Server Usage

The aiofmp package includes a built-in MCP server that exposes all FMP APIs as AI-friendly tools.

#### Configuration

Set up environment variables for MCP server configuration:

```bash
# Required: FMP API Key
export FMP_API_KEY="your_api_key_here"

# Optional: MCP Server Configuration
export MCP_TRANSPORT="stdio"  # or "http"
export MCP_HOST="localhost"   # for HTTP transport
export MCP_PORT="3000"        # for HTTP transport
export MCP_LOG_LEVEL="INFO"   # DEBUG, INFO, WARNING, ERROR
```

#### Running the MCP Server

**STDIO Transport (for MCP clients like Claude Desktop):**
```bash
aiofmp-mcp-server
```

**HTTP Transport (for web-based MCP clients):**
```bash
aiofmp-mcp-server --transport http
```

**Custom Configuration:**
```bash
aiofmp-mcp-server --transport http --host 0.0.0.0 --port 8080
```

**With API Key:**
```bash
aiofmp-mcp-server --api-key your_api_key_here
```

**With Debug Logging:**
```bash
aiofmp-mcp-server --log-level DEBUG
```

**Include text content alongside structured content:**
```bash
aiofmp-mcp-server --text-content
```

#### Claude Desktop Integration

Add to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "aiofmp": {
      "command": "aiofmp-mcp-server",
      "args": ["--api-key", "your_api_key_here"]
    }
  }
}
```

**Alternative with environment variable:**
```json
{
  "mcpServers": {
    "aiofmp": {
      "command": "aiofmp-mcp-server",
      "env": {
        "FMP_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### CLI Reference

The `aiofmp-mcp-server` command provides a user-friendly interface for running the MCP server:

```bash
# Basic usage
aiofmp-mcp-server

# Show help
aiofmp-mcp-server --help

# HTTP transport
aiofmp-mcp-server --transport http --host 0.0.0.0 --port 8080

# With API key
aiofmp-mcp-server --api-key your_api_key_here

# Debug logging
aiofmp-mcp-server --log-level DEBUG

# Include text content alongside structured content
aiofmp-mcp-server --text-content

# All options
aiofmp-mcp-server --transport http --host localhost --port 3000 --log-level INFO --api-key your_key --text-content
```

**Command Options:**
- `--transport`: Transport mode (`stdio` or `http`, default: `stdio`)
- `--host`: Host for HTTP transport (default: `localhost`)
- `--port`: Port for HTTP transport (default: `3000`)
- `--log-level`: Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, default: `INFO`)
- `--api-key`: FMP API key (can also be set via `FMP_API_KEY` environment variable)
- `--text-content`: Include text content alongside structured content in MCP tool responses (default: text content is empty when structured content is present)

### Available API Categories

The aiofmp client provides access to 22+ FMP API categories:

- **Analyst**: Financial estimates, ratings, price targets, and analyst recommendations
- **Calendar**: Earnings, dividends, IPOs, and economic events
- **Chart**: Historical price data and technical analysis
- **Company**: Company profiles, key metrics, and corporate information
- **Commodity**: Commodity prices, quotes, and historical data
- **COT**: Commitment of Traders reports for commodities
- **Crypto**: Cryptocurrency prices, quotes, and market data
- **DCF**: Discounted Cash Flow valuations and analysis
- **Directory**: Symbol lists, exchanges, sectors, and reference data
- **Economics**: Economic indicators, treasury rates, and macro data
- **ETF**: ETF holdings, performance, and analysis
- **Forex**: Foreign exchange rates and currency data
- **Form 13F**: Institutional holdings and filings
- **Indexes**: Stock market indices and performance
- **Insider Trades**: Insider trading activity and statistics
- **Market Performance**: Sector performance, market movers, and P/E ratios
- **News**: Financial news, press releases, and market updates
- **Quote**: Real-time quotes, price changes, and market data
- **Search**: Symbol search, company search, and stock screening
- **Senate**: Congressional trading disclosures and activity
- **Statements**: Financial statements, ratios, and metrics
- **Technical Indicators**: Moving averages, RSI, and technical analysis tools

## Examples

### Client Examples

The `examples/` directory contains comprehensive examples for each API category:

```bash
# Run specific examples
python examples/fmp_search_example.py
python examples/fmp_company_example.py
python examples/fmp_statements_example.py
python examples/fmp_technical_indicators_example.py
```

### MCP Server Examples

**Example 1: Basic MCP Tool Usage**
```python
# These are example prompts that would be sent to an AI assistant using the MCP server
"What is the current stock quote for Apple (AAPL)?"
"Show me the 20-day Simple Moving Average for Microsoft (MSFT)"
"Get the latest financial statements for Tesla (TSLA)"
```

**Example 2: Advanced Financial Analysis**
```python
# Complex analysis prompts
"Compare the P/E ratios of Apple, Microsoft, and Google over the past year"
"Find all technology stocks with market cap over $100 billion"
"Show me the insider trading activity for Tesla in the last 3 months"
```

**Example 3: Market Research**
```python
# Market research prompts
"What are the biggest gainers in the market today?"
"Show me the sector performance for the technology sector"
"Get the latest earnings calendar for next week"
```

### Example Files

- `fmp_analyst_example.py` - Analyst estimates and ratings
- `fmp_calendar_example.py` - Earnings and dividend calendars
- `fmp_chart_example.py` - Historical price data
- `fmp_company_example.py` - Company profiles and metrics
- `fmp_commodity_example.py` - Commodity prices and data
- `fmp_cot_example.py` - Commitment of Traders reports
- `fmp_crypto_example.py` - Cryptocurrency data
- `fmp_dcf_example.py` - DCF valuations
- `fmp_directory_example.py` - Symbol lists and reference data
- `fmp_economics_example.py` - Economic indicators
- `fmp_etf_example.py` - ETF analysis
- `fmp_forex_example.py` - Foreign exchange data
- `fmp_form13f_example.py` - Institutional holdings
- `fmp_indexes_example.py` - Market indices
- `fmp_insider_trades_example.py` - Insider trading
- `fmp_search_example.py` - Symbol and company search
- `fmp_statements_example.py` - Financial statements

### MCP Server Testing

Test the MCP server functionality:

```bash
# Run all MCP tests
uv run pytest tests/test_mcp_tools.py tests/test_mcp_server.py -v

# Run specific category tests
uv run pytest tests/test_mcp_tools.py::TestSearchTools -v
uv run pytest tests/test_mcp_server.py::TestMCPServer -v

# Test with debug logging
aiofmp-mcp-server --log-level DEBUG
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FMP_API_KEY` | Financial Modeling Prep API key | None | Yes |
| `MCP_TRANSPORT` | MCP server transport mode | `stdio` | No |
| `MCP_HOST` | MCP server host (HTTP mode) | `localhost` | No |
| `MCP_PORT` | MCP server port (HTTP mode) | `3000` | No |
| `MCP_LOG_LEVEL` | Logging level | `INFO` | No |

### MCP Server Modes

**STDIO Mode (Default):**
- Used by MCP clients like Claude Desktop
- Communicates via standard input/output
- No network configuration required

**HTTP Mode:**
- Used by web-based MCP clients
- Requires host and port configuration
- Supports multiple concurrent connections

## API Reference

### Client Categories

Each API category provides methods that mirror the FMP API structure:

```python
# Search and discovery
await client.search.symbols("AAPL")
await client.search.companies("Apple")
await client.search.screener(sector="Technology")

# Company information
await client.company.profile("AAPL")
await client.company.key_metrics("AAPL")

# Financial statements
await client.statements.income_statement("AAPL")
await client.statements.balance_sheet("AAPL")
await client.statements.cash_flow_statement("AAPL")

# Market data
await client.quote.stock_quote("AAPL")
await client.chart.historical_price_full("AAPL")

# Technical analysis
await client.technical_indicators.simple_moving_average("AAPL", 20, "1day")
await client.technical_indicators.relative_strength_index("AAPL", 14, "1day")
```

### MCP Tools

The MCP server exposes 160+ tools across all categories. Each tool includes:
- Detailed descriptions and parameter documentation
- Natural language examples for AI assistants
- Comprehensive error handling
- Type validation and parameter checking

## Error Handling

The client includes comprehensive error handling:

```python
from aiofmp.exceptions import FmpError, FmpRateLimitError, FmpAPIError

try:
    data = await client.search.symbols("INVALID")
except FmpAPIError as e:
    print(f"API Error: {e}")
except FmpRateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except FmpError as e:
    print(f"General error: {e}")
```

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
uv run pytest

# Run specific test categories
uv run pytest tests/test_search.py -v
uv run pytest tests/test_mcp_tools.py -v

# Run with coverage
uv run pytest --cov=aiofmp --cov-report=html
```

## Performance

- **Async Operations**: All API calls are non-blocking
- **Connection Pooling**: Efficient HTTP connection management
- **Rate Limiting**: Built-in rate limiting to respect API limits
- **Caching**: Optional response caching for improved performance
- **Concurrent Requests**: Support for multiple simultaneous API calls

## Security

- **API Key Management**: Secure handling of API keys
- **Environment Variables**: Support for environment-based configuration
- **No Hardcoded Secrets**: All sensitive data via configuration
- **HTTPS Only**: All API communications over secure connections

## Release Process

This project uses [Semantic Release](https://semantic-release.gitbook.io/) for automated versioning and publishing. The release process is fully automated through GitHub Actions.

### How It Works

1. **Conventional Commits**: All commits must follow the [Conventional Commits](https://conventionalcommits.org/) specification
2. **Automatic Versioning**: Semantic Release analyzes commit messages to determine the next version
3. **Automatic Publishing**: When a new version is detected, it automatically:
   - Creates a git tag
   - Updates the CHANGELOG.md
   - Publishes to PyPI
   - Creates a GitHub release

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test additions or changes
- `chore`: Build process or auxiliary tool changes

**Examples:**
```bash
feat(mcp): add new search tools for financial data
fix(api): resolve authentication error in client
docs: update installation instructions
test: add unit tests for MCP server
chore: update dependencies
```

### Setting Up Releases

1. **Configure Git** (run once):
   ```bash
   ./scripts/setup-git.sh
   ```

2. **Set up PyPI Token**:
   - Go to [PyPI Account Settings](https://pypi.org/manage/account/)
   - Create an API token
   - Add it to GitHub Secrets as `PYPI_API_TOKEN`

3. **Update Repository URLs**:
  - Update URLs in `pyproject.toml`
  - Update author information

4. **Make Changes and Commit**:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   git push origin main
   ```

The GitHub Action will automatically:
- Run quick tests and linting
- Check code quality
- Determine if a release is needed
- Create a new version and publish to PyPI

### Manual Testing

For comprehensive testing, you can manually trigger the test workflow:

1. Go to the "Actions" tab in your GitHub repository
2. Select the "Test" workflow
3. Click "Run workflow"
4. Choose:
   - **Python version**: 3.10, 3.11, 3.12, or 3.13
   - **Test type**: all, unit, mcp, or integration
5. Click "Run workflow"

This allows you to run tests on specific Python versions or test categories without using your free tier minutes unnecessarily.

## Contributing

Contributions are welcome! We appreciate any help in improving aiofmp.

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/your-username/aiofmp.git
cd aiofmp
uv sync --dev

# Install pre-commit hooks
pre-commit install

# Run tests
uv run pytest

# Run linting
uv run ruff check .
uv run ruff format .
```

### Contribution Guidelines

1. **Fork the repository** and create a feature branch
2. **Follow the coding standards** (type hints, docstrings, error handling)
3. **Add comprehensive tests** for new functionality
4. **Update documentation** for any API changes
5. **Ensure all tests pass** before submitting a PR
6. **Use conventional commits** for commit messages

### Areas for Contribution

- **New API Endpoints**: Add support for new FMP API endpoints
- **Performance Improvements**: Optimize existing functionality
- **Documentation**: Improve examples and documentation
- **Testing**: Add more comprehensive test coverage
- **MCP Tools**: Enhance MCP tool descriptions and examples
- **Error Handling**: Improve error messages and handling

### Reporting Issues

Please report bugs and request features through GitHub Issues. Include:
- Python version and operating system
- Steps to reproduce the issue
- Expected vs actual behavior
- Relevant error messages and logs

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Financial Modeling Prep](https://financialmodelingprep.com/) for providing the comprehensive financial data API
- [FastMCP](https://github.com/jlowin/fastmcp) for the MCP server framework
- The Python asyncio community for excellent async programming tools

## Support

- **Documentation**: Check the examples directory and inline docstrings
- **Issues**: Report bugs and request features via GitHub Issues
- **Discussions**: Use GitHub Discussions for questions and community support
- **API Reference**: Full API documentation available in the code

---

**Built with ❤️ for the financial data community**
