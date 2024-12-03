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
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
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
                    max-width: 220px;
                    height: auto;
                }}
                a {{
                    color: #0073bb;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <h1>Amazon Search Results - {query}</h1>
            <table border="1" cellpadding="10">
                <tr>
                    <th>Image</th>
                    <th>Product Name</th>
                    <th>Rating</th>
                    <th>Reviews</th>
                    <th>Price</th>
                </tr>
    """

    for result in results:
        html += f"""
        <tr>
            <td><img src="{result['image']}" alt="Product Image"></td>
            <td><a href="{result['url']}" target="_blank">{result['name']}</a></td>
            <td>{result['rating']} stars</td>
            <td>{result['reviews']} reviews</td>
            <td>{result['price']}</td>
        </tr>
        """

    html += """
            </table>
        </body>
    </html>
    """
    return html
