# Crawling Q&A dataset from Website (Korean and Vietnamese)
## 1. Goal:
The objective of this project is to create a chatbot capable of answering questions to reduce the workload of human instructors. This code facilitates the crawling of Q&A datasets from the Navercafe website, gathering the following information:
      + Published Date
      + Categories
      + Question or Concern
      + Content of Problem
      + Answer to the Question or Concern
      + Link Referenced
      + Crawled Date

## 2. Method:
- The project utilizes Large Language Model (LLM)-based approaches to enhance the coverage and quality of answers compared to traditional Q&A methods:
+ LLama 3 Pre-training and Fine-tuning:

      + Use pre-trained LLama 3 models with prompts tailored to specific tasks.
      + Apply fine-tuning techniques, such as zero-shot prompting, supervised fine-tuning (SFT), and retrieval-augmented generation (RAG).
+ Efficient Resource Utilization:

      + Address the memory and hardware limitations of large LLMs, which often require high VRAM GPUs.
      + Leverage quantization techniques and lightweight adapters to make the models smaller and more efficient for consumer hardware.
## 3. Main Steps:
1. Data Collection

      + Crawl customer questions and answers from Navercafe using JSON requests to create a comprehensive dataset for training, testing, and validation.
2. Data Preprocessing

      + Utilize TensorFlow and Keras to preprocess data, including:
            + Text tokenization
            + Removing accents
            + Padding sequences
3. Model Building

      + Build LLMs to capture complex patterns and dependencies in textual data.
4. Model Training

      + Train the models on the preprocessed dataset for robust question-answering capabilities.
5. Model Evaluation

      + Evaluate model performance using metrics such as precision, recall, and F1-score.
6. Utilize the Model

      + Apply the trained model to new datasets for predicting customer answers.

## 4. Repository:
This project includes:

      + Crawling scripts
      + Preprocessing tools
      + Training and evaluation scripts
      + Deployment-ready chatbot implementations
