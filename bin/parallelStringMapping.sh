#!/bin/bash
#SBATCH --job-name=mapping
#SBATCH --mail-user=evonne.mcarthur@vanderbilt.edu
#SBATCH --mail-type=FAIL
#SBATCH --time=1-00:00:00
#SBATCH --nodes=1
#SBATCH --mem=2G
#SBATCH --begin=6:00:00
#SBATCH --output=tmp/mapping_%a.out
#SBATCH --array=0-84

i=$SLURM_ARRAY_TASK_ID
start=$(($i * 1000))
end=$(($start + 1000))

source activate hpo

python mapping.py -f hpo -t ICD9 -m string -i "$start"-"$end" -o ./intermediate/
python mapping.py -f hpo -t ICD10 -m string -i "$start"-"$end" -o ./intermediate/
python mapping.py -f hpo -t phecode1.2 -m string -i "$start"-"$end" -o ./intermediate/
python mapping.py -f hpo -t phecodeX -m string -i "$start"-"$end" -o ./intermediate/
python mapping.py -f hpo -t phecodeXupdated -m string -i "$start"-"$end" -o ./intermediate/

python mapping.py -f hpo -t ICD9 -m substring -i "$start"-"$end" -o ./intermediate/
python mapping.py -f hpo -t ICD10 -m substring -i "$start"-"$end" -o ./intermediate/
python mapping.py -f hpo -t phecode1.2 -m substring -i "$start"-"$end" -o ./intermediate/
python mapping.py -f hpo -t phecodeX -m substring -i "$start"-"$end" -o ./intermediate/
python mapping.py -f hpo -t phecodeXupdated -m substring -i "$start"-"$end" -o ./intermediate/

python mapping.py -f hpo -m wikimed -i "$start"-"$end" -o ./intermediate/ 

python mapping.py -f ICD9 -t hpo -m substring -i "$start"-"$end" -o ./intermediate/
python mapping.py -f ICD10 -t hpo -m substring -i "$start"-"$end" -o ./intermediate/
python mapping.py -f phecode1.2 -t hpo -m substring -i "$start"-"$end" -o ./intermediate/
python mapping.py -f phecodeX -t hpo -m substring -i "$start"-"$end" -o ./intermediate/
python mapping.py -f phecodeXupdated -t hpo -m substring -i "$start"-"$end" -o ./intermediate/
