#Load the Population estiamates data
import pandas as pd

#  path to the CSV file
csv_file_path = 'C:/Users/obypa/OWiDApplication/WPP2022_Population1JanuaryBySingleAgeSex_Medium_1950-2021.csv'

# Read the CSV file
df = pd.read_csv(csv_file_path, low_memory=False)

# Display the first few rows of the dataframe
print(df.head())

# Filter the data for the year 2019 and for the United States and Uganda
population= df[(df['Time'] == 2019) & (df['Location'].isin(['United States of America', 'Uganda']))]

# Display the first few rows of the filtered dataset
print(population.head())

# Define a function to filter and summarize population data for a given location
def summarize_population_by_location(dataframe, location):
    return dataframe[dataframe['Location'] == location].groupby(['Location', 'AgeGrp'])['PopTotal'].sum().reset_index()

# Use the function to get the population summaries for Uganda and USA
uganda_population_summary = summarize_population_by_location(population, 'Uganda')
usa_population_summary = summarize_population_by_location(population, 'United States of America')

# Display the summaries
print("Uganda Population Summary:")
print(uganda_population_summary)

print("\nUSA Population Summary:")
print(usa_population_summary)

def map_age_to_group(age):
    if age == '100+':
        return '85+'
    age = int(age)  
    if age < 5:
        return '0-4'
    elif age < 10:
        return '5-9'
    elif age < 15:
        return '10-14'
    elif age < 20:
        return '15-19'
    elif age < 25:
        return '20-24'
    elif age < 30:
        return '25-29'
    elif age < 35:
        return '30-34'
    elif age < 40:
        return '35-39'
    elif age < 45:
        return '40-44'
    elif age < 50:
        return '45-49'
    elif age < 55:
        return '50-54'
    elif age < 60:
        return '55-59'
    elif age < 65:
        return '60-64'
    elif age < 70:
        return '65-69'
    elif age < 75:
        return '70-74'
    elif age < 80:
        return '75-79'
    elif age < 85:
        return '80-84'
    else:
        return '85+'
    
    # Define a custom sort order for age categories
age_category_order = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85+']
# Convert age_category_order to a dict that maps each category to its index for sorting
age_category_sort_order = {key: index for index, key in enumerate(age_category_order)}

def process_population_data(df):
    # Map ages to age groups
    df['AgeCategory'] = df['AgeGrp'].apply(map_age_to_group)
    
    # Sum population totals by Location and AgeCategory
    grouped_df = df.groupby(['Location', 'AgeCategory'], as_index=False)['PopTotal'].sum()
    
    # Add a sorting key based on the custom order
    grouped_df['SortKey'] = grouped_df['AgeCategory'].map(age_category_sort_order)
    
    # Sort by this key and drop it
    sorted_grouped_df = grouped_df.sort_values(['Location', 'SortKey']).drop(columns=['SortKey'])
    
    return sorted_grouped_df

# Process the dataframes 
uganda_pop_data = process_population_data(uganda_population_summary)
usa_pop_data = process_population_data(usa_population_summary)

# Display the corrected result
print("Uganda Population Grouped Corrected Order:")
print(uganda_pop_data)
print("\nUSA Population Grouped Corrected Order:")
print(usa_pop_data)

import tabula

# Path to the PDF file
file_path = "C:/Users/obypa/OWiDApplication/AgeStandardizationofRates-ANewWHOStandard.pdf"

# extract tables into a list of DataFrame objects
dfs = tabula.read_pdf(file_path, pages="11", multiple_tables=True)

# print the list of tables found in the PDF, each one as a separate DataFrame
for table in dfs:
    print(table)


# The table needed is the first one on the page
data = dfs[0] if dfs else None
print(data.head())

# First, we remove the header row since it complicates splitting.
whostandard_pop =data.iloc[1:].copy()

# Splitting the 'Table 1. Standard Population Distribution (percent)' column into three new columns
whostandard_pop[['Segi Standard', 'Scandinavian Standard', 'WHO World Standard']] = whostandard_pop['Table 1. Standard Population Distribution (percent)'].str.split(expand=True)
whostandard_pop['Age group'] = whostandard_pop['Unnamed: 0']

