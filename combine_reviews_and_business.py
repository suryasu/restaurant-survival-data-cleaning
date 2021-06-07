"""Combine Yelp's review dataset and Yelp's business dataset"""

import json
import argparse
import csv

FIELDNAMES = ['count', 'postal_code', 'city', 'attributes_RestaurantsDelivery', 'stars', 'latitude', 'business_id', 'name', 'attributes_RestaurantsPriceRange2', 'longitude', 'is_open', 'review_count', 'state', 'attributes_RestaurantsTakeOut', 'filtered_categories', 'useful', 'funny', 'cool']
BUSINESS_LIST = []

def combine_reviews_and_business (cleaned_business_dataset, cleaned_reviews_dataset, final_dataset):

    with open(cleaned_business_dataset, 'rU') as business:
        reader = csv.DictReader(business, delimiter=',')
        for business_line in reader:
            BUSINESS_LIST.append(business_line)

    with open(cleaned_reviews_dataset) as reviews:
        for review_line in reviews:
            review_contents = json.loads(review_line)
            for business in BUSINESS_LIST:
                if review_contents["business_id"] == business['business_id']:
                    business = add_sentiment(business, review_contents)
    
    with open(final_dataset, 'w+') as final_dataset:
        writer = csv.DictWriter(final_dataset, fieldnames=FIELDNAMES)
        writer.writeheader()
        for business in BUSINESS_LIST:
            writer.writerow(business)

def add_sentiment (business_line, review_line):
    business_line["useful"] = review_line['useful']
    business_line["funny"] = review_line["funny"]
    business_line["cool"] = review_line["cool"]

    return business_line
    # if 'useful' in business_line:
    #     business_line['useful'] += review_line['useful']
    # else:
    #     business_line['useful'] = review_line['useful']
    
    # if 'funny' in business_line:
    #     business_line['funny'] += review_line['funny']
    # else:
    #     business_line['funny'] = review_line['funny']
    
    # if 'cool' in business_line:
    #     business_line['cool'] += review_line['cool']
    # else:
    #     business_line['cool'] = review_line['cool']
    # return business_line


if __name__ == '__main__':
    """Clean dataset"""

    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file', type=str, help='Cleaned dataset')
    parser.add_argument('json_file', type=str, help='Yelp review json')
    args = parser.parse_args()

    csv_file = args.csv_file
    json_file = args.json_file
    final_dataset = '{0}.csv'.format(csv_file.split('.csv')[0] + '_cleaned')

    combine_reviews_and_business(csv_file, json_file, final_dataset)