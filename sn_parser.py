#!/usr/bin/env python3
"""
Super Notation v1.0 Parser and Renderer

This module provides a complete implementation of the SN v1.0 specification,
including tokenization, parsing, AST construction, and HTML rendering.
"""

import re
import html
from typing import List, Optional, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ParseMode(Enum):
    """Parser mode: lenient or strict"""
    LENIENT = "lenient"
    STRICT = "strict"


# ============================================================================
# AST Node Definitions
# ============================================================================

@dataclass
class ASTNode:
    """Base class for all AST nodes"""
    pass


@dataclass
class MetaNode(ASTNode):
    """Metadata node (not rendered)"""
    content: str


@dataclass
class TitleNode(ASTNode):
    """Document title"""
    text: str


@dataclass
class SectionDefNode(ASTNode):
    """Section definition: sec:id"""
    section_id: str


@dataclass
class SectionLinkNode(ASTNode):
    """Section link: sec=id: Visible Text"""
    section_id: str
    text: str


@dataclass
class ParagraphNode(ASTNode):
    """Paragraph with inline formatting support"""
    text: str


@dataclass
class BreakLineNode(ASTNode):
    """Horizontal rule"""
    pass


@dataclass
class ListNode(ASTNode):
    """Ordered or unordered list"""
    list_type: str  # 'bullet' or 'numbers'
    items: List[str] = field(default_factory=list)


@dataclass
class CodeBlockNode(ASTNode):
    """Code block (literal text)"""
    code: str


@dataclass
class ImageNode(ASTNode):
    """Image reference"""
    path: str
    alt_text: str = ""


@dataclass
class LinkNode(ASTNode):
    """Simple link (URL as text)"""
    url: str


@dataclass
class LinkTextNode(ASTNode):
    """Link with custom text"""
    text: str
    url: str


@dataclass
class OpenSNNode(ASTNode):
    """Cross-file navigation link"""
    location: str
    text: str


@dataclass
class EndNewSNNode(ASTNode):
    """Forward navigation to next file"""
    filepath: str


@dataclass
class SignatureNode(ASTNode):
    """Cryptographic signature"""
    signature: str


@dataclass
class CloseNode(ASTNode):
    """Document seal marker"""
    pass


@dataclass
class UnknownNode(ASTNode):
    """Unknown/unrecognized command (lenient mode)"""
    raw_text: str


@dataclass
class Document:
    """Root document node"""
    version: str = "v1"
    metadata: List[MetaNode] = field(default_factory=list)
    nodes: List[ASTNode] = field(default_factory=list)
    is_closed: bool = False
    signature: Optional[str] = None


# ============================================================================
# Tokenizer
# ============================================================================

class SNTokenizer:
    """Tokenizes Super Notation files"""
    
    def __init__(self, content: str):
        self.lines = content.split('\n')
        self.current_line = 0
    
    def peek_line(self) -> Optional[str]:
        """Peek at current line without consuming"""
        if self.current_line < len(self.lines):
            return self.lines[self.current_line]
        return None
    
    def consume_line(self) -> Optional[str]:
        """Consume and return current line"""
        line = self.peek_line()
        if line is not None:
            self.current_line += 1
        return line
    
    def is_comment(self, line: str) -> bool:
        """Check if line is a comment"""
        stripped = line.lstrip()
        return stripped.startswith('#')
    
    def is_blank(self, line: str) -> bool:
        """Check if line is blank"""
        return line.strip() == ''
    
    def has_more(self) -> bool:
        """Check if more lines available"""
        return self.current_line < len(self.lines)


# ============================================================================
# Parser
# ============================================================================

