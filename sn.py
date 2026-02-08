#!/usr/bin/env python3
"""
Super Notation v1.0 - Command Line Interface

Main tool for parsing, rendering, signing, and verifying SN files.
"""

import sys
import argparse
from pathlib import Path

from sn_parser import SNParser, HTMLRenderer, ParseMode
from sn_signing import (
    compute_signature, verify_signature, sign_file, 
    unsign_file, has_close_marker
)


def cmd_parse(args):
    """Parse an SN file and show AST"""
    parser = SNParser(mode=ParseMode.STRICT if args.strict else ParseMode.LENIENT)
    
    with open(args.file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        doc = parser.parse(content)
        print(f"✓ Successfully parsed: {args.file}")
        print(f"  Version: {doc.version}")
        print(f"  Metadata entries: {len(doc.metadata)}")
        print(f"  Content nodes: {len(doc.nodes)}")
        print(f"  Signed: {doc.signature is not None}")
        print(f"  Sealed: {doc.is_closed}")
        
        if args.verbose:
            print("\n--- Document Structure ---")
            for i, node in enumerate(doc.nodes, 1):
                print(f"{i}. {node.__class__.__name__}")
    
    except Exception as e:
        print(f"✗ Parse error: {e}", file=sys.stderr)
        return 1
    
    return 0


def cmd_render(args):
    """Render an SN file to HTML"""
    parser = SNParser(mode=ParseMode.STRICT if args.strict else ParseMode.LENIENT)
    
    with open(args.file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        doc = parser.parse(content)
        renderer = HTMLRenderer()
        html_output = renderer.render(doc)
        
        # Determine output file
        if args.output:
            output_path = Path(args.output)
        else:
            input_path = Path(args.file)
            output_path = input_path.with_suffix('.html')
        
        # Write HTML
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        print(f"✓ Rendered to: {output_path}")
        return 0
    
    except Exception as e:
        print(f"✗ Render error: {e}", file=sys.stderr)
        return 1


def cmd_sign(args):
    """Sign an SN file"""
    try:
        signature = sign_file(args.file, in_place=True)
        print(f"✓ File signed: {args.file}")
        print(f"  Signature: {signature}")
        return 0
    
    except Exception as e:
        print(f"✗ Signing error: {e}", file=sys.stderr)
        return 1


def cmd_verify(args):
    """Verify an SN file's signature"""
    try:
        is_valid, message = verify_signature(args.file)
        
        if is_valid:
            print(message)
            return 0
        else:
            print(message, file=sys.stderr)
            return 1
    
    except Exception as e:
        print(f"✗ Verification error: {e}", file=sys.stderr)
        return 1


def cmd_unsign(args):
    """Remove signature from an SN file"""
    try:
        removed = unsign_file(args.file)
        
        if removed:
            print(f"✓ Signature removed from: {args.file}")
            return 0
        else:
            print(f"ℹ No signature found in: {args.file}")
            return 0
    
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


def cmd_info(args):
    """Show information about an SN file"""
    try:
        # Parse the file
        parser = SNParser(mode=ParseMode.LENIENT)
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        doc = parser.parse(content)
        
        # Check signature
        is_signed = doc.signature is not None
        is_sealed = doc.is_closed
        
        print(f"File: {args.file}")
        print(f"Version: {doc.version}")
        print(f"Metadata entries: {len(doc.metadata)}")
        print(f"Content nodes: {len(doc.nodes)}")
        print(f"Signed: {is_signed}")
        print(f"Sealed: {is_sealed}")
        
        if is_signed:
            is_valid, message = verify_signature(args.file)
            if is_valid:
                print(f"Signature: ✓ VALID")
            else:
                print(f"Signature: ✗ INVALID")
        
        # Extract title
        for node in doc.nodes:
            if node.__class__.__name__ == 'TitleNode':
                print(f"Title: {node.text}")
                break
        
        # Show metadata
        if doc.metadata and args.verbose:
            print("\nMetadata:")
            for meta in doc.metadata:
                print(f"  {meta.content}")
        
        return 0
    
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Super Notation v1.0 - Documentation format interpreter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Parse and validate an SN file
  sn parse document.sn
  
  # Render to HTML
  sn render document.sn
  
  # Sign a document
  sn sign document.sn
  
  # Verify signature
  sn verify document.sn
  
  # Get file info
  sn info document.sn
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Parse command
    parse_parser = subparsers.add_parser('parse', help='Parse and validate an SN file')
    parse_parser.add_argument('file', help='SN file to parse')
    parse_parser.add_argument('--strict', action='store_true', help='Use strict parsing mode')
    parse_parser.add_argument('-v', '--verbose', action='store_true', help='Show detailed structure')
    
    # Render command
    render_parser = subparsers.add_parser('render', help='Render SN file to HTML')
    render_parser.add_argument('file', help='SN file to render')
    render_parser.add_argument('-o', '--output', help='Output HTML file (default: same name with .html)')
    render_parser.add_argument('--strict', action='store_true', help='Use strict parsing mode')
    
    # Sign command
    sign_parser = subparsers.add_parser('sign', help='Sign an SN file')
    sign_parser.add_argument('file', help='SN file to sign')
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify SN file signature')
    verify_parser.add_argument('file', help='SN file to verify')
    
    # Unsign command
    unsign_parser = subparsers.add_parser('unsign', help='Remove signature from SN file')
    unsign_parser.add_argument('file', help='SN file to unsign')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show information about SN file')
    info_parser.add_argument('file', help='SN file to inspect')
    info_parser.add_argument('-v', '--verbose', action='store_true', help='Show detailed info')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Dispatch to command handlers
    commands = {
        'parse': cmd_parse,
        'render': cmd_render,
        'sign': cmd_sign,
        'verify': cmd_verify,
        'unsign': cmd_unsign,
        'info': cmd_info,
    }
    
    return commands[args.command](args)


if __name__ == '__main__':
    sys.exit(main())
