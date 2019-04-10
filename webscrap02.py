# # import pandas as pd
# import pandas as pd
#
# # list of strings
# lst = ['Geeks', 'For', 'Geeks', 'is',
# 			'portal', 'for', 'Geeks']
#
# # Calling DataFrame constructor on list
# df = pd.DataFrame(lst)
# print(df)

#
# urls = {'Laptops': 'https://10ngah.com/704-laptop-deals', 'Perfumes': 'https://10ngah.com/345-perfume'}
#
# for name_of_url, url in urls.items():
#      print name_of_url


price_result = '1,650.00'
mystring = price_result.replace(",", "")
print(mystring)


# count_of_occurrence_of_HP_LAPTOPS_at_TENGA_greater_than_the_mean = 0
# for item_price in pd.to_numeric(HP_TENGA_Filtered_data["Price(Now)"]):
#     if (item_price > HP_TENGA_Filtered_data_average_price):
#         count_of_occurrence_of_HP_LAPTOPS_at_TENGA_greater_than_the_mean += 1
#     else:
#         item_price = False
#
# print("Occurence of items in the Tenga Dataframe with prices that are greater than the average is {0}".format(
#     count_of_occurrence_of_HP_LAPTOPS_at_TENGA_greater_than_the_mean))


#
# count_of_occurrence_of_HP_LAPTOPS_at_ZIMALL_greater_than_the_mean = 0
# for item_price in pd.to_numeric(HP_ZIMALL_Filtered_data["Price(Now)"]):
#     if (item_price > HP_ZIMALL_Filtered_data_average_price):
#         count_of_occurrence_of_HP_LAPTOPS_at_ZIMALL_greater_than_the_mean += 1
#     else:
#         item_price = False
#
# print("Occurence of items in the ZIMALL Dataframe with prices that are greater than their average is {0}".format(
#     count_of_occurrence_of_HP_LAPTOPS_at_ZIMALL_greater_than_the_mean))


count_of_occurrence_of_LAPTOPS_at_TENGA_and_ZIMALL_greater_than_the_mean = 0
for item_price in pd.to_numeric(tenga_and_zimall_merged_dataframe_minus_the_perfumes["Price(Now)"]):
    if (item_price > tenga_and_zimall_average_laptop_price):
        count_of_occurrence_of_LAPTOPS_at_TENGA_and_ZIMALL_greater_than_the_mean += 1
    else:
        item_price = False

print("The number of laptops that have the best specifications are {0}".format(
    count_of_occurrence_of_LAPTOPS_at_TENGA_and_ZIMALL_greater_than_the_mean))