class SNParser:
    """Parses Super Notation files into AST"""
    
    def __init__(self, mode: ParseMode = ParseMode.LENIENT):
        self.mode = mode
        self.tokenizer: Optional[SNTokenizer] = None
    
    def parse(self, content: str) -> Document:
        """Parse SN content into a Document AST"""
        self.tokenizer = SNTokenizer(content)
        doc = Document()
        
        # Parse header
        if not self._parse_header():
            raise ValueError("Missing or invalid <super-notation-v1> header")
        
        # Parse metadata (must come before content)
        doc.metadata = self._parse_metadata()
        
        # Parse body
        while self.tokenizer.has_more():
            node = self._parse_node()
            if node:
                doc.nodes.append(node)
                
                # Handle signature and close
                if isinstance(node, SignatureNode):
                    doc.signature = node.signature
                elif isinstance(node, CloseNode):
                    doc.is_closed = True
                # Stop after endnewsn in strict mode
                elif isinstance(node, EndNewSNNode) and self.mode == ParseMode.STRICT:
                    break
        
        return doc
    
    def _parse_header(self) -> bool:
        """Parse and validate file header"""
        while self.tokenizer.has_more():
            line = self.tokenizer.peek_line()
            if self.tokenizer.is_blank(line) or self.tokenizer.is_comment(line):
                self.tokenizer.consume_line()
                continue
            
            # First non-blank, non-comment line must be header
            if line.strip() == '<super-notation-v1>':
                self.tokenizer.consume_line()
                return True
            else:
                return False
        
        return False
    
    def _parse_metadata(self) -> List[MetaNode]:
        """Parse metadata section"""
        metadata = []
        
        while self.tokenizer.has_more():
            line = self.tokenizer.peek_line()
            
            if self.tokenizer.is_blank(line) or self.tokenizer.is_comment(line):
                self.tokenizer.consume_line()
                continue
            
            # Check if it's a meta: line
            stripped = line.strip()
            if stripped.lower().startswith('meta:'):
                self.tokenizer.consume_line()
                content = stripped[5:].strip()
                metadata.append(MetaNode(content))
            else:
                # No more metadata
                break
        
        return metadata
    
    def _parse_node(self) -> Optional[ASTNode]:
        """Parse a single node"""
        line = self.tokenizer.peek_line()
        
        if line is None:
            return None
        
        # Skip blank lines and comments
        if self.tokenizer.is_blank(line) or self.tokenizer.is_comment(line):
            self.tokenizer.consume_line()
            return None
        
        stripped = line.strip()
        lower = stripped.lower()
        
        # Title
        if lower.startswith('title:'):
            self.tokenizer.consume_line()
            return TitleNode(stripped[6:].strip())
        
        # Section definition
        if lower.startswith('sec:') and '=' not in stripped[:4]:
            self.tokenizer.consume_line()
            sec_id = stripped[4:].strip()
            return SectionDefNode(sec_id)
        
        # Section link
        if lower.startswith('sec='):
            self.tokenizer.consume_line()
            match = re.match(r'sec=([^:]+):\s*(.*)', stripped, re.IGNORECASE)
            if match:
                return SectionLinkNode(match.group(1).strip(), match.group(2).strip())
        
        # Paragraph
        if lower.startswith('para:'):
            self.tokenizer.consume_line()
            return ParagraphNode(stripped[5:].strip())
        
        # Break line
        if lower in ['break-line', 'break-line:']:
            self.tokenizer.consume_line()
            return BreakLineNode()
        
        # Ordered/unordered list
        if lower.startswith('olist:'):
            return self._parse_list(stripped)
        
        # Code block
        if lower == 'code:':
            return self._parse_code_block()
        
        # Image
        if lower.startswith('img:='):
            self.tokenizer.consume_line()
            return self._parse_image(stripped[5:])
        
        # Links
        if lower.startswith('link:'):
            self.tokenizer.consume_line()
            return LinkNode(stripped[5:].strip())
        
        if lower.startswith('linktxt:'):
            self.tokenizer.consume_line()
            return self._parse_link_text(stripped[8:])
        
        # Cross-file navigation
        if lower.startswith('opensn='):
            self.tokenizer.consume_line()
            match = re.match(r'opensn=([^:]+):\s*(.*)', stripped, re.IGNORECASE)
            if match:
                return OpenSNNode(match.group(1).strip(), match.group(2).strip())
        
        # End new SN
        if lower.startswith('endnewsn:'):
            self.tokenizer.consume_line()
            return EndNewSNNode(stripped[9:].strip())
        
        # Signature
        if lower.startswith('sign:'):
            self.tokenizer.consume_line()
            return SignatureNode(stripped[5:].strip())
        
        # Close
        if lower == 'close:':
            self.tokenizer.consume_line()
            return CloseNode()
        
        # Unknown command
        if self.mode == ParseMode.STRICT:
            raise ValueError(f"Unknown command in strict mode: {line}")
        else:
            self.tokenizer.consume_line()
            return UnknownNode(line)
    
    def _parse_list(self, first_line: str) -> ListNode:
        """Parse a list block"""
        # Extract list type
        match = re.match(r'olist:(bullet|numbers)', first_line, re.IGNORECASE)
        if not match:
            raise ValueError(f"Invalid list type: {first_line}")
        
        list_type = match.group(1).lower()
        self.tokenizer.consume_line()
        
        items = []
        while self.tokenizer.has_more():
            line = self.tokenizer.peek_line()
            
            # Stop on blank line or new command
            if self.tokenizer.is_blank(line):
                break
            if self.tokenizer.is_comment(line):
                self.tokenizer.consume_line()
                continue
            
            # Check if it's a command (starts with known keyword followed by :)
            if self._looks_like_command(line):
                break
            
            self.tokenizer.consume_line()
            items.append(line.strip())
        
        return ListNode(list_type, items)
    
    def _parse_code_block(self) -> CodeBlockNode:
        """Parse a code block"""
        self.tokenizer.consume_line()  # consume 'code:'
        
        code_lines = []
        while self.tokenizer.has_more():
            line = self.tokenizer.peek_line()
            
            if line.strip().lower() == 'endcode:':
                self.tokenizer.consume_line()
                break
            
            self.tokenizer.consume_line()
            code_lines.append(line)
        
        return CodeBlockNode('\n'.join(code_lines))
    
    def _parse_image(self, content: str) -> ImageNode:
        """Parse image reference"""
        if '|' in content:
            parts = content.split('|', 1)
            return ImageNode(parts[0].strip(), parts[1].strip())
        return ImageNode(content.strip())
    
    def _parse_link_text(self, content: str) -> LinkTextNode:
        """Parse link with text"""
        # Try pipe separator first
        if '|' in content:
            parts = content.split('|', 1)
            return LinkTextNode(parts[0].strip(), parts[1].strip())
        # Try colon separator
        if ':' in content:
            parts = content.split(':', 1)
            return LinkTextNode(parts[0].strip(), parts[1].strip())
        
        return LinkTextNode(content, content)
    
    def _looks_like_command(self, line: str) -> bool:
        """Check if line looks like a command"""
        stripped = line.strip().lower()
        commands = [
            'title:', 'sec:', 'sec=', 'para:', 'break-line', 
            'olist:', 'code:', 'img:=', 'link:', 'linktxt:',
            'opensn=', 'endnewsn:', 'sign:', 'close:', 'meta:'
        ]
        return any(stripped.startswith(cmd) for cmd in commands)


