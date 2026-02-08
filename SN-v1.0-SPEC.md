# Super Notation — SN v1.0 (Official Specification)

**File extension:** `.sn`  
**Formal name:** Super Notation v1 (SN v1.0) — stable standard  
**Initial release:** 2026-02-09

---

## Table of contents
1. Overview & goals  
2. Quick example  
3. File header & versioning  
4. Lexical rules & canonicalization (for signing)  
5. Command & block reference (complete v1)  
6. Multi-file flow (`endnewsn:`)  
7. Signing and locking (versioned documents)  
8. Parsing & rendering rules (lenient/strict)  
9. Security considerations  
10. Serialization & archival rules  
11. Interop: tools & reference implementation notes  
12. Publishing & release instructions  
13. Minimal test suite layout & examples  
14. License & contribution notes  
15. Appendix: scripts (sign / verify)

---

## 1 — Overview & goals

**Super Notation (SN v1.0)** is a human-first, machine-friendly plain-text format designed specifically for documentation. It is intentionally minimal and intended to be a **stable standard**:

- Readable in raw form, easy to parse.
- Small, predictable keyword set.
- Supports multi-file linear documentation flows.
- Supports document metadata, code blocks, ordered lists, navigation, images, and cryptographic sealing for published docs.
- **No plugin system** in v1 — unknown keywords degrade to visible plain text (lenient) or error (strict).

Use-cases: manuals, released product docs, legal/archival documentation, tutorials, knowledge bases.

---

## 2 — Quick example

A simple `.sn` file:

```
<super-notation-v1>

meta: author=Jane Doe
meta: version=1.0
title: Getting Started

sec:introduction
para: Welcome to our product.

sec:installation
para: Follow steps below.

olist:numbers
Download the package
Run installer
Start the app

code:
# example
print("Hello SN")
endcode:

endnewsn: install_part2.sn

sign: SHA256-XXXXX...
close:
```

---

## 3 — File header & versioning

- Each SN file MUST start with the **declaration line** on the first non-empty, non-comment line:

  ```
  <super-notation-v1>
  ```

- The file extension for v1: **`.sn`**
- Suggested MIME hint: `text/x-super-notation-sn`
- If a parser does not support the declared version, it MUST refuse (strict) or enter compatibility mode (lenient).

---

## 4 — Lexical rules & canonicalization (for signing)

**Encoding**

- SN files MUST be UTF-8 encoded.

**Line endings**

- Accept `LF` or `CRLF` on input.
- For canonicalization (signing/verification): normalize to `LF` (`
`) only.

**Comments**

- Lines whose first non-space character is `#` are comments and ignored by the parser.

**Blank lines**

- Blank lines separate logical groups and are otherwise ignored.

**Canonicalization algorithm (for signatures)**

When producing or verifying a signature, implementers MUST canonicalize the document the same way:

1. Read file bytes as UTF-8; if BOM present, remove it.
2. Convert all line endings to `LF` (`
`).
3. Preserve all characters exactly except for the line ending normalization.
4. Identify the earliest line that begins (after trimming leading spaces) with `sign:` — the signature line itself **and everything after it (including `close:`)** are **not included** in the signed material. That is, the signature covers the canonicalized bytes from the beginning up to but *not including* the `sign:` line.
5. Compute SHA-256 over those canonicalized bytes (no further normalization).
6. Represent signatures as uppercase hex prefixed with `SHA256-`. Example: `SHA256-3A1F...9C`.

(Implementation note: use consistent normalization across all tools. The reference scripts in the Appendix implement this.)

---

## 5 — Command & block reference (SN v1)

**General syntax patterns**

- `key:value` — declaration (value visible)
- `key=target: Visible Text` — reference/link (target may be file path or section id)
- `key:=value` — used when value itself may contain separators (e.g., `img:=path`)
- Keywords are case-insensitive for parsing.

### Core commands (v1)

- `meta: <text>`  
  Arbitrary metadata. Must appear before visible content. Not shown in rendered output.

- `title: <text>`  
  Document title (renderers may use as page title).

- `sec:<id>`  
  Define a section. `id` must be unique per document. Allowed characters: letters, digits, `-` and `_`. Flat-only structure (no nesting).

- `sec=<id>: <Visible Text>`  
  Internal link to a section in the same document.

- `para: <text>`  
  Paragraph.

- `break-line` or `break-line:`  
  Horizontal rule.

