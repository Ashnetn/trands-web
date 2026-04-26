# Trands - High Performance Electronics

This is a modern eCommerce web application for Trands, an electronics store, built with HTML, Tailwind CSS, and vanilla JavaScript. The project features a high-fidelity, professional-grade design tailored for electronics products.

## Pages Included

*   **`index.html`** - Main Homepage featuring hero banners, product categories, featured products, and promotional sections.
*   **`about.html`** - About Us page detailing the company's story, mission, and team.
*   **`products.html`** - Product Category Hub for navigating through different types of electronics.
*   **`headphones.html`** - A sample category page specifically for headphones, with filtering and sorting options.
*   **`product-details.html`** - Detailed view for an individual product, including image galleries, specifications, and add-to-cart functionality.
*   **`contact.html`** - Contact Us page with contact information and a message form.
*   **`service.html`** - Services & Warranty information page.

## Technologies Used

*   **HTML5**
*   **Tailwind CSS** (via CDN for rapid styling)
*   **JavaScript** (for interactivity like mobile menus, carousels, and UI states)
*   **Font Awesome / Phosphor Icons** (for UI iconography)

## Getting Started

Because this project consists of static files, no build step is strictly required to view the pages. 

### Option 1: Direct File Access
You can simply double-click any of the `.html` files in your file explorer to open them directly in your web browser.

### Option 2: Local Development Server (Recommended)
For the best experience, especially if using certain browser features that require a server environment (like some local storage or fetch API calls in the future), use a simple local server.

If you have Node.js installed, you can use `npx serve`:

```bash
npx serve .
```

Or using Python:

```bash
python -m http.server 8000
```

Then navigate to `http://localhost:8000` (or the port provided by your server) in your browser.
