from django.core.management.base import BaseCommand
from base.models import SupportLink
import requests
from bs4 import BeautifulSoup
from django.db import transaction


class Command(BaseCommand):
    help = "Run the scraping logic"

    def handle(self, *args, **kwargs):
        supportForYouURL = "https://www.qub.ac.uk/students/"

        try:
            support_links = self.scrape_support_for_you(supportForYouURL)

            if support_links:
                with transaction.atomic():
                    # Save the extracted support links to the database
                    for link_info in support_links:
                        for link_data in link_info.get("Links", []):
                            link_text = link_data.get(
                                "Link Text", ""
                            )  # Check for existence
                            link_url = link_data.get("Link URL", "")
                            support_link = SupportLink(
                                url=supportForYouURL,
                                link_text=link_text,
                                link_url=link_url,
                            )
                            support_link.save()
            else:
                self.stdout.write(
                    self.style.ERROR("Failed to scrape Support for You links.")
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))

    def scrape_support_for_you(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

            page_content = response.text
            soup = BeautifulSoup(page_content, "html.parser")

            # Find the main accordion section
            accordion = soup.find(
                "ul", class_="accordion accordion-boxed accordion-large bg-white"
            )

            if accordion:
                support_links = []

                # Iterate through each accordion item
                accordion_items = accordion.find_all("li", class_="accordion-item")
                for item in accordion_items:
                    # Extract the title of the accordion section
                    title = item.find("a", class_="accordion-title")
                    if title:
                        section_title = title.text.strip()

                        # Extract links within the accordion content
                        content_links = []
                        content = item.find("div", class_="accordion-content")
                        if content:
                            link_items = content.find_all("li")
                            for link_item in link_items:
                                link = link_item.find("a")
                                if link:
                                    link_text = link.text.strip()
                                    link_url = link.get("href")
                                    content_links.append(
                                        {"Link Text": link_text, "Link URL": link_url}
                                    )
                                else:
                                    print("No link found in the accordion content.")

                        support_links.append(
                            {"Section Title": section_title, "Links": content_links}
                        )
                    else:
                        print("No title found for accordion item.")

                return support_links

        except requests.exceptions.RequestException as re:
            raise Exception(f"Request error: {str(re)}")
        except Exception as e:
            raise Exception(f"Parsing error: {str(e)}")

        return None
