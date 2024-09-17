from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

import pandas as pd
import numpy as np

import base64
import os
import io
import json
import ast
import copy
import logging
logger = logging.getLogger('SmartData')

from .config import Config
from .memory import Memory  # Import Memory from memory.py
from .custom_agent import *
from .util import *

global config
config = dict(Config.__dict__)

class SmartData:
    def __init__(self, df_list, llm = None, show_detail = config['SHOW_DETAIL'], memory_size = config['MEMORY_SIZE'], 
                 max_iterations = config['MAX_ITERATIONS'], max_execution_time = config['MAX_EXECUTION_TIME'], seed = 0):
        
        # Use ChatGPT 4o-mini by default
        if llm is None:
            chat_llm = ChatOpenAI(temperature=config['TEMP_CHAT'], model=config['CHAT_MODEL'], seed = seed)
            self.llm = chat_llm
        else:
            self.llm = llm
        
        self.df_list = copy.deepcopy(df_list)
        self.df_change = []
        self.memory_size = memory_size
        self.max_iterations = max_iterations
        self.max_execution_time = max_execution_time
        self.show_detail = show_detail
        self.image_fig_list = []
        self.check_error_substring_list = config['CHECK_ERROR_SUBSTRING_LIST']
        self.check_plot_substring_list = config['CHECK_PLOT_SUBSTRING_LIST']
        self.add_on_plot_library_list = config["ADD_ON_PLOT_LIBRARY_LIST"]

        self.check_datachange_substring_list = config['CHECK_DATACHANGE_SUBSTRING_LIST']
        self.add_on_datachange_library_list = config["ADD_ON_DATACHANGE_LIBRARY_LIST"]
        
        self.prompt_clean_data = config["PROMPT_CLEAN_DATA"]
        self.prompt_create_data_clean_summary = config["PROMPT_CREATE_DATA_CLEAN_SUMMARY"]
        
        self.model = None
        self.memory = Memory()
        self.message_count = 1
        # self.df
        # self.create_model()

    def create_model(self, use_openai_llm = True, seed = 0):
        df = self.df_list
        prefix_df = config['DEFAULT_PREFIX_SINGLE_DF']
        if use_openai_llm:
            self.llm = ChatOpenAI(temperature=config['TEMP_CHAT'], model=config['CHAT_MODEL'], seed = seed)
        
        prompt, agent_executor = custom_create_pandas_dataframe_agent(llm = self.llm,df = df,
            verbose=self.show_detail,
            return_intermediate_steps = True,
            agent_type="tool-calling",
            allow_dangerous_code=True,
            prefix = prefix_df,
            max_iterations = self.max_iterations,
            max_execution_time=self.max_execution_time,
            agent_executor_kwargs={'handle_parsing_errors':True}
        )
        self.model = agent_executor
        return prompt, agent_executor

    def run_model(self, question):
        for i in range(10):
            prompt, _ = self.create_model(use_openai_llm = True, seed = i)
            try:
                # self.image_fig_list.clear()
                self.image_fig_list.clear()
                self.df_change.clear()
                chat_model = self.model
                code_list = []
                code_list_plot_wo_add_on = []
                code_list_plot_with_add_on = []

                code_list_datachange_wo_add_on = []
                code_list_datachange_with_add_on = []
                has_plots = False
                has_changes_to_df = False
                new_prompt = None

                question_with_history = copy.deepcopy(question)
                if self.memory.is_not_empty():
                    question_with_history = f"My question is: {question}. Below is the our previous conversation and codes in chronological order, from the earliest to the latest.: {self.memory.recall_last_conversation(self.memory_size)}."
                
                response = chat_model.invoke({"input": question_with_history})
                answer = response['output']
                code_list = self.extract_code_from_response(response)

                # Process plot into fig -------------------------------------------------------------------------------------------------------------------------
                if len(code_list)>0:
                    code_list_plot_wo_add_on, code_list_plot_with_add_on = self.process_with_plot_code(code_list)

                if len(code_list_plot_with_add_on)>0:
                    for plot_code in code_list_plot_with_add_on:
                        exec(plot_code, {'image_fig_list': self.image_fig_list, 'df': self.df_list},{})
                    if len(self.image_fig_list)>0:
                        has_plots = True
                        # print("no plot code")

                # Process data change into a new dataset --------------------------------------------------------------------------------------------------------
                if len(code_list)>0:
                    code_list_datachange_wo_add_on, code_list_datachange_with_add_on = self.process_with_datachange_code(code_list)

                if len(code_list_datachange_with_add_on)>0:
                    for data_code in code_list_datachange_with_add_on:
                        exec(data_code, {'df_change': self.df_change, 'df': self.df_list},{})
                        # data_code_exe = True
                        # print("no plot code")
                    if len(self.df_change)>0:
                        has_changes_to_df = not self.df_list.equals(self.df_change[-1])
                        self.df_list = copy.deepcopy(self.df_change[-1])
                        new_prompt, _ = self.create_model(use_openai_llm = True, seed = i)

                # Store the chat history
                self.remember_conversation(question, answer,code_list,code_list_plot_wo_add_on)
                if any(error_substring in str(answer) for error_substring in config['AGENT_STOP_SUBSTRING_LIST']):
                    answer = config['AGENT_STOP_ANSWER']
                else:
                    break
            except Exception as e:
                    print(f"Fail to process: {e}")

        return answer, has_plots, has_changes_to_df, self.image_fig_list, self.df_list, response, code_list, code_list_plot_with_add_on, code_list_datachange_with_add_on
        # return answer, self.image_fig_list, response, code_list, code_list_plot_with_add_on, new_prompt

    def clean_data_without_ai(self):
        df_clean_without_ai, summary_without_ai = clean_dataframe(df = self.df_list)
        self.df_list = df_clean_without_ai
        return summary_without_ai, df_clean_without_ai

    def clean_data_with_ai(self):
        # data_before_ai = self.df_list
        # self.df_list = data_before_ai
        # new_prompt, _ = self.create_model(use_openai_llm = True, seed = 0)
        # print(new_prompt)
        answer, has_plots, has_changes_to_df, image_fig_list, df_new, response, code_list, code_list_plot_with_add_on, code_list_datachange_with_add_on = self.run_model(question = self.prompt_clean_data)
        return answer, has_changes_to_df, df_new

    def clean_data(self):
        summary = ""
        summary_without_ai, df_clean_without_ai = self.clean_data_without_ai()
        answer, has_changes_to_df, df_new = self.clean_data_with_ai()
        summary = summary_without_ai + answer
        _, final_summary = self.create_data_clean_summary(summary)
        return final_summary, has_changes_to_df, self.df_list

    def create_data_clean_summary(self, result):
        human_template = config['PROMPT_CREATE_DATA_CLEAN_SUMMARY']
        prompt_template_list = [human_template]
        prompt_template= '\n\n'.join(prompt_template_list)

        summary_prompt = PromptTemplate(template = prompt_template,input_variables = ['result'])
        message = summary_prompt
    
        summary_model = ChatOpenAI(temperature=config['TEMP_CHAT'],model=config['CHAT_MODEL'], seed = 0)
        
        chain = summary_prompt | summary_model | StrOutputParser()
        answer = chain.invoke({"result": result,
                            })
        return message, answer
    
    def remember_conversation(self, question, answer,code_list, code_list_plot_wo_add_on):
        self.memory.remember(key = self.message_count, role = 'Human', value = question)
        self.memory.remember(key = self.message_count, role = 'AI', value = answer)
        # self.memory.remember(key = self.message_count, role = 'All Codes', value = code_list)
        self.memory.remember(key = self.message_count, role = 'Plot Code Generate By AI', value = code_list_plot_wo_add_on)
        self.message_count = self.message_count + 1

    def recall_all_conversation(self):
        return self.memory.recall_all()

    def recall_last_conversation(self,number_last_conversation):
        return self.memory.recall_last_conversation(number_last_conversation)

    def clear_all_conversation(self):
        return self.memory.clear_all_conversation()
    
    def extract_code_from_response(self, response):
        code_list = []
        try:
            last_response = response['intermediate_steps'][-1]
            if (len(last_response)>1 and len(str(last_response[1])) == 0) or (len(last_response)==1) or ((len(last_response)>1) and (not any(substring in str(last_response[1]).lower() for substring in self.check_error_substring_list))):
                for tool_call in response['intermediate_steps'][-1][0].message_log[0].tool_calls:
                    # print("\n-----\n")
                    # print(call)
                    # print(call['name'])
                    # print(tool_call['args']['query'])
                    if tool_call['name'] == 'python_repl_ast':
                        code = tool_call['args']['query']
                        code_list.append(code)
        except:
            code_list = []
        return code_list

    def process_with_plot_code(self, string_list):
        # Filter only the code with all required plot substrings
        code_list_plot_wo_add_on = [
            s for s in string_list 
            if all(substring in s for substring in self.check_plot_substring_list)
        ]
        
        # Make sure no duplicates
        code_list_plot_wo_add_on = list(dict.fromkeys(code_list_plot_wo_add_on))
    
        # Add in the import library if they are missing from the plot to make it produce figs
        for i in range(len(code_list_plot_wo_add_on)):
            missing_imports = [
                library for library in self.add_on_plot_library_list if library not in code_list_plot_wo_add_on[i]
            ]
            if missing_imports:
                # Add the missing imports at the top of the plot code
                code_list_plot_wo_add_on[i] = "\n".join(missing_imports) + "\n" + code_list_plot_wo_add_on[i]

        # Add in the long label at the end
        add_on_format_long_label = config['ADD_ON_FORMAT_LABEL_FOR_AXIS']
        code_list_plot_with_add_on_label = [
            code + add_on_format_long_label for code in code_list_plot_wo_add_on]
        
        # Add in the fig code at the end
        add_on_fig = config['ADD_ON_FIG']
        code_list_plot_with_add_on_label_fig = [
            code + add_on_fig for code in code_list_plot_with_add_on_label
        ]
        
        return code_list_plot_wo_add_on, code_list_plot_with_add_on_label_fig

    def process_with_datachange_code(self, string_list):
        # Filter only the code with all required plot substrings
        code_list_datachange_wo_add_on = [
            s for s in string_list 
            if all(substring in s for substring in self.check_datachange_substring_list)
        ]
        
        # Make sure no duplicates
        code_list_datachange_wo_add_on = list(dict.fromkeys(code_list_datachange_wo_add_on))
    
        # Add in the import library if they are missing
        for i in range(len(code_list_datachange_wo_add_on)):
            missing_imports = [
                library for library in self.add_on_datachange_library_list if library not in code_list_datachange_wo_add_on[i]
            ]
            if missing_imports:
                # Add the missing imports at the top of the plot code
                code_list_datachange_wo_add_on[i] = "\n".join(missing_imports) + "\n" + code_list_datachange_wo_add_on[i]

        # Add in the df_change code at the end
        add_on_df = config['ADD_ON_DF']
        code_list_datachange_with_add_on = [
            code + add_on_df for code in code_list_datachange_wo_add_on
        ]
        
        return code_list_datachange_wo_add_on, code_list_datachange_with_add_on
