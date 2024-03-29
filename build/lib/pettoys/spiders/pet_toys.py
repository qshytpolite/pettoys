from typing import Iterable
import scrapy
from time import sleep


class PetToysSpider(scrapy.Spider):
    name = "pet_toys"
    visited_pages = 0
    download_delay = 3  # 3 seconds

    def start_requests(self):
        yield scrapy.Request(
            url="https://trading.made-in-china.com/deals/Toys-Catalog/Pet-Toys.html",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                errback=self.errback,
            ),
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()
        # Extracting product details
        print("Extracting product details")

        for product in response.css('.products-item'):
            item = {
                'title': product.css('.prod-title > a::text').get(),
                'price_per_piece': product.css('.J-faketitle.prod-price .price::text').get(),
                'minimum_order': product.css('.quantity-num::text').get(),
                'supplier': product.css('a.com-link::text').get(),
                'url': product.css('.prod-title > a[title]::attr(href)').get(),
            }

            print(f"Yielding item: {item}")
            yield item

        # Increment the visited pages count
        self.visited_pages += 1
        sleep(self.download_delay)  # Add a delay between requests

        # Check if the limit of 5 pages has been reached
        if self.visited_pages < 5:
            # Pagination (update if URLs are relative)
            # Assuming relative URL for pagination
            next_page_url = response.urljoin(
                response.css('a.main.nextpage::attr(href)').get()
            )
            if next_page_url:
                yield scrapy.Request(
                    next_page_url,
                    meta=dict(
                        playwright=True,
                        playwright_include_page=True,
                        errback=self.errback,
                    ),
                )

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
        print(failure)
