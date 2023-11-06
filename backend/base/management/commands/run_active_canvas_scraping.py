from django.core.management.base import BaseCommand
from django.conf import settings  # Import Django settings
import requests
from bs4 import BeautifulSoup
from base.models import ScrapedData, Event


class Command(BaseCommand):
    help = "Run the active canvas scraping logic"

    def handle(self, *args, **kwargs):
        activeCanvasURL = "https://www.queenssport.com/StudentSport/ActiveCampus/"

        # Define a user-agent string for a popular web browser
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

        headers = {"User-Agent": user_agent}

        response = requests.get(activeCanvasURL, headers=headers)

        if response.status_code == 200:
            # You successfully retrieved the web page
            page_content = response.text

            soup = BeautifulSoup(page_content, "html.parser")

            # Find the table within the HTML
            table = soup.find("table")

            if table:
                # Once you have the table, you can extract and process its data
                rows = table.find_all("tr")
                scraped_data = []  # Initialize a list to store the scraped data

                for row in rows:
                    columns = row.find_all("td")
                    row_data = (
                        {}
                    )  # Initialize a dictionary to store data for the current row

                    if len(columns) == 7:
                        row_data["Event/Programme"] = columns[0].get_text()
                        row_data["Date"] = columns[1].get_text()
                        row_data["Duration"] = columns[2].get_text()
                        row_data["Day"] = columns[3].get_text()
                        row_data["Time"] = columns[4].get_text()
                        row_data["Venue"] = columns[5].get_text()
                        row_data["Registration"] = columns[6].get_text()
                        scraped_data.append(
                            row_data
                        )  # Add the row data to the scraped_data list

                for event_data in scraped_data:
                    event = Event(
                        name=event_data["Event/Programme"],
                        date=event_data["Date"],
                        duration=event_data["Duration"],
                        day=event_data["Day"],
                        time=event_data["Time"],
                        venue=event_data["Venue"],
                        registration=event_data["Registration"],
                    )
                    event.save()

                # Create a new ScrapedData instance for the entire table and save it
                scraped_item = ScrapedData(
                    url=activeCanvasURL,
                    title="Scraped Data",
                    description=str(scraped_data),
                )
                scraped_item.save()
            else:
                self.stdout.write(self.style.ERROR("Table not found on the page."))
        else:
            # Handle the error
            self.stdout.write(self.style.ERROR("Failed to fetch the web page."))
