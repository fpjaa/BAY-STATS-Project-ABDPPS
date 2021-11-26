
    data {
        int<lower=0> p;
        int<lower=0> n;
        matrix[n, p] X;
        vector[n] y;
    }
    
    parameters {
        real<lower=0> tau;
        real alpha;
        vector[p] beta;
        real sigma;
        vector<lower=0>[p] lambda;
        vector<lower=0>[p] lambda_t2;

    }
    
    transformed parameters {
        vector[n] mean = X * beta + alpha;
    }
    
    model {
    c ~ inv_gamma(1.5, 1.5);
        tau ~ cauchy(0, 1);
        sigma ~ lognormal(0, 3);
        alpha ~ normal(9, 2);
        for (i in 1:p) {
            lambda[i] ~ cauchy(0, 1);
            lambda_t2[i] = (square(c*lambda[i]))/(square(c) + square(tau*lambda[i]))
            beta[i] = normal(0, square(tau*lambda[i]));
    }
        y ~ normal(mean, sigma);
    }

