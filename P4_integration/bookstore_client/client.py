#!/usr/bin/env python3
"""
Bookstore Client

A client application for interacting with the Bookstore API.
This client is intentionally incomplete and contains TODOs for implementation.
"""
import requests
import json
from tabulate import tabulate
import sys
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Constants
API_BASE_URL = "http://localhost:5000/api"
BOOKS_ENDPOINT = f"{API_BASE_URL}/books"
#need to change my endpoints urls to use this
#f"{BOOKS_ENDPOINT}/{query}"

# Helper functions for formatting output
def print_success(message):
    """Print a success message in green."""
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

def print_error(message):
    """Print an error message in red."""
    print(f"{Fore.RED}Error: {message}{Style.RESET_ALL}")

def print_info(message):
    """Print an info message in blue."""
    print(f"{Fore.BLUE}{message}{Style.RESET_ALL}")

def format_book_table(books):
    """Format a list of books as a table."""
    if not books:
        return "No books found."
    
    # Convert single book to list if needed
    if isinstance(books, dict):
        books = [books]
    
    headers = ["ID", "Title", "Author", "Price", "In Stock"]
    rows = [
        [
            book.get("id", "N/A"),
            book.get("title", "N/A"),
            book.get("author", "N/A"),
            f"${book.get('price', 0):.2f}",
            "Yes" if book.get("in_stock", False) else "No"
        ]
        for book in books
    ]
    
    return tabulate(rows, headers=headers, tablefmt="grid")

# API client functions

def get_all_books():
    """Retrieve all books from the API."""
    try:
        response = requests.get(BOOKS_ENDPOINT)
        response.raise_for_status()
        books = response.json()
        return books
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to retrieve books: {e}")
        return []

def display_all_books():
    """Display all books in a formatted table."""
    print_info("Fetching all books...")
    books = get_all_books()
    print(format_book_table(books))

# TODO: Implement the get_book_by_id function
def get_book_by_id(book_id):
    """
    Retrieve a specific book by ID.
    
    Parameters:
        book_id (str): The ID of the book to retrieve
        
    Returns:
        dict: The book data if found, None otherwise
    """
    # TODO: Implement this function
    # 1. Send a GET request to the appropriate endpoint
    # 2. Handle any errors that might occur
    # 3. Return the book data if successful
    # API endpoint
    #url = f"{BOOKS_ENDPOINT}/{book_id}"

    #Intiate the GET request with error handling
    try:
        response = requests.get(f"{BOOKS_ENDPOINT}/{book_id}",timeout = 5)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as err:
        
        if response.status_code == 404:
            return {
                'error': f"Book with ID '{book_id}' not found",
                'status_code': 404
            }
        return {
            'error': f"Server returned {response.status_code} error",
            'status_code': response.status_code
        }
        
    except requests.exceptions.ConnectionError:
        return {
            'error': "Could not connect to the server",
            'status_code': None
        }
        
    except requests.exceptions.Timeout:
        return {
            'error': "Request timed out (5 seconds)",
            'status_code': None
        }
        
    except requests.exceptions.RequestException as err:
        return {
            'error': f"Request failed: {str(err)}",
            'status_code': None
        }
        
    except ValueError:  # Invalid JSON
        return {
            'error': "Received invalid response from server",
            'status_code': None
        }
    

def display_book_details():
    """Display details for a specific book."""
    #book_id = input("Enter book ID: ")
    while True:
        book_id = input("Enter book ID: ").strip()
        if book_id:
            break
        print("Book Id cannot be empty")
    
    # TODO: Implement this functionality
    # 1. Call get_book_by_id function
    # 2. Display the book details or error message
    #print_error("This functionality is not implemented yet.")
    response_book = get_book_by_id(book_id)

    if isinstance(response_book, dict) and 'title' in response_book:#check if actual boo details are returned otherwise error message
       print(format_book_table(response_book))
    else:
        print(response_book)
   
    

