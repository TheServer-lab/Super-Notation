#!/usr/bin/env python3
"""
Super Notation v1.0 - Signing and Verification Utilities

Implements the canonicalization and signature algorithm as per SN v1.0 spec.
"""

import hashlib
from typing import Tuple, Optional


def canonical_bytes(filepath: str) -> bytes:
    """
    Canonicalize SN file content for signing/verification.
    
    Process:
    1. Read as UTF-8, remove BOM if present
    2. Normalize line endings to LF
    3. Find the sign: line and exclude it and everything after
    4. Return the canonical bytes
    
    Args:
        filepath: Path to the .sn file
        
    Returns:
        Canonicalized bytes ready for hashing
    """
    # Read file as binary
    with open(filepath, 'rb') as f:
        content = f.read()
    
    # Remove BOM if present (UTF-8 BOM: EF BB BF)
    if content.startswith(b'\xef\xbb\xbf'):
        content = content[3:]
    
    # Normalize line endings: CRLF -> LF, CR -> LF
    content = content.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
    
    # Split into lines
    lines = content.split(b'\n')
    
    # Find the sign: line
    for i, line in enumerate(lines):
        stripped = line.lstrip().lower()
        if stripped.startswith(b'sign:'):
            # Everything up to (but not including) this line
            canonical = b'\n'.join(lines[:i])
            return canonical
    
    # No signature found - return entire canonicalized content
    return content


def extract_signature(filepath: str) -> Optional[str]:
    """
    Extract the signature line from an SN file.
    
    Args:
        filepath: Path to the .sn file
        
    Returns:
        The signature string (e.g., "SHA256-ABC123...") or None if not found
    """
    with open(filepath, 'rb') as f:
        content = f.read()
    
    # Remove BOM if present
    if content.startswith(b'\xef\xbb\xbf'):
        content = content[3:]
    
    # Normalize line endings
    content = content.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
    
    # Split into lines
    lines = content.split(b'\n')
    
    # Find the sign: line
    for line in lines:
        stripped = line.strip()
        lower = stripped.lower()
        if lower.startswith(b'sign:'):
            # Extract signature value
            sig_line = stripped.decode('utf-8', errors='ignore')
            if ':' in sig_line:
                sig_value = sig_line.split(':', 1)[1].strip()
                return sig_value
    
    return None


def has_close_marker(filepath: str) -> bool:
    """
    Check if the file has a close: marker.
    
    Args:
        filepath: Path to the .sn file
        
    Returns:
        True if close: is present, False otherwise
    """
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.strip().lower() == 'close:':
                return True
    return False


def compute_signature(filepath: str) -> str:
    """
    Compute the SHA-256 signature for an SN file.
    
    Args:
        filepath: Path to the .sn file
        
    Returns:
        Signature string in format "SHA256-<HEX>"
    """
    canonical = canonical_bytes(filepath)
    hash_obj = hashlib.sha256(canonical)
    hex_digest = hash_obj.hexdigest().upper()
    return f"SHA256-{hex_digest}"


def verify_signature(filepath: str) -> Tuple[bool, str]:
    """
    Verify the signature of an SN file.
    
    Args:
        filepath: Path to the .sn file
        
    Returns:
        Tuple of (is_valid, message)
    """
    # Extract existing signature
    existing_sig = extract_signature(filepath)
    
    if existing_sig is None:
        return False, "No signature found in file"
    
    # Compute expected signature
    expected_sig = compute_signature(filepath)
    
    # Compare
    if existing_sig == expected_sig:
        # Check for close marker
        is_closed = has_close_marker(filepath)
        if is_closed:
            return True, f"✓ Signature valid and document is sealed: {expected_sig}"
        else:
            return True, f"✓ Signature valid (but document not sealed - missing close:): {expected_sig}"
    else:
        return False, f"✗ Signature mismatch!\nExpected: {expected_sig}\nFound:    {existing_sig}"


def sign_file(filepath: str, in_place: bool = False) -> str:
    """
    Sign an SN file.
    
    Args:
        filepath: Path to the .sn file
        in_place: If True, append signature to the file. If False, just return it.
        
    Returns:
        The signature string
    """
    signature = compute_signature(filepath)
    
    if in_place:
        # Read current content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove any existing signature and close
        lines = content.split('\n')
        filtered_lines = []
        for line in lines:
            stripped = line.strip().lower()
            if not (stripped.startswith('sign:') or stripped == 'close:'):
                filtered_lines.append(line)
        
        # Remove trailing blank lines
        while filtered_lines and filtered_lines[-1].strip() == '':
            filtered_lines.pop()
        
        # Append signature and close
        filtered_lines.append('')
        filtered_lines.append(f'sign: {signature}')
        filtered_lines.append('close:')
        
        # Write back
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(filtered_lines))
    
    return signature


def unsign_file(filepath: str) -> bool:
    """
    Remove signature and close marker from an SN file.
    
    Args:
        filepath: Path to the .sn file
        
    Returns:
        True if signature was removed, False if no signature was present
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    filtered_lines = []
    found_signature = False
    
    for line in lines:
        stripped = line.strip().lower()
        if stripped.startswith('sign:') or stripped == 'close:':
            found_signature = True
        else:
            filtered_lines.append(line)
    
    if found_signature:
        # Remove trailing blank lines
        while filtered_lines and filtered_lines[-1].strip() == '':
            filtered_lines.pop()
        
        # Write back
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(filtered_lines))
        
        return True
    
    return False
