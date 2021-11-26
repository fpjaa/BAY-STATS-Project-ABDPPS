
    data {
        int<lower=0> D;
        int<lower=0> k;
        int E[D, k];
        matrix[k, k] Sigma;
        vector[k] mu;
    }
    
    parameters {
        matrix[D, k] H;
    }
    
    transformed parameters {
        matrix[D, k] Theta;
        for (i in 1:D) {
            Theta[i] = to_row_vector(softmax(to_vector(H[i])));
        }
    }
    
    model {
        int u;
        for (i in 1:D){
            H[i] ~ multi_normal(mu, Sigma);  
            E[i] ~ multinomial(Theta[i]);
        }

    }

