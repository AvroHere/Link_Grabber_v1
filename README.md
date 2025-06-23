# 1. 🏁 **Header**
🌐 **Link Grabber Pro** 🔗  
*A lightning-fast web scraper to collect links with smart filtering*

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)  
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20Mac-lightgrey)  
[![Author](https://img.shields.io/badge/Author-AvroHere-green?logo=github)](https://github.com/AvroHere)

# 2. 🧩 **Features**
✨ **Smart Filtering** - Include/exclude links containing specific keywords  
⚡ **Parallel Processing** - Scrape multiple URLs simultaneously (10 threads)  
📂 **File Input** - Process hundreds of URLs from a text file  
🕵️ **Manual Mode** - Interactive URL-by-URL scanning  
📊 **Real-time Stats** - Shows new vs. total links collected  
💾 **Auto-named Output** - Saves with link count in filename (e.g., `42_links_output.txt`)  
🛡️ **Error Resilient** - Handles failed requests gracefully  
🎯 **Precise Targeting** - URL joining ensures valid absolute links

# 3. 💾 **Installation**
```bash
# Clone the repository
git clone https://github.com/AvroHere/link-grabber.git
cd link-grabber

# Install requirements
pip install -r requirements.txt

# Run the tool
python main.py
```

# 4. 🧠 **Usage**
1️⃣ **Choose Filters**  
   - Set include/exclude keywords (e.g., ".pdf" or "archive")  
   
2️⃣ **Select Input Method**  
   - 📄 File mode (parallel processing)  
   - ✍️ Manual entry (URL-by-URL)  

3️⃣ **Let It Scan**  
   - Watch real-time progress with emoji indicators  

4️⃣ **Get Results**  
   - Auto-saved with count (e.g., `127_links_output.txt`)


# 5. 📁 **Folder Structure
```bash
link-grabber/
├── LICENSE.txt       # MIT License
├── README.md         # This documentation
├── main.py           # Main script (40KB)
└── requirements.txt  # Dependencies (see below)
```

# 6. 🛠 **Built With**
🔹 **External Libraries**  
- `requests` - HTTP requests  
- `beautifulsoup4` - HTML parsing  
- `concurrent.futures` - Parallel processing  
- `tkinter` - File dialog GUI  

🔹 **Standard Library**  
- `urllib.parse` - URL handling  
- `os` - File operations  
- `time` - Performance tracking

# 7. 🚧 **Roadmap**
- [ ] Add depth control for recursive scraping  
- [ ] Export to CSV/JSON formats  
- [ ] GUI interface with progress bars  
- [ ] Cloud integration (Save to Google Drive)  
- [ ] Docker containerization  
- [ ] Rate limiting configuration

# 8. ❓ **FAQ**
**Q: Why are some links missing?**  
A: The tool skips non-HTTP(S) links and respects your include/exclude filters. Check your filters and the source webpage.

**Q: Can I increase thread count?**  
A: Yes! Modify `MAX_THREADS` in main.py (balance speed vs. server load).


# 9. 📄 **License**
MIT License  
Copyright (c) 2025 AvroHere  

Permission is hereby granted... [Full text in LICENSE.txt]


# 10. 👨‍💻 **Author**
**Avro**  
[GitHub](https://github.com/AvroHere) 

💡 *"Debugging is like being a detective in a crime movie where you're also the murderer."*  

⭐ **If this tool saved you time, consider starring the repo!**

