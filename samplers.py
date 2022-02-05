import subprocess
import numpy as np


#########################
# 
# MC_sample_Z
#
#########################

def MC_sample_Z(Z, W, Theta, B, E, C, debug=False):  # D, k are global variables
    
    # Retrieving dimensions from input matrices 
    D, V = W.shape
    k = B.shape[0]
    
    for d in range(D):
        for v in range(V):
            I_di = int(W[d, v])
            for j in range(I_di):
                
                #We are in the instance of a word
                z_hat = int(Z[d, v, j])
                
                if z_hat != -1:  # Bug fix: Took invalid topics and assigned them
                
                    E[d, z_hat] = max(0, E[d, z_hat]-1)

                    C[z_hat, v] = max(0, C[z_hat, v]-1)

                    Rho = []  # Needs to start from zero to have the interval to fall into topic 1
                    Rho_z = 0
                    #Rho.append(Rho_z)

                    for z in range(k):
                        # Compute the denominator sum
                        C_vk = 0
                        for b in range(V):
                            if b != v:
                                C_vk += C[z, b]
                        # Compute the upper limits of the topic probabilities
                        d_part = E[d, z] + Theta[d, z]
                        z_part = C[z, v] + B[z, v]
                        denom = C_vk + V * B[z, v]
                        prob = d_part * z_part / denom
                        if isinstance(prob, float):  # Check NaN
                            Rho.append(prob)
                        else:
                            Rho.append(Rho_z)
                        
                        if debug and not isinstance(prob, float):  # NaN
                            print('E='+str(E[d, z])+', Theta='+str(Theta[d, z])+', d part is '+str(d_part))
                            print('C='+str(C[z, v])+', B='+str(B[z, v])+', z part is '+str(z_part)+', Cb='+str(C_vk)+', denom is '+str(denom))
                        
                    Rho = Rho / np.sum(Rho, axis=0)
                       
                    z_hat = np.random.choice(k, 1, p=Rho)

                    E[d, z_hat] += 1
                    C[z_hat, v] += 1
                    Z[d, v, j] = z_hat
                  
    # Note that we directly modify Z since the update per topic helps for the next iteration 
    return Z, E, C


#########################
# 
# MC_sample_B
#
#########################

def MC_sample_B(alpha, C):
    # B, C are (k, V) -> Generate k vectors
    B = np.random.dirichlet(alpha + C[0,:], size=1)  # Topic 0
    for i in range(C.shape[0]-1):  # Go through topics: Fix is excluding topic 0 already generated
        B = np.concatenate((B, np.random.dirichlet(alpha + C[i+1,:], size=1)), axis=0)
    return B



#########################
# 
# MC_sample_H
#
#########################

# Argument of the exponential in the kernel numerator
def log_kernel_numerator(eta, K, E):
    k = eta.shape[0]
    eta_K_eta = -0.5 * (eta.dot(K)).dot(eta)
    E_eta = E.dot(eta)
    return eta_K_eta + E_eta

# Kernel denominator
def sum_eta(eta):
    #k = eta.shape[0]
    sum_eta = np.sum(np.exp(eta))
    return sum_eta


def MC_sample_H(E, Sigma, K, H_current=None, step_size=0.125, adaptive_step_ratio=1.5, adaptive_step_threshold=0.44, max_step=0.25, burn_in=0, seed=None):
    
    np.random.seed(seed)
        
    D, k = E.shape  # Number of documents, Number of topics
    
    if H_current is None:
        H_current = np.zeros((D, k))
        
    mean = np.zeros((k,))
    Cov = step_size * np.identity(k)
    acceptance_counter = 0
    
    for d in range(D):  # Iterating over each document
        
        E_d = E[d]
        
        current_eta = H_current[d]
        
        #Other option:           
        proposed_eta = np.random.multivariate_normal(current_eta, Cov)

        #Logarithm of the kernel numerator
        lkn_proposed_eta = log_kernel_numerator(proposed_eta, K, E_d)
        lkn_current_eta = log_kernel_numerator(current_eta, K, E_d)

        #Logarithm of the kernel denominator
        lkd_proposed_eta = k * np.log(sum_eta(proposed_eta))
        lkd_current_eta = k * np.log(sum_eta(current_eta))

        #Logarithm of the proportion
        log_p_proportion = (lkn_proposed_eta + lkd_current_eta) - (lkd_proposed_eta + lkn_current_eta)

        alpha = min(0, log_p_proportion)

        if np.log(np.random.uniform(0.0, 1.0)) < alpha:
            acceptance_counter += 1
            current_eta = proposed_eta

        H_current[d] = current_eta
    
    if acceptance_counter / D < adaptive_step_threshold:  # Acceptance rate too low, decreasing the step
        step_size /= adaptive_step_ratio
    else:  # Acceptance rate high, increasing the step
        step_size = min(step_size * adaptive_step_ratio, max_step) 
    
    return H_current, step_size


#########################
# 
# MC_sample_GK
#
#########################

# Functions used to serialize and deserialize matrices between python and R
def serialize_matrix(m):
    if len(m.shape) != 2:
        raise Exception("Can not serialize ill-shaped matrix!")
    res = '\n'.join(' '.join(str(entry) for entry in row)  # Space between entries, newline between rows
                     for row in m)
    return '"' + res + '"'


def deserialize_matrix(line, shape, separator=' '):
    return np.fromstring(line, sep=separator).reshape(shape)


def MC_sample_GK(G, H, degrees_of_freedom_b, debug=False):
    size = G.shape[0]
    n = H.shape[0]
    
    # Serialize the inputs
    G = serialize_matrix(G)
    
    # Transform H into the BDGraph data matrix
    data_matrix = H.T.dot(H)
    data_matrix = serialize_matrix(data_matrix)
    
    # call R script using python.subprocess
    # The parameter order is: deg.of freedom b, 
    #                         number of data samples (documents) n, 
    #                         graph adjacency matrix G, 
    #                         data matrix,
    #                         debug ("TRUE" or "FALSE"), 
    command = f"Rscript --vanilla bdmcmc.R {degrees_of_freedom_b} {n} {G} {data_matrix} {'TRUE' if debug else 'FALSE'}"
    result = subprocess.run(command, 
                            shell=True, 
                            capture_output=True,
                            text=True)
    
    if result.returncode != 0:  # Something went wrong
        print(result.stdout)
        print(result.stderr)
        raise Exception("Rscript error! Check the previous logs for more details")
    
    if debug:
        print(result.stdout)
    
    # The last two lines of the R output MUST be the sampled matrices
    lines = result.stdout.rsplit('\n', 3)  # Split only the last three lines  https://www.w3schools.com/python/ref_string_rsplit.asp
    waiting_time = float(lines[-3])  # 3rd from the end
    G = deserialize_matrix(lines[-2], shape=(size, size))  # Line before last
    K = deserialize_matrix(lines[-1], shape=(size, size))  # Last line
    return waiting_time, G, K