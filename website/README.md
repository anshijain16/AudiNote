# Website Starter

A clean, responsive static website with dark mode, mobile navigation, and a basic contact form demo.

## Structure

```
website/
├─ index.html
├─ assets/
│  ├─ css/
│  │  └─ styles.css
│  ├─ js/
│  │  └─ main.js
│  └─ img/
│     └─ favicon.svg
```

## Features

- Responsive layout and accessible semantics
- Auto dark mode with manual toggle (persisted)
- Mobile menu toggle and focus-visible styles
- Contact form validation with demo submit

## Run locally

Open `index.html` directly in a browser, or serve the folder with a static server:

```bash
# Using Python 3
cd /workspace/website
python3 -m http.server 8000
# Then visit http://localhost:8000
```

Or with Node.js:

```bash
npm -g install serve
serve -l 8000 .
```

## Customization

- Update branding by editing the `logo` text in the nav and the hero copy in `index.html`.
- Tweak colors in `assets/css/styles.css` under the `:root` variables.
- Replace `assets/img/favicon.svg` with your own.

## License

MIT