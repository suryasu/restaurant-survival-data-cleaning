"""Remove all Yelp business from the Yelp Business Dataset that are not restaurants or bars, flatten the dataset, and remove all business categories that are not in the top 17 categories"""
import json
import argparse

final_categories = {"American (New)", "American (Traditional)", "Asian Fusion", "Barbeque", "Bars", "Breakfast & Brunch", "Burgers", "Cafes", "Chicken Wings", "Chinese", "Fast Food", "Indian", "Italian", "Japanese", "Korean", "Mexican", "Pizza", "Sandwiches", "Thai"}


def read_and_write_json_file(cleaned_json, original_json):
    """Read in original json, clean it, and write to new json set"""
    with open(cleaned_json, 'wb+') as fout:
        with open(original_json) as fin:
            for line in fin:
                line_contents = json.loads(line)
                flattened_line = flatten_json(line_contents)
                # flatten json
                # clean line_contents
                if (is_restaurant(flattened_line)):
                    json.dump(clean_json(flatten_json(line_contents)), fout)
                    fout.write('\n')

def flatten_json(line_contents):
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(line_contents)
    return out


def is_restaurant(line_contents):
    """Clean flattened json in line"""
    if line_contents and line_contents['categories'] and ("Restaurants" in line_contents['categories'] or "Nightlife" in line_contents['categories']):
        return True
    return False

def addToDict(line_contents, attr1, attr2=None):
    return line_contents[attr1] if attr1 in line_contents else None

def clean_json(line_contents):
    #line_contents = clean_categories(line_contents)
    new_json = {
        "business_id": addToDict(line_contents, "business_id"),
        "city": addToDict(line_contents, "city"),
        "state": addToDict(line_contents, "state"),
        "postal_code": addToDict(line_contents, "postal_code"),
        "stars": addToDict(line_contents, "stars"),
        "is_open": addToDict(line_contents, "is_open"),
        "is_closed"
        "categories": addToDict(line_contents, "categories"),
        "review_count": addToDict(line_contents, "review_count"),
        "attributes": addToDict(line_contents, "attributes"),
        "RestaurantsTakeOut": addToDict(line_contents, "attributes_RestaurantsTakeOut"),
        "OutdoorSeating": addToDict(line_contents, "attributes_OutdoorSeating"),
        "RestaurantsPriceRange2": addToDict(line_contents, "attributes_RestaurantsPriceRange2"),
        "RestaurantsDelivery": addToDict(line_contents, "attributes_RestaurantsDelivery"),
        "BusinessAcceptsCreditCards": addToDict(line_contents, "attributes_BusinessAcceptsCreditCards"),
        "RestaurantsReservations": addToDict(line_contents, "attributes_RestaurantsReservations"),
        "RestaurantsGoodForGroups": addToDict(line_contents, "attributes_RestaurantsGoodForGroups"),
        "WiFi": addToDict(line_contents, "attributes_WiFi"),
        "Alcohol": addToDict(line_contents, "attributes_Alcohol")
    }
    return new_json

def check_reviews(line_contents): 
    with open(cleaned_json, 'wb+') as fout:
        with open(original_json) as fin:
            for line in fin:
                line_contents = json.loads(line)
                flattened_line = flatten_json(line_contents)
                # flatten json
                # clean line_contents
                if (is_restaurant(flattened_line)):
                    json.dump(clean_json(flatten_json(line_contents)), fout)
                    #json.dump(flattened_line, fout)
                    fout.write('\n')
 
if __name__ == '__main__':
    """Clean dataset"""

    parser = argparse.ArgumentParser()
    parser.add_argument('json_file', type=str, help='The json file to clean')
    args = parser.parse_args()

    json_file = args.json_file
    cleaned_json_file = '{0}.json'.format(json_file.split('.json')[0] + '_cleaned')

    read_and_write_json_file(cleaned_json_file, json_file)