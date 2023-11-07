import snowflake.connector
import pandas as pd
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import create_engine


#importing the files 
file="CMS File April 23 Payout Detail (February Actuals).xlsx"
sheet="Payment Details"
df=pd.read_excel(io=file,sheet_name=sheet,skiprows=2,skipfooter=2)

#replacing the space in column name with _
df.columns = df.columns.str.replace(' ', '_')


#extracting the date from the file name provided
pattern = r'(\w+ \d{1,2})'

match=re.search(pattern, file)

if match:
    extracted_text = match.group(0)
    date = datetime.strptime(extracted_text, "%B %d")
    current_year = datetime.now().year
    date = date.replace(year=current_year)
    
#get actual date which is 2 months before the date in filename
actual_date=date-relativedelta(months=2)

#get the date in yyyy-mm format
formatted_date=actual_date.strftime('%Y-%m')

#adding extra columns as actuals
df['Actuals']=formatted_date
# print(df.head(10))


#initialising the snowflake credentials
snowflake_user = 'DEEPAK28'
snowflake_password = 'DaDa2802#'
snowflake_account = 'ic80573.ap-southeast-1'
snowflake_database = 'PROD_SOURCES'
snowflake_schema = 'PUBLIC'
snowflake_role='ACCOUNTADMIN'

# #establish snowflake connection
# conn = snowflake.connector.connect(
#     user=snowflake_user,
#     password=snowflake_password,
#     account=snowflake_account,
#     database=snowflake_database,
#     schema=snowflake_schema,
#     role=snowflake_role
#     )

# Create a SQLAlchemy Engine
engine = create_engine(f'snowflake://{snowflake_user}:{snowflake_password}@{snowflake_account}/{snowflake_database}/{snowflake_schema}')

# Upload the DataFrame to Snowflake
df.to_sql(name='payment_details', con=engine, if_exists='replace', index=False)

# Close the SQLAlchemy Engine
engine.dispose()
print('Data Uploaded Successfully')