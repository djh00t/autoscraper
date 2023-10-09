###
### Scraper Testing - Trainer
###
# Load modules
import os
from autoscraper import AutoScraper

# Training array
data = [
    # Woolworths Half-Price Specials
    ('https://www.woolworths.com.au/shop/browse/specials/half-price', [' Half Price ','Doritos Corn Chips Cheese Supreme Share Pack 170g','Cheezels Cheese Box 125g','Thins Chips Original 175g','Thins Chips Light & Tangy 175g','Mars Chocolate Bar With Nougat & Caramel 47g']),
    #('https://www.woolworths.com.au/shop/browse/specials/half-price', [' Half Price ','https://www.woolworths.com.au/shop/productdetails/826731/doritos-corn-chips-cheese-supreme-share-pack','https://www.woolworths.com.au/shop/productdetails/660337/cheezels-cheese-box','https://www.woolworths.com.au/shop/productdetails/274324/thins-chips-original','https://www.woolworths.com.au/shop/productdetails/274326/thins-chips-light-tangy','https://www.woolworths.com.au/shop/productdetails/160905/mars-chocolate-bar-with-nougat-caramel']),
    # some Ebay examples
    # ('https://www.ebay.com/itm/195583842395', ['Boxed Sony Playstation 4 PS4 Pro 1Tb Black Console', 'Used', '3 available', '2 sold', 'Shipping: AU $21.95', 'Located in: Brookfield, Australia', 'AU $478.80']),
#    ('https://www.ebay.com/itm/195583842395', ['Boxed Sony Playstation 4 PS4 Pro 1Tb Black Console', 'AU $478.80']),
#    ('https://www.ebay.com/itm/285200383550', ['NVIDIA GeForce RTX 4090 Founders Edition 24GB GDDR6X Graphics Card', 'US $2,100.00']),
#    ('https://www.ebay.com/itm/354451590518', ["8PCS Whopper Plopper 4'' Floating Bait Rotating Tail Fishing Lures For Bass Set", 'US $8.99']),

    #some Walmart examples
    #('https://www.walmart.com/ip/Slumber-1-By-Zinus-6-Comfort-Innerspring-Mattress-Twin/1040702932', ['<title>Slumber 1 By Zinus 6" Comfort Innerspring Mattress, Twin - Walmart.com</title>', '<span aria-hidden="true" itemprop="price">$65.00</span>', '<div class="f7 f6-l gray ml1 ttc strike" aria-hidden="true">$73.00</div>']),
    #('https://www.walmart.com/ip/LG-55-Class-4K-UHD-2160P-webOS-Smart-TV-55UQ7070ZUE/332111459', ['<title>LG 55" Class 4K UHD 2160P webOS Smart TV - 55UQ7070ZUE - Walmart.com</title>', '$358.00', '$448.00']),
    #('https://www.walmart.com/ip/Joyracer-4x4-24V-Kids-Ride-Car-Truck-w-2-Seater-Remote-Control-4-200W-Motor-9AH-Battery-Powered-Electric-Toys-Car-3-Speeds-Wheels-Spring-Suspension-B/565366581', ['Joyracer 4x4 24V Kids Ride on Car Truck w/ 2 Seater Remote Control, 4*200W Motor 9AH Battery Powered Electric Ride on Toys Car, 3 Speeds, Wheels,Spring Suspension, Bluetooth Music for Girls Boys Black - Walmart.com', '$329.99', '$589.99']),

    #some Etsy examples
#    ('https://www.etsy.com/listing/805075149/starstruck-silk-face-mask-black-silk', ['StarStruck Silk Face Mask, Black Silk and Cotton Mask, Nose Wire Mask, Filter Pocket Mask, Washable Silk and Cotton Mask, Made in USA', 'AU$19.67']),
#    ('https://www.etsy.com/au/listing/493287626/white-snowboarding-evolution-sticker', ['White Snowboarding evolution sticker', 'AU$16.39']),
]

scraper = AutoScraper()

###
### Training Code
###
def check_file_exists(filename):
    """Checks if a file exists in the current directory."""
    return os.path.isfile(filename)

# Loop through the training data
for url, wanted_list in data:
    """Checks if the file `shopping-scraper` exists and runs scraper.load() if it does."""
    if check_file_exists('shopping-scraper'):
        scraper.load('shopping-scraper')
    result=scraper.build(url=url, wanted_list=wanted_list, update=True)
    scraper.save('shopping-scraper')
    print(result)

