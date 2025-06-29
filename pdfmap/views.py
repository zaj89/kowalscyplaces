from django.shortcuts import render
from django.conf import settings
import os
import pdfplumber
import re
import urllib.parse

UPLOAD_FOLDER = os.path.join(settings.BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def is_address_continuation(text):
    return bool(re.search(r'\d{2}-\d{3}|ul\.|[0-9]{1,4}[A-Za-z]?|,', text))


def extract_addresses_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        lines = []
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines.extend(text.splitlines())

    addresses = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        match = re.search(r"(Zaladunek|Rozładunek)", line, re.IGNORECASE)
        if match:
            split_parts = re.split(r"Zaladunek|Rozładunek", line, flags=re.IGNORECASE)
            address_part = split_parts[1].strip() if len(split_parts) > 1 else ""
            if not address_part and i + 1 < len(lines):
                address_part = lines[i + 1].strip()
                i += 1
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if is_address_continuation(next_line):
                        address_part += " " + next_line
                        i += 1
            addresses.append(address_part)
        i += 1
    return ["My Location"] + addresses


def generate_google_maps_link(addresses):
    origin = urllib.parse.quote_plus("My Location", safe=",")
    destination = urllib.parse.quote_plus(addresses[-1], safe=",")
    waypoints = [urllib.parse.quote_plus(addr, safe=",") for addr in addresses[:-1]]
    base_url = "https://www.google.com/maps/dir/?api=1"
    link = f"{base_url}&origin={origin}&destination={destination}"
    if waypoints:
        link += "&waypoints=" + "|".join(waypoints)
    return link


def index(request):
    if request.method == "POST":
        if "pdf" not in request.FILES:
            return render(request, "pdfmap/index.html", {"error": "Brak pliku PDF"})
        file = request.FILES["pdf"]
        if file.name == "":
            return render(request, "pdfmap/index.html", {"error": "Nie wybrano pliku"})

        file_path = os.path.join(UPLOAD_FOLDER, file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        addresses = extract_addresses_from_pdf(file_path)
        link = generate_google_maps_link(addresses)
        return render(request, "pdfmap/index.html", {"addresses": addresses, "link": link})
    return render(request, "pdfmap/index.html")
