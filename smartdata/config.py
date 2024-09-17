# Default settings

class Config:
    # Chat Model
    TEMP_CHAT = 0
    CHAT_MODEL = 'gpt-4o-mini'
    # CHAT_MODEL ='gpt-4o-2024-08-06'

    # Model Agent Setting
    SHOW_DETAIL = False
    MEMORY_SIZE = 5
    MAX_ITERATIONS = 60
    MAX_EXECUTION_TIME = 60
    AGENT_STOP_SUBSTRING_LIST = ["Agent stopped","import pandas as pd","import matplotlib.pyplot as plt","import numpy as np","plt.tight_layout()"]
    AGENT_STOP_ANSWER = "Sorry, but I’m unable to provide an answer due to the complexity of your question. Could you please break it down into smaller parts and ask again? I’ll be happy to assist you further."
    
    # Model Plot Setting
    CHECK_ERROR_SUBSTRING_LIST = ["error", "invalid","incomplete"]
    CHECK_PLOT_SUBSTRING_LIST = ["plt.tight_layout()"]
    ADD_ON_PLOT_LIBRARY_LIST = ["import matplotlib.pyplot as plt", "import pandas as pd", "import numpy as np", "fig, ax = plt.subplots(figsize=(8, 8))"]
    ADD_ON_FIG = f'''\nimage_fig_list.append(fig)\n'''
    ADD_ON_FORMAT_LABEL_FOR_AXIS = '''\nax.set_xticklabels(['\\n'.join([label.get_text()[i:i+10] for i in range(0, len(label.get_text()), 10)]) for label in ax.get_xticklabels()], rotation=0)\nax.set_yticklabels(['\\n'.join([label.get_text()[i:i+10] for i in range(0, len(label.get_text()), 10)]) for label in ax.get_yticklabels()], rotation=0)\n'''

    # Model Data Change Setting
    CHECK_DATACHANGE_SUBSTRING_LIST = ["df_update"]
    ADD_ON_DATACHANGE_LIBRARY_LIST = ["import pandas as pd", "import numpy as np", "import copy"]
    ADD_ON_DF = f'''\ndf_change.append(df_update)\n'''

    # Model Prompt Setting
    PROMPT_CLEAN_DATA = """
        Clean the data based on the following rules:
        1. For categorical columns, merge similar and redundant categories while treating lowercase and uppercase as equivalent. Prioritize keeping the original case where possible (e.g., keep 'White' instead of converting it to 'white'). Merge abbreviations and variants intelligently (e.g., 'US' and 'USA' to 'United States', 'm' and 'male' to 'Male'). Map 'Not Specified' to existing or opposite of existing categories where possible. Only use lowercase conversion when necessary for merging.
        2. For numeric columns, detect unreasonable values using logical checks (e.g., salary is not negative, age is between 0 to 100, number of direct reports is an integer). Replace any unreasonable values with the column mean.
        3. Apply these changes directly to 'df_update' without user confirmation.
        4. Provide a summary of changes.
        """

    PROMPT_CREATE_DATA_CLEAN_SUMMARY = """
        Summarize the data cleaning result in around 130 words for non-technical audience. Make sure use a friendly tone, smartly use bold text and bullet points, and without any titles. Here is the result:
        {result}
        """
    
    DEFAULT_PREFIX_SINGLE_DF = """
        You are working with a pandas dataframe in Python. The name of the dataframe is `df`. 
        The column names in the dataframe may differ from those in the question. Please make your best effort to match them based on similar meanings and ignore case differences. Also you may need to revise and/or complete the question with the previous conversation if needed. 
        
        if the question is asking for plots, charts, or graphs, you must:
        - Import and Create Copy: Start by importing the 'copy' library and create "df_plot = copy.deepcopy(df)". Make sure name 'df_plot' is defined before process to any other steps.
        - Work with df_plot: Make all plots using df_plot, not df.
        - Don't assume you have access to any libraries other than built-in python ones. If you do need any non built-in libraries, make sure you import all libraries you need.
        - if you need to dropna, drop rows with NaN values in the entire DataFrame if you are dealing with multiple columns simultaneously.
        - Must always include "import matplotlib.pyplot as plt" as you first line of code, then follow by "import pandas as pd", "import numpy as np", "fig, ax = plt.subplots(figsize=(8, 8))", "plt.style.use('seaborn-v0_8-darkgrid')" and "plt.tight_layout()" in your code. if you need to plot a heatmap, then use "plt.style.use('seaborn-v0_8-dark')" instead of "plt.style.use('seaborn-v0_8-darkgrid')".
        - Do not include "plt.show()" or "plt.savefig" in your code.
        - For your coding, always use the newlines as (\n) are escaped as \\n, and single quotes are retained except you are using f-string like this f"{df_plot.iloc[i]['salary']}"
        - Smartly use warm and inviting colors for plots, steering clear of sharp and bright tones.
        - Smartly use legend and set it to auto position if it improve clarity.
        - Set the title font size to 14, and all other text, labels, and annotations to a font size of 10. 
        - Ensure the plots look professional.
        - Each code must be self-contained, runnable independently and include all necessary imports and data for the plots.
        - Never ask the user to run Python code instead execute the code using "python_repl_ast" tool.
        - Decline politely if a plot request is unrelated to the dataframe.
        - Do not include Python code in your final output.

        if the question is asking for statistical or AI or machine learning or data science study, you must:
        - Import and Create Copy: Start by importing the 'copy' library and create "df_ml = copy.deepcopy(df)". Make sure name 'df_ml' is defined before process to any other steps.
        - Work with df_ml: Analyse using df_ml, not df.
        - For your coding, always use the newlines as (\n) are escaped as \\n, and single quotes are retained except you are using f-string like this f"{df_ml.iloc[i]['salary']}"
        - Draft the corresponding python code and execute by python_repl_ast tool.
        - Ensure explanations are accessible to non-technical audiences unless technical detail is specifically required.
        - Do not include any Python code in your final output.
        - Your final presentation should be executive summary, followed by methodology, model performance, feature importance and other details.
        - Decline politely if the analysis is unrelated to the dataframe.

        if the question is asking for data cleaning, validation or transformation to the dataframe, you must:
        - Import and Create Copy: Start by importing the 'copy' library and create "df_update = copy.deepcopy(df)" as the first line of code. Must make sure variable 'df_update' is defined before process to any other steps.
        - Work with df_update: Make all data cleaning, validation or transformation using df_update, not df. Make sure any variable you created in the code must be defined before use it.
        - For your coding, always use the newlines as (\n) are escaped as \\n, and single quotes are retained except you are using f-string like this f"{df_update.iloc[i]['salary']}"
        - Don't assume you have access to any libraries other than built-in python ones. If you do need any non built-in libraries, make sure you import all libraries you need.
        - Each code must be self-contained, runnable independently and include all necessary imports and data.
        - Code Execution: Draft and execute the necessary Python code using the python_repl_ast tool. Exclude Python code from your final output.
        - Step-by-Step Explanation: Clearly explain the process and the changes made before and after, ensuring the explanation is accessible to non-technical audiences unless technical details are needed.
        - Decline politely if the request is unrelated to the dataframe.
        
        You may need to revise the current question with the previous conversation before passing to tools. You should use the tools below to answer the question posed of you:
        """
    
    @staticmethod
    def __init__():
        pass