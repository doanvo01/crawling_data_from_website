# Crawling Q&A dataset from Website (Korean and Vietnamese)
## 1. Goal:
To create a chatbot for question and answer that support reduce the work-load of human instructors. This code can crawl Q&A dataset from:
-Navercafe web: garthering informations including "published_date", "categories", "question or concern", "content of problem", "answer the question or concern", "link referened and "Crawed date".    
## 2. Method:
- Applying large language model (LLM)-based approaches to improve the coverage and answer quality over traditional Q&A methods.
      - Pre-trained LLama 3 models using the question and system describes in the prompt. We adopt fine-tuning techniques in our experiments, like zero-shot prompting, supervised fine-tuning (SFT) with and without assist of retrieval-augmented generation (RAG).
      - To adapt requirements of memory where (LLMs) are often too large to run on consumer hardware. These models may exceed billions of parameters and generally need GPUs with large amounts of VRAM to speed up inference. Therefore, we use quantization for LLMs that can help these models smaller through improved training, adapters, ...
  
## 3. Main Steps:
- Data Collection: Crawled customer questions and answers from Navercafe using JSON requests to obtain a diverse dataset for training, testing, and validation.
- Data Preprocessing: Apply TensorFlow and Keras for data preprocessing, including text tokenization, remove accent and padding sequences,...
- Model Building: Create a LLMs to capture complex patterns and dependencies in the text data.
- Model Training: Train the deep learning model on the preprocessed dataset.
- Model Evaluation: Evaluate the accuracy and performance of analysis approaches by precision, recall and f1-score.
- Utilize Model: Apply for new dataset to predict anwers of  customer.
