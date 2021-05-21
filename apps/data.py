import pandas as pd


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
        df = pd.read_excel(self.file, 'options', usecols="A")
        return df
    
    @property
    def implementers(self):
        df = pd.read_excel(self.file, 'implementers')
        return df
    
    @property
    def project_statuses(self):
        df = pd.read_excel(self.file, 'options', usecols="B")
        return df
    
    @property
    def rfmps(self):
        df = pd.read_excel(self.file, 'options', usecols="C")
        return df
    
    @property
    def counties(self):
        df = pd.read_excel(self.file, 'options', usecols="D")
        return df
    
    @property
    def conservation_planning_areas(self):
        df = pd.read_excel(self.file, 'options', usecols="E")
        return df
    
    @property
    def waterbodies(self):
        df = pd.read_excel(self.file, 'options', usecols="J")
        return df

    @property
    def project_elements(self):
        df = pd.read_excel(self.file, 'options', usecols="F")
        return df

    @property
    def programs(self):
        df = pd.read_excel(self.file, 'options', usecols="G")
        return df
    
    @property
    def habitat_types(self):
        df = pd.read_excel(self.file, 'habitat_types')
        return df
    
    @property
    def mitigation_types(self):
        df = pd.read_excel(self.file, 'mitigation_types')
        return df    
    
    @property
    def projects(self):
        df = pd.read_excel(self.file, 'projects', 
                           usecols="A:D, F, H:I, M, O:U")
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
        df = pd.read_excel(self.file, 'project_project_elements', usecols="B, D")
        return df
        
    @property
    def projects_programs(self):
        df = pd.read_excel(self.file, 'projects_programs', usecols="B,D")
    
    @property 
    def habitat_parcels(self):
        df = pd.read_excel(self.file, 'habitat_outcomes', usecols="A,B,D")
        return df

    @property
    def habitat_outcomes(self):
        df = pd.read_excel(self.file, 'habitat_outcomes', usecols="A,E:N")
        df = df.melt(id_vars=['parcel_id', 'verified'], 
                     var_name='habitat_type', value_name='quantity')\
                .dropna(subset=['quantity'])
        df = df.reset_index().rename({'index':'id'}, axis=1)
        df = df[['parcel_id', 'verified', 'quantity', 'habitat_type']]
        
        # sub habitat_type for reference
        df = self._sub_habitat(df)
        
        return df
    
    @property
    def mitigation_parcels(self):
        df = pd.read_excel(self.file, 'project_mitigation', usecols="A,B,D")
        return df

    @property
    def project_mitigation(self):
        df = pd.read_excel(self.file, 'project_mitigation', usecols="A,E:Z")  # expand
        df = df.melt(id_vars=['parcel_id'], 
                     var_name='mitigation_type', value_name='quantity')\
                .dropna(subset=['quantity'])
        df = df[['parcel_id', 'quantity', 'mitigation_type']]
        
        # sub mitigation_type for reference
        df = self._sub_mitigation(df)
        
        return df
    
    @property
    def projects_permits(self):
        df = pd.read_excel(self.file, 'projects_permits', usecols="A, C")
        return df
    
    @property
    def credit_approvers(self):
        df = pd.read_excel(self.file, 'credit_approvers', usecols="A, D")
        return df
    
    @property
    def credit_purchases(self):
        df = pd.read_excel(self.file, 'credit_purchases', usecols="A:D")
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
    def mitigation_needs(self):
        df = pd.read_excel(self.file, 'mitigation_needs', usecols="A, C:AA")
        df = df.melt(id_vars=['permit_id'], 
                     var_name='mitigation_type', value_name='quantity')\
                .dropna(subset=['quantity'])
        df = df.reset_index().rename({'index':'id'}, axis=1)
        df = df[['permit_id', 'quantity', 'mitigation_type']]
        
        # sub mitigation_type for reference
        df = self._sub_mitigation(df)
        
        return df        
    
    @property
    def project_commitments(self):
        df = pd.read_excel(self.file, 'project_commitments', usecols="A:B,D,F")
        return df    
    
    @property
    def credit_commitments(self):
        df = pd.read_excel(self.file, 'credit_commitments', usecols="A,C,D")
        return df
    
    @property
    def permits(self):
        df = pd.read_excel(self.file, 'options', usecols="K")
        return df
    
    @property
    def fpts(self):
        df = pd.read_excel(self.file, 'projects', usecols="V")
        return df

    @property
    def project_fpts(self):
        df = pd.read_excel(self.file, 'projects', usecols="A,V")
        return df
    
    @property
    def funding_source(self):
        df = pd.read_excel(self.file, 'funding_sources')
        return df
    
    @property
    def project_funding(self):
        df = pd.read_excel(self.file, 'proejct_funding', usecols="A:B,D,F:G")
        return df
    
    @property
    def cosmos_targets(self):
        df = pd.read_excel(self.file, 'cosmos_targets', usecols="A:E,G")
        return df
