import pandas as pd
import numpy as np


class xlForecast:
    def __init__(self, file_xlsx):
        self.file = file_xlsx
        
        
    def _sub_habitat(self, df):
        habitat_df = pd.read_excel(self.file, 'habitat_types', index_col='habitat_type')
        habitat_dict = habitat_df['id'].to_dict()
        df['habitat_type'] = df['habitat_type'].replace(habitat_dict)
        return df
    
    
    def _sub_mitigation(self, df):
        mitigation_df = pd.read_excel(self.file, 'mitigation_types', index_col='mitigation_type')
        mitigation_dict = mitigation_df['id'].to_dict()
        df['mitigation_type'] = df['mitigation_type'].replace(mitigation_dict)
        return df        
    
    
    @property
    def agencies(self):
        return pd.read_excel(self.file, 'options', usecols="A").dropna()

    @property
    def implementers(self):
        return pd.read_excel(self.file, 'implementers', usecols="B:E")
    
    @property
    def project_statuses(self):
        return pd.read_excel(self.file, 'options', usecols="B").dropna()
    
    @property
    def rfmps(self):
        return pd.read_excel(self.file, 'options', usecols="C").dropna()
    
    @property
    def counties(self):
        return pd.read_excel(self.file, 'options', usecols="D").dropna()
    
    @property
    def conservation_planning_areas(self):
        return pd.read_excel(self.file, 'options', usecols="E").dropna()
    
    @property
    def water_bodies(self):
        return pd.read_excel(self.file, 'options', usecols="J").dropna()

    @property
    def project_elements(self):
        return pd.read_excel(self.file, 'options', usecols="F").dropna()

    @property
    def programs(self):
        return pd.read_excel(self.file, 'options', usecols="G").dropna()
    
    @property
    def habitat_types(self):
        return pd.read_excel(self.file, 'habitat_types', usecols="B:D")
    
    @property
    def mitigation_types(self):
        return pd.read_excel(self.file, 'mitigation_types', usecols="B:D")    
    
    @property
    def projects(self):
        df =  pd.read_excel(self.file, 'projects', 
                             usecols="A:D, F, H:I, M, O:U")
        df = df.replace({np.NaN: None})
        return df
        
    @property
    def projects_counties(self):
        df = pd.read_excel(self.file, 'projects', 
                            usecols="A, K")
        df2 = pd.read_excel(self.file, 'addl_county', usecols="B, D")
        df2.columns = df.columns
        df = df.append(df2, ignore_index=True)
        return df
    
    @property
    def projects_project_elements(self):
        return pd.read_excel(self.file, 'project_project_elements', usecols="B, D")
        
    @property
    def projects_programs(self):
        return pd.read_excel(self.file, 'projects_programs', usecols="B,D")
    
    @property
    def habitat_parcels(self):
        df = pd.read_excel(self.file, 'habitat_outcomes', usecols="A,B,D")
        df = df.rename({'parcel_id': 'id'}, axis=1)
        return df

    @property
    def habitat_outcomes(self):
        df = pd.read_excel(self.file, 'habitat_outcomes', usecols="A,E:O")
        df = df.melt(id_vars=['parcel_id', 'confidence'], 
                     var_name='habitat_type', value_name='quantity')\
                .dropna(subset=['quantity'])
        df = df.reset_index().rename({'index':'id'}, axis=1)
        df = df[['parcel_id', 'confidence', 'quantity', 'habitat_type']]
        
        # sub habitat_type for reference
        df = self._sub_habitat(df)
        
        return df
    
    @property
    def mitigation_parcels(self):
        df = pd.read_excel(self.file, 'project_mitigation', usecols="A,B,D")
        df = df.rename({'parcel_id': 'id'}, axis=1)
        return df

    @property
    def project_mitigation(self):
        df = pd.read_excel(self.file, 'project_mitigation', usecols="A,E:AA")  # expand
        df = df.melt(id_vars=['parcel_id'], 
                     var_name='mitigation_type', value_name='quantity')\
                .dropna(subset=['quantity'])
        df = df[['parcel_id', 'quantity', 'mitigation_type']]
        
        # sub mitigation_type for reference
        df = self._sub_mitigation(df)
        
        return df
    
    @property
    def projects_permits(self):
        return pd.read_excel(self.file, 'projects_permits', usecols="A, C")
    
    @property
    def credit_approvers(self):
        return pd.read_excel(self.file, 'credit_approvers', usecols="A, D")
    
    @property
    def credit_purchases(self):
        df = pd.read_excel(self.file, 'credit_purchases', usecols="A:D")
        df = df.replace({np.NaN: None})
        return df
    
    @property
    def credit_values(self):
        df = pd.read_excel(self.file, 'credit_purchases', usecols="A, E:Z")
        df = df.rename({'id': 'credit_id'}, axis=1)
        df = df.melt(id_vars=['credit_id'], 
                     var_name='mitigation_type', value_name='quantity')\
                .dropna(subset=['quantity'])
        df = df.reset_index().rename({'index':'id'}, axis=1)
        df = df[['credit_id', 'quantity', 'mitigation_type']]
        
        # sub mitigation_type for reference
        df = self._sub_mitigation(df)
        
        return df
    
    @property
    def permits(self):
        return pd.read_excel(self.file, 'options', usecols="H").dropna()
    
    @property
    def mitigation_needs(self):
        df = pd.read_excel(self.file, 'mitigation_needs', usecols="A, C:AB")
        df = df.melt(id_vars=['permit', 'needed_by'], 
                     var_name='mitigation_type', value_name='quantity')\
                .dropna(subset=['quantity'])
        df = df.reset_index().rename({'index':'id'}, axis=1)
        df = df[['permit', 'quantity', 'needed_by', 'mitigation_type']]
        
        # sub mitigation_type for reference
        df = self._sub_mitigation(df)
        df = df.replace({np.NaN: None})
        
        return df        
    
    @property
    def project_commitments(self):
        return pd.read_excel(self.file, 'project_commitments', usecols="A:B,D,F")    
    
    @property
    def credit_commitments(self):
        return pd.read_excel(self.file, 'credit_commitments', usecols="A:B,D:E")
    
    
    @property
    def fpts(self):
        return pd.read_excel(self.file, 'projects', usecols="V").dropna().drop_duplicates()

    @property
    def project_fpts(self):
        return pd.read_excel(self.file, 'projects', usecols="A,V").dropna()
    
    @property
    def funding_source(self):
        return pd.read_excel(self.file, 'funding_sources')
    
    @property
    def project_funding(self):
        return pd.read_excel(self.file, 'project_funding', usecols="A:B,D,F:G")
    
    @property
    def cosmos_targets(self):
        df = pd.read_excel(self.file, 'cosmos_targets', usecols="A:C,E:F")
        df = df.replace({np.NaN: None})
        return df
