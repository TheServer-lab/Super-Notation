#!/usr/bin/env python3
"""
Test script for Super Notation v1.0 interpreter

This script demonstrates all the features of the SN interpreter.
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from sn_parser import SNParser, HTMLRenderer, ParseMode
from sn_signing import sign_file, verify_signature, unsign_file


def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def test_basic_parsing():
    """Test basic parsing functionality"""
    print_section("Test 1: Basic Parsing")
    
    parser = SNParser(mode=ParseMode.LENIENT)
    
    with open('example_basic.sn', 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        doc = parser.parse(content)
        print("✓ Successfully parsed example_basic.sn")
        print(f"  - Metadata entries: {len(doc.metadata)}")
        print(f"  - Content nodes: {len(doc.nodes)}")
        print(f"  - Node types found:")
        
        node_types = {}
        for node in doc.nodes:
            node_type = node.__class__.__name__
            node_types[node_type] = node_types.get(node_type, 0) + 1
        
        for node_type, count in sorted(node_types.items()):
            print(f"    • {node_type}: {count}")
    
    except Exception as e:
        print(f"✗ Parse error: {e}")
        return False
    
    return True


def test_html_rendering():
    """Test HTML rendering"""
    print_section("Test 2: HTML Rendering")
    
    parser = SNParser(mode=ParseMode.LENIENT)
    
    with open('example_basic.sn', 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        doc = parser.parse(content)
        renderer = HTMLRenderer()
        html_output = renderer.render(doc)
        
        # Write to file
        with open('example_basic.html', 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        print("✓ Successfully rendered to HTML")
        print(f"  - Output: example_basic.html")
        print(f"  - HTML size: {len(html_output)} bytes")
        print(f"  - Contains <h1>: {'<h1' in html_output}")
        print(f"  - Contains <code>: {'<code>' in html_output}")
        print(f"  - Contains <strong> (bold): {'<strong>' in html_output}")
    
    except Exception as e:
        print(f"✗ Render error: {e}")
        return False
    
    return True


def test_signing():
    """Test document signing"""
    print_section("Test 3: Document Signing")
    
    # Create a test file
    test_content = """<super-notation-v1>

meta: author=Test Author
title: Test Document

para: This is a test document for signing.
"""
    
    with open('test_sign.sn', 'w', encoding='utf-8', newline='\n') as f:
        f.write(test_content)
    
    try:
        # Sign the file
        signature = sign_file('test_sign.sn', in_place=True)
        print("✓ Successfully signed test_sign.sn")
        print(f"  - Signature: {signature[:32]}...")
        
        # Verify
        is_valid, message = verify_signature('test_sign.sn')
        
        if is_valid:
            print("✓ Signature verification passed")
            print(f"  - {message}")
        else:
            print("✗ Signature verification failed")
            print(f"  - {message}")
            return False
    
    except Exception as e:
        print(f"✗ Signing error: {e}")
        return False
    
    return True


def test_signature_invalidation():
    """Test that modifying a signed document invalidates signature"""
    print_section("Test 4: Signature Invalidation")
    
    try:
        # Read signed file
        with open('test_sign.sn', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Modify content (add a line before signature)
        lines = content.split('\n')
        
        # Insert new content before sign: line
        for i, line in enumerate(lines):
            if line.strip().lower().startswith('sign:'):
                lines.insert(i, 'para: This modification should invalidate the signature.')
                break
        
        modified_content = '\n'.join(lines)
        
        # Write modified file
        with open('test_sign_modified.sn', 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        # Verify - should fail
        is_valid, message = verify_signature('test_sign_modified.sn')
        
        if not is_valid:
            print("✓ Signature correctly invalidated after modification")
            print(f"  - Expected behavior: signature should be invalid")
        else:
            print("✗ Unexpected: signature still valid after modification")
            return False
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    
    finally:
        # Clean up
        if os.path.exists('test_sign_modified.sn'):
            os.remove('test_sign_modified.sn')
    
    return True


def test_inline_formatting():
    """Test inline formatting parsing"""
    print_section("Test 5: Inline Formatting")
    
    test_content = """<super-notation-v1>

