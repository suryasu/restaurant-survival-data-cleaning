"""Remove all the businesses that are not restaurants or bars from Yelp's review dataset"""
import json
import argparse
import csv

BUSINESS_LIST = []
BUSINESS_IDS = set()
BUSINESS_DICT = {}

def clean_reviews_dataset(cleaned_dataset, reviews_dataset, cleaned_reviews_dataset):
    # capture list of businesses and business ids in memory
    with open(cleaned_dataset, 'rU') as business:
        reader = csv.DictReader(business, delimiter=',')
        for business_line in reader:
            BUSINESS_LIST.append(business_line)
            BUSINESS_IDS.add(business_line['business_id'])

    with open (reviews_dataset) as reviews:
        for review in reviews:
            review_contents = json.loads(review)
            if review_contents["business_id"] in BUSINESS_IDS:
                remove_attributes(review_contents)

    with open(cleaned_reviews_dataset, 'wb+') as cleaned:
        for key in BUSINESS_DICT:
            json.dump(BUSINESS_DICT[key], cleaned)
            cleaned.write('\n')
    
def remove_attributes(review_contents):
    business_id = review_contents["business_id"]
    if (business_id in BUSINESS_DICT):
        BUSINESS_DICT[business_id]["useful"] += review_contents["useful"]
        BUSINESS_DICT[business_id]["cool"] += review_contents["cool"]
        BUSINESS_DICT[business_id]["funny"] += review_contents["funny"]
    else:
        new_json = {
            "business_id": business_id,
            "useful": review_contents["useful"],
            "funny": review_contents["funny"],
            "cool": review_contents["cool"]
        }

        BUSINESS_DICT[business_id] = new_json
            

if __name__ == '__main__':
    """Clean dataset"""

    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file', type=str, help='Cleaned dataset')
    parser.add_argument('json_file', type=str, help='Yelp review json')
    args = parser.parse_args()

    csv_file = args.csv_file
    json_file = args.json_file
    cleaned_reviews_dataset = '{0}.json'.format(json_file.split('.json')[0] + '_cleaned')

    clean_reviews_dataset(csv_file, json_file, cleaned_reviews_dataset)