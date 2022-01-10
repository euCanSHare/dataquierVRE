# Usage basic test


### RUNNER execution with test data
- Run the test as if VRE initiated the job 
```bash
cd tests/basic/
./test_VRE_RUNNER.sh
```
- See the results in `run000` folder.


### Direct App execution (docker-based)
- Run the App wrapped in the RUNNER for debugging
```bash
cd tests/basic/
docker run -v $PWD:/shared_volume  --workdir /shared_volume/run000/ -u root lcodo/dataquier Rscript $PWD/../../AssessDataQuality/dataquieR.R /shared_volume/study_data.xlsx XLSX /shared_volume/meta_data.xlsx XLSX LABEL checks=/shared_volume/checks.xlsx checks_file_type=XLSX code_labels=/shared_volume/code_labels.xlsx code_labels_file_type=XLSX
```
- See the results in `run000` folder.
