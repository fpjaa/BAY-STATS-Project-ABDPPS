
    data {
        int<lower=0> d;
        int<lower=0> tau;
    }
    
    parameters {
        vector[d] x;
        vector[d] lambda;
    }
    
    transformed parameters {
        vector[d] sigma;
        for (j in 1:d) {
            sigma[j] = tau^2 * lambda[j]^2;
        }
    }
    
    model {
        for (j in 1:d) {
            x[j] ~ normal(0.0, sigma[j]);
            lambda[j] ~ cauchy(0.0, 1.0);
        }
    }

