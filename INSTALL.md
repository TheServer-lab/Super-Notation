# Super Notation v1.0 Interpreter - Installation & Usage

## 📦 What You Have

A complete Python interpreter for Super Notation v1.0 with:

- **Parser** (`sn_parser.py`) - Lexer, AST builder, HTML renderer
- **Signing** (`sn_signing.py`) - Cryptographic signing & verification
- **CLI Tool** (`sn.py`) - Command-line interface
- **Tests** (`test_sn.py`) - Comprehensive test suite
- **Demo** (`demo.py`) - Interactive demonstration
- **Examples** (`example_*.sn`) - Sample documents

## 🚀 Quick Installation

### Option 1: Direct Usage
```bash
# No installation needed! Just run:
python sn.py --help
```

### Option 2: Make it a System Command
```bash
# Make executable
chmod +x sn.py

# Create symlink (optional - requires sudo)
sudo ln -s $(pwd)/sn.py /usr/local/bin/sn

# Now you can use:
sn --help
```

### Option 3: Add to PATH
```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
export PATH="$PATH:/path/to/sn-interpreter"

# Reload shell
source ~/.bashrc  # or ~/.zshrc
```

## 🎯 Quick Commands

### Parse and Validate
```bash
python sn.py parse document.sn
python sn.py parse --strict document.sn  # Strict mode
```

### Render to HTML
```bash
python sn.py render document.sn
python sn.py render document.sn -o output.html
```

### Sign a Document
```bash
python sn.py sign document.sn
```

### Verify Signature
```bash
python sn.py verify document.sn
```

### Get Document Info
```bash
python sn.py info document.sn
python sn.py info -v document.sn  # Verbose
```

### Remove Signature
```bash
python sn.py unsign document.sn
```

## 🧪 Testing

### Run the Full Test Suite
```bash
python test_sn.py
```

Expected output: `7/7 tests passed 🎉`

### Run Interactive Demo
```bash
python demo.py
```

## 📝 Creating Your First Document

1. **Create `hello.sn`:**
```
<super-notation-v1>

meta: author=Your Name
title: My First Document

sec:introduction
para: Hello, {b:Super Notation}!

para: This is a simple document with some {i:formatting}.

code:
# Example code
print("Hello, World!")
endcode:
```

2. **Render it:**
```bash
python sn.py render hello.sn
```

3. **Open `hello.html` in your browser!**

## 📚 Example Workflow

### 1. Technical Documentation
```bash
# Write your documentation in .sn format
vim api-docs.sn

# Validate
python sn.py parse api-docs.sn

# Render to HTML
python sn.py render api-docs.sn

# Sign for official release
python sn.py sign api-docs.sn

# Verify before distribution
python sn.py verify api-docs.sn
```

### 2. Multi-Part Tutorial
```bash
# Create linked documents
echo "endnewsn: part2.sn" >> part1.sn

# Render all parts
for file in part*.sn; do
    python sn.py render "$file"
done
```

### 3. Batch Processing
```bash
# Render all .sn files in a directory
for file in *.sn; do
    python sn.py render "$file"
    echo "Rendered $file"
done
```

## 🔧 Programmatic Usage

### Python API Example
```python
from sn_parser import SNParser, HTMLRenderer, ParseMode
from sn_signing import sign_file, verify_signature

# Parse a document
parser = SNParser(mode=ParseMode.LENIENT)
with open('document.sn', 'r') as f:
    doc = parser.parse(f.read())

# Render to HTML
renderer = HTMLRenderer()
html = renderer.render(doc)

# Save HTML
with open('output.html', 'w') as f:
    f.write(html)

# Sign document
signature = sign_file('document.sn', in_place=True)
print(f"Signed with: {signature}")

# Verify
is_valid, message = verify_signature('document.sn')
if is_valid:
    print("✓ Valid signature")
else:
    print("✗ Invalid signature")
```

## 🎨 Supported Features

### Commands
- ✅ `meta:` - Metadata
- ✅ `title:` - Document title
- ✅ `sec:id` - Section definitions
- ✅ `sec=id: Text` - Section links
- ✅ `para:` - Paragraphs
- ✅ `break-line` - Horizontal rules
- ✅ `olist:bullet` / `olist:numbers` - Lists
- ✅ `code:` / `endcode:` - Code blocks
- ✅ `img:=path | alt` - Images
- ✅ `link:` - Links
- ✅ `linktxt:` - Links with custom text
- ✅ `opensn=` - Cross-file navigation
- ✅ `endnewsn:` - Next document
- ✅ `sign:` / `close:` - Signatures

### Inline Formatting
- ✅ `{b:text}` - Bold
- ✅ `{i:text}` - Italic
- ✅ `{u:text}` - Underline
- ✅ `{color=#hex:text}` - Colors
- ✅ `{{` and `}}` - Escaped braces

### Modes
- ✅ Lenient mode (default) - Unknown commands render as text
- ✅ Strict mode - Unknown commands cause errors

## 🔒 Security Features

- SHA-256 cryptographic signatures
- Document sealing with `close:` marker
- Tamper detection
- Canonicalization algorithm for reproducible signatures
- HTML escaping to prevent XSS

## 📖 Documentation

- `README.md` - Complete documentation
- `QUICKSTART.md` - Quick reference
- `SN-v1_0-SPEC.md` - Official specification (uploaded by you)

## 🐛 Troubleshooting

### "No such file or directory"
Make sure you're in the correct directory:
```bash
cd /path/to/sn-interpreter
ls  # Should show sn.py, sn_parser.py, etc.
```

### "Permission denied"
Make scripts executable:
```bash
chmod +x *.py
```

### "Import error"
Make sure all three core files are in the same directory:
- `sn_parser.py`
- `sn_signing.py`
- `sn.py`

## 🎓 Learning Path

1. **Start**: Read `QUICKSTART.md`
2. **Practice**: Run `demo.py`
3. **Experiment**: Modify `example_basic.sn`
4. **Test**: Run `test_sn.py`
5. **Build**: Create your own documents
6. **Deep Dive**: Read the full specification

## 💡 Tips

1. **Use strict mode for validation**: `python sn.py parse --strict doc.sn`
2. **Sign important documents**: `python sn.py sign release-notes.sn`
3. **Always verify signatures**: `python sn.py verify doc.sn`
4. **Use metadata**: Add author, version, date to all documents
5. **Link documents**: Use `endnewsn:` for multi-part docs

## 🌟 Next Steps

- Create your first SN document
- Build a documentation website
- Set up a signing workflow
- Contribute improvements
- Share your experience!

---

**Made with ❤️ for clear, maintainable documentation**

Version: Super Notation v1.0 (2026-02-09)
