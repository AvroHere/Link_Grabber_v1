import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import tkinter as tk
from tkinter import filedialog
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Configuration
MAX_THREADS = 10  # Adjust based on your network and system capabilities
TIMEOUT = 10  # seconds for requests timeout

def get_links(url, include_filter=None, exclude_filter=None):
    """Fetch links from a webpage with optional filters."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        
        if response.status_code != 200:
            print(f"⚠️ Failed to retrieve {url} (Status code: {response.status_code})")
            return set()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        unique_links = set()
        
        for anchor in soup.find_all('a', href=True):
            full_url = urljoin(url, anchor['href'])
            
            include = True
            if include_filter and include_filter.lower() not in full_url.lower():
                include = False
            if exclude_filter and exclude_filter.lower() in full_url.lower():
                include = False
            
            if include and full_url.startswith(('http://', 'https://')):
                unique_links.add(full_url)
        
        return url, unique_links  # Return both URL and found links
    except Exception as e:
        print(f"❌ Error processing {url}: {str(e)}")
        return url, set()

def parallel_get_links(urls, include_filter=None, exclude_filter=None):
    """Process multiple URLs in parallel."""
    all_links = set()
    processed_urls = set()
    
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {
            executor.submit(get_links, url, include_filter, exclude_filter): url 
            for url in urls
        }
        
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                processed_url, links = future.result()
                processed_urls.add(processed_url)
                if links:
                    new_count = len(links)
                    existing_count = len(all_links)
                    all_links.update(links)
                    added_count = len(all_links) - existing_count
                    print(f"✅ {processed_url}: Found {new_count} links ({added_count} new)")
                else:
                    print(f"ℹ️ {processed_url}: No matching links found")
            except Exception as e:
                print(f"❌ Error processing {url}: {str(e)}")
    
    return all_links, processed_urls

def save_links(links, filename):
    """Save links to a file with the count in the filename."""
    try:
        with open(filename, 'w') as file:
            file.writelines(f"{link}\n" for link in sorted(links))
        return True
    except Exception as e:
        print(f"❌ Error saving file: {str(e)}")
        return False

def get_user_input(prompt, default=None):
    """Get user input with optional default value."""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    return input(prompt).strip()

def select_file():
    """Open a file dialog to select a file."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select a text file with URLs",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    return file_path

def manual_url_entry(include_filter, exclude_filter):
    """Handle manual URL entry one by one."""
    all_links = set()
    while True:
        print("\n" + "="*40)
        url = get_user_input("\nEnter URL to scan (or 'q' to finish):")
        
        if url.lower() == 'q':
            break
        
        print(f"\n🔍 Scanning {url}...")
        start_time = time.time()
        _, new_links = get_links(url, include_filter, exclude_filter)
        elapsed = time.time() - start_time
        
        if new_links:
            new_count = len(new_links)
            existing_count = len(all_links)
            all_links.update(new_links)
            added_count = len(all_links) - existing_count
            
            print(f"✅ Found {new_count} links ({added_count} new) in {elapsed:.2f}s")
        else:
            print(f"ℹ️ No matching links found (took {elapsed:.2f}s)")
        
        # Show summary
        if all_links:
            print(f"\n📊 Current total: {len(all_links)} unique links collected")
            continue_option = get_user_input("\nAdd another URL? (y/n)", "y")
            if continue_option.lower() != 'y':
                break
    
    return all_links

def file_url_entry(include_filter, exclude_filter):
    """Handle URL entry from file."""
    print("\nPlease select a text file containing URLs...")
    filename = select_file()
    all_links = set()
    
    if filename:
        print(f"\nSelected file: {filename}")
        urls_to_process = load_urls_from_file(filename)
        
        if not urls_to_process:
            print("ℹ️ No valid URLs found in the file")
            return all_links
            
        print(f"\n🔍 Found {len(urls_to_process)} URLs in the file. Processing in parallel...")
        start_time = time.time()
        all_links, processed_urls = parallel_get_links(urls_to_process, include_filter, exclude_filter)
        elapsed = time.time() - start_time
        
        print(f"\n⚡ Processed {len(processed_urls)} URLs in {elapsed:.2f} seconds")
        print(f"📊 Total unique links collected: {len(all_links)}")
    else:
        print("❌ No file selected")
    
    return all_links

def load_urls_from_file(filename):
    """Load URLs from a text file."""
    try:
        with open(filename, 'r') as file:
            urls = {line.strip() for line in file if line.strip()}
        return urls
    except Exception as e:
        print(f"❌ Error reading file: {str(e)}")
        return set()

def main():
    print("🌐 Link Grabber Tool 🌐")
    print("="*40)
    
    # Get initial filters
    include_filter = get_user_input("Include links containing (leave empty for all):") or None
    exclude_filter = get_user_input("Exclude links containing (leave empty for none):") or None
    
    all_links = set()
    
    print("\n" + "="*40)
    print("\nChoose input method:")
    print("1. Load URLs from a text file (parallel processing)")
    print("2. Other options")
    choice = get_user_input("Select option (1/2):", "2")
    
    if choice == "1":
        # File input mode with parallel processing
        new_links = file_url_entry(include_filter, exclude_filter)
        all_links.update(new_links)
    elif choice == "2":
        print("\nChoose input method:")
        print("1. Enter URLs one by one manually")
        print("2. Select a text file containing URLs (parallel processing)")
        sub_choice = get_user_input("Select option (1/2):", "1")
        
        if sub_choice == "1":
            new_links = manual_url_entry(include_filter, exclude_filter)
            all_links.update(new_links)
        elif sub_choice == "2":
            new_links = file_url_entry(include_filter, exclude_filter)
            all_links.update(new_links)
    
    if all_links:
        # Generate filename with count
        filename = f"{len(all_links)}_links_output.txt"
        
        # Save the file
        if save_links(all_links, filename):
            print(f"\n🎉 Success! Saved {len(all_links)} links to '{filename}'")
            print(f"📂 File location: {os.path.abspath(filename)}")
        else:
            print("\n❌ Failed to save links")
    else:
        print("\nℹ️ No links were collected")
    
    print("\nThank you for using Link Grabber! 👋")

if __name__ == "__main__":
    main()