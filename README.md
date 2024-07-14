# OAI-API-MMLU-Pro

This is a modified version of https://github.com/chigkim/Ollama-MMLU-Pro benchmark via the OpenAI Chat Completion API. Works great for VLLM or Aphrodite engine for super fast batching inference.

The  testing and scoring  method is exactly the same as the original script from TIGER-LAB, adding only a few features to simplify running the test and displaying the results. To see the exact changes, compare between mmlu-pro branch against main with git diff:

```bash
git diff mmlu-pro..main -- run_openai.py
```

This fork adds support and the dataset for Indonesian MMLU-Pro testing and also some small fixes like: 
- Prevent errors when there is zero random guesses.
- Ignore words inside brackets of answer and only take the letter as answer.
- Include square brackets [ ] for answer format as well as regular brackets ( ).

## Usage

Change the config.toml according to your setup.

```shell
pip install -r requirements.txt
python run_openai.py # Or run_openai_id.py for Indonesian.
```

You can also override   settings in configuration file    with  command line flags like --model, ----category, etc. For example, if you   specify `--model phi3`, all the settings  from configuration file will be loaded except model. See `python run_openai.py -h` for more info.

## Additional Notes

* If an answer cannot be extracted from the model's response, the script will randomly assign an answer. It's the same way as the original script.
* The total score represents the number of correct answers out of the total number of attempts including random guess attempts. This is the score from the original script.
* "Random Guess Attempts" indicates the total number of random guesses out of the total attempts.
* "Correct Random Guesses" shows the number of random guesses that were correct out of all the random guesses.
* "Adjusted Score Without Random Guesses" subtracts all random guesses from the correct answers and the total answers.
* The last overall   score in the table  is calculated as: the total number of correct answers across all categories / the total number of all attempts across all categories * 100.
* All the   scores in percentage are rounded numbers.

## Example config file
```yaml
[server]
url = "http://localhost:8000/v1"
api_key = "api key"
model = "llama3"
timeout = 600.0

[inference]
# Ssettings   below are from evaluate_from_local.py for VLLM  on TIGER-AI-Lab/MMLU-Pro
temperature = 0.0
top_p = 1.0 # not specified but  default for VLLM
max_tokens = 1024

# The variable {subject} will be replaced with appropriate value in  runtime.
system_prompt = "You are an expert assitant AI that knows everything. You are tasked with answering a multiple-choice question. The following is a multiple choice question (with answers) about {subject}. Give your final answer in the format of `The answer is (chosen answer)`."

# "single_chat" inserts all the COT examples and question into a single message. Default  style for GPT-4O script, but raises a lot of format issues especially for small models.
# "multi_chat" inserts COT examples into multi-turn messages. Use for instruct/chat models.
# "no_chat" uses v1/completion api. Use for non-instruct/chat model.
style = "multi_chat"

[test]
categories = ['biology', 'business', 'chemistry', 'computer science', 'economics', 'engineering', 'health', 'history', 'law', 'math', 'philosophy', 'physics', 'psychology', 'other']
parallel = 16

[log]
# Verbosity between 0-2
verbosity = 0
# If true, logs exact prompt sent to the model in the test result files.
log_prompt = true
```