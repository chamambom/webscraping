import requests
from bs4 import BeautifulSoup
import urllib3
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

pd.set_option('display.max_colwidth', -1)


# disable warnings (these are definitely not fatal)
urllib3.disable_warnings()

urls = {'Laptops': 'https://10ngah.com/704-laptop-deals', 'Perfumes': 'https://10ngah.com/345-perfume'}

print(
    "[Question i.] Use Beautifulsoup library and other useful libraries to download the data required from ZIMALL and TENGA")
print("[Question ii.] Clean and parse the data - below code scraps and cleans data for TENGA and ZIMALL")

dataframes = []
for name_of_url, url in urls.items():
    # Get URL and pass the verify=False parameter to ignore SSL cert checks

    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.content, 'lxml')

    headline = soup.find('h1', class_='page-heading')
    # print (headline.text)

    product_list = soup.find_all('div', class_='second-block')
    # number_of_products = len(product_list)
    COLUMNS = ['ProductName', 'Price(Now)', 'Price(Was)', 'Discount', 'Currency', 'Availability', 'Description']
    tenga_data = []
    for item in product_list:
        product_name = (item.h5.a.text)
        product_first_price = item.find('span', class_='price')
        # Below i sliced product price to get read of the funny character $ , well not a funny character
        # but just wanted to make the data statistically possible to use
        product_price = product_first_price.text[1:].replace(",", "")

        product_second_price = item.find('span', class_='regular-price')
        if product_second_price is not None:
            product_sec_price = product_second_price.text
        else:
            product_sec_price = "No original price"

        product_discount = item.find('span', class_='discount-product')
        if product_discount is not None:
            product_disc = product_discount.text
        else:
            product_disc = "No discount "

        product_currency = item.find("meta")
        prod_curr = product_currency["content"]

        product_availability = item.find('span', class_='available')
        if product_availability is not None:
            prod_avail = product_availability.text
        else:
            prod_avail = "No status given"

        product_description = item.find('div', class_='product-description-short')
        if product_description is not None:
            prod_desc = product_description.text
        else:
            prod_desc = "No description given"
        tenga_data.append(
            [product_name, product_price, product_sec_price, product_disc, prod_curr, prod_avail, prod_desc])
    dataframes.append(pd.DataFrame(tenga_data, columns=COLUMNS))

combined_laptop_and_perfume_dataframe_from_tenga = pd.concat(dataframes).reset_index(drop=True)

# Webscrapping code for zimall data

second_url = "https://www.zimall.co.zw/shop/categories/18/laptops-and-notebooks.html"
page = requests.get(second_url, verify=False)
soup = BeautifulSoup(page.content, 'lxml')

product_list_two = soup.find_all('div', class_='product-block')

COLS = ['ProductName', 'Price(Now)', 'Price(Was)', 'Currency', 'Description']
zimall_data = []
for item in product_list_two:
    product_name = (item.h4.a).text
    product_description = item.find('div', class_='product-desc').text
    product_price = item.find('span', itemprop='price').text
    second_price = item.find('span', class_='old-price product-price')
    if second_price is not None:
        second_pri = second_price.text
    else:
        second_pri = "No original price"

    product_currency = item.find("meta", itemprop='priceCurrency')
    prod_curr = product_currency["content"]

    zimall_data.append(
        [str(product_name), str(product_price[1:]).replace(",", ""), str(second_pri), str(prod_curr),
         product_description.strip()])

zimall_dataframe = pd.DataFrame(zimall_data, columns=COLS)

print("[Question iii.] Create a dataframe for products from ZIMALL")
print(zimall_dataframe)

print("[Question iv.] Create a dataframe for products from TENGA")
print(combined_laptop_and_perfume_dataframe_from_tenga)

print("[Question v.] How many products have you found at ZIMALL")
print(len(zimall_dataframe))

print("[Question v.] How many products have you found at TENGA")
print(len(combined_laptop_and_perfume_dataframe_from_tenga))

print("[Question vi.] Merge the two dataframes")
# I first need to make sure they both have the same columns so i need to drop some non essential columns that wont affect
# my statistics
tenga_and_zimall_merged_dataframe = pd.merge(zimall_dataframe, combined_laptop_and_perfume_dataframe_from_tenga,
                                             how='outer')
print(tenga_and_zimall_merged_dataframe)

print("[Question vii.] Using the analytics tools at your disposal find the average price for laptops at ZIMALL ")
prod_cur = zimall_dataframe["Currency"][
    0]  # could have written a function for this code but thats code optimisation , will consider it later
convert_price_to_numeric = pd.to_numeric(zimall_dataframe["Price(Now)"])
zimall_average_laptop_price = convert_price_to_numeric.mean()
print("The average price of a laptop at ZIMALL is {0} {1}".format(int(zimall_average_laptop_price), prod_cur))

print("[Question viii.] Using the analytics tools at your disposal find the average price for laptops at TENGA ")
# My Tenga dataframe also includes perfumes so if i  do an average of the whole dataframe , my mean will be distorted
# so i need to slice my pandas dataframe to only include laptops
laptops_from_tenga_sliced_from_original_dataframe = combined_laptop_and_perfume_dataframe_from_tenga[0:18]
prod_curr = laptops_from_tenga_sliced_from_original_dataframe["Currency"][
    0]  # could have written a function for this code but thats code optimisation , will consider it later

tenga_average_laptop_price = pd.to_numeric(laptops_from_tenga_sliced_from_original_dataframe["Price(Now)"]).mean()

print("The average price of a laptop at TENGA is {0} {1}".format(int(tenga_average_laptop_price), prod_curr))

print("[Question ix.] What is the average price for perfume at Tenga")

