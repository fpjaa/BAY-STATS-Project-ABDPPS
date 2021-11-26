
    data {
        int<lower=0> p;
        int<lower=0> n;
        matrix[n, p] X;
        matrix[n, 1] y;
    }
    
    parameters {
        real<lower=0> tau;
        real alpha;
        vector[p] beta;
        real sigma;
        vector<lower=0>[p] lambda;
    }
    
    transformed parameters {
        vector[n] mean = X * beta + alpha;
    }
    
    model {
        tau ~ cauchy(0, 1);
        sigma ~ lognormal(0, 3);
        alpha ~ normal(9, 2);
        lambda ~ cauchy(0, 1);
        beta ~ normal(0, tau * lambda);
        y ~ normal(mean, sigma);
    }

