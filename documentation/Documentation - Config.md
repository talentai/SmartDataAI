
# Configuration Documentation

This document provides an overview of the `Config` class, which contains default settings for the `SmartData` application. These settings govern the behavior of chat models, agents, and data cleaning prompts, along with plotting and data transformation settings.

---

### `Config`

#### Class Variables:

---

#### **Chat Model Settings:**

- **`TEMP_CHAT`**: `int`  
  Default value: `0`  
  Description: The temperature for the chat model's responses, which controls the randomness of the output.

- **`CHAT_MODEL`**: `str`  
  Default value: `'gpt-4o-mini'`  
  Description: The chat model to be used (e.g., `gpt-4o-mini` or other versions).

---

#### **Agent Settings:**

- **`SHOW_DETAIL`**: `bool`  
  Default value: `False`  
  Description: Controls whether details are displayed during the agent’s operation.

- **`MEMORY_SIZE`**: `int`  
  Default value: `5`  
  Description: Specifies the number of previous conversations the agent will remember.

- **`MAX_ITERATIONS`**: `int`  
  Default value: `60`  
  Description: Maximum number of iterations the agent can perform in a single task.

- **`MAX_EXECUTION_TIME`**: `int`  
  Default value: `60` (seconds)  
  Description: Maximum time allowed for a task to execute before being stopped.

- **`AGENT_STOP_SUBSTRING_LIST`**: `list[str]`  
  Default value: A list containing substrings like `"Agent stopped"`, `"import pandas as pd"`, etc.  
  Description: A list of substrings that will trigger the agent to stop if detected in the response.

- **`AGENT_STOP_ANSWER`**: `str`  
  Default value: A message guiding the user to rephrase their request.  
  Description: The agent's response when it's unable to answer due to complexity.

---

#### **Plotting Settings:**

- **`CHECK_ERROR_SUBSTRING_LIST`**: `list[str]`  
  Default value: `["error", "invalid", "incomplete"]`  
  Description: A list of substrings to detect errors in plotting code.

- **`CHECK_PLOT_SUBSTRING_LIST`**: `list[str]`  
  Default value: `["plt.tight_layout()"]`  
  Description: A list of substrings required for plot generation.

- **`ADD_ON_PLOT_LIBRARY_LIST`**: `list[str]`  
  Default value: A list including `"import matplotlib.pyplot as plt"`, `"import pandas as pd"`, `"import numpy as np"`, etc.  
  Description: List of required libraries to be imported when generating plots.

- **`ADD_ON_FIG`**: `str`  
  Default value: A code snippet to append the figure to `image_fig_list`.  
  Description: Adds generated figures to a predefined list.

- **`ADD_ON_FORMAT_LABEL_FOR_AXIS`**: `str`  
  Default value: Code that formats labels on the x and y axes for better readability.  
  Description: Ensures long labels on axes are formatted properly.

---

#### **Data Change Settings:**

- **`CHECK_DATACHANGE_SUBSTRING_LIST`**: `list[str]`  
  Default value: `["df_update"]`  
  Description: List of substrings required for detecting changes in the dataset.

- **`ADD_ON_DATACHANGE_LIBRARY_LIST`**: `list[str]`  
  Default value: Libraries required for data change, such as `"import pandas as pd"` and `"import copy"`.  
  Description: List of libraries that are appended to data transformation code.

- **`ADD_ON_DF`**: `str`  
  Default value: A code snippet to append updates to the dataframe (`df_change.append(df_update)`).  
  Description: Adds the updated dataframe to a list for further processing.

---

#### **Model Prompt Settings:**

- **`PROMPT_CLEAN_DATA`**: `str`  
  Default value: A detailed prompt guiding the AI model to clean the dataframe.  
  Description: This prompt specifies rules for cleaning categorical and numeric columns, with intelligent merging and value replacement.

- **`PROMPT_CREATE_DATA_CLEAN_SUMMARY`**: `str`  
  Default value: A template to summarize the cleaning result for non-technical audiences.  
  Description: Helps create a concise, user-friendly summary of the data cleaning results.

---

#### **Miscellaneous Settings:**

- **`DEFAULT_PREFIX_SINGLE_DF`**: `str`  
  Default value: A detailed instruction set for how to handle a single dataframe during plotting, data science, or cleaning tasks.  
  Description: Provides detailed instructions for the AI agent to process the dataframe, including how to import required libraries and create visualizations or analysis reports.

---

### `__init__` Method (Static)

The constructor (`__init__`) method is defined but not used in this class. It is included to allow future extensions or initialization logic if necessary.

```python
@staticmethod
def __init__():
    pass
```
