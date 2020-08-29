# Standard library imports
from zipfile import ZipFile

# Related third party imports
import pandas as pd


class ReadFiles():
    """
    Class to read necessary files to train models, make recommendations and visualizations.    
    """    
    def __init__(self, report_features=None):
        """
        Define paths to files and features to be retrieved from 'original market dataframe' (estaticos_market.csv).
        :param report_features: list of strings, default=None, has to contain names of features to be retrieved from the original dataframe (e.g. not processed. See more about this in the projects' GitHub page or in the main.ipynb notebook). If not defined, the features id, de_natureza_juridica, sg_uf, de_ramo, setor, idade_emp_cat, de_nivel_atividade, and de_faixa_faturamento_estimado are retrieved.
        """
        self._output_path = "output/"
        self._data_path = "data/"
        if report_features == None:
            self.report_features = "de_natureza_juridica sg_uf de_ramo setor idade_emp_cat de_faixa_faturamento_estimado".split()
            print(f"Features retrieved from original dataframe: {self.report_features}")
        else:
            self.report_features = report_features
            print(f"Features retrieved from original dataframe: {self.report_features}")
        
    def get_data(self):
        """
        Return tables with data.
        :return tuple:
            - pos 0: Pandas DataFrame, contains all the companies' IDs as index.
            - pos 1: Pandas DataFrame, contains numbers from 0 to max number of clusters. Maps each company to a cluster.
            - pos 3: Pandas Dataframe, contains all the companies ids and some of their original features: id, de_natureza_juridica, sg_uf, de_ramo setor, idade_emp_cat, de_nivel_atividade, de_faixa_faturamento_estimado.
            - pos 4: Pandas Dataframe, contains a snippet with clients IDs for portfolio 2.
            
        """
        # Main Dataset
        dataset_files = []
        for file_idx in range(11):
            dataset_files.append(pd.read_csv(self._output_path + f"companies_profile_{file_idx}.bz2", compression="bz2"))     
        database = pd.concat(dataset_files, axis=0, ignore_index=True).set_index("id")
        
        # Cluster labels
        cluster_labels = pd.read_csv(self._output_path + "cluster_labels.zip", compression="zip", index_col=0)   
        
        # Portfolios
        portfolio2_snippet = pd.read_csv(self._data_path + "estaticos_portfolio2.csv", usecols=["id"])
            
        # Important features from the original dataset, used for visualization/context
        try:
            with ZipFile(self._data_path + "estaticos_market.csv.zip").open("estaticos_market.csv") as original_dataset:
                original_market_df = pd.read_csv(original_dataset, index_col=0, usecols=(["id"] + self.report_features))  
        except:
            raise Exception("Are the features chosen available in the original dataset?")
            
        return database, cluster_labels, original_market_df, portfolio2_snippet