perfumes_from_tenga_sliced_from_original_dataframe = pd.to_numeric(
    combined_laptop_and_perfume_dataframe_from_tenga[18:]["Price(Now)"])
tenga_average_perfume_price = perfumes_from_tenga_sliced_from_original_dataframe.mean()
print("The average price of perfume at TENGA is {0} {1}".format(int(tenga_average_perfume_price), prod_curr))

print("[Question x.] Which company is selling HP laptops at higher prices")

HP_TENGA_Filtered_data = laptops_from_tenga_sliced_from_original_dataframe[
    laptops_from_tenga_sliced_from_original_dataframe.ProductName.str.contains('HP', case=False)]
HP_TENGA_Filtered_data_average_price = pd.to_numeric(HP_TENGA_Filtered_data["Price(Now)"]).mean()

print("Below is a list of HP Laptops from TENGA \n{0}  ".format(pd.to_numeric(HP_TENGA_Filtered_data["Price(Now)"])))
print("HP_TENGA_AVERAGE_LAPTOP_PRICE_IS {0}".format(HP_TENGA_Filtered_data_average_price))

HP_ZIMALL_Filtered_data = zimall_dataframe[
    zimall_dataframe.ProductName.str.contains('HP', case=False)]
HP_ZIMALL_Filtered_data_average_price = pd.to_numeric(HP_ZIMALL_Filtered_data["Price(Now)"]).mean()

print("Below is a list of HP Laptops from ZIMALL \n{0} ".format(pd.to_numeric(HP_ZIMALL_Filtered_data["Price(Now)"])))
print("HP_ZIMALL_AVERAGE_LAPTOP_PRICE_IS {0}".format(HP_ZIMALL_Filtered_data_average_price))

print(
    "Using the values obtained above , the average price of an HP LAPTOP from Tenga is higher as compared to ZIMALL")

print(
    "[Question xi. ] Among the laptops from the two sites which laptops have the best specifications according to a data scientist and how many are they")

# As a data scientist a laptop with better RAM ,Core i3 , i5 is okay

tenga_and_zimall_merged_dataframe_minus_the_perfumes = tenga_and_zimall_merged_dataframe[:47]

SPEC_A = tenga_and_zimall_merged_dataframe_minus_the_perfumes[tenga_and_zimall_merged_dataframe_minus_the_perfumes['ProductName'].str.contains("i7")]
SPEC_B = tenga_and_zimall_merged_dataframe_minus_the_perfumes[tenga_and_zimall_merged_dataframe_minus_the_perfumes['ProductName'].str.contains("i5")]
SPEC_C = tenga_and_zimall_merged_dataframe_minus_the_perfumes[tenga_and_zimall_merged_dataframe_minus_the_perfumes['ProductName'].str.contains("i3")]

BEST_PRODUCT_SPECS_FOR_A_DATA_SCIENTIST = pd.merge(SPEC_A, SPEC_B,
                                                   how='outer')

# print("Laptops from TENGA and ZIMALL with the best SPECIFICATIONS \n {0}".format(
#   BEST_PRODUCT_SPECS_FOR_A_DATA_SCIENTIST))

count_of_laptops_from_TENGA_and_ZIMALL_with_the_best_specs = BEST_PRODUCT_SPECS_FOR_A_DATA_SCIENTIST[
    'ProductName'].count()

print("Laptops from TENGA and ZIMALL with the best SPECIFICATIONS are {0}".format(
    count_of_laptops_from_TENGA_and_ZIMALL_with_the_best_specs))

print("[Question xii. ] Use any of the missing data techniques to replace missing data in your dataframe")
# Good thing is i handled most of the missing data through code by putting in placeholder text , and more over , most
# of the colums like Availability all have data that cant be computed statically

tenga_and_zimall_merged_dataframe['Discount'] = tenga_and_zimall_merged_dataframe['Discount'].fillna(0)
tenga_and_zimall_merged_dataframe['Availability'] = tenga_and_zimall_merged_dataframe['Availability'].fillna(
    "No status given")
# print(tenga_and_zimall_merged_dataframe)

print(
    "[Question xiii.] Show the correlation between products specifications and price , draw graphs that demonstrate this relationship ")

FEATURE_A = SPEC_A.assign(ProductName='7')
FEATURE_B = SPEC_B.assign(ProductName='5')
FEATURE_C = SPEC_C.assign(ProductName='3')

FEATURE_MERGED_DATAFRAME = FEATURE_A.merge(FEATURE_B, how='outer').merge(FEATURE_C, how='outer')

print(FEATURE_MERGED_DATAFRAME)

PRICE = (FEATURE_MERGED_DATAFRAME['Price(Now)']).astype(float)
PRODUCTS = (FEATURE_MERGED_DATAFRAME['ProductName']).astype(float)

PRODUCTS_SPECS_AND_PRICE_correlation = PRICE.corr(PRODUCTS, method='pearson')

print("The correlation between product specs and price is {0}".format(
    PRODUCTS_SPECS_AND_PRICE_correlation) + " and it shows that there is a positive correlation between product features and price ")
stats = linregress(PRICE, PRODUCTS)

m = stats.slope
b = stats.intercept

plt.scatter(PRICE, PRODUCTS, color='r')
plt.plot(PRICE, m * PRICE + b, color="blue")  # I've added a color argument here
plt.xlabel('Price')
plt.ylabel('CPU Feature')
plt.show()

print (
    "[Question xiv.] Extract features which have a strong pearson correlation with price and create a separate data frame from "
    "these features, categorical feature values must be trasnformed by integer encoding.")

print("Below is a dataframe containing items that have a strong pearson correlation with price \n {0}".format(FEATURE_A))








