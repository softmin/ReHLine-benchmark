cd benchmark_SVM
benchopt run . -d classification_data --n-repetitions 10 --timeout 1000

cd ../benchmark_sSVM
benchopt run . -d classification_data --n-repetitions 10 --timeout 1000

cd ../benchmark_Huber
benchopt run . -d reg_data --n-repetitions 10 --timeout 1000

cd ../benchmark_QR
benchopt run . -d reg_data --n-repetitions 10 --timeout 1000

cd ../benchmark_FairSVM
benchopt run . -d classification_data --n-repetitions 10 --timeout 1000
