# miRNA and Disease Association Finder

The command\_line.py script finds  associations between microRNAs \(miRNA\) and diseases on the provided dataset. The script has the capability of investigating diseases associated with a given miRNA or identify miRNAs linked to a specific disease. Additionally, the program allows partial matching for both miRNA and disease names.

## Prerequisites

- Python 3
- Pandas library (`pip install pandas`)

## Usage

For gene confidence, the default value is 81, and it must be between 81 and 100.
For disease score, the default value is 0.8, and it must be between 0.81 and 1.
Important: Only one argument \(miRNA, disease, miRNA partial, or disease partial\) can be provided for functionality purposes. Please refer to the examples for correct usage.

### Command-line arguments

- `-m, --miRNA`: Specify the miRNA to find associated diseases.
- `-d, --disease`: Specify the disease to find associated miRNAs. Note: For multi\-word diseases, use quotation marks.
- `-sb, --scoreBoolean`: Print gene to disease score if set to `True` \(default is `False`\). The following 'yes', or  'true', or 't', or  'y', or  '1'\) are also accepted as True. And, 'no', 'false', 'f', 'n', '0' are accepted as False
- `-cb, --confBoolean`: Print miRNA to gene confidence if set to `True` \(default is `False`\). The following 'yes', or  'true', or 't', or  'y', or  '1'\) are also accepted as True. And, 'no', 'false', 'f', 'n', '0' are accepted as False
- `-s, --score_disease`: Only select rows with a gene to disease association score above the given number \(default is `0.81`\).
- `-c, --conf_gene`: Only select rows with a miRNA to gene association confidence above the given number \(default is `81`\).
- `-sm, --miRNA_partial`: Find all miRNAs containing the provided string in the name.
- `-sd, --disease_partial`: Find all diseases containing the provided string in the name.

### Examples

1. Find diseases associated with a specific miRNA with a gene to disease score above 95 and miRNA to gene confidence above 0.9

- With both the score and the confidence:

python command_line.py -m hsa-miR-6088 -sb True -cb True -s 0.9 -c 95

| diseaseName                                                | Gene   |   score |   confidence |
|:-----------------------------------------------------------|:-------|--------:|-------------:|
| Deafness, Autosomal Recessive 37                           | MYO6   |     0.9 |      96.1381 |
| Deafness, autosomal dominant nonsyndromic sensorineural 22 | MYO6   |     0.9 |      96.1381 |

- Does not print the score nor the confidence

python command_line.py -m hsa-miR-6088  -s 0.9 -c 95

| diseaseName                                                | Gene   |
|:-----------------------------------------------------------|:-------|
| Deafness, Autosomal Recessive 37                           | MYO6   |
| Deafness, autosomal dominant nonsyndromic sensorineural 22 | MYO6   |

2. Find miRNAs associated with a specific disease. As done above, the program will print or not the score and confidence depending on the user-input(in this instance the scores, and confidence are both printed):

python command_line.py -d "CARDIOMYOPATHY, DILATED, 1HH" -sb True -cb True -s 0.9 -c 90
yes disease CARDIOMYOPATHY, DILATED, 1HH

| miRNA           | Gene   |   score |   confidence |
|:----------------|:-------|--------:|-------------:|
| hsa-let-7a-2-3p | BAG3   |     0.9 |      90.9806 |
| hsa-let-7g-3p   | BAG3   |     0.9 |      90.9806 |
| hsa-miR-646     | BAG3   |     0.9 |      93.9651 |
| hsa-miR-891b    | BAG3   |     0.9 |      97.3996 |

3. Find miRNAs with partial name matching:

python command_line.py -sm 266

| Matches         |
|:----------------|
| hsa-miR-1266-5p |
| hsa-miR-4266    |
| hsa-miR-1266-3p |

4. Find diseases with partial name matching:

python command_line.py -sd rett

| Matches       |
|:--------------|
| Rett Syndrome |

### Output

The script outputs a Markdown table with relevant associations based on your query. An Exception is raised in case no associations are found, or the input is inserted incorrectly.

