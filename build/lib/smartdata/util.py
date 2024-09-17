import pandas as pd
import numpy as np

def replace_invalid_values(x):
    # Attempt to convert the value to a string and check for invalid values
    if isinstance(x, str) or isinstance(x, (int, float)):
        if str(x).strip().lower() in ['na', 'nan', 'not applicable', 'n/a', 'n.a.', 'null', 'empty', 'blank']:
            return np.nan
    # If x is a valid numeric value, return it as is
    return x

def clean_dataframe(df):
    df_update = df.copy()
    summary = {
        'numeric_columns_filled': {},
        'numeric_outliers_capped': {},
        'categorical_columns_filled': {},
        'categorical_columns_removed': [],
        'datetime_columns_filled': {},
        'rows_removed': 0,
        'columns_removed': 0
    }

    # 1. Remove empty rows and columns
    rows_before = df_update.shape[0]
    df_update.dropna(how='all', inplace=True)
    rows_after = df_update.shape[0]
    summary['rows_removed'] = rows_before - rows_after
    
    columns_before = df_update.shape[1]
    df_update.dropna(axis=1, how='all', inplace=True)
    columns_after = df_update.shape[1]
    summary['columns_removed'] = columns_before - columns_after
    
    # 2. Clean numeric columns
    for col in df_update.select_dtypes(include=[np.number]).columns:
        # Replace invalid entries with NaN
        # print(col)
        df_update[col] = df_update[col].apply(replace_invalid_values)
        
        # Fill missing values with the mean
        missing_count = df_update[col].isnull().sum()
        if missing_count > 0:
            mean_value = df_update[col].mean()
            df_update[col].fillna(mean_value, inplace=True)
            summary['numeric_columns_filled'][col] = missing_count
        
        # Detect outliers using IQR and cap them
        # Q1 = df_update[col].quantile(0.25)
        # Q3 = df_update[col].quantile(0.75)
        # IQR = Q3 - Q1
        # lower_bound = Q1 - 2.5 * IQR
        # upper_bound = Q3 + 2.5 * IQR

        lower_bound = df_update[col].quantile(0.01)
        upper_bound = df_update[col].quantile(0.99)
        
        outliers_lower = df_update[df_update[col] < lower_bound][col].count()
        outliers_upper = df_update[df_update[col] > upper_bound][col].count()
        
        if outliers_lower > 0 or outliers_upper > 0:
            df_update[col] = np.where(df_update[col] < lower_bound, lower_bound, df_update[col])
            df_update[col] = np.where(df_update[col] > upper_bound, upper_bound, df_update[col])
            summary['numeric_outliers_capped'][col] = {'lower_capped': outliers_lower, 'upper_capped': outliers_upper}

    # 3. Clean categorical/string/object columns
    for col in df_update.select_dtypes(include=['object']).columns:
        # Replace invalid entries with NaN and trim spaces
        
        df_update[col] = df_update[col].apply(lambda x: replace_invalid_values(x))
        # Remove column if more than 90% of values are missing
        missing_percentage = df_update[col].isnull().mean()
    
        df_update[col] = df_update[col].astype(str).str.strip()
        df_update[col] = df_update[col].apply(lambda x: replace_invalid_values(x))
        # print(col)
        # print(missing_percentage)
        if missing_percentage > 0.9:
            df_update.drop(columns=[col], inplace=True)
            summary['categorical_columns_removed'].append(col)
        else:
            # Fill missing values with 'unknown'
            missing_count = df_update[col].isnull().sum()
            if missing_count > 0:
                df_update[col].fillna('Not Specified', inplace=True)
                summary['categorical_columns_filled'][col] = missing_count

    # 3. Clean datetime columns
    for col in df_update.select_dtypes(include=['datetime']).columns:
        # print(col)
        try:
            df_update[col] = pd.to_datetime(df_update[col], errors='coerce')
            # Replace missing values with mode
            missing_count = df_update[col].isnull().sum()
            if missing_count > 0:
                mode_value = df_update[col].mode()[0]
                df_update[col].fillna(mode_value, inplace=True)
                summary['datetime_columns_filled'][col] = missing_count
        except Exception:
            continue
    
    # Build the markdown summary string dynamically
    summary_md = "**Data Cleaning Result:**\n\n"
    
    if summary['numeric_columns_filled']:
        summary_md += "- Numeric columns with missing values filled using the column mean:\n  "
        summary_md += ', '.join([f"{col} ({count} values)" for col, count in summary['numeric_columns_filled'].items()]) + "\n\n"
    
    if summary['numeric_outliers_capped']:
        summary_md += "- Numeric columns had outliers capped between the 1st and 99th percentiles:\n  "
        summary_md += ', '.join([f"{col} (lower capped: {caps['lower_capped']}, upper capped: {caps['upper_capped']})" for col, caps in summary['numeric_outliers_capped'].items()]) + "\n\n"
    
    if summary['categorical_columns_filled']:
        summary_md += "- Categorical columns with missing values filled with 'Not Specified':\n  "
        summary_md += ', '.join([f"{col} ({count} values)" for col, count in summary['categorical_columns_filled'].items()]) + "\n\n"
    
    if summary['categorical_columns_removed']:
        summary_md += "- Categorical columns removed due to over 90% missing data:\n  "
        summary_md += ', '.join(summary['categorical_columns_removed']) + "\n\n"
    
    if summary['datetime_columns_filled']:
        summary_md += "- Datetime columns with missing values filled using the column mode:\n  "
        summary_md += ', '.join([f"{col} ({count} values)" for col, count in summary['datetime_columns_filled'].items()]) + "\n\n"
    
    summary_md += f"- Total number of rows removed: {summary['rows_removed']}\n"
    summary_md += f"- Total number of columns removed: {summary['columns_removed']}\n\n"
    
    summary_md += "Next, we review and standardize categorical fields, identifying any unreasonable values.\n"

    # Output the summary
    # print(summary_md)
    
    return df_update, summary_md