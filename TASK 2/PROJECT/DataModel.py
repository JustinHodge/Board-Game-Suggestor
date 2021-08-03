import pandas as pd
from matplotlib import colors
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import numpy as np
from collections import OrderedDict

class DataModel:
    def __init__(self, path_to_unclean_set = 'TASK 2\PROJECT\games_detailed_info.csv'):
        self.unclean_set= pd.read_csv(path_to_unclean_set)
        self.language_value = {
            'NO' : 1,
            'SOME' : 2,
            'MODERATE' : 3,
            'EXTENSIVE' : 4,
            'UNPLAYABLE' : 5
        }

        self.result_value = {
            'BEST' : 3,
            'RECOMMENDED' : 2,
            'NOTRECOMMENDED' : 1
        }

        self.random_seed = 222
        self.cmap = colors.ListedColormap(['r','g','b','c','m', 'y'])
        self.clean_data_set = self.create_clean_data_set(self.unclean_set)

        self.scaler_model = StandardScaler().fit(self.clean_data_set)
        self.pca_model = PCA(n_components=2, random_state=self.random_seed).fit(self.get_scaled_data(self.get_clean_data))
        self.split_data()
        self.kmeans_model = KMeans(n_clusters=6, random_state=self.random_seed).fit(self.train_set)
        self.linear_regression_model = LinearRegression().fit(self.train_set, self.get_kmeans_prediction(self.train_set))

        self.add_cluster_numbers()

    def add_cluster_numbers(self):
        all_games_kmeans = self.kmeans_model.predict(self.get_pca_data(self.clean_data_set))
        self.clean_data_set['cluster'] = all_games_kmeans.tolist()
        self.unclean_set['cluster'] = self.clean_data_set['cluster']

    def add_brackets_and_eval(self, string_item):
        string_item = str(string_item)
        if string_item[0] != '[':
            string_item = '[' + str(string_item)
        if string_item[-1] != ']':
            string_item = str(string_item) + ']'
        return eval(string_item)

    def calculate_players_from_ordered_dict(self, game):
        playercount_normalized_results = {}
        for playercount in game:
            if not 'result' in playercount:
                return 0
            total_votes = 0
            result_total_result = 0
            result_normalized_result = 0
            for result in playercount['result']:
                # current_player_count = result['@value']
                multiplier = self.result_value[result['@value'].upper().replace(' ', '')]
                total_votes += int(result['@numvotes'])
                result_total_result += int(result['@numvotes']) * multiplier
            if(total_votes):
                result_normalized_result = result_total_result / total_votes
            else:
                result_normalized_result = 0
                result_normalized_result = 0
            playercount_normalized_results[playercount['@numplayers']]=result_normalized_result
        sum_of_weighted_players = 0
        sum_of_keys = 0
        num_of_keys = 0
        for key in playercount_normalized_results.keys():
            if not key.isnumeric():
                num = int(key[:-1]) + 1
            else:
                num = int(key)
            sum_of_weighted_players += num * (playercount_normalized_results[key]/3)
            sum_of_keys += num
            num_of_keys += 1
        return (sum_of_weighted_players)/(sum_of_keys/num_of_keys)

    def calculate_age_from_ordered_dict(self, game):
        weighted_age_sum = 0
        total_votes = 0
        for age in game:
            votes = age['@numvotes']
            if age['@value'].isnumeric():
                age_num = age['@value']
            else:
                age_num = 25
            weighted_age_sum += int(age_num) * int(votes) 
            total_votes += int(votes)
        if total_votes:
            return weighted_age_sum/total_votes
        else:
            return 0

    def normalize_language_dependence(self, game):
        sum_of_weighted_language = 0
        total_num_votes = 0
        for level in game:
            value_key = level['@value'].split(' ')[0].upper()
            language_multiplier = self.language_value[value_key]
            votes = int(level['@numvotes'])
            total_num_votes += votes
            sum_of_weighted_language += language_multiplier * votes
        return (sum_of_weighted_language / total_num_votes) if total_num_votes > 0 else 0

    def create_clean_data_set(self, unclean_set):
        clean_data_set = None
        clean_data_set = unclean_set.drop(['Unnamed: 0', 'type', 'id', 'thumbnail', 'image', 'primary',
            'alternate', 'description', 'yearpublished', 'boardgameexpansion', 'boardgameimplementation',
            'boardgamedesigner', 'boardgameartist', 'boardgamepublisher', 'boardgameintegration', 'boardgamecompilation', 'boardgamecategory',
            'boardgamemechanic', 'boardgamefamily', 'RPG Item Rank', 'Accessory Rank', 'Video Game Rank', 'Amiga Rank',
            'Commodore 64 Rank', 'Arcade Rank', 'Atari ST Rank'], axis=1)
        clean_data_set = clean_data_set.fillna(0)
        clean_data_set['suggested_num_players'] = clean_data_set['suggested_num_players'].apply(self.add_brackets_and_eval)
        clean_data_set['suggested_num_players'] = clean_data_set['suggested_num_players'].apply(self.calculate_players_from_ordered_dict)
        clean_data_set = clean_data_set[clean_data_set['suggested_playerage'] != 0]
        clean_data_set['suggested_playerage'] = clean_data_set['suggested_playerage'].apply(self.add_brackets_and_eval)
        clean_data_set['suggested_playerage'] = clean_data_set['suggested_playerage'].apply(self.calculate_age_from_ordered_dict)
        clean_data_set = clean_data_set[clean_data_set['suggested_language_dependence'] != 0]
        clean_data_set['suggested_language_dependence'] = clean_data_set['suggested_language_dependence'].apply(self.add_brackets_and_eval)
        clean_data_set['suggested_language_dependence'] = clean_data_set['suggested_language_dependence'].apply(self.normalize_language_dependence)
        clean_data_set = clean_data_set[clean_data_set['suggested_num_players'] > 0]
        clean_data_set = clean_data_set[clean_data_set['suggested_playerage'] > 0]
        clean_data_set = clean_data_set[clean_data_set['suggested_language_dependence'] > 0]
        return clean_data_set

    def get_clean_data(self):
        return self.clean_data_set

    def get_pca_model(self):
        return self.pca_model

    def get_scaler_model(self):
        return self.scaler_model

    def get_scaled_data(self, clean_data):
        return self.scaler_model.transform(clean_data)
    
    def get_pca_data(self, scaled_data):
        return self.pca_model.transform(scaled_data)

    def split_data(self, pca_data_frame=None):
        if pca_data_frame is None:
            pca_data_frame = self.get_pca_data(self.pca_model.transform(self.clean_data_set))
        train_set, test_set = train_test_split(pca_data_frame, test_size=0.2, random_state=self.random_seed, shuffle=True)
        self.train_set = train_set
        self.test_set = test_set
    
    def get_test_set(self):
        return self.test_set
    
    def get_train_set(self):
        return self.train_set

    def get_kmeans_prediction(self, pca_data):
        return self.kmeans_model(pca_data)
    
    def get_regression_prediction(self, kmeans_data):
        return self.linear_regression_model.predict(kmeans_data)