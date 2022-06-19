from utils.parse import parse_profiles, parse_profiles_images_by_id, parse_profiles_with_images
from utils.export import list2json


if __name__ == "__main__":
    result = parse_profiles_with_images((139132090, 148693908))
    list2json(result, 'data/result.json')
    print(result)
