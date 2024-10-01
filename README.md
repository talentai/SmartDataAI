# SmartDataAI

✨ SmartDataAI: Intelligent Data Cleaning, Transformation, Charting, and Analysis with LLM ✨

SmartDataAI is a powerful Python library designed for developers to create interactive, conversational interfaces for data cleaning, transformation, charting, and analysis. By leveraging large language models (LLMs), Smartdataai enables quick responses to your data queries and effortlessly returns answers.

Need to update or clean your dataset? Simply request changes, and Smartdataai will provide a new, updated dataframe. For charting, it delivers a fully-rendered Matplotlib figure object, ready to be displayed in your interface or saved locally.

Bring your data to life with Smartdataai!

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install SmartDataAI.

```bash
pip install smartdataai
```

## Features
Smartdataai acts as an intelligent LLM agent designed specifically to manage dataframe-related requests. You can easily integrate any LLM class from Langchain, with GPT-4-mini as the default. While Langchain agents are simple to use, getting actionable outputs like dataframes and charts can be tricky. That's where Smartdataai shines — delivering answers, dataframes, and visualizations all in one seamless interaction.

Key Features:
- Supports any LLM class from Langchain (default: GPT-4-mini)
- Conversational interface with memory
- Buildin auto data cleaning
- Effortlessly generate answers, update dataframes, and create charts
- Easy integration with FastAPI or Streamlit

🔥 If you are using any LLM that required an API Key (like GPT), you should setup as evniroment variable, See example 1.

## Auto Data Cleaning Guideline

**General**: 
- Remove empty rows and remove columns with over 90% missing data.

**Numeric Data**:
- Impute missing and N/A values with the mean.
- Outliers are capped between the 1st and 99th percentiles.
- Replace unreasonable values (e.g., negative salary or age over 200) with the mean.

