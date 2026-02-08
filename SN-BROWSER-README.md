# Super Notation Browser - Web Application

A beautiful, single-file web application for viewing Super Notation (SN v1.0) documents in your browser.

## 🌟 Features

- **📁 File Upload** - Drag and drop or select `.sn` files from your computer
- **🔗 URL Loading** - Load SN files from any accessible URL
- **🎨 Beautiful Rendering** - Modern, responsive design with gradient backgrounds
- **📱 Mobile Friendly** - Works great on all devices
- **⚡ Fast** - Pure JavaScript, no dependencies, instant parsing
- **🔒 Signature Display** - Shows when documents are sealed and signed
- **📋 Metadata Panel** - Displays document metadata clearly
- **🎯 Zero Setup** - Single HTML file, works offline

## 🚀 Quick Start

### Option 1: Direct Use
1. Download `sn-browser.html`
2. Open it in any modern web browser
3. Upload an SN file or enter a URL
4. Done! 🎉

### Option 2: Host it
```bash
# Simple HTTP server (Python)
python -m http.server 8000

# Or with Node.js
npx http-server

# Then open: http://localhost:8000/sn-browser.html
```

### Option 3: Deploy Online
Upload `sn-browser.html` to:
- GitHub Pages
- Netlify
- Vercel
- Any static hosting service

## 📖 How to Use

### Upload a File
1. Click "Choose File" button
2. Select your `.sn` file
3. Document renders automatically

### Load from URL
1. Paste URL in the text field
2. Click "Load" or press Enter
3. Document fetches and renders

**Example URLs you can try:**
- `https://example.com/docs/manual.sn`
- `https://raw.githubusercontent.com/user/repo/main/doc.sn`

## 🎨 Supported Features

### All SN v1.0 Commands
- ✅ Document titles
- ✅ Sections with anchors
- ✅ Paragraphs with formatting
- ✅ Ordered/unordered lists
- ✅ Code blocks with syntax
- ✅ Images
- ✅ Links (internal and external)
- ✅ Multi-file navigation
- ✅ Document metadata
- ✅ Signature display

### Inline Formatting
- ✅ **Bold** text
- ✅ *Italic* text
- ✅ <u>Underlined</u> text
- ✅ Colored text
- ✅ Escaped braces

## 🔧 Technical Details

### Architecture
- **Parser**: Complete JavaScript implementation of SN v1.0 spec
- **Renderer**: HTML generator with CSS styling
- **UI**: Responsive single-page application
- **Size**: ~15 KB (single file, no dependencies)

### Browser Compatibility
- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers

### CORS Limitations
When loading from URLs:
- ✅ Same-origin files work perfectly
- ✅ URLs with CORS headers enabled work
- ❌ URLs without CORS may be blocked by browser

**Workaround**: Download the file and upload it instead.

## 📋 Example Usage

### Example 1: View Documentation
```
1. Open sn-browser.html
2. Click "Choose File"
3. Select your project's README.sn
4. Read beautifully rendered docs!
```

### Example 2: Share Documents
```
1. Host your .sn file online
2. Share the browser URL with the file URL as parameter
3. Example: sn-browser.html?url=https://example.com/doc.sn
```

### Example 3: Offline Documentation
```
1. Download sn-browser.html
2. Keep it with your .sn files
3. Open it anytime, anywhere
4. No internet needed!
```

## 🎨 Customization

The browser is a single HTML file with embedded CSS. You can easily customize:

### Change Colors
Edit the gradient background:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Adjust Typography
Modify fonts and sizes:
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', ...;
font-size: 1.05em;
```

### Customize Rendering
Edit the CSS classes:
- `.sn-title` - Document title
- `.sn-section` - Section headings
- `.sn-para` - Paragraphs
- `.sn-code` - Code blocks
- And more...

## 🔒 Security

- ✅ All content is HTML-escaped
- ✅ XSS protection built-in
- ✅ No external dependencies
- ✅ No data sent to servers
- ✅ Works 100% client-side
- ✅ Privacy-friendly

**Note**: When loading from URLs, be careful with untrusted sources.

## 📱 Mobile Usage

The browser is fully responsive:
- Touch-friendly buttons
- Readable text sizes
- Smooth scrolling
- Landscape/portrait support

## 🐛 Troubleshooting

### File won't upload
- Check file extension is `.sn`
- Try a different browser
- Check file isn't corrupted

### URL won't load
- Verify URL is accessible
- Check CORS headers on server
- Try downloading and uploading instead

### Formatting looks wrong
- Verify file follows SN v1.0 spec
- Check for syntax errors
- Try a valid example file first

### Browser compatibility
- Update to latest browser version
- Try Chrome/Firefox if issues persist
- Check JavaScript is enabled

## 🎓 Tips & Tricks

1. **Bookmark it**: Save the browser page for quick access
2. **Offline use**: Download and keep it with your docs
3. **Share easily**: Host online and share the link
4. **Mobile reading**: Perfect for documentation on the go
5. **Print friendly**: Use browser print for PDF export

## 📚 Example Files

The `sn-interpreter` directory includes example files you can test:
- `example_basic.sn` - Basic features demo
- `example_part1.sn` - Multi-file navigation (part 1)
- `example_part2.sn` - Multi-file navigation (part 2)

Try them to see the browser in action!

## 🔮 Future Enhancements

Possible additions (PRs welcome!):
- [ ] Dark mode toggle
- [ ] Print stylesheet
- [ ] Export to PDF
- [ ] Search within document
- [ ] Table of contents sidebar
- [ ] Signature verification
- [ ] Syntax highlighting for code
- [ ] Markdown export

## 📄 License

Same as the Super Notation project (SOCL 1.0).

## 🙏 Credits

- Built for Super Notation v1.0
- Pure JavaScript implementation
- No frameworks or libraries
- Designed for simplicity and speed

---

**Made with ❤️ for beautiful documentation**

Version: 1.0 (Compatible with SN v1.0 specification)
