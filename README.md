## Workflow

For all benchmarks, it is necessary to install the following packages.

```bash
pip install benchopt scikit-learn
```

Then each problem has its own dependencies,
described in each subsection.

### SVM

For the SVM task, you also need to install the
[CVXPY](https://www.cvxpy.org/) package:

```bash
pip install cvxpy[MOSEK]
```

The command above will also install the commercial
[MOSEK](https://www.mosek.com/) solver, but you
still need a license to use it.

Follow the [MOSEK website](https://www.mosek.com/resources/getting-started/)
to obtain a license. For students and professors at a university, the
[academic license](https://www.mosek.com/products/academic-licenses/)
is also available. Once you get a license, follow the
[instructions](https://docs.mosek.com/latest/licensing/quickstart.html#local)
to install it on your machine.

To run all benchmarks available, enter the SVM directory and use the following command:

```bash
cd benchmark_SVM
benchopt run . -d classification_data
```

To gather more repetitions, add the following options:

```bash
benchopt run . -d classification_data --n-repetitions 10 --timeout 1000
```

To run the benchmark for a specific solver and data set,
add the corresponding parameters. For example:

```bash
benchopt run . -d classification_data[dataset_name="steel-plates-fault"] -s rehline
```

The command above then only tests the ReHLine solver on the `steel-plates-fault` data set.

### Smoothed SVM (sSVM)

Running sSVM benchmarks require the following additional package:

```bash
pip install sklearn-contrib-lightning
```

And the running commands are similar to those in the SVM subsection.

```bash
cd benchmark_sSVM
benchopt run . -d classification_data --n-repetitions 10 --timeout 1000
```

### Ridge regularized Huber minimization

Running the Huber benchmarks requires the [CVXPY](https://www.cvxpy.org/) package
and the R software. It would be easier to operate
within a Conda environment.

```bash
pip install cvxpy[MOSEK]
conda install r-base rpy2 -c conda-forge
R -e "chooseCRANmirror(ind = 1); install.packages(c('hqreg'))"
```

Also see the SVM subsection for the configuration of the
[MOSEK](https://www.mosek.com/) commercial solver.

To run all benchmarks available, enter the Huber directory and use the following command:

```bash
cd benchmark_Huber
benchopt run . -d reg_data --n-repetitions 10 --timeout 1000
```

### Elastic net regularized quantile regression (QR)

First follow the Huber subsection to install the
dependencies there.
Additionally, in order to include the
[CPLEX](https://www.ibm.com/products/ilog-cplex-optimization-studio)
and [Gurobi](https://www.gurobi.com/)
commercial solvers, you will need to install the following two PyPI packages:

```bash
pip install gurobipy cplex
```

Due to the use of these two commercial solvers, the Community Edition or Restricted license is being used here. You may encounter the following errors:

> **CPLEX**: CPLEX Error 1016 - Community Edition. Problem size limits have been exceeded. Please purchase a license at http://ibm.biz/error1016.
>
> **GUROBI**: Restricted license - for non-production use only - expires 2024-10-28.

Please visit http://ibm.biz/error1016 to update your CPLEX license. Additionally, for GUROBI, please check the ARGUMENT 'env' which allows for the passage of a Gurobi Environment, specifying parameters and license information. You can find further information regarding the placement of the Gurobi license file `gurobi.lic` at https://support.gurobi.com/hc/en-us/articles/360013417211-Where-do-I-place-the-Gurobi-license-file-gurobi-lic.

*PS: We use `reg_sim` data to demonstrate that the free version of the two solvers has a very limited capacity to handle data scales.*

Finally, we also test the R implementation of
ReHLine. Use the following commands to download
the source package and install it.

```bash
conda install r-rcpp r-rcppeigen -c conda-forge
curl -L -O https://github.com/softmin/ReHLine-r/archive/refs/heads/main.zip
unzip main.zip
R CMD INSTALL ReHLine-r-main
```

To run all benchmarks available, enter the QR directory and use the following command:

```bash
cd benchmark_QR
benchopt run . -d reg_data --n-repetitions 10 --timeout 1000
```

There are also some simulated data sets available:

```bash
benchopt run . -d reg_sim
```

### FairSVM

Following the Huber and QR subsections, first install
[CVXPY](https://www.cvxpy.org/) with commercial solvers
[MOSEK](https://www.mosek.com/),
[CPLEX](https://www.ibm.com/products/ilog-cplex-optimization-studio),
and [Gurobi](https://www.gurobi.com/):

```bash
pip install cvxpy[MOSEK] gurobipy cplex
```

We also include the original implementation of
[FairSVM](https://github.com/mbilalzafar/fair-classification)
based on the
[DCCP](https://github.com/cvxgrp/dccp) package:

```bash
pip install dccp==1.0.3
```

Note that we explicitly specify the version of DCCP, since otherwise
the installation may encounter errors.
The file `benchmark_FairSVM/fair_classification/linear_clf_pref_fairness.py`
is derived from the original
[FairSVM](https://github.com/mbilalzafar/fair-classification) repository,
with slight modifications for software compatibility.

To run all benchmarks available, enter the FairSVM directory and use the following command:

```bash
cd benchmark_FairSVM
benchopt run . -d classification_data --n-repetitions 10 --timeout 1000
```

There are also some simulated data sets available:

```bash
benchopt run . -d classification_sim
```

## Overall benchmarks

Assuming all dependencies are properly installed,
the following commands are used to generate benchmark results in the article:

```bash
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
```