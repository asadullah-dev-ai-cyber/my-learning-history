import requests
from bs4 import BeautifulSoup
import smtplib

# 1. The Amazon URL you are scraping
url = "https://www.amazon.com/Meta-Quest-512GB-Digital-Currency-Code/dp/B0GX2SDKW9/"

# 2. Headers to make our script look like a real browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

# 3. Download the page content
response = requests.get(url, headers=headers)
print(f"Response Status Code: {response.status_code}") # 200 means success!

# 4. Feed the raw HTML into BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

print("\n--- Scraping Results ---")

# 5. Extract the Product Title
title_element = soup.find(id="productTitle")
product_title = title_element.get_text().strip() if title_element else "Meta Quest 3"

# 6. Extract the Product Price
price_element = soup.find("span", class_="a-offscreen")
if price_element:
    product_price = price_element.get_text().strip()
    price_as_float = float(product_price.split("$")[1])

    print(f"Current Price: ${price_as_float}")

    TARGET_PRICE = 650.00

    if price_as_float <= TARGET_PRICE:
        print("Price dropped! Attempting to send email...")

        EMAIL_ADDRESS = "pythonunknown2026@gmail.com"
        PASSWORD = "yaju dmrj xljo jvht"
        SMTP_SERVER = "smtp.gmail.com"

        message = f"Subject: Amazon Price Alert!\n\n{product_title} is now ${price_as_float}!\nBuy it here: {url}"


        try:
            with smtplib.SMTP(SMTP_SERVER, 587) as connection:
                connection.starttls()
                connection.login(user=EMAIL_ADDRESS, password=PASSWORD)
                connection.sendmail(
                    from_addr=EMAIL_ADDRESS,
                    to_addrs="habibya1401@gmail.com",
                    msg = message.encode('utf-8')
                )
            print("Email sent successfully! 🚀")

        except Exception as e:
            print(f"Error sending email: {e}")
    else:
        print(f"No discount yet. The price (${price_as_float}) is still above your target (${TARGET_PRICE}).")
else:
    print("Could not retrieve the price from the page.")