# TODO: Implement the add_book function
def add_book():
    """
    Add a new book to the bookstore.
    
    Gather book details from the user and send them to the API.
    """
    # TODO: Implement this function
    # 1. Gather book information from the user (title, author, price, in_stock)
    # 2. Validate the inputs
    # 3. Send a POST request to the appropriate endpoint
    # 4. Handle any errors and display appropriate messages
    #print_error("This functionality is not implemented yet.")
    #title = input("Enter the book Title:")
    #author = input("Enter the book's author:")
    # Get and validate book title
    while True:
        title = input("Enter the book title: ").strip()
        if title:
            break
        print("Error: Book Title cannot be empty\n")

    # Get and validate book author
    while True:
        author = input("Enter the book's author: ").strip()
        if author:
            break
        print("Error: Book Author cannot be empty\n")

    # Validate and convert price
    try:
        price = float(input("Enter the book's price: "))
    except ValueError:
        print("Error: Price must be a valid number")
        return

    # Validate stock status
    stock_input = input("Enter the stock status of the book (True/False): ").lower()
    in_stock = stock_input in ['true', 't', '1', 'yes']

    # Prepare API data
    data = {
        'title': title,
        'author': author,
        'price': price,
        'in_stock': in_stock  # Match the API's expected field name
    }


    try:
        # Send POST request with JSON data
        response = requests.post(
            BOOKS_ENDPOINT,
            json=data,  # Automatically sets Content-Type to application/json
            timeout=10  # 10-second timeout
        )
        
        # Check for HTTP errors
        response.raise_for_status()
        
        # Process successful response
        result = response.json()
        print(f"Successfully added book with ID: {result.get('id')}")
        return result

    except requests.exceptions.HTTPError as err:
        error_msg = f"Server Error ({response.status_code})"
        if response.status_code == 400:
            error_details = response.json().get('error', 'Invalid request format')
            print(f"{error_msg}: {error_details}")
        else:
            print(f"{error_msg}: {err}")
        return None

    except requests.exceptions.ConnectionError:
        print("Error: Failed to connect to the server. Check if it's running.")
        return None

    except requests.exceptions.Timeout:
        print("Error: Request timed out. Server took too long to respond.")
        return None

    except requests.exceptions.RequestException as err:
        print(f"Network Error: {err}")
        return None

    except ValueError:  # Invalid JSON response
        print("Error: Received invalid response from server")
        return None




# TODO: Implement the update_book function
def update_book():
    """
    Update an existing book's information.
    
    Retrieve the current book information and allow the user to modify it.
    """
    # TODO: Implement this function
    # 1. Ask for the book ID to update
    # 2. Fetch the current book information
    # 3. Allow the user to update each field (or keep existing values)
    # 4. Send a PUT request to the appropriate endpoint
    # 5. Handle any errors and display appropriate messages
    #print_error("This functionality is not implemented yet.")
    # Get and validate book ID
    while True:
        book_id = input("Enter the book ID to delete: ").strip()
        if book_id:
            break
        print("Error: Book ID cannot be empty\n")

    # First get existing book data
    try:
        response = requests.get(f"{BOOKS_ENDPOINT}/{book_id}", timeout=5)
        response.raise_for_status()
        current_book = response.json()
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print(f"Error: Book with ID '{book_id}' not found")
        else:
            print(f"Failed to fetch book: {err}")
        return
    except requests.exceptions.RequestException as err:
        print(f"Network error fetching book: {err}")
        return

    # Display current values and get updates
    print("\nCurrent values (press Enter to keep):")
    updates = {}
    
    # Title
    new_title = input(f"Title [{current_book['title']}]: ").strip()
    updates['title'] = new_title if new_title else current_book['title']
    
    # Author
    new_author = input(f"Author [{current_book['author']}]: ").strip()
    updates['author'] = new_author if new_author else current_book['author']
    
    # Price
    while True:
        price_input = input(f"Price [${current_book['price']}]: ").strip()
        if not price_input:
            updates['price'] = current_book['price']
            break
        try:
            updates['price'] = float(price_input)
            break
        except ValueError:
            print("Invalid price - must be a number (e.g. 29.99)")
    
    # Stock status
    stock_map = {True: 'yes', False: 'no'}
    current_stock = stock_map[current_book['in_stock']]
    stock_input = input(f"In stock? (yes/no) [{current_stock}]: ").strip().lower()
    updates['in_stock'] = stock_input in ['y', 'yes', 'true', '1'] if stock_input else current_book['in_stock']

    # Send update
    #url = f"http://localhost:5000/api/books/{book_id}"
    
    try:
        response = requests.put(
            f"{BOOKS_ENDPOINT}/{book_id}",
            json=updates,  # Send as JSON body
            timeout=10  # Longer timeout for update operation
        )
        response.raise_for_status()
        
        updated_book = response.json()
        print(f"\nSuccessfully updated book {book_id}:")
        print(f"New title: {updated_book['title']}")
        print(f"New author: {updated_book['author']}")
        print(f"New price: ${updated_book['price']:.2f}")
        print(f"Stock status: {'In stock' if updated_book['in_stock'] else 'Out of stock'}")
        return updated_book

    except requests.exceptions.HTTPError as err:
        if response.status_code == 400:
            error = response.json().get('error', 'Invalid request')
            print(f"Validation error: {error}")
        else:
            print(f"Server error: {err}")
        return None
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server")
        return None
        
    except requests.exceptions.Timeout:
        print("Error: Update timed out - try again later")
        return None
        
    except requests.exceptions.RequestException as err:
        print(f"Network error: {err}")
        return None
        
    except ValueError:
        print("Error: Received invalid response from server")
        return None

