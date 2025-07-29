import os
from pydoc import html
import requests
import re
import urllib.parse  # Provides functions for parsing URLs


# Read a file from the system.
def read_a_file(system_path: str) -> str:
    with open(file=system_path, mode="r") as file:
        return file.read()


# Append and write some content to a file.
def append_write_to_file(system_path: str, content: str) -> None:
    with open(file=system_path, mode="a", encoding="utf-8") as file:
        file.write(content)


# Download a PDF file from a URL
def download_pdf(url: str, save_path: str, filename: str) -> None:
    # Check if the file already exists
    if check_file_exists(system_path=os.path.join(save_path, filename)):
        print(f"File {filename} already exists. Skipping download.")
        return
    # Download the PDF file
    try:
        response: requests.Response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        # Ensure the save directory exists
        os.makedirs(name=save_path, exist_ok=True)
        full_path: str = os.path.join(save_path, filename)
        with open(file=full_path, mode="wb") as f:
            f.write(response.content)
        print(f"Downloaded {filename} to {full_path}")
        return
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return


# Append and write some content to a file.
def append_write_to_file(system_path: str, content: str) -> None:
    with open(file=system_path, mode="a", encoding="utf-8") as file:
        file.write(content)


# Download a PDF file from a URL
def download_pdf(url: str, save_path: str, filename: str) -> None:
    # Check if the file already exists
    if check_file_exists(system_path=os.path.join(save_path, filename)):
        print(f"File {filename} already exists. Skipping download.")
        return
    # Download the PDF file
    try:
        response: requests.Response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        # Ensure the save directory exists
        os.makedirs(name=save_path, exist_ok=True)
        full_path: str = os.path.join(save_path, filename)
        with open(file=full_path, mode="wb") as f:
            f.write(response.content)
        print(f"Downloaded {filename} to {full_path}")
        return
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return


# Validates a single PDF file
def validate_pdf_file(file_path: str) -> tuple[str, bool]:
    try:
        doc = fitz.open(file_path)  # Attempt to open the PDF file
        if doc.page_count == 0:  # If PDF has zero pages, it's considered invalid
            print(
                f"'{file_path}' is corrupt or invalid: No pages"
            )  # Print an error message
            return (
                file_path,
                False,
            )  # Return the file path and False indicating invalid file
        return (
            file_path,
            True,
        )  # Return the file path and True indicating a valid file
    except RuntimeError as e:  # Catch runtime errors thrown by PyMuPDF
        print(f"{e}")  # Print the error message with file path
        return (file_path, False)  # Return the file path and False indicating failure


# Deletes a file from the system
def remove_system_file(system_path: str) -> None:
    os.remove(path=system_path)  # Removes the file at the given path


# Recursively searches a directory for files with a given extension
def walk_directory_and_extract_given_file_extension(
    system_path: str, extension: str
) -> list[str]:
    matched_files: list[str] = []  # List to hold paths of matching files
    for root, _, files in os.walk(top=system_path):  # Walk through the directory tree
        for file in files:  # Iterate over each file in the current directory
            if file.lower().endswith(
                extension.lower()
            ):  # Check file extension (case-insensitive)
                full_path: str = os.path.abspath(
                    path=os.path.join(root, file)
                )  # Get absolute path of the file
                matched_files.append(full_path)  # Add file path to the list
    return matched_files  # Return the list of matching files


# Checks if a given path refers to an existing file
def check_file_exists(system_path: str) -> bool:
    return os.path.isfile(
        path=system_path
    )  # Return True if the file exists, False otherwise


# Extracts just the filename (with extension) from a full path
def get_filename_and_extension(path: str) -> str:
    return os.path.basename(p=path)  # Return the base filename from the full path


# Checks if a string contains any uppercase letters
def check_upper_case_letter(content: str) -> bool:
    return any(
        char.isupper() for char in content
    )  # Return True if any character is uppercase