- `olist:bullet` or `olist:numbers`  
  List container. Following lines (non-empty, until blank line or next command) are items. `bullet` renders as unordered bullets; `numbers` renders as ordered (renderer may auto-number). No nesting.

- `code:` ... `endcode:`  
  Literal code block. Everything between `code:` and `endcode:` is raw text (no parsing).

- `img:=<path> | <alt text>`  
  Insert image. The `:=` syntax allows including `:` in the path. `path` may be a local path or URL. `|` separates optional alt text.

- `link: <url>`  
  Rendered as a link whose text is the URL.

- `linktxt: <text> | <url>` or `linktxt: <text> : <url>`  
  Rendered as a link with custom text.

- `opensn=<location>: <Visible Text>`  
  Cross-file navigation. `<location>` may be a local `.sn` path or an HTTP/HTTPS URL. Renderer behavior: open `.sn` in SN viewer; open URL in external browser.

- `endnewsn: <file path>`  
  When encountered, the current document's flow indicates a forward link to the named file. Parsers/renderers should record a forward navigation action (e.g., Next). No further content in the current file should be considered part of the current logical page; implementations may stop processing further lines in the file after this command in strict mode.

- `sign: <signature>`  
  Cryptographic signature for the canonicalized content preceding the `sign:` line. Format: `SHA256-<HEX>`. Placed at end of file.

- `close:`  
  Marks the document as sealed. When present *and* the `sign:` matches the canonicalized content, the document is considered **closed** and tools should treat it as read-only unless unlocking (which invalidates the signature).

### Inline formatting (v1 — minimal)

- `{b:...}` or `{bold:...}` → bold
- `{i:...}` or `{italic:...}` → italic
- `{u:...}` → underline
- `{color=<name|#hex>:...}` → inline color
- `{{` and `}}` → literal braces

Note: inline formatting is optional for renderers; it is recommended but not mandatory.

---

## 6 — Multi-file & flow (`endnewsn:`)

- `endnewsn: path` defines a forward link (Next) to another `.sn` file. For a linear documentation flow, connect files with `endnewsn` links.
- Paths are resolved relative to the current document directory.
- On export to HTML, a `Next` link should be added linking to the target page (rendered HTML).
- In GUI viewers, show a Next button that opens the target file in the SN viewer.

---

## 7 — Signing & locking (release-grade documents)

**Goal:** support official, versioned, sealed documentation.

**Workflow to seal and lock a document:**

1. Author finalizes document content.
2. Ensure first line declaration `<super-notation-v1>` is present and all metadata is set.
3. Compute canonical representation (see §4).
4. Compute SHA-256 over canonical bytes and produce uppercase hex string.
5. Append at the end of file:

```
sign: SHA256-<HEX>
close:
```

6. Publish the `.sn` file.

**Open/verify:**
- Viewer verifies: canonicalize, compute SHA256, compare to signature.
- If match and `close:` present → show as *sealed* (read-only).
- Any modification invalidates the signature.

**Unlocking/editing:**
- To edit, tools must remove `sign:` and `close:` (or modify them), which means the document is no longer sealed or must be re-signed.

---

## 8 — Parsing & rendering rules

**Parser behavior**

- Two modes:
  - **Lenient** (default): unknown keywords produce visible paragraphs (best-effort rendering).
  - **Strict**: unknown or malformed keywords produce errors and halt parsing or report warnings.

**Process:**

1. Normalize BOM and line endings for parsing only.
2. Find the first non-empty, non-comment line; it must be `<super-notation-v1>`.
3. Consume top `meta:` lines (if any).
4. Process lines sequentially: commands produce nodes. For block commands (`olist`, `code`, etc.), consume lines appropriately (see command definitions).
5. When `endnewsn:` encountered, register forward link and stop processing further content in strict implementations.

**Rendering**

- Renderers must not execute arbitrary content.
- Keep visual output consistent and predictable: `sec:` definitions should be anchored in rendered document for `sec=` links.
- For `opensn=` to local files, web renderers should not automatically expose local file URIs without user permission.

---

## 9 — Security considerations

- **Local file references:** `img:=` or `opensn=` referencing local files should be guarded by viewers. Web-hosted renderers must not access `file:///` URIs automatically.
- **XSS:** When exporting to HTML, escape all text content; do not inject raw HTML from SN (unless explicitly allowed in a future version).
- **Signatures:** Use SHA-256 for integrity. Consider GPG signatures for author verification if needed (not mandated in v1).
- **Closed docs:** Treat `close:` + correct `sign:` as authoritative; editors must require explicit action to unlock (and document that unlocking invalidates signature).

