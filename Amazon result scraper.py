import requests
from bs4 import BeautifulSoup
import webbrowser
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_amazon_search_results(query, pages=1, min_rating=4.3):
    results = []
    logging.info(f"Starting search for: {query}")

    for page in range(1, pages + 1):
        url = f"https://www.amazon.co.uk/s?k={query}&page={page}"
        try:
            logging.info(f"Fetching page {page}...")
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching page {page}: {e}")
            continue  # Skip this page and move on to the next one

        logging.info(f"Page {page} fetched successfully.")
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all product containers on the current page
        items = soup.select('.s-main-slot .s-result-item')

        for item in items:
            name_tag = item.select_one('h2 a')
            rating_tag = item.select_one('.a-icon-alt')
            reviews_tag = item.select_one('.a-size-base')
            price_tag = item.select_one('.a-price-whole')
            image_tag = item.select_one('.s-image')

            if name_tag and rating_tag and reviews_tag and price_tag and image_tag:
                name = name_tag.get_text(strip=True)
                url = 'https://www.amazon.co.uk' + name_tag['href']
                rating = float(rating_tag.get_text(strip=True).split()[0])

                if rating < min_rating:
                    logging.debug(f"Skipping {name} due to low rating: {rating}")
                    continue  # Skip items below minimum rating

                reviews = reviews_tag.get_text(strip=True).replace(",", "")
                try:
                    reviews = int(reviews) if reviews.isdigit() else 0
                except ValueError:
                    reviews = 0

                price = price_tag.get_text(strip=True).replace(",", "")
                try:
                    price = float(price)
                except ValueError:
                    price = 0.0

                # Get the image URL
                image_url = image_tag['src']

                results.append({
                    'name': name,
                    'url': url,
                    'rating': rating,
                    'reviews': reviews,
                    'price': f"£{price:.2f}".rstrip('0').rstrip('.'),  # Format the price
                    'image': image_url
                })
            else:
                # Log just the name if data is missing
                name = name_tag.get_text(strip=True) if name_tag else "Unnamed product"
                logging.warning(f"Missing data for item: {name}")

    # Remove duplicates by creating a set of seen URLs
    seen_urls = set()
    unique_results = []
    for result in results:
        if result['url'] not in seen_urls:
            seen_urls.add(result['url'])
            unique_results.append(result)

    # Sort results by the number of reviews, descending
    unique_results.sort(key=lambda x: x['reviews'], reverse=True)

    # Limit to the first 50 results
    unique_results = unique_results[:50]

    logging.info(f"Found {len(unique_results)} unique results.")
    return unique_results

def generate_html(results, query):
    html = f"""
    <html>
        <head>
            <title>Amazon Search Results - {query}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    font-size: 20px;
                    line-height: 1.6;
                    margin: 20px;
                }}
                h1 {{
                    font-size: 32px;
                    margin-bottom: 20px;
                    font-weight: 600;
                }}
                table {{
                    width: 70%;  /* Set the table to 70% of the screen width */
                    border-collapse: collapse;
                    margin-top: 20px;
                    table-layout: auto;  /* Allow columns to adjust based on content */
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    vertical-align: top;
                }}
                th {{
                    background-color: #f2f2f2;
                    font-size: 24px;
                    font-weight: 600;
                }}
                td {{
                    font-size: 20px;
                    word-wrap: break-word;
                    max-width: 300px;
                    overflow-wrap: break-word;
                    white-space: normal;
                }}
                img {{
                    max-width: 200px;  /* Limit the image size */
                    height: auto;
                    display: block;
                    margin: 0 auto;
                }}
                a {{
                    color: #0073bb;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
                .image-col {{
                    width: 150px;  /* Set fixed width for image column */
                    text-align: center;
                }}
                .name-col {{
                    width: 50%;  /* Wider width for Product Name column */
                }}
                .rating-col {{
                    width: 15%;  /* Set fixed width for rating column */
                }}
                .reviews-col {{
                    width: 15%;  /* Set fixed width for reviews column */
                }}
                .price-col {{
                    width: 10%;  /* Set fixed width for price column */
                }}
            </style>
        </head>
        <body>
            <h1>Amazon Search Results - {query}</h1>
            <table border="1" cellpadding="10">
                <tr>
                    <th class="image-col">Image</th>
                    <th class="name-col">Product Name</th>
                    <th class="rating-col">Rating</th>
                    <th class="reviews-col">Reviews</th>
                    <th class="price-col">Price</th>
                </tr>
    """

    for result in results:
        html += f"""
        <tr>
            <td class="image-col"><img src="{result['image']}" alt="Product Image"></td>
            <td class="name-col"><a href="{result['url']}" target="_blank">{result['name']}</a></td>
            <td class="rating-col">{result['rating']} stars</td>
            <td class="reviews-col">{result['reviews']} reviews</td>
            <td class="price-col">{result['price']}</td>
        </tr>
        """

    html += """
            </table>
        </body>
    </html>
    """
    return html


def main():
    query = "Network switch"  # Example search query
    pages = 5  # Number of pages to scrape
    min_rating = 4.3  # Minimum rating filter

    try:
        results = get_amazon_search_results(query, pages, min_rating)
        if not results:
            logging.warning("No results found.")
            return

        html = generate_html(results, query)

        # Save the results to an HTML file
        with open('amazon_results.html', 'w', encoding='utf-8') as f:
            f.write(html)

        # Open the results in the default web browser
        webbrowser.open('amazon_results.html')

    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