# TODO: Implement the delete_book function
def delete_book():
    """
    Delete a book from the bookstore.
    
    Ask for confirmation before deleting.
    """
    # TODO: Implement this function
    # 1. Ask for the book ID to delete
    # 2. Ask for confirmation (y/n)
    # 3. Send a DELETE request to the appropriate endpoint
    # 4. Handle any errors and display appropriate messages
    #print_error("This functionality is not implemented yet.")
    """Delete a book from the bookstore with confirmation"""
    #base_url = "http://localhost:5000"
    
    # Get and validate book ID
    while True:
        book_id = input("Enter the book ID to delete: ").strip()
        if book_id:
            break
        print("Error: Book ID cannot be empty\n")

    # Get confirmation
    confirm = input(f"Are you sure you want to delete book {book_id}? (y/n): ").lower()
    if confirm not in ['y', 'yes']:
        print("Deletion cancelled.")
        return

    #url = f"{base_url}/api/books/{book_id}"
    
    try:
        response = requests.delete(f"{BOOKS_ENDPOINT}/{book_id}", timeout=5)
        response.raise_for_status()
        
        result = response.json()
        print(f"\nSuccess: {result.get('message', 'Book deleted successfully')}")
        return True

    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            error_msg = response.json().get('description', 'Book not found')
            print(f"\nError: {error_msg}")
        else:
            print(f"\nHTTP Error ({response.status_code}): {err}")
        return False

    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to server. Check if it's running.")
        return False

    except requests.exceptions.Timeout:
        print("\nError: Delete operation timed out. Try again later.")
        return False

    except requests.exceptions.RequestException as err:
        print(f"\nNetwork Error: {err}")
        return False

    except ValueError:
        print("\nError: Received invalid response from server")
        return False


# TODO: Implement the search_books function
def search_books():
    """
    Search for books by title or author.
    
    Send a search query to the API and display the results.
    """
    # TODO: Implement this function
    # 1. Ask for the search query
    # 2. Validate the query (not empty)
    # 3. Send a GET request to the search endpoint with the query as a parameter
    # 4. Handle any errors and display appropriate messages or search results
    #print_error("This functionality is not implemented yet.")
    """Search books through the API endpoint"""
    #base_url = "http://localhost:5000"
    #url = f"{base_url}/api/books/search"

    # Get and validate search query
    while True:
        query = input("Enter search query (title or author): ").strip()
        if query:
            break
        print("Error: Search query cannot be empty\n")

    try:
        # Send search request
        response = requests.get(
            f"{BOOKS_ENDPOINT}/search",
            params={'query': query},
            timeout=5
        )
        response.raise_for_status()

        results = response.json()

        if not results:
            print("\nNo books found matching your search")
            return

        # Display results
        print(f"\nFound {len(results)} matching {'book' if len(results) == 1 else 'books'}:")
        for i, book in enumerate(results, 1):
            stock_status = "In stock" if book['in_stock'] else "Out of stock"
            print(f"{i}. {book['title']}")
            print(f"   Author: {book['author']}")
            print(f"   Price: ${book['price']:.2f}")
            print(f"   Status: {stock_status}\n")

    except requests.exceptions.HTTPError as err:
        if response.status_code == 400:
            try:
                error_data = response.json()
                print(f"\nError: {error_data.get('description', 'Invalid search request')}")
            except ValueError:
                print(f"\nError: {response.text}")
        else:
            print(f"\nHTTP Error ({response.status_code}): {err}")

    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the server. Check if it's running.")

    except requests.exceptions.Timeout:
        print("\nError: Search timed out. Please try again later.")

    except requests.exceptions.RequestException as err:
        print(f"\nNetwork Error: {err}")

    except ValueError:
        print("\nError: Received invalid response format from server")


def display_menu():
    """Display the main menu options."""
    print("\n" + "=" * 50)
    print("             BOOKSTORE CLIENT              ")
    print("=" * 50)
    print("1. View All Books")
    print("2. View Book Details")
    print("3. Add New Book")
    print("4. Update Book")
    print("5. Delete Book")
    print("6. Search Books")
    print("7. Exit")
    print("=" * 50)

def main():
    """Main application function."""
    try:
        while True:
            display_menu()
            choice = input("Enter your choice (1-7): ")
            
            if choice == "1":
                display_all_books()
            elif choice == "2":
                display_book_details()
            elif choice == "3":
                add_book()
            elif choice == "4":
                update_book()
            elif choice == "5":
                delete_book()
            elif choice == "6":
                search_books()
            elif choice == "7":
                print_info("Exiting Bookstore Client. Goodbye!")
                break
            else:
                print_error("Invalid choice. Please enter a number between 1 and 7.")
            
            input("\nPress Enter to continue...")
            
    except KeyboardInterrupt:
        print_info("\nApplication terminated by user.")
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 