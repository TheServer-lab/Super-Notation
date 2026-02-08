# Super Notation v1.0 - Python Interpreter

A complete implementation of the Super Notation (SN) v1.0 specification - a human-first, machine-friendly plain-text documentation format.

## Features

✨ **Complete SN v1.0 Support**
- All commands: meta, title, sec, para, lists, code blocks, images, links, navigation
- Inline formatting: bold, italic, underline, colors
- Multi-file documentation flows with `endnewsn:`
- Cryptographic signing and sealing with SHA-256

🔧 **Two Parsing Modes**
- **Lenient** (default): Unknown commands render as plain text
- **Strict**: Unknown commands cause parsing errors

🎨 **HTML Rendering**
- Beautiful, responsive HTML output
- Built-in CSS styling
- Proper escaping and security

🔐 **Document Signing**
- Sign documents with SHA-256 cryptographic signatures
- Verify document integrity
- Seal documents as read-only

## Installation

No external dependencies required - uses Python standard library only!

```bash
# Make the CLI executable
chmod +x sn.py

# Optional: Create a symlink for easier access
ln -s $(pwd)/sn.py /usr/local/bin/sn
```

## Quick Start

### Command Line Tools

### 1. Parse and validate an SN file

```bash
python sn.py parse example_basic.sn
```

### 2. Render to HTML

```bash
python sn.py render example_basic.sn
# Creates example_basic.html
```

### 3. Sign a document

```bash
python sn.py sign example_basic.sn
# Adds signature and close: marker
```

### 4. Verify signature

```bash
python sn.py verify example_basic.sn
```

### 5. Get document info

```bash
python sn.py info example_basic.sn
```

### Web Browser (NEW! 🌐)

**Interactive web-based SN viewer - no installation required!**

1. Open `sn-browser.html` in any modern web browser
2. Upload an `.sn` file or paste a URL
3. View beautifully rendered documentation instantly!

```bash
# Or try the demo page
open sn-browser-demo.html
```

Features:
- 📁 Drag & drop file upload
- 🔗 Load from URLs
- 🎨 Beautiful, responsive design
- 📱 Works on mobile
- ⚡ Zero dependencies
- 🔌 Works offline

See `SN-BROWSER-README.md` for details!

## File Structure

```
.
├── sn_parser.py          # Core parser, lexer, AST, and HTML renderer
├── sn_signing.py         # Signing and verification utilities
├── sn.py                 # Command-line interface (main tool)
├── test_sn.py            # Comprehensive test suite
├── demo.py               # Interactive demonstration
├── sn-browser.html       # Web-based SN file viewer (NEW!)
├── sn-browser-demo.html  # Demo page for the browser
├── example_basic.sn      # Basic example document
├── example_part1.sn      # Multi-file example (part 1)
├── example_part2.sn      # Multi-file example (part 2)
└── README.md             # This file
```

## Usage Examples

### Command Line Interface

```bash
# Parse with strict mode
python sn.py parse --strict document.sn

# Render with custom output
python sn.py render document.sn -o output.html

# Show detailed structure
python sn.py parse -v document.sn

# Get detailed info
python sn.py info -v document.sn

# Remove signature
python sn.py unsign document.sn
```

### Programmatic Usage

```python
from sn_parser import SNParser, HTMLRenderer, ParseMode
from sn_signing import sign_file, verify_signature

# Parse a document
parser = SNParser(mode=ParseMode.LENIENT)
with open('document.sn', 'r') as f:
    content = f.read()

doc = parser.parse(content)

# Render to HTML
renderer = HTMLRenderer()
html = renderer.render(doc)

# Sign and verify
sign_file('document.sn', in_place=True)
is_valid, message = verify_signature('document.sn')
```

## Running Tests

```bash
python test_sn.py
```

The test suite covers:
1. ✓ Basic parsing
2. ✓ HTML rendering
3. ✓ Document signing
4. ✓ Signature invalidation
5. ✓ Inline formatting
6. ✓ Strict vs lenient modes
7. ✓ Multi-file navigation

## SN Format Overview

### Basic Syntax

```
<super-notation-v1>

meta: author=Your Name
title: Document Title

sec:introduction
para: This is a paragraph with {b:bold} and {i:italic} text.

olist:bullet
First item
Second item
Third item

code:
def example():
    return "Hello, SN!"
endcode:

link: https://example.com
```

### Supported Commands

| Command | Description | Example |
|---------|-------------|---------|
| `<super-notation-v1>` | File header (required) | Must be first line |
| `meta:` | Metadata (not rendered) | `meta: author=Jane` |
| `title:` | Document title | `title: Getting Started` |
| `sec:id` | Section definition | `sec:introduction` |
| `sec=id: Text` | Section link | `sec=intro: Go to intro` |
| `para:` | Paragraph | `para: Text here` |
| `break-line` | Horizontal rule | `break-line` |
| `olist:bullet` | Unordered list | Followed by items |
| `olist:numbers` | Ordered list | Followed by items |
| `code:` / `endcode:` | Code block | Literal text |
| `img:=path \| alt` | Image | `img:=pic.png \| Photo` |
| `link:` | Simple link | `link: https://...` |
| `linktxt: text \| url` | Link with text | `linktxt: Click \| url` |
| `opensn=file: Text` | Cross-file link | Opens in SN viewer |
| `endnewsn:` | Next document | `endnewsn: part2.sn` |
| `sign:` | Signature | `sign: SHA256-ABC...` |
| `close:` | Seal marker | `close:` |

### Inline Formatting

- `{b:text}` or `{bold:text}` → **bold**
- `{i:text}` or `{italic:text}` → *italic*
- `{u:text}` → <u>underline</u>
- `{color=#hex:text}` or `{color=name:text}` → colored text
- `{{` and `}}` → literal braces

## Security Notes

- Documents are signed using SHA-256 hashes
- Signatures cover the canonicalized content (normalized line endings, BOM removed)
- Sealed documents (`close:` marker) should be treated as read-only
- HTML rendering properly escapes all content to prevent XSS
- Local file references in `img:=` and `opensn=` should be handled carefully

## Specification

This implementation follows the [Super Notation v1.0 Specification](SN-v1_0-SPEC.md).

Key specification points:
- UTF-8 encoding required
- Line endings normalized to LF for signing
- Comments start with `#`
- Flat section structure (no nesting)
- Canonicalization algorithm for reproducible signatures

## Contributing

This interpreter is designed to be:
- **Minimal**: No external dependencies
- **Clear**: Well-documented code
- **Spec-compliant**: Follows SN v1.0 exactly
- **Extensible**: Easy to add features for future versions

## License

Licensed under the Server-Lab Open-Control License (SOCL) 1.0.

## Version

Implements: **Super Notation v1.0** (2026-02-09)

---

Made with ❤️ for clear, maintainable documentation
