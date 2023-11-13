from django.core.management.base import BaseCommand
from base.models import SupportLink, SupportSection
import requests
from bs4 import BeautifulSoup
from django.db import transaction


class Command(BaseCommand):
    help = "Run the scraping logic"

    def handle(self, *args, **kwargs):
        supportForYouURL = "https://www.qub.ac.uk/students/"

        try:
            support_links_data = self.scrape_support_for_you(supportForYouURL)

            if support_links_data:
                with transaction.atomic():
                    for section_data in support_links_data:
                        section_title = section_data["Section Title"]
                        links_data = section_data["Links"]

                        # Create a SupportSection instance for the section title
                        section, created = SupportSection.objects.get_or_create(
                            title=section_title
                        )

                        # Create SupportLink instances for each link and associate them with the section
                        for link_data in links_data:
                            link_text = link_data["Link Text"]
                            link_url = link_data["Link URL"]

                            SupportLink.objects.create(
                                section=section, link_text=link_text, link_url=link_url
                            )
            else:
                self.stdout.write(
                    self.style.ERROR("Failed to scrape Support for You links.")
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))

    def scrape_support_for_you(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()

            page_content = response.text
            soup = BeautifulSoup(page_content, "html.parser")

            support_links = []

            # Find all accordion items
            accordion_items = soup.find_all("li", class_="accordion-item")
            for item in accordion_items:
                section_title = item.find("a", class_="accordion-title").text.strip()
                content_links = []

                # Find links within the accordion content
                link_items = item.find("div", class_="accordion-content").find_all("li")
                for link_item in link_items:
                    link = link_item.find("a")
                    if link:
                        link_text = link.text.strip()
                        link_url = link.get("href")
                        content_links.append(
                            {"Link Text": link_text, "Link URL": link_url}
                        )

                support_links.append(
                    {"Section Title": section_title, "Links": content_links}
                )

            return support_links

        except requests.exceptions.RequestException as re:
            raise Exception(f"Request error: {str(re)}")
        except Exception as e:
            raise Exception(f"Parsing error: {str(e)}")

        return None
