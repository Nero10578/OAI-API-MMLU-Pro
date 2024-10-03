import os
import json
import matplotlib.pyplot as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Generate bar graphs from benchmark results.")
parser.add_argument('--benchmark-folder', type=str, required=True, help='Path to the benchmark results folder')
parser.add_argument('--output-folder', type=str, required=True, help='Path to the output folder where graphs will be saved')
args = parser.parse_args()

benchmark_folder = args.benchmark_folder
output_folder = args.output_folder

os.makedirs(output_folder, exist_ok=True)

model_data = {}
categories = set()

for model_folder in os.listdir(benchmark_folder):
    model_path = os.path.join(benchmark_folder, model_folder)
    
    if os.path.isdir(model_path):
        model_summary = {"Model": model_folder}
        total_corr = 0
        total_wrong = 0
        total_no_answer = 0
        
        for result_file in os.listdir(model_path):
            if result_file.endswith("_summary.json"):
                result_path = os.path.join(model_path, result_file)
                
                with open(result_path, 'r') as f:
                    result_data = json.load(f)
                
                for category, data in result_data.items():
                    if category == 'total':
                        continue
                    
                    categories.add(category.capitalize())
                    
                    corr = data.get('corr', 0)
                    wrong = data.get('wrong', 0)
                    no_answer = data.get('no_answer', 0)
                    total_questions_category = corr + wrong
                    
                    accuracy_percent = (corr / total_questions_category) * 100 if total_questions_category > 0 else 0
                    no_answer_percent = (no_answer / total_questions_category) * 100 if total_questions_category > 0 else 0

                    model_summary[f"{category.capitalize()} Accuracy %"] = accuracy_percent
                    model_summary[f"{category.capitalize()} No Answer %"] = no_answer_percent
                    
                    total_corr += corr
                    total_wrong += wrong
                    total_no_answer += no_answer
        
        total_questions = total_corr + total_wrong
        total_accuracy_percent = (total_corr / total_questions) * 100 if total_questions > 0 else 0
        total_no_answer_percent = (total_no_answer / total_questions) * 100 if total_questions > 0 else 0
        
        model_summary['Total Accuracy %'] = total_accuracy_percent
        model_summary['Total No Answer %'] = total_no_answer_percent
        
        model_data[model_folder] = model_summary

categories = sorted(categories)
models = sorted(list(model_data.keys()))  # Sort models alphabetically
category_accuracy = {cat: [] for cat in categories}
category_no_answer = {cat: [] for cat in categories}
total_accuracy = []
total_no_answer = []

for model in models:
    for category in categories:
        category_accuracy[category].append(model_data[model].get(f"{category} Accuracy %", 0))
        category_no_answer[category].append(model_data[model].get(f"{category} No Answer %", 0))
    total_accuracy.append(model_data[model].get("Total Accuracy %", 0))
    total_no_answer.append(model_data[model].get("Total No Answer %", 0))

def create_horizontal_bar_graph(y_labels, x_values, title, x_label, file_name):
    y = np.arange(len(y_labels))
    plt.figure(figsize=(10, 6))
    bars = plt.barh(y, x_values, color='skyblue')
    plt.yticks(y, y_labels)
    plt.xlabel(x_label)
    plt.title(title)
    plt.tight_layout()
    
    for bar in bars:
        xval = bar.get_width()
        if xval == 0:  
            plt.text(xval + 0.05, bar.get_y() + bar.get_height()/2, f'{xval:.2f}', va='center', color='black')
        else:
            plt.text(xval - 0.05, bar.get_y() + bar.get_height()/2, f'{xval:.2f}', va='center', color='black')
    
    max_xval = max(x_values)
    plt.xlim(0, max_xval * 1.1)
    
    plt.savefig(os.path.join(output_folder, file_name), format='png')
    plt.close()

for category in categories:
    create_horizontal_bar_graph(models, category_accuracy[category], f"{category} Accuracy Comparison", "Accuracy %", f"{category}_Accuracy_Comparison.png")
    create_horizontal_bar_graph(models, category_no_answer[category], f"{category} No Answer Comparison", "No Answer %", f"{category}_No_Answer_Comparison.png")

create_horizontal_bar_graph(models, total_accuracy, "Total Accuracy Comparison", "Total Accuracy %", "Total_Accuracy_Comparison.png")
create_horizontal_bar_graph(models, total_no_answer, "Total No Answer Comparison", "Total No Answer %", "Total_No_Answer_Comparison.png")