title: Formatting Test

para: This is {b:bold}, {i:italic}, and {u:underlined} text.
para: This is {color=#ff0000:red text} and {color=blue:blue text}.
para: Escaped braces: {{ and }} should appear literally.
"""
    
    parser = SNParser(mode=ParseMode.LENIENT)
    
    try:
        doc = parser.parse(test_content)
        renderer = HTMLRenderer()
        html_output = renderer.render(doc)
        
        print("✓ Inline formatting parsed successfully")
        print(f"  - Contains <strong>: {'<strong>' in html_output}")
        print(f"  - Contains <em>: {'<em>' in html_output}")
        print(f"  - Contains <u>: {'<u>' in html_output}")
        print(f"  - Contains color style: {'color:' in html_output}")
        print(f"  - Escaped braces preserved: {'{ and }' in html_output or '{{ and }}' in html_output}")
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    
    return True


def test_strict_mode():
    """Test strict parsing mode"""
    print_section("Test 6: Strict vs Lenient Mode")
    
    # Content with unknown command
    test_content = """<super-notation-v1>

title: Test

para: Valid paragraph
unknown_command: This should fail in strict mode
para: Another paragraph
"""
    
    # Test lenient mode
    print("Testing LENIENT mode:")
    parser_lenient = SNParser(mode=ParseMode.LENIENT)
    try:
        doc = parser_lenient.parse(test_content)
        print("  ✓ Lenient mode: parsed successfully (unknown commands treated as text)")
        print(f"    - Nodes: {len(doc.nodes)}")
    except Exception as e:
        print(f"  ✗ Lenient mode failed: {e}")
        return False
    
    # Test strict mode
    print("\nTesting STRICT mode:")
    parser_strict = SNParser(mode=ParseMode.STRICT)
    try:
        doc = parser_strict.parse(test_content)
        print("  ✗ Strict mode should have failed on unknown command")
        return False
    except ValueError as e:
        print(f"  ✓ Strict mode: correctly rejected unknown command")
        print(f"    - Error: {e}")
    
    return True


def test_multi_file_navigation():
    """Test multi-file navigation"""
    print_section("Test 7: Multi-File Navigation")
    
    parser = SNParser(mode=ParseMode.LENIENT)
    
    try:
        # Parse part 1
        with open('example_part1.sn', 'r', encoding='utf-8') as f:
            content = f.read()
        
        doc = parser.parse(content)
        
        # Check for EndNewSNNode
        has_endnewsn = any(node.__class__.__name__ == 'EndNewSNNode' for node in doc.nodes)
        
        if has_endnewsn:
            print("✓ Found endnewsn: navigation command")
            
            # Render to check Next link
            renderer = HTMLRenderer()
            html_output = renderer.render(doc)
            
            if 'Next:' in html_output or 'example_part2.sn' in html_output:
                print("  ✓ Next link rendered in HTML")
            else:
                print("  ✗ Next link not found in HTML")
                return False
        else:
            print("✗ endnewsn: command not found")
            return False
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    
    return True


def main():
    """Run all tests"""
    print("\n" + "█" * 70)
    print("  SUPER NOTATION v1.0 - INTERPRETER TEST SUITE")
    print("█" * 70)
    
    tests = [
        ("Basic Parsing", test_basic_parsing),
        ("HTML Rendering", test_html_rendering),
        ("Document Signing", test_signing),
        ("Signature Invalidation", test_signature_invalidation),
        ("Inline Formatting", test_inline_formatting),
        ("Strict vs Lenient Mode", test_strict_mode),
        ("Multi-File Navigation", test_multi_file_navigation),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}  {name}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n  🎉 All tests passed! 🎉")
        return 0
    else:
        print(f"\n  ⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
