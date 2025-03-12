#Option 1: Create virtual environment locally
conda create -n sdv_test python=3.10 anaconda
#To activate
conda activate sdv_test 
#To deactivate
conda deactivate

#Option 2: If you are not using conda, you can also use python
#On Mac
python -m sdv_test .venv
#To activate
source .venv/bin/activate
#To deactivate
deactivate

#On Windows
python -m venv sdv_test
#To activate
sdv_test\Scripts\activate
#To deactivate
deactivate

#Go to SDV-main and install required dependencies
pip install --upgrade pip
pip install -r requirements.txt

#If your OS cannot run the requirements.txt successfully, you can also manually install 
pip install pandas faker copulas rdt graphviz platformdirs pyyaml cloudpickle tqdm ctgan sdmetrics deepecho

#To fix conflict issues
pip install --upgrade "click>=8.1.3"
pip uninstall rundoc

#If you have Numpy,Scipy or Pandas conflict issues:
pip uninstall -y numpy scipy
rm -rf ~/.local/lib/python3.10/site-packages/numpy*
rm -rf ~/.local/lib/python3.10/site-packages/scipy*
pip install numpy==1.23.5 scipy==1.10.1
python -c "import numpy, scipy; print(numpy.__version__, scipy.__version__)"
pip install --upgrade pandas sdv copulas



#Process missing data
#--method 1: Generate a random value
#--method 2: Use mean/mode values
#--method 3: Discard rows with missing data


#Run with default output file (cleaned_data.csv)
#If you see module not found error, please use pip install MODULE_NAME to install and rerun
python handle_missing_data.py --input test.csv --metadata test.json --method 1

#Run with a custom output file
python handle_missing_data.py --input test.csv --metadata test.json --method 2 --output processed_data.csv

#Run in Debug Mode (-d to print modified rows)
python handle_missing_data.py --input test.csv --metadata test.json --method 1 -d


#Run test generation with the --synthesizer flag to choose the model:
#Gaussian Copula Synthesizer
#Model: Probabilistic model using Gaussian copula functions
#Strengths:
##Fastest among all
##Works well for numerical and categorical data
##Can handle small datasets
#Weaknesses:
##Assumes normal distribution
##Struggles with highly complex relationships
#Best for: Simple structured datasets with moderate correlations
python test.py --input cleaned_data.csv --metadata test.json --synthesizer gaussian

#CTGAN Synthesizer
#Model: Conditional Tabular GAN
#Strengths:
##Handles complex relationships and multimodal distributions
##Good for mixed data types (categorical & numerical)
#Weaknesses:
##Slower training time
##Needs more data for training
#Best for: Complex datasets with both categorical and numerical variables
python test.py --input cleaned_data.csv --metadata test.json --synthesizer ctgan

#TVAESynthesizer
#Model: Variational Autoencoder (VAE)
#Strengths:
##Good for modeling tabular data with complex structures
##Works well with missing data
#Weaknesses:
##Computationally expensive
##May overfit on small datasets
#Best for: Datasets with missing values and strong nonlinear dependencies
python test.py --input cleaned_data.csv --metadata test.json --synthesizer tvae

#CopulaGAN Synthesizer
#Model: Hybrid of Copula models & GANs
#Strengths:
##Captures complex dependencies while being more stable than CTGAN
##Works well with both categorical and numerical features
#Weaknesses:
##Slower than Gaussian Copula
##Still needs enough data for effective training
#Best for: Medium to large datasets with nontrivial dependencies
python test.py --input cleaned_data.csv --metadata test.json --synthesizer copulagan