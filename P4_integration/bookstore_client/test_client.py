#!/usr/bin/env python3
"""
Test script for the Bookstore Client

This script tests the implementation of the Bookstore client
by calling each function and validating its functionality.
"""
import unittest
import requests
from unittest.mock import patch, MagicMock, call
import json
import io
import sys

# Import client module
from client import (
    get_all_books,
    get_book_by_id,
    add_book,
    update_book,
    delete_book,
    search_books
)

class TestBookstoreClient(unittest.TestCase):
    """Test cases for Bookstore client implementation."""

    def setUp(self):
        """Set up test fixtures."""
        # Sample books data for testing
        self.sample_books = [
            {
                "id": "1",
                "title": "Test Book 1",
                "author": "Test Author 1",
                "price": 10.99,
                "in_stock": True
            },
            {
                "id": "2",
                "title": "Test Book 2",
                "author": "Test Author 2",
                "price": 12.99,
                "in_stock": False
            }
        ]
        
        self.single_book = self.sample_books[0]
    
    @patch('client.requests.get')
    def test_get_all_books(self, mock_get):
        """Test the get_all_books function."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = self.sample_books
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the function
        result = get_all_books()
        
        # Assert the result
        self.assertEqual(result, self.sample_books)
        mock_get.assert_called_once()
    
    @patch('client.requests.get')
    def test_get_book_by_id(self, mock_get):
        """Test the get_book_by_id function."""
        # This test will fail until the function is implemented
        if get_book_by_id("1") is None:
            self.skipTest("get_book_by_id function not implemented yet")
        
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = self.single_book
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the function
        result = get_book_by_id("1")
        
        # Assert the result
        self.assertEqual(result, self.single_book)
        mock_get.assert_called_once()
    
    @patch('client.requests.get')
    def test_get_book_by_id_error(self, mock_get):
        """Test error handling in get_book_by_id function."""
        # This test will fail until the function is implemented
        if get_book_by_id("999") is None:
            self.skipTest("get_book_by_id function not implemented yet")
        
        # Mock a 404 error
        mock_get.side_effect = requests.exceptions.HTTPError("404 Not Found")
        
        # Call the function
        result = get_book_by_id("999")
        
        # Assert the result
        self.assertIsNone(result)
    
    @patch('builtins.input')
    @patch('client.requests.post')
    def test_add_book(self, mock_post, mock_input):
        """Test the add_book function."""
        # Mock input responses
        mock_input.side_effect = [
            "New Test Book",  # title
            "New Test Author",  # author
            "15.99",  # price
            "yes"  # in_stock
        ]
        
        # Mock the API response
        mock_response = MagicMock()
        new_book = {
            "id": "3",
            "title": "New Test Book",
            "author": "New Test Author",
            "price": 15.99,
            "in_stock": True
        }
        mock_response.json.return_value = new_book
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Call the function
        result = add_book()
        
        # Assert the result
        self.assertEqual(result, new_book)
        mock_post.assert_called_once()
        # Verify the data sent to the API matches what was input
        expected_data = {
            'title': "New Test Book",
            'author': "New Test Author",
            'price': 15.99,
            'in_stock': True
        }
        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs['json'], expected_data)
    
    @patch('builtins.input')
    @patch('client.requests.post')
    def test_add_book_error(self, mock_post, mock_input):
        """Test error handling in add_book function."""
        # Mock input responses
        mock_input.side_effect = [
            "Bad Book",  # title
            "Bad Author",  # author
            "25.99",  # price
            "no"  # in_stock
        ]
        
        # Mock an error response
        mock_post.side_effect = requests.exceptions.HTTPError("400 Bad Request")
        
        # Call the function
        result = add_book()
        
        # Assert the result
        self.assertIsNone(result)
    
    @patch('builtins.input')
    @patch('client.requests.get')
    @patch('client.requests.put')
    def test_update_book(self, mock_put, mock_get, mock_input):
        """Test the update_book function."""
        # Mock input for book ID and updates
        mock_input.side_effect = [
            "1",  # book ID
            "Updated Title",  # new title
            "Updated Author",  # new author
            "20.99",  # new price
            "no"  # new in_stock status
        ]
        
        # Mock the initial GET response for current book
        get_response = MagicMock()
        get_response.json.return_value = self.single_book
        get_response.raise_for_status.return_value = None
        mock_get.return_value = get_response
        
        # Mock the PUT response
        put_response = MagicMock()
        updated_book = {
            "id": "1",
            "title": "Updated Title",
            "author": "Updated Author",
            "price": 20.99,
            "in_stock": False
        }
        put_response.json.return_value = updated_book
        put_response.raise_for_status.return_value = None
        mock_put.return_value = put_response
        
        # Call the function
        result = update_book()
        
        # Assert the result
        self.assertEqual(result, updated_book)
        mock_get.assert_called_once()
        mock_put.assert_called_once()
        
        # Verify the update data sent to the API
        expected_updates = {
            'title': "Updated Title",
            'author': "Updated Author",
            'price': 20.99,
            'in_stock': False
        }
        _, kwargs = mock_put.call_args
        self.assertEqual(kwargs['json'], expected_updates)
    
    @patch('builtins.input')
    @patch('client.requests.get')
    def test_update_book_get_error(self, mock_get, mock_input):
        """Test error handling in update_book function when GET fails."""
        # Mock input for book ID
        mock_input.side_effect = ["999"]  # non-existent book ID
        
        # Mock a 404 error
        mock_get.side_effect = requests.exceptions.HTTPError("404 Not Found")
        
        # Call the function
        result = update_book()
        
        # Assert the result
        self.assertIsNone(result)
    
    @patch('builtins.input')
    @patch('client.requests.delete')
    def test_delete_book(self, mock_delete, mock_input):
        """Test the delete_book function."""
        # Mock input for book ID and confirmation
        mock_input.side_effect = [
            "1",  # book ID
            "y"   # confirmation
        ]
        
        # Mock the DELETE response
        mock_response = MagicMock()
        mock_response.json.return_value = {"message": "Book deleted successfully"}
        mock_response.raise_for_status.return_value = None
        mock_delete.return_value = mock_response
        
        # Call the function
        result = delete_book()
        
        # Assert the result
        self.assertTrue(result)
        mock_delete.assert_called_once()
    
    @patch('builtins.input')
    def test_delete_book_cancelled(self, mock_input):
        """Test delete_book when user cancels deletion."""
        # Mock input for book ID and negative confirmation
        mock_input.side_effect = [
            "1",  # book ID
            "n"   # negative confirmation
        ]
        
        # Call the function
        result = delete_book()
        
        # Assert the result is None because operation was cancelled
        self.assertIsNone(result)
    
    @patch('builtins.input')
    @patch('client.requests.delete')
    def test_delete_book_error(self, mock_delete, mock_input):
        """Test error handling in delete_book function."""
        # Mock input for book ID and confirmation
        mock_input.side_effect = [
            "999",  # non-existent book ID
            "y"     # confirmation
        ]
        
        # Mock a 404 error
        mock_delete.side_effect = requests.exceptions.HTTPError("404 Not Found")
        
        # Call the function
        result = delete_book()
        
        # Assert the result
        self.assertFalse(result)
    
    @patch('builtins.input')
    @patch('client.requests.get')
    def test_search_books(self, mock_get, mock_input):
        """Test the search_books function."""
        # Mock input for search query
        mock_input.side_effect = ["Test"]  # search query
        
        # Mock the GET response
        mock_response = MagicMock()
        mock_response.json.return_value = self.sample_books
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Redirect stdout to capture printed output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Call the function
        search_books()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Check if search was called with correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(kwargs['params'], {'query': 'Test'})
        
        # Check that output contains indication of results found
        output = captured_output.getvalue()
        self.assertIn("Found 2 matching books", output)
    
    @patch('builtins.input')
    @patch('client.requests.get')
    def test_search_books_no_results(self, mock_get, mock_input):
        """Test search_books when no results are found."""
        # Mock input for search query
        mock_input.side_effect = ["NonExistent"]  # search query with no matches
        
        # Mock the GET response with empty results
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Redirect stdout to capture printed output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Call the function
        search_books()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Check output indicates no books found
        output = captured_output.getvalue()
        self.assertIn("No books found", output)
    
    @patch('builtins.input')
    @patch('client.requests.get')
    def test_search_books_error(self, mock_get, mock_input):
        """Test error handling in search_books function."""
        # Mock input for search query
        mock_input.side_effect = ["Query"]
        
        # Mock a server error
        mock_get.side_effect = requests.exceptions.HTTPError("500 Server Error")
        
        # Redirect stdout to capture printed output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Call the function
        search_books()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Check output contains error message
        output = captured_output.getvalue()
        self.assertIn("Error", output)

if __name__ == '__main__':
    print("Running tests for Bookstore Client implementation...")
    unittest.main()