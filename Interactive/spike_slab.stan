
    data {
        int<lower=0> p;
        int<lower=0> n;
        matrix[n, p] X;
        vector[n] y;
    }
    
    parameters {
        real alpha;
        vector[p] beta;
        real<lower=0> sigma;
    }
    
    transformed parameters {
        vector[n] mean = X * beta + alpha;
    }
    
    model {
        sigma ~ lognormal(0, 3);
        alpha ~ normal(9, 2);
        target += log_mix(0.5, 
                normal_lpdf(beta | 0, 0.1), 
                normal_lpdf(beta | 0, 10));
        //for (i in 1:p) {
          //  target += log_mix(0.5, 
            //    normal_lpdf(beta[i] | 0, 0.1), 
              //  normal_lpdf(beta[i] | 0, 10));
       // }
        y ~ normal(mean, sigma);
    }

