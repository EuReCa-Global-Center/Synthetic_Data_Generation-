Setup Instructions

Option 1: Create a Virtual Environment Locally using Conda
	1.	Create a new Conda environment:

conda create -n sdv_test python=3.10 anaconda


	2.	To activate the environment:

conda activate sdv_test


	3.	To deactivate the environment:

conda deactivate



Option 2: Create a Virtual Environment Using Python (If not using Conda)

On macOS/Linux:
	1.	Create a new virtual environment:

python -m venv .venv


	2.	To activate the environment:

source .venv/bin/activate


	3.	To deactivate the environment:

deactivate



On Windows:
	1.	Create a new virtual environment:

python -m venv sdv_test


	2.	To activate the environment:

sdv_test\Scripts\activate


	3.	To deactivate the environment:

deactivate



Install Required Dependencies
	1.	Upgrade pip and install dependencies:

pip install --upgrade pip
pip install -r requirements.txt


	2.	If you encounter issues with the requirements.txt, manually install the necessary packages:

pip install pandas faker copulas rdt graphviz platformdirs pyyaml cloudpickle tqdm ctgan sdmetrics deepecho


	3.	To fix any conflict issues, update or uninstall problematic packages:

pip install --upgrade "click>=8.1.3"
pip uninstall rundoc


	4.	If you encounter NumPy, SciPy, or Pandas conflicts:

pip uninstall -y numpy scipy
rm -rf ~/.local/lib/python3.10/site-packages/numpy*
rm -rf ~/.local/lib/python3.10/site-packages/scipy*
pip install numpy==1.23.5 scipy==1.10.1
python -c "import numpy, scipy; print(numpy.__version__, scipy.__version__)"
pip install --upgrade pandas sdv copulas

Handling Missing Data

You can handle missing data in three different ways:
	•	Method 1: Generate a random value for missing data.
	•	Method 2: Use the mean or mode values.
	•	Method 3: Discard rows with missing data.

Example Usage:
	1.	Run the script with the default output file (cleaned_data.csv):

python handle_missing_data.py --input test.csv --metadata test.json --method 1


	2.	Run with a custom output file:

python handle_missing_data.py --input test.csv --metadata test.json --method 2 --output processed_data.csv


	3.	Run in debug mode (use -d to print modified rows):

python handle_missing_data.py --input test.csv --metadata test.json --method 1 -d

Data Generation with Different Synthesizers

Choose a synthesizer model based on your dataset:

1. Gaussian Copula Synthesizer
	•	Model: Probabilistic model using Gaussian copula functions.
	•	Strengths:
	•	Fastest model.
	•	Works well for numerical and categorical data.
	•	Handles small datasets.
	•	Weaknesses:
	•	Assumes normal distribution.
	•	Struggles with highly complex relationships.
	•	Best for: Simple structured datasets with moderate correlations.
	•	Command:

python test.py --input cleaned_data.csv --metadata test.json --synthesizer gaussian



2. CTGAN Synthesizer
	•	Model: Conditional Tabular GAN.
	•	Strengths:
	•	Handles complex relationships and multimodal distributions.
	•	Works well for mixed data types (categorical & numerical).
	•	Weaknesses:
	•	Slower training time.
	•	Needs more data for training.
	•	Best for: Complex datasets with both categorical and numerical variables.
	•	Command:

python test.py --input cleaned_data.csv --metadata test.json --synthesizer ctgan



3. TVAE Synthesizer
	•	Model: Variational Autoencoder (VAE).
	•	Strengths:
	•	Good for modeling tabular data with complex structures.
	•	Works well with missing data.
	•	Weaknesses:
	•	Computationally expensive.
	•	May overfit on small datasets.
	•	Best for: Datasets with missing values and strong nonlinear dependencies.
	•	Command:

python test.py --input cleaned_data.csv --metadata test.json --synthesizer tvae



4. CopulaGAN Synthesizer
	•	Model: Hybrid of Copula models & GANs.
	•	Strengths:
	•	Captures complex dependencies while being more stable than CTGAN.
	•	Works well with both categorical and numerical features.
	•	Weaknesses:
	•	Slower than Gaussian Copula.
	•	Needs enough data for effective training.
	•	Best for: Medium to large datasets with nontrivial dependencies.
	•	Command:

python test.py --input cleaned_data.csv --metadata test.json --synthesizer copulagan