# Drop the original combined column and the 'Unnamed: 0' column as they are no longer needed
whostandard_pop = whostandard_pop.drop(columns=['Table 1. Standard Population Distribution (percent)', 'Unnamed: 0'])

# Reorder the DataFrame to have 'age_group' as the first column
whostandard_pop = whostandard_pop[['Age group', 'Segi Standard', 'Scandinavian Standard', 'WHO World Standard']]

# Reset index
whostandard_pop.reset_index(drop=True, inplace=True)

# Remove the last two rows which are not needed 
whostandard_pop = whostandard_pop.iloc[:-2]

print(whostandard_pop.head())

# Convert data to DataFrame
whostandard_pop["WHO World Standard"] = whostandard_pop["WHO World Standard"].astype(float)

#  path to the CSV file
copd_file_path = 'C:/Users/obypa/OWiDApplication/age specific death rates of COPD.csv'
# Read the CSV file
copd_rates = pd.read_csv(copd_file_path, low_memory=False)

# Display the first few rows of the dataframe
print(copd_rates.head())

copd_rates.columns = ['age_group', 'death_rate_us_2019', 'death_rate_uganda_2019']
usa_pop_data.columns = ['location', 'age_group', 'population_total']
uganda_pop_data.columns = ['location', 'age_group', 'population_total']
whostandard_pop.columns = ['age_group', 'segi_standard', 'scandinavian_standard', 'who_world_standard']

# Merge population data with COPD death rates and WHO standard population for the USA
usa_merged_df = pd.merge(pd.merge(usa_pop_data, copd_rates.drop(columns="death_rate_uganda_2019"), on="age_group"), whostandard_pop, on="age_group")

# Merge population data with COPD death rates and WHO standard population for Uganda
uganda_merged_df = pd.merge(pd.merge(uganda_pop_data, copd_rates.drop(columns="death_rate_us_2019"), on="age_group"), whostandard_pop, on="age_group")


# calculate the number of age specific deaths for the uganda population
uganda_merged_df['number_of_deaths'] = uganda_merged_df.apply(
    lambda row: round(row['death_rate_uganda_2019'] * row['population_total'], 2), axis=1
)

# calculate the number of age specific deaths for the uganda population
usa_merged_df['number_of_deaths'] = usa_merged_df.apply(
    lambda row: round(row['death_rate_us_2019'] * row['population_total'], 2), axis=1
)



def calculate_death_rates(df, death_rate_column):
    """
    Calculates both crude and age-standardized death rates for a given dataframe.
  
    Args:
        df (pandas.DataFrame): The dataframe containing population and death rate data.
        death_rate_column (str): The name of the column containing death rates for the specific country.
  
    Returns:
        dict: A dictionary containing the crude death rate and age-standardized death rate.
    """
    # Calculate crude death rate
    total_deaths = df['number_of_deaths'].sum()
    total_population = df['population_total'].sum()
    crude_death_rate = (total_deaths / total_population) 
  
    # Calculate age-standardized death rate
    df['standardized_deaths'] = df[death_rate_column] / 100000 * df['population_total'] * df['who_world_standard'] / 100
    age_standardized_rate = df['standardized_deaths'].sum() / df['who_world_standard'].sum() * 100000
  
    return {
        "crude_death_rate": round(crude_death_rate, 1),
        "age_standardized_death_rate": round(age_standardized_rate, 1)
    }

# Example usage:
uganda_death_rates = calculate_death_rates(uganda_merged_df.copy(), 'death_rate_uganda_2019')
usa_death_rates = calculate_death_rates(usa_merged_df.copy(), 'death_rate_us_2019')

# Print results
print("Uganda:")
print(f"Crude death rate: {uganda_death_rates['crude_death_rate']:.1f} deaths per 100,000")
print(f"Age-standardized death rate: {uganda_death_rates['age_standardized_death_rate']:.1f} deaths per 100,000")

print("\nUSA:")
print(f"Crude death rate: {usa_death_rates['crude_death_rate']:.1f} deaths per 100,000")
print(f"Age-standardized death rate: {usa_death_rates['age_standardized_death_rate']:.1f} deaths per 100,000")
