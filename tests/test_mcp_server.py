"""
Unit tests for MCP server

This module provides comprehensive unit tests for the MCP server
in the aiofmp package.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from aiofmp.mcp_server import get_fmp_client, run_server, main
from aiofmp.base import FMPAuthenticationError, FMPRateLimitError, FMPResponseError


class TestMCPServer:
    """Test MCP server functionality."""
    
    def test_get_fmp_client_creation(self):
        """Test FMP client creation."""
        with patch.dict(os.environ, {'FMP_API_KEY': 'test_key'}):
            client = get_fmp_client()
            assert client is not None
            assert client.api_key == 'test_key'
    
    def test_get_fmp_client_missing_api_key(self):
        """Test FMP client creation with missing API key."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(FMPAuthenticationError, match="FMP_API_KEY environment variable is required"):
                get_fmp_client()
    
    def test_get_fmp_client_singleton(self):
        """Test that FMP client is a singleton."""
        with patch.dict(os.environ, {'FMP_API_KEY': 'test_key'}):
            client1 = get_fmp_client()
            client2 = get_fmp_client()
            assert client1 is client2
    
    @pytest.mark.asyncio
    async def test_run_server_stdio(self):
        """Test running server with STDIO transport."""
        with patch.dict(os.environ, {'FMP_API_KEY': 'test_key', 'MCP_TRANSPORT': 'stdio'}):
            with patch('aiofmp.mcp_server.mcp.run') as mock_run:
                mock_run.return_value = None
                
                await run_server()
                
                mock_run.assert_called_once_with(transport="stdio")
    
    @pytest.mark.asyncio
    async def test_run_server_http(self):
        """Test running server with HTTP transport."""
        with patch.dict(os.environ, {'FMP_API_KEY': 'test_key', 'MCP_TRANSPORT': 'http', 'MCP_HOST': 'localhost', 'MCP_PORT': '3000'}):
            with patch('aiofmp.mcp_server.mcp.run') as mock_run:
                mock_run.return_value = None
                
                await run_server()
                
                mock_run.assert_called_once_with(transport="http", host="localhost", port=3000)
    
    @pytest.mark.asyncio
    async def test_run_server_missing_api_key(self):
        """Test running server with missing API key."""
        with patch.dict(os.environ, {}, clear=True):
            with patch('sys.exit') as mock_exit:
                await run_server()
                mock_exit.assert_called_once_with(1)
    
    @pytest.mark.asyncio
    async def test_run_server_keyboard_interrupt(self):
        """Test handling keyboard interrupt."""
        with patch.dict(os.environ, {'FMP_API_KEY': 'test_key'}):
            with patch('aiofmp.mcp_server.mcp.run') as mock_run:
                mock_run.side_effect = KeyboardInterrupt()
                
                await run_server()
                
                # Should not raise an exception
                assert True
    
    @pytest.mark.asyncio
    async def test_run_server_general_exception(self):
        """Test handling general exceptions."""
        with patch.dict(os.environ, {'FMP_API_KEY': 'test_key'}):
            with patch('aiofmp.mcp_server.mcp.run') as mock_run:
                mock_run.side_effect = Exception("Server error")
                
                with patch('sys.exit') as mock_exit:
                    await run_server()
                    mock_exit.assert_called_once_with(1)
    
    def test_main_function(self):
        """Test main function entry point."""
        with patch('aiofmp.mcp_server.run_server') as mock_run_server:
            mock_run_server.return_value = None
            
            main()
            
            mock_run_server.assert_called_once()


class TestMCPServerErrorHandling:
    """Test MCP server error handling."""
    
    def test_error_handler_authentication_error(self):
        """Test error handler for authentication errors."""
        from aiofmp.mcp_server import mcp
        
        # Mock the error handler
        error_handler = None
        for handler in mcp._error_handlers:
            if hasattr(handler, '__name__') and handler.__name__ == 'handle_error':
                error_handler = handler
                break
        
        if error_handler:
            error = FMPAuthenticationError("Invalid API key")
            result = error_handler(error)
            
            assert result["error"] == "Authentication failed"
            assert result["message"] == "Invalid API key"
            assert result["type"] == "authentication_error"
    
    def test_error_handler_rate_limit_error(self):
        """Test error handler for rate limit errors."""
        from aiofmp.mcp_server import mcp
        
        # Mock the error handler
        error_handler = None
        for handler in mcp._error_handlers:
            if hasattr(handler, '__name__') and handler.__name__ == 'handle_error':
                error_handler = handler
                break
        
        if error_handler:
            error = FMPRateLimitError("Rate limit exceeded")
            result = error_handler(error)
            
            assert result["error"] == "Rate limit exceeded"
            assert result["message"] == "Too many requests, please try again later"
            assert result["type"] == "rate_limit_error"
    
    def test_error_handler_response_error(self):
        """Test error handler for response errors."""
        from aiofmp.mcp_server import mcp
        
        # Mock the error handler
        error_handler = None
        for handler in mcp._error_handlers:
            if hasattr(handler, '__name__') and handler.__name__ == 'handle_error':
                error_handler = handler
                break
        
        if error_handler:
            error = FMPResponseError("API response error")
            result = error_handler(error)
            
            assert result["error"] == "API response error"
            assert result["message"] == "API response error"
            assert result["type"] == "api_error"
    
    def test_error_handler_general_error(self):
        """Test error handler for general errors."""
        from aiofmp.mcp_server import mcp
        
        # Mock the error handler
        error_handler = None
        for handler in mcp._error_handlers:
            if hasattr(handler, '__name__') and handler.__name__ == 'handle_error':
                error_handler = handler
                break
        
        if error_handler:
            error = Exception("General error")
            result = error_handler(error)
            
            assert result["error"] == "Internal server error"
            assert result["message"] == "General error"
            assert result["type"] == "internal_error"


class TestMCPServerConfiguration:
    """Test MCP server configuration."""
    
    def test_environment_variables(self):
        """Test environment variable configuration."""
        with patch.dict(os.environ, {
            'FMP_API_KEY': 'test_key',
            'MCP_TRANSPORT': 'http',
            'MCP_HOST': 'localhost',
            'MCP_PORT': '3000'
        }):
            assert os.getenv('FMP_API_KEY') == 'test_key'
            assert os.getenv('MCP_TRANSPORT') == 'http'
            assert os.getenv('MCP_HOST') == 'localhost'
            assert os.getenv('MCP_PORT') == '3000'
    
    def test_default_configuration(self):
        """Test default configuration values."""
        with patch.dict(os.environ, {}, clear=True):
            assert os.getenv('MCP_TRANSPORT', 'stdio') == 'stdio'
            assert os.getenv('MCP_HOST', 'localhost') == 'localhost'
            assert os.getenv('MCP_PORT', '3000') == '3000'
    
    def test_port_conversion(self):
        """Test port string to integer conversion."""
        with patch.dict(os.environ, {'MCP_PORT': '8080'}):
            port = int(os.getenv('MCP_PORT', '3000'))
            assert port == 8080
            assert isinstance(port, int)


if __name__ == "__main__":
    pytest.main([__file__])
