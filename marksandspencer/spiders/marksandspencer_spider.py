import scrapy

class MarksandspencerSpider(scrapy.Spider):
    name = "marksandspencer"
    allowed_domains = ["marksandspencer.com"]
    start_urls = ["https://www.marksandspencer.com/l/women/dresses"]

    def parse(self, response):
        # Product links: updated selector
        product_links = response.css('a.Product_tile::attr(href), a[href*="/p/"]::attr(href)').getall()
        for link in product_links:
            yield response.follow(link, callback=self.parse_product)

        # Pagination link
        next_page = response.css('a[aria-label="Next page"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        def extract(css):
            return response.css(css).get(default='').strip()

        yield {
            "product_url": response.url,
            "product_name": extract('h1::text'),
            "price": extract('span[data-test-id="price"]::text, span[class*="Price"]::text'),
            "color": extract('span[data-test-id="colour-name"]::text, span[class*="Colour"]::text'),
            "breadcrumb": " > ".join(response.css('nav[aria-label="breadcrumb"] a::text').getall()),
            "brand": "M&S Collection",
            "currency": "£",
            "review": extract('span[data-test-id="review-count"]::text, span[class*="ReviewCount"]::text'),
            "product_code": extract('span[data-test-id="product-code"]::text, p:contains("Product code")::text'),
            "description": " ".join(response.css('div[data-test-id="product-description"] *::text, section[class*="Description"] *::text').getall()).strip(),
            "image_urls": response.css('img::attr(src)').getall(),
        }
