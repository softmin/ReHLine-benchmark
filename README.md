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
benchopt run . -d classification_data --max-runs 10 --n-repetitions 10
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
benchopt run . -d classification_data --max-runs 10 --n-repetitions 10
```

### Elastic net regularized quantile regression (QR)

Running the QR benchmarks requires the CVXPY package
and the R software. It would be easier to operate
within a Conda environment.

```bash
pip install cvxpy
conda install r-base r-rcpp r-rcppeigen rpy2 -c conda-forge
R -e "chooseCRANmirror(ind = 1); install.packages(c('hqreg'))"
```

Additionally, in order to include the 'CPLEX' and 'GUROBI' commercial solvers, you will need to install the following two PyPI packages:
```bash
pip install gurobipy cplex
```
Due to the use of these two commercial solvers, the Community Edition or Restricted license is being used here. You may encounter the following errors:

> **CPLEX**: CPLEX Error 1016 - Community Edition. Problem size limits have been exceeded. Please purchase a license at http://ibm.biz/error1016.
>
> **GUROBI**: Restricted license - for non-production use only - expires 2024-10-28.

Please visit http://ibm.biz/error1016 to update your CPLEX license. Additionally, for GUROBI, please check the ARGUMENT 'env' which allows for the passage of a Gurobi Environment, specifying parameters and license information. You can find further information regarding the placement of the Gurobi license file 'gurobi.lic' at https://support.gurobi.com/hc/en-us/articles/360013417211-Where-do-I-place-the-Gurobi-license-file-gurobi-lic.

*PS: We use `reg_sim` data to demonstrate that the free version of the two solvers has a very limited capacity to handle data scales.*

In addition, we also test the R implementation of
ReHLine. Use the following commands to download
the source package and install it.

```
curl -L -O https://github.com/softmin/ReHLine-r/archive/refs/heads/main.zip
unzip main.zip
R CMD INSTALL ReHLine-r-main
```

To run all benchmarks available, enter the QR directory and use the following command:

```bash
cd benchmark_QR
benchopt run . -d reg_data  --max-runs 10 --n-repetitions 10
```

There are also some simulated data sets available:

```bash
benchopt run . -d reg_sim
```

### Ridge regularized Huber minimization

The dependencies are the same as those in the QR subsection.

To run all benchmarks available, enter the Huber directory and use the following command:

```bash
cd benchmark_Huber
benchopt run . -d reg_data  --max-runs 10 --n-repetitions 10
```

### FairSVM

(To be completed)

```bash
pip install cvxpy dccp
```

```bash
benchopt run . -d classification_data
benchopt run . -d classification_sim
```