# ============================================================================
# HTML Renderer
# ============================================================================

class HTMLRenderer:
    """Renders SN AST to HTML"""
    
    def __init__(self):
        self.output = []
    
    def render(self, doc: Document) -> str:
        """Render document to HTML"""
        self.output = []
        
        # HTML header
        title = self._extract_title(doc)
        self.output.append('<!DOCTYPE html>')
        self.output.append('<html lang="en">')
        self.output.append('<head>')
        self.output.append('    <meta charset="UTF-8">')
        self.output.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
        self.output.append(f'    <title>{html.escape(title)}</title>')
        self.output.append('    <style>')
        self.output.append(self._get_default_css())
        self.output.append('    </style>')
        self.output.append('</head>')
        self.output.append('<body>')
        self.output.append('<div class="sn-document">')
        
        # Render nodes
        for node in doc.nodes:
            self._render_node(node)
        
        # Seal indicator
        if doc.is_closed and doc.signature:
            self.output.append('<div class="sn-seal">🔒 Document sealed and signed</div>')
        
        self.output.append('</div>')
        self.output.append('</body>')
        self.output.append('</html>')
        
        return '\n'.join(self.output)
    
    def _extract_title(self, doc: Document) -> str:
        """Extract document title"""
        for node in doc.nodes:
            if isinstance(node, TitleNode):
                return node.text
        return "Untitled Document"
    
    def _render_node(self, node: ASTNode):
        """Render a single AST node"""
        if isinstance(node, TitleNode):
            self.output.append(f'<h1 class="sn-title">{self._format_inline(node.text)}</h1>')
        
        elif isinstance(node, SectionDefNode):
            self.output.append(f'<h2 id="{html.escape(node.section_id)}" class="sn-section">{html.escape(node.section_id)}</h2>')
        
        elif isinstance(node, SectionLinkNode):
            self.output.append(f'<p><a href="#{html.escape(node.section_id)}">{self._format_inline(node.text)}</a></p>')
        
        elif isinstance(node, ParagraphNode):
            self.output.append(f'<p class="sn-para">{self._format_inline(node.text)}</p>')
        
        elif isinstance(node, BreakLineNode):
            self.output.append('<hr class="sn-break">')
        
        elif isinstance(node, ListNode):
            tag = 'ol' if node.list_type == 'numbers' else 'ul'
            self.output.append(f'<{tag} class="sn-list">')
            for item in node.items:
                self.output.append(f'    <li>{self._format_inline(item)}</li>')
            self.output.append(f'</{tag}>')
        
        elif isinstance(node, CodeBlockNode):
            escaped = html.escape(node.code)
            self.output.append('<pre class="sn-code"><code>')
            self.output.append(escaped)
            self.output.append('</code></pre>')
        
        elif isinstance(node, ImageNode):
            alt = html.escape(node.alt_text) if node.alt_text else ""
            self.output.append(f'<img src="{html.escape(node.path)}" alt="{alt}" class="sn-image">')
        
        elif isinstance(node, LinkNode):
            self.output.append(f'<p><a href="{html.escape(node.url)}" class="sn-link">{html.escape(node.url)}</a></p>')
        
        elif isinstance(node, LinkTextNode):
            self.output.append(f'<p><a href="{html.escape(node.url)}" class="sn-link">{self._format_inline(node.text)}</a></p>')
        
        elif isinstance(node, OpenSNNode):
            self.output.append(f'<p><a href="{html.escape(node.location)}" class="sn-opensn">{self._format_inline(node.text)}</a></p>')
        
        elif isinstance(node, EndNewSNNode):
            self.output.append(f'<div class="sn-next"><a href="{html.escape(node.filepath)}">Next: {html.escape(node.filepath)} →</a></div>')
        
        elif isinstance(node, UnknownNode):
            self.output.append(f'<p class="sn-unknown">{html.escape(node.raw_text)}</p>')
    
    def _format_inline(self, text: str) -> str:
        """Process inline formatting"""
        # Escape HTML first
        result = html.escape(text)
        
        # Handle escaped braces {{  }}
        result = result.replace('{{', '\x00LEFTBRACE\x00')
        result = result.replace('}}', '\x00RIGHTBRACE\x00')
        
        # Bold: {b:...} or {bold:...}
        result = re.sub(r'\{b:(.*?)\}', r'<strong>\1</strong>', result, flags=re.IGNORECASE)
        result = re.sub(r'\{bold:(.*?)\}', r'<strong>\1</strong>', result, flags=re.IGNORECASE)
        
        # Italic: {i:...} or {italic:...}
        result = re.sub(r'\{i:(.*?)\}', r'<em>\1</em>', result, flags=re.IGNORECASE)
        result = re.sub(r'\{italic:(.*?)\}', r'<em>\1</em>', result, flags=re.IGNORECASE)
        
        # Underline: {u:...}
        result = re.sub(r'\{u:(.*?)\}', r'<u>\1</u>', result, flags=re.IGNORECASE)
        
        # Color: {color=name|#hex:...}
        result = re.sub(
            r'\{color=([^:]+):(.*?)\}',
            lambda m: f'<span style="color: {html.escape(m.group(1))}">{m.group(2)}</span>',
            result,
            flags=re.IGNORECASE
        )
        
        # Restore escaped braces
        result = result.replace('\x00LEFTBRACE\x00', '{')
        result = result.replace('\x00RIGHTBRACE\x00', '}')
        
        return result
    
    def _get_default_css(self) -> str:
        """Get default CSS for rendered HTML"""
        return """
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        .sn-document {
            background: #fff;
        }
        .sn-title {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        .sn-section {
            color: #34495e;
            margin-top: 2em;
            margin-bottom: 1em;
            border-bottom: 1px solid #ecf0f1;
            padding-bottom: 5px;
        }
        .sn-para {
            margin: 1em 0;
            text-align: justify;
        }
        .sn-break {
            margin: 2em 0;
            border: none;
            border-top: 2px solid #bdc3c7;
        }
        .sn-list {
            margin: 1em 0;
            padding-left: 2em;
        }
        .sn-list li {
            margin: 0.5em 0;
        }
        .sn-code {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: 'Courier New', Courier, monospace;
            font-size: 14px;
        }
        .sn-code code {
            background: none;
            color: inherit;
        }
        .sn-image {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 1em 0;
            border-radius: 5px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .sn-link, .sn-opensn {
            color: #3498db;
            text-decoration: none;
        }
        .sn-link:hover, .sn-opensn:hover {
            text-decoration: underline;
        }
        .sn-next {
            margin-top: 3em;
            padding: 15px;
            background: #ecf0f1;
            border-left: 4px solid #3498db;
            border-radius: 3px;
        }
        .sn-next a {
            color: #2c3e50;
            text-decoration: none;
            font-weight: bold;
        }
        .sn-seal {
            margin-top: 3em;
            padding: 15px;
            background: #d5f4e6;
            border: 2px solid #27ae60;
            border-radius: 5px;
            text-align: center;
            color: #27ae60;
            font-weight: bold;
        }
        .sn-unknown {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 10px;
            margin: 1em 0;
            font-family: monospace;
        }
        """
