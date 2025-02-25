import json
import sys

from get_species_annotation_dic import get_species_annotation_dic
from microbial_interactions import MicrobialInteractions


def main(species_annotation_file_name, gpr_rules_file, pathways_file, species_to_exclude_file, max_number_of_species_in_each_group=None):
    """
    :param species_annotation_file_name: str - path to file Species_Annotation.csv, OrtAn output
    :param gpr_rules_file: str - path to json file containing gpr rules
    :param pathways_file: str - path to json file containing pathways info {path1: {reaction1: [enz1, enz2], reaction2: [enz3]}...} --> it can have only one path
    :param species_to_exclude_file: str - path to json file containing a list of the species to exclude from the combinations (the ones that are able to perform the paths alone)
    :param max_number_of_species_in_each_group: int - max number of species in each group of the combinations, if it is not given it will make all the possible combinations by default
    :return: dict - for each path, a list of the groups of species capable of performing the complete path
    """

    groups_with_complete_path = {}

    with open(gpr_rules_file, 'r') as handle:
        gpr_rules = json.load(handle)

    with open(pathways_file, 'r') as handle:
        paths_dict = json.load(handle)

    with open(species_to_exclude_file, 'r') as handle:
        species_to_exclude = json.load(handle)

    # transforming species annotation information into a dictionary
    species_annotation_dict = get_species_annotation_dic(species_annotation_file_name)

    if max_number_of_species_in_each_group is None:
        max_number_of_species_in_each_group = len(species_annotation_dict) - len(species_to_exclude)

    # creating class instance to calculate the microbial interactions
    microbial_interactions_class = MicrobialInteractions(species_annotation_dict, gpr_rules)

    # for each one of the pathways
    for path in paths_dict:
        groups_with_complete_path[path] = []
        # perform combinations where the number of species goes from 2 to the max_number_of_species_in_each_group
        for number_of_species in range(2, max_number_of_species_in_each_group + 1):
            groups = microbial_interactions_class.get_species_groups_performing_path(paths_dict[path],
                                                                                     number_of_species,
                                                                                     species_to_exclude)

            groups_with_complete_path[path] += groups

    return groups_with_complete_path


if __name__ == "__main__":
    species_annotation_file = sys.argv[1] #'./data/Species_Annotation.csv'
    gpr_rules = sys.argv[2] #'./data/GP_rules.json'
    pathways = sys.argv[3] #'./data/paths.json'
    species_to_exclude = sys.argv[4] #'./data/species_to_exclude.json'
    max_number_of_species = None

    groups_with_complete_path = main(species_annotation_file,
                                     gpr_rules,
                                     pathways,
                                     species_to_exclude,
                                     max_number_of_species)

    #with open(sys.argv[5], 'w') as file:
    print(groups_with_complete_path)
