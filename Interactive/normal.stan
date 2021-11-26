
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
        real<lower=0> sigma;
    }
    
    transformed parameters {
        vector[n] mean = X * beta + alpha;
    }
    
    model {
        tau ~ cauchy(0, 1);
        sigma ~ lognormal(0, 3);
        beta ~ normal(0, tau);   
        alpha ~ normal(9, 2);
        for (i in 1:n){
            y[i] ~ normal(mean[i], sigma);
        }
    }

