import urllib.request
import json
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Fetch the last verse for a predefined list of Surahs from the Quran API and save to a text file'

    def handle(self, *args, **kwargs):
        surahs = [
            "78:40", "79:46", "80:42", "81:29", "82:19", "83:36", "84:25", "85:22", 
            "86:17", "87:19", "88:26", "89:30", "90:20", "91:15", "92:21", "93:11", 
            "94:8", "95:8", "96:19", "97:5", "98:8", "99:8", "100:11", "101:11", 
            "102:8", "103:3", "104:9", "105:5", "106:4", "107:7", "108:3", "109:6", 
            "110:3", "111:5", "112:4", "113:5", "114:6"
        ]
k
        # Open the text file for writing
        with open('last_verses.txt', 'w', encoding='utf-8') as file:
            for i in range(len(surahs) - 1):  # Loop through each pair of consecutive Surahs
                current_surah_verse = surahs[i]
                next_surah_verse = surahs[i + 1]

                current_surah_number, current_verse_number = current_surah_verse.split(":")
                next_surah_number, next_verse_number = next_surah_verse.split(":")

                # Fetch current surah details
                url_current = f"http://api.alquran.cloud/v1/ayah/{current_surah_number}:{current_verse_number}"
                url_next = f"http://api.alquran.cloud/v1/ayah/{next_surah_number}:1"

                try:
                    # Fetch current Surah data
                    with urllib.request.urlopen(url_current) as response:
                        data_current = json.loads(response.read().decode())
                        verse_text_current = data_current['data']['text']
                        surah_name_current = data_current['data']['surah']['name']
                        total_verses_current = data_current['data']['surah']['numberOfAyahs']

                    # Fetch next Surah data
                    with urllib.request.urlopen(url_next) as response:
                        data_next = json.loads(response.read().decode())
                        verse_text_next = data_next['data']['text']
                        surah_name_next = data_next['data']['surah']['name']
                        total_verses_next = data_next['data']['surah']['numberOfAyahs']

                    # Remove Basmala from the next verse if it exists
                    basmala = "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَـٰنِ ٱلرَّحِیمِ"
                    if verse_text_next.startswith(basmala):
                        verse_text_next = verse_text_next[len(basmala):].strip()

                    # Write the structured output to the file
                    file.write(f"{surah_name_current} ({current_surah_number} : {total_verses_current}) "
                               f"-----> {surah_name_next} ({next_surah_number} : {total_verses_next})\n")
                    file.write(f"{verse_text_current}\n")
                    file.write(f"---\n")  # Delimiter between verses
                    file.write(f"{verse_text_next}\n\n")

                    # Output success message
                    self.stdout.write(self.style.SUCCESS(
                        f"{surah_name_current} ({current_surah_number} : {total_verses_current}) "
                        f"-----> {surah_name_next} ({next_surah_number} : {total_verses_next})"
                    ))
                    self.stdout.write(self.style.SUCCESS(f"{verse_text_current}"))
                    self.stdout.write(self.style.SUCCESS(f"{verse_text_next}"))

                except Exception as e:
                    # Handle and log errors
                    error_message = f"Failed to fetch verse {current_surah_number}:{current_verse_number} or {next_surah_number}:1 - {e}"
                    file.write(error_message + "\n")
                    self.stdout.write(self.style.ERROR(error_message))
