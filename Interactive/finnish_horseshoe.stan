
    data {
        int<lower=0> d;
        real<lower=0> tau;
    }
    
    parameters {
        vector[d] x;
        vector[d] lambda;
        real c;
    }
    
    transformed parameters {
        vector[d] sigma;
        for (j in 1:d) {
            sigma[j] = (lambda[j]^2 * c^2) / (tau ^2 * lambda[j]^2 + c^2);
        }
    }
    
    model {
        for (j in 1:d) {
            x[j] ~ normal(0.0, sigma[j]);
            lambda[j] ~ cauchy(0.0, 1.0);
            c ~ inv_gamma(1.5, 1.5);
        }
    }