**Text Data**:
- Mark missing and N/A values as "Not Specified"
- Merge similar categories by treating lowercase and uppercase values as equivalent, and combining abbreviations (e.g., 'US' and 'USA' merged into 'United States' or 'Women', F' and 'female' into 'Female').

## Integration with Streamlit
Intration with streamlit is natual where you may use st.pyplot to show the charts and use st.dataframe to show the dataframe. Here is an application we developed for a human resources dataset.

[![Watch the demo for data designer](https://github.com/talentai/SmartDataAI/blob/main/demo/thumb_designer.jpg)](https://www.youtube.com/watch?v=DbmfQ7ToolM)

[![Watch the demo for data analyst](https://github.com/talentai/SmartDataAI/blob/main/demo/thumb_analyst.jpg)](https://www.youtube.com/watch?v=9YlnDKCQwzA)

## Integration with FastAPI
Once you have the matplotlib figures from the model, you may convert it to 

```python
import io
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import matplotlib.pyplot as plt

app = FastAPI()

@app.get("/plot")
async def get_plot(fig):
    
    # 1. Convert the figure to PNG image bytes using BytesIO
    img_io = io.BytesIO()
    fig.savefig(img_io, format='png')
    img_io.seek(0)  # Rewind the buffer to the beginning
    
    # 2. Return the image as a StreamingResponse
    return StreamingResponse(img_io, media_type="image/png")
```

## Example 1 - Getting Start with Auto Clean Data

```python
import os
import pandas as pd
from smartdata import SmartData
from dotenv import load_dotenv

load_dotenv()
os.getenv('OPENAI_API_KEY')

# Or Set OpenAI API key here :)
# os.environ["OPENAI_API_KEY"] = "Your openai key"

# Read sample data
df = pd.read_csv(r"https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv", index_col=0)

# Create SmartData Model
sd = SmartData(df, memory_size = 0, show_detail = True)
prompt, sd_model = sd.create_model()

# Clean Data 
# - summary: this is a summary of data cleaning result include action taken, impacted records etc. 
# - has_changes_to_df: this is a boolean to indicate whether any changes to the existing df.
# - df_new: this is the new cleaned dataframe after all the clean process.
summary, has_changes_to_df, df_new = sd.clean_data()
print(summary)
print("has_changes_to_df: "+has_changes_to_df)
print(df_new.head(5))

```

## Example 2 - Q&A with Auto Clean Data

```python
import os
import pandas as pd
from smartdata import SmartData
from dotenv import load_dotenv
from matplotlib import pyplot as plt

load_dotenv()
os.getenv('OPENAI_API_KEY')

# Or Set OpenAI API key here :)
# os.environ["OPENAI_API_KEY"] = "Your openai key"

# Load sample data
df_clean = pd.read_csv(r"https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv", index_col=0)

# Initialize SmartData Model to clean up data
sd_clean = SmartData(df_list=df_clean, memory_size=0, show_detail=False)
prompt, sd_model = sd_clean.create_model()
summary, has_changes_to_df, df_new = sd_clean.clean_data()

# Initialize SmartData Model with memory for the last 3 conversations and detailed outputs
# Load in cleaned data
smartdata_qa = SmartData(df_list=df_new, memory_size=3, show_detail=False)
qa_prompt, qa_model = smartdata_qa.create_model()

# Start Q&A session -------------------------------------------------

# Output Explanation:
# answer: The response to your question, formatted in markdown.
# has_plots: Boolean indicating if a chart was generated.
# has_changes_to_df: Boolean indicating if the dataframe was updated.
# image_fig_list: List of matplotlib figures (if has_plots is True).
# df_new: Updated dataframe (if has_changes_to_df is True); otherwise, a copy of the original dataframe.
# response: Detailed output of all intermediate steps generated by the model.
# code_list_plot_with_add_on: Python code to generate the figures in image_fig_list.
# code_list_datachange_with_add_on: Python code to apply the dataframe updates resulting in df_new.

# Q1 - General analytics question - no charting no new dataframe
question_1 = "Please show me the average fare by sex in a table."
answer, has_plots, has_changes_to_df, image_fig_list, df_new, response, code_list, code_list_plot_with_add_on, code_list_datachange_with_add_on = smartdata_qa.run_model(question=question_1)
print("\n------------Q1------------\n")
print(answer)
print("has_plots - " + str(has_plots))
print("has_changes_to_df - " + str(has_changes_to_df))

# Q2 - Ask for making a chart
question_2 = "Please make a bar chart with average Age by Pclass."
answer, has_plots, has_changes_to_df, image_fig_list, df_new, response, code_list, code_list_plot_with_add_on, code_list_datachange_with_add_on = smartdata_qa.run_model(question=question_2)
print("\n------------Q2------------\n")
print(answer)
print("has_plots - " + str(has_plots))
print("has_changes_to_df - " + str(has_changes_to_df))
for fig in image_fig_list:
    plt.show(fig)

# Q3 - Ask for data transformation
question_3 = "Can you create a new column called age over 30, valid entries are yes or no."
answer, has_plots, has_changes_to_df, image_fig_list, df_new, response, code_list, code_list_plot_with_add_on, code_list_datachange_with_add_on = smartdata_qa.run_model(question=question_3)
print("\n------------Q3------------\n")
print(answer)
print("has_plots - " + str(has_plots))
print("has_changes_to_df - " + str(has_changes_to_df))
print(df_new.head(3))

# Q4 - Chat with memory
question_4 = "Can you delete the new column you just created?"
answer, has_plots, has_changes_to_df, image_fig_list, df_new, response, code_list, code_list_plot_with_add_on, code_list_datachange_with_add_on = smartdata_qa.run_model(question=question_4)
print("\n------------Q4------------\n")
print(answer)
print("has_plots - " + str(has_plots))
print("has_changes_to_df - " + str(has_changes_to_df))
print(df_new.head(3))

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change. Email us at contact@talentainow.com

## License

[MIT](https://choosealicense.com/licenses/mit/)