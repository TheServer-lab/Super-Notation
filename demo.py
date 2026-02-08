#!/usr/bin/env python3
"""
Super Notation v1.0 - Interactive Demo

This script demonstrates the key features of the SN interpreter.
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from sn_parser import SNParser, HTMLRenderer, ParseMode
from sn_signing import sign_file, verify_signature


def print_header(text):
    """Print a styled header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def demo():
    """Run interactive demo"""
    print("\n" + "█" * 70)
    print("  SUPER NOTATION v1.0 - INTERACTIVE DEMO")
    print("█" * 70)
    
    print("\nThis demo will show you how to:")
    print("  1. Parse SN documents")
    print("  2. Render them to HTML")
    print("  3. Sign and verify documents")
    print()
    
    input("Press Enter to start the demo...")
    
    # Demo 1: Parse
    print_header("DEMO 1: Parsing an SN Document")
    
    print("\nParsing example_basic.sn...")
    parser = SNParser(mode=ParseMode.LENIENT)
    
    with open('example_basic.sn', 'r', encoding='utf-8') as f:
        content = f.read()
    
    doc = parser.parse(content)
    
    print("✓ Successfully parsed!")
    print(f"  • Title: {[n.text for n in doc.nodes if hasattr(n, 'text') and n.__class__.__name__ == 'TitleNode'][0]}")
    print(f"  • Sections: {sum(1 for n in doc.nodes if n.__class__.__name__ == 'SectionDefNode')}")
    print(f"  • Paragraphs: {sum(1 for n in doc.nodes if n.__class__.__name__ == 'ParagraphNode')}")
    print(f"  • Code blocks: {sum(1 for n in doc.nodes if n.__class__.__name__ == 'CodeBlockNode')}")
    
    input("\nPress Enter to continue...")
    
    # Demo 2: Render
    print_header("DEMO 2: Rendering to HTML")
    
    print("\nRendering to HTML...")
    renderer = HTMLRenderer()
    html = renderer.render(doc)
    
    output_file = 'demo_output.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Rendered to {output_file}")
    print(f"  • HTML size: {len(html):,} bytes")
    print(f"  • Open it in your browser to see the result!")
    
    input("\nPress Enter to continue...")
    
    # Demo 3: Signing
    print_header("DEMO 3: Signing and Verification")
    
    # Create a demo document
    demo_doc = """<super-notation-v1>

meta: author=Demo User
meta: date=2026-02-09

title: Demo Document

para: This document demonstrates cryptographic signing in SN.

sec:features
para: When signed, the document is {b:sealed} and read-only.
"""
    
    demo_file = 'demo_signed.sn'
    with open(demo_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(demo_doc)
    
    print(f"\nCreated {demo_file}")
    print("Signing the document...")
    
    signature = sign_file(demo_file, in_place=True)
    print(f"✓ Document signed!")
    print(f"  • Signature: {signature[:50]}...")
    
    print("\nVerifying signature...")
    is_valid, message = verify_signature(demo_file)
    
    if is_valid:
        print("✓ Signature verified!")
        print(f"  • {message.split(':')[0]}")
    else:
        print("✗ Verification failed!")
    
    input("\nPress Enter to continue...")
    
    # Demo 4: Modification detection
    print_header("DEMO 4: Tampering Detection")
    
    print("\nLet's see what happens if someone modifies the signed document...")
    
    with open(demo_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Insert a modification
    modified = content.replace(
        'para: This document demonstrates',
        'para: This MODIFIED document demonstrates'
    )
    
    modified_file = 'demo_tampered.sn'
    with open(modified_file, 'w', encoding='utf-8') as f:
        f.write(modified)
    
    print(f"Created {modified_file} with unauthorized changes...")
    print("Verifying signature...")
    
    is_valid, message = verify_signature(modified_file)
    
    if not is_valid:
        print("✓ Tampering detected!")
        print("  • The signature no longer matches")
        print("  • This proves the document was modified after signing")
    else:
        print("✗ Unexpected: signature still valid!")
    
    # Cleanup
    for f in [modified_file, demo_file, output_file]:
        if os.path.exists(f):
            os.remove(f)
    
    print_header("DEMO COMPLETE")
    
    print("\nYou've seen how to:")
    print("  ✓ Parse SN documents")
    print("  ✓ Render them to beautiful HTML")
    print("  ✓ Sign documents cryptographically")
    print("  ✓ Detect unauthorized modifications")
    
    print("\nNext steps:")
    print("  • Read QUICKSTART.md for basic usage")
    print("  • Read README.md for detailed documentation")
    print("  • Run test_sn.py to see the full test suite")
    print("  • Try: python sn.py --help")
    
    print("\n" + "█" * 70)
    print("  Thank you for trying Super Notation!")
    print("█" * 70 + "\n")


if __name__ == '__main__':
    try:
        demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nDemo error: {e}")
        sys.exit(1)
