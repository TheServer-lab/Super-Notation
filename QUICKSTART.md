# Super Notation Interpreter - Quick Start Guide

## Installation

1. **No dependencies required!** The interpreter uses only Python standard library.

2. **Files you need:**
   - `sn_parser.py` - Core parser and renderer
   - `sn_signing.py` - Signing utilities
   - `sn.py` - Command-line interface

3. **Make it executable:**
   ```bash
   chmod +x sn.py
   ```

## Basic Commands

### 1. Validate a document
```bash
python sn.py parse mydoc.sn
```

### 2. Convert to HTML
```bash
python sn.py render mydoc.sn
# Creates mydoc.html
```

### 3. Sign a document
```bash
python sn.py sign mydoc.sn
# Adds cryptographic signature
```

### 4. Verify signature
```bash
python sn.py verify mydoc.sn
```

## Create Your First SN Document

1. **Create a file `hello.sn`:**
```
<super-notation-v1>

meta: author=Your Name
title: Hello World

sec:introduction
para: This is my first {b:Super Notation} document!

code:
print("Hello, SN!")
endcode:
```

2. **Render it:**
```bash
python sn.py render hello.sn
```

3. **Open `hello.html` in your browser!**

## Testing

Run the test suite:
```bash
python test_sn.py
```

## Need Help?

- See `README.md` for detailed documentation
- See `SN-v1_0-SPEC.md` for the full specification
- Examples: `example_basic.sn`, `example_part1.sn`, `example_part2.sn`

## Supported Features

✅ Metadata and titles
✅ Sections with anchors
✅ Paragraphs with inline formatting
✅ Code blocks
✅ Ordered and unordered lists
✅ Images and links
✅ Multi-file navigation
✅ Document signing and sealing
✅ Two parsing modes (lenient/strict)

## Common Use Cases

**1. Technical Documentation**
```bash
python sn.py render api-docs.sn
```

**2. Signed Release Notes**
```bash
python sn.py sign release-notes.sn
python sn.py verify release-notes.sn
```

**3. Multi-Part Tutorial**
```
tutorial-part1.sn (contains: endnewsn: tutorial-part2.sn)
tutorial-part2.sn (contains: endnewsn: tutorial-part3.sn)
tutorial-part3.sn
```

Render all:
```bash
for file in tutorial-part*.sn; do python sn.py render "$file"; done
```

---

That's it! You're ready to use Super Notation. 🎉