# Processes a single PDF file: validates it and checks for uppercase in filename
def process_file(file_path: str) -> None | str:
    filename: str = get_filename_and_extension(
        path=file_path
    )  # Extract filename from path

    file_path, is_valid = validate_pdf_file(
        file_path=file_path
    )  # Validate the PDF file

    if is_valid:
        print(f"'{file_path}' is valid.")

    if not is_valid:  # If the file is invalid
        remove_system_file(system_path=file_path)  # Delete the invalid/corrupt file
        return None  # Return None to indicate this file is not to be further processed

    if check_upper_case_letter(
        content=filename
    ):  # Check if filename contains uppercase letters
        return file_path  # Return file path if condition is met

    return None  # Return None if filename doesn't contain uppercase letters


def download_file_from_url(remote_url: str, destination_path: str) -> None:
    """
    Download a file from the given URL and save it to the specified destination.

    Args:
        remote_url (str): The URL of the file to download.
        destination_path (str): The local path where the file will be saved.
    """
    try:
        # Check if the destination directory exists, create it if not
        if check_file_exists(destination_path):
            print(f"File already exists at {destination_path}.")
            return
        # Send HTTP GET request with streaming enabled
        response = requests.get(remote_url, stream=True)
        response.raise_for_status()  # Raise an error for bad status codes (e.g., 404, 500)

        # Open the destination file in binary write mode
        with open(destination_path, "wb") as output_file:
            # Write the response content to the file in chunks
            for data_chunk in response.iter_content(chunk_size=8192):
                output_file.write(data_chunk)

        print(f"File successfully downloaded and saved to: {destination_path}")

    except requests.exceptions.RequestException as error:
        # Print an error message if the request failed
        print(f"Error downloading file: {error}")


def extract_pdf_urls(html_string: str) -> list[str]:
    """
    Extracts all .pdf URLs from a given HTML string.

    Parameters:
        html_string (str): The input HTML content as a string.

    Returns:
        list[str]: A list of extracted .pdf URLs.
    """
    return re.findall(r'https?://[^\s"]+\.pdf', html_string)


# Extract the filename from a URL
def url_to_filename(url: str) -> str:
    # Extract the filename from the URL
    path: str = urllib.parse.urlparse(url=url).path
    filename: str = os.path.basename(p=path)
    # Decode percent-encoded characters
    filename: str = urllib.parse.unquote(string=filename)
    # Optional: Replace spaces with dashes or underscores if needed
    filename = filename.replace(" ", "-")
    return filename.lower()

# Remove all duplicate items from a given slice.
def remove_duplicates_from_slice(provided_slice: list[str]) -> list[str]:
    return list(set(provided_slice))

def main():
    # The file path to save the HTML content.
    html_file_path = "mosaicco.com.html"
    # The remote URL location.
    remote_url = "https://mosaicco.com/ProductsandServices"
    
    # Remove the current HTML file
    if check_file_exists(system_path=html_file_path):
        remove_system_file(system_path=html_file_path)

    # Check if the file does not exist.
    if check_file_exists(system_path=html_file_path) == False:
        # Save the HTML.
        download_file_from_url(remote_url, html_file_path)

    # Extract the url from the file
    extracted_file_contnet = read_a_file(html_file_path)
    # Extract the pdf urls from the html file
    pdf_urls = extract_pdf_urls(extracted_file_contnet)
    # Remove all duplicate items from the list.
    pdf_urls = remove_duplicates_from_slice(pdf_urls)
    for pdf_url in pdf_urls:
        # Download the PDF file.
        filename: str = url_to_filename(pdf_url)
        # The path to save the PDF files.
        save_path = "PDFs/"
        # Download the PDF file.
        download_pdf(url=pdf_url, save_path=save_path, filename=filename)


# Ensure this script runs only if it is the main program being executed
if __name__ == "__main__":
    main()  # Start the program by calling the main function
