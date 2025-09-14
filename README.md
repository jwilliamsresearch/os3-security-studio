# OS³ Website

A modern, responsive promotional website for the OS³ (Open Source Security Studio) cyber security education platform by James Williams.

## 🌟 Features

- **Modern Design**: Clean, professional layout with smooth animations
- **Fully Responsive**: Optimized for desktop, tablet, and mobile devices
- **Interactive Elements**: Animated terminal, smooth scrolling, and hover effects
- **Performance Optimized**: Fast loading with minimal dependencies
- **SEO Friendly**: Proper meta tags and semantic HTML structure
- **Accessibility**: WCAG compliant with keyboard navigation support
- **Documentation Site**: Dedicated documentation section with VitePress-inspired design

## 🚀 Quick Start

### Development
```bash
# Serve locally (Python)
cd os3-website
python -m http.server 8000

# Or use Node.js
npx http-server .

# Or use PHP
php -S localhost:8000
```

Visit `http://localhost:8000` to view the website.

### GitHub Pages Deployment

1. Push this folder to your GitHub repository
2. Go to repository Settings → Pages
3. Select source branch (usually `main`)
4. Set folder to `/os3-website` (if in subdirectory)
5. Website will be available at `https://yourusername.github.io/repository-name/`

## 📁 File Structure

```
os3-website/
├── index.html              # Main website file
├── documentation/          # Documentation site
│   ├── index.html         # Documentation coming soon page
│   └── assets/
│       ├── css/
│       │   └── docs.css   # Documentation-specific styling
│       └── js/
│           └── docs.js    # Documentation functionality
├── assets/
│   ├── css/
│   │   └── styles.css      # All styling and responsive design
│   ├── js/
│   │   └── main.js         # Interactive functionality
│   └── images/
│       ├── os3-logo.png    # OS³ logo
│       └── favicon.ico     # Website favicon
└── README.md               # This file
```

## 🎨 Customization

### Colors
Edit CSS variables in `assets/css/styles.css`:
```css
:root {
    --primary-color: #2563eb;      /* Main brand color */
    --secondary-color: #1f2937;    /* Dark sections */
    --accent-color: #10b981;       /* Success/accent color */
    /* ... more variables */
}
```

### Content
- **Hero Section**: Update title, subtitle, and stats in `index.html`
- **Features**: Modify the features grid to highlight key benefits
- **Modules**: Add or remove security module cards
- **Installation**: Update GitHub repository URLs and commands

### Branding
- Replace `assets/images/os3-logo.png` with your logo
- Update meta tags for SEO and social sharing
- Modify footer with your contact information

## 🛠 Technical Details

### Dependencies
- **Font Awesome**: Icons (CDN)
- **Google Fonts**: Inter and JetBrains Mono (CDN)
- **No frameworks**: Pure HTML, CSS, and JavaScript

### Browser Support
- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

### Performance
- Optimized images and minimal HTTP requests
- CSS and JS minification ready
- Lazy loading for images
- Smooth animations with hardware acceleration

## 📱 Responsive Breakpoints

- **Desktop**: 1024px+
- **Tablet**: 768px - 1023px
- **Mobile**: < 768px

## 🎯 SEO Features

- Semantic HTML5 structure
- Open Graph meta tags for social sharing
- Twitter Card support
- Proper heading hierarchy
- Alt tags for all images
- Structured data ready

## 🔧 Development Tips

### Adding New Sections
1. Add HTML structure to `index.html`
2. Style in `assets/css/styles.css`
3. Add interactions in `assets/js/main.js`
4. Update navigation if needed

### Image Optimization
- Use WebP format for better compression
- Provide fallbacks for older browsers
- Optimize file sizes for web delivery

### Performance Monitoring
```javascript
// Built-in performance logging
window.addEventListener('load', function() {
    console.log('Page loaded in:', performance.now(), 'ms');
});
```

## 📋 Deployment Checklist

- [ ] Update all GitHub repository URLs
- [ ] Replace placeholder content with actual information
- [ ] Optimize and compress images
- [ ] Test on multiple devices and browsers
- [ ] Validate HTML and CSS
- [ ] Check accessibility with screen readers
- [ ] Verify all links work correctly
- [ ] Test contact forms (if added)
- [ ] Set up analytics (Google Analytics, etc.)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

The OS³ platform uses dual licensing:
- **Software/Code**: [MIT License](../LICENSE.md#software-license-mit)
- **Website Content**: [Creative Commons Attribution 4.0 International (CC BY 4.0)](../LICENSE.md#content-license-cc-by-40)

This website content is licensed under CC BY 4.0 by James Williams.

## 🆘 Support

For issues or questions about the website:
- Open an issue on GitHub
- Contact: [your-email@domain.com]
- Documentation: [link-to-docs]

---

**Note**: This is a static website template. For dynamic features (contact forms, user accounts, etc.), you'll need to integrate with backend services or serverless functions.
