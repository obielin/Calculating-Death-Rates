# Calculating-Death-Rates
The process used to calculate the crude and age-standardized death rates from Chronic Obstructive Pulmonary Disease (COPD) in Uganda and the United States for 2019.
### This report details the process used to calculate the crude and age-standardized death rates from Chronic Obstructive Pulmonary Disease (COPD) in Uganda and the United States for 2019.
Data Acquisition and Preprocessing:
-   Population Data:
    -   Obtained from the World Population Prospects database.
    -	Filtered to include only data for Uganda and the USA in 2019.
    -   Grouped by location and age group to obtain population totals for each age category.

-   COPD Death Rates:
    -	Obtained from a separate CSV file.
    -	Merged with the population data based on the corresponding age groups.

-   WHO Standard Population:
    -	Extracted from a PDF file using the "tabula" library.
    -	Processed to separate the standard population percentages for different regions into separate columns.
    -	Merged with the combined population and death rate data.


Death Rate Calculations:
-   Crude Death Rate (CDR):
    -	Calculated by dividing the total number of deaths from COPD by the total population and multiplying by 100,000.
-   Age-standardized death Rate (ASDR):
    -	Calculated by weighting the age-specific death rates by the corresponding WHO standard population and then summing these weighted values.
    -	The final result is divided by the total WHO standard population and multiplied by 100,000 to express the rate as deaths per 100,000 people.

#### - Assumptions made
-   The age-specific death rates provided were accurate and represented the entire population of each country. 
-   The WHO World Standard Population reasonably represents the global age structure, allowing for a comparatively fair comparison between countries with differing age distributions. 

#### - Outcome of the Analysis
While Uganda's crude death rate (5.8 deaths/100,000) is lower than the USA's (56.9 deaths/100,000), its age-standardized rate (75.3 deaths/100,000) is significantly lower than the USA's (3410.6 deaths/100,000). This indicates potentially differing age-specific mortality patterns.
