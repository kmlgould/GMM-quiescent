def calc_qprob(cat):
    
    # given NUVU, UV, VJ colours for a catalog (and their errors), calculate the boot strapped
    # quiescent probabilities based on the gaussian mixture model 

    NUV = cat['rest121']
    U = cat['restU']
    V = cat['restV']
    J = cat['restJ']

    NUVerr = cat['rest121_err']
    Uerr = cat['restU_err']
    Verr = cat['restV_err']
    Jerr = cat['restJ_err']

    # First we set the parameters of the program:

    N_exp = 1000           # Number of "experiments" (i.e. drawing from random distributions)
    r = np.random
    r.seed(42)

    prob_q = np.zeros([len(NUV),5])
    prob_all = []

    for n,(nuv,nuverr,u,uerr,v,verr,j,jerr) in enumerate(zip(NUV, NUVerr, U,Uerr,V,Verr,J,Jerr)):
    # create 1000 u,v,j, NUV values for each galaxy based on its u,v,j, NUV and errors, assuming gaussian d. 


        nuvdata = r.normal(nuv,nuverr,N_exp)
        udata = r.normal(u,uerr,N_exp)
        vdata = r.normal(v,verr,N_exp)
        jdata = r.normal(j,jerr,N_exp)

        # recalculate colours 

        nuvu = -2.5*np.log10(nuvdata/udata)
        uv = -2.5*np.log10(udata/vdata)
        vj = -2.5*np.log10(vdata/jdata)

        if np.sum(np.isnan(nuvu)) or np.sum(np.isnan(uv)) or np.sum(np.isnan(vj)):

            prob_q[n,:] = [-99,-99,-99,-99,-99]

        else: 

            X_t = np.array([np.array(vj),np.array(uv),np.array(nuvu)]).T
            with open('colours_model-v4.0.pkl', 'rb') as f:
                gmm = pickle.load(f) 
                
            zscore_t = gmm.predict_proba(X_t)


            group1_t = zscore_t.T[0]
            group2_t = zscore_t.T[1]
            group3_t = zscore_t.T[2]
            group4_t = zscore_t.T[3]
            group5_t = zscore_t.T[4]
            group6_t = zscore_t.T[5]

            pc = np.percentile(group4_t,q=(5,16,50,84,95))

            prob_q[n,:] = pc # add to 2d array of Lxn [N,1000] where N = len(data)  
            
            prob_all.append(group3_t)

    cat['p(q)_5'] = prob_q[:,0]
    cat['p(q)_16'] = prob_q[:,1]
    cat['p(q)_50'] = prob_q[:,2]
    cat['p(q)_84'] = prob_q[:,3]
    cat['p(q)_95'] = prob_q[:,4]
    cat['p(q)_whole'] = prob_all
    #cat['p(q)_whole'] = group3_t
    return cat 
