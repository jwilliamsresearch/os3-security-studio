# OS³ Website Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: GitHub Pages (Recommended)

1. **Push to GitHub**:
   ```bash
   git add os3-website/
   git commit -m "Add OS³ promotional website"
   git push origin main
   ```

2. **Enable GitHub Pages**:
   - Go to your repository on GitHub
   - Click "Settings" tab
   - Scroll down to "Pages" section
   - Select source: "Deploy from a branch"
   - Choose branch: `main`
   - Choose folder: `/os3-website` (if in subdirectory)
   - Click "Save"

3. **Access your site**:
   - URL: `https://yourusername.github.io/repositoryname/os3-website/`
   - Updates automatically when you push changes

### Option 2: Netlify

1. **Connect Repository**:
   - Go to [netlify.com](https://netlify.com)
   - Click "New site from Git"
   - Connect your GitHub repository
   - Set build command: (leave empty for static site)
   - Set publish directory: `os3-website`

2. **Custom Domain** (optional):
   - Add your domain in Netlify dashboard
   - Update DNS records as instructed

### Option 3: Vercel

1. **Deploy**:
   ```bash
   npx vercel --cwd os3-website
   ```

2. **Follow prompts** to connect your GitHub account

### Option 4: Traditional Web Hosting

1. **Upload files**:
   - Use FTP/SFTP client
   - Upload entire `os3-website` folder
   - Ensure `index.html` is in the root

2. **Web servers**:
   - Apache: Works out of the box
   - Nginx: May need basic configuration
   - IIS: Enable static content serving

## 🔧 Pre-Deployment Checklist

### Content Updates
- [ ] Update GitHub repository URLs in HTML
- [ ] Replace placeholder email addresses
- [ ] Add actual social media links
- [ ] Update contact information in footer

### Technical Checks
- [ ] Test website locally
- [ ] Validate HTML: [W3C Validator](https://validator.w3.org/)
- [ ] Check CSS: [CSS Validator](https://jigsaw.w3.org/css-validator/)
- [ ] Test responsive design on multiple devices
- [ ] Verify all links work
- [ ] Check image loading
- [ ] Test JavaScript functionality

### SEO & Performance
- [ ] Add Google Analytics (optional)
- [ ] Submit to Google Search Console
- [ ] Test page speed: [PageSpeed Insights](https://pagespeed.web.dev/)
- [ ] Check mobile usability
- [ ] Verify Open Graph tags

### Security
- [ ] Ensure HTTPS is enabled
- [ ] Check for mixed content warnings
- [ ] Verify no sensitive information is exposed

## 📊 Analytics Setup (Optional)

### Google Analytics 4

1. **Create GA4 Property**:
   - Go to [analytics.google.com](https://analytics.google.com)
   - Create new property
   - Get Measurement ID

2. **Add to website**:
   ```html
   <!-- Add before closing </head> tag -->
   <script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
   <script>
     window.dataLayer = window.dataLayer || [];
     function gtag(){dataLayer.push(arguments);}
     gtag('js', new Date());
     gtag('config', 'GA_MEASUREMENT_ID');
   </script>
   ```

### Simple Analytics (Privacy-focused alternative)

1. **Sign up** at [simpleanalytics.com](https://simpleanalytics.com)
2. **Add script**:
   ```html
   <script async defer src="https://scripts.simpleanalyticscdn.com/latest.js"></script>
   ```

## 🌐 Custom Domain Setup

### For GitHub Pages

1. **Add CNAME file**:
   ```bash
   echo "yourdomain.com" > os3-website/CNAME
   ```

2. **Configure DNS**:
   - Add CNAME record: `www` → `yourusername.github.io`
   - Add A records for apex domain:
     ```
     185.199.108.153
     185.199.109.153
     185.199.110.153
     185.199.111.153
     ```

### SSL Certificate
- GitHub Pages: Automatic with custom domains
- Netlify: Automatic with Let's Encrypt
- Other hosts: May need manual setup

## 🔄 Continuous Deployment

### GitHub Actions (Advanced)

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to GitHub Pages
on:
  push:
    branches: [ main ]
    paths: [ 'os3-website/**' ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./os3-website
```

## 🐛 Troubleshooting

### Common Issues

1. **404 Error**:
   - Check file paths are correct
   - Ensure `index.html` is in root directory
   - Verify GitHub Pages is enabled

2. **CSS/JS Not Loading**:
   - Check relative paths in HTML
   - Ensure files are uploaded correctly
   - Check browser developer tools for errors

3. **Images Not Displaying**:
   - Verify image file extensions
   - Check file paths are correct
   - Ensure images are optimized and not too large

4. **Mobile Issues**:
   - Test viewport meta tag
   - Check responsive CSS breakpoints
   - Verify touch interactions work

### Support Resources
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Netlify Documentation](https://docs.netlify.com/)
- [Web Development MDN](https://developer.mozilla.org/)

---

**Success!** Your OS³ promotional website should now be live and promoting your cybersecurity education platform to the world! 🎉