---

## 10 — Serialization & archival rules

- SN is textual and round-trip-friendly. Tools should preserve metadata and canonicalization rules to guarantee reproducible signatures.
- For archive packaging, include original `.sn` file(s) along with the signature and any assets (images). Recommended structure:

```
docs/
  chapter01.sn
  chapter02.sn
  assets/
    img1.png
release/
  docs-chapter01.sn
  docs-chapter01.sn.sig
```

---

## 11 — Interop: tools & reference implementation notes

To seed the standard, create:

- A **reference parser** (Python) that produces AST + HTML renderer.
- A **signing/verification CLI** (Python) implementing the canonicalization and signature algorithm above.
- A minimal **viewer/editor** (Tkinter or web) that forbids editing sealed docs.

Provide test fixtures (example `.sn` files and expected HTML outputs).

---

## 12 — Publishing & release instructions

Suggested repo layout and steps to publish SN v1.0 on GitHub.

### Suggested repo structure

```
super-notation/
  SPEC.md
  README.md
  EXAMPLES/
    example-intro.sn
  TOOLS/
    sign_verify.py
  LICENSE.md
  RELEASE.md
```

### Steps

1. Create the repository and add files above.
2. Commit and push to GitHub.
3. Create a release named `v1.0` with release notes describing the stable spec.
4. Tag and publish source and examples.

---

## 13 — Minimal test suite layout & examples

Create `tests/` with input `.sn` and expected `.html` outputs:

```
tests/
  basic.sn
  basic.expected.html
  code_block.sn
  code_block.expected.html
  sealed.sn
  sealed.expected.html
```

Add a small script (`run_tests.py`) to run parser/renderer and compare outputs (insensitive to whitespace differences in HTML).

---

## 14 — License & contribution notes

You indicated use of **Server-Lab Open-Control License (SOCL) 1.0** for the project. Include a copy of that license in `LICENSE.md` in your repository.

Contributions: contributors grant the owner the right to use and relicense contributions as described by SOCL.

---

## 15 — Appendix: Sign & Verify (reference scripts)

### sign_sn.py — produce signature

```python
#!/usr/bin/env python3
import sys, hashlib

def canonical_bytes(path):
    b = open(path, "rb").read()
    if b.startswith(b"ï»¿"):
        b = b[3:]
    b = b.replace(b"
", b"
").replace(b"", b"
")
    lines = b.split(b"
")
    for i, line in enumerate(lines):
        if line.lstrip().lower().startswith(b"sign:"):
            up_to = b"
".join(lines[:i])
            return up_to
    return b

def sign(path):
    cb = canonical_bytes(path)
    h = hashlib.sha256(cb).hexdigest().upper()
    print("SHA256-" + h)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: sign_sn.py file.sn")
        sys.exit(2)
    sign(sys.argv[1])
```

### verify_sn.py — verify signature

```python
#!/usr/bin/env python3
import sys, hashlib

def canonical_bytes(path):
    b = open(path, "rb").read()
    if b.startswith(b"ï»¿"):
        b = b[3:]
    b = b.replace(b"
", b"
").replace(b"", b"
")
    lines = b.split(b"
")
    for i, line in enumerate(lines):
        if line.lstrip().lower().startswith(b"sign:"):
            up_to = b"
".join(lines[:i])
            sig_line = lines[i].decode('utf-8', errors='ignore').strip()
            return up_to, sig_line
    return b, None

def verify(path):
    cb, sig_line = canonical_bytes(path)
    h = hashlib.sha256(cb).hexdigest().upper()
    expected = "SHA256-" + h
    if sig_line is None:
        print("No signature found.")
        return 2
    if sig_line.strip() == ("sign: " + expected):
        print("Signature valid:", expected)
        return 0
    else:
        print("Signature mismatch.")
        print("Expected:", expected)
        print("Found   :", sig_line)
        return 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: verify_sn.py file.sn")
        sys.exit(2)
    sys.exit(verify(sys.argv[1]))
```

---

## Final notes

This SPEC.md is the official reference for **Super Notation v1.0**. It is intentionally small and stable — the goal is long-term compatibility and predictable implementations.

If you want, I can now:
- save this SPEC.md into a file and give you a download link,
- generate README.md and examples,
- create `TOOLS/sign_verify.py` files,
- initialize a suggested Git repo structure as files you can download.

Which would you like me to produce now?