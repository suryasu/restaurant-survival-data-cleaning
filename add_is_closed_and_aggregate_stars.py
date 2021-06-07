"""Count number of closed businesses and aggregate number of businesses at each star rating"""
import json
import argparse
import csv
from collections import defaultdict

FIELDNAMES = ['count', 'postal_code', 'city', 'attributes_RestaurantsDelivery', 'stars', 'latitude', 'business_id', 'name', 'attributes_RestaurantsPriceRange2', 'longitude', 'is_open', 'review_count', 'state', 'attributes_RestaurantsTakeOut', 'filtered_categories', 'useful', 'funny', 'cool', 'is_closed', 'aggregated_by_star']
BUSINESS_LIST = []
STAR_AGGREGATE = defaultdict(lambda: 0)

def add_is_closed_and_aggregate_stars(business_data, cleaned_business_data):
    with open(business_data, 'rU') as business:
        reader = csv.DictReader(business, delimiter=',')
        for business_line in reader:
            BUSINESS_LIST.append(business_line)
            STAR_AGGREGATE[business_line['stars']] += 1

    with open(cleaned_business_data, 'wb+') as cleaned:
        writer = csv.DictWriter(cleaned, fieldnames=FIELDNAMES)
        writer.writeheader()
        for business in BUSINESS_LIST:
            business['is_closed'] = 0 if int(business['is_open']) == 1 else 1
            business['aggregated_by_star'] = STAR_AGGREGATE[business['stars']]
            writer.writerow(business)


if __name__ == '__main__':
    """Clean dataset"""

    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file', type=str, help='Cleaned dataset')
    args = parser.parse_args()

    csv_file = args.csv_file
    final_dataset = '{0}.csv'.format(csv_file.split('.csv')[0] + '_new')

    add_is_closed_and_aggregate_stars(csv_file, final_dataset)
    